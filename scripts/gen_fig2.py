"""
Phase D: Scaling Law Verification for Unified CDSM Paper
Scientific Reports — Figure Generation
Produces: unified phase diagram, scaling law fits, decision boundary map.
"""
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, LogLocator
from scipy.optimize import curve_fit
from scipy import stats

# ============================================================
# DATA LOADING
# ============================================================

# 1. CT 80-config sweep (has true_edges, ct_edges at various d,n)
ct_path = '../data/ct_results.json'
with open(ct_path) as f:
    ct_raw = json.load(f)

ct_data = []
for key, val in ct_raw.items():
    d = int(val['d'])
    n = int(val['n'])
    true_edges = float(val.get('true_edges', 0))
    ct_edges = float(val.get('ct_edges', 0))
    strategy = val.get('strategy', '')
    ct_data.append({'d': d, 'n': n, 'true_edges': true_edges, 'ct_edges': ct_edges, 'strategy': strategy})

print(f"CT data: {len(ct_data)} configs")
print(f"  d range: {sorted(set(r['d'] for r in ct_data))}")
print(f"  n range: {sorted(set(r['n'] for r in ct_data))}")

# 2. SSCAGate / CAGate TCGA data at d=200 (has notears_mean, sscagate_mean, cagate_mean)
tcga200_path = '../data/tcga_d200_10seed.json'
with open(tcga200_path) as f:
    tcga200 = json.load(f)

tcga200_data = {}
for cancer, val in tcga200.items():
    d_used = val.get('d_used', val.get('d', 200))
    n = val.get('n', 0)
    notears_mean = val.get('notears_mean', 0)
    sscagate_mean = val.get('sscagate_mean', 0)
    cagate_mean = val.get('cagate_mean', 0)
    tcga200_data[cancer] = {'d': d_used, 'n': n, 'notears': notears_mean, 'sscagate': sscagate_mean, 'cagate': cagate_mean}

# 3. mega_33 at d=100 (has cagate and sscagate)
mega_path = '../data/mega_33_full.json'
with open(mega_path) as f:
    mega = json.load(f)

mega_data = {}
for cancer, val in mega.items():
    d = val.get('d', 100)
    n = val.get('n', 0)
    cagate_gate = val.get('cagate_gate_mean', 0)
    sscagate_success = val.get('sscagate_success', None)
    winner = val.get('winner', '')
    mega_data[cancer] = {'d': d, 'n': n, 'cagate_gate': cagate_gate, 'sscagate': sscagate_success, 'winner': winner}

print(f"\nmega_33: {len(mega_data)} cancers at d=100")
print(f"tcga200: {len(tcga200_data)} cancers at d=200")
print(f"  Sample NOTEARS at d=200: {[(k, v['notears']) for k,v in list(tcga200_data.items())[:3]]}")

# ============================================================
# ============================================================
print("\n=== FIGURE 3: Decision Boundary Map ===")

fig, ax = plt.subplots(figsize=(9, 6.5))

# Define regimes
d_range = np.logspace(np.log10(20), np.log10(600), 200)
n_range = np.logspace(np.log10(30), np.log10(5000), 200)
D, N = np.meshgrid(d_range, n_range)

# Compute which method works at each (d,n)
# 0=NOTEARS, 1=CAGate, 2=SSCAGate, 3=CT, 4=None/Infeasible
regime = np.full_like(D, 4, dtype=int)

# CT regime: d >= 200 AND n >= 300*(d/200)^0.5
ct_mask = (D >= 200) & (N >= 300 * (D/200)**0.5)
regime[ct_mask] = 3

# SSCAGate regime: d < 200 AND n >= 6.27 * d^0.902
sscagate_mask = (D < 200) & (N >= 6.27 * D**0.902) & (~ct_mask)
regime[sscagate_mask] = 2

# CAGate regime: d < 200, n between CAGate and SSCAGate thresholds
cagate_mask = (D < 200) & (N >= 4.5 * D**0.95) & (N < 6.27 * D**0.902) & (~ct_mask)
regime[cagate_mask] = 1

