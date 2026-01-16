# MonTamerGens CLI Guide

This guide documents the current command-line interface for MonTamerGens. It covers
all commands, arguments, default output locations, and examples. The CLI entrypoint
is the `mongen` command (from `src/mongens/cli.py`).

---

## Quick Start

Generate a canonical dex entry (writes a text entry to the default assets file):

```
mongen dexentry -c 1
```

Generate a unique monster (prints seed data to console):

```
mongen unique
```

Generate an art prompt and save it to the default assets file:

```
mongen artprompt
```

---

## Output Paths (Defaults)

The CLI writes into the assets folder for this project:

-   JSONL cache (all saved seeds):
    -   `src/mongens/assets/generated_monsters.jsonl`
-   Dex text output (default for `dexentry`):
    -   `src/mongens/assets/generated_monsters.txt`
-   Art prompt output (default for `artprompt`):
    -   `src/mongens/assets/art_prompts.txt`

When `--json` is used alongside a text output file, the CLI also writes a sidecar
JSON file named `<output>.seed.json` in the same directory.

Example:

-   `--output src/mongens/assets/my_dex.txt` produces:
    -   `src/mongens/assets/my_dex.txt`
    -   `src/mongens/assets/my_dex.txt.seed.json`

---

## Command: `dexentry`

Generate canonical Pokedex-style entries for a species.

**Usage**

```
mongen dexentry [options]
```

**Arguments**

-   `-t1`, `--primary_type` (string): Primary type. Defaults to `random`.
-   `-t2`, `--secondary_type` (string): Secondary type. Defaults to `random`.
    -   Use `none` to force no secondary type.
-   `-maj`, `--majors` (int): Number of major mutagens to apply. Default: `1`.
-   `-ut`, `--utils` (int): Number of utility mutagens to apply. Default: `1`.
-   `-c`, `--count` (int): Number of entries to generate. Default: `1`.
-   `-o`, `--output` (string): Output file for dex text.
    -   Default: `src/mongens/assets/generated_monsters.txt`
-   `--json` (flag): Save the generated seeds to JSONL cache and write a sidecar
    `<output>.seed.json` file.

**Examples**
Generate 5 dex entries with a forced primary type:

```
mongen dexentry -t1 Axiom -c 5
```

Generate 10 entries with no secondary type and save JSON:

```
mongen dexentry -t1 Echo -t2 none -c 10 --json
```

Write dex entries to a custom file:

```
mongen dexentry -c 3 -o src/mongens/assets/custom_dex.txt
```

---

## Command: `unique`

Generate a unique monster instance (wild-style) and print its seed data.

**Usage**

```
mongen unique [options]
```

**Arguments**

-   `-t1`, `--primary_type` (string): Primary type. Defaults to `random`.
-   `-t2`, `--secondary_type` (string): Secondary type. Defaults to `random`.
    -   Use `none` to force no secondary type.
-   `--majors` (int): Number of major mutagens. Default: `1`.
-   `--utils` (int): Number of utility mutagens. Default: `1`.
-   `--json` (flag): Save the generated seed to JSONL cache.

**Examples**
Generate a random unique monster:

```
mongen unique
```

Generate a Spur/Flow monster and save to cache:

```
mongen unique -t1 Spur -t2 Flow --json
```

---

## Command: `alternatives`

Generate alternative names for a monster seed.

**Usage**

```
mongen alternatives [options]
```

**Arguments**

-   `--pin` (string): Load an existing monster by PIN and generate alternatives.
-   `-t1`, `--primary_type` (string): Primary type (if `--pin` not provided).
-   `-t2`, `--secondary_type` (string): Secondary type (if `--pin` not provided).
-   `--majors` (int): Number of major mutagens (if `--pin` not provided).
-   `--utils` (int): Number of utility mutagens (if `--pin` not provided).
-   `-c`, `--count` (int): Number of alternative names. Default: `10`.
-   `--json` (flag): Save the base seed to JSONL cache.

**Examples**
Generate alternatives from a cached monster:

```
mongen alternatives --pin ABC123XYZ9 -c 8
```

Generate alternatives from a random seed and save:

```
mongen alternatives -t1 Rift --json
```

---

## Command: `artprompt`

Generate a formatted art prompt for a monster.

**Usage**

```
mongen artprompt [options]
```

**Arguments**

-   `--pin` (string): Load an existing monster by PIN.
-   `-t1`, `--primary_type` (string): Primary type (if `--pin` not provided).
-   `-t2`, `--secondary_type` (string): Secondary type (if `--pin` not provided).
-   `-maj`, `--majors` (int): Number of major mutagens. Default: `1`.
-   `-ut`, `--utils` (int): Number of utility mutagens. Default: `1`.
-   `-o`, `--output` (string): Output file for prompts.
    -   Default: `src/mongens/assets/art_prompts.txt`
-   `--json` (flag): Save the generated seed to JSONL cache and write a sidecar
    `<output>.seed.json` file.

**Examples**
Generate a prompt from a cached monster:

```
mongen artprompt --pin ABC123XYZ9
```

Generate a Flow/Idol prompt and save output:

```
mongen artprompt -t1 Flow -t2 Idol -o src/mongens/assets/flow_idol_prompts.txt
```

---

## Command: `list`

List available data (types, habitats, mutagens).

**Usage**

```
mongen list [--types] [--habitats] [--mutagens]
```

**Examples**
List all types:

```
mongen list --types
```

List all habitats:

```
mongen list --habitats
```

List all mutagens:

```
mongen list --mutagens
```

---

## Command: `lumenkin`

Generate a Lumen-Kin starter candidate based on resonance inputs.

**Usage**

```
mongen lumenkin [options]
```

**Arguments**

-   `--courage` (int): Resonance value (0–10). Default: `5`.
-   `--empathy` (int): Resonance value (0–10). Default: `5`.
-   `--instinct` (int): Resonance value (0–10). Default: `5`.
-   `--memory` (int): Resonance value (0–10). Default: `5`.
-   `--curiosity` (int): Resonance value (0–10). Default: `5`.
-   `--archetype` (string): One of:
    -   Strength Mirror
    -   Flaw Mirror
    -   Deep Memory
    -   Hidden Desire
    -   Potential Form
-   `--json` (flag): Save the generated seed to JSONL cache.

**Examples**
Generate a Lumen‑Kin with tuned resonance and save it:

```
mongen lumenkin --courage 8 --empathy 7 --archetype "Hidden Desire" --json
```

---

## Command: `reroll`

Re-roll attributes of an existing cached monster and save as a new entry.

**Usage**

```
mongen reroll <pin> [--traits] [--majors]
```

**Arguments**

-   `pin` (string): The 10-character unique ID to re-roll.
-   `--traits` (flag): Re-roll physical traits.
-   `--majors` (flag): Re-roll major mutagen.

**Examples**
Re-roll physical traits:

```
mongen reroll ABC123XYZ9 --traits
```

Re-roll the major mutagen:

```
mongen reroll ABC123XYZ9 --majors
```

---

## Notes on Determinism

-   Seeds are deterministic when generation inputs are fixed.
-   Mutagen selection respects type gating, rarity, and compatibility rules.
-   Cache writes are append‑only in `generated_monsters.jsonl`.

---

## Troubleshooting

-   If a command fails with a type error, run `mongen list --types` to verify names.
-   If cache reads fail, ensure the PIN is correct and exists in `generated_monsters.jsonl`.
-   If outputs are missing, confirm that the assets directory exists:
    -   `src/mongens/assets/`
