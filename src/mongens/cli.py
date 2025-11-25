import argparse
from dataclasses import asdict
from pprint import pprint
from random import choice

from mongens.data.data import (
    SEED_TYPES,
    HABITATS_BY_TYPE,
    MAJOR_MODS,
    MINOR_MODS,
    UTILITY_MODS
)
# Import the tools from your library
from .dex_entries import dex_formatter
from .mon_forge import generate_monster, forge_seed_monster


def main():
    """
    Main function for the 'mongen' command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="A command-line tool for generating fantasy monsters.",
        epilog="Use 'mongen <command> --help' for more information on a specific command."
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # ===================================================================
    # 'dexentry' command - Now generates CANONICAL/TEMPLATE entries
    # ===================================================================
    parser_dex = subparsers.add_parser("dexentry", help="Generate canonical Pokedex-style entries for a species (no mutagens).")
    parser_dex.add_argument(
        "-t1", "--primary_type",
        type=str,
        default="random",
        choices=SEED_TYPES + ["random"],
        help="The primary type of monster to generate. Defaults to a random type."
    )
    parser_dex.add_argument(
        "-t2", "--secondary_type",
        type=str,
        default="random",
        choices=SEED_TYPES + ["random"],
        help="The secondary type of monster to generate. Defaults to a random type. Only the primary type is guaranteed, the second is only possible."
    )
    parser_dex.add_argument(
        "-c", "--count",
        type=int,
        default=1,
        help="The number of monsters to generate. Defaults to 1."
    )
    parser_dex.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Optional file path to save the generated dex entries."
    )

    # ===================================================================
    # 'list' command
    # ===================================================================
    parser_list = subparsers.add_parser("list", help="List available data like monster types, habitats, etc.")
    parser_list.add_argument("--types", action="store_true", help="List all available monster main types.")
    parser_list.add_argument("--habitats", action="store_true", help="List all available habitats.")
    parser_list.add_argument("--mutagens", action="store_true", help="List all available mutagens.")

    # ===================================================================
    # 'unique' command - Now generates WILD/RANDOMIZED instances
    # ===================================================================
    parser_unique = subparsers.add_parser("unique", help="Generate the raw data for a unique 'wild' monster instance (with mutagens).")
    parser_unique.add_argument(
        "-t1", "--primary_type",
        type=str,
        default="random",
        choices=SEED_TYPES + ["random"],
        help="The primary type of monster to generate. Defaults to a random type."
    )
    parser_unique.add_argument(
        "-t2", "--secondary_type",
        type=str,
        default="random",
        choices=SEED_TYPES + ["random"],
        help="The secondary type of monster to generate."
    )
    parser_unique.add_argument("--majors", type=int, default=1, help="Number of major mutagens.")
    parser_unique.add_argument("--minors", type=int, default=1, help="Number of minor mutagens.")
    parser_unique.add_argument("--utils", type=int, default=1, help="Number of utility mutagens.")

    # ===================================================================
    # --- Execution Logic ---
    # ===================================================================
    args = parser.parse_args()

    # --- Logic for the 'dexentry' command ---
    if args.command == "dexentry":
        print(f"Generating {args.count} canonical dex entries of type '{args.primary_type}'...")

        output_lines = []
        for i in range(args.count):
            monster_template = None
            while monster_template is None:
                try:
                    primary_type = args.primary_type if args.primary_type != "random" else choice(SEED_TYPES)
                    secondary_type = args.secondary_type
                    if secondary_type == "random":
                        possible_secondary_types = [t for t in SEED_TYPES if t != primary_type]
                        secondary_type = choice(possible_secondary_types) if possible_secondary_types else None

                    monster_template = forge_seed_monster(
                        primary_type=primary_type,
                        secondary_type=secondary_type,
                        idnum=i + 1
                    )
                except ValueError:
                    continue
            entry_text = dex_formatter(monster_template)
            output_lines.append(entry_text)

        full_output = ("\n\n" + "-" * 60 + "\n\n").join(output_lines)

        if args.output:
            try:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(full_output)
                print(f"Successfully saved {args.count} entries to {args.output}")
            except IOError as e:
                print(f"Error: Could not write to file {args.output}. {e}")
        else:
            print(full_output)

    # --- Logic for the 'list' command ---
    elif args.command == "list":
        if not any([args.types, args.habitats, args.mutagens]):
            print("Please specify what to list, e.g., 'mongen list --types'")
            parser_list.print_help()
            return

        if args.types:
            print("--- Available Monster Types ---")
            for t in sorted(SEED_TYPES):
                print(f"- {t}")

        if args.habitats:
            print("\n--- Available Habitats ---")
            all_habitats = set()
            for habitats_list in HABITATS_BY_TYPE.values():
                if isinstance(habitats_list, list):
                    all_habitats.update(h for h in habitats_list if isinstance(h, str))
            for h in sorted(list(all_habitats)):
                print(f"- {h}")

        if args.mutagens:
            print("\n--- Major Mutagens ---")
            for m in sorted(MAJOR_MODS.keys()):
                print(f"- {m}")
            print("\n--- Minor Mutagens ---")
            for m in sorted(MINOR_MODS.keys()):
                print(f"- {m}")
            print("\n--- Utility Mutagens ---")
            for m in sorted(UTILITY_MODS.keys()):
                print(f"- {m}")

    # --- Logic for the 'unique' command ---
    elif args.command == "unique":
        print(f"Generating raw data for one unique '{args.primary_type}' monster instance...")
        wild_monster = None
        while wild_monster is None:
            try:
                primary_type = args.primary_type if args.primary_type != "random" else choice(SEED_TYPES)
                secondary_type = args.secondary_type
                if secondary_type == "random":
                    possible_secondary_types = [t for t in SEED_TYPES if t != primary_type]
                    secondary_type = choice(possible_secondary_types) if possible_secondary_types else None

                wild_monster = generate_monster(
                    primary_type=primary_type,
                    secondary_type=secondary_type,
                    idnum=1,
                    major_count=args.majors,
                    minor_count=args.minors,
                    util_count=args.utils
                )
            except ValueError:
                continue
        pprint(asdict(wild_monster))


if __name__ == "__main__":
    main()
