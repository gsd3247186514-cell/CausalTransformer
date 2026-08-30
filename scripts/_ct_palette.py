"""Shared unified high-end palette for the CT paper figures.

Design principle: one cold-primary scheme (blue) for the method under study (CT),
a warm accent for the baseline for contrast, and desaturated neutrals for
context/annotations. This gives all six figures a consistent, journal-grade feel
instead of rainbow defaults.
"""
import matplotlib

# --- Core identity colors ---
CT      = '#1F5C8B'   # deep blue  - the method under study
CT_LT   = '#D7E6F2'   # light blue - CT fill / secondary
NOT  = '#B4513C'      # brick      - NOTEARS baseline (warm contrast)
NOT_LT  = '#F2DDD8'   # light brick- baseline fill
CAG = '#C98A2D'       # amber      - CAGate
CAG_LT  = '#F5E7CD'
SSC = '#4E8770'       # muted green- SSCAGate
SSC_LT  = '#DCEBE4'
GRAY    = '#6B7280'   # neutral gray
GRAY_LT = '#EDEFF2'   # light gray fills
INK     = '#1A1A1A'   # near-black text
MUTED   = '#7A8087'   # muted caption gray

# --- Sequential blue ramp (for 8 attention heads / per-category series) ---
def blue_ramp(n):
    """Return n desaturated grades from deep to light blue."""
    import matplotlib.colors as mcolors
    base = matplotlib.colors.to_rgb(CT)
    ramp = []
    for i in range(n):
        # interpolate toward white-light blue
        t = i / (n - 1) if n > 1 else 0
        r = base[0] + (0.82 - base[0]) * t
        g = base[1] + (0.90 - base[1]) * t
        b = base[2] + (0.96 - base[2]) * t
        ramp.append((r, g, b))
    return ramp

# --- matplotlib style hook ---
def apply_style():
    plt = matplotlib.pyplot
    plt.rcParams.update({
        'font.family': 'DejaVu Sans',
        'font.size': 9.5,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'axes.titleweight': 'bold',
        'axes.edgecolor': INK,
        'axes.labelcolor': INK,
        'xtick.color': '#444A52',
        'ytick.color': '#444A52',
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'axes.grid': True,
        'grid.color': '#D9DDE2',
        'grid.linewidth': 0.6,
        'grid.alpha': 0.8,
        'axes.axisbelow': True,
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'legend.frameon': True,
        'legend.framealpha': 0.9,
        'legend.edgecolor': '#D9DDE2',
        'savefig.dpi': 300,
        'pdf.fonttype': 42,   # embed TrueType for vector PDF text
        'ps.fonttype': 42,
    })

def save(fig, base_path):
    """Save a figure as PNG (300dpi) + vector PDF with tight bbox."""
    import os
    for ext in ('png', 'pdf'):
        p = f'{base_path}.{ext}'
        fig.savefig(p, dpi=300, bbox_inches='tight', pad_inches=0.05,
                    facecolor='white', edgecolor='none')
        sz = os.path.getsize(p) / 1024
        print(f'   saved {os.path.basename(p)}  ({sz:.0f} KB)')
