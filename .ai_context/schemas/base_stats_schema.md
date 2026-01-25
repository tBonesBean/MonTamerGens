# **base_stats_schema.md — Canonical Schema for `BASE_STATS`**  
_Describes the required structure, allowed stat names, constraints, and usage rules for the base stat block._

---

# 🧩 **1. Purpose of This Schema**

`BASE_STATS` defines the **default stat block** for all monsters before any type modifiers, secondary type adjustments, mutagens, or narrative effects are applied.

This schema ensures:

- consistent stat names  
- predictable numeric types  
- compatibility with type attributes  
- compatibility with mutagens  
- deterministic stat pipelines  

It is enforced by:

- `calculate_base_stats()` in `monsterseed.py`  
- `_validate_seed_type_data()` in `data.py`  
- mutagen application logic in `mon_forge.py`  

---

# 🧱 **2. High-Level Structure**

`BASE_STATS` must be a **mapping** of:

```
<STAT_NAME>: <integer>
```

Example from your engine:

```python
BASE_STATS = {
    "HP": 100,
    "ATK": 50,
    "DEF": 50,
    "SPATK": 50,
    "SPDEF": 50,
    "SPD": 50,
    "ACC": 95,
    "EVA": 5,
    "LUCK": 10,
}
```

---

# 🧬 **3. Allowed Stat Names**

These stat names are **canonical** and must be used consistently across:

- seed types  
- mutagens  
- synergy tables  
- naming logic  
- prompt generation  
- future evolution systems  

### **Valid Stats:**

| Stat | Meaning |
|------|---------|
| **HP** | Hit Points / Vitality |
| **ATK** | Physical attack power |
| **DEF** | Physical defense |
| **SPATK** | Special attack power |
| **SPDEF** | Special defense |
| **SPD** | Speed / turn order |
| **ACC** | Accuracy |
| **EVA** | Evasion |
| **LUCK** | Critical chance, proc chance, narrative luck |

Any stat outside this list will cause validation errors.

---

# 🧪 **4. Field Constraints**

### ✔ Keys must be strings  
### ✔ Keys must match the allowed stat names  
### ✔ Values must be integers  
### ✔ Values must be ≥ 0  
### ✔ No floats allowed in the base block  
### ✔ No missing stats  
### ✔ No additional stats  

This ensures all monsters begin with a complete, predictable stat set.

---

# 🧱 **5. How the Engine Uses BASE_STATS**

### **5.1 In `calculate_base_stats()`**
- Primary type multipliers apply directly to these values  
- Additive bonuses apply directly  
- Secondary type multipliers apply at 50% strength  
- Secondary additive bonuses apply at 50% strength  

### **5.2 In `apply_mutagens()`**
- Multiplicative mutagens apply on top of the modified base stats  
- Additive mutagens apply afterward  

### **5.3 In naming logic**
- Stat biases influence syllable selection and epithets  

### **5.4 In prompt generation**
- Stat shape influences silhouette and posture descriptors  

### **5.5 In future evolution systems**
- Stat deltas may influence evolution triggers  

---

# 🧩 **6. Normalized Internal Shape**

After loading, the engine treats `BASE_STATS` as:

```python
{
  "HP": int,
  "ATK": int,
  "DEF": int,
  "SPATK": int,
  "SPDEF": int,
  "SPD": int,
  "ACC": int,
  "EVA": int,
  "LUCK": int,
}
```

This shape must never change.

---

# 🚫 **7. Forbidden Changes**

To preserve determinism and compatibility:

- Do **not** remove stats  
- Do **not** rename stats  
- Do **not** add new stats without updating:
  - seed type schema  
  - mutagen schema  
  - stat pipeline  
  - naming logic  
  - prompt engine  
- Do **not** convert values to floats  
- Do **not** use negative values  

---

# 🟦 **8. AI Usage Notes**

When generating or modifying base stats, an AI agent must:

- never invent new stat names  
- never omit required stats  
- always use integers  
- always keep values ≥ 0  
- never assume mechanical meaning beyond what is documented  
- never modify `BASE_STATS` at runtime  

---

