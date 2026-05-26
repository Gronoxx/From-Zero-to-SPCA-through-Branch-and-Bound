#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prototipo: valida a projecao ortografica da esfera unitaria com os 3 circulos de
coordenadas (conjuntos-k), oclusao frente/tras, e coloracao por f=x'Qx. So para VER o
look antes de portar para o canvas."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

ACCENT="#3b54c4"; PURPLE="#7a3fc4"; GREEN="#1f9a55"; RED="#b23b3b"; GREY="#9aa0aa"; DARK="#1f3b6e"

Q = np.array([[2.0,1.2,0.8],[1.2,2.2,1.0],[0.8,1.0,1.6]])

# rotacao de visualizacao (iso): Rz(az) depois Rx(el)
az, el = np.radians(32), np.radians(24)
Rz = np.array([[np.cos(az),-np.sin(az),0],[np.sin(az),np.cos(az),0],[0,0,1]])
Rx = np.array([[1,0,0],[0,np.cos(el),-np.sin(el)],[0,np.sin(el),np.cos(el)]])
R = Rx @ Rz
def proj(p):           # retorna (X, Y, depth) ; +depth = mais perto do observador
    v = R @ p
    return v[0], v[2], v[1]   # olha de "cima/frente": usa x->X, z->Y, y->profundidade

# cor por valor f em [fmin,fmax] -> azul(baixo)->ambar(alto)
def fcolor(val, lo, hi):
    tt = np.clip((val-lo)/(hi-lo+1e-9), 0, 1)
    c0 = np.array([0.18,0.33,0.77]); c1 = np.array([0.86,0.47,0.04])  # accent->amber
    c = (1-tt)*c0 + tt*c1
    return (c[0],c[1],c[2])

pairs = [((0,1),"{1,2}"),((0,2),"{1,3}"),((1,2),"{2,3}")]
fall = []
for (i,j),_ in pairs:
    th=np.linspace(0,2*np.pi,180)
    for t in th:
        x=np.zeros(3); x[i]=np.cos(t); x[j]=np.sin(t)
        fall.append(x@Q@x)
flo, fhi = min(fall), max(fall)

fig, axs = plt.subplots(1,2, figsize=(12,6), dpi=200)
for ax in axs: ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.4,1.4); ax.set_ylim(-1.4,1.4)

# ---------- painel A: normalizacao (pontos varios raios -> raio 1) ----------
axA=axs[0]
rng=np.random.default_rng(3)
# silhueta da esfera
th=np.linspace(0,2*np.pi,200); axA.plot(np.cos(th),np.sin(th), color="#d8dbe0", lw=1.2)
for (i,j),lab in pairs:
    col={ "{1,2}":ACCENT,"{1,3}":GREEN,"{2,3}":PURPLE }[lab]
    angs=np.linspace(0,2*np.pi,17)[:-1]
    for a in angs:
        r=rng.uniform(0.45,1.5)
        x=np.zeros(3); x[i]=np.cos(a); x[j]=np.sin(a)
        X,Y,d=proj(r*x)
        axA.scatter([X],[Y], s=14, color=col, alpha=0.85 if d>=0 else 0.30, zorder=3 if d>=0 else 1)
axA.set_title("Aplicar normalização: pontos em vários raios →\n(animariam) para raio 1, formando os 3 círculos", fontsize=11, color=DARK)

# ---------- painel B: normalizado + Q (circulos coloridos por f, oclusao) ----------
axB=axs[1]
axB.plot(np.cos(th),np.sin(th), color="#e2e5ea", lw=1.0)
for (i,j),lab in pairs:
    t=np.linspace(0,2*np.pi,200)
    pts=[]; cols=[]; depths=[]
    for k in range(len(t)-1):
        x0=np.zeros(3); x0[i]=np.cos(t[k]); x0[j]=np.sin(t[k])
        x1=np.zeros(3); x1[i]=np.cos(t[k+1]); x1[j]=np.sin(t[k+1])
        X0,Y0,d0=proj(x0); X1,Y1,d1=proj(x1)
        fmid=0.5*((x0@Q@x0)+(x1@Q@x1))
        pts.append([(X0,Y0),(X1,Y1)]); cols.append(fcolor(fmid,flo,fhi)); depths.append(0.5*(d0+d1))
    # desenha tras primeiro (alpha menor), frente depois
    order=np.argsort(depths)
    for k in order:
        a=0.95 if depths[k]>=0 else 0.28
        lw=3.4 if depths[k]>=0 else 2.0
        (X0,Y0),(X1,Y1)=pts[k]
        axB.plot([X0,X1],[Y0,Y1], color=cols[k], lw=lw, alpha=a, solid_capstyle="round")
# quinas (axis points)
for s in [1,-1]:
    for e in np.eye(3):
        X,Y,d=proj(s*e)
        axB.scatter([X],[Y], s=46 if d>=0 else 22, color=RED, zorder=6,
                    edgecolor="white", linewidth=1.2, alpha=1 if d>=0 else 0.4)
axB.set_title("Aplicar Q: os 3 círculos coloridos pela variância f\n(azul=baixa, âmbar=alta) — a inclinação aparece", fontsize=11, color=DARK)

fig.savefig("/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools/proto_sphere3d.png",
            dpi=200, facecolor="white", bbox_inches="tight")
print("flo,fhi=",round(flo,3),round(fhi,3),"salvo")
