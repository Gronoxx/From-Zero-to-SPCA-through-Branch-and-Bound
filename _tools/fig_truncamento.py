#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figura: o mecanismo 'dar o passo e depois truncar' (IHT/potencia truncada), em barras.
4 estagios: x esparso -> passo do gradiente (denso) -> truncar (top-k) -> renormalizar."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ACCENT="#3b54c4"; AMBER="#c2790a"; GREEN="#1f9a55"; SLATE="#5b6573"
DARK="#1f3b6e"; GREY="#b9bec6"; RED="#b23b3b"
BARC=[ACCENT,AMBER,GREEN]
LBL=["$x_1$","$x_2$","$x_3$"]

# estagio 1: x atual, 2-esparso no pedaco {1,2}
x1=np.array([0.83,0.55,0.0])
# estagio 2: x' = x + passo do gradiente (denso) -- ilustrativo
xp=np.array([0.95,0.78,0.40])
# estagio 3: trunca (mantem as 2 maiores em modulo, zera a menor = x3)
xt=np.array([0.95,0.78,0.0])
# estagio 4: renormaliza
xr=xt/np.linalg.norm(xt)

stages=[(x1,"(1) x atual","2 variáveis ligadas\n(no pedaço $\\{x_1,x_2\\}$)",None),
        (xp,"(2) + passo do gradiente","o passo enche TODAS\nas variáveis (fica denso)",None),
        (xt,"(3) trunca (top-$k$)","mantém as $k\\!=\\!2$ maiores\nem módulo, zera o resto",2),
        (xr,"(4) renormaliza","divide por $\\|\\cdot\\|$ ->\nvolta à norma 1",None)]

fig, axes = plt.subplots(1,4, figsize=(13.6,4.4), dpi=200, sharey=True)
plt.subplots_adjust(left=0.05, right=0.985, top=0.80, bottom=0.28, wspace=0.34)

for k,(vec,title,sub,zero_idx) in enumerate(stages):
    ax=axes[k]
    for i in range(3):
        col=BARC[i]
        if zero_idx is not None and i==zero_idx:
            col=GREY
        if k>=3 and i==2:  # x3 ja zerado no estagio 4
            col=GREY
        ax.bar(i, vec[i], width=0.62, color=col, edgecolor="white", linewidth=1.2, zorder=3)
    # destaca o que sera zerado no estagio 3
    if zero_idx is not None:
        ax.bar(zero_idx, xp[zero_idx], width=0.62, color="none",
               edgecolor=RED, linewidth=2.4, ls=(0,(3,2)), zorder=4)
        ax.annotate("zera\n(menor)", (zero_idx, xp[zero_idx]), textcoords="offset points",
                    xytext=(0,6), ha="center", va="bottom", color=RED, fontsize=10, fontweight="bold")
    ax.set_xticks([0,1,2]); ax.set_xticklabels(LBL, fontsize=12)
    ax.set_title(title, fontsize=12, color=DARK, fontweight="bold", pad=8)
    ax.text(0.5, -0.20, sub, transform=ax.transAxes, ha="center", va="top",
            fontsize=9.6, color=SLATE)
    ax.set_ylim(0,1.12)
    ax.spines[["top","right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.18)
axes[0].set_ylabel("valor da componente", fontsize=10.6, color=SLATE)

# setas entre paineis (coordenadas de figura)
ops=["$+\\,\\eta\\nabla f$","manter\ntop-$k$","$\\div\\,\\|\\cdot\\|$"]
for k in range(3):
    xa=0.05+ (k+0.88)*(0.985-0.05)/4
    fig.text(0.05+(k+0.96)*(0.985-0.05)/4, 0.52, "➜", fontsize=26, color=SLATE,
             ha="center", va="center")
    fig.text(0.05+(k+0.96)*(0.985-0.05)/4, 0.63, ops[k], fontsize=11, color=DARK,
             ha="center", va="center", fontweight="bold")

fig.suptitle("O mecanismo “dar o passo e depois truncar” (uma iteração)",
             fontsize=13.5, color=DARK, fontweight="bold", y=0.96)
OUT="/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools/fig_truncamento.png"
fig.savefig(OUT, dpi=200, facecolor="white")
print("salvo:", OUT, "| xr=", np.round(xr,3))
