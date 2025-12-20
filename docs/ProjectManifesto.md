# MonTamerGens Project Manifesto

## 1. What is the project?

MonTamerGens is a procedural generation engine designed to create cohesive, statistically balanced, and thematically consistent monster data for a
monster-taming game. It aims to automate the creative heavy lifting—stats, names, visual descriptions, and lore—while ensuring every output feels like a
distinct, viable creature rather than a random jumble of attributes.

The key to understanding the broader purpose of the project is:  
Read and stay updated on 2 particular documents.

**'D:ProjectsPyCharmMonTamerGensdocsLUMENSTORYNOTES.MD'**  
AND  
**'D:ProjectsPyCharmMonTamerGensdocsPIXELARTSTYLEGUIDE.MD'**

## 2. What are the major subsystems?

* **Creature Generation**: The core factory (`MonsterSeed.forge`) that instantiates base monster data, assigning species, habitats, and initial attributes based
  on type.
* **Stat Pipelines**: A layered system that derives stats from base types, applies "mutagen" modifiers (with synergy bonuses), and ensures balanced
  distributions.
* **Naming Logic**: A deterministic, syllable-based generator (`forge_name.py`) that constructs names reflecting the creature's type, traits, and mutagens (
  e.g., "Inferno" types get fire-themed prefixes).
* **Silhouettes & Visuals**: A visual classification system that determines physical forms (e.g., "Serpentine", "Quadruped") and translates abstract data into
  concrete AI art prompts (`prompt_engine.py`).
* **Biomes**: Contextual logic that places monsters in appropriate environments (e.g., "Volcanic", "Deep Sea"), influencing their traits and descriptions.
* **RNG Orchestration**: A controlled random number generation layer that allows for deterministic recreation of monsters via seeds, ensuring the same ID always
  yields the same monster.
* **Dex Formatter**: A module (`dex_entries.py`) that synthesizes all generated data into human-readable, Pokedex-style entries, including flavor text and stat
  summaries.

## 3. What are the non-negotiable rules?

* **Stats are emergent, not assigned**: Final stats must flow from the combination of type, mutagens, and base seeds; they are never arbitrarily hardcoded.
* **Naming can be influenced by stats**: A bulky, high-defense monster should sound different from a speedy, fragile one.
* **Generators must remain composable**: Systems (like naming or visual generation) must work independently or together without tight coupling.
* **YAML is authoritative for content, not logic**: Data files define *what* exists (items, traits), while Python code defines *how* they interact.
* **Deterministic Seeds**: The same seed and configuration must always yield the exact same monster.

## 4. Narrative & Visual Foundation

The tools built here serve a specific creative vision:

* **The Core Concept**: "Lumen" is cognitive radiance—energy generated when internal truth harmonizes with external reality. Monsters are physical expressions
  of this energy.
* **The Bond**: Players do not choose a starter; they bond with a "Lumen-Kin" that resonates with their generated backstory (fears, aspirations, wounds). This
  bond is quantum-entangled, offering unique "Kin Passives" and evolutionary paths ("Sparks") based on narrative triggers rather than just XP.
* **Visual Style**: A "2.5D" aesthetic blending SNES/PSX era pixel art (Fire Emblem, Golden Sun) with modern lighting.
	* **Silhouettes**: Strictly defined archetypes (e.g., "Bipedal-Striker", "Avian-Proud") ensure readability.
	* **Palette**: 32-bit limitations with high-contrast shading and specific color rules for types (e.g., "Dread" uses purples/blacks).
	* **Readability**: Visuals prioritize clarity over noise; mutagens and traits add specific, readable details (e.g., "Bioluminescent" adds a glow, "
	  RuneReader" adds glyphs) without cluttering the sprite.

## 5. Current state

- Stat flow refactor complete (for now)
- Silhouette rules drafted
- Biome palettes - WIP
- Naming pipeline partially integrated and showing promise ('epithets' still a bit buggy)
- Mutagen application logic updated with partial synergy support - WIP (not adhering to type allowance params)
- Visual prompt generation prototype active

---

#### + TODO list (as of latest version of this document)

	{} A HIGH priority should be assigned to populating the existing data sets that source MonsterSeed attributes.
	{} Continue defining any game-wide visuals, stylistic aspects that make sense being serialized.
	{} Tweak the generation to produce far fewer cases of Mons with empty or lopsided attribute fields.

------
