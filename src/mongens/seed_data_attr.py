from __future__ import annotations

from dataclasses import dataclass
from random import choice
from typing import Dict, List, Any, Optional

from mongens.data.data import (
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
    """
    A quiet little snapshot of a monster *before* combat math,
    move learnsets, and full encounter logic are layered on.
    """
    idnum: int
    species: str
    primary_type: str
    secondary_type: Optional[str]
    habitat: str
    # later these will get populated/expanded by mutagen passes
    elements: Dict[str, List[str]]
    traits: List[str]
    tempers: Dict[str, str]
    stats: Dict[str, int]
    meta: Dict[str, Any]

    @classmethod
    def forge(cls, primary_type: str, idnum: int, secondary_type: Optional[str] = None) -> MonsterSeed:
        """
        Factory method to create a new, properly biased MonsterSeed
        from a primary type, an optional secondary type, and an ID number.
        """
        if primary_type not in SEED_TYPES:
            raise ValueError(f"Unknown primary_type: {primary_type!r}")
        if secondary_type and secondary_type not in SEED_TYPES:
            raise ValueError(f"Unknown secondary_type: {secondary_type!r}")
        if secondary_type and frozenset([primary_type, secondary_type]) in INCOMPATIBLE_TYPE_PAIRS:
            raise ValueError(f"Incompatible type pair: {primary_type} and {secondary_type}")

        # All the logic from the old `forge_seed_monster` now lives here.
        # Species and habitat are determined by the primary type
        species = choice(FORMS_BY_TYPE[primary_type])
        habitat = choice(HABITATS_BY_TYPE[primary_type])

        main_types = [primary_type]
        if secondary_type:
            main_types.append(secondary_type)
        elements = {"main": main_types, "major": [], "minor": [], "utility": []}

        # We can call the roll functions directly
        col1, col2, col3 = COL_TRAITS
        traits = [choice(col1), choice(col2), choice(col3)]

        mood = choice(TEMPERS_COUPLED["mood"])
        affinity = choice(TEMPERS_COUPLED["affinity"])
        tempers = {"mood": mood, "affinity": affinity}

        stats = BASE_STATS.copy()
        meta: Dict[str, Any] = {"tags": [], "resist": [], "weak": [], "notes": []}

        # Instantiate the class using `cls`
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

        # Apply the type bias immediately after creation
        for monster_type in main_types:
            bias = SEEDTYPE_ATTR.get(monster_type)
            if bias:
                muls = bias.get("mul", {})
                adds = bias.get("add", {})
                for stat, mult in muls.items():
                    if stat in seed.stats:
                        seed.stats[stat] = int(round(seed.stats[stat] * mult))
                for stat, addition in adds.items():
                    if stat in seed.stats:
                        seed.stats[stat] += addition

        return seed

    @classmethod
    def get(cls):
        pass
