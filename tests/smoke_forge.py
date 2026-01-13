import sys
from pathlib import Path
# Ensure local src on path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from mongens.monsterseed import MonsterSeed
from mongens.data.data import SEED_TYPES, MAJOR_MODS, UTILITY_MODS

print('Forging one seed per type...')
for i, t in enumerate(SEED_TYPES, start=1):
    try:
        seed = MonsterSeed.forge(i, primary_type=t, secondary_type=None, secondary_chance=0.0)
        major = seed.mutagens['major'][0]
        utility = seed.mutagens['utility'][0]
        major_allowed = MAJOR_MODS.get(major, {}).get('allowed_types')
        util_allowed = UTILITY_MODS.get(utility, {}).get('allowed_types')
        print(f"{i:02d}. {t} -> form={seed.form!r}, habitat={seed.habitat!r}, hp={seed.stats.get('HP')}, atk={seed.stats.get('ATK')} | major={major} allowed={major_allowed} | util={utility} allowed={util_allowed}")
    except Exception as e:
        print(f"{i:02d}. {t} -> ERROR: {e}")
