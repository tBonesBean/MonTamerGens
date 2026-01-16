"""
MonsterSeed is a canonical, encyclopedic definition of a monster species.
It is discovered through exploratory RNG, using randomness as a creative tool.
Once accepted into the catalog, a MonsterSeed becomes the authoritative source
that defines the fixed identity and constrained possibility space for all of its
future MonsterInstances.
"""

import random
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple, Union

from .data.data import (
    BASE_STATS,
    FORMS_BY_TYPE,
    HELD_ITEMS,
    INCOMPATIBLE_TYPE_PAIRS,
    MAJOR_MODS,
    PHYSICAL_TRAITS,
    SEED_TYPES,
    SEED_TYPES_WEIGHTED,
    SEED_TYPE_DATA,
    TEMPERS_COUPLED,
    TYPE_SYNERGY_BOOSTS,
    UTILITY_MODS,
)

ChoiceList = Union[Mapping[Any, float], Iterable[Tuple[Any, float]]]


def weighted_choice(choices_with_weights: ChoiceList):
    """Selects an item from a weighted list of choices.

    Args:
        choices_with_weights: A dictionary mapping choices to weights or an iterable
                              of (choice, weight) tuples.

    Returns:
        The selected item.

    Raises:
        ValueError: If the choice list is empty, a weight is non-numeric or negative,
                    or the total weight is not positive.
        RuntimeError: If an item fails to be selected due to a floating point edge case.
    """
    if isinstance(choices_with_weights, dict):
        items_weights = list(choices_with_weights.items())
    else:
        items_weights = list(choices_with_weights)

    if not items_weights:
        raise ValueError("weighted_choice: empty choices")

    total = 0.0
    normalized = []
    for item, w in items_weights:
        # Support weights provided directly as numbers or as dicts containing a 'weight' key.
        if isinstance(w, dict):
            if "weight" in w:
                w = w["weight"]
            else:
                raise ValueError(
                    f"weighted_choice: weight for {item!r} is not numeric: {w!r}"
                )
        try:
            w = float(w)
        except Exception:
            raise ValueError(
                f"weighted_choice: weight for {item!r} is not numeric: {w!r}"
            )
        if w < 0:
            raise ValueError(f"weighted_choice: negative weight for {item!r}: {w}")
        normalized.append((item, w))
        total += w

    if total <= 0:
        raise ValueError("weighted_choice: total weight must be > 0")

    r = random.random() * total
    upto = 0.0
    for item, weight in normalized:
        upto += weight
        if r < upto:
            return item

    # Shouldn't happen, but be explicit
    raise RuntimeError(
        "weighted_choice: failed to select an item (floating point edge-case)"
    )


def rarity_to_weight(rarity_val: Any, alpha: float = 1.0) -> float:
    """Convert a rarity value into a sampling weight (rarer -> lower weight)."""
    try:
        r = float(rarity_val)
    except Exception:
        r = 1.0
    r = max(r, 1e-6)
    return 1.0 / (r ** float(alpha))


def choose_type_pair(
    primary_type_override: Optional[str] = None,
    secondary_chance: float = 0.65,
) -> Tuple[str, Optional[str]]:
    """Selects a primary and optional secondary type, respecting weights and rules.

    Args:
        primary_type_override: If provided, this primary type is used instead of a random one.
        secondary_chance: The probability of attempting to add a secondary type.

    Returns:
        A tuple containing the primary type and an optional secondary type.
    """
    # Primary type selection (use override or pick by weighted chance)
    primary_type = (
        primary_type_override
        if primary_type_override
        else weighted_choice(SEED_TYPES_WEIGHTED)
    )

    # Quickly decide not to include secondary
    if random.random() > secondary_chance:
        return primary_type, None

    # Build candidate pool respecting incompatibilities and synergy modifiers
    candidates: Dict[str, float] = {}
    for t in SEED_TYPES:
        if t == primary_type:
            continue
        if frozenset([primary_type, t]) in INCOMPATIBLE_TYPE_PAIRS:
            continue

        base_weight = SEED_TYPES_WEIGHTED.get(t, 1.0)
        synergy_mult = TYPE_SYNERGY_BOOSTS.get(frozenset([primary_type, t]), 1.0)
        candidates[t] = base_weight * synergy_mult

    if not candidates:
        return primary_type, None

    secondary_type = weighted_choice(candidates)
    return primary_type, secondary_type


