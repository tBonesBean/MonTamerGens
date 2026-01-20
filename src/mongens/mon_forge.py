from __future__ import annotations

import os
import random
from typing import Any, List, Optional, Dict

from . import monster_cache
from .data.data import MAJOR_MODS, UTILITY_MODS
from .forge_name import forge_monster_name
from .monsterseed import MonsterSeed


# ---- Module-level tuning knobs
DEFAULT_SYNERGY_FACTOR = 2.0  # Multiplicative synergy per match (tweak to taste)
MAX_SYNERGY_MULT = 8.0  # Hard cap on total synergy multiplier so weights don't explode
RARITY_ALPHA = 1.0  # Rarity -> weight exponent (1.0 = 1/r, <1 flatter, >1 steeper)
DEBUG = bool(
    os.getenv("DEX_DEBUG")
)  # Optional debug toggle (set env var DEX_DEBUG=1 to enable)


def dbg(*args, **kwargs):
    """
    Summary:
        Prints debug messages if the DEX_DEBUG environment variable is set.

    Args:
        *args: Positional arguments to be printed.
        **kwargs: Keyword arguments to be printed.
    """
    if DEBUG:
        print("[mon_forge DEBUG]", *args, **kwargs)


def rarity_to_weight(rarity_val: Any, alpha: float = RARITY_ALPHA) -> float:
    """
    Summary:
        Converts a 'rarity' numeric value into a sampling weight.

    Args:
        rarity_val: The rarity value to convert.
        alpha: The exponent to apply to the rarity value.

    Returns:
        The calculated sampling weight. The default behavior is
        weight = 1.0 / (rarity ** alpha). It guards against
        non-numeric and zero/negative rarities.
    """
    try:
        r = float(rarity_val)
    except Exception(BaseException):
        r = 1.0
    r = max(r, 1e-6)  # avoid 0 or negative
    return 1.0 / (r ** float(alpha))


def forge_seed_monster(
    idnum: int, primary_type: str, secondary_type: Any
) -> MonsterSeed:
    """
    Summary:
        A factory function that uses the MonsterSeed's own forge method to create a new monster seed.

    Args:
        idnum: The ID number for the new monster.
        primary_type: The primary type of the monster.
        secondary_type: The secondary type of the monster.

    Returns:
        A new MonsterSeed object.
    """
    seed = MonsterSeed.forge(idnum, primary_type, secondary_type)
    return seed


def weighted_sample_without_replacement(
    weight_dict: Dict[str, float], k: int
) -> List[str]:
    """
    Summary:
        Draws up to k unique keys from a dictionary of weights without replacement,
        respecting the weights of each key.

    Args:
        weight_dict: A dictionary where keys are the items to sample and values are their weights.
        k: The number of items to sample.

    Returns:
        A list of the selected keys. The length of the list may be less than k
        if the pool of available items is smaller than k.
    """
    population = list(weight_dict.keys())
    weights = [float(weight_dict[p]) for p in population]
    selected: List[str] = []

    if not population or k <= 0:
        return selected

    # If k >= population size, return all keys ordered by weight desc (strongest first)
    if k >= len(population):
        ordered = [p for p, _ in sorted(zip(population, weights), key=lambda x: -x[1])]
        dbg("weighted_sample: k >= pool -> returning all ordered by weight:", ordered)
        return ordered

    for _ in range(k):
        total = sum(weights)
        if total <= 0:
            dbg("weighted_sample: total weight <= 0; stopping early")
            break
        r = random.random() * total
        upto = 0.0
        picked_idx = None
        for idx, w in enumerate(weights):
            upto += w
            if r < upto:
                picked_idx = idx
                break
        if picked_idx is None:
            # Floating point edge-case: pick last
            picked_idx = len(weights) - 1

        selected_key = population.pop(picked_idx)
        weights.pop(picked_idx)
        selected.append(selected_key)
        dbg("weighted_sample: picked", selected_key)
    return selected


