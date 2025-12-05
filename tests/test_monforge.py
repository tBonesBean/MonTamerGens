# tests/check_mon_forge.py
from mongens.mon_forge import generate_monster
import random

random.seed(42)

m = generate_monster(1, "Insectoid", major_count=1, util_count=1)
print("mutagens:", m.mutagens)
print("meta:", m.meta)
print("stats:", m.stats)
