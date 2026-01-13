# **cli.md - Module Purpose & Technical Canon**
_Describes the role, responsibilities, and command map of `cli.py`._

---

# dY- **1. Purpose of This Module**

`cli.py` is the user-facing entry point for MonTamerGens. It parses command-line
arguments and orchestrates the generation pipeline to create monsters, dex
entries, prompts, and rerolls.

This module is the interface layer between humans and the engine.

---

# dY- **2. Responsibilities**

`cli.py` is responsible for:

### - Command definition
- Defining subcommands and flags with `argparse`
- Providing help text and usage guidance

### - Orchestration
- Translating flags into pipeline inputs
- Calling the appropriate generation functions

### - Output handling
- Printing results to stdout
- Writing files for dex entries and prompts
- Saving or loading cached monsters

---

# dY- **3. Inputs & Data Dependencies**

`cli.py` consumes:

### From `data.py`
- `SEED_TYPES`, `SEED_TYPES_WEIGHTED`
- `ALL_HABITATS`
- `MAJOR_MODS`, `UTILITY_MODS`
- `KIN_WOUNDS`

### From pipeline modules
- `mon_forge.generate_monster()`
- `dex_entries.dex_formatter()`
- `forge_name.generate_alternative_names()`
- `prompt_engine.construct_mon_prompt()`
- `monster_cache.load_monster()` and `monster_cache.save_monster()`
- `monsterseed.choose_type_pair()` and `monsterseed.weighted_choice()`
- `reroll.reroll_monster_attributes()` (imported on demand)

---

# dY- **4. Outputs**

The CLI produces:

- printed summaries to stdout
- appended dex entry files (text)
- appended prompt files (text)
- JSONL cache entries via `save_monster()`

---

# dY- **5. Internal Logic Summary**

1. Parse args and subcommands.
2. Resolve primary and secondary types.
3. Load an existing seed or generate a new one.
4. Execute command-specific behavior.
5. Print output and optionally persist artifacts.

---

# dY- **6. Key Functions**

## **6.1 main()**
Defines CLI arguments and dispatches command logic.

## **6.2 _get_monster_types_from_args()**
Resolves primary and secondary types, respecting weights and compatibility.

## **6.3 _get_or_generate_seed()**
Loads a cached monster by PIN or generates a new one.

## **6.4 _generate_kin_properties()**
Placeholder logic for Kin passives, drives, wounds, and sparks.

---

# dY- **7. Invariants & Guarantees**

- Uses canonical type lists and weights from `data.py`.
- Honors compatibility rules via `choose_type_pair()`.
- Uses `generate_monster()` for full pipeline generation.

---

# dY- **8. Known Pitfalls / Refactor Notes**

- `generate_monster()` saves to cache even when the user does not request JSON output.
- The `artprompt` default output path is hard-coded to a local desktop path.
- Error handling is print-based and not standardized.

---

# dY- **9. Future Expansion Hooks**

- Add config support for output paths and defaults.
- Move command handlers into separate modules.
- Add batch generation for prompts and alternatives.
- Support structured output formats (JSON, CSV).

---

# dY- **10. AI Usage Notes**

When an AI agent interacts with this module, it should:

- treat CLI code as orchestration, not core logic
- keep commands aligned with pipeline invariants
- update help text whenever new flags are introduced

