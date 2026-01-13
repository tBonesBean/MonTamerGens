from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from mongens.data.data import MAJOR_MODS

target='Vessel'
allowed = []
for name, mod in MAJOR_MODS.items():
    ats = mod.get('allowed_types')
    if ats is None:
        allowed.append((name, 'ANY'))
    elif target in ats:
        allowed.append((name, ats))

print(f'Mods allowing {target}:')
for it in allowed:
    print(it)
print('\nTotal:', len(allowed))
