"""Generate Nature-level graphical abstract for CT paper."""
import sys, os
import sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data'))
from nature_style import apply_nature_style, save_nature_figure, N_BLUE, N_ORANGE, N_GREEN, N_RED, N_PURPLE, N_TEAL, N_GRAY, N_DARK, N_WHITE, FIG_W_FULL, FIG_H_GOLDEN
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

apply_nature_style()

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'figures')
os.makedirs(OUT_DIR, exist_ok=True)

# ── Colors ──
GREEN_ZONE = '#D5F5E3'   # d<200 safe zone
RED_ZONE   = '#FADBD8'   # d=200-500 gap
CT_COLOR   = '#1A5276'   # CT bridge
TEXT_DARK  = '#2C3E50'
FAIL_COLOR = '#E74C3C'
WORK_COLOR = '#27AE60'

# ── 拉大画幅，扩大 Y 轴空间 ──
fig, ax = plt.subplots(1, 1, figsize=(FIG_W_FULL * 1.0, FIG_H_GOLDEN * 0.9))
ax.set_xlim(0, 10)
ax.set_ylim(-0.2, 5.8)  # 核心：把高度从 4.8 提升到 5.8，给所有文字留足呼吸空间
ax.axis('off')

# ── 区域背景框 (整体下压，留出标题高度) ──
zone_y_start = 0.3
zone_height = 4.2  # 比原来 3.9 更高一些

left_zone = FancyBboxPatch((0, zone_y_start), 4.2, zone_height, boxstyle="round,pad=0.15",
                           facecolor=GREEN_ZONE, edgecolor='#A9DFBF', linewidth=1.2, zorder=0)
ax.add_patch(left_zone)

gap_zone = FancyBboxPatch((4.4, zone_y_start), 3.7, zone_height, boxstyle="round,pad=0.15",
                          facecolor=RED_ZONE, edgecolor='#F5B7B1', linewidth=1.2, zorder=0)
ax.add_patch(gap_zone)

ct_zone = FancyBboxPatch((8.3, zone_y_start), 1.5, zone_height, boxstyle="round,pad=0.15",
                         facecolor='#D6EAF8', edgecolor='#85C1E9', linewidth=1.2, zorder=0)
ax.add_patch(ct_zone)

# ── 区域文字标签 (与背景框上边缘拉开 0.2 间距) ──
zone_title_y = zone_y_start + zone_height - 0.2

ax.text(2.1, zone_title_y, r'$\mathbf{d < 200}$', ha='center', va='top',
        fontsize=11, fontweight='bold', color=TEXT_DARK)
ax.text(2.1, zone_title_y - 0.5, 'Existing methods\noperate here', ha='center', va='top',
        fontsize=7.5, color=N_GRAY, linespacing=1.3)

ax.text(6.15, zone_title_y, r'$\mathbf{d = 200{--}500}$', ha='center', va='top',
        fontsize=11, fontweight='bold', color=FAIL_COLOR)
ax.text(6.15, zone_title_y - 0.5, 'THE GAP\nNo DAG method\nproduces any edges', ha='center', va='top',
        fontsize=7.5, color=FAIL_COLOR, linespacing=1.3)

ax.text(9.15, zone_title_y, r'$\mathbf{d \leq 500}$', ha='center', va='top',
        fontsize=11, fontweight='bold', color=CT_COLOR)
ax.text(9.15, zone_title_y - 0.5, 'CT bridges\nthe gap', ha='center', va='top',
        fontsize=7.5, color=CT_COLOR, linespacing=1.3)

# ── 方法框 (整体下移，居中于区域下半部分) ──
method_box_y = 2.7
methods_left = [
    ('NOTEARS', 0.8, method_box_y, WORK_COLOR),
    ('CAGate',  2.0, method_box_y, WORK_COLOR),
    ('SSCAGate',3.2, method_box_y, WORK_COLOR),
]

for name, x, y, color in methods_left:
    box = FancyBboxPatch((x-0.55, y-0.22), 1.1, 0.44, boxstyle="round,pad=0.06",
                         facecolor=color, edgecolor='none', alpha=0.30, zorder=2)
    ax.add_patch(box)
    ax.text(x, y, name, ha='center', va='center', fontsize=7, fontweight='bold',
            color='#1E8449', zorder=3)
    ax.text(x, y-0.48, 'OK', ha='center', va='center', fontsize=10,
            color=WORK_COLOR, fontweight='bold', zorder=3)

