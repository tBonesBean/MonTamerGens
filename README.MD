# Monster Generators

This project is a Python package for procedurally generating fantasy monster data. It includes tools for creating monster "seeds" with unique stats, traits, and elements, and for formatting this data into detailed descriptions or image generation prompts.

## Features

*   **Monster Forging**: Generate foundational monster data including species, type, habitat, and base stats.
*   **Mutagens**: Apply "mutagens" to modify monster stats and grant them special tags, resistances, and weaknesses.
*   **Dex Formatter**: Convert monster data into a human-readable, Pokédex-style entry.
*   **Prompt Engine**: Translate monster data into a detailed, style-compliant prompt for use with image generation models like DALL-E or Stable Diffusion.
*   **Command-Line Interface**: A simple CLI for generating monsters.

## Installation

To install the package for development, clone the repository and run the following command in the project root:

```shell
pip install -e .
```

This installs the package in "editable" mode, so changes to the source files will be immediately reflected.

## Usage

Once installed, you can use the command-line script `mongen` to generate monsters:

```shell
# Generate a single monster of a random type
mongen unique

# Generate a monster of a specific primary type
mongen unique --primary_type Geomorph

# Generate a monster with a primary and secondary type
mongen unique --primary_type Geomorph --secondary_type Aquatic

# Generate a batch of 5 monsters and save them to a file
mongen dexentry --count 5 --output dex.txt

# Subcommands
mongen list         # list available data like monster types, habitats, etc.
mongen dexentry     # generate canonical, templated, Pokedex-style entries for a species (no mutagens)
mongen unique       # generate a unique monster with mutagens

# Examples
mongen list --types --mutagens
mongen unique --primary_type Pyro
mongen dexentry --primary_type Geomorph --count 20 --output dex.txt
```

You can also use the library directly in your Python code:

```python
from .mon_forge import generate_monster
from mongens.dex_entries import dex_formatter

# Generate a single monster
monster = generate_monster(primary_type="Pyro", idnum=1, major_count=1, minor_count=2, util_count=1)

# Generate a dual-type monster
dual_type_monster = generate_monster(primary_type="Pyro", secondary_type="Geomorph", idnum=2, major_count=1, minor_count=2, util_count=1)

# Format it as a dex entry
dex_entry = dex_formatter(monster)
print(dex_entry)

dex_entry_dual = dex_formatter(dual_type_monster)
print(dex_entry_dual)
```
