import argparse
import json
from dataclasses import asdict
from pprint import pprint
from random import choice, random

from .data.data import SEED_TYPES, ALL_HABITATS, MAJOR_MODS, MINOR_MODS, UTILITY_MODS
from .dex_entries import dex_formatter
# --- Core Function Imports ---
# The CLI should only need to import the high-level functions.
from .mon_forge import generate_monster, forge_seed_monster
from .prompt_engine import construct_mon_prompt


def main():
	parser = argparse.ArgumentParser(
			description="A command-line tool for generating fantasy monsters.",
			epilog="Use 'mongen <command> --help' for more information on a specific command."
	)
	subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

	# ===================================================================
	# 'dexentry' command - Generates CANONICAL/TEMPLATE entries
	# ===================================================================
	parser_dex = subparsers.add_parser("dexentry", help="Generate canonical Pokedex-style entries for a species.")
	parser_dex.add_argument("-t1", "--primary_type", type=str, default="random", choices=SEED_TYPES + ["random"], help="Primary type of the monster.")
	parser_dex.add_argument("-t2", "--secondary_type", type=str, default="random", choices=SEED_TYPES + ["random", None], help="Optional secondary type.")
	parser_dex.add_argument("-c", "--count", type=int, default=1, help="Number of monsters to generate.")
	parser_dex.add_argument("-o", "--output", type=str, default="C:/Users/Bean/Desktop/PokeDex/dex_entries.txt", help="Optional file path to save the generated dex entries.")

	# ===================================================================
	# 'unique' command - Generates WILD/RANDOMIZED instances
	# ===================================================================
	parser_unique = subparsers.add_parser("unique", help="Generate the raw data for a unique 'wild' monster instance (with mutagens).")
	parser_unique.add_argument("-t1", "--primary_type", type=str, default="random", choices=SEED_TYPES + ["random"], help="Primary type of the monster.")
	parser_unique.add_argument(
		"-t2", "--secondary_type", type=str, default="random", choices=SEED_TYPES + ["random", None], help="Optional secondary type. Set to 'random' for a 60%%"
		                                                                                                   " chance of a secondary type."
		)
	parser_unique.add_argument("--majors", type=int, default=1, choices=range(3), help="Number of major mutagens.")
	parser_unique.add_argument("--minors", type=int, default=1, choices=range(3), help="Number of minor mutagens.")
	parser_unique.add_argument("--utils", type=int, default=1, choices=range(2), help="Number of utility mutagens.")

	# ===================================================================
	# 'artprompt' command - Generates an image prompt
	# ===================================================================
	parser_prompt = subparsers.add_parser("artprompt", help="Generate a Stable Diffusion-style art prompt for a monster.")
	parser_prompt.add_argument("-t1", "--primary_type", type=str, default="random", choices=SEED_TYPES + ["random"], help="Primary type for the monster.")
	parser_prompt.add_argument("-t2", "--secondary_type", type=str, default="random", choices=SEED_TYPES + ["random", None], help="Optional secondary type.")
	parser_prompt.add_argument("-c", "--count", type=int, default=1, choices=[range(21)] + ["random"], help="Number of prompt dictionaries to generate.")
	parser_prompt.add_argument("-maj", "--majors", type=int, default=1, choices=[range(3)] + ["random"], help="Number of major mutagens.")
	parser_prompt.add_argument("-min", "--minors", type=int, default="random", choices=[range(3)] + ["random"], help="Number of minor mutagens.")
	parser_prompt.add_argument("-ut", "--utils", type=int, default=1, choices=[range(2)] + ["random"], help="Number of utility mutagens.")
	parser_prompt.add_argument("-o", "--output", type=str, default="C:/Users/Bean/Desktop/PokeDex/art_prompts.txt", help="Optional path to append the prompt to a file.")
	parser_prompt.add_argument("--json", action="store_true", help="Also save the raw seed JSON to '<output>.seed.json'.")

	# ===================================================================
	# 'list' command
	# ===================================================================
	parser_list = subparsers.add_parser("list", help="List available data like monster types, habitats, etc.")
	parser_list.add_argument("--types", action="store_true", help="List all available monster main types.")
	parser_list.add_argument("--habitats", action="store_true", help="List all available habitats.")
	parser_list.add_argument("--mutagens", action="store_true", help="List all available mutagens.")

	# --- Execution Logic ---
	args = parser.parse_args()
	p_type: str
	s_type: str | None

	# --- Helper function for choosing types ---
	def get_monster_types(primary_arg, secondary_arg):
		p_type = primary_arg if primary_arg != "random" else choice(SEED_TYPES)
		s_type = None
		if secondary_arg == "random" and random() <= 0.6:
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
				monster_template = forge_seed_monster(idnum=i + 1, primary_type=p_type, secondary_type=s_type)
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

	elif args.command == "unique":
		print("Generating raw data for one unique monster instance...")
		p_type, s_type = get_monster_types(args.primary_type, args.secondary_type)
		try:
			wild_monster = generate_monster(
					idnum=1, primary_type=p_type, secondary_type=s_type,
					major_count=args.majors, minor_count=args.minors, util_count=args.utils
			)
			pprint(asdict(wild_monster))
		except ValueError as e:
			print(f"Error generating monster: {e}")

	elif args.command == "artprompt":
		print("Generating art prompt...")
		p_type, s_type = get_monster_types(args.primary_type, args.secondary_type)
		try:
			monster_seed = generate_monster(
					idnum=1, primary_type=p_type, secondary_type=s_type,
					major_count=args.majors, minor_count=args.minors, util_count=args.utils
			)
			art_prompt = construct_mon_prompt(monster_seed)  # Pass the object directly
			print("\n=== ART PROMPT ===\n")
			print(art_prompt)
			print("\n==================\n")

			if args.output:
				with open(args.output, "a", encoding="utf-8") as f:
					f.write(art_prompt + "\n\n" + ("-" * 60) + "\n\n")
				print(f"Saved prompt to {args.output}")
				if args.json:
					seed_out_path = f"{args.output}.seed.json"
					with open(seed_out_path, "a", encoding="utf-8") as sf:
						json.dump(asdict(monster_seed), sf, indent=2)
					print(f"Saved raw seed JSON to {seed_out_path}")

		except ValueError as e:
			print(f"Error generating prompt: {e}")

	elif args.command == "list":
		if args.types:
			print("--- Available Monster Types ---", *sorted(SEED_TYPES), sep="\n- ")
		if args.habitats:
			print("\n--- Available Habitats ---", *sorted(ALL_HABITATS), sep="\n- ")
		if args.mutagens:
			print("\n--- Major Mutagens ---", *sorted(MAJOR_MODS.keys()), sep="\n- ")
			print("\n--- Minor Mutagens ---", *sorted(MINOR_MODS.keys()), sep="\n- ")
			print("\n--- Utility Mutagens ---", *sorted(UTILITY_MODS.keys()), sep="\n- ")
		if not any([args.types, args.habitats, args.mutagens]):
			parser_list.print_help()


if __name__ == "__main__":
	main()
