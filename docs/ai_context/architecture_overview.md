# **MonTamerGens — Architecture Overview**

_A complete, accurate, and refactor‑aligned map of the engine._

Last updated: 2026-01-13 04:56:41 -07:00

---

# 🌐 **1. High‑Level Summary**

MonTamerGens is a **modular, data‑driven creature generation engine** built around a deterministic pipeline:

```
YAML Data → MonsterSeed → Mutagen Forge → Naming → Output Layer
```

It produces:

- canonical species seeds
- unique monster instances
- dex entries
- visual prompts
- persistent cached monsters
- rerolled variants
- Kin‑aligned starter candidates

The system is designed for:

- extensibility
- deterministic generation
- content‑driven evolution
- narrative richness
- future game integration

---

# 🧱 **2. Layered Architecture**

MonTamerGens is composed of **eight major layers**, each with a clear responsibility:

```
1. Data Layer
2. Seed Forge Layer
3. Mutagen Forge Layer
4. Naming Layer
5. Output Layer (Dex + Visuals)
6. Persistence Layer
7. Post‑Forge Mutation Layer (Reroll)
8. CLI Orchestration Layer
```

Each layer is independent, testable, and replaceable.

---

# 📦 **3. Data Layer (data.py + YAML)**

**Purpose:** Load, validate, normalize, and expose all content.

### Responsibilities:

- Load YAML files:
  - seed types
  - type forms
  - physical traits
  - held items
  - tempers
  - mutagens
- Validate schema correctness
- Normalize shapes
- Provide canonical data structures
- Maintain backward compatibility via `LEGACY_TYPE_MAP`

### Key Outputs:

- `SEED_TYPE_DATA`
- `SEED_TYPES_WEIGHTED`
- `SEED_TYPES`
- `FORMS_BY_TYPE`
- `BASE_STATS`
- `MAJOR_MODS`
- `UTILITY_MODS`
- `TYPE_SYNERGY_BOOSTS`
- `INCOMPATIBLE_TYPE_PAIRS`

This layer is the **source of truth** for all content.

---

# 🌱 **4. Seed Forge Layer (monsterseed.py)**

**Purpose:** Create a deterministic “intent snapshot” of a monster.

### Responsibilities:

- Select primary/secondary types
- Select form (species silhouette)
- Select habitat
- Select initial mutagens (1 major, 1 utility)

- Select physical traits
- Select held item
- Compute base stats
- Compute base meta (tags/resist/weak)
- Produce a complete `MonsterSeed` dataclass

### Output:

A fully formed **MonsterSeed**, ready for mutagen forging.

This is the **heart** of the engine.

---

# 🔥 **5. Mutagen Forge Layer (mon_forge.py)**

**Purpose:** Apply major + utility mutagens to shape mechanical identity.

### Responsibilities:

- Filter mutagens by:
  - allowed types
  - incompatible types
  - rarity
  - synergy multipliers
- Weighted sampling without replacement
- Apply:
  - multiplicative stat changes
  - additive stat changes
  - tags
  - resistances
  - weaknesses
- Save final monster to cache
- Produce a fully forged monster

### Output:

A **mechanically complete monster**, ready for naming and output.

This is the **muscle** of the engine.

---

# 🔤 **6. Naming Layer (forge_name.py)**

**Purpose:** Generate deterministic, pronounceable, lore‑aligned names.

### Responsibilities:

- Type‑biased prefixes/suffixes
- Syllable chain fallback
- Mutagen‑driven epithets
- Dual‑type formatting
- Deterministic RNG seeding
- Alternative name generation

### Output:

A monster with a **canonical name**.

This is the **identity layer** of the engine.

---

# 📘 **7. Output Layer**

## 7.1 Dex Formatting (dex_entries.py)

**Purpose:** Produce Pokédex‑style text entries.

### Responsibilities:

- Format:
  - name
  - form
  - types
  - mutagens
  - stats
  - habitat
  - traits
  - meta tags
- Save to text file
- Save seeds to cache

This is the **narrative output layer**.

---

## 7.2 Visual Prompt Generation (prompt_engine.py + gen_visuals.py)

**Purpose:** Produce detailed image prompts for AI art.

### Responsibilities:

- Convert monster attributes into visual descriptors
- Integrate:
  - type
  - form
  - traits
  - mutagens
  - habitat
  - meta tags
- Output a Stable Diffusion‑style prompt

This is the **visual output layer**.

---

# 💾 **8. Persistence Layer (monster_cache.py)**

**Purpose:** Store and retrieve monsters across sessions.

### Responsibilities:

- Generate unique IDs
- Append seeds to JSONL cache
- Load seeds by ID
- Reconstruct MonsterSeed objects
- Ensure ID uniqueness

This is the **storage backbone** of the engine.

---

# 🔁 **9. Post‑Forge Mutation Layer (reroll.py)**

**Purpose:** Modify existing monsters while preserving identity lineage.

### Responsibilities:

- Load monster from cache
- Reroll:
  - physical traits
  - major mutagens
- Recompute stats from scratch
- Reapply mutagens
- Reforge name
- Save as a new monster

This is the **mutation/evolution layer**.

---

# 🧭 **10. CLI Orchestration Layer (cli.py)**

**Purpose:** Provide user‑facing commands to drive the engine.

### Commands:

- `dexentry` → canonical species entries
- `unique` → wild monster instances
- `alternatives` → name variants
- `artprompt` → visual prompts
- `list` → available content
- `lumenkin` → Kin starter candidates
- `reroll` → mutate existing monsters

This is the **interface layer**.

---

# 🌟 **11. Kin Resonance Subsystem (prototype)**

**Purpose:** Generate starter monsters influenced by player resonance.

### Responsibilities:

- Interpret resonance values
- Select drives, wounds, sparks
- Attach Kin metadata to seeds

This subsystem is embryonic but architecturally important.

---

# 🧬 **12. Full Pipeline Overview**

```
YAML Data
    ↓
Data Layer (load + validate + normalize)
    ↓
MonsterSeed.forge()
    ↓
apply_mutagens()
    ↓
forge_monster_name()
    ↓
[Branch A] dex_formatter() → text output
[Branch B] construct_mon_prompt() → visual output
[Branch C] save_monster() → persistence
[Branch D] reroll_monster_attributes() → mutation
```

This is the **complete lifecycle** of a monster.

---

# 🚀 **13. Future Expansion Hooks**

The architecture naturally supports:

- evolutions
- biome‑driven stat shifts
- emotional resonance systems
- battle simulation
- procedural lore generation
- visual silhouette selection
- quest integration
- item drops
- breeding systems
- encounter tables
- world generation

Your foundation is _strong_.

---

# 🟦 **14. Design Principles**

MonTamerGens is built on:

- **Determinism**
- **Data‑driven content**
- **Layered modularity**
- **Narrative coherence**
- **Extensibility**
- **Backward compatibility**
- **Separation of concerns**

This is why the system feels so alive.

---