# ── 失败方法框 ──
gap_method_box_y = 2.7
gap_labels = [
    ('NOTEARS', 4.95, gap_method_box_y),
    ('CAGate',  6.15, gap_method_box_y),
    ('SSCAGate',7.35, gap_method_box_y),
]
for name, x, y in gap_labels:
    box = FancyBboxPatch((x-0.55, y-0.22), 1.1, 0.44, boxstyle="round,pad=0.06",
                         facecolor='#E0E0E0', edgecolor='none', alpha=0.5, zorder=2)
    ax.add_patch(box)
    ax.text(x, y, name, ha='center', va='center', fontsize=7,
            color='#AAAAAA', zorder=3)
    ax.text(x, y-0.48, '0', ha='center', va='center', fontsize=10,
            color=FAIL_COLOR, fontweight='bold', zorder=3)

# ── CT 框 (右侧) ──
ct_box = FancyBboxPatch((8.55, 2.48), 1.3, 0.44, boxstyle="round,pad=0.06",
                        facecolor=CT_COLOR, edgecolor='none', alpha=0.9, zorder=2)
ax.add_patch(ct_box)
ax.text(9.15, 2.7, 'CT', ha='center', va='center', fontsize=7.5, fontweight='bold',
        color='white', zorder=3)
ax.text(9.15, 2.22, '1,028 edges', ha='center', va='center', fontsize=7.5,
        color=CT_COLOR, fontweight='bold', zorder=3)

# ── 蓝色大箭头 (比之前整体下移) ──
arrow_y = 1.2
ax.annotate('', xy=(9.15, arrow_y), xytext=(0.5, arrow_y),
            arrowprops=dict(arrowstyle='->', color=CT_COLOR, lw=3.5,
                          connectionstyle='arc3,rad=0'),
            zorder=5)

# CT 标签（悬浮在箭头正上方，红色区域中心）
ax.text(6.15, arrow_y + 0.35, 'CAUSAL TRANSFORMER', ha='center', va='bottom',
        fontsize=11, fontweight='bold', color=CT_COLOR, zorder=5,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                  edgecolor=CT_COLOR, linewidth=1.2))

# 箭头下方解释文字（紧贴箭头，红色区域中心）
ax.text(6.15, arrow_y - 0.28, 'Self-attention treats variables as tokens\nMulti-head specialization discovers causal edges',
        ha='center', va='top', fontsize=6.5, color=N_GRAY, zorder=5, linespacing=1.3)

# ── 统计信息框 (移到标题正下方空白区) ──
ax.text(5.05, 4.95, '335 experiments · 7 evidence lines · Consumer GPU · All 5+ seeds',
        ha='center', va='center', fontsize=6.5, color=N_GRAY, fontstyle='italic',
        zorder=5, bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                           edgecolor='#DDDDDD', linewidth=0.5))

# ── 底部坐标轴 ──
ax.plot([0.3, 9.8], [0.55, 0.55], 'k-', lw=0.8, alpha=0.4, zorder=1)

# 刻度标记 (200对齐绿/红分割线4.20, 500对齐红/蓝分割线8.15)
for d_val, x_pos in [(30, 0.8), (50, 1.5), (100, 2.5), (200, 4.20), (300, 5.52), (400, 6.83), (500, 8.15)]:
    ax.plot([x_pos, x_pos], [0.45, 0.65], 'k-', lw=0.6, alpha=0.4, zorder=1)
    ax.text(x_pos, 0.3, str(d_val), ha='center', va='top', fontsize=7.0,
            color=N_GRAY, zorder=2)

# 轴标签
ax.text(5.05, 0.05, r'Number of variables (\(d\))', ha='center', va='top',
        fontsize=8.5, color=N_GRAY, zorder=2)

# ── 区域分割虚线 ──
for x_div, color in [(4.20, '#A9DFBF'), (8.15, '#F5B7B1')]:
    ax.plot([x_div, x_div], [0.7, zone_title_y], '--', color=color, lw=1.0, alpha=0.8, zorder=1)

# ── 顶部标题 ──
ax.text(5.05, 5.6, 'Causal Transformer', ha='center', va='center',
        fontsize=13, fontweight='bold', color=N_DARK, zorder=5)

# ── 保存 ──
basepath = os.path.join(OUT_DIR, 'fig_ga_graphical_abstract')
save_nature_figure(fig, basepath)
print(f'Graphical abstract saved to: {basepath}.pdf / {basepath}.png')
