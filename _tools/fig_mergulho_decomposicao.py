#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figura CONSTRUTIVA: a profundidade de uma bacia e inteiramente montada a partir de Q.
Convencao desta figura: variancia POSITIVA com eixo invertido (vale embaixo), para casar
com os numeros da tabela do texto (2,0 / 2,10 / 1,20 / 3,30).
Painel A: relevo das 3 bacias (e1->e2->e3->e1), cada quina rotulada em Q; na bacia AZUL,
          a decomposicao fundo = meio das pontas + mergulho.
Painel B: contraexemplo -> mesmas pontas (2,0;2,0), acoplamentos 0 vs 1,5 -> fundos diferentes.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ACCENT="#3b54c4"; BLUE="#2f53c0"; AMBER="#c2790a"; PURPLE="#7a3fc4"
GREEN="#1f9a55"; SLATE="#5b6573"; DARK="#1f3b6e"; GREY="#9aa0aa"; RED="#b23b3b"

def br(x, nd=2):
    return ("{:."+str(nd)+"f}").format(x).replace(".", ",")

Q = np.array([[2.0, 1.2, 0.8],
              [1.2, 2.2, 1.0],
              [0.8, 1.0, 1.6]])

def f_arc(i, j, t):            # variancia ao longo do arco {i,j}, t em [0, pi/2]
    c, s = np.cos(t), np.sin(t)
    return Q[i, i]*c*c + Q[j, j]*s*s + 2*Q[i, j]*c*s

def lam_max(qii, qjj, qij):
    return (qii+qjj)/2.0 + np.sqrt(((qii-qjj)/2.0)**2 + qij**2)
def mergulho(qii, qjj, qij):
    return np.sqrt(((qii-qjj)/2.0)**2 + qij**2)

fig, (axA, axB) = plt.subplots(2, 1, figsize=(11.0, 10.8), dpi=200)
plt.subplots_adjust(left=0.105, right=0.965, top=0.955, bottom=0.058, hspace=0.255)

# ===================== Painel A: relevo das 3 bacias + decomposicao ===========
N = 300
S, F, seg = [], [], []
t = np.linspace(0, np.pi/2, N)
S += list(0 + t/(np.pi/2)); F += list(f_arc(0, 1, t)); seg += [0]*N          # {x1,x2}
t = np.linspace(0, np.pi/2, N)
S += list(1 + t/(np.pi/2)); F += list(f_arc(1, 2, t)); seg += [1]*N          # {x2,x3}
t = np.linspace(0, np.pi/2, N)
f2 = Q[2, 2]*np.cos(t)**2 + Q[0, 0]*np.sin(t)**2 + 2*Q[0, 2]*np.cos(t)*np.sin(t)  # {x3,x1}: e3->e1
S += list(2 + t/(np.pi/2)); F += list(f2); seg += [2]*N
S = np.array(S); F = np.array(F); seg = np.array(seg)

cols = [ACCENT, PURPLE, GREEN]
labs = ["bacia $\\{x_1,x_2\\}$", "bacia $\\{x_2,x_3\\}$", "bacia $\\{x_1,x_3\\}$"]
for sid in range(3):
    m = seg == sid
    axA.plot(S[m], F[m], color=cols[sid], lw=3.0, zorder=3, label=labs[sid])

# quinas (cristas) rotuladas em Q: e1->Q11, e2->Q22, e3->Q33
# (alinhamento por quina: e1 nas bordas alinha p/ dentro; e2 sobe acima da linha tracejada)
corners = [(0, "$e_1\\!:\\,Q_{11}=%s$" % br(Q[0,0]), Q[0,0], "left",   (4, 13)),
           (1, "$e_2\\!:\\,Q_{22}=%s$" % br(Q[1,1]), Q[1,1], "center", (0, 18)),
           (2, "$e_3\\!:\\,Q_{33}=%s$" % br(Q[2,2]), Q[2,2], "center", (0, 13)),
           (3, "$e_1$", Q[0,0], "right", (-4, 13))]
for sc, name, fv, hal, off in corners:
    axA.scatter([sc], [fv], s=92, color=RED, zorder=6, edgecolor="white", linewidth=1.4)
    axA.annotate(name, (sc, fv), textcoords="offset points", xytext=off,
                 ha=hal, color=RED, fontsize=10.4, fontweight="bold")

# --- decomposicao na bacia AZUL {x1,x2} (s em [0,1]) ---
qii, qjj, qij = Q[0,0], Q[1,1], Q[0,1]      # 2.0, 2.2, 1.2
meio = (qii+qjj)/2.0                          # 2,10
merg = mergulho(qii, qjj, qij)               # 1,204
mblue = seg == 0
s_bot = S[mblue][np.argmax(F[mblue])]; f_bot = F[mblue].max()   # ~ (0.53, 3.30)

# linha tracejada no "meio das pontas" (para antes de e2; rotulo na faixa vazia do topo)
axA.plot([0, 0.90], [meio, meio], color=SLATE, lw=1.7, ls=(0, (5, 3)), zorder=4)
axA.annotate("meio das pontas:  $(Q_{11}+Q_{22})/2=%s$" % br(meio),
             xy=(0.46, 1.50), fontsize=11.0, color=SLATE, ha="center", va="top")
