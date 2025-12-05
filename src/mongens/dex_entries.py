from pathlib import Path
from random import choice, random
from typing import List, Optional, Any

from .data import data
from .data import art_data
from .mon_forge import forge_seed_monster, apply_mutagens, generate_monster
from .monsterseed import MonsterSeed, weighted_choice


def _summarize_stats(stats: dict) -> str:
    """
    Turn the raw stats dictionary into a compact 'stat line' string.
    Example: 'HP 62 • ATK 54 • DEF 60 • SPATK 55 • SPDEF 58 • SPD 49'
    """

    order = ["HP", "ATK", "DEF", "SPATK", "SPDEF", "SPD"]
    int_order = ["ACC", "EVA", "LUCK"]
    int_pieces = []
    pieces = []

    for key in order:
        if key in stats:
            pieces.append(f"{key} {stats[key]}")
    for key in int_order:
        if key in stats:
            int_pieces.append(f"{key} {stats[key]}")
    stat_summary = str(
        " • ".join(pieces) + "\n" + "    -Intangibles: " + " • ".join(int_pieces)
    )
    return stat_summary


def _summarize_traits(traits: List[str]) -> str:
    """
    Turn the 3 trait phrases into one readable sentence fragment.
    We treat them as: appearance / gear / quirk.
    """
    if not traits:
        return "Details about this creature are still under study."

    # Pad to length 3 so we don't crash if a future seed has fewer.
    t = (traits + ["", "", ""])[:3]

    # Ensure all traits are strings
    str_traits = []
    for trait in t:
        if isinstance(trait, list):
            str_traits.append(" ".join(trait))
        else:
            str_traits.append(trait)

    appearance, gear, quirk = str_traits

    parts = []
    if appearance:
        parts.append(f"Appearance: {appearance}")
    if gear:
        parts.append(f"Token: {gear}")
    if quirk:
        parts.append(f"Recorded Quirk: {quirk}")

    # Join nicely and add a period.
    text = "\n".join(parts)
    if not text.endswith("."):
        text += "."
    return text


def dex_formatter(seed: MonsterSeed) -> str:
    """
    Main formatter: takes a fully prepared MonsterSeed and returns a Pokédex-style text block.
    """
    num = seed.idnum
    name = seed.name
    species = seed.species
    habitat = seed.habitat
    primary_type = seed.primary_type
    secondary_type = seed.secondary_type
    mutagens = seed.mutagens
    traits_line = _summarize_traits(seed.traits)
    stat_line = _summarize_stats(seed.stats)
    # Simple tags summary from meta, if present
    tags = seed.meta.get("tags", []) or []
    resist = seed.meta.get("resist", []) or []
    weak = seed.meta.get("weak", []) or []

    tags_str = ", ".join(tags)
    resist_str = ", ".join(resist)
    weak_str = ", ".join(weak)

    # Build the final entry text
    lines = []
    sep_line = f"{'-' * 60}"

    lines.append(sep_line)
    lines.append("")
    header_line = f"#{num:03d}:   ({name})"
    lines.append(header_line)

    if not secondary_type:
        type_line = f"  - {primary_type} '{species}'"
    else:
        type_line = f"  - {primary_type}/{secondary_type} '{species}'"
    lines.append(type_line)

    # Mutagens
    mutagen_lines = []
    if mutagens["major"]:
        mutagen_lines.append(f"Documented Near-Lumen Mutagen: {mutagens['major']}")
    if mutagens["utility"]:
        mutagen_lines.append(f"Known Utility: {mutagens['utility']}")
    lines.append(" | ".join(mutagen_lines))
    lines.append("\n")  # blank line

    # Stats
    lines.append(f"Base Profile: {stat_line}")
    lines.append("\n")

    # Flavor text
    habitat_line = f"Habitat: {habitat}"
    lines.append(habitat_line)
    lines.append("\n")
    lines.append(traits_line)

    # Optional meta info
    if tags_str or resist_str or weak_str:
        lines.append("")
        if tags_str:
            lines.append(f"Tags: {tags_str}")
        if resist_str:
            lines.append(f"Resists: {resist_str}")
        if weak_str:
            lines.append(f"Weak To: {weak_str}")

    return "\n".join(lines)


def generate_dex_batch(
    count: int, major_count: int, util_count: int, output_path: str
) -> list[str]:
    """
    Forge a batch of monsters, format each as a Dex entry, and optionally write them to a text file.
      Returns the list of entry strings either way.
    """
    entries: list[str] = []

    for i in range(count):
        dex_number = i + 1
        seed = None
        while seed is None:
            try:
                primary_type = choice(data.SEED_TYPES)
                secondary_type = None
                if random() < 0.5:  # 50% chance of having a secondary type
                    possible_secondary_types = [
                        t for t in SEED_TYPES if t != primary_type
                    ]
                    if possible_secondary_types:
                        secondary_type = choice(possible_secondary_types)

                seed = forge_seed_monster(
                    idnum=dex_number,
                    primary_type=primary_type,
                    secondary_type=secondary_type,
                )
            except ValueError:
                continue

        # Layer 2: apply mutagens to flesh out stats/mutagens/meta
        full_seed = apply_mutagens(
            seed,
            major_count=major_count,
            util_count=util_count,
        )

        # Turn the fully-forged seed into Dex text
        entry_text = dex_formatter(full_seed)
        entries.append(entry_text)

    # If the caller gave us a path, write everything to disk
    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("a", encoding="utf-8") as f:
            for idx, entry in enumerate(entries):
                f.write(entry)
                f.write("\n")  # newline after each entry
                if idx != len(entries) - 1:
                    # divider between entries, but not after the last one
                    f.write("-" * 60 + "\n\n")

    return entries


if __name__ == "__main__":
    # Example: generate 50 entries, each with 1 major and 1 bonus mutagen,
    # and save them to a text file.
    dexstack = generate_dex_batch(
        count=75,
        major_count=1,
        util_count=1,
        output_path="D:/Projects/MonsterDex/dex_batch_001.txt",
    )

    # Also echo the first one so you can sanity check in the console
    print(dexstack[0])
