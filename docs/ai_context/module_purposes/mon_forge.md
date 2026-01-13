# **mon_forge.md — Module Purpose & Technical Canon**  
_Describes the role, responsibilities, data flow, and invariants of `mon_forge.py`._

---

# 🧩 **1. Purpose of This Module**

`mon_forge.py` is the **mutagen engine** of MonTamerGens.  
It takes a freshly‑forged `MonsterSeed` and applies:

- major mutagens  
- utility mutagens  
- stat multipliers  
- additive bonuses  
- tags  
- resistances  
- weaknesses  

It is the **second stage** of the monster generation pipeline, responsible for transforming a conceptual creature into a mechanically distinct entity.

This module is where monsters become **unique**.

---

# 🧱 **2. Responsibilities**

`mon_forge.py` is responsible for:

### ✔ Mutagen selection  
- Weighted sampling without replacement  
- Rarity‑driven weighting  
- Synergy multipliers  
- Type gating  
- Incompatibility gating  

### ✔ Mutagen application  
- Multiplicative stat adjustments  
- Additive stat adjustments  
- Tag assignment  
- Resist/weak parsing  
- Meta enrichment  

### ✔ Deterministic orchestration  
- Ensures stable selection order  
- Ensures reproducible outcomes when RNG is seeded  

### ✔ Final assembly  
- Applies mutagens  
- Generates name  
- Saves to cache  

---

# 🧬 **3. Inputs & Data Dependencies**

This module consumes:

### From `monsterseed.py`:
- A fully constructed `MonsterSeed` object

### From `data.py`:
- `MAJOR_MODS`  
- `UTILITY_MODS`  
- `TYPE_SYNERGY_BOOSTS`  
- `INCOMPATIBLE_TYPE_PAIRS`  
- `LEGACY_TYPE_MAP` (indirectly relevant)  

### From other modules:
- `forge_monster_name()`  
- `monster_cache.save_monster()`  

---

# 🔄 **4. Data Flow**

```
MonsterSeed
    ↓
apply_mutagens()
    ↓
forge_monster_name()
    ↓
monster_cache.save_monster()
    ↓
Final MonsterSeed returned
```

This module is the **second stage** of the pipeline.

---

# 🧠 **5. Key Functions**

## **5.1 rarity_to_weight()**
Converts a rarity value into a sampling weight.

- Higher rarity → lower weight  
- Guards against invalid or zero rarity  
- Supports exponent shaping via `RARITY_ALPHA`  

This ensures rare mutagens appear less often.

---

## **5.2 weighted_sample_without_replacement()**
A deterministic weighted sampler that:

- selects up to `k` items  
- never repeats items  
- respects weight distribution  
- handles float edge cases  
- returns strongest items if `k >= pool size`  

This is the backbone of mutagen selection.

---

## **5.3 apply_mutagens()**
The core of the module.

### Steps:

1. **Initialize seed buckets**  
   Ensures `mutagens.major`, `mutagens.utility`, `meta.tags`, etc. exist.

2. **Determine monster types**  
   Builds a set of `{primary_type, secondary_type}`.

3. **Build synergy context**  
   Collects existing mutagens for synergy stacking.

4. **Filter available mutagens**  
   For each mod:
   - check allowed types  
   - check incompatible types  
   - compute rarity weight  
   - apply synergy multipliers  
   - clamp synergy explosion  

5. **Weighted selection**  
   Uses `weighted_sample_without_replacement()` to pick:
   - `major_count` major mutagens  
   - `util_count` utility mutagens  

6. **Apply mutagen effects**  
   For each chosen mod:
   - apply multiplicative stat changes  
   - apply additive stat changes  
   - parse tags into:
     - `meta.tags`
     - `meta.resist`
     - `meta.weak`  

7. **Return modified seed**

This function is the **mechanical identity forge**.

---

## **5.4 generate_monster()**
A convenience orchestrator.

### Steps:

1. `forge_seed_monster()`  
2. `apply_mutagens()`  
3. `forge_monster_name()`  
4. `monster_cache.save_monster()`  

Returns the final, fully‑generated monster.

This is the **public entry point** for generating a complete creature.

---

# 🧩 **6. Mutagen Selection Logic**

### ✔ Allowed types  
A mutagen is only eligible if:

```
allowed_types is empty
OR
monster has at least one allowed type
```

### ✔ Incompatible types  
A mutagen is rejected if:

```
monster has ANY type in incompatible_types
```

### ✔ Rarity  
Weight = `1 / rarity^alpha`

### ✔ Synergy  
For each monster type:

```
if type in synergy_bonus:
    synergy_mult *= synergy_bonus[type]
```

### ✔ Hard cap  
`synergy_mult` is clamped by `MAX_SYNERGY_MULT`.

This prevents runaway weights.

---

# 🧬 **7. Mutagen Application Logic**

Each mutagen may contain:

### **mul:**  
Multiplicative stat adjustments  
(e.g., `"ATK": 1.15`)

### **add:**  
Additive stat adjustments  
(e.g., `"HP": 10`)

### **tags:**  
Parsed into:

- `meta.tags`  
- `meta.resist`  
- `meta.weak`  

Rules:

- `"Resist:X"` → `meta.resist.append("X")`  
- `"Weak:X"` → `meta.weak.append("X")`  
- anything else → `meta.tags.append(tag)`  

This keeps meta clean and structured.

---

# 🧱 **8. Invariants & Guarantees**

- Mutagens never duplicate  
- Stats remain integers  
- Resist/weak lists never contain prefixes  
- Synergy never exceeds `MAX_SYNERGY_MULT`  
- Mutagen selection is deterministic when RNG is seeded  
- Seed always contains:
  - `mutagens.major`  
  - `mutagens.utility`  
  - `meta.tags`  
  - `meta.resist`  
  - `meta.weak`  

---

# ⚠️ **9. Known Pitfalls / Refactor Notes**

### 1. Legacy type references  
Many mutagens still reference old types (`Aether`, `Gaian`, etc.).  
These must be migrated using `LEGACY_TYPE_MAP`.

### 2. Duplicate synergy keys  
Some mods reference synergy keys that no longer exist (`Mythic`, `Insect`, etc.).  
These should be mapped or removed.

### 3. Mutagen pre‑selection in MonsterSeed  
`monsterseed.py` selects one major + one utility mutagen.  
`mon_forge.py` selects additional mutagens.  
This is fine, but should be documented clearly.

### 4. Some utility mods lack rarity  
Defaults to `1`, but should be explicit for clarity.

---

# 🚀 **10. Future Expansion Hooks**

- Move all mutagen selection into `mon_forge`  
- Add mutagen categories (elemental, anatomical, emotional)  
- Add synergy based on:
  - traits  
  - habitat  
  - form  
  - tempers  
- Add mutagen conflict rules  
- Add mutagen evolution paths  

---

# 🟦 **11. AI Usage Notes**

When an AI agent interacts with this module, it should:

- never invent new mutagen fields  
- always respect allowed/incompatible types  
- never bypass weighted sampling  
- never apply mutagens outside `apply_mutagens()`  
- never mutate stats directly  
- always treat mutagens as additive layers  
- always call `generate_monster()` for full pipeline generation  

---

