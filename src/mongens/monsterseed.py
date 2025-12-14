"""
Defines the core data structures for monster generation.

This module contains the `MonsterSeed` dataclass, which is the central data
structure representing a monster's generated attributes before final calculations.
It also includes helper functions for creating and manipulating these seeds,
such as `weighted_choice` for random selections and `choose_type_pair` for
generating valid monster type combinations.
"""
from dataclasses import dataclass
import random
from typing import Any, Iterable, List, Tuple, Union

from .data.data import *


ChoiceList = Union[Dict[Any, float], Iterable[Tuple[Any, float]]]


def weighted_choice(choices_with_weights: ChoiceList):
    """Select an item from a weighted list of choices.

    Args:
        choices_with_weights: A dictionary mapping choices to weights or an
            iterable of (choice, weight) tuples.

    Returns:
        The selected item.

    Raises:
        ValueError: If the choice list is empty, a weight is non-numeric
            or negative, or the total weight is not positive.
        RuntimeError: If an item fails to be selected due to a floating
            point edge case.
    """
    if isinstance(choices_with_weights, dict):
        items_weights = list(choices_with_weights.items())
    else:
        items_weights = list(choices_with_weights)

    if not items_weights:
        raise ValueError("weighted_choice: empty choices")

    # Validate weights and compute total
    total = 0.0
    for item, w in items_weights:
        try:
            w = float(w)
        except Exception:
            raise ValueError(
                f"weighted_choice: weight for {item!r} is not numeric: {w!r}"
            )
        if w < 0:
            raise ValueError(f"weighted_choice: negative weight for {item!r}: {w}")
        total += w

    if total <= 0:
        raise ValueError("weighted_choice: total weight must be > 0")

    r = random.random() * total
    upto = 0.0
    for item, weight in items_weights:
        upto += float(weight)
        if r < upto:
            return item

    # Shouldn't happen, but be explicit
    raise RuntimeError(
        "weighted_choice: failed to select an item (floating point edge-case)"
    )

def choose_type_pair(
    primary_type_override: str | None = None,
    secondary_chance: float = 0.65,
) -> tuple[str, str | None]:
    """
    Selects a primary and optional secondary type, respecting weights and rules.

    This is the canonical way to get a valid type combination, respecting
    base weights, synergy boosts, and incompatible pairs.

    Args:
        primary_type_override: If provided, this type is used as the primary
            type instead of choosing one randomly. Defaults to None.
        secondary_chance: The base probability (0.0 to 1.0) of generating a
            secondary type.

    Returns:
        A tuple containing the primary type and an optional secondary type.
    """
    # 1. Choose the primary type based on its base weight or use the override.
    primary_type = (
        primary_type_override if primary_type_override else weighted_choice(SEED_TYPES_WEIGHTED)
    )

    # 2. Decide if we should even try to add a secondary type.
    if random.random() > secondary_chance:
        return primary_type, None

    # 3. If so, build a list of valid secondary candidates.
    candidates = {}
    for t in SEED_TYPES:
        # A candidate must not be the same as the primary type.
        if t == primary_type:
            continue
        # It must not be in an incompatible pair.
        if frozenset([primary_type, t]) in INCOMPATIBLE_TYPE_PAIRS:
            continue

        # Start with the candidate's base weight.
        weight = SEED_TYPES_WEIGHTED.get(t, 1.0)
        # Apply synergy boost if one exists.
        synergy_mult = TYPE_SYNERGY_BOOSTS.get(frozenset([primary_type, t]), 1.0)
        candidates[t] = weight * synergy_mult

    if not candidates:
        return primary_type, None

    # 4. Choose a secondary type from the valid, weighted candidates.
    secondary_type = weighted_choice(candidates)
    return primary_type, secondary_type

