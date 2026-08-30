"""Fig 3: CT ablation study at d=200, n=1000 (3 panels).

Reads the real sweep results from ../data/ct_results.json (resolved relative to
this script) and the unified palette (_ct_palette.py), so it runs on any machine.
y-axis labeled with the paper's operability language (raw non-zero edges).
"""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import _ct_palette as P

P.apply_style()

# --- Relative paths so the package runs on any machine after unzip ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_DATAP = os.path.join(_ROOT, 'data', 'ct_results.json')
_FIGP  = os.path.join(_ROOT, 'figures')
if not os.path.isfile(_DATAP):
    raise FileNotFoundError(f'Missing data file: {_DATAP}')
os.makedirs(_FIGP, exist_ok=True)

data = json.load(open(_DATAP))

# Collect d=200, n=1000 configs
configs = {}
for k, v in data.items():
    if v['d'] == 200 and v['n'] == 1000:
        dm = v['kwargs']['d_model']; nh = v['kwargs']['n_heads']; ne = v['kwargs']['n_epochs']
        configs[k] = {'d_model': dm, 'n_heads': nh, 'n_epochs': ne, 'edges': v['ct_edges']}
        print(f'{k:32s} edges={v["ct_edges"]:8.1f}  dm={dm}  nh={nh}  ne={ne}')

def get(dm, nh, ne):
    for v in configs.values():
        if v['d_model'] == dm and v['n_heads'] == nh and v['n_epochs'] == ne:
            return v['edges']
    return 0.0

# Grouped-bar helper
def grouped(ax, xlabels, series, ylab, title, legend_loc='upper left'):
    x = np.arange(len(xlabels))
    nser = len(series)
    w = 0.78 / nser
    for i, (name, vals, col) in enumerate(series):
        off = (i - (nser - 1) / 2) * w
        bars = ax.bar(x + off, vals, w, color=col, label=name,
                      edgecolor='white', linewidth=0.5, zorder=3)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width()/2, b.get_height(), f'{v:.0f}',
                    ha='center', va='bottom', fontsize=8, fontweight='bold', zorder=4)
    ax.set_xticks(x); ax.set_xticklabels(xlabels)
    ax.set_ylabel(ylab, fontweight='bold')
    ax.set_title(title, fontweight='bold')
    ax.legend(fontsize=8.5, loc=legend_loc, framealpha=0.92, ncol=1)
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_ylim(0, max(max(s[1]) for s in series) * 1.20)

fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.3))

c4 = P.blue_ramp(2)        # 4-head / 8-head
cE = P.blue_ramp(2)        # 200 / 500 epochs

# Panel A: head count (4 vs 8) across d_model
pad = axes[0]
series_a = [
    ('4 heads',  [get(64, 4, 500), get(128, 4, 500)], P.GRAY),
    ('8 heads',  [get(64, 8, 500), get(128, 8, 500)], P.NOT),
]
grouped(pad, ['d_model=64', 'd_model=128'], series_a,
        'Raw non-zero edges', '(a) Head count')

# Panel B: epoch count (200 vs 500)
pb = axes[1]
series_b = [
    ('200 epochs', [get(64, 8, 200), get(128, 8, 200)], P.GRAY),
    ('500 epochs', [get(64, 8, 500), get(128, 8, 500)], P.CT),
]
grouped(pb, ['d_model=64', 'd_model=128'], series_b,
        'Raw non-zero edges', '(b) Epoch count')

# Panel C: d_model width
pc = axes[2]
vals = [get(64, 8, 500), get(128, 8, 500), get(256, 8, 200)]
labels = ['64', '128', '256*']
cols = [P.blue_ramp(3)[2], P.blue_ramp(3)[1], P.blue_ramp(3)[0]]
bars = pc.bar(range(3), vals, color=cols, edgecolor='white', linewidth=0.5, zorder=3, width=0.62)
for b, v in zip(bars, vals):
    pc.text(b.get_x() + b.get_width()/2, b.get_height(), f'{v:.0f}',
            ha='center', va='bottom', fontsize=9, fontweight='bold', zorder=4)
pc.set_xticks(range(3)); pc.set_xticklabels(labels)
pc.set_ylabel('Raw non-zero edges', fontweight='bold')
pc.set_title('(c) $d_{\\mathrm{model}}$ width', fontweight='bold')
pc.set_ylim(0, max(vals) * 1.20)
pc.text(2, vals[2] + max(vals)*0.04, '*200 epochs\n(8 GB VRAM limit)',
        ha='center', va='bottom', fontsize=6.8, color=P.MUTED)
pc.spines[['top', 'right']].set_visible(False)

# Values are raw counts (operability), NOT recovery quality.
for a in axes:
    a.set_axisbelow(True)
    a.grid(axis='y', color='#E3E6EA', linewidth=0.6)

fig.suptitle('CT ablation at $d=200$, $n=1{,}000$  (raw edge counts measure the '
             'operability of the gradient pathway, not recovery quality)',
             fontsize=10.5, fontweight='bold', y=1.03)
plt.tight_layout()

out = os.path.join(_FIGP, 'fig3_ablation')
P.save(fig, out)
plt.close()
print('fig3 done.')
