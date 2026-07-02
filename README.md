# Causal Transformer (CT)

**Causal Transformer: Scaling Gradient-Based Causal Discovery to 500 Variables**

Submitted to *Machine Learning* (Springer), 2026.

---

## Overview

Causal Transformer (CT) is a self-attention architecture for differentiable causal discovery at $d \geq 200$. It treats variables as tokens and learns causal edge strengths from multi-head attention weights, retaining NOTEARS' acyclicity constraint but constructing $W$ through attention rather than independent parameter optimization.

**Key result:** CT produces 1,028 edges at $d=200$ where NOTEARS returns exactly 0. On 10 TCGA cancer types, 75% of CT-discovered top-hub genes are ClinGen Tier-1 cancer drivers. CT extends DAG-based causal discovery to the frontier of $d \approx 500$, operating reliably at $d=250$–$350$, all on consumer hardware (RTX 5060, 8 GB).

---

## Repository Structure

```
.
├── README.md              ← This file
├── requirements.txt       ← Python dependencies
├── manuscript.pdf         ← Anonymized manuscript
├── ESM_1.pdf              ← Electronic Supplementary Material
├── cover_letter_mach.pdf  ← Cover letter
├── contribution_sheet.pdf ← Author contribution statement
├── figures/               ← 7 PDF figures (main + ESM)
├── scripts/               ← 7 Python scripts to regenerate all figures
├── data/                  ← Raw benchmark data (4 JSONs)
├── results/               ← 35-task real-data benchmark results
└── results_synth/         ← 300-task synthetic multi-seed sweep
```

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```
Requires: Python 3.12+, PyTorch 2.11+, CUDA 12.8+, NVIDIA GPU ≥ 8 GB VRAM.

### 2. Regenerate figures
```bash
cd scripts/
python gen_fig1.py   # Architecture diagram (Figure 1)
python gen_fig2.py   # Decision boundary map (Figure 2)
python gen_fig3.py   # Ablation study (Figure 3)
python gen_graphical_abstract.py  # Graphical abstract
```

Outputs are written to `../figures/`.

### 3. Generate all 7 figures at once
```bash
cd scripts/
for f in gen_*.py; do python $f; done
```

---

## Data Sources

- **TCGA RNA-Seq**: [UCSC Xena Browser](https://xenabrowser.net/datapages/)
- **Synthetic data**: Generated on-the-fly with deterministic seeds ($42 + d \cdot 100 + n \cdot 10 + \text{replicate}$)
- **Benchmark JSONs**: Pre-computed results for all 335 experiments, enabling instant verification of every table in the manuscript and ESM

---

## Citation

```bibtex
@article{gao2026ct,
  title={Causal Transformer: Scaling Gradient-Based Causal Discovery to 500 Variables},
  author={Anonymous},
  journal={Machine Learning},
  year={2026},
  note={Submitted}
}
```

---

## License

Code and data are provided for research reproducibility purposes.
