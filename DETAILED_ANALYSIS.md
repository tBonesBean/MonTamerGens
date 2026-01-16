# MONTAMERGENS: Detailed Analysis (Post-Refactor)

Last updated: 2026-01-13 04:56:41 -07:00

## **Executive Summary**

MonTamerGens has begun a deliberate migration of its core type system from in-code dictionaries to YAML-driven content. The canonical type set and species forms have been moved into `seed_types.yaml` and `type_forms.yaml` respectively, and `monsterseed.py` has been updated to consume the new structures. I also started reconciling `data.py`, remapping several legacy type references so the mod dataset begins to align with the new taxonomy.

The migration has restored correct type/species/habitat read-paths and prevented the previous crash caused by an undefined `SEEDTYPE_ATTR`. However, the migration is incomplete: many mutagen and utility mod entries and some compatibility/synergy tables still reference legacy type names. Those must be reconciled before mutagen selection, synergy calculations, and other downstream systems behave predictably.

## **Update Log (2026-01-13)**

-   Normalized `seed_types.yaml` to the schema shape (list habitats, explicit tags).
-   Clarified that `seed_types_schema.md` requires `attributes.notes`.
-   Added module purpose docs for cli, dex_entries, forge_name, monster_cache, and reroll.
-   Added schemas/00_README.md and aligned schema filenames in the IntelliHub index.

---

## **1. Project Vision & Core Principles**

The project's manifesto and non-negotiable principles remain unchanged: data (YAML) defines content, Python defines behavior; generation must be deterministic; stats should emerge from composable inputs (types + mutagens + seed). The current refactor enforces the principle that YAML is authoritative for type/content definitions while code reads and interprets those structures.

### Key Points for this migration

-   Preserve deterministic output for a given seed and configuration.
-   Keep data/logic separation: YAML describes types, habitats, attributes, and forms; code applies generation rules.
-   Maintain composability so naming, visuals, and stat pipelines remain decoupled from raw content files.

---

## **2. Architecture & Data Flow Analysis**

This section describes how the generation pipeline currently behaves and where the migration has changed behavior.

### 2.1 The Source of the Break (before fixes)

Previously the pipeline used two incompatible type taxonomies simultaneously:

-   Legacy in-code taxonomy (examples: `Argent`, `Kinetic`, `Gaian`, `Vermillion`, etc.) present in `data.py` (`MAJOR_MODS`, `UTILITY_MODS`, `TYPE_SYNERGY_BOOSTS`, `INCOMPATIBLE_TYPE_PAIRS`, `HABITATS_BY_TYPE`).
-   New YAML taxonomy defined in `seed_types.yaml` (now: `Axiom`, `Spur`, `Echo`, `Flow`, `Bastion`, `Rift`, `Mire`, `Idol`, `Geist`, `Bloom`, `Vessel`, `Dread`) and `type_forms.yaml` for species.

Result: type selection (from YAML) succeeded but downstream lookups (habitat, attributes, mutagen compatibility, synergy) failed or were inconsistent because code still expected legacy names.

### 2.2 Data Flow: Step-by-step (current)

1. MonsterSeed.forge()

    - choose_type_pair(): Uses `SEED_TYPES_WEIGHTED` from `seed_types.yaml` — OK.
    - species selection: `FORMS_BY_TYPE` now loaded from `type_forms.yaml`. `monsterseed` handles both list and weighted dict shapes — OK.
    - habitat selection: `monsterseed` now reads `habitats` from `SEED_TYPE_DATA` (YAML) — OK (provided YAML defines habitats).
    - base stats/meta: `monsterseed` now reads attributes/tags from `SEED_TYPE_DATA` (no longer using missing `SEEDTYPE_ATTR`) — OK.

2. Mutagen selection and application

    - `MAJOR_MODS` and `UTILITY_MODS` are still hosted in `data.py`. Some entries have been remapped to the new types, but many still reference legacy names. As a result:
        - Candidate filtering for mutagens (based on `allowed_types`) may be incorrect.
        - Synergy bonuses referencing legacy type names do not activate.

3. Other consumers (naming, visuals, dex formatting)
    - Modules that map type -> naming components, palettes, or silhouettes may still reference legacy names and thus produce incorrect or missing values until updated.

---

## **3. Detailed Reconciliation Plan**

