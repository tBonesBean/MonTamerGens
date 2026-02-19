# Type Systems Schema

This document defines the **authoritative schema and invariants** for the MonTamerGens type system. It is intended for use by AI tooling (IntelliHub MCP), validation layers, and future contributors.

This file describes **what is allowed**, **what is forbidden**, and **what must never be inferred implicitly**.

> **Governing authority:** `type_system_architecture.md` defines the canonical architecture from which this schema is derived.

---

## 1. System Overview

The type system is split into **two orthogonal layers**:

1. **Primary Type System** -- Ontological identity
2. **Secondary Type System** -- Interaction posture

These layers must never collapse into one another.

The four-layer identity stack (Primary Cluster, Primary Type, Secondary Cluster, Secondary Type) is collectively referred to as a monster's **BioMatrix**. The BioMatrix defines identity, determines possible forms, influences rarity, and shapes the generation process.

---

## 2. Primary Type System (Ontology Layer)

### 2.1 Primary Clusters

Primary clusters represent **existential categories**. They define *truth*, not behavior.

Allowed values:

```yaml
STRUCTURAL
DYNAMIC
POTENTIAL
RESIDUAL
```

Each Primary Type must belong to exactly **one** Primary Cluster.

---

### 2.2 Primary Types

Primary Types define **what a monster is**.

#### Invariants

- A monster **must have exactly one** Primary Type
- Primary Types **must not change** during combat
- Primary Types **must not be suppressed, overridden, or converted**
- Primary Types define long-term systems (evolution, lore, breeding, wounds)

#### Schema

```yaml
primary_type: <PrimaryTypeName>
```

Where `<PrimaryTypeName>` is a key defined in `primary_types.yaml`.

---

### 2.3 Developmental Evolution Constraints

Development operates on interference patterns, not identity. The following constraints are invariant:

- **Phase Shifts** modify interaction thresholds, conversion rules, harmonic interference patterns, and expression pathways. They must **never** modify Primary identity, Secondary cluster grammar, or ontological classification.
- **Kin Wounds** introduce distortion into the waveform (suppressed amplitudes, altered negotiation outcomes). They alter expression, not identity.
- **Lumen Embracing** realigns harmonics (restores suppressed amplitudes, unlocks alternate behavioral interactions). This is identity affirmation, not stat modification.

Any system that modifies Primary Type or Primary Cluster assignment through developmental mechanics is a **schema violation**.

---

## 3. Secondary Type System (Interaction Layer)

Secondary Types describe **how force is applied, redirected, or resisted**.

They are derivative, mutable, and context-sensitive.

---

### 3.1 Secondary Clusters

Secondary clusters are **interaction postures**, not identities.

Allowed values:

```yaml
IMPETUS
VEIL
HOLDFAST
```

These names are provisional but behaviorally fixed.

---

### 3.2 Secondary Types

Secondary Types:

- may be permanent, temporary, or conditional
- may be altered by combat, environment, Lumen effects, or mutations
- must never redefine Primary identity

#### Schema

```yaml
secondary_cluster: <SecondaryClusterName>
```

Where `<SecondaryClusterName>` is one of the allowed Secondary Clusters.

---

## 4. Interaction Model

Interactions follow a **context --> modifier** pattern.

- Primary Cluster defines the interaction context
- Secondary Cluster defines the modifier applied within that context

### 4.1 Branching Rule

```text
interaction = PrimaryCluster :: SecondaryCluster --> Effect
```

This is referred to as the **1 :: [3] model**.

### 4.2 Combat Resolution

Interactions resolve cross-layer:

```text
Attacker Primary --> Defender Secondary
Defender Primary --> Attacker Secondary
```

Not Primary vs Primary. This preserves ontological integrity.

---

### 4.3 Allowed Interaction Effects

Secondary interactions may:

- modify damage multipliers
- suppress passive tags
- grant temporary state tags

Secondary interactions must **not**:

- change Primary Type
- change Primary Cluster
- create new ontology

---

## 5. Interaction Effect Schema

```yaml
effect:
  incoming_damage_multiplier: <float>
  outgoing_damage_multiplier: <float>
  suppresses:
    - <PassiveTag>
  grants:
    - <StateTag>
```

All fields are optional.

---

## 6. Tag Interaction Rules

Tags referenced by the type system must be explicit and namespaced.

Examples:

```yaml
Passive:Stability
State:Braced
Passive:Afterimage
```

The type system must not create unnamed or implicit tags.

---

## 7. Waveform Model Constraints

Every monster is conceptually a composite waveform:

- Primary Cluster = Macro curvature class
- Primary Type = Centroid emphasis
- Secondary Cluster = Modulation style
- Secondary Type = Fine modulation
- Individual variation = Amplitude noise

Development modifies **phase and interference**, not frequency identity. Any system that redefines a monster's fundamental waveform components (Primary Cluster or Primary Type) is a schema violation.

---

## 8. Forbidden Patterns (Hard Errors)

The following are **schema violations**:

- Multiple Primary Types on one monster
- Elemental naming in Primary Types
- Secondary effects overriding Primary identity
- Implicit type conversions
- Undeclared interaction effects
- Developmental mechanics that alter Primary Type or Primary Cluster
- Tertiary hidden identity layers

Any AI or system encountering these must treat them as errors.

---

## 9. Design Intent (Non-Negotiable)

- Ontology precedes mechanics
- Interaction never redefines existence
- Complexity is layered, not entangled
- Monsters are signal profiles, not archetypes

This schema exists to **protect future systems from early collapse**.

---

*End of schema.*