@dataclass
class MonsterSeed:
    """A snapshot of a monster's generated attributes before final calculations."""

    idnum: int  # The unique identifier for this generation batch.
    name: str  # The monster's generated name.
    species: str  # The monster's base form/species.
    primary_type: str  # The primary elemental type.
    secondary_type: str | None # The optional secondary elemental type.
    habitat: str  # The monster's natural habitat.
    stats: Dict[str, int]  # A dictionary of the monster's stats (e.g., HP, ATK).
    mutagens: Dict[str, List[str]]  # Modifiers applied, categorized as 'major' or 'utility'.
    physical_traits: List[str]  # A list of notable physical characteristics.
    held_item: str | None  # An item the monster might be holding.
    tempers: Dict[str, str]  # The monster's personality traits (mood and affinity).
    meta: Dict[str, Any]  # A catch-all for other data like tags, resistances, and a unique pin.

    @classmethod
    def forge(
        cls,
        idnum: int,
        primary_type: str,
        secondary_type: str,
    ) -> "MonsterSeed":
        """
        Factory method to create a new, properly biased MonsterSeed.

        This method orchestrates the initial creation of a monster, including
        selecting its species, habitat, traits, and calculating its base stats
        and meta attributes based on its types.

        Args:
            idnum: A unique identifier for this generation batch.
            primary_type: The primary elemental type of the monster.
            secondary_type: The optional secondary elemental type.

        Returns:
            A new MonsterSeed instance with all base attributes generated.

        Raises:
            ValueError: If the provided types are invalid or incompatible.
        """
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

        name = ""
        species = weighted_choice(FORMS_BY_TYPE[primary_type])
        habitat = weighted_choice(HABITATS_BY_TYPE[primary_type])

        # Initialize all data structures
        mutagens = {"major": [], "utility": []}
        mood = weighted_choice(TEMPERS_COUPLED["mood"])
        affinity = weighted_choice(TEMPERS_COUPLED["affinity"])
        tempers = {"mood": mood, "affinity": affinity}

        # New, more flexible trait selection
        num_physical = 1 if random.random() < 0.75 else 2
        physical_traits = [weighted_choice(PHYSICAL_TRAITS) for _ in range(num_physical)]
        held_item = weighted_choice(HELD_ITEMS) if random.random() < 0.4 else None

        stats = calculate_base_stats(primary_type, secondary_type)
        meta = get_base_meta(primary_type, secondary_type)
        meta["notes"] = []


        # --- 3. Create the Seed Instance ---
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


def calculate_base_stats(primary_type: str, secondary_type: str | None) -> dict[str, int]:
    """
    Calculates base stats for a monster given its primary and secondary types.

    This function applies all type-based multipliers and additions from the
    `SEEDTYPE_ATTR` data to the `BASE_STATS`. Secondary type modifiers are
    applied at a reduced effectiveness.

    Args:
        primary_type: The primary elemental type.
        secondary_type: The optional secondary elemental type.

    Returns:
        A dictionary of the calculated base stats for the monster.
    """
    stats = BASE_STATS.copy()
    primary_bias = SEEDTYPE_ATTR.get(primary_type, {})
    for stat, mult in primary_bias.get("mul", {}).items():
        if stat in stats:
            stats[stat] = int(round(stats[stat] * mult))
    for stat, addition in primary_bias.get("add", {}).items():
        if stat in stats:
            stats[stat] += addition

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


def get_base_meta(primary_type: str, secondary_type: str | None) -> dict[str, list[str]]:
    """
    Gets the base meta tags, resistances, and weaknesses from the monster's types.

    Args:
        primary_type: The primary elemental type.
        secondary_type: The optional secondary elemental type.

    Returns:
        A dictionary containing lists of tags, resistances, and weaknesses
        derived from the monster's types.
    """
    meta = {"tags": [], "resist": [], "weak": []}

    def apply_type_meta(type_name, meta_dict):
        type_attrs = SEEDTYPE_ATTR.get(type_name, {})
        for tag in type_attrs.get("tags", []):
            if tag.startswith("Resist:"):
                meta_dict["resist"].append(tag.split(":", 1)[1])
            elif tag.startswith("Weak:"):
                meta_dict["weak"].append(tag.split(":", 1)[1])
            else:
                meta_dict["tags"].append(tag)

    apply_type_meta(primary_type, meta)
    if secondary_type:
        apply_type_meta(secondary_type, meta)

    return meta

