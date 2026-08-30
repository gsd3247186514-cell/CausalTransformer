"""ESM Fig 2: TCGA validation at d=200 across 10 cancer types.

(a) Per-cancer CT edge counts (post-hoc thresholded) vs the NOTEARS reference.
(b) Cluster coherence (biological plausibility proxy) per cancer.
All numbers are REAL from Table (tcga_ct) in the main text.
NOTEARS reference = official solver on TCGA-BRCA d=200: 61 edges (converges).
Unified high-end palette (see _ct_palette.py).
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

# Real per-cancer data (Table: tcga_ct)
cancers = ['BRCA', 'LUAD', 'COAD', 'LUSC', 'HNSC', 'KIRC', 'UCEC', 'BLCA', 'LIHC', 'PRAD']
edges =   [168,    205,   238,   182,   197,   176,   225,   191,   221,   169]
coher =   [0.72,   0.74,  0.78,  0.73,  0.75,  0.71,  0.76,  0.72,  0.75,  0.70]

fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(13.0, 5.6))
x = np.arange(len(cancers))

# ============================================================
# (a) Per-cancer CT edge counts vs NOTEARS reference
# ============================================================
bars = ax_a.bar(x, edges, color=P.CT, edgecolor='white', linewidth=0.6,
                zorder=3, width=0.66)
for xi, v in zip(x, edges):
    ax_a.text(xi, v + 4, f'{v}', ha='center', va='bottom',
              fontsize=7.4, fontweight='bold')
ax_a.axhline(y=61, color=P.NOT, linestyle='--', linewidth=1.6, zorder=4)
ax_a.text(len(cancers) - 0.45, 66, 'NOTEARS (official) BRCA: 61 edges ($d{=}200$)',
          transform=ax_a.transData, fontsize=6.6, color=P.NOT, va='bottom',
          ha='right', zorder=6)
ax_a.set_xticks(x); ax_a.set_xticklabels(cancers, fontsize=8)
ax_a.set_ylabel('Post-hoc CT edges', fontweight='bold')
ax_a.set_title('(a) Per-cancer CT edge count at $d{=}200$',
               fontweight='bold', loc='left')
ax_a.set_ylim(0, 290)
ax_a.grid(axis='y', color='#D9DDE2', linewidth=0.7)
ax_a.spines[['top', 'right']].set_visible(False)
ax_a.set_axisbelow(True)

# ============================================================
# (b) Cluster coherence per cancer
# ============================================================
ax_b.bar(x, coher, color=P.blue_ramp(len(cancers))[::-1], edgecolor='white',
         linewidth=0.6, zorder=3, width=0.66)
ax_b.axhline(y=0.73, color=P.NOT, linestyle='--', linewidth=1.6, zorder=4)
ax_b.text(len(cancers) - 0.45, 0.742, 'mean coherence 0.73', fontsize=7.4,
          color=P.NOT, va='bottom', ha='right')
ax_b.set_xticks(x); ax_b.set_xticklabels(cancers, fontsize=8)
ax_b.set_ylabel('Cluster coherence', fontweight='bold')
ax_b.set_title('(b) Cluster coherence per cancer (co-expression proxy)',
               fontweight='bold', loc='left')
ax_b.set_ylim(0, 1.0)
ax_b.grid(axis='y', color='#D9DDE2', linewidth=0.7)
ax_b.spines[['top', 'right']].set_visible(False)
ax_b.set_axisbelow(True)

fig.suptitle('Causal Transformer on 10 TCGA cancer types ($d=200$)',
             fontsize=13, fontweight='bold', y=0.985)
# single figure-level caption
fig.text(0.5, 0.015,
         'Top: post-hoc CT edge counts (coherence-screened). Bottom: coherence = '
         'fraction of CT-selected edges whose two genes are co-expressed (Pearson $r>0.4$) '
         'within a K-means cluster --- a biological-plausibility screen, NOT causal precision. '
         'CT and NOTEARS use different post-hoc rules, so counts are not directly comparable.',
         ha='center', va='bottom', fontsize=6.9, color=P.MUTED, style='italic',
         linespacing=1.4)
fig.tight_layout(rect=[0, 0.055, 1, 0.965])

out = os.path.join(figs, 'esm_fig2_tcga_validation')
P.save(fig, out)
plt.close()
print('esm_fig2_tcga_validation done.')
