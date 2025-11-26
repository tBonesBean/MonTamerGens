from __future__ import annotations

from dataclasses import dataclass
from random import choice
from typing import Dict, List, Any, Optional

# Correctly import from the sibling 'data' module
from .data import (
	BASE_STATS,
	SEED_TYPES,
	INCOMPATIBLE_TYPE_PAIRS,
	FORMS_BY_TYPE,
	SEEDTYPE_ATTR,
	COL_TRAITS,
	TEMPERS_COUPLED,
	HABITATS_BY_TYPE
)


@dataclass
class MonsterSeed:
    """A snapshot of a monster before combat math and other logic."""
    idnum: int
    species: str
    primary_type: str
    secondary_type: Optional[str]
    stats: Dict[str, int]
    elements: Dict[str, List[str]]
    habitat: str
    traits: List[str]
    tempers: Dict[str, str]
    meta: Dict[str, Any]

    @classmethod
    def forge(cls, idnum: int, primary_type: str, secondary_type: Optional[str] = None) -> MonsterSeed:
        """
        Factory method to create a new, properly biased MonsterSeed
        from a primary type, an optional secondary type, and an ID number.
        """
        # --- 1. Validate Types ---
        if primary_type not in SEED_TYPES:
            raise ValueError(f"Unknown primary_type: {primary_type!r}")

        if secondary_type:
            if secondary_type not in SEED_TYPES:
                raise ValueError(f"Unknown secondary_type: {secondary_type!r}")
            if secondary_type == primary_type:
                raise ValueError("Secondary type cannot be the same as the primary type.")
            if frozenset([primary_type, secondary_type]) in INCOMPATIBLE_TYPE_PAIRS:
                raise ValueError(f"Incompatible type pairing: {primary_type} and {secondary_type}")

        # --- 2. Assemble Base Data ---
        # The monster's core identity is based on its primary type
        species = choice(FORMS_BY_TYPE[primary_type])
        habitat = choice(HABITATS_BY_TYPE[primary_type])

        # Combine types for later processing
        active_types = [primary_type]
        if secondary_type:
            active_types.append(secondary_type)

        # Initialize all data structures
        elements = {"main": active_types, "major": [], "minor": [], "utility": []}
        col1, col2, col3 = COL_TRAITS
        traits = [choice(col1), choice(col2), choice(col3)]
        mood = choice(TEMPERS_COUPLED["mood"])
        affinity = choice(TEMPERS_COUPLED["affinity"])
        tempers = {"mood": mood, "affinity": affinity}
        stats = BASE_STATS.copy()
        meta: Dict[str, Any] = {"tags": [], "resist": [], "weak": [], "notes": []}

        # --- 3. Create the Seed Instance ---
        seed = cls(
            idnum=idnum,
            species=species,
            habitat=habitat,
            primary_type=primary_type,
            secondary_type=secondary_type,
            elements=elements,
            tempers=tempers,
            traits=traits,
            stats=stats,
            meta=meta,
        )

        # --- 4. Apply Stat Biases from Both Types ---
        # Primary type gets full stat multipliers
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
                    seed.stats[stat] += int(round(addition * 0.5))

        return seed
