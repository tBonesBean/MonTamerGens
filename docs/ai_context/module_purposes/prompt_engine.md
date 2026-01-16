# **prompt_engine.md - Module Purpose & Technical Canon**
_Describes the visual prompt construction layer for MonTamerGens._

---

# dY- **1. Purpose of This Module**

`prompt_engine.py` converts a fully forged `MonsterSeed` into a structured,
style-compliant image prompt for the pixel-art visual pipeline.

This module is the visual output layer for AI image generation.

---

# dY- **2. Responsibilities**

`prompt_engine.py` is responsible for:

### - Prompt assembly
- Translating seed attributes into visual descriptors
- Applying type and species visual guidance
- Incorporating mutagens, traits, and mood

### - Style compliance
- Enforcing the global art style header
- Injecting technical specs and pose guidance

---

# dY- **3. Inputs & Data Dependencies**

This module consumes:

- `MonsterSeed` objects
- `data.art_data` constants:
  - `STYLE_HEADER`
  - `TECHNICAL_SPECS`
  - `TYPE_VISUALS`
  - `SPECIES_VISUAL_OVERRIDES`
  - `VISUAL_TRANSLATION`
- `forge_name.format_dual_type()`

---

# dY- **4. Outputs**

It produces:

- a single formatted prompt string suitable for image generation

---

# dY- **5. Internal Logic Summary**

1. Read seed fields (type, form, habitat, traits, mutagens, mood).
2. Resolve the body plan via species overrides or type visuals.
3. Translate mutagens and traits into visual language.
4. Assemble prompt sections in a fixed order.
5. Return the final prompt string.

---

# dY- **6. Key Functions**

## **6.1 translate_term()**
Looks up a term in `VISUAL_TRANSLATION` and falls back to the raw term.

## **6.2 construct_mon_prompt()**
Builds the full prompt string for a given `MonsterSeed`.

---

# dY- **7. Invariants & Guarantees**

- Prompt formatting is deterministic given a fixed seed.
- Style header and technical specs are always present.
- Type and species visuals are prioritized over free-form descriptions.

---

# dY- **8. Known Pitfalls / Refactor Notes**

- Translation coverage depends on `VISUAL_TRANSLATION` completeness.
- Overly long mutagen/trait lists can crowd the prompt.

---

# dY- **9. Future Expansion Hooks**

- Add silhouette-driven descriptors from `choose_silhouette()`.
- Integrate palette rules and accent limits into the prompt.
- Add habitat-driven background cues.

---

# dY- **10. AI Usage Notes**

When an AI agent interacts with this module, it should:

- keep prompt structure stable for downstream tooling
- avoid adding conflicting descriptors
- ensure translations map to visual, not mechanical, language
