# GZ_3D_Hull_Method – Phase 3 (STL Geometry Ingestion)

Author: Samruddhi Goud  
Institute: IIT Madras  
Project: 3D Geometry-Based Ship Stability Solver

---

## Overview

This repository contains Phase 3 of a multi-phase project to build a ship stability solver from first principles.

Phase 3 introduces **STL-based hull input**, allowing real ship geometries (triangular meshes) to be used as truth geometry for hydrostatics computation. The existing Phase 2 geometry-based solver is reused unchanged.

This phase focuses strictly on **geometry ingestion and robustness**, not on equilibrium solving or damage stability.

---

## Phase Structure

- **Phase 1** – Offset table based GZ computation (baseline, frozen)
- **Phase 2** – True 3D geometry-based hydrostatics (parametric hulls)
- **Phase 3** – STL ingestion & real hull geometry pipeline (this repo)
- **Phase 4 (planned)** – Equilibrium solver, sinkage, trim, force balance
- **Phase 5 (planned)** – Damage stability & compartment modeling

---

## Phase 3 Scope

Included:
- ASCII & binary STL ingestion
- Mesh validation (manifold, degenerate triangles, orientation)
- Real geometry hydrostatics
- Geometry-based deck edge immersion detection
- KN & GZ computation from 3D mesh

Explicitly Excluded:
- Sinkage & trim iteration
- Force/moment equilibrium
- Damage stability
- Flooding
- Compartment modeling

---

## Folder Structure

GZ_STL_Ph3/
├── data/ # STL files
├── mesh/ # STL reader, validation, normalization
├── solver/ # Hydrostatics (Phase 2 logic)
└── main.py # Driver script

---

## How It Works

1. STL file is read (ASCII or binary)
2. Mesh is validated and cleaned
3. Hull is rotated for each heel angle
4. Mesh is clipped at fixed draft
5. Submerged volume and centroid are computed
6. KN is extracted from buoyancy shift
7. GZ is computed as:
   
   GZ = KN − KG sin(θ)

8. Deck edge immersion is detected from geometry

---

## Known Limitations

This phase operates under the following assumptions:

- Fixed draft (no sinkage or trim)
- No equilibrium solver
- No displacement conservation
- No damage stability
- Waterplane closed using fan triangulation (introduces small centroid bias)

As a result:
- GZ is not physically valid at large heel angles
- Positive GZ may appear at 90° due to model breakdown
- Small numerical irregularities may be present due to mesh quality

These behaviors are documented and intentional.

---

## Test Cases

- Rectangular box hull (analytical validation)
- KCS hull (real ship STL)

---

## How To Run

```bash
python3 main.py
