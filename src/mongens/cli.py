import argparse
from dataclasses import asdict
import json, sys
from pprint import pprint
from random import choice, random
from pathlib import Path

# The CLI should only need to import the high-level functions.
from .data.data import *
from .dex_entries import dex_formatter
from .forge_name import *
from .mon_forge import generate_monster
from .monster_cache import CACHE_FILE, OUTPUT_PATH, load_monster, save_monster
from .prompt_engine import construct_mon_prompt
from .monsterseed import MonsterSeed, choose_type_pair, weighted_choice


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
        type=int, # Corrected from str to int
        default=1,
        choices=range(3),
        help="Number of major mutagens."
    )
    parser_dex.add_argument(
        "-ut",
        "--utils", # Corrected from str to int
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
        default=str(OUTPUT_PATH),
        help="Optional file path to save the generated dex entries.",
    )
    parser_dex.add_argument(
        "--json",
        action="store_true",
        # default=True, # Let default be False, more intuitive for a flag
        help="Also save the raw seed JSON to '<output>.seed.json'.",
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
        # default=True, # Let default be False
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

    # ===================================================================
    # 'lumenkin' command - Generates a starter based on player resonance
    # ===================================================================
    parser_kin = subparsers.add_parser(
        "lumenkin",
        help="Generate a Lumen-Kin starter candidate based on player resonance values.",
        description="Simulates the starter generation from the Lumen Mythos. Resonance values influence the monster's type, stats, and Kin properties."
    )
    parser_kin.add_argument("--courage", type=int, default=5, help="Player's Courage resonance (0-10).")
    parser_kin.add_argument("--empathy", type=int, default=5, help="Player's Empathy resonance (0-10).")
    parser_kin.add_argument("--instinct", type=int, default=5, help="Player's Instinct resonance (0-10).")
    parser_kin.add_argument("--memory", type=int, default=5, help="Player's Memory resonance (0-10).")
    parser_kin.add_argument("--curiosity", type=int, default=5, help="Player's Curiosity resonance (0-10).")
    parser_kin.add_argument(
        "--archetype",
        type=str,
        default="Strength Mirror",
        choices=["Strength Mirror", "Flaw Mirror", "Deep Memory", "Hidden Desire", "Potential Form"],
        help="The archetypal mirror to generate for."
    )
    parser_kin.add_argument(
        "--json",
        action="store_true",
        help="Save the raw seed JSON to the cache file.",
    )

    # ===================================================================
    # 'reroll' command - Re-rolls attributes of an existing monster
    # ===================================================================
    parser_reroll = subparsers.add_parser(
        "reroll", help="Re-roll attributes of a cached monster."
    )
    parser_reroll.add_argument(
        "pin", type=str, help="The 10-character ID of the monster to re-roll."
    )
    parser_reroll.add_argument(
        "--traits", action="store_true", help="Re-roll the physical traits."
    )
    parser_reroll.add_argument(
        "--majors", action="store_true", help="Re-roll the major mutagen."
    )

    # ===================================================================
    # Helper function to generate Kin properties
    # ===================================================================
    def _generate_kin_properties(seed: MonsterSeed, resonance: dict) -> dict:
        """Generates Kin properties based on the seed and player resonance."""
        # This is a placeholder for more complex logic.
        # In the future, this could be its own module.
        kin_passives = ["Lumen Resonance: +5% healing received", "Kinetic Shield: +5% DEF when below 50% HP"]
        kin_drives = ["ATK_bias", "DEF_bias", "SPD_bias"]
        kin_sparks = [
            "Evolves when witnessing a Lumen Storm.",
            "Evolves when the player expresses Resolve.",
            "Evolves when its own Wound is healed."
        ]

        # Example of resonance influencing the outcome
        drive_choice = choice(kin_drives)
        if resonance.get('courage', 0) > 7:
            drive_choice = "ATK_bias"

        return {
            "kin_passive": choice(kin_passives),
            "kin_drive": drive_choice,
            "kin_wound": weighted_choice(KIN_WOUNDS),
            "kin_spark": choice(kin_sparks)
        }

    # --- Execution Logic ---
    args = parser.parse_args()

    # --- Helper functions ---
    def _get_monster_types_from_args(primary_arg: str, secondary_arg: str) -> tuple[str, str | None]:
        """Determines primary and secondary types from CLI args."""
        # If both are random, use the new weighted function.
        if primary_arg == "random" and secondary_arg == "random":
            return choose_type_pair()

        # Handle cases where one or both are specified.
        p_type = weighted_choice(SEED_TYPES_WEIGHTED) if primary_arg == "random" else primary_arg

        s_type = None
        if secondary_arg == "random":
            # Use the new function but force the primary type.
            _, s_type = choose_type_pair(primary_type_override=p_type)
        elif secondary_arg != "none":
            s_type = secondary_arg
        return p_type, s_type

    def _get_or_generate_seed(args: argparse.Namespace, idnum: int = 1) -> MonsterSeed | None:
        """Loads a monster by PIN or generates a new one based on args."""
        try:
            if hasattr(args, "pin") and args.pin:
                print(f"Loading pinned monster '{args.pin}'...")
                return load_monster(args.pin)
            
            print("Generating a temporary monster...")
            p_type, s_type = _get_monster_types_from_args(args.primary_type, args.secondary_type)
            return generate_monster(
                idnum=idnum,
                primary_type=p_type,
                secondary_type=s_type,
                major_count=args.majors,
                util_count=args.utils,
            )
        except (ValueError, KeyError, FileNotFoundError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return None



    # --- Command Logic ---
    if args.command == "dexentry":
        print(f"Generating {args.count} canonical dex entries...")
        output_lines = []
        generated_seeds = []
        for i in range(args.count):
            p_type, s_type = _get_monster_types_from_args(args.primary_type, args.secondary_type)
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
                generated_seeds.append(monster_template)
            except ValueError as e:
                print(f"Skipping combination {p_type}/{s_type}: {e}")
                continue

        full_output = ("\n\n" + "-" * 60 + "\n\n").join(output_lines)
        if args.output:
            # append textual dex entries (preserve existing file but allow overwrite option later)
            with open(args.output, "a", encoding="utf-8") as f:
                f.write(full_output + "\n")
            print(f"Successfully appended {len(output_lines)} entries to {args.output}")
        else:
            print(full_output)

        # Save raw seed JSON: write the entire batch as a JSON array (append-safe)
        if args.json:
            for seed in generated_seeds:
                save_monster(seed)
            print(f"Saved {len(generated_seeds)} seed object(s) to {CACHE_FILE}")

    elif args.command == "unique":
        print("Generating raw data for one unique monster instance...")
        p_type, s_type = _get_monster_types_from_args(args.primary_type, args.secondary_type)
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
        base_seed = _get_or_generate_seed(args)
        if base_seed:
            print(f"Generating {args.count} alternative names for '{base_seed.name}'...")
            
            alt_names = generate_alternative_names(base_seed, count=args.count)
            
            print(f"\nOriginal Name: {base_seed.name}")
            if 'unique_id' in base_seed.meta:
                print(f"Pin ID: {base_seed.meta['unique_id']}")
                
            print("\n--- Alternatives ---")
            for name in alt_names:
                print(f"- {name}")

    elif args.command == "artprompt":
        monster_seed = _get_or_generate_seed(args)
        if monster_seed:
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
                save_monster(monster_seed)
                print(f"Saved seed object to {CACHE_FILE}")

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


    elif args.command == "lumenkin":
        print(f"Generating Lumen-Kin candidate for archetype: {args.archetype}...")

        resonance_profile = {
            "courage": args.courage,
            "empathy": args.empathy,
            "instinct": args.instinct,
            "memory": args.memory,
            "curiosity": args.curiosity,
        }

        # Future logic: Use resonance to pick types and mutagens.
        # For now, we'll generate a random one and add the Kin properties.
        p_type, s_type = choose_type_pair()
        
        try:
            lumen_kin_seed = generate_monster(
                idnum=1, primary_type=p_type, secondary_type=s_type, major_count=1, util_count=1
            )
            
            # Generate and add the Kin properties to the monster's metadata
            kin_props = _generate_kin_properties(lumen_kin_seed, resonance_profile)
            lumen_kin_seed.meta.update(kin_props)

            pprint(asdict(lumen_kin_seed))
            if args.json:
                save_monster(lumen_kin_seed)
                print(f"Saved Lumen-Kin seed object to {CACHE_FILE}")
        except Exception as e:
            print(f"Error generating Lumen-Kin: {e}", file=sys.stderr)

    elif args.command == "reroll":
        if not args.traits and not args.majors:
            print("Error: You must specify an attribute to re-roll (e.g., --traits, --majors).", file=sys.stderr)
            print("Usage: mongen reroll <pin> [--traits] [--majors]")
            sys.exit(1)

        reroll_options = {
            "traits": args.traits,
            "majors": args.majors,
        }
        
        from .reroll import reroll_monster_attributes
        reroll_monster_attributes(args.pin, reroll_options)

if __name__ == "__main__":
    main()
