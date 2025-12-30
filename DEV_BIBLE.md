# DEV_BIBLE.MD: Master Instructions for AI Contributors

## ❗ ATTENTION AI AGENT
---

# 🌑 **MonTamerGens — Unified Design Bible (v1.0)**  
*A living canon for the MonTamerGens universe, systems, aesthetics, and architecture.*

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
Located in `src/mongens/data/`:

- `data.py` — base stats, types, mutagens  
- YAML files — traits, items, wounds  
- `art_data.py` — visual translation dictionary  

## **4.2 Generation Pipeline**
1. **MonsterSeed.forge()**  
   - type selection  
   - base stats  
   - initial attributes  

2. **mon_forge.generate_monster()**  
   - mutagen application  
   - synergy logic  
   - stat shaping  

3. **forge_name.py**  
   - deterministic naming  
   - syllable logic  
   - epithet generation  

4. **monster_cache.py**  
   - JSONL append  
   - unique ID assignment  

5. **prompt_engine.py**  
   - visual prompt construction  
   - art direction integration  

6. **dex_entries.py**  
   - formatted text output  
   - lore synthesis  

## **4.3 Determinism Rules**
- RNG must be seedable  
- Same seed = same monster  
- Mutagen order must be stable  
- Naming must be reproducible  

---

# **5. Systems Design**

## **5.1 Stats**
- Derived from type + mutagens  
- No hardcoded final values  
- Curves influenced by Kin Drive  

## **5.2 Mutagens**
### Major Mutagens  
- Always affect silhouette, color, aura  
- High‑impact visual identity  

### Utility Mutagens  
- Affect markings, accessories, mood  
- Low‑impact but flavorful  

## **5.3 Traits**
- Always visible  
- Always meaningful  
- Always serialized  

## **5.4 Evolution (Sparks)**
Evolution triggers include:

- emotional states  
- environmental events  
- narrative beats  
- bond strength  
- wound resolution  

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

---

## **9. Versioning**
This document is **v1.1** — updated to reflect the current canonical type taxonomy, YAML-first content model, and recent data migration.  
Changes in this release:
- Migrated core types to YAML (`seed_types.yaml` / `type_forms.yaml`).
- Reconciled major mutagens and utility mods to canonical type names.
- Adjusted generation code paths to use `SEED_TYPE_DATA` and `MonsterSeed.forge()` improvements.

All future edits should continue the principle: changes must be additive, clarifying, or canon‑strengthening.

---
