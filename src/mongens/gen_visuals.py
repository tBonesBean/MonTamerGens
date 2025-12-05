from pprint import pprint

from .mon_forge import generate_monster
from .prompt_engine import construct_mon_prompt

print("Generating a monster to visualize...")

# 1. Create a monster with a few interesting visual mutagens
psi_monster = generate_monster(
    idnum=77,
    primary_type=primary_type,
    secondary_type=secondary_type,
    major_count=1,
    util_count=1,
)
pprint(psi_monster)

# 2. Construct the detailed image prompt from the monster data
image_prompt = construct_mon_prompt(psi_monster)

pprint("\n--- AI IMAGE PROMPT ---")
pprint(image_prompt)
