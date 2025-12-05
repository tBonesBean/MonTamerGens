# MonsterGenerators

This project is a Python package for procedurally generating fantasy monster data. It includes a command-line tool and a library to create monster "seeds" with unique stats, traits, dual-types, and abilities. It can format this data into Pokedex-style catalog entries, raw data for game development, and detailed prompts for AI image generators.

## Features

*   **Dual-Type System**: Monsters are generated with a primary type and have a chance to gain a secondary type, creating complex and unique creatures.
*   **Stat Biasing**: Each monster's stats are intelligently biased based on its primary and secondary types, giving them a distinct feel.
*   **Mutagens**: Apply "mutagens" (major, minor, and utility) to generate unique "wild" instances with special stats, tags, and abilities.
*   **Multiple Output Formats**:
    *   **Canonical Dex Entries**: Generate Pokedex-style entries that describe the pure, base form of a species.
    *   **Unique Instances**: Generate the raw data for a fully randomized "wild" monster, perfect for in-game encounters.
    *   **AI Art Prompts**: Convert monster data into a detailed, style-compliant prompt for image models like DALL-E or Stable Diffusion.
*   **Powerful Command-Line Interface**: A rich CLI with subcommands for accessing all of the generator's features.

## Installation

This project is managed with modern Python packaging standards using `pyproject.toml`.

To install the package for development, clone the repository and run the following command in the project root:

```bash
pip install -e .[dev]
```

*   The `-e` flag installs the package in "editable" mode, so your code changes are immediately reflected.
*   The `[dev]` part installs all the extra tools for development and testing, like `pytest`.

This command also installs the `mongen` command-line tool.


## CLI Usage

The `mongen` tool uses subcommands to access its different features.

### `mongen dexentry`
Generates the "canonical" Pokedex-style entry for a species (base stats + type bias, no mutagens).

**Examples:**
```shell
  # Generate a single dex entry for a random monster
mongen dexentry

  # Generate 5 entries for Verdant monsters and save them to a file
mongen dexentry --primary_type Verdant --count 5 --output ./verdant_dex.txt

  # Generate an entry for a monster that is primarily Geomorph and secondarily Cryoform
mongen dexentry --primary_type Geomorph --secondary_type Cryoform
```

### `mongen unique`
Generates the raw data for a single "wild" monster instance, including randomized mutagens. This is perfect for game encounters.

**Examples:**
```shell
  # Get the raw data for one fully randomized monster
mongen unique

  # Generate a unique Dread monster with a 60% chance of a random secondary type
mongen unique --primary_type Dread --secondary_type random

  # Generate a powerful unique monster with extra mutagens
mongen unique --primary_type Pyro --majors 2 --minors 3
```

### `mongen artprompt`
Generates a detailed prompt for an AI image generator based on a fully realized monster.

**Examples:**
```shell
  # Generate a prompt for a random monster
mongen artprompt

  # Generate a prompt for a Mythic/Electric monster and save it
mongen artprompt -t1 Mythic -t2 Electric -o ./prompts.txt --json
```
*The `--json` flag will also save the monster's raw data, which is useful for regenerating the same image later.*

### `mongen list`
Lists the available data used by the generator.

**Examples:**
```shell
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
    primary_type="Verdant",
    major_count=1,
    minor_count=2,
    util_count=1,
    secondary_type="Geomorph"  # Optional
)

# The result is a MonsterSeed dataclass instance
print(monster.species)
print(monster.stats)
print(monster.elements)
```

### Creating a Dex Entry

You can format a `MonsterSeed` into a human-readable "Pokedex-style" entry.

```python
from mongens.mon_forge import generate_monster
from mongens.dex_entries import dex_formatter

# First, generate a monster
monster = generate_monster(
    idnum=1,
    primary_type="Astral",
    major_count=1,
    minor_count=1,
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
    primary_type="Cryoform",
    secondary_type="Electric",
    major_count=1,
    minor_count=2,
    util_count=1
)

# Construct the art prompt
art_prompt = construct_mon_prompt(monster)
print(art_prompt)
```