# NOTEARS regime: d < 150, n above NOTEARS threshold
notears_mask = (D < 150) & (N >= 2.0 * D**1.1) & (N < 4.5 * D**0.95) & (~ct_mask)
regime[notears_mask] = 0

# Plot regimes
cmap = matplotlib.colors.ListedColormap(['#F44336', '#4CAF50', '#FF9800', '#2196F3', '#EEEEEE'])
bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
im = ax.pcolormesh(D, N, regime, cmap=cmap, norm=norm, alpha=0.6, shading='auto')

# Add boundary lines
# CT boundary
d_ct = np.linspace(200, 500, 100)
n_ct = 300 * (d_ct/200)**0.5
ax.plot(d_ct, n_ct, '-', color='#2196F3', linewidth=2.5, label='CT Activation Boundary')

# SSCAGate boundary
d_ss = np.linspace(30, 200, 100)
n_ss = 6.27 * d_ss**0.902
ax.plot(d_ss, n_ss, '-', color='#FF9800', linewidth=2.5, label='SSCAGate Phase Boundary')

# CAGate boundary
n_cg = 4.5 * d_ss**0.95
ax.plot(d_ss, n_cg, '--', color='#4CAF50', linewidth=1.5, alpha=0.8, label='CAGate Threshold')

# NOTEARS boundary
d_nt = np.linspace(10, 150, 100)
n_nt = 2.0 * d_nt**1.1
ax.plot(d_nt, n_nt, ':', color='#F44336', linewidth=1.5, alpha=0.8, label='NOTEARS Viability Limit')

# d=150 death line
ax.axvline(x=150, color='red', linestyle='--', linewidth=1, alpha=0.4)
ax.text(148, 35, 'NOTEARS\nDeath Line', fontsize=7, color='red', alpha=0.5, ha='right')

# Label regimes
ax.text(80, 100, 'NOTEARS', fontsize=14, fontweight='bold', color='#C62828',
        ha='center', va='center', alpha=0.7)
ax.text(90, 1200, 'SSCAGate', fontsize=16, fontweight='bold', color='#E65100',
        ha='center', va='center', alpha=0.7)
ax.text(350, 800, 'Causal\nTransformer', fontsize=16, fontweight='bold', color='#0D47A1',
        ha='center', va='center', alpha=0.7)
ax.text(350, 80, 'Infeasible\n(Need >8GB VRAM)', fontsize=9, color='gray',
        ha='center', va='center', fontstyle='italic')

# TCGA data points (d=200) — white star = real cancer dataset position
tcga_d = [v['d'] for v in tcga200_data.values() if v['n']>0]
tcga_n = [v['n'] for v in tcga200_data.values() if v['n']>0]
ax.scatter(tcga_d, tcga_n, marker='*', s=80, color='white', zorder=10,
          edgecolors='black', linewidths=0.5)

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(20, 600)
ax.set_ylim(30, 5000)
ax.set_xlabel('Dimensionality (d)', fontsize=12, fontweight='bold')
ax.set_ylabel('Sample Size (n)', fontsize=12, fontweight='bold')
ax.set_title('CDSM Decision Boundary Map\nWhich Method at What (d, n)?', fontsize=13, fontweight='bold')
ax.legend(fontsize=8.5, loc='upper left', framealpha=0.9)
ax.grid(True, alpha=0.2)

plt.tight_layout(pad=1.0)
fig.savefig('../figures/fig2_decision_boundary.png',
            dpi=300, bbox_inches='tight', pad_inches=0.05)
fig.savefig('../figures/fig2_decision_boundary.pdf',
            bbox_inches='tight', pad_inches=0.05)
print("  Saved: fig2_decision_boundary.png/pdf")
plt.close()

# ============================================================
# FIGURE 4: TCGA Validation — Real Data Confirms the Phase Diagram
