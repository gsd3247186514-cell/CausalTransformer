"""
Fig 1: Causal Transformer Architecture. Small boxes, long arrows.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

FIG_W = 12.0; FIG_H = 8.5; DPI = 300

C_INPUT='#E8F5E9'; C_EMBED='#BBDEFB'; C_ATTN='#FFE0B2'
C_HEADS=['#FFAB91','#FFCC80','#FFE082','#A5D6A7','#90CAF9','#CE93D8','#EF9A9A','#FFF176']
C_AGG='#C8E6C9'; C_DAG='#F8BBD0'; C_OUT='#D1C4E9'
C_BORDER='#333333'; C_ARROW='#555555'; C_TEXT='#222222'; C_GRAD='#D32F2F'

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, 14); ax.set_ylim(0, 11); ax.axis('off')

def box(ax,x,y,w,h,c,t,s='',fs=9):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.1",
        facecolor=c,edgecolor=C_BORDER,linewidth=1.2,zorder=2))
    ax.text(x+w/2,y+h/2+0.04,t,ha='center',va='center',fontsize=fs,
        fontweight='bold',color=C_TEXT,zorder=3)
    if s:
        ax.text(x+w/2,y+h/2-0.22,s,ha='center',va='center',
            fontsize=fs-2,color='#555555',style='italic',zorder=3)

def arr(ax,x1,y1,x2,y2,c=C_ARROW,lw=1.8):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),
        arrowprops=dict(arrowstyle='->',color=c,lw=lw,
        connectionstyle='arc3,rad=0'),zorder=1)

CX=7.0; BW=2.0; AX=2.7; AW=8.6

# ============================================================
# 1. INPUT (y=9.0, h=0.7)
# ============================================================
box(ax, CX-BW/2, 9.0, BW, 0.7, C_INPUT, 'Input Data Matrix',
    r'$X \in \mathbb{R}^{n \times d}$', fs=9)
arr(ax, CX, 9.0, CX, 7.9)   # span=1.1
ax.text(CX - 0.8, 8.45, "per-variable", va="center", ha="center", fontsize=8.5, color='#333333')

# ============================================================
# 2. VARIABLE EMBEDDING (y=7.2, h=0.7)
# ============================================================
box(ax, CX-BW/2, 7.2, BW, 0.7, C_EMBED, 'Variable Embedding',
    r'$E_i = X_{:,i} \cdot W_{\mathrm{embed}}$', fs=8)
ax.text(CX - 0.8, 6.8, r'$E \in \mathbb{R}^{d \times d_{\mathrm{model}}}$',
    ha='center', fontsize=7, color='#777777', style='italic')
arr(ax, CX, 7.2, CX, 6.0)   # span=1.2
ax.text(CX - 0.8, 6.6, "split", va="center", ha="center", fontsize=8.5, color='#333333')

# ============================================================
# 3. MULTI-HEAD SELF-ATTENTION (y=2.2, h=3.8)
# ============================================================
box(ax, AX, 2.2, AW, 3.8, C_ATTN, '', '', fs=9)
ax.text(CX, 5.8, 'Multi-Head Self-Attention', ha='center',
        fontsize=10, fontweight='bold', color=C_TEXT)
ax.text(CX, 5.35, r'$A^{(h)} = \mathrm{softmax}\!\left(\frac{(E W_Q^{(h)})(E W_K^{(h)})^\top}{\sqrt{d_k}}\right)$',
        ha='center', fontsize=8, color=C_TEXT)

hw=1.6; hgap=0.5; hx0=AX+0.3; hyt=4.2; hyb=3.0
for i in range(8):
    r=0 if i<4 else 1; c=i if i<4 else i-4
    hx=hx0+c*(hw+hgap); hy=hyt if r==0 else hyb
    ax.add_patch(FancyBboxPatch((hx,hy),hw,0.55,boxstyle="round,pad=0.05",
        facecolor=C_HEADS[i],edgecolor=C_BORDER,linewidth=0.8,zorder=3))
    ax.text(hx+hw/2,hy+0.275,f'H{i+1}',ha='center',va='center',
        fontsize=7.5,fontweight='bold',color=C_TEXT,zorder=4)

ax.text(AX+AW-0.5,5.95,'Emergent Specialization\n(H2,H4: neg; H1,H3,H6: pos)',
    ha='right',va='top',fontsize=6.5,color='#E65100',zorder=5,
    bbox=dict(boxstyle='round,pad=0.15',facecolor='#FFF3E0',
    edgecolor='#E65100',alpha=0.85,linewidth=0.6))

# ============================================================
# 4. BOTTOM (y=0.4, h=1.0, gap=2.5)
# ============================================================
BY=0.4; BH=1.0; BW_b=2.0; BGAP=2.5
L_CX=CX-BW_b-BGAP/2; C_CX=CX; R_CX=CX+BW_b+BGAP/2

box(ax, L_CX-BW_b/2, BY, BW_b, BH, C_AGG, '', '', fs=9)
ax.text(L_CX, BY+BH-0.28, 'Head Aggregation', ha='center', fontsize=8, fontweight='bold', color=C_TEXT)
ax.text(L_CX, BY+BH*0.4, r'$W = \sum_h \alpha_h \cdot A^{(h)}$', ha='center', fontsize=7.5, color=C_TEXT)
ax.text(L_CX, BY+0.12, r'$W \in \mathbb{R}^{d \times d}$ (adj)', ha='center',
        fontsize=6.5, color='#666666', style='italic')

box(ax, C_CX-BW_b/2, BY, BW_b, BH, C_DAG, '', '', fs=9)
ax.text(C_CX, BY+BH-0.28, 'DAG Constraint', ha='center', fontsize=8, fontweight='bold', color=C_TEXT)
ax.text(C_CX, BY+BH*0.4, r'$h(W) = \mathrm{tr}(e^{W \odot W}) - d$', ha='center', fontsize=7.5, color=C_TEXT)

box(ax, R_CX-BW_b/2, BY, BW_b, BH, C_OUT, '', '', fs=9)
ax.text(R_CX, BY+BH-0.28, 'Causal Graph', ha='center', fontsize=8, fontweight='bold', color=C_TEXT)
ax.text(R_CX, BY+BH*0.4, r'$\widehat{W}$ (acyclic, DAG)', ha='center', fontsize=7.5, color=C_TEXT)

arr(ax, CX, 2.2, CX, BY+BH)  # span=0.8
ax.text(CX, 2.12, "weighted sum", va="bottom", ha="center", fontsize=8.5, color='#333333')

aly=BY+BH/2
arr(ax, L_CX+BW_b/2+0.05, aly, C_CX-BW_b/2-0.05, aly, lw=2.0)
ax.text((L_CX+BW_b/2+C_CX-BW_b/2)/2, aly+0.38, 'enforce',
        ha='center', va='bottom', fontsize=8.5, color='#333333')
arr(ax, C_CX+BW_b/2+0.05, aly, R_CX-BW_b/2-0.05, aly, lw=2.0)
ax.text((C_CX+BW_b/2+R_CX-BW_b/2)/2, aly+0.38, 'acyclic',
        ha='center', va='bottom', fontsize=8.5, color='#333333')

# ============================================================
# 5. LEFT: Key Innovations
# ============================================================
lx=0.2
ax.add_patch(FancyBboxPatch((lx,7.0),2.1,2.8,boxstyle="round,pad=0.2",
    facecolor='white',edgecolor='#999999',linewidth=0.8,zorder=5))
ax.text(lx+1.05,9.6,'Key Innovations',ha='center',fontsize=9,fontweight='bold',color=C_TEXT,zorder=6)
for i,(t,cl) in enumerate([(n,c) for n,c in zip(
    ['No positional encoding','Permutation-invariant','8 specialized heads',
     '\u2192 Pos/Neg edge experts','DAG penalty $h(W)$','Pairwise gradient signals'],
    ['#666666','#666666','#666666','#E65100','#666666','#666666'])]):
    w='bold' if '\u2192' in t else 'normal'
    ax.text(lx+0.15,9.2-i*0.42,t,fontsize=7.5,color=cl,fontweight=w,zorder=6)

# ============================================================
# 6. RIGHT: Total Loss + Gradient
# ============================================================
loss_x=AX+AW+0.5
ax.add_patch(FancyBboxPatch((loss_x,4.0),1.9,1.3,boxstyle="round,pad=0.12",
    facecolor='#FFF8E1',edgecolor='#F57F17',linewidth=0.8,zorder=5))
ax.text(loss_x+0.95,5.2,'Total Loss',ha='center',fontsize=8,fontweight='bold',color='#E65100',zorder=6)
ax.text(loss_x+0.95,4.8,r'$\mathcal{L} = \frac{1}{2n}\|X-XW\|_F^2$',ha='center',fontsize=6.5,color='#5D4037',zorder=6)
ax.text(loss_x+0.95,4.5,r'$+ \lambda_1\|W\|_1 + \frac{\rho}{2}h(W)^2$',ha='center',fontsize=6.5,color='#5D4037',zorder=6)

# Gradient: Output top → ATTN bottom (short, near-vertical)
ax.annotate('',xy=(AX+AW,2.2),xytext=(R_CX+BW_b/2,BY+BH),
    arrowprops=dict(arrowstyle='->',color=C_GRAD,lw=2.5,linestyle='dashed'),zorder=5)
ax.text(R_CX+BW_b/2+0.6,BY+BH+0.3,'Gradient pathway\n($\\partial\\mathcal{L}/\\partial Q,K$)',
    fontsize=7,color=C_GRAD,va='bottom',ha='left',zorder=5,
    bbox=dict(boxstyle='round,pad=0.1',facecolor='white',edgecolor='none'))

# ============================================================
# TITLE
# ============================================================
ax.text(CX,10.2,'Causal Transformer (CT) Architecture',
    ha='center',fontsize=13,fontweight='bold',color=C_TEXT)

# ============================================================
# SAVE
# ============================================================
out_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','figures')
os.makedirs(out_dir,exist_ok=True)
for fmt in['png','pdf']:
    p=f'{out_dir}/fig1_architecture.{fmt}'
    fig.savefig(p,dpi=DPI,bbox_inches='tight',pad_inches=0.1,facecolor='white',edgecolor='none')
    print(f'Saved: {p} ({os.path.getsize(p)/1024:.0f} KB)')
plt.close()
print('Done.')
