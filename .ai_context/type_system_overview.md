# Type System Overview

This document captures the **current mental model and architectural direction** of the MonTamerGens type system. It is not a final specification, but a _coherent snapshot_ of intent, ontology, and system boundaries.

> **Governing authority:** `type_system_architecture.md` defines the canonical architecture. This overview is derived from it.

---

## 1. Design Philosophy (High-Level)

The type system is intentionally split into **layers with different responsibilities**:

- **Primary** = Existential Identity (what a monster _is_)
- **Secondary** = Behavioral Negotiation (how that identity interacts with change)
- **Stats** = Potential energy landscape (capacity, not destiny)

This separation is the central innovation of the system. It exists to:

- avoid elemental reductionism
- preserve lore depth
- enable future systems (breeding, wounds, Lumen, evolution)
- prevent early design decisions from collapsing future mechanics

A monster may only ever have **one Primary Type**.
Secondary Types are **derivative, expressive, and mutable**.

### The BioMatrix (Identity Stack)

Every monster is generated with four type properties that collectively form its **BioMatrix** -- its layered identity. The BioMatrix defines identity, determines possible forms (silhouettes), influences rarity, and shapes the generation process.

The four layers, in order:

1. **Primary Cluster** -- macro stat curvature, shape tendency of identity
2. **Primary Type** -- centroid shift within cluster curvature, developmental leverage points
3. **Secondary Cluster** -- behavioral negotiation grammar in conflict
4. **Secondary Type** -- fine modulation style within that behavioral grammar

---

## 2. Primary Cluster Layer (Ontology)

Primary clusters answer **fundamental questions about existence**. They are not combat roles and are not designed around counter tables.

### The Four Primary Clusters

#### STRUCTURAL -- _Where things sit_

- Bounds, limits, load, inevitability
- Concerned with position, law, and collapse

Primary Types: Axiom, Nadir, Zenith

---

#### DYNAMIC -- _How things move_

- Motion, disruption, pressure, instability
- Concerned with change, momentum, rupture

Primary Types: Spur, Flux, Surge

---

#### POTENTIAL -- _What could be_

- Capacity, recursion, foresight
- Concerned with unrealized states and pattern emergence

Primary Types: Fractal, Vessel, Oracle

---

#### RESIDUAL -- _What remains_

- Persistence, decay, memory, aftermath
- Concerned with time, residue, and consequence

Primary Types: Echo, Relic, Mire

---

## 3. Primary Types (Rules)

- A monster may only ever have **one Primary Type**.
- Primary Types do **not change** during combat.
- Primary Types define narrative truth, evolution constraints, and long-term identity.
- Primary Clusters do **not** participate in simple rock-paper-scissors logic.

Primary interactions are _contextual_, not oppositional.

---

## 4. Secondary Cluster Layer (Interaction)

Secondary clusters exist to model **force, resistance, and interference** without redefining identity.

They are intentionally:

- more physical
- more mechanical
- more mutable
- more suitable for combat math

### The Locked Triad

#### IMPETUS

- Applied force and forward momentum
- Effects that escalate, propagate, or inherit motion once begun

Used for: damage amplification, initiative pressure, combo inheritance

---

#### VEIL

- Interference without destruction
- Effects that obscure, redirect, or distort interaction outcomes

Used for: passive suppression, redirection, information distortion

---

#### HOLDFAST

- Local resistance and inertial persistence
- Effects that mitigate, endure, or refuse displacement

Used for: damage mitigation, integrity preservation, defensive states

---

## 5. Combat Resolution Philosophy

Interactions resolve as:

> **Attacker Primary --> Defender Secondary**
> **Defender Primary --> Attacker Secondary**

Not Primary vs Primary.

This preserves ontological integrity and emphasizes behavioral negotiation over elemental counters.

### Interaction Model (1 :: [3])

Combat interactions follow a **context --> modifier** pattern:

- **Primary Cluster** defines the interaction context.
- **Secondary Cluster** defines how force behaves within that context.

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

## 6. Waveform Model (Conceptual Framework)

Every monster can be conceptualized as a composite waveform:

- Primary Cluster = Macro curvature class
- Primary Type = Centroid emphasis
- Secondary Cluster = Modulation style
- Secondary Type = Fine modulation
- Individual variation = Amplitude noise

The system intentionally limits decomposition to two fundamental identity components: Primary and Secondary.

Development modifies phase and interference -- not frequency identity.

---

## 7. Developmental Evolution

Instead of permanent stat inflation, development operates through non-permanent but transformative mechanisms.

### Phase Shifts

Experiential events modify:

- Interaction thresholds
- Conversion rules
- Harmonic interference patterns
- Expression pathways

But NOT: Primary identity, Secondary cluster grammar, or ontological classification.

### Kin Wounds

Kin Wounds introduce distortion into the waveform:

- Suppressed amplitudes
- Instability in resolution behavior
- Altered negotiation outcomes

They do not reduce identity -- they alter expression.

### Lumen Embracing

Lumen Embracing realigns harmonics:

- Restores suppressed amplitudes
- Unlocks alternate behavioral interactions
- Modifies how existing stats convert into outcomes

This is identity affirmation, not stat buffing.

---

## 8. Guardrails (Critical Invariants)

1. Primary defines existential identity.
2. Secondary defines negotiation behavior.
3. No tertiary hidden identity layer may emerge.
4. Development modifies interference, not essence.
5. Secondary never overrides Primary ontology.
6. Stats represent potential, not destiny.

---

## 9. Design Status

- Primary ontology is stabilizing
- Secondary interaction layer is intentionally provisional
- Naming is allowed to remain fluid until it becomes quiet

This system is considered **future-safe but intentionally unfinished**.

---

### VERSIONING

*version: 1.0.0*
*updated: 02/19/26*
*authority: type_system_architecture.md*
