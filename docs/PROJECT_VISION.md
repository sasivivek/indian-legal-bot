# Project Vision — AI-Native Built Environment Design Platform

> **Mission:** Build an AI-native professional platform that understands, generates, edits, analyzes,
> optimizes, and eventually helps construct the physical world.

---

## 1. What We Are Building

An AI-native professional design and engineering platform for the built environment.

### Building Types (Long-Term)

| Category | Types |
|---|---|
| Residential | Houses, Villas, Apartments, Condominiums |
| Commercial | Offices, Hotels, Retail, Mixed-Use |
| Institutional | Hospitals, Schools, Universities, Government |
| Industrial | Factories, Warehouses, Logistics centres |
| Infrastructure | Bridges, Flyovers, Roads, Tunnels |
| Public | Landmarks, Cultural buildings, Stadiums |
| Utilities | Water, Energy, Telecommunications |

### MVP Scope (Phase 1-10)

Start with residential buildings only:
- Villa (single-family detached)
- House (compact residential)
- Small apartment building (2-4 units)

---

## 2. What Makes This Different

| Conventional CAD / BIM Tools | This Platform |
|---|---|
| Manual drafting | AI-generated structured designs |
| Static files | Live building model — single source of truth |
| Generic parametric tools | Domain-specific AI understanding |
| No historical knowledge | Historical construction intelligence engine |
| No site awareness | Site-aware AI generation |
| No engineering feedback | AI → solver → AI improvement loop |
| Disconnected 2D / 3D / BIM | One master model drives all views |
| Expensive learning curve | Natural language interaction |
| No design alternatives | Generative multi-alternative exploration |

---

## 3. Core Product Philosophy

The system combines ten disciplines into one coherent platform:

1. **Artificial Intelligence** — LLMs, vision models, specialized domain models
2. **Generative Design** — Multi-alternative generation and evaluation
3. **CAD** — Precise 2D drafting, dimensions, annotations
4. **BIM** — Structured object model, IFC export, schedules, quantities
5. **Computational Geometry** — Layout engines, boolean ops, constraint solving
6. **2D Design** — Floor plans, sections, elevations
7. **3D Modeling** — Real-time 3D viewport, materials, lighting
8. **GIS / Site Intelligence** — Terrain, climate, solar, wind, access
9. **Environmental Analysis** — Energy, daylight, shadows, CFD
10. **Historical Knowledge** — Principled extraction from historical architecture

---

## 4. What the Platform Is NOT

- NOT an image generator. Images are outputs, not the core product.
- NOT a rendering engine. Visualization serves the design process.
- NOT a chatbot. The AI is a design reasoning engine.
- NOT a document generator. Documentation is derived from the building model.
- NOT a fake engineering tool. Engineering claims must come from validated solvers.
- NOT a replacement for engineers. It is a professional tool that supports them.

---

## 5. Historical Construction Intelligence Engine

One of the platform major long-term differentiators.

### Objective

Extract timeless design and engineering PRINCIPLES from historical architecture,
then translate them into modern building intelligence.

This is NOT about copying historical styles or generating "historical-looking" buildings.

### What We Extract

- Structural principles (arch, vault, dome, post-and-beam, load path)
- Environmental principles (passive cooling, passive ventilation, thermal mass)
- Spatial principles (spatial hierarchy, circulation, courtyard logic)
- Proportional systems (classical orders, modular ratios, golden section)
- Material knowledge (stone behaviour, timber joinery, brick bonding)
- Urban planning principles (street patterns, public space, defensible space)
- Construction techniques (sequence, centering, formwork principles)

### Translation Pipeline

```
1. Historical Source
   (public-domain book / treatise / archaeological report)
   ↓
2. Extracted Principle
   (structural / environmental / geometric / spatial)
   ↓
3. Physical / Engineering Explanation
   (why it works: physics, mechanics, thermodynamics)
   ↓
4. Modern Material and Technology Equivalent
   (concrete / steel / glass / composites / smart systems)
   ↓
5. Modern Architectural Implementation
   (detail, system, spatial configuration)
   ↓
6. Engineering Validation
   (structural / energy / daylight solver confirms performance)
   ↓
7. Integration into AI Generation
   (becomes a design strategy available to the generation engine)
```

### Examples

| Historical | Principle | Modern Application |
|---|---|---|
| Courtyard house (Islamic, Indian, Roman) | Passive ventilation + daylight + thermal mass + privacy | Atrium, light well, central garden |
| Roman stone arch | Compression-only load path, efficient span | Shell structures, arched bridges |
| Mughal jali screen | Solar control, wind channeling, privacy | Perforated facade, brise-soleil |
| Greek column proportions | Visual weight relative to load-bearing logic | Structural member sizing heuristics |
| Vernacular thick adobe walls | Thermal mass for hot-dry climates | Insulated mass wall, phase-change materials |
| Persian wind tower (badgir) | Stack effect + evaporative cooling | Passive ventilation shaft, solar chimney |
| Japanese engawa | Transition space, solar shading, thermal buffer | Deep overhangs, buffer zones |

### Knowledge Provenance Rules

Every historical fact in the system must carry:
- Source (book title, author, publication date, page)
- License status (public domain / Creative Commons / academic)
- Confidence level (well-established / traditional practice / scholarly interpretation)
- Modern applicability notes
- Date ingested

### What Historical Knowledge Must NOT Do

