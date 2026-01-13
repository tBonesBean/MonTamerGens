# **mutagen_schema.md — Canonical Schema for Major & Utility Mutagens**

_Describes the required structure, allowed fields, constraints, and validation rules for `MAJOR_MODS` and `UTILITY_MODS`, and their respective `major_mods.yaml` and `utility_mods.yaml` files._

---

# 🧬 **1. Purpose of This Schema**

Mutagens are high‑impact modifiers that shape a monster’s mechanical identity.  
This schema defines the **canonical shape** of both:

-   **Major Mutagens** (`MAJOR_MODS`)
-   **Utility Mutagens** (`UTILITY_MODS`)

It ensures:

-   consistent structure
-   valid stat modifiers
-   predictable tag behavior
-   correct type gating
-   safe synergy logic
-   compatibility with the mutagen forge

This schema is enforced by:

-   `apply_mutagens()` in `mon_forge.py`
-   mutagen filtering logic
-   synergy multiplier logic
-   stat application logic

---

# 🧱 **2. High-Level Structure**

Both `MAJOR_MODS` and `UTILITY_MODS` are **dicts** of:

```
<mod_name>: <mod_definition>
```

Each `<mod_definition>` is a mapping with the following possible fields:

```yaml
mul: # OPTIONAL
    <STAT>: <float>

add: # OPTIONAL
    <STAT>: <number>

tags: # OPTIONAL
    - <string>

allowed_types: # OPTIONAL
    - <string>

incompatible_types: # OPTIONAL
    - <string>

rarity: <float> # OPTIONAL (default: 1.0)

synergy_bonus: # OPTIONAL
    <TYPE_NAME>: <float>

# Utility-only fields (OPTIONAL)
identify_rates: <float>
quest_bonus: <float>
exp_mult: <float>
loot_mult: <float>
ally_buff: <mapping>
enemy_opening_debuff: <mapping>
double_rolls: <list>
unlock_tags: <list>
field_heal_ticks: <float>
ally_heal_ticks: <float>
```

Mutagens are intentionally flexible, but the **core fields** must follow strict rules.

---

# 🧩 **3. Core Fields (Shared by Major & Utility Mutagens)**

## **3.1 mul (OPTIONAL)**

**Type:** mapping of `<STAT>: <float>`  
**Purpose:** multiplicative stat adjustments.

**Constraints:**

-   keys must be valid stats from `BASE_STATS`
-   values must be numeric
-   values must be > 0

**Example:**

```yaml
mul:
    ATK: 1.15
    SPD: 1.10
```

---

## **3.2 add (OPTIONAL)**

**Type:** mapping of `<STAT>: <number>`  
**Purpose:** additive stat adjustments.

**Constraints:**

-   keys must be valid stats
-   values must be numeric

**Example:**

```yaml
add:
    HP: 10
    EVA: 5
```

---

## **3.3 tags (OPTIONAL)**

**Type:** list of strings  
**Purpose:** thematic or mechanical tags.

**Constraints:**

-   list may be empty
-   entries must be strings
-   special prefixes:
    -   `Resist:X` → adds to `meta.resist`
    -   `Weak:X` → adds to `meta.weak`
    -   everything else → `meta.tags`

**Example:**

```yaml
tags:
    - Resist:Astral
    - Weak:Tempest
    - VolcanicGlass
```

---

## **3.4 allowed_types (OPTIONAL)**

**Type:** list of strings  
**Purpose:** type gating for mutagen eligibility.

**Constraints:**

-   empty list means “allowed for all types”
-   if non-empty, monster must have at least one matching type

**Example:**

```yaml
allowed_types:
    - Axiom
    - Geist
```

---

## **3.5 incompatible_types (OPTIONAL)**

**Type:** list of strings  
**Purpose:** hard exclusion for certain types.

**Constraints:**

-   if monster has ANY listed type → mutagen is rejected

**Example:**

```yaml
incompatible_types:
    - Bloom
    - Flow
```

---

## **3.6 rarity (OPTIONAL)**

**Type:** float  
**Default:** `1.0`  
**Purpose:** controls weighted sampling.

**Constraints:**

-   must be numeric
-   must be > 0
-   weight = `1 / rarity^alpha`

**Example:**

```yaml
rarity: 1.3
```

---

## **3.7 synergy_bonus (OPTIONAL)**

**Type:** mapping of `<TYPE_NAME>: <float>`  
**Purpose:** multiplicative weight bonus when monster has matching type.

**Constraints:**

-   values must be numeric
-   values must be > 0
-   final synergy multiplier is clamped by `MAX_SYNERGY_MULT`

**Example:**

```yaml
synergy_bonus:
    Idol: 1.5
    Geist: 1.2
```

---

# 🧬 **4. Utility-Only Fields**

Utility mutagens may include additional fields that do **not** affect stats directly.

These fields are optional and may include:

-   `identify_rates`
-   `quest_bonus`
-   `exp_mult`
-   `loot_mult`
-   `ally_buff`
-   `enemy_opening_debuff`
-   `double_rolls`
-   `unlock_tags`
-   `field_heal_ticks`
-   `ally_heal_ticks`
-   `shop_discount`
-   `crafting_bonus`
-   `map_reveal_radius`
-   etc.

**Constraints:**

-   must be JSON‑serializable
-   must not conflict with core fields
-   must not require special logic unless implemented in future systems

---

# 🧪 **5. Validation Rules (as enforced by mon_forge.py)**

### ✔ Allowed types must match monster types

### ✔ Incompatible types must not overlap

### ✔ Rarity must be numeric

### ✔ Synergy bonuses must be numeric

### ✔ Stat keys must be valid

### ✔ Tags must be strings

### ✔ No negative multipliers

### ✔ No zero multipliers

### ✔ No malformed fields

If any rule is violated, the mutagen is silently skipped.

---

# 🧱 **6. Normalized Internal Shape**

After loading, each mutagen is treated as:

```python
{
  "mul": {...},
  "add": {...},
  "tags": [...],
  "allowed_types": [...],
  "incompatible_types": [...],
  "rarity": <float>,
  "synergy_bonus": {...},
  # utility-only fields...
}
```

This is the shape consumed by:

-   mutagen filtering
-   synergy calculation
-   stat application
-   meta enrichment

---

# 🚀 **7. Full Valid Example (Major Mutagen)**

```yaml
Starwarden:
    mul:
        SPDEF: 1.28
        LUCK: 1.20
        HP: 1.10
    add: {}
    allowed_types:
        - Axiom
        - Geist
        - Echo
    rarity: 1.3
    synergy_bonus:
        Mythic: 1.4
    tags: []
```

---

# 🌟 **8. Full Valid Example (Utility Mutagen)**

```yaml
Symbiote:
    field_heal_ticks: 0.08
    ally_heal_ticks: 0.04
    tags:
        - HealingAura
        - Lifebond
    rarity: 1
    allowed_types:
        - Bloom
        - Flow
```

---

# 🟦 **9. AI Usage Notes**

When generating or modifying mutagens, an AI agent must:

-   never invent new core fields
-   always validate stat names
-   always ensure multipliers are > 0
-   always ensure rarity is numeric
-   always ensure synergy bonuses are numeric
-   never assume tags have mechanical effects unless documented
-   never add fields requiring new logic unless requested

---
