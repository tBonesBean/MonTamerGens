import random
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from mongens.monsterseed import MonsterSeed
from mongens.data.data import SEED_TYPES, MAJOR_MODS, UTILITY_MODS

random.seed(42)

trials = 200
issues = []

def apply_mods_to_stats(base_stats, mod):
    stats = base_stats.copy()
    mul = mod.get('mul', {})
    add = mod.get('add', {})
    for s, m in mul.items():
        if s in stats:
            stats[s] = int(round(stats[s] * m))
    for s, a in add.items():
        if s in stats:
            stats[s] = int(round(stats[s] + a))
    return stats

print('Running exhaustive forge test')
for i in range(1, trials+1):
    try:
        seed = MonsterSeed.forge(i, secondary_chance=0.7)
    except Exception as e:
        print(f'Forge error on trial {i}: {e}')
        issues.append(('forge_error', i, str(e)))
        continue

    primary = seed.primary_type
    secondary = seed.secondary_type
    major = seed.mutagens['major'][0]
    util = seed.mutagens['utility'][0]

    major_mod = MAJOR_MODS.get(major, {})
    util_mod = UTILITY_MODS.get(util, {})

    allowed_major = major_mod.get('allowed_types')
    allowed_util = util_mod.get('allowed_types')

    compatible_major = (allowed_major is None) or (primary in allowed_major) or (secondary in allowed_major if secondary else False)
    compatible_util = (allowed_util is None) or (primary in allowed_util) or (secondary in allowed_util if secondary else False)

    base_stats = seed.stats
    post_stats = apply_mods_to_stats(base_stats, major_mod)

    # detect large unexpected changes
    hp_delta = post_stats.get('HP', base_stats.get('HP')) - base_stats.get('HP')

    if not compatible_major:
        issues.append(('incompatible_major', i, primary, secondary, major, allowed_major))

    if not compatible_util:
        issues.append(('incompatible_util', i, primary, secondary, util, allowed_util))

    if abs(hp_delta) > 50:
        issues.append(('large_hp_delta', i, primary, major, base_stats.get('HP'), post_stats.get('HP')))

# Report
print('\nSummary:')
print(f'Ran {trials} forges; found {len(issues)} issues')
for it in issues[:60]:
    print(it)

if issues:
    print('\nSample problematic seeds (first 10):')
    count = 0
    for t in issues:
        if count >= 10:
            break
        print(t)
        count += 1
else:
    print('No immediate issues found')
