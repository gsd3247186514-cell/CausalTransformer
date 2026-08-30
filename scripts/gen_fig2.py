"""Fig 2 (main text, 2x2): Causal Transformer results overview.

Panels (real data from this paper's own experiments):
  (a) Operability window: CT raw non-zero edges vs d, with the mid-range dense
      d^2 output and the official NOTEARS reference (61 edges, converges).
  (b) Standard F1 under an identical edge-selection rule: official NOTEARS vs CT.
  (c) Phase heatmap: max CT non-zero edges per (d, n) configuration.
  (d) Activation curves across d at each sample size.

This merges the former standalone "operability" (Fig 2) and "phase diagram"
(ESM Fig S1) panels into a single 2x2 main-text figure, so the paper keeps at
most five figures total. Unified high-end palette (see _ct_palette.py).
"""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LogNorm
import _ct_palette as P

P.apply_style()

# --- Reproducibility: resolve paths relative to THIS script, so the package
#     runs on any machine after unzip. data/ and figures/ sit one level up. ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_DATAP = os.path.join(_ROOT, 'data', 'ct_results.json')
_FIGP  = os.path.join(_ROOT, 'figures')
if not os.path.isfile(_DATAP):
    raise FileNotFoundError(f'Missing data file: {_DATAP}')
os.makedirs(_FIGP, exist_ok=True)

data = json.load(open(_DATAP))

# best edges per (d, n)
grid = {}
for k, v in data.items():
    key = (v['d'], v['n'])
    e = v['ct_edges']
    if key not in grid or e > grid[key]:
        grid[key] = e

d_list = sorted({v['d'] for v in data.values()})   # [30, 50, 100, 200]
n_list = sorted({k[1] for k in grid})              # [200, 500, 1000]

def best_edges(d, n):
    return grid.get((d, n), np.nan)

fig, axes = plt.subplots(2, 2, figsize=(13.0, 9.6))
ax_a, ax_b, ax_c, ax_d = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

# ============================================================
# (a) Operability window: CT non-zero edges vs d
# ============================================================
for n, color, marker in [(500, P.CT, 'o'), (1000, P.NOT, 's')]:
    ys = [best_edges(d, n) for d in d_list]
    ax_a.plot(d_list, ys, marker=marker, markersize=7.0, linewidth=2.2,
              color=color, label=f'CT (n = {n})', zorder=4,
              markeredgecolor='white', markeredgewidth=1.0)

mid_d = [250, 300, 350]
mid_edges = [d * d for d in mid_d]
ax_a.scatter(mid_d, mid_edges, marker='^', s=72, color=P.CT, zorder=5,
             edgecolor='white', linewidth=1.0, label='TCGA $d>200$ (dense)')

ax_a.axhline(y=61, color=P.NOT, linestyle='--', linewidth=1.5, zorder=3)
ax_a.text(212, 70, 'NOTEARS (official) $d{=}200$:\nconverges, 61 edges',
          fontsize=6.8, color=P.NOT, va='bottom', ha='left')

ax_a.axvspan(130, 230, color='#F2F7FC', alpha=0.85, zorder=1)
ax_a.axvline(x=200, color=P.CT, linestyle=':', linewidth=1.5, zorder=2)
ax_a.text(0.985, 0.05, 'CT activation $d \\approx 200$',
          transform=ax_a.transAxes, fontsize=8, fontweight='bold',
          color=P.CT, va='bottom', ha='right')
ax_a.annotate('near-zero edges', xy=(100, best_edges(100, 500)),
              xytext=(34, 900), fontsize=6.8, color=P.GRAY, ha='left',
              arrowprops=dict(arrowstyle='->', color=P.GRAY, lw=1.1))

ax_a.set_xscale('log'); ax_a.set_yscale('log')
ax_a.set_xlim(28, 380); ax_a.set_ylim(1, 9e5)
ax_a.set_xlabel('Dimensionality ($d$)', fontweight='bold')
ax_a.set_ylabel('Raw non-zero edges', fontweight='bold')
ax_a.set_title('(a) Operability window', fontweight='bold', loc='left')
ax_a.legend(fontsize=7.4, loc='upper left', framealpha=0.92)
ax_a.grid(True, which='major', color='#D9DDE2', linewidth=0.7)
ax_a.grid(True, which='minor', color='#EDEFF2', linewidth=0.5)
ax_a.spines[['top', 'right']].set_visible(False)
ax_a.set_axisbelow(True)

# ============================================================
# (b) Standard F1: CT vs official NOTEARS (identical edge rule)
# ============================================================
d_f1 = [50, 100, 200]
note_f1 = [0.975, 0.981, 0.993]
ct_f1 = [0.735, 0.674, 0.759]
x = np.arange(len(d_f1))
w = 0.34
ax_b.bar(x - w/2, note_f1, w, color=P.NOT, label='NOTEARS (official)', zorder=3,
         edgecolor='white', linewidth=0.6)
