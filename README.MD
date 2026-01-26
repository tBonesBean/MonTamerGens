# MonsterGenerators

Last updated: 2026-01-19 12:30:00 -07:00

This project is a Python package for procedurally generating fantasy monster data. It includes a command-line tool and a library to create monster "seeds" with unique stats, traits, dual-types, and abilities. It can format this data into Pokedex-style catalog entries, raw data for game development, and detailed prompts for AI image generators.

## Changelog

### 2026-01-13

- Updated documentation and examples to use the canonical type taxonomy.
- Clarified mutagen categories and CLI flag usage.
- Added documentation update stamps across core project docs.

## Features

- **Dual-Type System**: Monsters are generated with a primary type and have a chance to gain a secondary type, creating complex and unique creatures.
- **Stat Biasing**: Each monster's stats are intelligently biased based on its primary and secondary types, giving them a distinct feel.
- **Mutagens**: Apply "mutagens" (major and utility) to generate unique "wild" instances with special stats, tags, and abilities.
- **Re-roll Attributes**: Fine-tune generated monsters by re-rolling specific attributes like traits or major mutagens.
- **Multiple Output Formats**:
    - **Canonical Dex Entries**: Generate Pokedex-style entries that describe the pure, base form of a species.
    - **Unique Instances**: Generate the raw data for a fully randomized "wild" monster, perfect for in-game encounters.
    - **AI Art Prompts**: Convert monster data into a detailed, style-compliant prompt for image models like DALL-E or Stable Diffusion.
- **Powerful Command-Line Interface**: A rich CLI with subcommands for accessing all of the generator's features.

## Installation

This project is managed with modern Python packaging standards using `pyproject.toml`.

To install the package for development, clone the repository and run the following command in the project root:

```powershell
pip install -e .[dev]
```

- The `-e` flag installs the package in "editable" mode, so your code changes are immediately reflected.
- The `[dev]` part installs all the extra tools for development and testing, like `pytest`.

This command also installs the `mongen` command-line tool.

## CLI Usage

The `mongen` tool uses subcommands to access its different features.

### `mongen dexentry`

Generates the "canonical" Pokedex-style entry for a species (base stats + type bias, no mutagens).

**Examples:**

```powershell
  # Generate a single dex entry for a random monster
mongen dexentry

  # Generate 5 entries for Bloom monsters and save them to a file
mongen dexentry --primary_type Bloom --count 5 --output ./bloom_dex.txt

  # Generate an entry for a monster that is primarily Axiom and secondarily Flow
mongen dexentry --primary_type Axiom --secondary_type Flow
```

### `mongen unique`

Generates the raw data for a single "wild" monster instance, including randomized mutagens. This is perfect for game encounters.

**Examples:**

```powershell
  # Get the raw data for one fully randomized monster
mongen unique

  # Generate a unique Nadir monster with a 60% chance of a random secondary type
mongen unique --primary_type Nadir --secondary_type random

  # Generate a powerful unique monster with extra mutagens
mongen unique --primary_type Idol --majors 2 --utils 1
```

### `mongen reroll`

Re-rolls attributes of a previously generated monster. This is useful for fine-tuning a monster you like without starting from scratch. Each re-roll creates a _new_ monster with a new PIN.

**Examples:**

```powershell
  # Re-roll the traits of a monster with a given PIN
  mongen reroll <PIN> --traits

  # Re-roll the major mutagen of a monster with a given PIN
  mongen reroll <PIN> --majors
```

_You can find a monster's PIN in the output of the `unique` command or in the cached data._

### `mongen artprompt`

Generates a detailed prompt for an AI image generator based on a fully realized monster.

**Examples:**

```powershell
  # Generate a prompt for a random monster
mongen artprompt

  # Generate a prompt for a Geist/Spur monster and save it
mongen artprompt -t1 Geist -t2 Spur -o ./prompts.txt --json
```

_The `--json` flag will also save the monster's raw data, which is useful for regenerating the same image later._

### `mongen list`

Lists the available data used by the generator.

**Examples:**

```powershell
  # List all available primary monster types
mongen list --types

  # List all available mutagens
mongen list --mutagens
```

## Library Usage

In addition to the CLI, you can use `MonsterGenerators` as a Python library to integrate monster generation into your own applications.

### Generating a Monster

The core of the library is the `generate_monster` function, which creates a `MonsterSeed` object containing the monster's data.

```python
from mongens.mon_forge import generate_monster

  # Generate a complete monster with a primary type and a few mutagens
monster = generate_monster(
    idnum=1,
    primary_type="Bastion",
    secondary_type="Axiom",
    major_count=1,
    util_count=1,
)

  # The result is a MonsterSeed dataclass instance
print(monster.species)
print(monster.stats)
print(monster.mutagens)
```

### Creating a Dex Entry

You can format a `MonsterSeed` into a human-readable "Pokedex-style" entry.

```python
from mongens.mon_forge import generate_monster
from mongens.dex_entries import dex_formatter

  # First, generate a monster
monster = generate_monster(
    idnum=1,
    primary_type="Geist",
    major_count=1,
    util_count=0
)

# Then, format it into a dex entry
dex_entry = dex_formatter(monster)
print(dex_entry)
```

### Generating an AI Art Prompt

The library can also generate a detailed prompt for an AI image generator based on a monster's data.

```python
from mongens.mon_forge import generate_monster
from mongens.prompt_engine import construct_mon_prompt

  # Generate a visually interesting monster
monster = generate_monster(
    idnum=42,
    primary_type="Mire",
    secondary_type="Rift",
    major_count=1,
    util_count=1
)

  # Construct the art prompt
art_prompt = construct_mon_prompt(monster)
print(art_prompt)
```
