#!/usr/bin/env python3
"""
Test harness for mon_forge weighting/synergy (per-trial expected weights).
Runs N trials of generate_monster(..., major_count=1) and reports empirical vs
the average expected probability computed for each trial's freshly-forged seed.
"""
from collections import Counter, defaultdict
import random
from typing import Dict

# Adjust import path to your package layout if needed
from mongens import mon_forge
from mongens.data.data import MAJOR_MODS


# ---------- Config ----------
TRIALS = 20000
MONSTER_TYPE = "Insect"  # change to a type present in your data
RANDOM_SEED = 12345  # set to None for non-deterministic runs


# ----------------------------


def build_expected_weights_for_seed(seed) -> Dict[str, float]:
	"""Re-implement the same filtering + synergy computation used by mon_forge.apply_mutagens
	to produce an expected weight map for a freshly-forged seed.
	"""
	monster_types = {seed.primary_type}
	if getattr(seed, "secondary_type", None):
		monster_types.add(seed.secondary_type)

	# seed mutagens set for synergy checks (strings)
	seed_mutagen_set = set()
	for bucket in seed.mutagens.values():
		for e in bucket:
			seed_mutagen_set.add(str(e))

	available = {}
	for key, mod_def in MAJOR_MODS.items():
		required = mod_def.get("required_types", []) or []
		incompatible = mod_def.get("incompatible_types", []) or []

		if not all(t in monster_types for t in required):
			continue
		if any(t in monster_types for t in incompatible):
			continue

		base_w = mon_forge.rarity_to_weight(mod_def.get("rarity", 1.0))
		synergy_mult = 1.0
		for s in mod_def.get("synergy", []) or []:
			if str(s) in seed_mutagen_set:
				synergy_mult *= float(mod_def.get("synergy_factor", mon_forge.DEFAULT_SYNERGY_FACTOR))
		final_w = base_w * min(synergy_mult, mon_forge.MAX_SYNERGY_MULT)
		if final_w > 0.0:
			available[key] = final_w
	return available


def normalize_weights(wdict: Dict[str, float]) -> Dict[str, float]:
	total = sum(wdict.values())
	if total <= 0:
		return {k: 0.0 for k in wdict}
	return {k: v / total for k, v in wdict.items()}


def main():
	if RANDOM_SEED is not None:
		random.seed(RANDOM_SEED)

	counts = Counter()
	cumulative_expected = defaultdict(float)  # sum of expected probabilities per mod across trials
	none_count = 0

	for i in range(TRIALS):
		# Forge a fresh seed for this trial and compute expected probs for that seed
		seed = mon_forge.forge_seed_monster(i, MONSTER_TYPE, None)
		expected_weights = build_expected_weights_for_seed(seed)
		expected_probs = normalize_weights(expected_weights)

		# Accumulate expected probs (for averaging later)
		for k, p in expected_probs.items():
			cumulative_expected[k] += p

		# Run the actual generator (which forges internally too)
		m = mon_forge.generate_monster(idnum=i, primary_type=MONSTER_TYPE, major_count=1, util_count=0, secondary_type=None, )
		majors = m.mutagens.get("major", [])
		if majors:
			counts[majors[0]] += 1
		else:
			none_count += 1

	# Convert cumulative expected sums into average expected probabilities
	avg_expected = {k: v / TRIALS for k, v in cumulative_expected.items()}

	total_done = TRIALS
	print(f"\nTrials: {TRIALS}, Monster type: {MONSTER_TYPE}, random_seed: {RANDOM_SEED}")
	print(f"No major chosen (none_count): {none_count}\n")

	print(f"{'MOD':30} {'emp_freq':>10} {'avg_exp':>10} {'ratio(emp/exp)':>14}")
	print("-" * 70)
	all_keys = set(avg_expected.keys()) | set(counts.keys())
	for k in sorted(all_keys, key=lambda x: (-avg_expected.get(x, 0), -counts.get(x, 0))):
		emp = counts.get(k, 0) / total_done
		exp = avg_expected.get(k, 0.0)
		if exp > 0:
			ratio = emp / exp
		else:
			ratio = float("inf") if emp > 0 else 0.0
		print(f"{k:30} {emp:10.4f} {exp:10.4f} {ratio:14.3f}")


if __name__ == "__main__":
	main()
