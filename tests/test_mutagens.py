# tests/test_mutagens.py
import pytest
from mongens.mon_forge import apply_mutagens
from mongens.monsterseed import MonsterSeed
from mongens.data.data import MAJOR_MODS

# Fixture to create a basic monster seed
@pytest.fixture
def monster_seed():
    def _monster_seed(primary_type, secondary_type=None):
        # A simplified monster seed for testing purposes
        seed = MonsterSeed(
            idnum=1,
            name="Test Name",
            primary_type=primary_type,
            secondary_type=secondary_type,
            species="Test Species",
            habitat="Test Habitat",
            stats={"HP": 100, "ATK": 50, "DEF": 50, "SPATK": 50, "SPDEF": 50, "SPD": 50},
            meta={},
            mutagens={},
            physical_traits=[],
            held_item=None,
            tempers={}
        )
        return seed
    return _monster_seed

def test_mutagen_allowed_type_filtering(monster_seed, monkeypatch):
    """
    Tests that the mutagen list is correctly filtered based on allowed types.
    It checks if 'Starwarden' (only for Mythic, Astral, Anomalous) is available
    for a Mythic monster but not for a Beast monster.
    """
    # Mock the weighted sampling function to just return the keys of the dict it receives.
    # This lets us inspect the list of "available" mutagens.
    available_majors_for_call = {}
    def mock_weighted_sample(weight_dict, k):
        # Only capture the first call per test, which will be for major mutagens.
        if not available_majors_for_call:
            available_majors_for_call.update(weight_dict)
        return []

    monkeypatch.setattr(
        "mongens.mon_forge.weighted_sample_without_replacement", mock_weighted_sample
    )

    # --- Test Case 1: Mythic monster ---
    # 'Starwarden' should be an option.
    mythic_monster = monster_seed("Mythic")
    apply_mutagens(mythic_monster, major_count=1)
    
    assert "Starwarden" in available_majors_for_call, \
        "Starwarden should be in the list of available majors for a Mythic monster"

    # --- Test Case 2: Beast monster ---
    # Reset the captured dict and run again for the Beast monster.
    available_majors_for_call.clear()
    beast_monster = monster_seed("Beast")
    apply_mutagens(beast_monster, major_count=1)

    assert "Starwarden" not in available_majors_for_call, \
        "Starwarden should NOT be in the list of available majors for a Beast monster"

def test_mutagen_synergy_bonus_application(monster_seed, monkeypatch):
    """
    Tests that the synergy bonus is correctly applied to the weighting.
    'Starwarden' is allowed for both Mythic and Astral types, but has a 1.4x
    synergy bonus for Mythic. This test verifies the final weight is higher
    for the Mythic monster.
    """
    # This mock will be used by both calls to apply_mutagens
    captured_weights = {}
    def mock_weighted_sample(weight_dict, k):
        # Only capture the first call's dictionary (majors).
        # On the second run (Astral), we overwrite it.
        captured_weights.update(weight_dict)
        return []

    monkeypatch.setattr(
        "mongens.mon_forge.weighted_sample_without_replacement", mock_weighted_sample
    )

    # --- Run for Mythic monster ---
    mythic_monster = monster_seed("Mythic")
    apply_mutagens(mythic_monster, major_count=1)
    # The 'captured_weights' dict now holds the available majors for the Mythic monster
    available_majors_for_mythic = captured_weights.copy()

    # --- Run for Astral monster ---
    captured_weights.clear() # Clear before the next run
    astral_monster = monster_seed("Astral")
    apply_mutagens(astral_monster, major_count=1)
    # The 'captured_weights' dict now holds the available majors for the Astral monster
    available_majors_for_astral = captured_weights.copy()
    
    # --- Compare the calculated weights ---
    assert "Starwarden" in available_majors_for_mythic
    assert "Starwarden" in available_majors_for_astral

    weight_mythic = available_majors_for_mythic["Starwarden"]
    weight_astral = available_majors_for_astral["Starwarden"]

    assert weight_mythic > weight_astral, \
        "Weight for Starwarden should be higher for a Mythic monster due to synergy bonus"

    # Verify the math is correct (approximately)
    expected_synergy = MAJOR_MODS["Starwarden"]["synergy_bonus"]["Mythic"]
    assert pytest.approx(weight_mythic) == weight_astral * expected_synergy, \
        "Mythic weight should be astral weight times the synergy bonus"
