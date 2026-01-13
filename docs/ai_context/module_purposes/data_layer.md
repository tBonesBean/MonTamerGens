# **data_layer.md — Data Layer Purpose & Technical Canon**  
_Describes the role, responsibilities, data flow, validation rules, and invariants of `data.py`._

---

# 🧩 **1. Purpose of This Module**

`data.py` is the **content backbone** of MonTamerGens.  
It loads, validates, normalizes, and exposes all YAML‑driven content used by the generation pipeline.

If `monsterseed.py` is the heart,  
and `mon_forge.py` is the muscle,  
then `data.py` is the **circulatory system** that feeds every subsystem with structured, canonical truth.

This module ensures:

- content is consistent  
- content is safe  
- content is deterministic  
- content is future‑proof  
- content is decoupled from logic  

It is the **single source of truth** for all content in the engine.

---

# 🧱 **2. Responsibilities**

`data.py` is responsible for:

### ✔ Loading YAML content  
- seed types  
- type forms  
- traits  
- items  
- tempers  
- mutagens  
- any future content categories  

### ✔ Validating YAML structure  
- required keys  
- allowed keys  
- type correctness  
- stat references  
- weight constraints  
- cross‑file consistency  

### ✔ Normalizing content  
- flattening nested structures  
- ensuring consistent shapes  
- converting weights to floats  
- ensuring lists/dicts are predictable  

### ✔ Exposing canonical data structures  
- `SEED_TYPE_DATA`  
- `SEED_TYPES_WEIGHTED`  
- `SEED_TYPES`  
- `FORMS_BY_TYPE`  
- `BASE_STATS`  
- `MAJOR_MODS`  
- `UTILITY_MODS`  
- `TYPE_SYNERGY_BOOSTS`  
- `INCOMPATIBLE_TYPE_PAIRS`  
- `LEGACY_TYPE_MAP`  

### ✔ Backward compatibility  
- maps legacy type names to new canonical types  
- supports legacy YAML shapes  

### ✔ Content integrity  
- ensures no invalid stats  
- ensures no missing forms  
- ensures no malformed mutagens  
- ensures no incompatible type references  

---

# 🧬 **3. Inputs & Data Dependencies**

`data.py` consumes:

### YAML files:
- `seed_types.yaml`  
- `type_forms.yaml`  
- `physical_traits.yaml`  
- `held_items.yaml`  
- `kin_wounds.yaml`  
- any future YAML content  

### Python modules:
- `yaml.safe_load`  
- `pathlib.Path`  

It exposes all normalized content to:

- `monsterseed.py`  
- `mon_forge.py`  
- `forge_name.py`  
- `prompt_engine.py`  
- `dex_entries.py`  
- any future systems  

---

# 🔄 **4. Data Flow**

```
YAML files
    ↓
_load_yaml()
    ↓
_load_seed_types_data()
    ↓
_validate_seed_type_data()
_validate_type_forms()
    ↓
_normalize_seed_type_data()
    ↓
Canonical data structures exported
```

This module is the **first stage** of the entire engine.

---

# 🧠 **5. Key Functions**

## **5.1 _load_yaml()**
Generic YAML loader.

- loads file  
- parses with `yaml.safe_load`  
- raises errors for missing or invalid files  

Used for all non‑seed‑type YAML.

---

## **5.2 _load_seed_types_data()**
Specialized loader for `seed_types.yaml`.

Returns:

- `types_data` — full dict of type → attributes  
- `types_weighted` — type → weight  

Ensures:

- each entry has a `name`  
- weight is a float  
- YAML is a list  

---

## **5.3 _validate_seed_type_data()**
Ensures each seed type:

- has valid attributes  
- uses known stats  
- uses numeric multipliers  
- uses numeric additive values  
- has valid habitats  

This enforces the **schema contract** for seed types.

---

## **5.4 _validate_type_forms()**
Ensures:

- every type in `type_forms.yaml` exists in `seed_types.yaml`  
- each form has:
  - a name  
  - a weight  
  - optional notes  
- weights are positive numbers  

This enforces cross‑file consistency.

---

## **5.5 _normalize_seed_type_data()**
Converts raw YAML into a predictable shape:

```
{
  "Axiom": {
    "weight": 1.0,
    "habitats": [...],
    "attributes": {
      "mul": {...},
      "add": {...},
      "tags": [...]
    }
  },
  ...
}
```

This ensures all consumers see the same structure.

---

## **5.6 _remap_type()**
Maps legacy type names to canonical ones.

Used for:

- mutagen migration  
- synergy tables  
- compatibility tables  
- future content cleanup  

---

## **5.7 _normalize_mods()**
Normalizes mutagen definitions to use canonical type names.

This is the **migration engine** for legacy content.

---

# 🧩 **6. Canonical Data Structures**

`data.py` exports the following:

### **6.1 SEED_TYPE_DATA**
Normalized type definitions.

### **6.2 SEED_TYPES_WEIGHTED**
Type → weight mapping.

### **6.3 SEED_TYPES**
Sorted list of type names.

### **6.4 FORMS_BY_TYPE**
Mapping of type → forms (from YAML).

### **6.5 BASE_STATS**
Default stat block.

### **6.6 MAJOR_MODS / UTILITY_MODS**
Mutagen dictionaries.

### **6.7 TYPE_SYNERGY_BOOSTS**
Pairwise synergy multipliers.

### **6.8 INCOMPATIBLE_TYPE_PAIRS**
Forbidden type combinations.

### **6.9 LEGACY_TYPE_MAP**
Legacy → canonical type mapping.

---

# 🧱 **7. Invariants & Guarantees**

- All YAML content is validated before use  
- All types have:
  - valid stats  
  - valid habitats  
  - valid attributes  
- All forms belong to valid types  
- All weights are positive floats  
- All mutagens reference valid types  
- All legacy types are remappable  
- All exported structures are deterministic  

This module guarantees **content integrity**.

---

# ⚠️ **8. Known Pitfalls / Refactor Notes**

### 1. Mutagen dictionaries contain legacy types  
These must be migrated using `LEGACY_TYPE_MAP`.

### 2. Some synergy keys reference old type names  
These should be updated to canonical names.

### 3. Some mutagens reference nonexistent types  
These should be flagged and corrected.

### 4. YAML shape drift  
`tags` may appear under:
- `attributes.tags`  
- `meta.tags`  
- top‑level `tags`  

Normalization handles this, but schema docs should standardize it.

---

# 🚀 **9. Future Expansion Hooks**

- Add schema validation for mutagens  
- Add schema validation for traits/items  
- Add schema validation for tempers  
- Add YAML‑driven synergy tables  
- Add YAML‑driven incompatibility tables  
- Add versioning metadata to YAML  
- Add linting tools for content authors  

---

# 🟦 **10. AI Usage Notes**

When an AI agent interacts with this module, it should:

- never invent new fields  
- never bypass validation  
- always respect normalized shapes  
- always use exported structures, not raw YAML  
- never mutate exported structures at runtime  
- treat `data.py` as read‑only canonical truth  

---
