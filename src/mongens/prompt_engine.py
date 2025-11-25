from .seed_data_attr import MonsterSeed

# --- VISUAL TRANSLATION MAP ---
# Maps abstract game terms to concrete visual descriptions for image generation.
VISUAL_TRANSLATION = {
    # (The dictionary content remains the same)
    # ...
}

def translate_term(term: str) -> str:
    """Helper to translate a term if mapped, else return it as-is."""
    return VISUAL_TRANSLATION.get(term, term)

def construct_mon_prompt(seed: MonsterSeed) -> str:
    """
    Constructs a rigid, style-compliant image prompt for Stable Diffusion/DALL-E
    based on the 'Pixel Art Style Guide' and 'mon_forge' output.
    Uses VISUAL_TRANSLATION to convert abstract concepts into concrete prompts.
    """

    # --- 1. DECONSTRUCT SEED DATA (Corrected Access) ---
    # Use direct attribute access for the object's fields
    species = seed.species
    primary_type = seed.primary_type
    secondary_type = seed.secondary_type
    habitat = seed.habitat
    traits = seed.traits

    # Use .get() for the dictionaries *within* the object
    elements = seed.elements
    majors = elements.get("major", [])
    minors = elements.get("minor", [])
    utilities = elements.get("utility", [])

    tempers = seed.tempers
    mood = tempers.get("mood", "neutral")

    # --- 2. STYLE DEFINITIONS (The "Immutable Wrapper") ---
    art_style_header = (
        "32-bit pixel art sprite of a fantasy RPG monster, "
        "reminiscent of Fire Emblem Sacred Stones and Golden Sun but, "
        "with a distinct next-gen feel, that fits "
        "seamlessly into a 2.5-D world feel in Godot Engine."
        "2D sprite, rich textures, almost 'next-gen' pixel shading. "
        "World visuals, or any game visuals outside of: menus, system scenes, "
        "dialogue scenes, monster encounters/battle scenes are intended to feel 2.5-D."
    )

    technical_specs = (
        "High contrast, no anti-aliasing, pixel-perfect. "
        "Lighting from upper-left. Shadows have a slight purple tint. "
        "Neutral dark background. If creating in-game/overworld/battle sprite, " 
        "background must be an invisible layer, for easier workability in Godot. "
        "Aura effects have a bit of a margin for 'creative liberties' to "
        "be employed; this relying directly on how the aura in question is expected"
        " to move and visually behave in game-world scenes and animatable sprite images. "
        "If the species provided is capable of believably converting to Bipedalism "
        "(and isn't already bipedal) make it so ONLY if it doesn't lose aesthetic "
        "and visual value."
    )
    # --- 3. BODY PLAN (60% Weight) ---
    type_visuals = {
        "Geomorph": "typically thicker physique, rock-hewn or crystallized structures and silhouettes, diverse mineral textures/colors",
        "Beast": "muscular build, hybrid quadruped-biped posture, fur textures",
        "Aquatic": "smooth textures, fins and gills, fluid posture, ornaments or accessories to increase diversity of common 'fish' shape",
        "Cryoform": "sharp angular shapes, crystalline ice reflections, jagged silhouette",
        "Pugilist": "athletic stance, emphasized fists or striking limbs, bipedal",
        "Insectoid": "segmented carapace, multiple limbs, antennae, alien posture",
        "Mythic": "majestic presence, flowing fur or feathers, intricate details, exotic anatomical ornaments or fancy clothing items",
        "Electric": "jagged aura, static fur or plating, glowing nodes, expressions of magnetic fields if possible",
        "Verdant": "organic shapes and limbs, leaf/flower/root/petal clusters, often undergrowth or bark textured, rarely bipedal",
        "Avian": "upright aerodynamic posture, exagerrated feather forms and colors, enlarged physical attribute such as talons/beak/wingspan",
        "Dread": "unsettling elongated posture, asymmetrical shapes, shadowy presence, exotic anatomical figure, missing or extra physical features",
        "Pyro": "visible evidence of extreme heat without implying 'fire related damage or trauma', smoke tendrils, heat distortion",
        "Toxic": "bulbous glands, dripping textures, warning colors, exaggerated fangs/teeth and claws/talons, reptilian inspiration",
        "Ancient": "weathered scales, fossilized plating, prehistoric anatomy",
        "Psychokinetic": "floating elements, large eyes, glowing geometric patterns, species blurs toward humanoid form without losing identity",
        "Neutral": "balanced proportions, standard biological features",
        "Colorless": "desaturated palette, ghostly transparency, minimalist features"
    }

    body_desc = type_visuals.get(primary_type, "distinct creature silhouette")

    # Combine primary and secondary types for the subject line
    type_string = primary_type
    if secondary_type:
        type_string += f"/{secondary_type}"

    # Incorporating habitat into the subject line
    subject_line = f"A {species} monster, {type_string} type, {body_desc}, typically found in {habitat}."

    # --- 4. MUTAGENS (25% Weight) ---
    visual_modifiers = []

    if majors:
        translated_majors = [translate_term(m) for m in majors]
        visual_modifiers.append(f"infused with {', '.join(translated_majors)}")
    if minors:
        translated_minors = [translate_term(m) for m in minors]
        visual_modifiers.append(f"displaying traits of {', '.join(translated_minors)}")

    prompt_glow = ""
    combined_mods = majors + minors
    if any("Luminescent" in m or "Solar" in m or "Fire" in m for m in combined_mods):
        prompt_glow = "emitting a subtle bioluminescent glow, "

    mods_line = f"Visual features: {', '.join(visual_modifiers)}." if visual_modifiers else ""

    # --- 5. UTILITY & TRAITS (10% & 5% Weight) ---
    details_list = []

    if utilities:
        translated_utils = [translate_term(u) for u in utilities]
        details_list.append(f"carrying or wearing {', '.join(translated_utils)}")

    if traits:
        translated_traits = [translate_term(t) for t in traits]
        trait_str = ", ".join(translated_traits)
        details_list.append(f"distinctive features include: {trait_str}")

    details_line = f"Details: {', '.join(details_list)}." if details_list else ""

    # --- 6. POSE (The Action) ---
    # Incorporating mood into the pose
    pose_instruction = (
        f"Pose: 3/4 perspective facing diagonally forward with a {mood} expression. "
        "Slight idle lean forward ready to engage. "
        "Limbs and tail angled outward to show clear silhouette."
    )

    # --- ASSEMBLE PROMPT ---
    full_prompt = (
        f"{art_style_header}\n"
        f"Subject: {subject_line}\n"
        f"{mods_line} {prompt_glow}\n"
        f"{details_line}\n"
        f"{pose_instruction}\n"
        f"{technical_specs}"
    )

    return full_prompt
