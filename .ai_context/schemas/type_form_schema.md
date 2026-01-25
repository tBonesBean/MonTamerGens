# **type_form_schema.md — Canonical Schema for `type_forms.yaml`**  
_Describes the required structure, allowed fields, constraints, and validation rules for type → form mappings._

---

# 🌿 **1. Purpose of This Schema**

This schema defines the **canonical shape** of `type_forms.yaml`, which maps each seed type to its possible forms (species silhouettes). It ensures:

- every type has valid forms  
- every form has a weight  
- every form has optional descriptive notes  
- all types in this file exist in `seed_types.yaml`  
- the structure remains predictable for `MonsterSeed.forge()`  

This schema is enforced by:

- `_validate_type_forms()` in `data.py`  
- the form selection logic in `MonsterSeed.forge()`  

---

# 🧱 **2. High-Level Structure**

`type_forms.yaml` is a **mapping** of:

```
<type_name>: <form_definitions>
```

Each `<form_definitions>` is a **mapping** of:

```
<form_name>: <form_data>
```

Each `<form_data>` is a mapping with:

```yaml
weight: <float>        # REQUIRED
notes: <string>        # OPTIONAL
```

---

# 🧬 **3. Field-by-Field Specification**

## **3.1 Top-Level Keys (Type Names)**  
**Type:** string  
**Purpose:** Must match a type defined in `seed_types.yaml`.

**Constraints:**

- must be a valid type name  
- must appear exactly once  
- must map to a dict of forms  

**Example:**

```yaml
Axiom:
  Lattice:
    weight: 1.0
    notes: Ordered, repeating structure
```

---

## **3.2 Form Names (Second-Level Keys)**  
**Type:** string  
**Purpose:** Defines a canonical form/species silhouette for the type.

**Constraints:**

- must be non-empty  
- must be unique within the type  
- must map to a dict  

**Example:**

```yaml
Lattice:
  weight: 1.0
  notes: Ordered, repeating structure
```

---

## **3.3 weight (REQUIRED)**  
**Type:** float  
**Purpose:** Controls weighted selection of forms for a given type.

**Constraints:**

- must be numeric  
- must be > 0  
- used directly by `weighted_choice()`  

**Example:**

```yaml
weight: 0.8
```

---

## **3.4 notes (OPTIONAL)**  
**Type:** string  
**Purpose:** Describes the silhouette, anatomy, or thematic logic of the form.

**Constraints:**

- must be a string if present  
- may be omitted  
- used for:
  - prompt generation  
  - naming flavor  
  - future silhouette logic  

**Example:**

```yaml
notes: Interlocking parts, visible logic, precise motion
```

---

# 🧩 **4. Full Valid Example**

```yaml
Axiom:
  Lattice:
    weight: 1.0
    notes: Ordered, repeating structure; geometry-forward bodies
  Pillar:
    weight: 0.8
    notes: Upright, rigid, load-bearing presence
  Mechanism:
    weight: 0.6
    notes: Interlocking parts, visible logic, precise motion
  Constellation:
    weight: 0.5
    notes: Distributed form; body defined by relation, not mass
```

This is exactly the shape your engine expects.

---

# 🧪 **5. Validation Rules (as enforced by data.py)**

### ✔ Top-level must be a dict  
### ✔ Each type must exist in `seed_types.yaml`  
### ✔ Each form must be a dict  
### ✔ Each form must have a numeric `weight` > 0  
### ✔ `notes` must be a string if present  
### ✔ No empty form names  
### ✔ No malformed structures  

If any rule is violated, `_validate_type_forms()` raises a `ValueError`.

---

# 🧱 **6. Normalized Internal Shape**

`MonsterSeed.forge()` expects forms to be either:

### **Weighted dict (preferred):**

```python
{
  "Lattice": {"weight": 1.0, "notes": "..."},
  "Pillar": {"weight": 0.8, "notes": "..."},
  ...
}
```

### **OR simple list (legacy support):**

```python
["Lattice", "Pillar", "Mechanism"]
```

Your YAML uses the preferred weighted dict shape.

---

# 🚀 **7. How This Schema Is Used in the Engine**

### In `MonsterSeed.forge()`:

- forms are loaded from `SEED_TYPE_DATA[type]["forms"]` if present  
- otherwise from `FORMS_BY_TYPE[type]`  
- if dict → weighted selection  
- if list → random choice  

### In future systems:

- silhouette selection  
- prompt generation  
- naming flavor  
- evolution logic  
- biome adaptation  

This schema ensures all those systems have predictable input.

---

# 🟦 **8. AI Usage Notes**

When generating or modifying forms, an AI agent must:

- never invent new fields  
- always include `weight`  
- always ensure weights are > 0  
- always use strings for notes  
- never add forms to types that don’t exist  
- never remove required types  
- never assume notes have mechanical effects unless documented  

---

