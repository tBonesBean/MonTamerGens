# Type Systems Schema

This document defines the **authoritative schema and invariants** for the MonTamerGens type system. It is intended for use by AI tooling (IntelliHub MCP), validation layers, and future contributors.

This file describes **what is allowed**, **what is forbidden**, and **what must never be inferred implicitly**.

---

## 1. System Overview

The type system is split into **two orthogonal layers**:

1. **Primary Type System** — Ontological identity
2. **Secondary Type System** — Interaction posture

These layers must never collapse into one another.

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

Interactions follow a **context → modifier** pattern.

- Primary Cluster defines the interaction context
- Secondary Cluster defines the modifier applied within that context

### 4.1 Branching Rule

```text
interaction = PrimaryCluster :: SecondaryCluster → Effect
```

This is referred to as the **1 :: [3] model**.

---

### 4.2 Allowed Interaction Effects

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

## 7. Forbidden Patterns (Hard Errors)

The following are **schema violations**:

- Multiple Primary Types on one monster
- Elemental naming in Primary Types
- Secondary effects overriding Primary identity
- Implicit type conversions
- Undeclared interaction effects

Any AI or system encountering these must treat them as errors.

---

## 8. Design Intent (Non-Negotiable)

- Ontology precedes mechanics
- Interaction never redefines existence
- Complexity is layered, not entangled

This schema exists to **protect future systems from early collapse**.

---

*End of schema.*

