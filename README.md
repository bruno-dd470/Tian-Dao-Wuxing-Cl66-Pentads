# The Genetic Code as a 64→20 Clifford Invariant: Implications for Regulated AI

**Author:** Bruno DE DOMINICIS  
**ORCID:** [0009-0009-0380-3056](https://orcid.org/0009-0009-0380-3056)  
**Date:** April 2026  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

## 1. Description

This repository contains the manuscript, technical synthesis, and supplementary code for the research project **"The genetic code as a 64→20 Clifford invariant: implications for regulated AI"**.

The work formalizes the reduction of combinatorial complexity (64 configurations) into 20 functional classes, a structure observed in the genetic code. This reduction is derived from the geometry of the level-3 double tetrahedron (Merkabah) and the algebraic structure of $\mathrm{Cl}(6,0)$. The model proposes a substrate-independent framework for complexity regulation with applications in artificial intelligence (AI).

### Repository Split
To allow for independent citation and versioning, the materials in this repository are organized into **two separate Zenodo deposits**:

1.  **Scientific Manuscript:** The primary paper detailing the 64→20 reduction, the Merkabah filtration, and the biological validation.
2.  **Technical Synthesis & Code:** The detailed mathematical synthesis (spectral dynamics, Clifford algebra), Python verification scripts, and graph visualizations.

## 2. DOIs and Contents

### 📘 Part 1: Scientific Manuscript
**Title:** *The genetic code as a 64→20 Clifford invariant: implications for regulated AI*  
**DOI:** `10.5281/zenodo.XXXXXX` *(To be filled after publication)*

| File Name | Description |
| :--- | :--- |
| `rapport_merkabah_pour_revue_scientifique80.pdf` | The peer-reviewed manuscript submission. |
| `rapport_merkabah_pour_revue_scientifique80.md` | Source file of the manuscript (Markdown format). |

### 💻 Part 2: Technical Synthesis & Code
**Title:** *Merkabah, Clifford and Spectral Dynamics: A Comprehensive Synthesis*  
**DOI:** `10.5281/zenodo.YYYYYY` *(To be filled after publication)*

| File Name | Description |
| :--- | :--- |
| `Merkabah_Clifford_et_dynamique_spectrale_une_synthèse_complète.pdf` | Comprehensive synthesis report detailing the spectral dynamics and the $\mathrm{Cl}(6,6)$ bicosmic reservoir model. |
| `verify_merkabah_topology.py` | Python script to validate the topological properties of the 20 attractor graph (nodes, edges, girth, diameter). |
| `Graphe_dual_des_pentades_merkabah3.py` | Python script to visualize the dual graph of pentads, highlighting the tropical belts and thresholds. |
| `Penta_graph.png` | Output visualization of the dual pentad graph. |
| `readme.md` | This documentation file. |

## 3. Technical Requirements

To run the supplementary Python scripts located in **Part 2**, you will need **Python 3.x** and the following libraries:

```bash
pip install networkx matplotlib numpy
```

## 4. Usage

### Topological Verification
Run the script to verify that the 20 attractors form a valid Merkabah structure with the expected dual graph topology.
```bash
python verify_merkabah_topology.py
```
*Output: A console report verifying the 20 vertices, uniform pentad distribution, and the polarity gradient.*

### Dual Graph Visualization
Generate the visual representation of the 12 pentads as a graph.
```bash
python graphe_dual_des_pentades_merkabah3.py
```
*Output: A graphical window displaying the pentad network topology.*

## 5. Citation

This project is split into two citable entities. Please cite the version relevant to your work:

**For the scientific manuscript and biological application:**
> **DE DOMINICIS, B.** (2026). *The genetic code as a 64→20 Clifford invariant: implications for regulated AI*. Zenodo. [DOI: 10.5281/zenodo.XXXXXX]

**For the technical synthesis, spectral dynamics, and code implementation:**
> **DE DOMINICIS, B.** (2026). *Merkabah, Clifford and Spectral Dynamics: A Comprehensive Synthesis* [Data set and code]. Zenodo. [DOI: 10.5281/zenodo.YYYYYY]

## 6. Acknowledgements

We thank Peter Rowlands for his foundational work on nilpotent Clifford algebras and the genetic code.

For inquiries, please contact the author via the ORCID link provided above.
