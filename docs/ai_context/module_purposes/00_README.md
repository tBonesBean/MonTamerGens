# module_purposes/00_README.md — Module Index & Usage Guide
_Your guide to understanding the responsibilities of every Python module in MonTamerGens._

---

## 🧭 Purpose of This Folder

This directory contains one Markdown file per Python module in the codebase.  
Each file explains:

- what the module does  
- what inputs it expects  
- what outputs it produces  
- how it interacts with other modules  
- what assumptions it makes  
- what future expansions it anticipates  

This folder is the bridge between your code and your design documents.

---

## 📂 Folder Contents

```
module_purposes/
	├── 00_README.md
	├── data_layer.md
	├── monsterseed.md
	├── mon_forge.md
	├── forge_name.md
	├── dex_entries.md
	├── prompt_engine.md
	├── monster_cache.md
	└── reroll.md
```
---

## 📘 How to Use This Folder

Each module file follows a consistent structure:

1. **Purpose** — What the module does  
2. **Inputs** — What it expects  
3. **Outputs** — What it returns or modifies  
4. **Responsibilities** — What it owns  
5. **Integration Points** — What it connects to  
6. **Internal Logic Summary** — How it works  
7. **Future Expansion Hooks** — How it can evolve

This structure ensures every module is documented in a way that’s:

- readable  
- predictable  
- AI‑friendly  
- future‑proof  

---

## 🧠 AI Usage Notes

When I (or any other agent) need to:

- answer a question about the code  
- generate new features  
- debug a pipeline  
- write new modules  
- update schemas  
- refactor logic  

…I check this folder first.

It gives me the **semantic meaning** of the code — not just the syntax.

---