#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figura: 'na quina, o gradiente PENDE -- nao divide ao meio' (zoom no canto e1).
O gradiente eh UM vetor; a nao-suavidade esta no CONJUNTO VIAVEL (duas tangentes),
entao projetar da DUAS direcoes de descida (o garfo). A diagonal-gradiente eh a
diagonal de um retangulo cujos lados sao as inclinacoes (2,4 e 1,6): so bissecta
o angulo se o retangulo for um quadrado (inclinacoes iguais). Aqui pende para {1,2}."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

ACCENT="#3b54c4"; PURPLE="#7a3fc4"; GREEN="#1f9a55"; SLATE="#5b6573"
DARK="#1f3b6e"; GREY="#9aa0aa"; RED="#b23b3b"; AMBER="#c2790a"

fig, ax = plt.subplots(figsize=(9.0, 7.2), dpi=200)
plt.subplots_adjust(left=0.105, right=0.965, top=0.88, bottom=0.105)

# arcos: dois pedacos que passam por e1 (tangentes e2 e e3), levemente curvos
t=np.linspace(-0.80,0.80,200)
ax.plot(t, -0.20*t**2, color=ACCENT, lw=2.4, zorder=3, alpha=0.95)   # {1,2} ~ horizontal
ax.plot(-0.20*t**2, t, color=PURPLE, lw=2.4, zorder=3, alpha=0.95)   # {1,3} ~ vertical

# gradiente (componentes tangentes em e1) e suas projecoes -> setas de descida
gx,gy = 2.4,1.6; sc=0.26
px, py = gx*sc, gy*sc   # (0.624, 0.416)

# bissetriz de 45 graus (referencia): so coincidiria com o gradiente se as inclinacoes fossem iguais
bl=0.60
ax.plot([0,bl],[0,bl], color=AMBER, lw=1.7, ls=(0,(1,2)), zorder=2)
ax.text(0.50, 0.595, "bissetriz 45°", color=AMBER, fontsize=10.3, fontweight="bold",
        ha="left", va="center", rotation=45, rotation_mode="anchor")

# retangulo: lados = inclinacoes (linhas de projecao)
ax.plot([px,px],[py,0], color=GREY, lw=1.1, ls=":", zorder=2)
ax.plot([px,0],[py,py], color=GREY, lw=1.1, ls=":", zorder=2)
# gradiente (diagonal do retangulo)
ax.annotate("", xy=(px,py), xytext=(0,0),
            arrowprops=dict(arrowstyle="-|>", color=GREY, lw=2.8, ls=(0,(5,3))))
# projecoes (descida em cada pedaco) = os dois lados do retangulo
ax.annotate("", xy=(px,0), xytext=(0,0), arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=3.6))
ax.annotate("", xy=(0,py), xytext=(0,0), arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=3.6))

# arco do angulo real do gradiente (~33,7 graus) entre e2 e a diagonal
ang=np.degrees(np.arctan2(gy,gx))   # 33.69
ax.add_patch(Arc((0,0), width=0.40, height=0.40, angle=0, theta1=0, theta2=ang,
                 color=DARK, lw=1.6, zorder=4))
am=np.radians(ang/2)
ax.text(0.345*np.cos(am), 0.345*np.sin(am), "≈ 33,7°", color=DARK, fontsize=10.6,
        fontweight="bold", ha="left", va="center")

# e1 na origem
ax.scatter([0],[0], s=160, color=RED, zorder=9, edgecolor="white", linewidth=1.8)
ax.annotate("quina $e_1$", xy=(0,0), xytext=(-0.50,-0.50), color=RED, fontsize=12.5,
            fontweight="bold", ha="center", va="center",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))

# rotulos em zonas livres
ax.text(0.66, 0.40, "gradiente\n(UM vetor,\nbem-definido)", color=SLATE,
        fontsize=10.3, ha="left", va="center", fontweight="bold")
ax.text(-0.55, 0.82, "GARFO:\nduas respostas →\nescolher o pedaço",
        fontsize=10.3, color=DARK, fontweight="bold", ha="center", va="center")
ax.text(-0.44, 0.46, "desce no\npedaço $\\{x_1,x_3\\}$\ninclinação = 1,6", color=PURPLE,
        fontsize=10.4, ha="center", va="center", fontweight="bold")
ax.text(0.40, -0.20, "desce no pedaço $\\{x_1,x_2\\}$  ·  inclinação = 2,4", color=ACCENT,
        fontsize=10.6, ha="center", va="center", fontweight="bold")

ax.set_title("Na quina, o gradiente PENDE — não divide ao meio (zoom no canto $e_1$)",
             fontsize=13.2, color=DARK, fontweight="bold", pad=14)
ax.set_xlabel("direção $e_2$  (entrar com a variável 2)", fontsize=10.8, color=SLATE)
ax.set_ylabel("direção $e_3$  (entrar com a variável 3)", fontsize=10.8, color=SLATE)
ax.set_xlim(-0.92,1.06); ax.set_ylim(-0.92,1.06)
ax.axhline(0,color="#dde0e5",lw=1,zorder=1); ax.axvline(0,color="#dde0e5",lw=1,zorder=1)
ax.set_aspect("equal")
ax.grid(alpha=0.12)

OUT="/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools/fig_quina_fork.png"
fig.savefig(OUT, dpi=200, facecolor="white")
print("salvo:", OUT)
