import pytest

from mongens.data.data import BASE_STATS, SEED_TYPES
from mongens.dex_entries import dex_formatter
from mongens.mon_forge import apply_mutagens, forge_seed_monster, generate_monster
from mongens.prompt_engine import construct_mon_prompt


# Mark all tests in this file as being part of the 'generators' suite
@pytest.fixture
def base_monster():
    """Provides a simple, unmodified monster seed for testing."""
    return forge_seed_monster(idnum=1, primary_type="Aquatic", secondary_type=None)


def test_forge_seed_monster_creation():
    """Tests that a seed monster can be created with the correct basic attributes."""
    monster = forge_seed_monster(idnum=10, primary_type="Mineral", secondary_type=None)
    assert monster is not None
    assert monster.idnum == 10
    assert monster.primary_type == "Mineral"
    assert monster.secondary_type is None
    assert monster.species is not None
    assert monster.habitat is not None
    assert isinstance(monster.stats, dict)
    # Check that type biasing was applied (Mineral has modified stats)
    assert monster.stats["DEF"] != BASE_STATS["DEF"]


def test_forge_seed_monster_dual_type():
    """Tests creation with both a primary and secondary type."""
    monster = forge_seed_monster(
        idnum=11, primary_type="Inferno", secondary_type="Mineral"
    )
    assert monster is not None
    assert monster.primary_type == "Inferno"
    assert monster.secondary_type == "Mineral"
    assert "Inferno" in SEED_TYPES
    assert "Mineral" in SEED_TYPES
    # Check that biases from both types were applied
    # Inferno boosts SPATK, Mineral boosts DEF
    assert monster.stats["SPATK"] > BASE_STATS["SPATK"]
    assert monster.stats["DEF"] > BASE_STATS["DEF"]


def test_apply_mutagens():
    """Tests that mutagens correctly modify a monster's stats and mutagens."""
    monster = forge_seed_monster(idnum=1, primary_type="Sylvan", secondary_type=None)

    # Apply mutagens that are known to affect HP
    mutated_monster = apply_mutagens(monster, major_count=1, util_count=1)

    # This is a bit non-deterministic since mutagens are chosen randomly.
    # A more robust test would mock 'random.choice' to select a specific mutagen.
    assert mutated_monster.stats != BASE_STATS
    assert mutated_monster is not None
    assert mutated_monster.mutagens["major"]  # Should have one major


def test_generate_monster_full_process():
    """
    Tests the end-to-end generation process.
    """
    monster = generate_monster(
        idnum=99, primary_type="Inferno", major_count=1, util_count=1
    )
    assert monster is not None
    assert monster.primary_type == "Inferno"
    assert len(monster.mutagens["major"]) == 1
    assert len(monster.mutagens["utility"]) == 1


def test_dex_formatter(base_monster):
    """Tests that the dex formatter produces a non-empty string."""
    dex_entry = dex_formatter(base_monster)
    assert isinstance(dex_entry, str)
    assert "#001" in dex_entry
    assert "Aquatic" in dex_entry
    assert "Base Profile:" in dex_entry


def test_prompt_engine():
    """Tests that the prompt engine produces a valid prompt string."""
    monster = generate_monster(
        idnum=42, primary_type="Aerial", major_count=1, util_count=1
    )
    prompt = construct_mon_prompt(monster)

    assert isinstance(prompt, str)
    assert "32-bit pixel art" in prompt
    assert "Subject: A" in prompt
    assert "Aerial type" in prompt
    assert "Pose:" in prompt


@pytest.mark.parametrize("monster_type", SEED_TYPES)
def test_all_monster_types_generate(monster_type):
    """A powerful test to ensure no monster type crashes the generator."""
    try:
        monster = generate_monster(
            idnum=1, primary_type=monster_type, major_count=1, util_count=1
        )
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