def apply_mutagens(
    seed: MonsterSeed,
    major_count: int = 0,
    util_count: int = 0,
) -> MonsterSeed:
    """
    Summary:
        Applies a specified number of major and utility mutagens to a given MonsterSeed.
        This function modifies the seed by selecting and applying mutagens based on
        weighted probabilities, type compatibility, and synergy bonuses.

    Args:
        seed: The MonsterSeed object to modify.
        major_count: The number of major mutagens to apply.
        util_count: The number of utility mutagens to apply.

    Returns:
        The modified MonsterSeed object with the new mutagens applied.
    """
    # Ensure seed buckets exist for synergy checks (safe even if forge didn't create them)
    seed.mutagens.setdefault("major", [])
    seed.mutagens.setdefault("utility", [])
    seed.meta.setdefault("resist", [])
    seed.meta.setdefault("weak", [])
    seed.meta.setdefault("tags", [])

    monster_types = {seed.primary_type}
    if getattr(seed, "secondary_type", None):
        monster_types.add(seed.secondary_type)

    # Build a set of seed mutagens for quick synergy checks (strings)
    seed_mutagen_set = set()
    for bucket in seed.mutagens.values():
        for e in bucket:
            seed_mutagen_set.add(str(e))

    dbg("monster_types:", monster_types)
    dbg("seed mutagens:", seed.mutagens)
    dbg("seed_mutagen_set:", seed_mutagen_set)

    # --- Filter Available Mutagens (with synergy multiplier) ---
    available_majors: Dict[str, float] = {}
    for key, mod_def in MAJOR_MODS.items():
        if key in seed_mutagen_set:
            continue

        incompatible = mod_def.get("incompatible_types", []) or []

        # Type gating: monster cannot have any incompatible types.
        if any(t in monster_types for t in incompatible):
            continue

        base_w = rarity_to_weight(mod_def.get("rarity", 1.0))
        # Multiplicative synergy stacking based on monster type
        synergy_mult = 1.0
        synergy_bonuses = mod_def.get("synergy_bonus", {})
        for monster_type in monster_types:
            if monster_type in synergy_bonuses:
                synergy_mult *= float(synergy_bonuses[monster_type])

        final_w = base_w * min(synergy_mult, MAX_SYNERGY_MULT)
        if final_w > 0.0:
            available_majors[key] = final_w
            dbg(
                f"major candidate: {key}, base_w={base_w:.6f}, synergy_mult={synergy_mult:.3f}, final_w={final_w:.6f}"
            )

    available_utilities = {}
    for key, mod_def in UTILITY_MODS.items():
        if key in seed_mutagen_set:
            continue

        incompatible = mod_def.get("incompatible_types", []) or []

        # Type gating: monster cannot have any incompatible types.
        if any(t in monster_types for t in incompatible):
            continue

        base_w = rarity_to_weight(mod_def.get("rarity", 1.0))
        # Multiplicative synergy stacking based on monster type
        synergy_mult = 1.0
        synergy_bonuses = mod_def.get("synergy_bonus", {})
        for monster_type in monster_types:
            if monster_type in synergy_bonuses:
                synergy_mult *= float(synergy_bonuses[monster_type])

        final_w = base_w * min(synergy_mult, MAX_SYNERGY_MULT)
        if final_w > 0.0:
            available_utilities[key] = final_w
            dbg(
                f"util candidate: {key}, base_w={base_w:.6f}, synergy_mult={synergy_mult:.3f}, final_w={final_w:.6f}"
            )

    dbg("available_majors:", available_majors)
    dbg("available_utilities:", available_utilities)

    # --- Select Mutagens using weighted sampling without replacement ---
    chosen_majors = weighted_sample_without_replacement(available_majors, major_count)
    chosen_utilities = weighted_sample_without_replacement(
        available_utilities, util_count
    )

    dbg("chosen_majors:", chosen_majors)
    dbg("chosen_utilities:", chosen_utilities)

    # Append chosen keys to seed and apply their effects
    seed.mutagens["major"].extend(chosen_majors)
    seed.mutagens["utility"].extend(chosen_utilities)

    def apply_one(mod_def: dict):
        # multiplicative adjustments
        for stat, mult in mod_def.get("mul", {}).items():
            if stat in seed.stats:
                seed.stats[stat] = int(round(seed.stats[stat] * mult))
        # additive adjustments
        for stat, add in mod_def.get("add", {}).items():
            if stat in seed.stats and isinstance(add, (int, float)):
                seed.stats[stat] += int(round(add))
        # tags/resists/weaknesses
        for tag in mod_def.get("tags", []):
            if isinstance(tag, str) and tag.startswith("Resist:"):
                seed.meta.setdefault("resist", []).append(tag.split(":", 1)[1])
            elif isinstance(tag, str) and tag.startswith("Weak:"):
                seed.meta.setdefault("weak", []).append(tag.split(":", 1)[1])
            else:
                seed.meta.setdefault("tags", []).append(tag)

    for key in chosen_majors:
        mod_def = MAJOR_MODS.get(key)
        if mod_def:
            apply_one(mod_def)
    for key in chosen_utilities:
        mod_def = UTILITY_MODS.get(key)
        if mod_def:
            apply_one(mod_def)

    return seed


def generate_monster(
    idnum: int,
    primary_type: str,
    secondary_type: Optional[str] = None,
    major_count: int = 0,
    util_count: int = 0,
) -> MonsterSeed:
    """
    Summary:
        Combines monster seed forging, mutagen application, and naming into a single function call.

    Args:
        idnum: The ID number for the new monster.
        primary_type: The primary type of the monster.
        secondary_type: The optional secondary type of the monster.
        major_count: The number of major mutagens to apply.
        util_count: The number of utility mutagens to apply.

    Returns:
        A fully generated MonsterSeed object, including a name and applied mutagens.
    """
    generic = forge_seed_monster(idnum, primary_type, secondary_type)
    seed_with_mutagens = apply_mutagens(generic, major_count, util_count)
    seed_with_name = forge_monster_name(seed_with_mutagens)

    # Save the completed monster to the cache and embed the ID
    monster_cache.save_monster(seed_with_name)

    return seed_with_name


"""
def choose_silhouette(seed: MonsterSeed) -> Silhouette:
    weights: dict[Silhouette, float] = {}

    # 1. primary type bias
    apply_type_bias(weights, seed.primary_type)

    # 2. secondary type bias
    apply_type_bias(weights, seed.secondary_type, scale=0.5)

    # 3. habitat bias
    apply_habitat_bias(weights, seed.habitat)

    # 4. stat shape tiebreaker
    apply_stat_bias(weights, seed.stats)

    return weighted_choice(weights, deterministic=True)
"""
