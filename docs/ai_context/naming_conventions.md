# **naming_conventions.md — MonTamerGens Naming Standards**

### _Consistent naming rules for files, modules, classes, functions, YAML keys, and generated assets._

---

# 🧭 **Purpose**

These conventions ensure:

- clarity across the codebase  
- predictable file discovery  
- consistent AI agent behavior  
- reduced ambiguity in prompts  
- easier onboarding for future contributors  
- stable naming for deterministic systems  

This document defines how **files**, **modules**, **classes**, **functions**, **YAML keys**, and **generated assets** should be named throughout the project.

---

# 📁 **1. File & Directory Naming**

### **1.1 Python Files**
- Always **snake_case**  
- Name reflects the module’s responsibility  
- Avoid abbreviations unless universally understood  

**Examples:**
- `monsterseed.py`
- `mon_forge.py`
- `forge_name.py`
- `prompt_engine.py`
- `monster_cache.py`

### **1.2 YAML Files**
- Always **snake_case**  
- Name reflects the content category  
- Plural when representing lists or collections  

**Examples:**
- `seed_types.yaml`
- `type_forms.yaml`
- `physical_traits.yaml`
- `held_items.yaml`
- `kin_wounds.yaml`

### **1.3 Documentation Files**
- Always **PascalCase** or **TitleCase**  
- Words separated by no spaces or underscores  
- Ends with `.md`  

**Examples:**
- `ProjectManifesto.md`
- `LogicArchitecture.md`
- `PixelArtStyleGuide.md`
- `LumenStoryNotes.md`

### **1.4 IntelliHub Files**
- Always **snake_case**  
- Prefixed with numbers only for ordering  

**Examples:**
- `00_README.md`
- `design_bible.md`
- `architecture_overview.md`
- `lore_core.md`
- `naming_conventions.md`

---

# 🧱 **2. Module Naming Rules**

### **2.1 Single Responsibility**
A module name should describe *exactly one* responsibility.

**Good:**
- `forge_name.py`  
- `mon_forge.py`  
- `prompt_engine.py`  

**Avoid:**
- `utils.py`  
- `helpers.py`  
- `misc.py`  

### **2.2 Verb-Noun Pattern for Action Modules**
Modules that “do something” follow:

```
<action>_<object>.py
```

**Examples:**
- `forge_name.py`
- `generate_visuals.py` (if renamed from `gen_visuals.py`)
- `apply_mutagens.py` (if split from `mon_forge.py`)

---

# 🧬 **3. Class Naming**

### **3.1 PascalCase**
Classes always use **PascalCase**.

**Examples:**
- `MonsterSeed`
- `Mutagen`
- `DexEntry`
- `PromptBuilder`

### **3.2 No Abbreviations**
Avoid shortened forms unless they’re domain‑specific and documented.

---

# 🔧 **4. Function & Method Naming**

### **4.1 snake_case**
Functions and methods always use **snake_case**.

**Examples:**
- `choose_type_pair()`
- `calculate_base_stats()`
- `apply_mutagens()`
- `forge_monster_name()`

### **4.2 Verb-first**
Functions should start with a verb describing the action.

**Examples:**
- `load_yaml_data()`
- `apply_stat_modifiers()`
- `select_species()`

---

# 🗃️ **5. YAML Key Naming**

### **5.1 snake_case for keys**
All YAML keys use **snake_case**.

**Examples:**
```yaml
habitats:
attributes:
    mul:
    add:
tags:
allowed_types:
synergy_bonus:
```

### **5.2 Singular keys for objects, plural for lists**
**Examples:**
```yaml
species: <string>
species_list: <list>
habitats: <list>
attributes: <dict>
```

---

# 🧪 **6. Test Naming**

### **6.1 Test Files**
```
test_<module>.py
```

**Examples:**
- `test_mutagens.py`
- `test_generators.py`
- `test_weighting.py`

### **6.2 Test Functions**
```
test_<behavior>_<expected>()
```

**Examples:**
- `test_type_selection_is_deterministic()`
- `test_mutagen_synergy_applies_correctly()`

---

# 🧾 **7. Generated Asset Naming**

### **7.1 JSONL Cache**
- Append-only  
- snake_case  
- includes domain  

**Examples:**
- `generated_monsters.jsonl`
- `generated_monsters.txt`

### **7.2 Dex Entries**
- snake_case  
- descriptive  

**Examples:**
- `mongen_dexentry.txt`

---

# 🎨 **8. Naming Rules for Monsters (In-World)**

These rules guide the naming pipeline:

### **8.1 Deterministic**
Names must be reproducible from:

- types 
- forms  
- mutagens  
- traits  
- stats  

### **8.2 Syllable Pools**
Each type has:

- prefixes  
- infixes  
- suffixes  

### **8.3 Epithet Rules**
Epithets follow:

```
<Name> the <Descriptor>
```

Descriptors come from:

- traits  
- mutagens  
- stat biases  

### **8.4 No More Than 3 Syllables**
Unless the creature is legendary or aberrant.

---

# 🧩 **9. When to Update This File**

Update when:

- adding new modules  
- introducing new YAML categories  
- changing naming logic  
- restructuring directories  
- adding new asset types  

---

# 🎉 **Summary**

This file ensures that:

- your repo stays clean  
- AI agents stay aligned  
- naming stays predictable  
- future contributors understand the system  
- the IntelliHub remains coherent  

---

