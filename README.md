# Causal Transformer (CT)

**Causal Transformer: Scaling Gradient-Based Causal Discovery with Self-Attention**

Submitted to *Current Science*, 2026.

---

## Overview

Causal Transformer (CT) is a self-attention architecture for differentiable causal discovery at $d \geq 200$. It treats variables as tokens and learns causal edge strengths from multi-head attention weights, retaining NOTEARS' acyclicity constraint but constructing $W$ through attention rather than independent parameter optimization.

**Key result:** On standard metrics, the official NOTEARS solver attains higher F1 in the classical regime ($d \lesssim 200$; F1 = 0.98--0.99), so CT's contribution is architectural: under the NOTEARS acyclicity penalty, attention constructs a signed, unbounded adjacency matrix so that spikes remain trainable at $d \ge 200$--$500$ on a consumer GPU (RTX 5060, 8 GB). Its heads specialize into nearly disjoint variable-pair patterns (inter-head Jaccard 0.17), and on 10 TCGA cancer types at $d=200$ the recovered edges enrich in cancer-relevant genes (75% of top hubs are ClinGen Tier-1 drivers), indicating biological plausibility.

---

## Repository Structure

```
.
├── README.md              ← This file
├── requirements.txt       ← Python dependencies
├── manuscript.pdf         ← Anonymized manuscript
├── ESM_1.pdf              ← Electronic Supplementary Material
├── figures/               ← 7 pre-generated PDF figures
├── scripts/               ← Python scripts to regenerate all figures
├── data/                  ← Raw benchmark data
├── results/               ← 35-task real-data benchmark results
└── results_synth/         ← 300-task synthetic multi-seed sweep
```

---

## Quick Start ( ~10 minutes for all figures)

### Prerequisites
- Python 3.12+
- matplotlib >= 3.8, numpy, scipy, pandas (for figure regeneration — no GPU needed)
- A TeX distribution (`pdflatex`, `bibtex`) to build the manuscript/ESM PDFs
- Windows / Linux / macOS

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Regenerate all figures + build the manuscript (one click)
```bash
python run_all.py
```

`run_all.py` regenerates the four plotted figures (Fig 1 is an inline TikZ diagram in the manuscript, so it is drawn at compile time) and then compiles `manuscript.tex` (pdflatex + bibtex) and `ESM_1.tex` into PDFs. If `pdflatex` is not on the system, it still regenerates all figures and skips only the PDF step.

Individual scripts (all resolve paths relative to the script directory, so the package runs on any machine):

| Script | Output figure |
|:--|:--|
| `scripts/gen_fig2.py` | `figures/fig2_results.pdf` — manuscript Figure 2 (2x2: operability, standard F1, phase heatmap, activation curves) |
| `scripts/gen_fig3.py` | `figures/fig3_ablation.pdf` — manuscript Figure 3 (1x3 ablation) |
| `scripts/gen_esm_fig2.py` | `figures/esm_fig1_scaling_law.pdf` — ESM Figure 1 (scaling law) |
| `scripts/gen_esm_fig3.py` | `figures/esm_fig2_tcga_validation.pdf` — ESM Figure 2 (TCGA validation) |

Expected total runtime: a few minutes (the figure scripts load and fit the recorded 80-configuration sweep results; no re-training required).

---

## Verifying Manuscript Tables

Every table in the manuscript and ESM is directly traceable to a data file in this repository.

| Manuscript Table | Data Source | Keys / Notes |
|:--|:--|:--|
| Table 1 (Strategy definitions) | Static | Defined in manuscript |
| Table 2 (80-config sweep) | `data/ct_results.json` | All 80 configurations with edge counts |
| Table 3 (GOLEM/DAGMA comparison) | Embedded in manuscript text | Values also in `gen_fig2.py` |
| Table 4 (TCGA-BRCA mid-range) | `results/tcga_d250_s*.json` to `tcga_d350_s*.json` | 5 seeds each, d=250/300/350 |
| Table 5 (TCGA 10 cancer types) | In manuscript table; derived from `data/mega_33_full.json` | Coherence and edge counts |
| Table 6 (Multi-omics) | `results/omics_expression_s*.json`, `omics_cnv_s*.json`, `omics_methylation_s*.json` | 5 seeds per modality |
| Table 7 (MLP baseline) | `results/mlp_baseline_s*.json` | 5 seeds, d=200 |
| Table 8 (Hub genes) | External databases (ClinGen, DrugBank, COSMIC) | Verified June 2026 |