- Generate buildings in a "historical style" automatically (pastiche risk)
- Apply historical construction safety standards to modern buildings
- Treat historical proportions as engineering specifications without validation
- Override modern building regulations

---

## 6. Site Intelligence

The AI must understand the physical site before generating designs.

### Site Data Layers

| Layer | Data | Source |
|---|---|---|
| Boundary | Legal boundary, easements, setbacks | Cadastral / user input |
| Terrain | Topography, elevation, slope | DEM / survey |
| Climate | Temperature, humidity, rainfall, degree days | Climate APIs |
| Solar | Sun path, hours of exposure, shading | pysolar |
| Wind | Prevailing direction, local effects | Climate data |
| Context | Adjacent buildings, heights, uses | GIS / user input |
| Views | Positive views to preserve, negative to screen | User defined |
| Noise | Sources, estimated levels, buffers | User / GIS |
| Services | Utilities, drainage connections | User / GIS |
| Regulations | FAR, height limits, use zones | User input |

### Site-Aware Generation Example

> "Design a 5-storey apartment block on this site, maximizing south-facing living rooms
>  while minimizing shadow on the neighboring property."

System response:
1. Ingest site boundary, orientation, lat/long
2. Compute solar access and shadow constraints
3. Generate layout alternatives satisfying the brief
4. Evaluate and rank against all constraints
5. Present top candidates with trade-off analysis

---

## 7. Structured Building Model (Core Architectural Requirement)

**This is the single most important architectural requirement of the entire platform.**

One master structured building model drives all views.

### Hierarchy

```
Project
├── Site
│   ├── Boundary (polygon)
│   ├── Terrain (mesh / elevation data)
│   └── Context (neighboring buildings, roads)
├── Building
│   ├── Level[] (ground floor, first floor, ...)
│   │   ├── Room[] (bedroom, living, kitchen, ...)
│   │   ├── Wall[] (exterior, interior, party)
│   │   ├── Door[] (entry, internal, balcony)
│   │   ├── Window[] (standard, skylight, bay)
│   │   ├── Floor (slab / screed / finish)
│   │   ├── Ceiling
│   │   └── Furniture[] (optional spatial planning)
│   ├── Structure
│   │   ├── Column[]
│   │   ├── Beam[]
│   │   ├── Slab[]
│   │   └── Foundation
│   ├── Facade
│   └── Roof
├── MEP
│   ├── HVAC
│   ├── Plumbing
│   └── Electrical
├── Materials
│   └── Material[] (name, properties, cost/m2)
└── Metadata
    ├── ProjectInfo
    ├── Versions[]
    └── GenerationHistory[]
```

### Element Schema

Every building element must carry:

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique identifier |
| type | Enum | Room / Wall / Door / Window / Column / ... |
| geometry | GeometryDef | Points, polygon, extrusion parameters |
| parameters | Dict | Type-specific: width, height, area, etc. |
| relationships | List[Ref] | parent, children, adjacent, connected |
| material_id | UUID? | Reference to material |
| level_id | UUID? | Which floor level |
| properties | Dict | Fire rating, acoustic, thermal, structural |
| constraints | List | Min area, must-be-adjacent, load-bearing flag |
| locked | bool | If true, AI/editing cannot modify |
| generation_source | Enum | manual / ai_generated / template / imported |
| created_at | datetime | |
| updated_at | datetime | |
| version | int | Incremented on every modification |

---

## 8. AI Architecture Philosophy

### Command Chain

```
User (natural language)
  ↓
LLM Intent Parser
  → structured intent: { action, targets, parameters, constraints }
  ↓
Design Command Validator
  → verify action is valid given current locked elements and constraints
  ↓
Design Engine (geometry + rules)
  → compute new geometry
  ↓
Constraint Checker
  → validate area, adjacency, structural, regulatory constraints
  ↓
Master Building Model Update
  ↓
View Synchronization (2D / 3D / BIM / Schedules)
```

### What the LLM Does

- Parse natural language intent
- Reason about design alternatives
- Select appropriate design strategies
- Explain decisions in natural language
- Retrieve relevant historical or code knowledge

### What the LLM Does NOT Do

- Directly compute geometry coordinates
- Fabricate structural or energy analysis results
- Modify locked elements
- Bypass constraint validation
- Produce engineering certifications

---

## 9. Long-Term AI Model Strategy

| Phase | Strategy |
|---|---|
| 1-7 (MVP) | Frontier LLM APIs (Gemini, GPT-4, Claude) with structured prompting |
| 8-12 | Fine-tuned models for: requirements parsing, layout generation, code compliance |
| 13-17 | Specialized architecture domain models |
| 18+ | Architecture Foundation Model: multi-modal, geometry-native |
| Long-term | Built Environment Foundation Model |

Training the foundation model is a long-term research goal, not an MVP objective.
Attempting to train it during MVP development would be premature and wasteful.

---

## 10. Business Model

| Tier | Target | Model |
|---|---|---|
| Professional | Individual architects | Monthly/annual subscription |
| Studio | Small to mid firms (2-20 users) | Team subscription |
| Enterprise | Large firms, developers, government | Enterprise license |
| Platform | Third-party integrations | API licensing |

### Data Strategy

With explicit user consent and appropriate licensing:
- Aggregate anonymized design patterns to improve AI models
- Build proprietary training dataset for architecture foundation model
- All data handling legally compliant and fully transparent
- Users own their project data; they license anonymized patterns, not their projects

---

*Document version: 1.0 | Status: Foundation — Phase 1 | Last updated: 2026-09-10*
