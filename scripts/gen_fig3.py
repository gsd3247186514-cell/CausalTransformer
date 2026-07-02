"""Generate ablation figure (3 panels) for CT paper."""
import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Load data
with open('../data/ct_results.json') as f:
    data = json.load(f)

# Extract d=200, n=1000 configurations
configs = {}
for k, v in data.items():
    if v['d'] == 200 and v['n'] == 1000:
        dm = v['kwargs']['d_model']
        nh = v['kwargs']['n_heads']
        ne = v['kwargs']['n_epochs']
        configs[k] = {'d_model': dm, 'n_heads': nh, 'n_epochs': ne, 'edges': v['ct_edges']}
        print(f'{k:30s} edges={v["ct_edges"]:7.1f} dm={dm} nh={nh} ne={ne}')

# ===== FIGURE: Ablation Panels =====
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

# Panel A: Head count ablation
ax = axes[0]
dm64_4 = [v['edges'] for v in configs.values() if v['d_model']==64 and v['n_heads']==4 and v['n_epochs']==500]
dm64_8 = [v['edges'] for v in configs.values() if v['d_model']==64 and v['n_heads']==8 and v['n_epochs']==500]
dm128_4 = [v['edges'] for v in configs.values() if v['d_model']==128 and v['n_heads']==4 and v['n_epochs']==500]
dm128_8 = [v['edges'] for v in configs.values() if v['d_model']==128 and v['n_heads']==8 and v['n_epochs']==500]

x_pos = [0, 1]
w = 0.35
ax.bar([x-w/2 for x in x_pos], [dm64_4[0] if dm64_4 else 0, dm128_4[0] if dm128_4 else 0], w, color=colors[0], label='4 heads', edgecolor='white', linewidth=0.5)
ax.bar([x+w/2 for x in x_pos], [dm64_8[0] if dm64_8 else 0, dm128_8[0] if dm128_8 else 0], w, color=colors[1], label='8 heads', edgecolor='white', linewidth=0.5)
ax.set_xticks(x_pos)
ax.set_xticklabels(['d_model=64', 'd_model=128'])
ax.set_ylabel('Edges recovered')
ax.set_title('(a) Head count ablation')
ax.legend(fontsize=8)
ax.set_ylim(0, 1200)
# Annotate
for i, (v4, v8) in enumerate(zip([dm64_4[0] if dm64_4 else 0, dm128_4[0] if dm128_4 else 0],
                                   [dm64_8[0] if dm64_8 else 0, dm128_8[0] if dm128_8 else 0])):
    gain = (v8-v4)/max(v4,1)*100 if v4 > 0 else 0
    ax.annotate(f'{gain:+.0f}%', (x_pos[i]+w/2, v8), textcoords='offset points', xytext=(0,5), ha='center', fontsize=7, fontweight='bold')

# Panel B: Epoch count ablation
ax = axes[1]
dm128_e200 = [v['edges'] for v in configs.values() if v['d_model']==128 and v['n_heads']==8 and v['n_epochs']==200]
dm128_e500 = [v['edges'] for v in configs.values() if v['d_model']==128 and v['n_heads']==8 and v['n_epochs']==500]
dm64_e200 = [v['edges'] for v in configs.values() if v['d_model']==64 and v['n_heads']==8 and v['n_epochs']==200]
dm64_e500 = [v['edges'] for v in configs.values() if v['d_model']==64 and v['n_heads']==8 and v['n_epochs']==500]

ax.bar([x-w/2 for x in x_pos], [dm64_e200[0] if dm64_e200 else 0, dm128_e200[0] if dm128_e200 else 0], w, color=colors[2], label='200 epochs', edgecolor='white', linewidth=0.5)
ax.bar([x+w/2 for x in x_pos], [dm64_e500[0] if dm64_e500 else 0, dm128_e500[0] if dm128_e500 else 0], w, color=colors[3], label='500 epochs', edgecolor='white', linewidth=0.5)
ax.set_xticks(x_pos)
ax.set_xticklabels(['d_model=64', 'd_model=128'])
ax.set_ylabel('Edges recovered')
ax.set_title('(b) Epoch count ablation')
ax.legend(fontsize=8)
ax.set_ylim(0, 1200)
for i, (v200, v500) in enumerate(zip([dm64_e200[0] if dm64_e200 else 0, dm128_e200[0] if dm128_e200 else 0],
                                      [dm64_e500[0] if dm64_e500 else 0, dm128_e500[0] if dm128_e500 else 0])):
    gain = (v500-v200)/max(v200,1)*100 if v200 > 0 else 0
    ax.annotate(f'{gain:+.0f}%', (x_pos[i]+w/2, v500), textcoords='offset points', xytext=(0,5), ha='center', fontsize=7, fontweight='bold')

# Panel C: d_model ablation
ax = axes[2]
dm64 = [v['edges'] for v in configs.values() if v['d_model']==64 and v['n_heads']==8 and v['n_epochs']==500]
dm128 = [v['edges'] for v in configs.values() if v['d_model']==128 and v['n_heads']==8 and v['n_epochs']==500]
dm256 = [v['edges'] for v in configs.values() if v['d_model']==256 and v['n_heads']==8 and v['n_epochs']==200]
vals = [dm64[0] if dm64 else 0, dm128[0] if dm128 else 0, dm256[0] if dm256 else 0]
labels = ['64', '128', '256*']
bars = ax.bar(range(3), vals, color=[colors[0], colors[2], colors[1]], edgecolor='white', linewidth=0.5)
ax.set_xticks(range(3))
ax.set_xticklabels(labels)
ax.set_ylabel('Edges recovered')
ax.set_title('(c) d_model ablation')
ax.set_ylim(0, 1200)
for bar, v in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, f'{v:.0f}', ha='center', fontsize=9, fontweight='bold')
ax.text(2, vals[2]+50, '*200 epochs\n(VRAM limited)', ha='center', va='bottom', fontsize=6.5, color='gray')

fig.suptitle('CT Ablation Study at d=200, n=1,000', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()

out_base = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','figures','fig3_ablation')
fig.savefig(out_base + '.png', dpi=300, bbox_inches='tight', pad_inches=0.05)
fig.savefig(out_base + '.pdf', bbox_inches='tight', pad_inches=0.05)
print(f'\nSaved: fig3_ablation.png/pdf')
plt.close()
