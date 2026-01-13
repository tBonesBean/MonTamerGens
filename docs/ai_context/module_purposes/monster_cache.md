# **monster_cache.md - Module Purpose & Technical Canon**
_Describes the persistence layer for cached MonsterSeed objects._

---

# dY- **1. Purpose of This Module**

`monster_cache.py` is the storage backbone of MonTamerGens. It saves and loads
`MonsterSeed` objects to a JSONL cache and assigns unique IDs for retrieval.

---

# dY- **2. Responsibilities**

`monster_cache.py` is responsible for:

### - Persistence
- Appending seeds to the JSONL cache
- Loading cached seeds by unique ID
- Reconstructing `MonsterSeed` objects from raw data

### - Identity
- Generating unique alphanumeric IDs
- Persisting IDs under `meta.unique_id`

---

# dY- **3. Inputs & Data Dependencies**

This module consumes:

- `MonsterSeed` dataclass instances
- unique ID strings provided by the caller
- file paths defined by `CACHE_FILE` and `OUTPUT_PATH`

---

# dY- **4. Outputs**

It produces:

- JSONL cache entries on disk
- `MonsterSeed` objects when loading by ID
- the generated unique ID for newly saved seeds

---

# dY- **5. Data Flow**

```
MonsterSeed
    ->
save_monster()
    ->
generated_monsters.jsonl
```

```
unique_id
    ->
load_monster()
    ->
MonsterSeed
```

---

# dY- **6. Key Functions**

## **6.1 generate_id()**
Creates a random alphanumeric identifier.

## **6.2 _load_all_from_cache()**
Loads all cached seeds into memory, keyed by unique ID.

## **6.3 save_monster()**
Appends a seed to the JSONL cache and assigns a unique ID if missing.

## **6.4 load_monster()**
Rebuilds a `MonsterSeed` from cached JSON.

---

# dY- **7. Invariants & Guarantees**

- Cache writes are append-only.
- `save_monster()` only accepts dataclass instances.
- Unique IDs are stored under `meta.unique_id`.

---

# dY- **8. Known Pitfalls / Refactor Notes**

- `_load_all_from_cache()` reads the full cache and is not scalable.
- Corrupted JSONL lines are skipped with a warning.
- Cache schema changes can break reconstruction.

---

# dY- **9. Future Expansion Hooks**

- Add indexed storage for fast lookups.
- Add schema versioning and migration tools.
- Support database-backed persistence.

---

# dY- **10. AI Usage Notes**

When an AI agent interacts with this module, it should:

- treat cache writes as append-only operations
- preserve `meta.unique_id` during updates
- avoid loading the full cache in performance-critical paths
