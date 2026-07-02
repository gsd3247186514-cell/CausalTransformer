# -*- coding: utf-8 -*-
"""
Nature journal figure styling — applied globally to all figures.
Usage: at the top of any figure script:
    from nature_style import apply_nature_style
    apply_nature_style()
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ============================================================
# Nature Color Palette (muted, professional, colorblind-friendly)
# ============================================================
N_BLUE   = '#4472C4'
N_ORANGE = '#ED7D31'
N_GREEN  = '#70AD47'
N_RED    = '#C0392B'
N_PURPLE = '#9B59B6'
N_TEAL   = '#17BECF'
N_GRAY   = '#7F8C8D'
N_DARK   = '#2C3E50'
N_WHITE  = '#FFFFFF'
N_BG     = '#FAFAFA'

# Zone colors (lighter for scatter)
ZONE_COLORS = ['#95A5A6', '#E74C3C', '#E67E22', '#2980B9']

# Figure dimensions (Nature double-column: 180mm ~ 7.09 inches)
FIG_W_FULL = 7.09   # 180mm
FIG_H_GOLDEN = 4.4  # ~golden ratio
DPI = 300

def apply_nature_style():
    """Apply Nature journal styling globally."""
    plt.rcParams.update({
        # Font
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'axes.unicode_minus': False,
        # Quality
        'figure.dpi': DPI,
        'savefig.dpi': DPI,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.08,
        # Typography
        'font.size': 8,
        'axes.titlesize': 10,
        'axes.labelsize': 9,
        'xtick.labelsize': 7.5,
        'ytick.labelsize': 7.5,
        'legend.fontsize': 7.5,
        # Lines and markers
        'lines.linewidth': 1.2,
        'lines.markersize': 4,
        # Grid
        'axes.grid': False,
        'grid.alpha': 0.15,
        'grid.linewidth': 0.5,
        # Spines
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.linewidth': 0.8,
        # Background
        'figure.facecolor': N_WHITE,
        'axes.facecolor': N_WHITE,
        'savefig.facecolor': N_WHITE,
    })

def save_nature_figure(fig, basepath):
    """Save figure in both PDF (vector) and PNG (300dpi raster)."""
    for ext in ['pdf', 'png']:
        path = f'{basepath}.{ext}'
        fig.savefig(path, format=ext, dpi=DPI if ext == 'png' else None,
                    bbox_inches='tight', pad_inches=0.08, facecolor=N_WHITE)
        print(f'  Saved: {path}')
    plt.close(fig)
