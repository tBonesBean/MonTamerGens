# Appendix D — Project File Tree (Focused)

This appendix provides a focused file tree for the **MonTamerGens** project root, including the requested subdirectories and their contents.

```plaintext
MONTAMERGENS/
├── AGENTS.md
├── DETAILED_ANALYSIS.md
├── LICENSE.txt
├── README.md
├── CLI_USAGE.md
├── pyproject.toml
├── requirements.txt
├── .ai_context/
│   ├── 00_README.md
│   ├── architecture_overview.md
│   ├── design_bible.md
│   ├── lore_core.md
│   ├── naming_conventions.md
│   ├── type_glossary.md
│   ├── type_systems_overview.md
│   ├── appendices/
│   │   ├── A_appendix.md
│   │   ├── B_appendix.md
│   │   ├── C_appendix.md
│   │   └── D_appendix.md
│   ├── module_purposes/
│   │   ├── 01_README.md
│   │   ├── cli.md
│   │   ├── data_layer.md
│   │   ├── dex_entries.md
│   │   ├── forge_name.md
│   │   ├── gen_visuals.md
│   │   ├── mon_forge.md
│   │   ├── monster_cache.md
│   │   ├── monsterseed.md
│   │   ├── prompt_engine.md
│   │   └── reroll.md
│   └── schemas/
│       ├── 02_README.md
│       ├── base_stats_schema.md
│       ├── mutagen_schema.md
│       ├── seed_types_schema.md
│       ├── trait_schema.md
│       ├── type_form_schema.md
│       └── type_systems_schema.md
├── src/
│   └── mongens/
│       ├── __init__.py
│       ├── cli.py
│       ├── dex_entries.py
│       ├── forge_name.py
│       ├── gen_visuals.py
│       ├── mon_forge.py
│       ├── monster_cache.py
│       ├── monsterseed.py
│       ├── prompt_engine.py
│       ├── reroll.py
│       ├── assets/
│       │   ├── generated_monsters.jsonl
│       │   ├── generated_monsters.txt
│       │   ├── generated_monsters.txt.seed.json
│       │   └── mongen_dexentry.txt
│       └── data/
│           ├── __init__.py
│           ├── art_data.py
│           ├── data.py
│           ├── held_items.yaml
│           ├── json_importer.gd
│           ├── kin_wounds.yaml
│           ├── monster_resource.gd
│           ├── physical_traits.yaml
│           ├── type_forms.yaml
│           ├── mutagens/
│           │   ├── major_mods.yaml
│           │   └── utility_mods.yaml
│           ├── naming/
│           │   └── type_parts.yaml
│           └── types/
│               ├── #deprecated_unused.yaml
│               ├── cluster_interactions.yaml
│               ├── interaction_model.yaml
│               ├── primary_clusters.yaml
│               ├── primary_types.yaml
│               ├── secondary_clusters.yaml
│               ├── secondary_types.yaml
│               ├── seed_types.yaml
│               ├── type_affinities.yaml
│               └── type_clusters.yaml
├── tests/
│   ├── check_mon_forge.py
│   ├── exhaustive_forge.py
│   ├── inspect_mods.py
│   ├── smoke_forge.py
│   ├── test_forge_name.py
│   ├── test_formatting.py
│   ├── test_generators.py
│   ├── test_mutagens.py
│   ├── test_regression_visuals.py
│   └── test_weighting.py
├── output/
│   ├── last_validation.txt
│   ├── watch_yaml_stderr.log
│   └── watch_yaml_stdout.log
└── tools/
    ├── validate_yaml.py
    └── watch_yaml.py
```

---

For the full IntelliHub file tree, see [Appendix B — IntelliHub File Tree](B_appendix.md).
