# DEV_BIBLE.MD: Master Instructions for both AI and Stupid Human Contributors

# !!! ATTENTION AI AGENTS !!!

## MANDATORY PREREQUISITE: Full Context Review

Before making any contribution, you, the AI collaborator, **MUST** recursively read, understand, and adhere to the entire contents of the [`ai_context`](./docs/ai_context/) directory. This is not an optional step.

**Failure to comply will result in the immediate rejection of your contribution.**

The documents within `./docs/ai_context/` define the project's architecture, data schemas, naming conventions, and core principles. Any contribution made without this foundational knowledge will be considered misaligned and incorrect.

**By proceeding with any contribution, you affirm that you have fully reviewed and understood the complete contents of the [./ai_context/`](./docs/ai_context/00_README.md) directory.**

---

# 🌑 **MonTamerGens — Unified Design Bible (v1.2)**

_A living canon for the MonTamerGens universe, systems, aesthetics, and architecture._

---

# **1. Core Identity**

## **1.1 What MonTamerGens Is**

MonTamerGens is a procedural monster‑generation engine and narrative framework designed to produce creatures, lore, visuals, and emotional arcs that feel handcrafted, coherent, and alive. It blends:

- deterministic systems
- narrative metaphysics
- pixel‑art visual rules
- psychological resonance
- emergent stats and evolution

…into a unified creative and technical ecosystem.

## **1.2 Creative Pillars**

- **Lumen as Cognitive Radiance** — monsters are physical expressions of inner truth.
- **Bond Over Choice** — starters choose the player, not the other way around.
- **Emergent Identity** — stats, visuals, names, and evolution arise from data, not arbitrary assignment.
- **Readable Chaos** — randomness is allowed, but always constrained by silhouette, palette, and narrative logic.
- **Emotional Systems** — evolution, resonance, and growth reflect psychological states.

## **1.3 Non‑Negotiable Rules**

- Stats must be emergent.
- YAML defines content; Python defines logic.
- Silhouettes must follow archetypes.
- Lumen‑Kin bond is central to Act I.
- Evolution is narrative‑triggered, not XP‑triggered.
- Deterministic seeds must always reproduce identical monsters.

---

# **2. World & Narrative Canon**

## **2.1 The Nature of Lumen**

Lumen is **cognitive radiance** — energy generated when internal truth harmonizes with external reality. Monsters evolved to channel it long before humans. It manifests physically through:

- markings
- organs
- behaviors
- glow patterns
- emotional resonance

Lumen is not “light” — it is **attunement**.

## **2.2 Lumen‑Kin Bond**

The player’s starter is not chosen; it **manifests** based on resonance. Each Lumen‑Kin receives:

- **Kin Passive** — shared buff with the player
- **Kin Drive** — stat growth direction
- **Kin Wound** — flaw or neurosis
- **Kin Spark** — evolution trigger

These shape the creature’s identity and long‑term arc.

## **2.3 Resonance Variables**

Player backstory choices influence internal resonance values:

- Courage
- Empathy
- Instinct
- Memory
- Solitude
- Curiosity
- Discipline
- Lightbound (primary attunement)

These seed the starter generator.

## **2.4 Starter Archetypes**

Five emergent candidates are generated:

1. **Strength Mirror**
2. **Flaw Mirror**
3. **Deep Memory**
4. **Hidden Desire**
5. **Potential Form**

The strongest harmonic match becomes the Lumen‑Kin.

## **2.5 Act I Narrative Flow**

1. **Lumen Echo** — dreamlike intro, backstory creation
2. **Lumen Convergence** — starter manifests
3. **Collapse Into Reality** — world introduction
4. **First Lumen Storm** — tutorial battle
5. **Mentor Arrival** — exposition
6. **The Decision** — Act II begins

---

# **3. Visual Canon**

## **3.1 Art Philosophy**

A “32‑bit SNES/PSX hybrid with painterly pixels and modern lighting,” inspired by:

- Fire Emblem: Sacred Stones
- Golden Sun
- Chrono Trigger
- Octopath Traveler

## **3.2 Silhouette Archetypes**

Silhouettes define **form before detail**:

- Bipedal Striker
- Bipedal Heavy
- Avian Proud
- Avian Dynamic
- Amphibious Crustacean
- Amphibious Cephal/Jelly
- Quadruped Bestial

**Hard rules:**

- No default fish
- Aquatic must function on land
- Silhouette chosen before palette

## **3.3 Palette Rules**

- 32–40 colors
- Purple‑tinted shadows
- No pure white except glints
- No pure black except outlines

## **3.4 Visual Identity Formula**

- **Types + Traits = 60%**
- **Major Mutagens = 25%**
- **Utility Mutagens = 15%**

## **3.5 Trait Visibility Rules**

- Max 2 major color accents
- Max 1 aura
- Max 2 visible trait objects
- Mutagens must be readable at 48×48

---

# **4. Technical Architecture**

## **4.1 Data Layer**

Located in `src/mongens/data/`, the data layer establishes the foundational truths of the monster generation universe.

- **`data.py`**: The central nervous system of the data layer. It loads and processes all YAML files, preparing the data for the generation pipeline. It defines:
    - `BASE_STATS`: The default stat block for all monsters before any modifications.
    - `TYPE_SYNERGY_BOOSTS` and `INCOMPATIBLE_TYPE_PAIRS`: The rules governing type interactions.
    - `MAJOR_MODS` and `UTILITY_MODS`: Dictionaries of all possible mutagens, including their stat effects, tags, and type affinities.
    - `LEGACY_TYPE_MAP`: A critical dictionary for ensuring backward compatibility by mapping old type names to the new canonical system.

- **YAML Files**: These files represent the "canon" of the world, defining the specific properties of types, traits, and items. They are designed to be human-readable and easily editable.
    - `seed_types.yaml`: Defines the core monster archetypes ("seeds"), including their names, weights, habitats, and base attribute modifications.
    - `type_forms.yaml`: Maps types to their possible physical forms or species.
    - `physical_traits.yaml`, `held_items.yaml`, `kin_wounds.yaml`: Weighted lists of physical characteristics, items, and narrative flaws.

## **4.2 Generation Pipeline**

The generation of a monster is a multi-stage process that transforms raw data into a fully realized creature.

1. **`MonsterSeed.forge()`** (in `monsterseed.py`): This is the inception point. The `forge` class method creates a `MonsterSeed` object, which acts as a blueprint for the monster.
    - **Type Selection**: It uses `choose_type_pair` to select a primary and optional secondary type, respecting weights and compatibility rules.
    - **Base Stat Calculation**: `calculate_base_stats` applies the attribute modifiers from the chosen types to the `BASE_STATS`.
    - **Initial Attributes**: It selects a form, habitat, and initial meta-attributes (tags, resistances) based on the chosen types.

2. **`mon_forge.apply_mutagens()`** (in `mon_forge.py`): This function takes the `MonsterSeed` and applies "mutagens" to it, adding layers of complexity and uniqueness.
    - **Mutagen Selection**: It filters `MAJOR_MODS` and `UTILITY_MODS` based on type compatibility and selects a unique set of mutagens using a weighted sampling algorithm that considers both rarity and synergy.
    - **Stat Shaping**: It applies the `mul` (multiplicative) and `add` (additive) stat adjustments from the chosen mutagens to the seed's stats.
    - **Meta Enhancement**: It adds tags, resistances, and weaknesses from the mutagens to the seed's `meta` dictionary.

3. **`forge_name.py`**: A deterministic naming function is called to generate a unique name for the monster based on its properties.

4. **`monster_cache.py`**: The completed `MonsterSeed` is serialized and saved to a cache, typically a JSONL file, with a unique ID.

5. **`prompt_engine.py`**: This module will use the final `MonsterSeed` to construct a detailed prompt for a visual generation model.

6. **`dex_entries.py`**: This module will use the final `MonsterSeed` to generate formatted, narrative-rich text for a bestiary or "Dex."

## **4.3 Determinism Rules**

- RNG must be seedable.
- The same input `idnum` to the generation process must always produce an identical `MonsterSeed`.
- The order of mutagen application must be stable and reproducible.
- Naming must be deterministic.

---

# **5. Systems Design**

## **5.1 Stats**

- Stats are derived from a monster's primary and secondary types, and then modified by its mutagens.
- The initial stats are defined in `BASE_STATS` in `data.py`.
- `monsterseed.py` calculates the base stats by applying the `mul` and `add` modifiers from `seed_types.yaml`. Secondary type modifiers are applied at 50% effectiveness.
- `mon_forge.py` further modifies the stats based on the applied mutagens.
- There are no hardcoded final stat values; they are entirely emergent from the generation process.

## **5.2 Mutagens**

Mutagens are powerful modifiers that add significant variation to monsters. They are divided into two categories:

### Major Mutagens

- Have a significant impact on a monster's stats and abilities.
- Often grant powerful tags or stat multipliers.
- Their selection is heavily influenced by `synergy_bonus` rules, encouraging thematic combinations.
- Are expected to have a high-impact on visual identity (e.g., silhouette, color, aura).

### Utility Mutagens

- Provide more subtle or situational advantages.
- May affect non-combat abilities or grant flavorful tags.
- Are less visually impactful than Major Mutagens, often affecting markings, accessories, or mood.

## **5.3 Traits**

- Traits are inherent physical characteristics of a monster.
- They are defined in `physical_traits.yaml` with associated weights.
- A monster is assigned one or two physical traits during the `MonsterSeed.forge` process.
- All traits are expected to be visually represented and serialized.

## **5.4 Evolution (Sparks)**

Evolution is a narrative-driven event, not a result of grinding experience points. Triggers for evolution (called "Sparks") are tied to the monster's personal journey and its bond with the player. Potential triggers include:

- Reaching a critical emotional state.
- Experiencing a significant environmental event.
- Key narrative beats in the story.
- Achieving a certain level of bond strength.
- Resolving a "Kin Wound."

---

# **6. Prompt Engineering Canon**

## **6.1 Prompt Structure**

- STYLE_HEADER
- TECHNICAL_SPECS
- VISUAL_TRANSLATION
- Monster-specific attributes
- Mutagen/trait overlays

## **6.2 Prompt Rules**

- No conflicting descriptors
- No more than 2 color accents
- Silhouette must be clear
- Habitat must influence background

---

# **7. Production Rules**

## **7.1 Readability Over Novelty**

If a monster becomes visually overloaded, prune mutagens.

## **7.2 Serialization Rules**

Everything must be:

- JSON‑safe
- reproducible
- human‑readable

## **7.3 Testing Requirements**

Tests must cover:

- weighted sampling
- naming determinism
- mutagen synergy
- prompt formatting
- stat curve validity

---

# **8. Future Expansion Hooks**

- Lumen storms as world events
- NPC resonance profiles
- Kin Wound healing quests
- Multi‑form evolutions
- Procedural habitats
- Starter rejection path content
- Emotional AI for monsters
- Biome‑specific palettes
- Implementation of the `choose_silhouette` function in `mon_forge.py`.

---

## **9. Versioning**

This document is **v1.2** - updated to reflect the current canonical type taxonomy, YAML-first content model, and recent data migration.
Changes in this release:

- Normalized `seed_types.yaml` to the schema shape (list habitats, explicit tags).
- Clarified that `seed_types_schema.md` requires `attributes.notes`.
- Added schema and module-purpose documentation updates (including module_purposes and schemas readmes).
- Documented current pipeline behavior based on the refactor state.
- Confirmed `prompt_engine.py` and `dex_entries.py` are implemented (removed presumed labels).

All future edits should continue the principle: changes must be additive, clarifying, or canon-strengthening.

Last updated: 2026-01-13 04:56:41 -07:00

---
