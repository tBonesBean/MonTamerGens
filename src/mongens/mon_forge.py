from __future__ import annotations

from random import choice
from typing import Optional

from .data.data import (
    MAJOR_MODS,
    MINOR_MODS,
    UTILITY_MODS,
)
from .seed_data_attr import MonsterSeed


def forge_seed_monster(primary_type: str, idnum: int, secondary_type: Optional[str] = None) -> MonsterSeed:
    """
    Factory function that uses the MonsterSeed's own forge method.
    This keeps our creation logic centralized on the class itself.
    :rtype: MonsterSeed
    """
    return MonsterSeed.forge(primary_type, idnum, secondary_type)

def apply_mutagens(seed: MonsterSeed, major_count: int, minor_count: int, util_count: int) -> MonsterSeed:
    # (This function remains the same, as its job is to modify an *existing* seed)
    major_keys = list(MAJOR_MODS.keys())
    minor_keys = list(MINOR_MODS.keys())
    utility_keys = list(UTILITY_MODS.keys())
    chosen_majors = [choice(major_keys) for _ in range(major_count)]
    chosen_minors = [choice(minor_keys) for _ in range(minor_count)]
    chosen_utilities = [choice(utility_keys) for _ in range(util_count)]
    seed.elements["major"].extend(chosen_majors)
    seed.elements["minor"].extend(chosen_minors)
    seed.elements["utility"].extend(chosen_utilities)

    def apply_one(mut_def: dict):
        for stat, mult in mut_def.get("mul", {}).items():
            if stat in seed.stats:
                seed.stats[stat] = int(round(seed.stats[stat] * mult))
        for stat, add in mut_def.get("add", {}).items():
            if stat in seed.stats and isinstance(add, (int, float)):
                seed.stats[stat] = int(round(seed.stats[stat] + add))
        for tag in mut_def.get("tags", []):
            if tag.startswith("Resist:"):
                seed.meta["resist"].append(tag.split(":", 1)[1])
            elif tag.startswith("Weak:"):
                seed.meta["weak"].append(tag.split(":", 1)[1])
            else:
                seed.meta["tags"].append(tag)

    for key in chosen_majors:
        apply_one(MAJOR_MODS[key])
    for key in chosen_minors:
        apply_one(MINOR_MODS[key])
    for key in chosen_utilities:
        apply_one(UTILITY_MODS[key])
    return seed

def generate_monster(primary_type: str, idnum: int, major_count: int, minor_count: int, util_count: int, secondary_type: Optional[str] = None) -> MonsterSeed:
    seed = forge_seed_monster(primary_type, idnum, secondary_type)
    full_mon = apply_mutagens(seed, major_count, minor_count, util_count)
    # ... (rest of the function is the same)
    return full_mon

# (The rest of the file remains the same)