@dataclass
class MonsterSeed:
    """A deterministic intent snapshot used to generate a monster.
        Contains biases, constraints, and semantic identity — not final results.

    Attributes:
        idnum: Deterministic identifier for generation/tracking.
        name: Human-facing (or deterministic) name; empty string until named.
        form: Canonical form/species.
        primary_type: The primary type of the monster.
        secondary_type: The optional secondary type of the monster.
        stats: Calculated numeric stats (HP, ATK, DEF, etc.).
        mutagens: Mutagens / modifiers applied at forge-time.
        habitat: Habitat selection.
        physical_traits: List of physical trait keys.
        held_item: Optional held item.
        tempers: Temper dispositions (mood, affinity, etc.).
        meta: Meta information computed from types / mods (tags, resistances, weak).
    """

    idnum: int
    name: str
    form: str
    primary_type: str
    secondary_type: Optional[str]
    stats: Dict[str, int]
    mutagens: Dict[str, List[str]]
    habitat: str
    physical_traits: List[str]
    held_item: Optional[str]
    tempers: Dict[str, str]
    meta: Dict[str, Any]

    @classmethod
    def forge(
        cls,
        idnum: int,
        primary_type: Optional[str] = None,
        secondary_type: Optional[str] = None,
        secondary_chance: float = 0.65,
    ) -> "MonsterSeed":
        """Factory method to create a new, properly biased MonsterSeed.
            This method orchestrates the initial creation of a monster, including
            selecting its species, habitat, traits, and calculating its base stats
            and meta attributes based on its types.

        Args:
            idnum: The ID number for the new monster.
            primary_type: The primary type of the monster. If None, a random one is chosen.
            secondary_type: The secondary type of the monster. If None, one might be chosen based on `secondary_chance`.
            secondary_chance: The probability of adding a secondary type if one is not provided.

        Returns:
            A new, fully-formed MonsterSeed object.
        """
        # Choose valid primary/secondary pair if not fully specified
        if primary_type is None or (primary_type and secondary_type is None):
            chosen_primary, chosen_secondary = choose_type_pair(
                primary_type, secondary_chance
            )
            # If caller specified a primary explicitly, keep it (choose_type_pair already respects override).
            primary_type = chosen_primary if primary_type is None else primary_type
            secondary_type = (
                secondary_type if secondary_type is not None else chosen_secondary
            )

        # Validate provided types
        if primary_type not in SEED_TYPES:
            raise ValueError(f"Unknown primary_type: {primary_type!r}")
        if secondary_type:
            if secondary_type not in SEED_TYPES:
                raise ValueError(f"Unknown secondary_type: {secondary_type!r}")
            if secondary_type == primary_type:
                raise ValueError(
                    "Secondary type cannot be the same as the primary type."
                )
            if frozenset([primary_type, secondary_type]) in INCOMPATIBLE_TYPE_PAIRS:
                raise ValueError(
                    f"Incompatible type pairing: {primary_type} and {secondary_type}"
                )

        # Deterministic selection steps (using weighted_choice)
        # Forms can be defined either inside SEED_TYPE_DATA per-type under 'forms',
        # or in the legacy FORMS_BY_TYPE mapping (type_forms.yaml). Support both.

        forms_raw = SEED_TYPE_DATA.get(primary_type, {}).get(
            "forms"
        ) or FORMS_BY_TYPE.get(primary_type, [])
        if isinstance(forms_raw, dict):
            form = weighted_choice(forms_raw)
        else:
            # assume a simple list of names
            form = random.choice(forms_raw) if forms_raw else "Unknown"

        # Habitats are now provided by SEED_TYPE_DATA per-type under the 'habitats' key.
        habitats_raw = SEED_TYPE_DATA.get(primary_type, {}).get("habitats", {})
        if isinstance(habitats_raw, dict):
            habitat = weighted_choice(habitats_raw)
        else:
            if isinstance(habitats_raw, list):
                habitat = random.choice(habitats_raw) if habitats_raw else "Generic"
            else:
                habitat = habitats_raw or "Generic"

        # Select mutagens using their configured rarity weights (prefer rarer mods less)
        # Both MAJOR_MODS and UTILITY_MODS are dicts mapping mod-name -> metadata dict,
        # where the 'rarity' key is used as the selection weight (default 1.0).
        # Filter mods by allowed_types (if present) so selected mods are thematically appropriate.
        def _mod_allowed(mod: dict, primary: str, secondary: Optional[str]) -> bool:
            allowed = mod.get("allowed_types")
            if allowed is None or len(allowed) == 0:
                allowed_ok = True
            else:
                allowed_ok = (primary in allowed) or (
                    secondary in allowed if secondary else False
                )
            if not allowed_ok:
                return False

            incompatible = mod.get("incompatible_types", []) or []
            if primary in incompatible:
                return False
            if secondary and secondary in incompatible:
                return False

            return True

        major_weights = {
            name: rarity_to_weight(mod.get("rarity", 1.0))
            for name, mod in MAJOR_MODS.items()
            if _mod_allowed(mod, primary_type, secondary_type)
        }
        utility_weights = {
            name: rarity_to_weight(mod.get("rarity", 1.0))
            for name, mod in UTILITY_MODS.items()
            if _mod_allowed(mod, primary_type, secondary_type)
        }

        if not major_weights:
            major_weights = {
                name: rarity_to_weight(mod.get("rarity", 1.0))
                for name, mod in MAJOR_MODS.items()
            }
        if not utility_weights:
            utility_weights = {
                name: rarity_to_weight(mod.get("rarity", 1.0))
                for name, mod in UTILITY_MODS.items()
            }

        major_choice = weighted_choice(major_weights)
        utility_choice = weighted_choice(utility_weights)
        mutagens = {"major": [major_choice], "utility": [utility_choice]}

        mood = weighted_choice(TEMPERS_COUPLED["mood"])
        affinity = weighted_choice(TEMPERS_COUPLED["affinity"])
        tempers = {"mood": mood, "affinity": affinity}

        num_physical = 1 if random.random() < 0.75 else 2
        physical_traits = [
            weighted_choice(PHYSICAL_TRAITS) for _ in range(num_physical)
        ]

        held_item = weighted_choice(HELD_ITEMS) if random.random() < 0.4 else None

        stats = calculate_base_stats(primary_type, secondary_type)
        meta = get_base_meta(primary_type, secondary_type)
        meta.setdefault("notes", [])

        # Name placeholder (will be filled by forge_name)
        name = ""

        seed = cls(
            idnum=idnum,
            name=name,
            form=form,
            primary_type=primary_type,
            secondary_type=secondary_type,
            stats=stats,
            mutagens=mutagens,
            habitat=habitat,
            physical_traits=physical_traits,
            held_item=held_item,
            tempers=tempers,
            meta=meta,
        )

        return seed


