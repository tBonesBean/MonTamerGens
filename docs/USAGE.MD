
###### *USAGE.MD*

-----

# Command-Line Interface Guide

The `mongens` command-line tool provides direct access to the core generation, formatting, and prompt-writing functions of the package. It is designed to be used via the terminal after installing the `mongens` package (or while developing it, e.g., using `python -m mongens.cli`).

The primary entry point is the main program command, which we will refer to as `mongens`.

## General Usage

The tool uses subcommands to handle different tasks. To get specific help on any command, use the `--help` flag after the subcommand:

```bash
mongens <command> --help
```

-----

## 1\. `list` Command 📑

Lists all available data elements used by the generator, such as monster types, habitats, and mutagen names.

### Syntax

```bash
mongens list [FLAGS]
```

### Flags

| Flag | Description |
| :--- | :--- |
| `--types` | List all available monster **types** (e.g., Inferno, Aquatic, Plant). |
| `--habitats` | List all available **habitats** (e.g., Desert, Volcanic, Swamp). |
| `--mutagens` | List all available **mutagens** (major and utility). |

### Examples

| Goal | Command |
| :--- | :--- |
| List all available monster types. | `mongens list --types` |
| List all available habitats and mutagens. | `mongens list --habitats --mutagens` |

-----

## 2\. `dexentry` Command 📖

Generates canonical, Pokedex-style entries for a species. These entries are based on the core definition of the species (primary/secondary type) and can include a set number of mutagens for a "template" canonical form.

### Syntax

```bash
mongens dexentry [OPTIONS] [FLAGS]
```

### Options

| Option | Shorthand | Type | Default | Choices | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `--primary_type` | `-t1` | `str` | `"random"` | `[Type names, "random"]` | Primary type of the monster. |
| `--secondary_type` | `-t2` | `str` | `"random"` | `[Type names, "random"]` | Secondary type of the monster. Defaults to primary type if primary is 'random' and secondary is 'random'. |
| `--count` | `-c` | `int` | `1` | | Number of entries to generate. |
| `--majors` | | `int` | `1` | | Number of major mutagens to apply. |
| `--utils` | | `int` | `1` | | Number of utility mutagens to apply. |
| `--id_start` | | `int` | `1` | | Starting ID number for the entries. |
| `--output` | | `str` | `None` | | Path to save the output text file. |

### Flags

| Flag | Description |
| :--- | :--- |
| `--id_skip` | Don't assign sequential ID numbers (default: assign IDs). |
| `--no_mutagens` | Don't apply mutagens (overrides `--majors` and `--utils`). |

### Examples

| Goal | Command |
| :--- | :--- |
| Generate a single, random species entry. | `mongens dexentry` |
| Generate 10 **Ancient/Dread** entries, starting at ID 100, and save them to a file. | `mongens dexentry -t1 Ancient -t2 Dread -c 10 --id_start 100 --output ./canon_dex.txt` |
| Generate 5 random entries without assigning IDs or applying mutagens. | `mongens dexentry -c 5 --id_skip --no_mutagens` |

-----

## 3\. `prompt` Command 🖼️

Generates a detailed, style-compliant AI art prompt for a unique monster instance. This command is focused on creating a **single instance** of a monster based on its attributes.

### Syntax

```bash
mongens prompt [OPTIONS] [FLAGS]
```

### Options

| Option | Shorthand | Type | Default | Choices | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `--primary_type` | `-t1` | `str` | `"random"` | `[Type names, "random"]` | Primary type of the monster. |
| `--secondary_type` | `-t2` | `str` | `"random"` | `[Type names, "random"]` | Secondary type of the monster. |
| `--name` | `-n` | `str` | `None` | | A specific species name to use (a random one is chosen if omitted). |
| `--output` | | `str` | `None` | | Path to save the output text file. |

### Flags

| Flag | Description |
| :--- | :--- |
| `--json` | Also save the raw monster seed data as a JSON file alongside the text prompt. |

### Examples

| Goal | Command |
| :--- | :--- |
| Generate a completely random monster prompt. | `mongens prompt` |
| Generate a prompt for a **Plant/Aquatic** monster and save the prompt and the raw data. | `mongens prompt -t1 Plant -t2 Aquatic --output ./plant_prompt.txt --json` |
| Generate a prompt for a **Verdant** species named "Bloom Beast." | `mongens prompt -t1 Verdant -n "Bloom Beast"` |
