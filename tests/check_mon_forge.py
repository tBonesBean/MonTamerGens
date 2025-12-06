# tests/check_mon_forge.py
import random

from mongens.mon_forge import generate_monster


random.seed(42)

m = generate_monster(1, "Insect", major_count=1, util_count=1)
print("mutagens:", m.mutagens)
print("meta:", m.meta)
print("stats:", m.stats)
