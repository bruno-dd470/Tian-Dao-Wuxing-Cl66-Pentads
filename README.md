# WuXing and Cl(6,6): 144 Pentads for a Unified Relational Physics

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19947629.svg)](https://doi.org/10.5281/zenodo.19947629)

**Author:** Bruno DE DOMINICIS  
**ORCID:** [0009-0009-0380-3056](https://orcid.org/0009-0009-0380-3056)  
**Date:** April 2026  
**License:** CC BY 4.0

## Description

This repository contains the source code, data, and manuscript for the paper:

**"WuXing and Cl(6,6): 144 Pentads for a Unified Relational Physics"**

The work proposes a geometric and algebraic unification of particle physics and cosmology by replacing the paradigm of quantum fields on a fixed spacetime background with a relational pre‑geometric substrate based on the Clifford algebra $\text{Cl}(6,6)$. Integrating P. Rowlands' nilpotent formalism and J.-P. Petit's Janus bimetric model, we demonstrate that both frameworks are orthogonal projections of a single dual invariant.

## Repository Structure

```
Tian-Dao-Wuxing-Cl66-Pentads/
├── article/           # Manuscript source files
│   ├── 144_pentades9_en.md   # Main article (Markdown)
│   ├── 144_pentades9_en.pdf  # Main article (PDF)
│   ├── 144_pentades9_en.tex  # Generated LaTeX source
│   ├── template_ENG.tex      # LaTeX template
│   ├── references.bib        # Bibliography
│   └── ieee.csl              # Citation style
├── data/              # Lattice data (Nebe Λ₇₂)
│   ├── G72.npy               # Gram matrix (72×72)
│   ├── eigvals_72.txt        # 72 eigenvalues λ_i
│   ├── eigvecs_72.npy        # 72 eigenvectors
│   ├── W_light_144x10.npy    # Projection matrix (indices 0-9)
│   └── W_heavy_144x10.npy    # Projection matrix (indices 10+)
├── scripts/           # Python scripts for mass calculations
│   ├── lattice_utils.py      # Shared utilities
│   ├── masses_triplets.py    # Hadron masses (π, K, p)
│   ├── masses_paires.py      # Boson and lepton masses
│   ├── mass_e-_orbites.py    # Electron via cyclic orbits
│   ├── magnetar_resonance.py # 200 MeV resonance
│   └── matrice_opérateur_T.py # Transition operator T diagonalisation
├── docs/              # Additional documentation
├── notebooks/         # Jupyter notebooks (if any)
└── tests/             # Unit tests
```

## Reproducing the Results

### Requirements

```bash
pip install -r requirements.txt
```

### Run Mass Validation

```bash
python scripts/masses_triplets.py
python scripts/masses_paires.py
python scripts/magnetar_resonance.py
```

### Compile the Article

```bash
cd article
pandoc 144_pentades9_en.md \
  --template=template_ENG.tex \
  -o 144_pentades9_en.pdf \
  --pdf-engine=xelatex \
  --bibliography=references.bib \
  --csl=ieee.csl \
  --citeproc \
  --toc
```

## Citation

```bibtex
@misc{DeDominicis2026,
  author = {De Dominicis, Bruno},
  title = {WuXing and Cl(6,6): 144 Pentads for a Unified Relational Physics},
  year = {2026},
  doi = {10.5281/zenodo.19947629}
}
```

## Acknowledgments

The author thanks Professors Peter Rowlands and Jean-Pierre Petit for their foundational work on nilpotent algebras and bimetric cosmology. The contributions of Gabriele Nebe on 72-dimensional unimodular lattices have been essential to ground the pentadic network in a concrete discrete geometry.

## Contact

For inquiries, please contact the author via [ORCID](https://orcid.org/0009-0009-0380-3056).
EOF
```

## Commit et push

```bash
git add README.md
git rm README_old.md  # si vous avez fait la sauvegarde
git commit -m "Replace README with correct description of WuXing Cl(6,6) article"
git push origin main
```

## Vérification

```bash
# Voir le nouveau README
cat README.md | head -20
```

Le README est maintenant cohérent avec votre dépôt.