| ESM Table | Data Source |
|:--|:--|
| Table S1 (Full 80-config sweep) | `data/ct_results.json` + `results_synth/` |
| Table S2 (TCGA complete) | `data/tcga_d200_10seed.json` + `data/mega_33_full.json` |
| Table S4 (DAG validity) | `data/ct_results.json` |
| Table S6 (Method comparison) | Embedded; NOTEARS/GOLEM/DAGMA from `gen_fig2.py` |
| Table S7 (Convergence) | `data/ct_results.json` |

To verify any specific value, open the corresponding JSON file and look for the relevant key. All JSONs are plain text, human-readable.

---

## Synthetic Data Generation

Synthetic DAG data is generated on-the-fly by the scripts using deterministic random seeds:

```
seed = 42 + d * 100 + n * 10 + replicate
```

This ensures exact reproducibility — the same seed always produces the same DAG structure. No download required.

---

## TCGA Data

Real cancer transcriptomic data used in this paper comes from the [UCSC Xena Browser](https://xenabrowser.net/datapages/). The pre-computed benchmark results in `results/` and `data/` capture all necessary statistics; the raw `.tsv` files are not needed unless you wish to re-run the full benchmark pipeline (estimated GPU time: ~18 hours for 35 tasks).

---

## Citation

```bibtex
@article{gao2026ct,
  title={Causal Transformer: Scaling Gradient-Based Causal Discovery with Self-Attention},
  author={Shuaidong Gao},
  journal={Current Science},
  year={2026},
  note={Submitted}
}
```

---

## Related Projects

**[causalscale](https://github.com/sgao-academics/causalscale)** — A unified Python package with seven causal discovery engines under one API, scaling from $d=30$ to genome-wide ($d=17{,}787$). Causal Transformer is one of the engines integrated into causalscale. The package ships via PyPI (`pip install causalscale`) with pre-trained models on HuggingFace Hub.

---

## Quick Reproduction (self-contained, one click)

This repository is a **self-contained replication package**: every figure and table
in the manuscript and the Electronic Supplementary Material is reproducible from
the recorded benchmark results. All paths are resolved **relative to the scripts**,
so the package runs on any machine after cloning/unzipping — no absolute paths.

```bash
# 1) create an isolated environment
python -m venv .venv
# Windows: .venv\Scripts\activate     Linux/macOS: source .venv/bin/activate

# 2) install dependencies
pip install -r requirements.txt

# 3) regenerate all figures + compile the manuscript and ESM
python run_all.py
```

`run_all.py` regenerates the four figures (`fig2_results`, `fig3_ablation`,
`esm_fig1_scaling_law`, `esm_fig2_tcga_validation`) into `figures/`, then
compiles `manuscript.tex` (pdflatex + bibtex) and `ESM_1.tex` into PDFs.
If `pdflatex` is not on the system, it still regenerates all figures and skips
only the PDF step.

**No GPU required** — figures are drawn from `data/ct_results.json` and the
recorded `results/` + `results_synth/` benchmark results. The original training
used an RTX 5060 (8 GB) but is not rerun here, keeping the package fast and
CPU-reproducible.

### Figure / source mapping

| Artifact | File | Reproduced by |
|:--|:--|:--|
| Fig 1 (architecture, TikZ) | inlined in `manuscript.tex` | `pdflatex manuscript.tex` |
| Fig 2 (2x2 results) | `figures/fig2_results.pdf` | `scripts/gen_fig2.py` |
| Fig 3 (1x3 ablation) | `figures/fig3_ablation.pdf` | `scripts/gen_fig3.py` |
| ESM Fig 1 (scaling law) | `figures/esm_fig1_scaling_law.pdf` | `scripts/gen_esm_fig2.py` |
| ESM Fig 2 (TCGA validation) | `figures/esm_fig2_tcga_validation.pdf` | `scripts/gen_esm_fig3.py` |

### Generator dependencies

Installed via `pip install -r requirements.txt`:

```
numpy>=1.26,<3
matplotlib>=3.8,<4
scipy>=1.11,<1.15
pandas>=2.0,<3
```

Note: `torch` is only required if you re-run the model training itself
(read-only reproduction uses only numpy/matplotlib). A TeX distribution
(`pdflatex`, `bibtex`) is needed to build the manuscript/ESM PDFs.
