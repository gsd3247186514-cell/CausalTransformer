"""ESM Fig 2: CT scaling beyond the sweep — operable range and the attention ceiling.

All points are REAL numbers reported in this paper (mid-range table + d=500 result).
(a) Raw non-zero edges vs d on TCGA-BRCA: dense d^2 output until the O(d^2) memory
    ceiling collapses CT near d=500. (b) Operable vs degenerate viewpoint: the dense
    output is a *different* failure mode from an all-zero output, and neither equals
    successful recovery. Official NOTEARS is shown as an operable reference.
"""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import _ct_palette as P

P.apply_style()

# --- Relative paths so the package runs on any machine after unzip ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
figs = os.path.join(_ROOT, 'figures')
os.makedirs(figs, exist_ok=True)

# --- real data from main text ---
# id range  d    edges            note
d_ok = [200, 225, 250, 300]        # n=1218 TCGA-BRCA, CT operable & dense
# For d=200 the dense matrix is 200^2 = 40,000; 250^2=62,500; 300^2=90,000.
# Table reported CT Edges = d^2 exactly (dense). Use those.
edges_ok = [200**2, 225**2, 250**2, 300**2]
d_fail = [500]
edges_fail = [12]

fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(13.0, 5.6))

# (a) Operable range vs attention ceiling
ax_a.plot(d_ok, edges_ok, '-o', color=P.CT, markersize=7, linewidth=2.2,
          label='CT (TCGA-BRCA, dense $d^2$ output)', zorder=4,
          markeredgecolor='white', markeredgewidth=1.0)
ax_a.plot(d_fail, edges_fail, 'x', color=P.NOT, markersize=11, linewidth=2.4,
          label='CT at $d=500$ (collapse)', zorder=5)
ax_a.axhline(y=61, color=P.NOT, linestyle='--', linewidth=1.4, zorder=3)
ax_a.text(232, 75, 'NOTEARS (official) $d=200$: converges, 61 edges',
          fontsize=7.2, color=P.NOT, va='bottom', ha='left')

ax_a.annotate('attention ceiling\n$O(d^2)$ memory (8 GB)', xy=(500, 12),
              xytext=(405, 4e3), fontsize=7.6, color=P.NOT, ha='left',
              arrowprops=dict(arrowstyle='->', color=P.NOT, lw=1.2))

ax_a.axvspan(180, 320, color='#F2F7FC', alpha=0.85, zorder=1)
ax_a.text(0.52, 0.12, 'operable (dense $d^2$ output)', transform=ax_a.transAxes,
          fontsize=8, color=P.CT, fontweight='bold', ha='center', va='bottom')

ax_a.set_xscale('log'); ax_a.set_yscale('log')
ax_a.set_xlim(185, 560); ax_a.set_ylim(1, 3e5)
ax_a.set_xlabel('Dimensionality ($d$)', fontweight='bold')
ax_a.set_ylabel('Raw non-zero edges', fontweight='bold')
ax_a.set_title('(a) Operable range and the attention ceiling', fontweight='bold')
ax_a.legend(fontsize=7.8, loc='upper left', framealpha=0.92)
ax_a.grid(True, which='major', color='#D9DDE2', linewidth=0.7)
ax_a.grid(True, which='minor', color='#EDEFF2', linewidth=0.5)
ax_a.spines[['top', 'right']].set_visible(False)
ax_a.set_axisbelow(True)

# (b) Two degenerate failure modes: all-zero vs fully dense
modes = ['All-zero\n(d=100, n=200)', 'Dense $d^2$\n($d>200$)', 'Collapse\n($d=500$)', 'Valid\n(post-hoc)']
# representative qualitative illustration using reported numbers
vals = [0, max(edges_ok), 12, 198]   # 0 ; 90,000 ; 12 ; 198 post-hoc
colors = [P.GRAY, P.CT, P.NOT, P.SSC]
bars = ax_b.bar(range(4), vals, color=colors, edgecolor='white', linewidth=0.7, zorder=3, width=0.62)
ax_b.set_yscale('log')
for b, v in zip(bars, vals):
    ax_b.text(b.get_x() + b.get_width()/2, max(v, 1) * 1.25, f'{v:,}', ha='center',
              va='bottom', fontsize=7.5, fontweight='bold')
ax_b.set_xticks(range(4)); ax_b.set_xticklabels(modes, fontsize=7.6)
ax_b.set_ylabel('Edges (log scale)', fontweight='bold')
ax_b.set_ylim(0.5, 3e5)
ax_b.set_title('(b) Degenerate vs usable outputs', fontweight='bold')
ax_b.grid(axis='y', color='#D9DDE2', linewidth=0.7)
ax_b.spines[['top', 'right']].set_visible(False)
ax_b.set_axisbelow(True)

fig.suptitle('Causal Transformer scaling beyond the $d=200$ sweep',
             fontsize=13, fontweight='bold', y=0.985)
fig.text(0.5, 0.015,
         'An all-zero output (fails to fit) and a fully dense output (fails to select) are '
         'both degenerate; structure emerges only after post-hoc edge selection. '
         'Green bar = the post-hoc thresholded result (198 edges on TCGA, coherence 0.73).',
         ha='center', va='bottom', fontsize=6.9, color=P.MUTED, style='italic',
         linespacing=1.4)
fig.tight_layout(rect=[0, 0.055, 1, 0.965])

out = os.path.join(figs, 'esm_fig1_scaling_law')
P.save(fig, out)
plt.close()
print('esm_fig1_scaling_law done.')
