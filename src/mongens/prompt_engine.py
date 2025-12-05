from .data.art_data import *


def translate_term(term: str) -> str:
    """Helper to translate a term if mapped, else return it as-is."""
    return VISUAL_TRANSLATION.get(term, term)


def construct_mon_prompt(seed) -> str:
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
    mutagens = seed.mutagens
    majors = mutagens.get("major", [])
    utilities = mutagens.get("utility", [])

    tempers = seed.tempers
    mood = tempers.get("mood", "neutral")

    body_desc = SPECIES_VISUAL_OVERRIDES.get(species)

    # If there's no specific override, fall back to the type-based description
    if not body_desc:
        body_desc = type_visuals.get(primary_type, "distinct creature silhouette")

    subject_line = f"A {species} monster, {primary_type} type, {body_desc}."

    # --- 4. MUTAGENS (25% Weight) ---
    visual_modifiers = []

    if majors:
        translated_majors = [translate_term(m) for m in majors]
        visual_modifiers.append(f"infused with {', '.join(translated_majors)}")

    prompt_glow = ""
    combined_mods = majors + utilities
    if any("Luminescent" in m or "Solar" in m or "Fire" in m for m in combined_mods):
        prompt_glow = "emitting a subtle bioluminescent glow, "

    mods_line = (
        f"Visual features: {', '.join(visual_modifiers)}." if visual_modifiers else ""
    )

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
