# **reroll.md - Module Purpose & Technical Canon**
_Describes the post-forge mutation layer for existing monsters._

---

# dY- **1. Purpose of This Module**

`reroll.py` re-rolls selected attributes of an existing cached monster and
creates a new instance. It preserves identity while allowing targeted mutation
(traits or major mutagens).

---

# dY- **2. Responsibilities**

`reroll.py` is responsible for:

### - Attribute mutation
- Re-rolling physical traits
- Re-rolling major mutagens

### - Reconstruction
- Rebuilding stats and meta from base types
- Re-forging the monster name
- Saving the new monster to cache

---

# dY- **3. Inputs & Data Dependencies**

This module consumes:

- a monster PIN (unique ID)
- `reroll_options` describing which fields to re-roll
- data from `data.py`:
  - `PHYSICAL_TRAITS`
  - `HELD_ITEMS`
  - `MAJOR_MODS`
  - `UTILITY_MODS`
- helpers from `monsterseed.py`:
  - `calculate_base_stats()`
  - `get_base_meta()`
  - `weighted_choice()`
- `mon_forge.rarity_to_weight()`
- `monster_cache.load_monster()` and `monster_cache.save_monster()`

---

# dY- **4. Outputs**

It produces:

- a new `MonsterSeed` object with updated traits or mutagens
- a new cache entry with a fresh unique ID

---

# dY- **5. Internal Logic Summary**

1. Load the original monster from cache.
2. Deep-copy the seed to preserve lineage.
3. Re-roll selected fields.
4. Rebuild stats and meta from base types plus mutagens.
5. Re-forge the name and save the new monster.

---

# dY- **6. Key Functions**

## **6.1 _choose_physical_traits()**
Selects one or two weighted physical traits.

## **6.2 _choose_held_item()**
Selects a held item with a probability gate.

## **6.3 apply_mutagens_to_stats()**
Applies mutagen effects to clean base stats and meta.

## **6.4 reroll_monster_attributes()**
Public entry point for re-rolling a cached monster.

---

# dY- **7. Invariants & Guarantees**

- Re-rolls operate on a deep copy of the original seed.
- Major mutagens do not repeat the existing major.
- Stats and meta are rebuilt from base types before mutagens apply.
- New seeds are saved as distinct cache entries.

---

# dY- **8. Known Pitfalls / Refactor Notes**

- The major reroll filters use `required_types`, not `allowed_types`.
- The success message prints `meta.get("pin")`, but the cache uses `meta.unique_id`.
- `_choose_held_item()` exists but is not used.

---

# dY- **9. Future Expansion Hooks**

- Support re-rolling utility mutagens and forms.
- Add lineage metadata linking parent and child.
- Add deterministic rerolls based on explicit seeds.

---

# dY- **10. AI Usage Notes**

When an AI agent interacts with this module, it should:

- treat re-rolls as lineage-preserving mutations
- avoid mutating the original cached monster in place
- re-run stat and meta reconstruction after any changes