ax_b.bar(x + w/2, ct_f1, w, color=P.CT, label='CT (this work)', zorder=3,
         edgecolor='white', linewidth=0.6)
for xi, v in zip(x - w/2, note_f1):
    ax_b.text(xi, v + 0.015, f'{v:.3f}', ha='center', va='bottom',
              fontsize=7.6, fontweight='bold')
for xi, v in zip(x + w/2, ct_f1):
    ax_b.text(xi, v + 0.015, f'{v:.3f}', ha='center', va='bottom',
              fontsize=7.6, fontweight='bold')
ax_b.set_xticks(x); ax_b.set_xticklabels([f'd = {d}' for d in d_f1])
ax_b.set_ylim(0, 1.18)
ax_b.set_ylabel('Best standard F1', fontweight='bold')
ax_b.set_title('(b) Standard recovery: NOTEARS is stronger',
               fontweight='bold', loc='left')
ax_b.legend(fontsize=7.6, loc='lower right', framealpha=0.92)
ax_b.grid(axis='y', color='#D9DDE2', linewidth=0.7)
ax_b.spines[['top', 'right']].set_visible(False)
ax_b.set_axisbelow(True)

# ============================================================
# (c) Phase heatmap: max CT edges per (d, n)
# ============================================================
d_vals = sorted({k[0] for k in grid})
n_vals = sorted({k[1] for k in grid})
matrix = np.zeros((len(d_vals), len(n_vals)))
for i, d in enumerate(d_vals):
    for j, n in enumerate(n_vals):
        matrix[i, j] = grid.get((d, n), 0)

vmin = max(matrix[matrix > 0].min(), 0.1)
cmap = mcolors.LinearSegmentedColormap.from_list('ct_blue', ['#FFFFFF', P.CT])
im = ax_c.imshow(matrix, aspect='auto', cmap=cmap,
                 norm=LogNorm(vmin=vmin, vmax=matrix.max()))
ax_c.set_xticks(range(len(n_vals))); ax_c.set_xticklabels([str(n) for n in n_vals])
ax_c.set_yticks(range(len(d_vals))); ax_c.set_yticklabels([str(d) for d in d_vals])
ax_c.set_xlabel('n (samples)', fontweight='bold')
ax_c.set_ylabel('d (variables)', fontweight='bold')
cbar = plt.colorbar(im, ax=ax_c, shrink=0.82)
cbar.set_label('Max CT edges', fontweight='bold')
for i in range(len(d_vals)):
    for j in range(len(n_vals)):
        v = matrix[i, j]
        if v > 0:
            col = 'white' if v > vmin * (matrix.max()/vmin) ** 0.6 else 'black'
            ax_c.text(j, i, f'{v:.0f}', ha='center', va='center',
                      fontsize=7.2, color=col)
ax_c.set_title('(c) Phase: max CT edges per $(d, n)$',
               fontweight='bold', loc='left')
ax_c.grid(False)

# ============================================================
# (d) Activation curves across d at each n
# ============================================================
colors = P.blue_ramp(len(n_vals))[::-1]
for j, n in enumerate(n_vals):
    ys = [grid.get((d, n), 0) for d in d_vals]
    ax_d.plot(d_vals, ys, 'o-', color=colors[j], label=f'n = {n}',
              markersize=6.2, linewidth=2.2, markeredgecolor='white',
              markeredgewidth=0.8)
ax_d.set_xlabel('d (variables)', fontweight='bold')
ax_d.set_ylabel('Max CT edges', fontweight='bold')
ax_d.legend(fontsize=7.6, loc='upper left', framealpha=0.92)
ax_d.set_ylim(bottom=-30)
ax_d.axhline(y=1, color=P.GRAY, linestyle='--', linewidth=0.9, alpha=0.6)
ax_d.annotate('CT activates\n($d \\geq 200$)', xy=(200, grid.get((200, 1000), 500)),
              xytext=(95, 880), fontsize=7.4, color=P.CT, fontweight='bold',
              arrowprops=dict(arrowstyle='->', color=P.CT, lw=1.4))
ax_d.set_title('(d) Activation across $d$', fontweight='bold', loc='left')
ax_d.grid(True, color='#D9DDE2', linewidth=0.7)
ax_d.spines[['top', 'right']].set_visible(False)
ax_d.set_axisbelow(True)

fig.suptitle('Causal Transformer: operability, accuracy, and phase behaviour',
             fontsize=13, fontweight='bold', y=0.995)
fig.tight_layout(rect=[0, 0, 1, 0.973])

out = os.path.join(_FIGP, 'fig2_results')
P.save(fig, out)
plt.close()
print('fig2_results done.')
