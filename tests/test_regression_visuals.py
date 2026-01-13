import random
from mongens.monsterseed import MonsterSeed
from mongens.data.data import SEED_TYPES, SEED_TYPE_DATA
from mongens.data.art_data import PALETTE_BY_TYPE, TYPE_VISUALS


def test_forge_visuals_for_each_type():
    random.seed(12345)
    for i, t in enumerate(SEED_TYPES, start=1):
        # Forge deterministically with no secondary chance
        seed = MonsterSeed.forge(i, primary_type=t, secondary_type=None, secondary_chance=0.0)
        assert seed.form, f"Empty form for type {t}"

        # Validate habitat exists in SEED_TYPE_DATA
        type_entry = SEED_TYPE_DATA.get(t, {})
        habitats = type_entry.get("habitats")
        if isinstance(habitats, dict):
            assert seed.habitat in habitats.keys(), f"Habitat '{seed.habitat}' not in habitats for {t}"
        elif isinstance(habitats, list):
            assert seed.habitat in habitats, f"Habitat '{seed.habitat}' not in habitats for {t}"
        else:
            assert seed.habitat, f"No habitat for {t} and seed.habitat empty"

        # Visual mappings must include the canonical type
        assert t in PALETTE_BY_TYPE, f"Palette missing for type {t}"
        assert t in TYPE_VISUALS, f"TYPE_VISUALS missing for type {t}"
