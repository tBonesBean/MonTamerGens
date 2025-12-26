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

# Import generation data from the project's data module
from .data.data import (
    BASE_STATS,
    FORMS_BY_TYPE,
    HABITATS_BY_TYPE,
    HELD_ITEMS,
    INCOMPATIBLE_TYPE_PAIRS,
    MAJOR_MODS,
    PHYSICAL_TRAITS,
    SEED_TYPES,
    SEED_TYPES_WEIGHTED,
    SEEDTYPE_ATTR,
    TEMPERS_COUPLED,
    TYPE_SYNERGY_BOOSTS,
    UTILITY_MODS,
)

ChoiceList = Union[Mapping[Any, float], Iterable[Tuple[Any, float]]]


def weighted_choice(choices_with_weights: ChoiceList):
    """
    Select an item from a weighted list of choices.

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


def choose_type_pair(
    primary_type_override: Optional[str] = None,
    secondary_chance: float = 0.65,
) -> Tuple[str, Optional[str]]:
    """
    Selects a primary and optional secondary type, respecting weights and rules.

    This function chooses a primary type (or takes an override), then with some
    probability attempts to pick a valid secondary type that isn't incompatible
    and takes synergy boosts/penalties into account.

    Returns:
        Tuple(primary_type, secondary_type_or_None)
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
    """
    A deterministic intent snapshot used to generate a monster.
    Contains biases, constraints, and semantic identity — not final results.

    Note: fields are chosen to match how other modules in the project
    (e.g. `forge_name.py`, `mon_forge.py`) expect to interact with a seed.
    """

    # Deterministic identifier for generation/tracking
    idnum: int

    # Human-facing (or deterministic) name; empty string until named
    name: str

    # Canonical species (from FORMS_BY_TYPE)
    species: str

    # Primary / secondary type strings (from SEED_TYPES)
    primary_type: str
    secondary_type: Optional[str]

    # Calculated numeric stats (HP, ATK, DEF, etc.)
    stats: Dict[str, int]

    # Mutagens / modifiers applied at forge-time. Represented as lists of mod keys.
    # Example: {"major": ["Starwarden"], "utility": ["CosmicInterpreter"]}
    mutagens: Dict[str, List[str]]

    # Habitat selection (string)
    habitat: str

    # Physical traits (list of string keys)
    physical_traits: List[str]

    # Optional held item (string)
    held_item: Optional[str]

    # Temper dispositions: mood, affinity, etc.
    tempers: Dict[str, str]

    # Meta information computed from types / mods (tags, resistances, weak)
    meta: Dict[str, Any]

    @classmethod
    def forge(
        cls,
        idnum: int,
        primary_type: Optional[str] = None,
        secondary_type: Optional[str] = None,
        secondary_chance: float = 0.65,
    ) -> "MonsterSeed":
        """
        Factory method to create a new, properly biased MonsterSeed.

        This method orchestrates the initial creation of a monster, including
        selecting its species, habitat, traits, and calculating its base stats
        and meta attributes based on its types.

        Args:
            idnum: A unique identifier for this generation batch.
            primary_type: Optional fixed primary type. If None, chosen from weights.
            secondary_type: Optional fixed secondary type. If None, may be selected.
            secondary_chance: Chance to attempt adding a secondary type when one isn't provided.

        Returns:
            A new MonsterSeed instance with all base attributes generated.

        Raises:
            ValueError: If provided types are invalid / incompatible.
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
        species = weighted_choice(FORMS_BY_TYPE.get(primary_type, {}))
        habitat = weighted_choice(HABITATS_BY_TYPE.get(primary_type, {}))

        # Select mutagens using their configured rarity weights (prefer rarer mods less)
        # Both MAJOR_MODS and UTILITY_MODS are dicts mapping mod-name -> metadata dict,
        # where the 'rarity' key is used as the selection weight (default 1.0).
        major_weights = {
            name: mod.get("rarity", 1.0) for name, mod in MAJOR_MODS.items()
        }
        utility_weights = {
            name: mod.get("rarity", 1.0) for name, mod in UTILITY_MODS.items()
        }
        major_choice = weighted_choice(major_weights)
        utility_choice = weighted_choice(utility_weights)
        mutagens = {"major": [major_choice], "utility": [utility_choice]}

        # Tempers / mood
        mood = weighted_choice(TEMPERS_COUPLED["mood"])
        affinity = weighted_choice(TEMPERS_COUPLED["affinity"])
        tempers = {"mood": mood, "affinity": affinity}

        # Physical traits: 75% chance of 1, otherwise 2
        num_physical = 1 if random.random() < 0.75 else 2
        physical_traits = [
            weighted_choice(PHYSICAL_TRAITS) for _ in range(num_physical)
        ]

        # Held item sometimes
        held_item = weighted_choice(HELD_ITEMS) if random.random() < 0.4 else None

        # Compute base stats and meta
        stats = calculate_base_stats(primary_type, secondary_type)
        meta = get_base_meta(primary_type, secondary_type)
        meta.setdefault("notes", [])

        # Name placeholder (will be filled by forge_name)
        name = ""

        seed = cls(
            idnum=idnum,
            name=name,
            species=species,
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
    """
    Calculates base stats for a monster given its primary and secondary types.

    Applies multipliers and additions defined in SEEDTYPE_ATTR. Secondary type
    effects are applied at reduced effectiveness (50%).
    """
    stats = BASE_STATS.copy()
    primary_bias = SEEDTYPE_ATTR.get(primary_type, {})
    for stat, mult in primary_bias.get("mul", {}).items():
        if stat in stats:
            stats[stat] = int(round(stats[stat] * mult))
    for stat, addition in primary_bias.get("add", {}).items():
        if stat in stats:
            stats[stat] += int(round(addition))

    if secondary_type:
        secondary_bias = SEEDTYPE_ATTR.get(secondary_type, {})
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
    """
    Gets the base meta tags, resistances, and weaknesses from the monster's types.
    """
    meta: Dict[str, List[str]] = {"tags": [], "resist": [], "weak": []}

    def apply_type_meta(type_name: str, meta_dict: Dict[str, List[str]]):
        type_attrs = SEEDTYPE_ATTR.get(type_name, {})
        for tag in type_attrs.get("tags", []):
            if isinstance(tag, str) and tag.startswith("Resist:"):
                meta_dict["resist"].append(tag.split(":", 1)[1])
            elif isinstance(tag, str) and tag.startswith("Weak:"):
                meta_dict["weak"].append(tag.split(":", 1)[1])
            else:
                meta_dict["tags"].append(tag)

    apply_type_meta(primary_type, meta)
    if secondary_type:
        apply_type_meta(secondary_type, meta)

    return meta