# seta tracejada vertical = mergulho (do meio ate o fundo; eixo invertido => desce na tela)
axA.annotate("", xy=(s_bot, f_bot), xytext=(s_bot, meio),
             arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=2.6, ls="--"))
# rotulo do mergulho: curto (a formula ja esta na equacao acima), no espaco livre a direita da seta
axA.annotate("mergulho\n$=%s$" % br(merg), xy=(s_bot+0.10, 2.56),
             fontsize=11.0, color=AMBER, ha="left", va="center", fontweight="bold")
# fundo = lambda_max (rotulo na faixa vazia logo abaixo do arco)
axA.scatter([s_bot], [f_bot], s=150, color=AMBER, zorder=7, edgecolor="white", linewidth=1.8)
axA.annotate("fundo $=\\lambda_{\\max}=%s$" % br(f_bot),
             xy=(s_bot, f_bot), textcoords="offset points", xytext=(12, -17),
             fontsize=10.6, color=DARK, ha="left", va="center", fontweight="bold")

axA.set_title("A · O fundo $=$ meio das pontas $+$ mergulho",
              fontsize=11.6, color=DARK, fontweight="bold", pad=10)
axA.set_xlabel("percurso pela borda  $e_1\\!\\to\\!e_2\\!\\to\\!e_3\\!\\to\\!e_1$", fontsize=10.4, color=SLATE)
axA.set_ylabel("variância  $x^{\\top}Qx$", fontsize=10.7, color=SLATE)
axA.set_xlim(-0.12, 3.12); axA.set_xticks([0, 1, 2, 3])
axA.set_xticklabels(["$e_1$", "$e_2$", "$e_3$", "$e_1$"])
axA.set_ylim(1.30, 3.66); axA.invert_yaxis()      # vale (maior variancia) embaixo
axA.annotate("↓ mais fundo = mais variância", xy=(1.5, 3.55),
             fontsize=9.2, color=SLATE, ha="center", va="center")
axA.grid(alpha=0.18)
axA.legend(loc="lower right", fontsize=8.5, framealpha=0.93)

# ===================== Painel B: contraexemplo ================================
pairs = [(2.0, 2.0, 0.0, GREY,   "$Q_{ij}=0$  (arco plano)"),
         (2.0, 2.0, 1.5, ACCENT, "$Q_{ij}=1{,}5$  (bacia funda)")]
offs = [0.0, 2.0]
for (a, b, c, col, top), off in zip(pairs, offs):
    t = np.linspace(0, np.pi/2, N)
    fv = a*np.cos(t)**2 + b*np.sin(t)**2 + 2*c*np.cos(t)*np.sin(t)
    xs = off + t/(np.pi/2)
    axB.plot(xs, fv, color=col, lw=3.2, zorder=3)
    # rotulo do acoplamento no topo do arco
    axB.text(off+0.5, 1.66, top, ha="center", va="top", color=col,
             fontsize=9.6, fontweight="bold")
    # pontas (ambas = 2,0)
    for xc in (off, off+1.0):
        axB.scatter([xc], [a], s=66, color=RED, zorder=6, edgecolor="white", linewidth=1.2)
    # fundo (arco plano: argmax cairia na borda -> forco o centro)
    fundo = lam_max(a, b, c)
    xb = off+0.5 if c == 0 else off + t[np.argmax(fv)]/(np.pi/2)
    axB.scatter([xb], [fv.max()], s=120, color=col, zorder=7, edgecolor="white", linewidth=1.5)
    axB.annotate("fundo $=%s$" % br(fundo), (xb, fv.max()), textcoords="offset points",
                 xytext=(0, -15), ha="center", va="top", color=DARK, fontsize=10.0, fontweight="bold")

# rotulo das pontas (uma vez, no meio entre os dois arcos)
axB.annotate("pontas $=2{,}0$", (1.5, 2.0), textcoords="offset points", xytext=(0, 11),
             ha="center", color=RED, fontsize=9.2, fontweight="bold")

axB.set_title("B · Mesmas pontas, fundos diferentes", fontsize=11.6, color=DARK,
              fontweight="bold", pad=10)
axB.set_xlabel("dois arcos com pontas idênticas  $(2{,}0;\\,2{,}0)$", fontsize=10.4, color=SLATE)
axB.set_ylabel("variância  $x^{\\top}Qx$", fontsize=10.7, color=SLATE)
axB.set_xlim(-0.25, 3.25); axB.set_xticks([])
axB.set_ylim(1.55, 3.92); axB.invert_yaxis()
axB.grid(alpha=0.18)

OUT = "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools/fig_mergulho_decomposicao.png"
fig.savefig(OUT, dpi=200, facecolor="white")
print("salvo:", OUT)
print("  A: meio=%s mergulho=%s fundo(azul)=%s" % (br(meio), br(merg), br(f_bot)))
print("  B: fundo(c=0)=%s  fundo(c=1,5)=%s" % (br(lam_max(2,2,0)), br(lam_max(2,2,1.5))))
