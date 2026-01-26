# Type System Analysis

**Document Version:** 1.0  
**Last Updated:** 2026-01-21  
**Status:** Canonical Analysis

---

## Executive Summary

This document provides a comprehensive analysis of the MonTamerGens type system, examining the distinction between ontological types (what a monster **is**), functional types (what a monster **does**), and alignment types (how a monster **orients** itself). It categorizes 50+ potential type concepts into their appropriate system layer and maps them to conceptual clusters for implementation planning.

The analysis concludes with strategic recommendations for promoting high-impact types (Nexus, Flux, Veil, Hegemon, Paradox) to primary status while demoting transient states to mutagens and role-based concepts to tempers or secondary attributes.

---

## Table of Contents

1. [Core Distinction: Ontology, Function, and Alignment](#core-distinction)
2. [Type Categorization Framework](#type-categorization)
3. [Conceptual Cluster Mapping](#conceptual-clusters)
4. [Strategic Recommendations](#strategic-recommendations)
5. [Implementation Roadmap](#implementation-roadmap)

---

<a id="core-distinction"></a>

## 1. Core Distinction: Ontology, Function, and Alignment

### 1.1 Ontology — What a Monster **IS**

**Definition:** Ontological types define a creature's fundamental nature, its existence pattern, and how it manifests in reality. These are **identity-level** descriptors that cannot be easily changed or removed.

**Characteristics:**

- Permanent or semi-permanent
- Defines base stat tendencies and growth curves
- Shapes visual identity and form
- Influences naming conventions
- Core to Dex entry tone and lore

**Current Primary Types (16 Canonical):**

**Structural Cluster:**

- **Axiom** — Law, inevitability, foundational rules
- **Bastion** — Endurance, defense, immovability
- **Vessel** — Capacity, containment, potential
- **Nadir** — Collapse, terminal depth, lowest bound

**Vector Cluster:**

- **Spur** — Impulse, acceleration, momentum
- **Flow** — Adaptation, continuity, response
- **Rift** — Disruption, paradox, instability
- **Azimuth** — Orientation, bearing, vector

**Residual Cluster:**

- **Echo** — Memory, recurrence, resonance
- **Mire** — Decay, stagnation, corruption
- **Geist** — Absence, liminality, threshold
- **Fracture** — Strain, fault, imminent failure

**Expressive Cluster:**

- **Zenith** — Apex, culmination, realization
- **Oracle** — Pattern perception, foresight
- **Idol** — Symbol, belief, projection
- **Bloom** — Growth, vitality, expansion

---

### 1.2 Function — What a Monster **DOES**

**Definition:** Functional types describe a creature's operational mode, its role in systems, or how it expresses energy and change. These are **capability-level** descriptors that may shift with training, evolution, or environmental context.

**Characteristics:**

- Can be trained or developed
- Describes behavior patterns
- May be temporary or context-dependent
- Better suited as **Secondary Types** or **Tempers**
- Often role-based or capability-based

**Examples:**

- **Catalyst** — Triggers change in others
- **Sensor** — Information gathering specialist
- **Convert** — Transformation facilitator
- **Adept** — Skilled practitioner
- **Rogue** — Independent operator
- **Emissar/Emissary** — Communication specialist

**Recommendation:** Most functional types should be implemented as **Secondary Types** (modifiers to primary identity) or as **Tempers** (behavioral orientations).

---

### 1.3 Alignment — How a Monster **ORIENTS**

**Definition:** Alignment types describe a creature's relationship to authority, morality, power structures, and social/metaphysical hierarchies. These are **relational-level** descriptors that define how a monster positions itself in the world.

**Characteristics:**

- Describes social or metaphysical stance
- Relates to power, authority, and ethics
- May shift through narrative events
- Best implemented as **Tempers** or **Alignment Axes**
- Often moral or transgressive in nature

**Examples:**

- **Hegemon** — Dominance, authority, rule
- **Paragon** — Ideal exemplar, perfection
- **Profane** — Taboo-breaking, transgressive
- **Pious** — Devout, orthodox, faithful
- **Heretic** — Rejection of authority
- **Zealot** — Extreme devotion
- **Ordain** — Sanctioned, blessed, chosen

**Recommendation:** Alignment types should be implemented as **Tempers** or a separate **Moral/Authority Axis** rather than primary types.

---

<a id="type-categorization"></a>

## 2. Type Categorization Framework

This section categorizes the 50+ potential types identified in project notes into three implementation tiers.

### 2.1 Tier 1: Seed Types (Primary/Ontological)

**Current 16 Primary Types** — Already implemented as canonical seed types defining fundamental monster identity.

**Strong Candidates for Promotion:**

- **Nexus** — Connection point, hub, convergence (Positional/Structural)
- **Flux** — Constant change, instability, transformation (Dynamic/Energetic)
- **Veil** — Obscurity, hidden nature, concealment (Abstract/Exotic)
- **Hegemon** — Dominance, rule, authority (Power/Authority) _[Note: May be better as Temper]_
- **Paradox** — Self-contradiction, impossible existence (Abstract/Exotic)

**Rationale:** These types define **what a monster fundamentally is**, not what it does or how it behaves. They have strong ontological weight and can shape stat curves, visual identity, and naming patterns.

---

### 2.2 Tier 2: Mutagens/States (Temporary/Conditional)

**Definition:** These concepts represent transient conditions, reactive states, or situational modifiers. They should be implemented as **Mutagens** (applied during generation) or **Status Effects** (applied during gameplay).

**State-Based Types:**

- **Inert** — Dormant, inactive
- **Surge** — Temporary power spike
- **Pulse** — Rhythmic fluctuation
- **Excess** — Overloaded state
- **Phase** — Transitional state
- **Cyclic** — Repeating pattern
- **Convalesce** — Recovery state
- **Aquiescent** — Passive, waiting

**Reactive Types:**

- **Contrary** — Oppositional response
- **Inverse** — Reversal of normal function
- **Shear** — Stress response

**Implementation:** These should be **Mutagens** or **Conditional Modifiers**, not primary types.

---

### 2.3 Tier 3: Tempers/Alignments (Behavioral/Relational)

**Definition:** These concepts describe how a monster relates to the world, its role in systems, or its moral/social orientation. They should be implemented as **Tempers**, **Secondary Types**, or **Alignment Axes**.

**Role/Capability Types:**

- **Catalyst** — Change facilitator
- **Sensor** — Information specialist
- **Emissar/Emissary** — Messenger
- **Adept** — Skilled practitioner
- **Rogue** — Independent operator
- **Convert** — Transformation agent
- **Impostor/Impose** — Deception specialist
- **Paragon** — Ideal exemplar

**Power/Authority Types:**

- **Hegemon** — Ruler, dominator
- **Ordain** — Sanctioned authority

**Moral/Transgressive Types:**

- **Profane** — Taboo-breaker
- **Pious** — Devout follower
- **Heretic** — Authority-rejector
- **Zealot** — Extreme devotee

**Positional Types:**

- **Locus** — Focal point
- **Drift** — Unanchored wanderer

**Abstract/Exotic Types:**

- **Phenomena** — Event-based existence
- **Zeitgeist** — Cultural embodiment

**Implementation:** These should be **Tempers** (behavioral orientations), **Secondary Types** (modifiers), or a separate **Alignment System**.

---

<a id="conceptual-clusters"></a>

## 3. Conceptual Cluster Mapping

This section maps all 50+ potential types into 10 conceptual clusters (expanded from the 8 originally identified in BEANS_BRAIN.md).

### Cluster 1: 🧭 Positional / Structural

**Meaning:** Where something sits in a system; spatial or systemic position.

**Types:**

- **Nexus** ⭐ (Promote to Seed)
- **Locus** (Temper/Secondary)
- **Axiom** (Current Seed)
- **Bastion** (Current Seed)
- **Vessel** (Current Seed)
- **Nadir** (Current Seed)

---

### Cluster 2: ⚙️ Dynamic / Energetic

**Meaning:** How energy, change, or motion expresses.

**Types:**

- **Flux** ⭐ (Promote to Seed)
- **Spur** (Current Seed)
- **Flow** (Current Seed)
- **Rift** (Current Seed)
- **Azimuth** (Current Seed)
- **Surge** (Mutagen/State)
- **Pulse** (Mutagen/State)
- **Shear** (Mutagen/State)
- **Phase** (Mutagen/State)

---

### Cluster 3: 🎭 Expressive / Meaning

**Meaning:** How significance, belief, or culmination manifests.

**Types:**

- **Zenith** (Current Seed)
- **Oracle** (Current Seed)
- **Idol** (Current Seed)
- **Bloom** (Current Seed)

---

### Cluster 4: 🌫️ Residual / Aftermath

**Meaning:** What remains after an event; persistence and decay.

**Types:**

- **Echo** (Current Seed)
- **Mire** (Current Seed)
- **Geist** (Current Seed)
- **Fracture** (Current Seed)

---

### Cluster 5: 🌌 Abstract / Exotic

**Meaning:** How something exists outside normal parameters; paradoxes and impossibilities.

**Types:**

- **Veil** ⭐ (Promote to Seed)
- **Paradox** ⭐ (Promote to Seed)
- **Phenomena** (Temper/Secondary)
- **Zeitgeist** (Temper/Secondary)

---

### Cluster 6: 🔮 Contrarian / Circumvental

**Meaning:** How something reacts oppositionally; boundary-pushing behavior.

**Types:**

- **Contrary** (Mutagen/State)
- **Inverse** (Mutagen/State)
- **Heretic** (Temper/Alignment)

---

### Cluster 7: 👑 Power / Authority

**Meaning:** Social or metaphysical dominance; command and control.

**Types:**

- **Hegemon** ⭐ (Promote to Seed _or_ Temper)
- **Paragon** (Temper/Alignment)
- **Ordain** (Temper/Alignment)

---

### Cluster 8: ☠️ Moral / Transgressive

**Meaning:** Ethical alignment; how the world judges behavior.

**Types:**

- **Profane** (Temper/Alignment)
- **Pious** (Temper/Alignment)
- **Heretic** (Temper/Alignment)
- **Zealot** (Temper/Alignment)

---

### Cluster 9: 🧠 Role / Capability / Identity

**Meaning:** How competent, trained, or shaped something is; learned identity.

**Types:**

- **Catalyst** (Temper/Secondary)
- **Sensor** (Temper/Secondary)
- **Adept** (Temper/Secondary)
- **Rogue** (Temper/Secondary)
- **Convert** (Temper/Secondary)
- **Emissar/Emissary** (Temper/Secondary)
- **Impostor/Impose** (Temper/Secondary)

---

### Cluster 10: 🧪 State / Reactivity

**Meaning:** How something responds or changes in different conditions; transient states.

**Types:**

- **Inert** (Mutagen/State)
- **Excess** (Mutagen/State)
- **Cyclic** (Mutagen/State)
- **Convalesce** (Mutagen/State)
- **Aquiescent** (Mutagen/State)
- **Drift** (Mutagen/State)

---

<a id="strategic-recommendations"></a>

## 4. Strategic Recommendations

### 4.1 Promote to Primary Seed Types

**High Priority:**

1. **Nexus** — Connection, convergence, hub (Positional)
2. **Flux** — Constant transformation, instability (Dynamic)
3. **Veil** — Obscurity, hidden truth, concealment (Abstract)
4. **Paradox** — Self-contradiction, impossible existence (Abstract)

**Medium Priority:** 5. **Hegemon** — Dominance, authority, rule (Power)

- _Alternative:_ Implement as a powerful **Temper** instead

**Rationale:**

- These types define **fundamental existence patterns**, not behaviors or states
- They have strong ontological weight
- They can drive unique stat curves and visual identities
- They fill gaps in the current 16-type system
- They enable emergent narrative hooks

---

### 4.2 Demote to Mutagens

**All State/Reactivity Types:**

- Inert, Surge, Pulse, Excess, Phase, Cyclic, Convalesce, Aquiescent, Contrary, Inverse, Shear, Drift

**Implementation:**

- Create mutagens with these names
- Apply stat modifiers (e.g., "Surge" = +ATK, -DEF temporarily)
- Add visual tags (e.g., "Pulse" = rhythmic glow pattern)
- Make them compatible with specific primary types

---

### 4.3 Implement as Tempers/Alignments

**Role/Capability Types:**

- Catalyst, Sensor, Adept, Rogue, Convert, Emissar, Impostor

**Power/Authority Types:**

- Hegemon (if not promoted), Paragon, Ordain

**Moral/Transgressive Types:**

- Profane, Pious, Heretic, Zealot

**Implementation:**

- Create a **Temper** system (behavioral orientation layer)
- Tempers modify behavior, dialogue, evolution paths
- Tempers influence Kin Wounds, Kin Sparks, and resonance
- Tempers do not directly modify stats (or only minor modifiers)

---

### 4.4 Design Principles for Implementation

**Hierarchy of Identity:**

1. **Primary Type** (Seed) — What you **are** (ontology)
2. **Secondary Type** — How you **express** (modifier)
3. **Mutagens** — What **happened** to you (modifications)
4. **Temper** — How you **behave** (orientation)
5. **Kin Attributes** — Your **bond** (relationship)

**Non-Negotiables:**

- Stats must emerge from types + mutagens, not be hardcoded
- Primary types must be ontological, not functional
- States must be temporary (mutagens, not types)
- Alignment must be separate from identity (temper, not type)

---

<a id="implementation-roadmap"></a>

## 5. Implementation Roadmap

### Phase 1: Consolidate Current 16 Types (COMPLETE)

✅ Define 4 clusters of 4 types each  
✅ Update all documentation to canonical types  
✅ Migrate YAML data to new type names  
✅ Update code to consume YAML type data

### Phase 2: Add Promoted Types

- [ ] Design Nexus, Flux, Veil, Paradox stat curves
- [ ] Create type definitions in `seed_types.yaml`
- [ ] Add naming conventions to `type_parts.yaml`
- [ ] Generate forms/species for new types
- [ ] Update type compatibility matrices

### Phase 3: Implement Mutagen System for States

- [ ] Create mutagen definitions for state-based types
- [ ] Define stat modifiers and visual tags
- [ ] Add compatibility rules (type-mutagen affinity)
- [ ] Test mutagen application in generation pipeline

### Phase 4: Design Temper System

- [ ] Define temper architecture (separate from types)
- [ ] Create temper list (role, power, moral categories)
- [ ] Design temper → behavior mapping
- [ ] Integrate tempers with Kin Attributes
- [ ] Implement temper influence on evolution paths

### Phase 5: Testing and Balancing

- [ ] Generate 1000+ seeds with new system
- [ ] Validate stat curves and distributions
- [ ] Test naming output quality
- [ ] Review visual prompt accuracy
- [ ] Balance mutagen/temper impact

---

## Conclusion

The MonTamerGens type system benefits from clear separation of concerns:

- **Seed Types** define ontology (what a monster **is**)
- **Mutagens** define history (what **happened** to it)
- **Tempers** define behavior (how it **acts**)

By promoting high-impact ontological concepts (Nexus, Flux, Veil, Paradox) to seed types and demoting transient states and behavioral roles to their appropriate layers, the system gains clarity, flexibility, and narrative depth.

This analysis provides a blueprint for expanding the type system while maintaining the core design principles of emergence, determinism, and ontological coherence.

---

**Document Version:** 1.0  
**Author:** MonTamerGens Core Design Team  
**Status:** Approved for Implementation Planning
