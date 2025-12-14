import re

from mongens.forge_name import format_dual_type
from mongens.monsterseed import MonsterSeed
from mongens.dex_entries import dex_formatter


def make_seed(primary: str, secondary: str | None) -> MonsterSeed:
    # Minimal, deterministic MonsterSeed instance for formatting tests
    return MonsterSeed(
        idnum=1,
        name="Testling",
        species="TestSpecies",
        primary_type=primary,
        secondary_type=secondary,
        habitat="TestHabitat",
        stats={"HP": 100, "ATK": 50},
        mutagens={"major": [], "utility": []},
        physical_traits=["spiky"],
        held_item=None,
        tempers={"mood": "neutral", "affinity": "none"},
        meta={},
    )


def test_format_dual_type_adj_n():
    out = format_dual_type("Inferno", "Mineral", style="adj-n")
    assert out == "Ore Inferno"


def test_format_dual_type_hyphen():
    out = format_dual_type("Beast", "Astral", style="hyphen")
    assert out == "Astral-Beast"


def test_format_dual_type_epithet():
    out = format_dual_type("Sylvan", "Frost", style="epithet")
    assert out == "Sylvan, the Frost"


def test_dex_formatter_includes_formatted_type():
    seed = make_seed("Inferno", "Mineral")
    text = dex_formatter(seed)
    # Should include our formatted type and the raw type pair
    assert "Ore Inferno" in text
    assert "(Inferno/Mineral)" in text
