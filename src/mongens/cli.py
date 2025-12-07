import argparse
from dataclasses import asdict
import json
from pprint import pprint
from random import choice, random
import pathlib

# The CLI should only need to import the high-level functions.
from .data.data import *
from .dex_entries import dex_formatter
from .forge_name import *
from .mon_forge import generate_monster
from .monster_cache import CACHE_FILE, load_monster
from .prompt_engine import construct_mon_prompt


def main():
    parser = argparse.ArgumentParser(
        description="A command-line tool for generating fantasy monsters.",
        epilog="Use 'mongen <command> --help' for more information on a specific command.",
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # 'dexentry' command - Generates CANONICAL/TEMPLATE entries
    parser_dex = subparsers.add_parser(
        "dexentry", help="Generate canonical Pokedex-style entries for a species."
    )
    parser_dex.add_argument(
        "-t1",
        "--primary_type",
        type=str,
        default="random",
        choices=SEED_TYPES + ["random"],
        help="Primary type of the monster.",
    )
    parser_dex.add_argument(
        "-t2",
        "--secondary_type",
        type=str,
        default="random",
        choices=SEED_TYPES + ["random", "none"],
        help="Optional secondary type.",
    )
    parser_dex.add_argument(
        "-maj",
        "--majors",
        type=int,
        default=1,
        choices=range(3),
        help="Number of major mutagens.",
    )
    parser_dex.add_argument(
        "-ut",
        "--utils",
        type=int,
        default=1,
        choices=range(2),
        help="Number of utility mutagens.",
    )
    parser_dex.add_argument(
        "-c", "--count", type=int, default=1, help="Number of monsters to generate."
    )
    parser_dex.add_argument(
        "-o",
        "--output",
        type=str,
        default="..\\src\\mongens\\assets\\mongen_dexentry.txt",
        help="Optional file path to save the generated dex entries.",
    )

    # 'unique' command - Generates WILD/RANDOMIZED instances
    parser_unique = subparsers.add_parser(
        "unique",
        help="Generate the raw data for a unique 'wild' monster instance (with mutagens).",
    )
    parser_unique.add_argument(
        "-t1",
        "--primary_type",
        type=str,
        default="random",
        choices=SEED_TYPES + ["random"],
        help="Primary type of the monster.",
    )
    parser_unique.add_argument(
        "-t2",
        "--secondary_type",
        type=str,
        default="random",
        choices=SEED_TYPES + ["random", "none"],
        help="Optional secondary type. Set to 'random' for a 60%% chance of a secondary type.",
    )
    parser_unique.add_argument(
        "--majors",
        type=int,
        default=1,
        choices=range(3),
        help="Number of major mutagens.",
    )
    parser_unique.add_argument(
        "--utils",
        type=int,
        default=1,
        choices=range(2),
        help="Number of utility mutagens.",
    )

    # 'alternatives' command - Generates a list of names for a monster
    parser_alt = subparsers.add_parser(
        "alternatives",
        help="Generate a list of alternative names for a given monster.",
    )
    parser_alt.add_argument(
        "--pin",
        type=str,
        help="The 10-character ID of a previously generated monster to use as a base.",
    )
    parser_alt.add_argument(
        "-t1",
        "--primary_type",
        type=str,
        default="random",
        choices=SEED_TYPES + ["random"],
        help="Primary type of the monster (used if --pin is not provided).",
    )
    parser_alt.add_argument(
        "-t2",
        "--secondary_type",
        type=str,
        default="random",
        choices=SEED_TYPES + ["random", "none"],
        help="Optional secondary type (used if --pin is not provided).",
    )
    parser_alt.add_argument(
        "--majors",
        type=int,
        default=1,
        choices=range(3),
        help="Number of major mutagens (used if --pin is not provided).",
    )
    parser_alt.add_argument(
        "--utils",
        type=int,
        default=1,
        choices=range(2),
        help="Number of utility mutagens (used if --pin is not provided).",
    )
    parser_alt.add_argument(
        "-c",
        "--count",
        type=int,
        default=10,
        help="Number of alternative names to generate.",
    )

    # ===================================================================
    # 'artprompt' command - Generates an image prompt
    # ===================================================================
    parser_prompt = subparsers.add_parser(
        "artprompt", help="Generate a Stable Diffusion-style art prompt for a monster."
    )
    parser_prompt.add_argument(
        "--pin",
        type=str,
        help="The 10-character ID of a previously generated monster to use as a base.",
    )
    parser_prompt.add_argument(
        "-t1",
        "--primary_type",
        type=str,
        default="random",
        choices=SEED_TYPES + ["random"],
        help="Primary type for the monster (used if --pin is not provided).",
    )
    parser_prompt.add_argument(
        "-t2",
        "--secondary_type",
        type=str,
        default="random",
        choices=SEED_TYPES + ["random", "none"],
        help="Optional secondary type (used if --pin is not provided).",
    )
    parser_prompt.add_argument(
        "-maj",
        "--majors",
        type=int,
        default=1,
        choices=range(3),
        help="Number of major mutagens (used if --pin is not provided).",
    )
    parser_prompt.add_argument(
        "-ut",
        "--utils",
        type=int,
        default=1,
        choices=range(2),
        help="Number of utility mutagens (used if --pin is not provided).",
    )
    parser_prompt.add_argument(
        "-o",
        "--output",
        type=str,
        default="C:/Users/Bean/Desktop/PokeDex/art_prompts.txt",
        help="Optional path to append the prompt to a file.",
    )
    parser_prompt.add_argument(
        "--json",
        action="store_true",
        default=True,
        help="Also save the raw seed JSON to '<output>.seed.json'.",
    )

    # ===================================================================
    # 'list' command
    # ===================================================================
    parser_list = subparsers.add_parser(
        "list", help="List available data like monster types, habitats, etc."
    )
    parser_list.add_argument(
        "--types", action="store_true", help="List all available monster main types."
    )
    parser_list.add_argument(
        "--habitats", action="store_true", help="List all available habitats."
    )
    parser_list.add_argument(
        "--mutagens", action="store_true", help="List all available mutagens."
    )

    # --- Execution Logic ---
    args = parser.parse_args()

    # --- Helper function for choosing types ---
    def get_monster_types(primary_arg, secondary_arg):
        s_type = None
        if primary_arg == "random":
            p_type = choice(SEED_TYPES)
        else:
            p_type = primary_arg

        if secondary_arg == "none":
            s_type = None
        elif secondary_arg == "random" and random.random() <= 0.65:
            possible_seconds = [t for t in SEED_TYPES if t != p_type]
            if possible_seconds:
                s_type = choice(possible_seconds)
        elif secondary_arg in SEED_TYPES:
            s_type = secondary_arg

        return p_type, s_type

    # --- Command Logic ---
    if args.command == "dexentry":
        print(f"Generating {args.count} canonical dex entries...")
        output_lines = []
        for i in range(args.count):
            p_type, s_type = get_monster_types(args.primary_type, args.secondary_type)
            try:
                monster_template = generate_monster(
                    idnum=i + 1,
                    primary_type=p_type,
                    secondary_type=s_type,
                    major_count=args.majors,
                    util_count=args.utils,
                )
                entry_text = dex_formatter(monster_template)
                output_lines.append(entry_text)
            except ValueError as e:
                print(f"Skipping combination {p_type}/{s_type}: {e}")
                continue

        full_output = ("\n\n" + "-" * 60 + "\n\n").join(output_lines)
        if args.output:
            with open(args.output, "a", encoding="utf-8") as f:
                f.write(full_output)
            print(f"Successfully appended {len(output_lines)} entries to {args.output}")
        else:
            print(full_output)
        if args.json:
            seed_out_path = CACHE_FILE
            with open(seed_out_path, "a", encoding="utf-8") as sf:
                # Use asdict on the fetched or generated seed
                json.dump(asdict(monster_template), sf, indent=2)
                sf.write("\n") # Add a newline for better formatting
            print(f"Saved raw seed JSON to {CACHE_FILE}")
    elif args.command == "unique":
        print("Generating raw data for one unique monster instance...")
        p_type, s_type = get_monster_types(args.primary_type, args.secondary_type)
        try:
            wild_monster = generate_monster(
                idnum=1,
                primary_type=p_type,
                secondary_type=s_type,
                major_count=args.majors,
                util_count=args.utils,
            )

            pprint(asdict(wild_monster))
            print(f"\nMonster Pin ID: {wild_monster.meta.get('unique_id')}")
        except ValueError as e:
            print(f"Error generating monster: {e}")

    elif args.command == "alternatives":
        base_seed = None
        try:
            if args.pin:
                print(f"Loading pinned monster '{args.pin}'...")
                base_seed = load_monster(args.pin)
            else:
                print("Generating a temporary monster...")
                p_type, s_type = get_monster_types(
                    args.primary_type, args.secondary_type
                )
                base_seed = generate_monster(
                    idnum=1,  # Temporary monster, idnum is not critical
                    primary_type=p_type,
                    secondary_type=s_type,
                    major_count=args.majors,
                    util_count=args.utils,
                )

            print(f"Generating {args.count} alternative names for '{base_seed.name}'...")
            
            alt_names = generate_alternative_names(base_seed, count=args.count)
            
            print(f"\nOriginal Name: {base_seed.name}")
            if 'unique_id' in base_seed.meta:
                print(f"Pin ID: {base_seed.meta['unique_id']}")
                
            print("\n--- Alternatives ---")
            for name in alt_names:
                print(f"- {name}")

        except (ValueError, KeyError, FileNotFoundError) as e:
            print(f"Error: {e}")

    elif args.command == "artprompt":
        monster_seed = None
        try:
            if args.pin:
                print(f"Loading pinned monster '{args.pin}' for art prompt...")
                monster_seed = load_monster(args.pin)
            else:
                print("Generating a temporary monster for art prompt...")
                p_type, s_type = get_monster_types(
                    args.primary_type, args.secondary_type
                )
                monster_seed = generate_monster(
                    idnum=1,
                    primary_type=p_type,
                    secondary_type=s_type,
                    major_count=args.majors,
                    util_count=args.utils,
                )

            art_prompt = construct_mon_prompt(monster_seed)
            print("\n=== ART PROMPT ===\n")
            print(art_prompt)
            print("\n==================\n")
            if 'unique_id' in monster_seed.meta:
                print(f"Monster Pin ID: {monster_seed.meta.get('unique_id')}")

            if args.output:
                with open(args.output, "a", encoding="utf-8") as f:
                    f.write(art_prompt + "\n\n" + ("-" * 60) + "\n\n")
                print(f"Saved prompt to {args.output}")
                if args.json:
                    seed_out_path = CACHE_FILE
                    with open(seed_out_path, "a", encoding="utf-8") as sf:
                        # Use asdict on the fetched or generated seed
                        json.dump(asdict(monster_seed), sf, indent=2)
                        sf.write("\n") # Add a newline for better formatting
                    print(f"Saved raw seed JSON to {CACHE_FILE}")

        except (ValueError, KeyError, FileNotFoundError) as e:
            print(f"Error: {e}")

    elif args.command == "list":
        if args.types:
            print("--- Available Monster Types ---", *sorted(SEED_TYPES), sep="\n- ")
        if args.habitats:
            print("\n--- Available Habitats ---", *sorted(ALL_HABITATS), sep="\n- ")
        if args.mutagens:
            print("\n--- Major Mutagens ---", *sorted(MAJOR_MODS.keys()), sep="\n- ")
            print(
                "\n--- Utility Mutagens ---", *sorted(UTILITY_MODS.keys()), sep="\n- "
            )
        if not any([args.types, args.habitats, args.mutagens]):
            parser_list.print_help()


if __name__ == "__main__":
    main()
