from __future__ import annotations
from typing import Optional, List, Dict, Any
import random
import os

from .data import data  # MAJOR_MODS, UTILITY_MODS, etc.
from .monsterseed import MonsterSeed, weighted_choice


# ---- Module-level tuning knobs
DEFAULT_SYNERGY_FACTOR = 2.0  # Multiplicative synergy per match (tweak to taste)
MAX_SYNERGY_MULT = 8.0  # Hard cap on total synergy multiplier so weights don't explode
RARITY_ALPHA = 1.0  # Rarity -> weight exponent (1.0 = 1/r, <1 flatter, >1 steeper)
DEBUG = bool(
    os.getenv("DEX_DEBUG")
)  # Optional debug toggle (set env var DEX_DEBUG=1 to enable)


def dbg(*args, **kwargs):
    if DEBUG:
        print("[mon_forge DEBUG]", *args, **kwargs)


def rarity_to_weight(rarity_val: Any, alpha: float = RARITY_ALPHA) -> float:
    """
    Convert a 'rarity' numeric value into a sampling weight.
    Default behavior: weight = 1.0 / (rarity ** alpha)
    Guards against non-numeric and zero/negative rarities.
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
    """Factory function that uses the MonsterSeed's own forge method."""
    return MonsterSeed.forge(idnum, primary_type, secondary_type)


def weighted_sample_without_replacement(
    weight_dict: Dict[str, float], k: int
) -> List[str]:
    """
    Draw up to k unique keys from weight_dict without replacement, respecting weights.
    Returns selected keys (length may be < k if pool is smaller).
    This is an iterative algorithm: pick according to weights, remove chosen, repeat.
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
    Apply mutagens to a MonsterSeed.
    - Uses inverse-rarity weighting (rarity_to_weight).
    - Applies a multiplicative synergy factor if a mod lists 'synergy' items found in the seed.
    - Samples without replacement (so majors/utilities will be unique within their category).
    - Defensively handles missing keys on seed (uses setdefault).
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
        required = mod_def.get("required_types", []) or []
        incompatible = mod_def.get("incompatible_types", []) or []

        # type gating: all required must be present, and none of incompatible present
        if not all(t in monster_types for t in required):
            continue
        if any(t in monster_types for t in incompatible):
            continue

        base_w = rarity_to_weight(mod_def.get("rarity", 1.0))
        # multiplicative synergy stacking
        synergy_mult = 1.0
        for s in mod_def.get("synergy", []) or []:
            if str(s) in seed_mutagen_set:
                synergy_mult *= float(
                    mod_def.get("synergy_factor", DEFAULT_SYNERGY_FACTOR)
                )
        final_w = base_w * min(synergy_mult, MAX_SYNERGY_MULT)
        if final_w > 0.0:
            available_majors[key] = final_w
            dbg(
                f"major candidate: {key}, base_w={base_w:.6f}, synergy_mult={synergy_mult:.3f}, final_w={final_w:.6f}"
            )

    available_utilities: Dict[str, float] = {}
    for key, mod_def in UTILITY_MODS.items():
        required = mod_def.get("required_types", []) or []
        incompatible = mod_def.get("incompatible_types", []) or []

        if not all(t in monster_types for t in required):
            continue
        if any(t in monster_types for t in incompatible):
            continue

        base_w = rarity_to_weight(mod_def.get("rarity", 1.0))
        synergy_mult = 1.0
        for s in mod_def.get("synergy", []) or []:
            if str(s) in seed_mutagen_set:
                synergy_mult *= float(
                    mod_def.get("synergy_factor", DEFAULT_SYNERGY_FACTOR)
                )
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

    def apply_one(mut_def: dict):
        # multiplicative adjustments
        for stat, mult in mut_def.get("mul", {}).items():
            if stat in seed.stats:
                seed.stats[stat] = int(round(seed.stats[stat] * mult))
        # additive adjustments
        for stat, add in mut_def.get("add", {}).items():
            if stat in seed.stats and isinstance(add, (int, float)):
                seed.stats[stat] += int(round(add))
        # tags/resists/weaknesses
        for tag in mut_def.get("tags", []):
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
    """Combines forging and mutagen application into one call."""
    seed = forge_seed_monster(idnum, primary_type, secondary_type)
    return apply_mutagens(seed, major_count, util_count)
