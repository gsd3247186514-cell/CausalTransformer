"""ESM Fig 1: Unified Phase Diagram — CT edge count across (d,n) grid."""
import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import os

base = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
figs_dir = os.path.join(base, 'figures')

# Load CT sweep data
with open(r'D:\NO.1\_nightly\ct_results.json') as f:
    data = json.load(f)

# Extract (d,n) -> max edges across strategies
grid = {}
for k, v in data.items():
    d, n = v['d'], v['n']
    edges = v['ct_edges']
    key = (d, n)
    if key not in grid or edges > grid[key]:
        grid[key] = edges

# Build matrix for heatmap
d_vals = sorted(set(k[0] for k in grid))
n_vals = sorted(set(k[1] for k in grid))
matrix = np.zeros((len(d_vals), len(n_vals)))
for i, d in enumerate(d_vals):
    for j, n in enumerate(n_vals):
        matrix[i, j] = grid.get((d, n), 0)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))

# Panel A: Heatmap
im = ax1.imshow(matrix, aspect='auto', cmap='YlOrRd',
                norm=LogNorm(vmin=max(matrix[matrix>0].min(), 0.1), vmax=matrix.max()))
ax1.set_xticks(range(len(n_vals)))
ax1.set_xticklabels([str(n) for n in n_vals])
ax1.set_yticks(range(len(d_vals)))
ax1.set_yticklabels([str(d) for d in d_vals])
ax1.set_xlabel('n (samples)')
ax1.set_ylabel('d (variables)')
cbar = plt.colorbar(im, ax=ax1, shrink=0.8)
cbar.set_label('Max CT edges')
# Annotate cells
for i in range(len(d_vals)):
    for j in range(len(n_vals)):
        v = matrix[i, j]
        color = 'white' if v > 500 else 'black'
        ax1.text(j, i, f'{v:.0f}', ha='center', va='center', fontsize=7, color=color)
ax1.set_title('(a) CT Edge Recovery Heatmap')

# Panel B: d-n performance curves (best strategy per (d,n))
ax2.set_title('(b) CT Performance Curves')
colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(n_vals)))
for j, n in enumerate(n_vals):
    ys = [grid.get((d, n), 0) for d in d_vals]
    ax2.plot(d_vals, ys, 'o-', color=colors[j], label=f'n={n}', markersize=6, linewidth=2)
ax2.set_xlabel('d (variables)')
ax2.set_ylabel('CT edges')
ax2.legend(fontsize=8, loc='upper left')
ax2.set_ylim(bottom=-10)
ax2.axhline(y=1, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

# Add phase boundary annotation
ax2.annotate('CT activates\n(d >= 200)', xy=(200, grid.get((200, 1000), 500)),
             xytext=(150, 800), fontsize=8, color='red', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

fig.suptitle('ESM Fig 1: CT Phase Diagram Across (d, n) Configurations', fontsize=12, fontweight='bold')
plt.tight_layout(pad=1.2)

for ext in ['png', 'pdf']:
    out = os.path.join(figs_dir, f'esm_fig1_phase_diagram.{ext}')
    fig.savefig(out, dpi=300, bbox_inches='tight', pad_inches=0.05)
    print(f'Saved: {out}')

plt.close()
print('ESM Fig 1 done.')
