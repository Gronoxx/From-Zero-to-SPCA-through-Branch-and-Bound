#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figura (convencao de MINIMIZACAO, g=-x'Qx): o que a quina faz com o gradiente.
Painel A: um pedaco (suporte fixo) -> bacia lisa, minimo interior (descida).
Painel B: a uniao -> 3 bacias separadas por cristas (quinas), gradiente preso num minimo local.
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

def f_arc(i,j,t):
    c,s = np.cos(t), np.sin(t)
    return (Q[i,i]*c*c + Q[j,j]*s*s + 2*Q[i,j]*c*s)
def g_arc(i,j,t):   # objetivo minimizado: g = -f
    return -f_arc(i,j,t)

fig, (axA, axB) = plt.subplots(1, 2, figsize=(13.4, 5.3), dpi=200)
plt.subplots_adjust(left=0.075, right=0.985, top=0.84, bottom=0.16, wspace=0.21)

# ---------------- Painel A: um pedaco {1,2}, theta em [0, pi] ----------------
th = np.linspace(0, np.pi, 600)
gA = g_arc(0,1,th)
axA.plot(np.degrees(th), gA, color=ACCENT, lw=3.0, zorder=3)
# minimo interior (fundo da bacia)
tbot = th[np.argmin(gA)]; gbot = gA.min()
axA.scatter([np.degrees(tbot)],[gbot], s=140, color=AMBER, zorder=6,
            edgecolor="white", linewidth=1.7)
axA.annotate("fundo da bacia (mínimo)\nusa as 2 variáveis",
             xy=(np.degrees(tbot),gbot), xytext=(np.degrees(tbot), gbot+1.22),
             fontsize=10.5, color=DARK, ha="center", va="bottom",
             arrowprops=dict(arrowstyle="->", color=AMBER, lw=2))
# setas de descida dos dois lados (ambas apontam para o fundo)
for t0 in [np.radians(20), np.radians(72)]:
    g0 = g_arc(0,1,t0)
    step = 13 if t0 < tbot else -13
    t1 = np.radians(np.degrees(t0)+step)
    axA.annotate("", xy=(np.degrees(t1), g_arc(0,1,t1)), xytext=(np.degrees(t0), g0),
                 arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.6))
axA.text(95, gA.max()+0.06, "o gradiente desce e PARA no fundo —\nnunca chega às quinas (pontos de eixo)",
         color=GREEN, fontsize=10.2, ha="center", va="bottom", fontweight="bold")
# pontos de eixo (quinas na uniao)
for deg, name in [(0,"$e_1$"),(90,"$e_2$"),(180,"$-e_1$")]:
    gv = g_arc(0,1,np.radians(deg))
    axA.scatter([deg],[gv], s=72, color=RED, zorder=5, marker="o",
                edgecolor="white", linewidth=1.2)
    axA.annotate(name, (deg,gv), textcoords="offset points", xytext=(0,-15),
                 ha="center", color=RED, fontsize=11, fontweight="bold")
axA.set_title("A · Dentro de um pedaço (descida ao mínimo interior, $\\{x_1,x_2\\}$)",
              fontsize=12.2, color=DARK, fontweight="bold", pad=10)
axA.set_xlabel("posição ao longo do circulozinho do pedaço  (ângulo, graus)", fontsize=10.5, color=SLATE)
axA.set_ylabel("objetivo  $-x^{\\top}Qx$  (minimizamos)", fontsize=10.8, color=SLATE)
axA.set_xlim(-6,186); axA.set_xticks([0,45,90,135,180])
axA.set_ylim(gbot-0.55, gA.max()+1.0)   # mais negativo (fundo) embaixo
axA.annotate("↓ mais fundo = mais variância", xy=(150, gbot-0.18),
             fontsize=9.3, color=SLATE, ha="center", va="top")
axA.grid(alpha=0.18)

# ---------------- Painel B: a uniao, perimetro e1->e2->e3->e1 ----------------
N=300
S=[]; G=[]; seg_id=[]
t=np.linspace(0,np.pi/2,N); S+=list(0+t/(np.pi/2)); G+=list(g_arc(0,1,t)); seg_id+=[0]*N
t=np.linspace(0,np.pi/2,N); S+=list(1+t/(np.pi/2)); G+=list(g_arc(1,2,t)); seg_id+=[1]*N
t=np.linspace(0,np.pi/2,N)
g2=-(Q[2,2]*np.cos(t)**2 + Q[0,0]*np.sin(t)**2 + 2*Q[0,2]*np.cos(t)*np.sin(t))
S+=list(2+t/(np.pi/2)); G+=list(g2); seg_id+=[2]*N
S=np.array(S); G=np.array(G); seg_id=np.array(seg_id)

