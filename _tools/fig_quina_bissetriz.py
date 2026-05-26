#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figura comparativa: o gradiente bissecta o angulo do garfo SO no caso simetrico.
A diagonal-gradiente eh a diagonal de um retangulo cujos lados sao as inclinacoes ao
longo de cada arco (2*Q1j). Diagonal bissecta o angulo reto <=> retangulo eh quadrado
<=> inclinacoes iguais (Q12=Q13). A esfera ||x||=1 eh IDENTICA nos dois paineis (mesmo
arco pontilhado): quem cria a assimetria eh o Q, nao a normalizacao."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

ACCENT="#3b54c4"; PURPLE="#7a3fc4"; GREEN="#1f9a55"; SLATE="#5b6573"
DARK="#1f3b6e"; GREY="#9aa0aa"; RED="#b23b3b"; AMBER="#c2790a"

SC=0.30          # px por unidade de inclinacao
R=0.82           # raio do quarto de circulo ||x||=1 (igual nos dois paineis)

def br(v):
    return ("%.1f" % v).replace(".", ",")

def panel(ax, sA, sB, title, sym):
    px, py = sA*SC, sB*SC
    # arcos (tangentes e2, e3) -- IDENTICOS nos dois paineis
    t=np.linspace(-0.18,0.96,160)
    ax.plot(t, -0.11*t**2, color=ACCENT, lw=2.2, zorder=3, alpha=0.95)
    ax.plot(-0.11*t**2, t, color=PURPLE, lw=2.2, zorder=3, alpha=0.95)
    # quarto de circulo ||x||=1 (mesmo raio nos dois)
    th=np.linspace(0, np.pi/2, 120)
    ax.plot(R*np.cos(th), R*np.sin(th), color=GREY, lw=1.2, ls=(0,(2,2)), zorder=2, alpha=0.8)
    # bissetriz 45 graus
    ax.plot([0,0.66],[0,0.66], color=AMBER, lw=1.6, ls=(0,(1,2)), zorder=2)
    # retangulo (lados = inclinacoes)
    ax.plot([px,px],[py,0], color=GREY, lw=1.0, ls=":", zorder=2)
    ax.plot([px,0],[py,py], color=GREY, lw=1.0, ls=":", zorder=2)
    # gradiente (diagonal)
    ax.annotate("", xy=(px,py), xytext=(0,0),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=2.6, ls=(0,(5,3))))
    # projecoes (lados do retangulo)
    ax.annotate("", xy=(px,0), xytext=(0,0), arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=3.3))
    ax.annotate("", xy=(0,py), xytext=(0,0), arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=3.3))
    # rotulos das inclinacoes
    ax.text(px/2, -0.075, br(sA), color=ACCENT, fontsize=11, ha="center", va="center", fontweight="bold")
    ax.text(-0.075, py/2, br(sB), color=PURPLE, fontsize=11, ha="center", va="center", fontweight="bold")
    # arco do angulo
    ang=np.degrees(np.arctan2(sB,sA))
    ax.add_patch(Arc((0,0), width=0.34, height=0.34, angle=0, theta1=0, theta2=ang,
                     color=DARK, lw=1.5, zorder=4))
    am=np.radians(ang/2)
    if sym:
        ax.text(0.31*np.cos(am), 0.31*np.sin(am)+0.02, "45°", color=GREEN, fontsize=11,
                fontweight="bold", ha="left", va="center")
        ax.text(px+0.02, py+0.03, "bissecta ✓", color=GREEN, fontsize=11.2, fontweight="bold",
                ha="left", va="bottom")
    else:
        ax.text(0.30*np.cos(am), 0.30*np.sin(am), "%s°" % br(ang), color=DARK, fontsize=11,
                fontweight="bold", ha="left", va="center")
        ax.text(px+0.02, py+0.03, "pende para\n$\\{x_1,x_2\\}$", color=RED, fontsize=11.2,
                fontweight="bold", ha="left", va="bottom")
    # e1
    ax.scatter([0],[0], s=120, color=RED, zorder=9, edgecolor="white", linewidth=1.6)
    ax.set_title(title, fontsize=12.3, color=DARK, fontweight="bold", pad=10)
    ax.set_xlim(-0.30,1.06); ax.set_ylim(-0.30,1.06)
    ax.axhline(0,color="#dde0e5",lw=1,zorder=1); ax.axvline(0,color="#dde0e5",lw=1,zorder=1)
    ax.set_aspect("equal"); ax.grid(alpha=0.11)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("direção $e_2$", fontsize=10.2, color=SLATE)
    ax.set_ylabel("direção $e_3$", fontsize=10.2, color=SLATE)

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.5, 5.4), dpi=200)
plt.subplots_adjust(left=0.05, right=0.975, top=0.80, bottom=0.10, wspace=0.13)

panel(axL, 2.0, 2.0, "Simétrico ($Q_{12}=Q_{13}$): retângulo é quadrado", sym=True)
panel(axR, 2.4, 1.6, "Assimétrico ($Q_{12}>Q_{13}$): retângulo deitado", sym=False)

# rotulo do circulo (so no painel esquerdo, em zona livre)
axL.text(0.60, 0.86, "círculo $\\|x\\|=1$\n(idêntico nos dois)", color=SLATE, fontsize=9.6,
         ha="left", va="center", style="italic")

fig.suptitle("A diagonal só corta o ângulo ao meio se o retângulo for um QUADRADO (inclinações iguais)",
             fontsize=13.5, color=DARK, fontweight="bold", y=0.965)

OUT="/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools/fig_quina_bissetriz.png"
fig.savefig(OUT, dpi=200, facecolor="white")
print("salvo:", OUT)
