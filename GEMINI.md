# MonTamerGens

## Project Overview

This project, `MonTamerGens`, is a Python package designed for the procedural generation of fantasy monster data. It provides a command-line tool (`mongen`) and a library to create detailed and unique monsters. Key features include a dual-type system, stat biasing based on type, the application of "mutagens" for unique variations, and the ability to format the generated data into various outputs like Pokedex-style entries, raw data for game development, or prompts for AI image generators.

The project is structured as a standard Python package with a `src` directory containing the `mongens` module. The core logic is split into several modules:
- `cli.py`: Implements the command-line interface.
- `mon_forge.py`: Contains the main monster generation logic.
- `data/data.py`: Stores all the base data for generation, such as monster types, stats, and attributes.
- `monsterseed.py`: Defines the `MonsterSeed` data structure.
- `dex_entries.py`: Formats monster data into Pokedex-style entries.
- `prompt_engine.py`: Constructs AI art prompts.
- `monster_cache.py`: Handles caching of generated monsters.

## Building and Running

### Installation

To install the project for development, including all necessary dependencies and the `mongen` command-line tool, clone the repository and run the following command in the project's root directory:

```bash
pip install -e .[dev]
```

### Running Tests

The project uses `pytest` for testing. To run the tests, execute the following command:

```bash
pytest
```

## Development Conventions

- The project follows standard Python packaging conventions using `pyproject.toml`.
- It uses `pylint` for linting and `isort` for import sorting, as defined in the `[dev]` optional dependencies.
- The command-line interface is implemented using the `argparse` module.
- Monster data is structured using dataclasses.
- The project makes use of YAML files for storing some of the generation data, such as held items and physical traits.
- The code is organized into modules with specific responsibilities, promoting modularity and maintainability.
