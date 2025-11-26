from pathlib import Path
from random import choice, random
from typing import List

from .data.data import (
	SEED_TYPES
)
from .mon_forge import (
	MonsterSeed,
	apply_mutagens,
	forge_seed_monster
)


# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, project_root)

def _summarize_stats(stats: dict) -> str:
    """
    Turn the raw stats dictionary into a compact 'stat line' string.
    Example: 'HP 62 • ATK 54 • DEF 60 • SPATK 55 • SPDEF 58 • SPD 49'
    """
    order = ["HP", "ATK", "DEF", "SPATK", "SPDEF", "SPD"]
    pieces = []
    for key in order:
        if key in stats:
            pieces.append(f"{key} {stats[key]}")
    return " • ".join(pieces)


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
        parts.append(appearance)
    if gear:
        parts.append(f"often seen with {gear.lower()}")
    if quirk:
        parts.append(f"and is known for {quirk.lower()}")

    # Join nicely and add a period.
    text = ", ".join(parts)
    if not text.endswith("."):
        text += "."
    return text


def dex_formatter(seed: MonsterSeed) -> str:
    """
    Main formatter: takes a fully prepared MonsterSeed and
    returns a Pokédex-style text block.
    """
    # Basic identity
    num = seed.idnum
    name = seed.species
    habitat = seed.habitat
    primary_type = seed.primary_type
    secondary_type = seed.secondary_type

    # Elements and traits
    elems_major = ", ".join(seed.elements.get("major", []))
    elems_minor = ", ".join(seed.elements.get("minor", []))
    elems_utility = ", ".join(seed.elements.get("utility", []))

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
    lines = [f"#{num:03d}  {name}"]

    # Header
    type_line = f"Primary Type: {primary_type}"
    if secondary_type:
        type_line += f" / Secondary Type: {secondary_type}"
    lines.append(type_line)

    if elems_major:
        lines.append(f"Elements: {elems_major}")
    if elems_minor:
        lines.append(f"  Minor: {elems_minor}")
    if elems_utility:
        lines.append(f"  Utility: {elems_utility}")

    lines.append("")  # blank line

    # Flavor text
    lines.append(habitat)
    lines.append(traits_line)
    lines.append("")  # blank line

    # Stats
    lines.append(f"Base Profile: {stat_line}")

    # Optional meta info
    if tags_str or resist_str or weak_str:
        lines.append("")
        if tags_str:
            lines.append(f"Tags: {tags_str}")
        if resist_str:
            lines.append(f"Resists: {resist_str}")
        if weak_str:
            lines.append(f"Weak to: {weak_str}")

    return "\n".join(lines)


def generate_dex_batch(
        count: int,
        major_count: int,
        minor_count: int,
        util_count: int,
        output_path: str | Path | None = None,
) -> list[str]:
    """
    Forge a batch of monsters, format each as a Dex entry, and
    optionally write them to a text file.

    Returns the list of entry strings either way.
    """
    entries: list[str] = []

    for i in range(count):
        dex_number = i + 1
        seed = None
        while seed is None:
            try:
                primary_type = choice(SEED_TYPES)
                secondary_type = None
                if random() < 0.5:  # 50% chance of having a secondary type
                    possible_secondary_types = [t for t in SEED_TYPES if t != primary_type]
                    if possible_secondary_types:
                        secondary_type = choice(possible_secondary_types)

                seed = forge_seed_monster(
                    primary_type=primary_type,
                    idnum=dex_number,
                    secondary_type=secondary_type
                )
            except ValueError:
                continue

        # Layer 2: apply mutagens to flesh out stats/elements/meta
        full_seed = apply_mutagens(
            seed,
            major_count=major_count,
            minor_count=minor_count,
            util_count=util_count
        )

        # Turn the fully-forged seed into Dex text
        entry_text = dex_formatter(full_seed)
        entries.append(entry_text)

    # If the caller gave us a path, write everything to disk
    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            for idx, entry in enumerate(entries):
                f.write(entry)
                f.write("\n")  # newline after each entry
                if idx != len(entries) - 1:
                    # divider between entries, but not after the last one
                    f.write("\n" + "-" * 60 + "\n\n")

    return entries


if __name__ == "__main__":
    # Example: generate 50 entries, each with 2 minor and 1 bonus mutagen,
    # and save them to a text file.
    dexstack = generate_dex_batch(
        count=75,
        major_count=1,
        minor_count=2,
        util_count=1,
        output_path="D:/Projects/MonsterDex/dex_batch_001.txt",
    )

    # Also echo the first one so you can sanity check in the console
    print(dexstack[0])
