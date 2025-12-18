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

- **Creature Generation**: The core factory that instantiates `MonsterSeed` objects, assigning types and base attributes.
- **Stat Pipelines**: A layered system that derives stats from base types, applies "mutagen" modifiers, and ensures balanced distributions.
- **Naming Logic**: A syllable-based or thematic name generator that constructs names reflecting the creature's type and traits.
- **Silhouettes**: A visual classification system (e.g., Serpentine, Quadruped) determined by stats and types to ground the creature's physical form.
- **Biomes**: Contextual logic that places monsters in appropriate environments, influencing their traits and descriptions.
- **RNG Orchestration**: A controlled random number generation layer that allows for deterministic recreation of monsters via seeds.
- **Prompt Engine**: Translates structured monster data into natural language prompts for AI art generation.

## 3. What are the non-negotiable rules?

- **Stats are emergent, not assigned**: Final stats must flow from the combination of type, mutagens, and base seeds; they are never arbitrarily hardcoded.
- **Naming can be influenced by stats**: A bulky, high-defense monster should sound different from a speedy, fragile one.
- **Generators must remain composable**: Systems (like naming or visual generation) must work independently or together without tight coupling.
- **YAML is authoritative for content, not logic**: Data files define *what* exists (items, traits), while Python code defines *how* they interact.
- **Deterministic Seeds**: The same seed and configuration must always yield the exact same monster.

## 4. Current state

- Stat flow refactor complete
- Silhouette rules drafted
- Biome palette - WIP
- Naming pipeline partially integrated but promising, 'epithets' still a bit buggy
- Mutagen application logic updated with partial synergy support - WIP
- Visual prompt generation prototype active
- A HIGH priority should be assigned to populating the existing data sets that source MonsterSeed attributes.