This is a prioritized, actionable plan to fully reconcile the codebase with the YAML-first type system. Items are ordered by risk and impact.

### Priority 1: Finish `monsterseed` migration and verify behavior

-   Status: Completed. `monsterseed.py` now:
    -   Uses `SEED_TYPE_DATA` for habitats and attributes.
    -   Selects species from `FORMS_BY_TYPE` whether it is a dict (weighted) or list.
    -   Applies stat multipliers/additions from per-type `attributes` entries.

Verification: Add a small test that forges one seed per type and asserts `species`, `habitat`, `stats`, and `meta` are present.

### Priority 2: Fully migrate `MAJOR_MODS` and `UTILITY_MODS`

-   Problem: Mutagens currently reference legacy type names (many entries). This prevents correct filtering and synergy application.
-   Action:
    1. Create a mapping table from legacy types → new canonical types.
    2. Update every `allowed_types` list and every `synergy_bonus` key to use new names.
    3. Where a legacy type had no direct analogue, choose the best-fit based on semantics (I can assist with mapping decisions).
    4. Run tests to ensure mutagens are selectable for intended types.

### Priority 3: Migrate and validate `TYPE_SYNERGY_BOOSTS` and `INCOMPATIBLE_TYPE_PAIRS`

-   Problem: These tables are still partially legacy; incomplete remapping yields incorrect secondary type weights and forbidden pair checks.
-   Action: review each pair, confirm semantics, and express them using the new type names. Consider consolidating into YAML to keep all type-driven content together.

### Priority 4: Remove legacy habitat & type cruft

-   Action: Remove `HABITATS_BY_TYPE` (if present elsewhere) and any other static type lists that duplicate YAML. Ensure no module imports those symbols.

### Priority 5: Update other subsystems

-   `forge_name.py`: Replace legacy-type hooks for prefixes/suffixes with a YAML-driven mapping or updated logic keyed by `SEED_TYPE_DATA` metadata.
-   `prompt_engine.py` / `gen_visuals.py`: Update type → silhouette/palette mappings to use new type names (or move mappings into YAML).
-   `mon_forge.py` / `dex_entries.py`: Confirm they consume the same `MonsterSeed` shape and don't rely on legacy type strings.

### Priority 6: Tests and CI

-   Update unit tests that assert legacy type strings or directly import the old `FORMS_BY_TYPE` dict.
-   Add a regression test that forges a seed for every type to detect missing habitats/attributes or failing mod selection.

---

## **4. Migration Notes & Code Changes (what to watch for)**

-   `SEED_TYPE_DATA` shape: YAML entries should expose `attributes` (with `mul`/`add`), optional `tags`, and `habitats`. Example shape should be standardized and documented.
-   `FORMS_BY_TYPE` now loads from `type_forms.yaml`. The loader supports dict (weighted) or list shapes; prefer dict if you need per-form weighting.
-   Move type-driven configuration (mod allowed_types, palettes, name tokens) into YAML where practical to keep content editable by non-developers.

---

## **5. Recommended immediate steps**

1. Run the test suite (`pytest`) and capture failing locations referencing legacy type names.
2. Finish the bulk remap of `MAJOR_MODS` and `UTILITY_MODS` entries to the new types. I can continue this mapping — it requires some semantic judgment.
3. Add the small forge-per-type regression test described above.
4. Consider migrating `TYPE_SYNERGY_BOOSTS` and `INCOMPATIBLE_TYPE_PAIRS` into YAML so all type content is collocated.

---

If you'd like I will now:

-   continue remapping the remainder of `MAJOR_MODS` and `UTILITY_MODS` to the new types and
-   run `pytest` to produce a prioritized list of remaining failures.

## Which should I do next?

## What I changed

-   Rewrote `src/mongens/data/seed_types.yaml` to the new canonical types: `Axiom, Spur, Echo, Flow, Bastion, Rift, Mire, Idol, Geist, Bloom, Vessel, Dread`.
-   Replaced the old `type_forms` dictionary with `src/mongens/data/type_forms.yaml` containing example species lists per new type.
-   Updated `src/mongens/monsterseed.py` to:
    -   Pick `species` safely from either list or weighted dict in `FORMS_BY_TYPE`.
    -   Read `habitats` and per-type attributes from `SEED_TYPE_DATA` instead of legacy `HABITATS_BY_TYPE`/`SEEDTYPE_ATTR`.
    -   Apply stat multipliers/additions using `SEED_TYPE_DATA[<type>].get("attributes", {})`.
