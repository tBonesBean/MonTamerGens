# Type System Overview

This document captures the **current mental model and architectural direction** of the MonTamerGens type system as of this checkpoint. It is not a final specification, but a *coherent snapshot* of intent, ontology, and system boundaries.

---

## 1. Design Philosophy (High-Level)

The type system is intentionally split into **layers with different responsibilities**:

- **Primary Types** describe *what a monster is* at an ontological level.
- **Primary Clusters** group those truths into existential categories.
- **Secondary Types (Clusters)** describe *how force interacts* with those truths.

This separation exists to:
- avoid elemental reductionism
- preserve lore depth
- enable future systems (breeding, wounds, Lumen, evolution)
- prevent early design decisions from collapsing future mechanics

A monster may only ever have **one Primary Type**.
Secondary Types are **derivative, expressive, and mutable**.

---

## 2. Primary Cluster Layer (Ontology)

Primary clusters answer **fundamental questions about existence**. They are not combat roles and are not designed around counter tables.

### The Four Primary Clusters

#### 🧱 STRUCTURAL — *Where things sit*
- Bounds, limits, load, inevitability
- Concerned with position, law, and collapse

Representative Primary Types:
- Axiom
- Nadir
- Zenith

---

#### ⚙️ DYNAMIC — *How things move*
- Motion, disruption, pressure, instability
- Concerned with change, momentum, rupture

Representative Primary Types:
- Spur
- Flux
- Surge

---

#### 🌱 POTENTIAL — *What could be*
- Capacity, recursion, foresight
- Concerned with unrealized states and pattern emergence

Representative Primary Types:
- Fractal
- Vessel
- Oracle

---

#### 🕯 RESIDUAL — *What remains*
- Persistence, decay, memory, aftermath
- Concerned with time, residue, and consequence

Representative Primary Types:
- Echo
- Relic
- Mire

---

## 3. Primary Types (Rules)

- A monster may only ever have **one Primary Type**.
- Primary Types do **not change** during combat.
- Primary Types define narrative truth, evolution constraints, and long-term identity.
- Primary Clusters do **not** participate in simple rock–paper–scissors logic.

Primary interactions are *contextual*, not oppositional.

---

## 4. Secondary Cluster Layer (Interaction)

Secondary clusters exist to model **force, resistance, and interference** without redefining identity.

They are intentionally:
- more physical
- more mechanical
- more mutable
- more suitable for combat math

### Current Working Triad (Provisional)

#### 🟥 IMPETUS
- Applied force
- Forward pressure
- Momentum that continues because it has begun

Used for:
- damage amplification
- initiative pressure
- combo inheritance

---

#### 🟦 VEIL
- Interference without destruction
- Obscuring, refracting, redirecting

Used for:
- passive suppression
- redirection
- information distortion

---

#### 🟩 HOLDFAST
- Local resistance
- Inertial presence
- Refusal through persistence

Used for:
- damage mitigation
- integrity preservation
- defensive states

---

## 5. Interaction Model (1 :: [3])

Combat interactions follow a **context → modifier** model:

- **Primary Cluster** defines the interaction context.
- **Secondary Cluster** defines how force behaves within that context.

### Conceptual Example

```yaml
interaction:
  primary_cluster: STRUCTURAL
  secondary_cluster:
    IMPETUS:
      incoming_damage_multiplier: 1.25
    VEIL:
      suppresses:
        - Passive:Stability
    HOLDFAST:
      incoming_damage_multiplier: 0.9
```

Key rules:
- Secondary effects may modify damage, suppress passives, or grant states
- Secondary effects may **never** override Primary identity

---

## 6. Guardrails (Critical Invariants)

- Primary Types define *truth*, not tactics
- Secondary Types define *interaction*, not essence
- No monster ever has two Primary Types
- Secondary clusters must never collapse back into elemental identity

---

## 7. Design Status

- Primary ontology is stabilizing
- Secondary interaction layer is intentionally provisional
- Naming is allowed to remain fluid until it becomes quiet

This system is considered **future-safe but intentionally unfinished**.

Next steps may include:
- YAML formalization
- interaction simulations
- secondary subtypes
- Lumen integration
- wound and resolution systems

---

*Checkpoint reached.*

