from pytest import mark

from mongens.dex_entries import dex_formatter
from mongens.mon_forge import forge_seed_monster, apply_mutagens, generate_monster
from mongens.prompt_engine import construct_mon_prompt
from mongens.seed_data_attr import SEED_TYPES, BASE_STATS

# Mark all tests in this file as being part of the 'generators' suite
pytestmark = mark.generators()


@pytest.fixture
def base_monster():
    """Provides a simple, unmodified monster seed for testing."""
    return forge_seed_monster(primary_type="Neutral", idnum=1)


def test_forge_seed_monster_creation():
    """Tests that a seed monster can be created with the correct basic attributes."""
    monster = forge_seed_monster(primary_type="Geomorph", idnum=10)
    assert monster is not None
    assert monster.idnum == 10
    assert monster.primary_type == "Geomorph"
    assert monster.secondary_type is None
    assert monster.species is not None
    assert monster.habitat is not None
    assert isinstance(monster.stats, dict)
    # Check that type biasing was applied (Geomorph has modified stats)
    assert monster.stats["DEF"] != BASE_STATS["DEF"]


def test_forge_seed_monster_dual_type():
    """Tests creation with both a primary and secondary type."""
    monster = forge_seed_monster(primary_type="Pyro", secondary_type="Geomorph", idnum=11)
    assert monster is not None
    assert monster.primary_type == "Pyro"
    assert monster.secondary_type == "Geomorph"
    assert "Pyro" in monster.elements["main"]
    assert "Geomorph" in monster.elements["main"]
    # Check that biases from both types were applied
    # Pyro boosts SPATK, Geomorph boosts DEF
    assert monster.stats["SPATK"] > BASE_STATS["SPATK"]
    assert monster.stats["DEF"] > BASE_STATS["DEF"]


def test_apply_mutagens():
    """Tests that mutagens correctly modify a monster's stats and elements."""
    monster = forge_seed_monster(primary_type="Verdant", idnum=1)
    original_hp = BASE_STATS["HP"]

    # Apply mutagens that are known to affect HP
    mutated_monster = apply_mutagens(monster, major_count=1, minor_count=1, util_count=1)

    # This is a bit non-deterministic since mutagens are chosen randomly.
    # A more robust test would mock 'random.choice' to select a specific mutagen.
    assert mutated_monster.stats["HP"] != original_hp
    assert mutated_monster is not None
    assert mutated_monster.elements["major"]  # Should have one major element


def test_generate_monster_full_process():
    """
    Tests the end-to-end generation process.
    """
    monster = generate_monster(primary_type="Pyro", idnum=99, major_count=1, minor_count=1, util_count=1)
    assert monster is not None
    assert monster.primary_type == "Pyro"
    assert len(monster.elements["major"]) == 1
    assert len(monster.elements["minor"]) == 1
    assert len(monster.elements["utility"]) == 1


def test_dex_formatter(base_monster):
    """Tests that the dex formatter produces a non-empty string."""
    dex_entry = dex_formatter(base_monster)
    assert isinstance(dex_entry, str)
    assert "#001" in dex_entry
    assert "Primary Type: Neutral" in dex_entry
    assert "Base Profile:" in dex_entry


def test_prompt_engine():
    """Tests that the prompt engine produces a valid prompt string."""
    monster = generate_monster(primary_type="Avian", idnum=42, major_count=1, minor_count=2, util_count=1)
    prompt = construct_mon_prompt(monster)

    assert isinstance(prompt, str)
    assert "32-bit pixel art sprite" in prompt
    assert "Subject: A" in prompt
    assert "Avian type" in prompt
    assert "Pose:" in prompt


@pytest.mark.parametrize("monster_type", SEED_TYPES)
def test_all_monster_types_generate(monster_type):
    """A powerful test to ensure no monster type crashes the generator."""
    try:
        monster = generate_monster(monster_type, 1, 1, 1, 1)
        assert monster is not None
        dex_entry = dex_formatter(monster)
        assert isinstance(dex_entry, str)
        prompt = construct_mon_prompt(monster)
        assert isinstance(prompt, str)
    except Exception as e:
        pytest.fail(f"Generator failed for type '{monster_type}': {e}")

# To run these tests:
# 1. Install pytest: pip install pytest
# 2. Navigate to your project root in the terminal.
# 3. Run the command: pytest
