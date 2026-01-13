# **dex_entries.md - Module Purpose & Technical Canon**
_Describes the formatting and batch generation of Dex-style entries._

---

# dY- **1. Purpose of This Module**

`dex_entries.py` formats a fully prepared `MonsterSeed` into a readable,
Pokedex-style text block. It also supports batch generation of entries and
persists seeds to the monster cache during batch runs.

This module is the narrative output layer for text-based entries.

---

# dY- **2. Responsibilities**

`dex_entries.py` is responsible for:

### - Formatting
- Summarizing stats into a compact line
- Rendering type labels and mutagen summaries
- Formatting physical traits and held items

### - Batch generation
- Forging seeds in a loop
- Applying mutagens
- Writing entries to disk
- Saving seeds to cache

---

# dY- **3. Inputs & Data Dependencies**

This module consumes:

- `MonsterSeed` objects
- `mon_forge.forge_seed_monster()` and `mon_forge.apply_mutagens()`
- `monster_cache.save_monster()` and `monster_cache.OUTPUT_PATH`
- `forge_name.format_dual_type()`
- `monsterseed.choose_type_pair()` for batch generation

---

# dY- **4. Outputs**

`dex_entries.py` produces:

- formatted dex entry strings
- optional appended output files
- JSONL cache entries via `save_monster()` (batch generation)

---

# dY- **5. Data Flow**

```
forge_seed_monster()
    ->
apply_mutagens()
    ->
dex_formatter()
    ->
save_monster()
```

Batch generation repeats this flow per entry and appends to disk.

---

# dY- **6. Key Functions**

## **6.1 _summarize_stats()**
Formats stats into a fixed-order, compact summary line.

## **6.2 _summarize_physical_details()**
Formats physical traits and held items into a readable block.

## **6.3 dex_formatter()**
Assembles the full dex entry text for a `MonsterSeed`.

## **6.4 generate_dex_batch()**
Generates a batch of monsters, formats them, saves to cache, and optionally
writes to disk.

---

# dY- **7. Invariants & Guarantees**

- Uses a consistent stat order across entries.
- Expects `mutagens` to contain `major` and `utility` lists.
- Type formatting respects dual-type readability.
- Writes are append-only unless the caller changes behavior.

---

# dY- **8. Known Pitfalls / Refactor Notes**

- Batch generation retries until a valid type pair is found.
- The stat separator in `_summarize_stats()` is a non-ASCII glyph; keep it
  consistent if the format changes.
- Output files are appended without overwrite safeguards.

---

# dY- **9. Future Expansion Hooks**

- Add structured output formats (JSON, YAML).
- Include narrative flavor text from type notes and traits.
- Add per-entry metadata blocks (temper, kin data).

---

# dY- **10. AI Usage Notes**

When an AI agent interacts with this module, it should:

- avoid changing the dex format without updating downstream tooling
- keep stat ordering stable for determinism
- treat the formatter as pure output, not mutation logic
