from dataclasses import dataclass
import random
from typing import Any, Iterable, List, Tuple, Union

from .data.data import *


ChoiceList = Union[Dict[Any, float], Iterable[Tuple[Any, float]]]


def weighted_choice(choices_with_weights: ChoiceList):
    """
    Select an item from dict(item->weight) or iterable of (item, weight).
    Raises ValueError on bad inputs (non-positive total weight or negative weights).
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


@dataclass
class MonsterSeed:
    """A snapshot of a monster before combat math and other logic."""

    idnum: int
    name: str
    species: str
    primary_type: str
    secondary_type: str
    habitat: str
    stats: Dict[str, int]
    mutagens: Dict[str, List[str]]
    traits: List[str]
    tempers: Dict[str, str]
    meta: Dict[str, Any]

    @classmethod
    def forge(
        cls,
        idnum: int,
        primary_type: str,
        secondary_type: str,
    ) -> "MonsterSeed":
        """
        Factory method to create a new, properly biased MonsterSeed from a primary type,
        an optional secondary type, and an ID number.
        """
        if primary_type not in SEED_TYPES:
            raise ValueError(f"Unknown primary_type: {primary_type!r}")

        active_types = [primary_type]
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
            active_types.append(secondary_type)

        name = ""
        species = weighted_choice(FORMS_BY_TYPE[primary_type])
        habitat = weighted_choice(HABITATS_BY_TYPE[primary_type])

        # Initialize all data structures
        mutagens = {"major": [], "utility": []}
        mood = weighted_choice(TEMPERS_COUPLED["mood"])
        affinity = weighted_choice(TEMPERS_COUPLED["affinity"])
        tempers = {"mood": mood, "affinity": affinity}

        traits = [weighted_choice(col) for col in COL_TRAITS]

        stats = BASE_STATS.copy()
        meta: Dict[str, Any] = {"tags": [], "resist": [], "weak": [], "notes": []}

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
            tempers=tempers,
            traits=traits,
            meta=meta,
        )

        primary_bias = SEEDTYPE_ATTR.get(primary_type, {})
        for stat, mult in primary_bias.get("mul", {}).items():
            if stat in seed.stats:
                seed.stats[stat] = int(round(seed.stats[stat] * mult))
        for stat, addition in primary_bias.get("add", {}).items():
            if stat in seed.stats:
                seed.stats[stat] += addition

        # Secondary type gets reduced multipliers (e.g., 50% effect) to feel less dominant
        if secondary_type:
            secondary_bias = SEEDTYPE_ATTR.get(secondary_type, {})
            for stat, mult in secondary_bias.get("mul", {}).items():
                # Apply the multiplier at a reduced effectiveness
                effective_mult = 1 + ((mult - 1) * 0.5)
                if stat in seed.stats:
                    seed.stats[stat] = int(round(seed.stats[stat] * effective_mult))
            for stat, addition in secondary_bias.get("add", {}).items():
                # Apply additions at reduced effectiveness
                if stat in seed.stats:
                    seed.stats[stat] = int(round(seed.stats[stat] + (addition * 0.5)))
        return seed
