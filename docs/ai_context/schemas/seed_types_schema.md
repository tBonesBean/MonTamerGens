# **seed_types_schema.md — Canonical Schema for `seed_types.yaml`**

_Describes the required structure, allowed fields, constraints, and validation rules for the foundational monster archetypes known as "Seed Types"._

---

# 🌰 **1. Purpose of This Schema**

`seed_types.yaml` defines the core monster archetypes, or "seeds," which serve as the foundational layer of a monster's identity before specific `types` are applied. Each seed represents a primal concept or narrative theme.

This schema ensures that all seed types:

-   Follow a consistent and predictable structure.
-   Have valid stat modifiers and habitat associations.
-   Remain compatible with the `MonsterSeed.forge()` creation process.
-   Provide a stable foundation for emergent monster generation.

Seed Types are the first major data source used in the generation pipeline, loaded by `data.py` and consumed almost immediately by `monsterseed.py`.

---

# 🧱 **2. High-Level Structure**

`seed_types.yaml` must be a **list** of seed type entries.

Each entry must be a **mapping** with the following structure:

```yaml
- name: <string> # REQUIRED
  weight: <float> # OPTIONAL (default: 1.0)
  habitats: <list[string]> # REQUIRED
  attributes: # REQUIRED
      mul: <dict> # OPTIONAL
      add: <dict> # OPTIONAL
	  tags: <list[string]> # OPTIONAL
      notes: <list[string]> # OPTIONAL
```

---

# 🧬 **3. Field-by-Field Specification**

## **3.1 name (REQUIRED)**

**Type:** string
**Purpose:** The canonical, thematic name of the seed type. This is a primary identifier used for logging and debugging the generation process.

**Constraints:**

-   Must be a non-empty string.
-   Must be unique across all entries in `seed_types.yaml`.

**Example:**

```yaml
name: Bastion
```

## **3.2 weight (OPTIONAL)**

**Type:** float
**Default:** `1.0`
**Purpose:** Controls the weighted selection of the seed type during the initial phase of monster generation. Higher weights are more common.

**Constraints:**

-   Must be a numeric value.
-   Must be greater than 0.

**Example:**

```yaml
weight: 1.0
```

## **3.3 habitats (REQUIRED)**

**Type:** list[string]
**Purpose:** A list of habitats where monsters of this seed type are likely to be found. This influences the monster's `habitat` property.

**Constraints:**

-   Must be a list.
-   Each item in the list must be a non-empty string.

**Example:**

```yaml
habitats:
    - Monolithic Structures
    - Ancient Battlefield
```

## **3.4 attributes (REQUIRED)**

**Type:** mapping
**Purpose:** A container for all stat modifications and descriptive notes associated with the seed type.

### **3.4.1 attributes.mul (OPTIONAL)**

**Type:** mapping[string, float]
**Purpose:** Defines **multiplicative** stat modifiers applied to the monster's `BASE_STATS`.

**Constraints:**

-   Keys must be valid stat acronyms (e.g., `HP`, `ATK`, `SPD`).
-   Values must be numeric. A value of `1.10` represents a 10% increase.

**Example:**

```yaml
mul:
    DEF: 1.20
    HP: 1.15
```

### **3.4.2 attributes.add (OPTIONAL)**

**Type:** mapping[string, int]
**Purpose:** Defines **additive** stat modifiers applied to the monster's `BASE_STATS` _after_ multipliers.

**Constraints:**

-   Keys must be valid stat acronyms.
-   Values must be integers.

**Example:**

```yaml
add:
    DEF: 10
```

### **3.4.3 attributes.tags (OPTIONAL)**

**Type:** list[string]
**Purpose:** Identify 'type-specific' strengths, weaknesses, abilities, synergies, etc.

**Constraints:**

-   Must be a list of strings.
-   Special prefixes: (**examples**)
    -   `Resist:X` → adds to `meta.resist`
    -   `Weak:X` → adds to `meta.weak`
    -   `Ability:X` → adds to `meta.abilities`

