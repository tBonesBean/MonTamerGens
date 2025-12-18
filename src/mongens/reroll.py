import copy
import random
from typing import Any

from . import mon_forge, monster_cache
from .data.data import HELD_ITEMS, MAJOR_MODS, PHYSICAL_TRAITS, UTILITY_MODS
from .monsterseed import (
    MonsterSeed,
    calculate_base_stats,
    get_base_meta,
    weighted_choice,
)

"""
This module contains the logic for re-rolling attributes of existing monsters. This is achieved by loading a cached monster, surgically modifying its attributes, and then re-running the necessary parts of the generation pipeline to ensure consistency. The new monster is saved to the cache with a new PIN.
"""

mutation_context = "species" | "instance" | "encounter"


def _choose_physical_traits() -> list[str]:
    """
    Selects one or two random physical traits based on weighted choices.
    Returns: A list containing one or two randomly selected physical traits.
    """
    num_physical = 1 if random.random() < 0.75 else 2
    return [weighted_choice(PHYSICAL_TRAITS) for _ in range(num_physical)]


def _choose_held_item() -> str | None:
    """
    Selects a random held item with a 40% probability.
    Returns: A string representing the chosen held item, or None if no item is chosen.
    """
    return weighted_choice(HELD_ITEMS) if random.random() < 0.4 else None


def apply_mutagens_to_stats(
    base_stats: dict[str, int], base_meta: dict[str, list], mutagens: list[str]
) -> tuple[dict[str, int], dict[str, Any]]:
    """
    Applies a list of mutagens to a set of base stats and returns the new stats and meta.
    This function takes a clean set of stats and meta dictionaries and applies the
    effects of the provided mutagens (both major and utility) to them.
    base_stats: A dictionary of the monster's stats before any mutagens are applied.
    base_meta: A dictionary of the monster's meta attributes (tags, resistances, etc.) before any mutagens are applied.
    mutagens: A list of strings representing the keys of the mutagens to apply.
        Returns: A tuple containing the modified stats dictionary and the modified meta dictionary.
    """

    stats = copy.deepcopy(base_stats)
    meta = copy.deepcopy(base_meta)

    all_mods = {**MAJOR_MODS, **UTILITY_MODS}

    for mutagen_key in mutagens:
        mod_def = all_mods.get(mutagen_key)
        if mod_def:
            # multiplicative adjustments
            for stat, mult in mod_def.get("mul", {}).items():
                if stat in stats:
                    stats[stat] = int(round(stats[stat] * mult))
            # additive adjustments
            for stat, add in mod_def.get("add", {}).items():
                if stat in stats and isinstance(add, (int, float)):
                    stats[stat] += int(round(add))
            # tags/resists/weaknesses
            for tag in mod_def.get("tags", []):
                if isinstance(tag, str) and tag.startswith("Resist:"):
                    meta.setdefault("resist", []).append(tag.split(":", 1)[1])
                elif isinstance(tag, str) and tag.startswith("Weak:"):
                    meta.setdefault("weak", []).append(tag.split(":", 1)[1])
                else:
                    meta.setdefault("tags", []).append(tag)
    return stats, meta


def reroll_monster_attributes(pin: str, reroll_options: dict) -> MonsterSeed | None:
    """
    Loads a monster, re-rolls attributes, saves it as new, and returns the seed.

    This is the main function for the re-roll feature. It orchestrates the process of
    loading a monster, recalculating its attributes based on user choices,
    re-forging its name, and saving it as a new entry in the monster cache.

    Args:
        pin: The 10-character unique ID of the monster to be re-rolled.
        reroll_options: A dictionary specifying which attributes to re-roll.
                        e.g., {'traits': True, 'majors': False}

    Returns:
        The MonsterSeed of the newly created monster, or None if the original
        monster was not found or the re-roll could not be completed.
    """
    original_monster = monster_cache.load_monster(pin)
    if not original_monster:
        print(f"Error: Monster with PIN {pin} not found in cache.")
        return None

    new_monster = copy.deepcopy(original_monster)

    rerolled = False
    if reroll_options.get("traits"):
        new_monster.physical_traits = _choose_physical_traits()
        rerolled = True
        print("Re-rolled physical traits.")

    if reroll_options.get("majors"):
        # 1. Calculate base stats and meta from types to get a clean slate
        base_stats = calculate_base_stats(
            new_monster.primary_type, new_monster.secondary_type
        )
        base_meta = get_base_meta(new_monster.primary_type, new_monster.secondary_type)

        # 2. Select a new major mutagen that is compatible and not the same as the old one
        old_majors = new_monster.mutagens.get("major", [])
        monster_types = {new_monster.primary_type}
        if new_monster.secondary_type:
            monster_types.add(new_monster.secondary_type)

        available_majors = {}
        for key, mod_def in MAJOR_MODS.items():
            if key in old_majors:
                continue

            required = mod_def.get("required_types", []) or []
            incompatible = mod_def.get("incompatible_types", []) or []

            if not all(t in monster_types for t in required):
                continue
            if any(t in monster_types for t in incompatible):
                continue

            available_majors[key] = mon_forge.rarity_to_weight(
                mod_def.get("rarity", 1.0)
            )

        if not available_majors:
            print("No other compatible major mutagens available to re-roll to.")
            return None

        new_major = weighted_choice(available_majors)
        new_monster.mutagens["major"] = [new_major]
        print(f"Re-rolled major mutagen to: {new_major}")

        # 3. Re-apply all mutagens (new major + old utilities) to the clean stats and meta
        utility_mutagens = new_monster.mutagens.get("utility", [])
        all_mutagens = new_monster.mutagens["major"] + utility_mutagens

        new_stats, new_meta = apply_mutagens_to_stats(
            base_stats, base_meta, all_mutagens
        )
        new_monster.stats = new_stats
        new_monster.meta = new_meta

        rerolled = True

    if rerolled:
        # 4. Re-forge the name and save the new monster
        new_monster = mon_forge.forge_monster_name(new_monster)
        monster_cache.save_monster(new_monster)
        print(f"Successfully re-rolled monster. New PIN: {new_monster.meta.get('pin')}")
        return new_monster

    print("No attributes were re-rolled.")
    return original_monster