-   Remapped the initial portion of `src/mongens/data/data.py`:
    -   Replaced legacy keys in `TYPE_SYNERGY_BOOSTS` and `INCOMPATIBLE_TYPE_PAIRS` with pairs expressed using the new type names (examples: `Spur`, `Axiom`, `Bloom`, `Flow`, `Idol`, `Dread`, etc.).
    -   Updated a first subset of `MAJOR_MODS` entries to use the new type names in their `allowed_types` and `synergy_bonus` fields.

These edits restore a consistent read-path for selecting types, forms, habitats, and base attributes when forging a `MonsterSeed`.

---

## Current state (what works now)

-   Type selection: `choose_type_pair()` uses `SEED_TYPES_WEIGHTED` loaded from `seed_types.yaml` and returns new-type names.
-   Species selection: `FORMS_BY_TYPE` (loaded from `type_forms.yaml`) supplies species; `monsterseed` handles both lists and weighted dicts.
-   Habitat and attributes: `monsterseed` now reads `habitats` and `attributes` from `SEED_TYPE_DATA` (the YAML loader), so habitats defined in the YAML are used.
-   Base stat calculation and meta tag extraction use `SEED_TYPE_DATA` and no longer rely on the missing `SEEDTYPE_ATTR` symbol.

---

## Remaining issues / reconciliation tasks (high priority)

1. Finish migrating `MAJOR_MODS` and `UTILITY_MODS` to the new type taxonomy

    - Many entries still reference legacy types (e.g., `Argent`, `Aether`, `Chrono`, `Gaian`, `Vermillion`, `Veridian`, `Azure`, etc.).
    - Action: systematically map legacy type names to the best-fit new types (I began this mapping in `data.py`), then update every `allowed_types` and `synergy_bonus` to use the new names.
    - Note: this step is the most time-consuming but is required for mutagen selection and effective stat/tag application.

2. Audit `UTILITY_MODS` (not yet updated)

    - Ensure the `allowed_types` and `tags` in utility mods align with the new type semantics.

3. Validate `TYPE_SYNERGY_BOOSTS` and `INCOMPATIBLE_TYPE_PAIRS` globally

    - I replaced the top-level examples with new-type pairs but the dataset must be reviewed for completeness and thematic correctness.

4. Remove legacy habitat sources

    - Remove `HABITATS_BY_TYPE` and any other in-code habitat lists if they were left elsewhere; YAML should be authoritative.

5. Update other modules to the new type shape

    - `mon_forge.py`: confirm it consumes `MonsterSeed` fields that now derive from `SEED_TYPE_DATA` (habitats, species, attributes).
    - `forge_name.py`: ensure naming rules that reference legacy type names are updated to produce appropriate syllables/prefixes for new types.
    - `prompt_engine.py` / `gen_visuals.py`: ensure type-to-silhouette/palette mappings reference the new types.
    - `dex_entries.py`: validate formatting code still expects fields present on `MonsterSeed` (habitat, meta, tags).

6. Tests and data fixtures
    - Update tests that reference old type names or rely on `data.FORMS_BY_TYPE` being a dict in-code.
    - Add small unit tests ensuring `MonsterSeed.forge()` returns a valid seed for all new types.

---

## Suggested immediate next steps (concrete)

1. Complete `MAJOR_MODS` and `UTILITY_MODS` mapping to new types (bulk edit). I can continue this mapping if you want; it requires semantic judgment per mod.
2. Run `pytest` and capture failing tests — they will show remaining places referencing legacy types.
3. Update naming and prompt rules in `forge_name.py` and `prompt_engine.py` to match the new type semantics.
4. Add regression tests: one that forges a seed per new type and verifies `species`, `habitat`, `stats`, and `meta` are non-empty and that mutagens are chosen from mods whose `allowed_types` include the seed's type.

---

If you want, I will:

-   finish remapping all `MAJOR_MODS` and `UTILITY_MODS` entries to the new types (I started the process), and
-   run the test suite to enumerate remaining breakages and produce a prioritized fix list.

Which would you prefer I do next? (I recommend running tests to surface the full scope.)