**Example:**

```yaml
tags:
    - Resist:Apex
    - Weak:Echo
    - Ability:TimeShift
```

### **3.4.4 attributes.notes (REQUIRED)**

**Type:** list[string]
**Purpose:** Provides thematic keywords or flavor text that describe the core concept of the seed. This can be used to influence downstream generation like dex entries or naming.

**Constraints:**

-   Must be a list of strings.

**Example:**

```yaml
notes:
    - Resilient
    - Stalwart
```

---

# 🧩 **4. Full Valid Example**

```yaml
- name: Flow
  weight: 1.0
  habitats:
      - Freshwater Springs
      - Riverlands
  attributes:
      mul:
          SPDEF: 1.12
          SPD: 1.05
      add:
          HP: 10
	  tags:
	  	- Resist:Dread
	  	- Weak:Vessel
		- Ability:HealAlly
      notes:
          - Empathic
          - Adaptive
```

---

# 🧪 **5. Validation Rules**

The following rules are enforced by `data.py` upon loading `seed_types.yaml`:

-   The root object must be a list.
-   Each entry in the list must be a dictionary.
-   Each entry must contain a unique `name` (string) and a `habitats` (list).
-   If `weight` is present, it must be a number greater than 0.
-   `attributes` must be a dictionary if present.
-   `mul` and `add` keys must correspond to known stats.
-   `mul` and `add` values must be numeric.
-   `tags` must be a list of strings if present, and contain values defined within the lore and data_layer.
-   `notes` must be a list of strings that are coherent, sensible, brief descriptors of the type, easily accepted by downstream systems.

Violation of these rules will raise an error during application startup.

---

# 🧱 **6. Normalized Internal Shape**

After being loaded and processed by `data.py`, the collection of seed types is stored in a dictionary where keys are the seed `name`. Each entry has a structure similar to this:

```python
"Flow": {
  "name": "Flow",
  "weight": 1.0,
  "habitats": ["Freshwater Springs", "Riverlands"],
  "attributes": {
    "mul": {"SPDEF": 1.12, "SPD": 1.05},
    "add": {"HP": 10},
	"tags": ["Resist:Dread", "Weak:Vessel", "Ability:HealAlly"],
    "notes": ["Empathic", "Adaptive"]
  }
}
```

This normalized dictionary is what `monsterseed.py` uses for generation.

---

# 🚀 **7. How Seed Types Are Used in the Engine**

1.  **Selection:** In `MonsterSeed.forge()`, a primary seed type is chosen using a weighted random selection from all loaded seeds.
2.  **Stat Foundation:** The `mul` and `add` attributes from the chosen seed are the **first** modifiers applied to the monster's `BASE_STATS`. This establishes the creature's core statistical leaning. `tags` provide diversity to be applied later.
3.  **Habitat Assignment:** One of the seed's `habitats` is randomly chosen and assigned to the monster.
4.  **Flavor and Downstream Influence:** The `name` and `notes` are stored in the `MonsterSeed` object and can be used later by the naming (`forge_name.py`), dex entry (`dex_entries.py`), and visual prompt (`prompt_engine.py`) generators.

---

# 🟦 **8. AI Usage Notes**

When you are asked to generate or modify entries in `seed_types.yaml`:

-   **Do not invent new top-level fields.** The allowed fields are `name`, `weight`, `habitats`, and `attributes`.
-   Ensure `name` is a unique, descriptive, single-word concept.
-   Stat modifications in `mul` and `add` should be subtle. Large changes are typically handled by `type_data.yaml` or mutagens.
-   The `tags` should be appropriately formatted `PREFIX:VALUE` strings that maintain coherence when processed by downstream systems.
-   The `notes` should be high-level thematic keywords, not detailed sentences. Intended to guide narrative, as well as AI image generation.
-   The habitats should align with the theme of the seed.
