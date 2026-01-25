# **forge_name.md - Module Purpose & Technical Canon**
_Describes deterministic naming logic for MonTamerGens monsters._

---

# dY- **1. Purpose of This Module**

`forge_name.py` generates deterministic, lore-aligned monster names. It uses
type-biased syllable pools, a weighted syllable chain, and optional epithets
derived from applied mutagens.

This module is the identity layer of the pipeline.

---

# dY- **2. Responsibilities**

`forge_name.py` is responsible for:

### - Name generation
- Deterministic naming from seed inputs
- Type-biased prefix/suffix selection
- Syllable-chain fallback when needed

### - Epithets and formatting
- Optional mutagen-driven epithets
- Dual-type label formatting
- Slug-safe name formatting

---

# dY- **3. Inputs & Data Dependencies**

This module consumes:

- `MonsterSeed` objects (or seed-like objects)
- primary and secondary type names
- mutagen lists (`major`, `utility`)
- optional naming salts and style flags

It relies on module-level data:

- `_SYLLABLE_CHAIN`
- `_TYPE_FLAVORS`
- `_MAJOR_EPITHETS`, `_UTILITY_EPITHETS`, `_GENERIC_EPITHETS`
- `TYPE_TO_ADJ`

---

# dY- **4. Outputs**

It produces:

- name strings
- updated `MonsterSeed.name` values via `forge_monster_name()`
- alternative name lists for display or selection

---

# dY- **5. Internal Logic Summary**

1. Build a stable hash seed from `idnum`, types, and mutagens.
2. Prefer type-flavored prefix/suffix assembly.
3. Fall back to syllable-chain generation if needed.
4. Optionally attach a mutagen-based epithet.
5. Truncate and return the final name.

---

# dY- **6. Key Functions**

## **6.1 deterministic_name()**
Core deterministic naming logic driven by type flavor and mutagens.

## **6.2 format_dual_type()**
Formats dual-type labels into readable adjective-noun strings.

## **6.3 forge_monster_name()**
Mutates a `MonsterSeed` by assigning its name.

## **6.4 generate_alternative_names()**
Generates non-deterministic alternatives by varying the salt.

## **6.5 slugify()**
Creates a slug-safe identifier from a name string.

---

# dY- **7. Invariants & Guarantees**

- Identical inputs produce identical names when salt is stable.
- Type flavor is preferred when pools exist.
- Epithets are derived from mutagens when available.

---

# dY- **8. Known Pitfalls / Refactor Notes**

- Missing type flavor entries can raise a KeyError.
- Epithet pools must be kept aligned with mutagen keys.
- Alternative name generation is intentionally non-deterministic.

---

# dY- **9. Future Expansion Hooks**

- Add language packs or phoneme profiles per biome.
- Let traits and forms bias syllable selection.
- Add name length heuristics per form or archetype.

---

# dY- **10. AI Usage Notes**

When an AI agent interacts with this module, it should:

- keep deterministic inputs stable for reproducibility
- avoid adding epithets that conflict with the mutagen schema
- update type adjective mappings when types change
