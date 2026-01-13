from pathlib import Path

from .forge_name import format_dual_type
from typing import List

from .mon_forge import apply_mutagens, forge_seed_monster
from .monster_cache import OUTPUT_PATH, save_monster
from .monsterseed import MonsterSeed, choose_type_pair


def _summarize_stats(stats: dict) -> str:
    """
    Summary:
        Turns the raw stats dictionary into a compact 'stat line' string.

    Args:
        stats: A dictionary of monster stats.

    Returns:
        A formatted string summarizing the monster's stats.
        Example: 'HP 62 • ATK 54 • DEF 60 • SPATK 55 • SPDEF 58 • SPD 49'
    """
    order = ["HP", "ATK", "DEF", "SPATK", "SPDEF", "SPD", "ACC", "EVA", "LUCK"]
    pieces = []

    for key in order:
        if key in stats:
            pieces.append(f"{key} {stats[key]}")
    stat_summary = str(" • ".join(pieces) + "\n")
    return stat_summary


def _summarize_physical_details(
    physical_traits: List[str], held_item: str | None
) -> str:
    """
    Summary:
        Formats the physical traits and held item into a readable block.

    Args:
        physical_traits: A list of strings describing the monster's physical traits.
        held_item: An optional string for the item the monster is holding.

    Returns:
        A formatted string detailing the physical traits and held item, or a default
        message if no details are available.
    """
    parts = []
    if physical_traits:
        parts.append(f"Physical Traits: {', '.join(physical_traits)}")
    if held_item:
        parts.append(f"Observed carrying: {held_item}")

    if not parts:
        return "Distinctive features have not yet been documented."

    return "\n".join(parts)


def dex_formatter(seed: MonsterSeed) -> str:
    """
    Summary:
        Main formatter that takes a fully prepared MonsterSeed and returns a
        Pokédex-style text block.

    Args:
        seed: The MonsterSeed object to format.

    Returns:
        A string containing the formatted Pokédex-style entry.
    """
    num = seed.idnum
    name = seed.name
    species = seed.species
    habitat = seed.habitat
    primary_type = seed.primary_type
    secondary_type = seed.secondary_type
    mutagens = seed.mutagens
    traits_line = _summarize_physical_details(seed.physical_traits, seed.held_item)
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
    header_line = f"#{num:03d}: '{name}' --- a(n) {species} monster"
    lines.append(header_line)
    lines.append("")

    # Type (use formatted dual-type when available)
    if not secondary_type:
        type_line = f"  -Type: {primary_type}"
    else:
        # prefer adjective-noun formatting for readability
        formatted = format_dual_type(primary_type, secondary_type, style="adj-n")
        type_line = f"  -Types: {formatted} ({primary_type}/{secondary_type})"
    lines.append(type_line)
    lines.append("")

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
    Summary:
        Forges a batch of monsters, formats each as a Dex entry, and optionally
        writes them to a text file.

    Args:
        count: The number of monsters to generate.
        major_count: The number of major mutagens for each monster.
        util_count: The number of utility mutagens for each monster.
        output_path: The path to the file to save the entries to.

    Returns:
        A list of strings, where each string is a formatted dex entry.
    """
    entries: list[str] = []

    for i in range(count):
        dex_number = i + 1
        seed = None
        while seed is None:
            try:
                primary_type, secondary_type = choose_type_pair(secondary_chance=0.5)
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
        save_monster(full_seed)  # Also save the generated seed to the JSONL cache
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
        count=75, major_count=1, util_count=1, output_path=str(OUTPUT_PATH)
    )

    # Also echo the first one so you can sanity check in the console
    print(dexstack[0])