cols=[ACCENT,PURPLE,GREEN]
labs=["pedaço $\\{x_1,x_2\\}$","pedaço $\\{x_2,x_3\\}$","pedaço $\\{x_1,x_3\\}$"]
for sid in range(3):
    m=seg_id==sid
    axB.plot(S[m],G[m], color=cols[sid], lw=3.0, zorder=3, label=labs[sid])

# quinas (cristas) em s=0/3->e1, 1->e2, 2->e3
corners=[(0,"$e_1$",-Q[0,0]),(1,"$e_2$",-Q[1,1]),(2,"$e_3$",-Q[2,2]),(3,"$e_1$",-Q[0,0])]
for sc,name,gv in corners:
    axB.scatter([sc],[gv], s=95, color=RED, zorder=6, edgecolor="white", linewidth=1.4)
    axB.annotate(name,(sc,gv),textcoords="offset points",xytext=(0,13),
                 ha="center",color=RED,fontsize=11,fontweight="bold")
axB.text(2.0, -1.30, "quinas = cristas\n(vincos, não-liso)", color=RED, fontsize=9.4,
         ha="center", va="bottom")

# fundos das bacias (minimos locais)
bots=[]
for sid in range(3):
    m=seg_id==sid
    idx=np.argmin(G[m]); s_b=S[m][idx]; g_b=G[m][idx]; bots.append((s_b,g_b,sid))
    axB.scatter([s_b],[g_b], s=90, color=cols[sid], zorder=6, edgecolor="white", linewidth=1.4)
sg,gg,_=min(bots,key=lambda z:z[1])   # vale mais fundo
axB.annotate("MELHOR GLOBAL\n(vale mais fundo, $\\{x_1,x_2\\}$)", xy=(sg,gg), xytext=(sg-0.05,gg-0.42),
             ha="center", color=DARK, fontsize=10.4, fontweight="bold",
             arrowprops=dict(arrowstyle="->",color=DARK,lw=1.8))

# bolinha presa no fundo da bacia 1 (pedaço {2,3})
sb1=bots[1][0]; gb1=bots[1][1]
s_start=1.16
m1=seg_id==1; ss=S[m1]; gg1=G[m1]
g_start=gg1[np.argmin(np.abs(ss-s_start))]
axB.scatter([s_start],[g_start], s=120, color="#111",
            zorder=8, edgecolor="white", linewidth=1.5)
nA=6; sa=np.linspace(s_start, sb1, nA)
for a in range(nA-1):
    ya=gg1[np.argmin(np.abs(ss-sa[a]))]; yb=gg1[np.argmin(np.abs(ss-sa[a+1]))]
    axB.annotate("",xy=(sa[a+1],yb),xytext=(sa[a],ya),
                 arrowprops=dict(arrowstyle="-|>",color="#111",lw=1.9))
axB.annotate("solta aqui → rola e\nfica PRESO (subótimo)",
             xy=(s_start, g_start-0.05), xytext=(1.24,-1.48),
             ha="center", va="center", color="#111", fontsize=9.8,
             arrowprops=dict(arrowstyle="->",color="#111",lw=1.6))

axB.set_title("B · A união dos pedaços (gradiente preso num mínimo local)",
              fontsize=12.2, color=DARK, fontweight="bold", pad=10)
axB.set_xlabel("percurso pela borda: $e_1\\!\\to\\!e_2\\!\\to\\!e_3\\!\\to\\!e_1$ (3 pedaços emendados)",
               fontsize=10.5, color=SLATE)
axB.set_ylabel("objetivo  $-x^{\\top}Qx$  (minimizamos)", fontsize=10.8, color=SLATE)
axB.set_xlim(-0.1,3.1); axB.set_xticks([0,1,2,3]); axB.set_xticklabels(["$e_1$","$e_2$","$e_3$","$e_1$"])
axB.set_ylim(gg-1.0, -0.85)   # mais negativo (fundo) embaixo
axB.grid(alpha=0.18)
axB.legend(loc="lower right", fontsize=9.0, framealpha=0.92)

OUT="/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools/fig_quina_gradiente.png"
fig.savefig(OUT, dpi=200, facecolor="white")
print("salvo:", OUT, "| fundos (s,g):", [(round(a,2),round(b,2)) for a,b,_ in bots])