def calculate_base_stats(
    primary_type: str, secondary_type: Optional[str]
) -> Dict[str, int]:
    """Calculates base stats for a monster given its primary and secondary types.

    Args:
        primary_type: The primary type of the monster.
        secondary_type: The optional secondary type of the monster.

    Returns:
        A dictionary of the monster's base stats.
    """
    stats = BASE_STATS.copy()
    primary_entry = SEED_TYPE_DATA.get(primary_type, {})
    primary_bias = primary_entry.get("attributes", {})
    for stat, mult in primary_bias.get("mul", {}).items():
        if stat in stats:
            stats[stat] = int(round(stats[stat] * mult))
    for stat, addition in primary_bias.get("add", {}).items():
        if stat in stats:
            stats[stat] += int(round(addition))

    if secondary_type:
        secondary_entry = SEED_TYPE_DATA.get(secondary_type, {})
        secondary_bias = secondary_entry.get("attributes", {})
        for stat, mult in secondary_bias.get("mul", {}).items():
            effective_mult = 1 + ((mult - 1) * 0.5)
            if stat in stats:
                stats[stat] = int(round(stats[stat] * effective_mult))
        for stat, addition in secondary_bias.get("add", {}).items():
            if stat in stats:
                stats[stat] = int(round(stats[stat] + (addition * 0.5)))
    return stats


def get_base_meta(
    primary_type: str, secondary_type: Optional[str]
) -> Dict[str, List[str]]:
    """Gets the base meta tags, resistances, and weaknesses from the monster's types.
    Args:
        primary_type: The primary type of the monster.
        secondary_type: The optional secondary type of the monster.

    Returns:
        A dictionary containing the base meta information (tags, resistances, weaknesses).
    """
    meta: Dict[str, List[str]] = {
        "tags": [],
        "resist": [],
        "weak": [],
        "abilities": [],
        "triggers": [],
    }

    def apply_type_meta(type_name: str, meta_dict: Dict[str, List[str]]):
        type_entry = SEED_TYPE_DATA.get(type_name, {})
        # tags may live directly under the type, under 'meta', or under 'attributes'
        tags = (
            type_entry.get("tags")
            or type_entry.get("meta", {}).get("tags")
            or type_entry.get("attributes", {}).get("tags")
            or []
        )
        for tag in tags:
            if isinstance(tag, str) and tag.startswith("Resist:"):
                meta_dict["resist"].append(tag.split(":", 1)[1])
            elif isinstance(tag, str) and tag.startswith("Weak:"):
                meta_dict["weak"].append(tag.split(":", 1)[1])
            elif isinstance(tag, str) and tag.startswith("Ability:"):
                meta_dict["abilities"].append(tag.split(":", 1)[1])
            elif isinstance(tag, str) and tag.startswith("Trigger:"):
                meta_dict["triggers"].append(tag.split(":", 1)[1])
            else:
                meta_dict["tags"].append(tag)

    apply_type_meta(primary_type, meta)
    if secondary_type:
        apply_type_meta(secondary_type, meta)

    return meta

    @property
    def species(self) -> str:
        """A backward-compatible alias for the `form` attribute.

        Returns:
            The canonical form name of the monster.
        """
        return self.form
