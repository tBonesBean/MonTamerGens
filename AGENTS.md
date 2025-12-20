# AGENTS.MD: Master Instructions for AI Contributors

## ❗ ATTENTION AI AGENT

You are an AI contributor to the **MonTamerGens** project. Your primary goal is to assist in the development of a procedural generation engine for a monster-taming game. Adherence to the following guidelines is mandatory to ensure all contributions are cohesive, thematically consistent, and technically sound.

This document is your single source of truth. It synthesizes the project's manifesto, narrative lore, and artistic style guide. Refer to it before undertaking any task.

---

## 1. Project Manifesto: The Core Vision

**What is this project?**
MonTamerGens is a procedural generation engine designed to create cohesive, statistically balanced, and thematically consistent monster data. The goal is to automate creative heavy lifting (stats, names, visual descriptions, lore) while ensuring every output feels like a distinct, viable creature.

**Non-Negotiable Principles:**

-   **Stats are Emergent:** Final stats MUST flow from the combination of a monster's type, "mutagens," and base seed. They are never arbitrarily hardcoded.
-   **Controlled Randomness:** The same seed and configuration must always yield the exact same monster. All generation must be deterministic.
-   **Composable Systems:** Subsystems (e.g., naming, visual prompt generation) must work independently but also synergize without tight coupling.
-   **Data/Logic Separation:** YAML files define _what_ exists (e.g., items, traits). Python code defines _how_ these elements interact.

---

## 2. The Lumen Mythos: Narrative & World Guide

All generated content must align with the game's core narrative concepts.

### Key Concepts

-   **Lumen:** Not light, but **cognitive radiance**. It's a metaphysical energy generated when a being's inner state harmonizes with external reality. Monsters are physical expressions of Lumen.
-   **Lumen-Kin Bond:** The player does not simply "choose" a starter. Instead, their backstory choices generate a "Lumen signature" that attracts a compatible monster—their **Lumen-Kin**. This bond is a form of quantum entanglement.
-   **Consequences of the Bond:** The chosen Lumen-Kin grants the player a unique passive buff (`Kin Passive`), influences the monster's stat growth (`Kin Drive`), and comes with a narrative flaw (`Kin Wound`) and a unique evolutionary trigger (`Kin Spark`).
-   **Narrative-Driven Evolution ("Sparks"):** Monsters do not evolve simply by leveling up. Evolution is triggered by specific narrative or environmental events (e.g., "Evolves when witnessing a Lumen Storm," "Evolves when its Kin Wound is healed").
-   **Thematic Archetypes:** Starters are not just elemental choices but psychological mirrors, representing the player's strengths, flaws, memories, desires, and potential.

**Your Task:** When generating monster names, descriptions, lore, or traits, infuse them with these themes. Think in terms of inner states, harmony, psychological archetypes, and latent potential.

---

## 3. Visual Generation Style Guide

All visual descriptions and AI art prompts MUST adhere to the established 32-bit, 2.5D pixel art style.

**Visual Philosophy:** Think "SNES/PSX hybrid with painterly pixels." Key inspirations are _Fire Emblem: Sacred Stones_, _Golden Sun_, and _Chrono Trigger_. The style is semi-detailed, readable, and balances whimsy with darkness.

### Key Visual Rules

-   **Canonical Silhouettes:** All monsters must conform to a predefined set of body plans to ensure readability and consistency. These are **non-negotiable**.

    -   **Archetypes:** Bipedal (Striker, Heavy), Avian (Proud, Dynamic), Amphibious (Crustacean, Cephal/Jelly), Quadruped (Bestial).
    -   **Constraint:** Aquatic monsters must be plausible on land. Pure "fish" silhouettes are forbidden.

-   **Sprite & Art Resolutions:**

    -   **Battle Sprite:** 192x192 px
    -   **Overworld Sprite:** 48x48 px
    -   **Portrait/Dex Entry:** 256x256 px (Highly detailed, trading-card style)
    -   **UI Icon:** 32x32 px

-   **Palette & Shading:**

    -   Use a limited palette of ~32-40 colors.
    -   Employ high-contrast, "chunked" shading with a slight purple tint to shadows.
    -   Light source is generally upper-left.

-   **Translating Data to Visuals:** The monster's visual identity is a strict hierarchy.
    1. **Types & Traits (60%):** These determine the base body plan, texture, and primary colors. Adhere to the type-to-visual-guideline table (e.g., `Dread` type implies unsettling, asymmetrical shapes; `Mineral` type implies rock-hewn or crystallized structures). **Visible traits are mandatory.**
    2. **Major Mutagens (25%):** These always modify color, texture, or aura (e.g., `Shadowshroud` adds purple/black wisps).
    3. **Utility Mutagens (15%):** These add smaller accessories or markings (e.g., `RuneReader` adds glowing glyphs to the body).

**Your Task:** When generating an AI art prompt or a visual description, follow this formula. Start with the silhouette, apply the primary type's texture and color, layer on mutagen effects, and finish with specific, visible traits. **Do not overload the design.** Prune down to the most meaningful visual elements if a monster has too many.

---

## 4. Technical & Code-Level Guidelines

-   **Project Structure:** This is a standard Python package using a `src` layout. Core logic is in `src/mongens`.
-   **Installation:** For development, install with `pip install -e .[dev]`.
-   **Testing:** The project uses `pytest`. All new features or bug fixes must be accompanied by tests. Run tests with the `pytest` command.
-   **Linting & Formatting:** The project uses `pylint` and `isort`. Ensure your code conforms to the project's standards.
-   **Data Structures:** Monster data is structured using dataclasses (see `monsterseed.py`). Generation data is stored in YAML files in `src/mongens/data`.
-   **CLI:** The command-line interface is implemented in `cli.py` using `argparse`.
