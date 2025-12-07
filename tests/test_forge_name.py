import pytest
from mongens.monsterseed import MonsterSeed
from mongens.forge_name import forge_monster_name, deterministic_name

# A dummy MonsterSeed for testing purposes
# We can create a fixture later if needed
def create_seed(
    idnum: int,
    primary_type: str,
    secondary_type: str = None,
    mutagens: dict = None,
) -> MonsterSeed:
    """Helper to create a valid MonsterSeed for testing."""
    if mutagens is None:
        mutagens = {"major": [], "utility": []}

    return MonsterSeed(
        idnum=idnum,
        name="",
        species="test_species",
        primary_type=primary_type,
        secondary_type=secondary_type,
        habitat="test_habitat",
        stats={},
        mutagens=mutagens,
        traits=[],
        tempers={},
        meta={},
    )

def test_basic_name_generation():
    """Tests that a name is generated without errors."""
    seed = create_seed(idnum=1, primary_type="Inferno")
    forge_monster_name(seed)
    assert seed.name
    assert isinstance(seed.name, str)
    print(f"Generated name: {seed.name}")

def test_deterministic_generation():
    """Tests that the name generation is deterministic."""
    seed1 = create_seed(idnum=42, primary_type="Aquatic", secondary_type="Sylvan")
    forge_monster_name(seed1)
    name1 = seed1.name

    seed2 = create_seed(idnum=42, primary_type="Aquatic", secondary_type="Sylvan")
    forge_monster_name(seed2)
    name2 = seed2.name

    seed3 = create_seed(idnum=43, primary_type="Aquatic", secondary_type="Sylvan")
    forge_monster_name(seed3)
    name3 = seed3.name

    assert name1 == name2
    assert name1 != name3

def test_epithet_generation():
    """Tests that mutagens correctly generate epithets."""
    mutagens = {"major": [], "utility": ["CosmicInterpreter"]}
    
    # We test deterministic_name directly to force the epithet probability
    name = deterministic_name(
        idnum=101,
        primary_type="Astral",
        secondary_type=None,
        mutagens=mutagens,
        epithet_prob=1.0,  # Force epithet generation
    )

    # Check if one of the expected epithets is in the name
    possible_epithets = ["the Star-Reader", "of Stellar Origin"]
    assert any(e in name for e in possible_epithets)
    print(f"Generated epithet name: {name}")

def test_syllable_fallback_generation(monkeypatch):
    """Tests the syllable-based fallback generator."""
    # This forces the deterministic_name function to use the syllable chain
    monkeypatch.setattr("random.Random.random", lambda self: 0.9)

    seed = create_seed(idnum=202, primary_type="Inferno")
    forge_monster_name(seed)
    
    assert seed.name
    assert isinstance(seed.name, str)
    print(f"Generated fallback name: {seed.name}")


