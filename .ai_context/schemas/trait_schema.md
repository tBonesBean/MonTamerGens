# **trait_schema.md — Canonical Schema for `physical_traits.yaml`**  
_Describes the required structure, allowed fields, constraints, and validation rules for physical trait definitions._

---

# 🌿 **1. Purpose of This Schema**

Physical traits are small, flavorful descriptors that influence:

- silhouette  
- visual prompt generation  
- naming flavor  
- dex entry flavor  
- emergent identity  

This schema ensures that all traits:

- follow a consistent structure  
- have valid weights  
- have clear descriptive notes  
- remain compatible with `MonsterSeed.forge()`  
- remain predictable for future systems (e.g., silhouette logic)  

Traits are loaded and used by:

- `MonsterSeed.forge()`  
- `weighted_choice()`  
- prompt generation  
- naming logic  

---

# 🧱 **2. High-Level Structure**

`physical_traits.yaml` must be a **list** of trait entries.

Each entry must be a **mapping** with the following structure:

```yaml
- name: <string>          # REQUIRED
  weight: <float>         # OPTIONAL (default: 1.0)
  notes: <string>         # OPTIONAL
```

This is the same pattern as seed types and forms, but simpler.

---

# 🧬 **3. Field-by-Field Specification**

## **3.1 name (REQUIRED)**  
**Type:** string  
**Purpose:** The canonical identifier for the trait.

**Constraints:**

- must be non-empty  
- must be unique across all traits  
- must be a string  
- used directly in:
  - `MonsterSeed.physical_traits`
  - prompt generation
  - dex entries  

**Example:**

```yaml
name: Translucent Skin
```

---

## **3.2 weight (OPTIONAL)**  
**Type:** float  
**Default:** `1.0`  
**Purpose:** Controls weighted selection of traits.

**Constraints:**

- must be numeric  
- must be > 0  
- used by `weighted_choice()`  

**Example:**

```yaml
weight: 0.8
```

---

## **3.3 notes (OPTIONAL)**  
**Type:** string  
**Purpose:** Describes the visual or thematic meaning of the trait.

**Constraints:**

- must be a string if present  
- may be omitted  
- used for:
  - prompt generation  
  - future silhouette logic  
  - flavor text  

**Example:**

```yaml
notes: Skin appears semi-transparent, revealing faint Lumen glow.
```

---

# 🧩 **4. Full Valid Example**

```yaml
- name: Translucent Skin
  weight: 1.0
  notes: Skin appears semi-transparent, often glowing faintly.

- name: Feathered Cloak
  weight: 0.8
  notes: A mantle of feathers that shifts with emotional state.

- name: Moss-Covered Shoulders
  weight: 0.6
  notes: Indicates long periods spent in damp, shaded habitats.
```

This is exactly the shape your engine expects.

---

# 🧪 **5. Validation Rules (as enforced by data.py)**

While `data.py` doesn’t currently validate traits explicitly, the following rules are implied by:

- `weighted_choice()`  
- `MonsterSeed.forge()`  
- YAML loading logic  

### ✔ Trait list must be a list  
### ✔ Each entry must be a dict  
### ✔ Each entry must contain `"name"`  
### ✔ `"weight"` must be numeric if present  
### ✔ `"notes"` must be a string if present  
### ✔ No empty names  
### ✔ No negative or zero weights  

If any rule is violated, trait selection may fail or behave unpredictably.

---

# 🧱 **6. Normalized Internal Shape**

After loading, each trait is treated as:

```python
{
  "name": <string>,
  "weight": <float>,
  "notes": <string or None>
}
```

This shape is consumed by:

- `weighted_choice()`  
- `MonsterSeed.forge()`  
- prompt generation  

---

# 🚀 **7. How Traits Are Used in the Engine**

### **7.1 In MonsterSeed.forge()**
- 75% chance of 1 trait  
- 25% chance of 2 traits  
- selected via weighted choice  

### **7.2 In prompt generation**
Traits influence:

- silhouette  
- texture  
- aura  
- posture  
- environmental cues  

### **7.3 In naming**
Traits may bias:

- epithets  
- syllable selection  
- flavor suffixes  

### **7.4 In dex entries**
Traits appear as “Appearance” descriptors.

---

# 🟦 **8. AI Usage Notes**

When generating or modifying traits, an AI agent must:

- never invent new fields  
- always include `"name"`  
- ensure `"weight"` is numeric and > 0  
- ensure `"notes"` is a string if present  
- never assume traits have mechanical effects unless documented  
- never add traits that conflict with silhouette logic  

---

