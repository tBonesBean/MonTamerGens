# schemas/00_README.md - Schema Index & Usage Guide
_Your guide to the canonical data shapes used by MonTamerGens._

---

## Purpose of This Folder

This directory contains Markdown schema files that define the required structure,
allowed fields, constraints, and validation rules for YAML content and core data
structures. Treat these documents as the source of truth when editing any data
file under `src/mongens/data/` or adjusting the corresponding validators in
`src/mongens/data/data.py`.

---

## Folder Contents

```plaintext
schemas/
  00_README.md
  base_stats_schema.md
  mutagen_schema.md
  seed_types_schema.md
  trait_schema.md
  type_form_schema.md
```

---

## Document Overview

### [base_stats_schema.md](base_stats_schema.md)
Defines the stat block shape and valid stat keys for the engine baseline.

### [mutagen_schema.md](mutagen_schema.md)
Defines the required fields, tags, and constraints for major and utility mutagens.

### [seed_types_schema.md](seed_types_schema.md)
Defines the structure of seed type entries, including habitats, attributes,
and required notes.

### [trait_schema.md](trait_schema.md)
Defines the shape and validation rules for physical traits.

### [type_form_schema.md](type_form_schema.md)
Defines the mapping from types to available forms and their weights.

---

## How to Use This Folder

- Check the relevant schema before editing a YAML file.
- Follow required vs optional fields exactly as specified.
- Keep values within documented constraints (weights, stat keys, tags).
- Update schemas first if a data shape change is needed, then update YAML and validation logic.

---

## AI Usage Notes

When generating or editing data files:

- Do not invent new fields that are not in the schema.
- Use the schema to confirm required keys and value types.
- Keep content deterministic, consistent, and easy to validate.

If something is not documented here, it is not canonical yet.
