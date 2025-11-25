from mongens.mon_forge import generate_monster
from mongens.prompt_engine import construct_mon_prompt

print("Generating a monster to visualize...")

# 1. Create a monster with a few interesting visual mutagens
psi_monster = generate_monster(
    main_type="Psychokinetic",
    idnum=77,
    major_count=1,
    minor_count=2,
    util_count=1
)

# 2. Construct the detailed image prompt from the monster data
image_prompt = construct_mon_prompt(psi_monster)

print("\n--- AI IMAGE PROMPT ---")
print(image_prompt)