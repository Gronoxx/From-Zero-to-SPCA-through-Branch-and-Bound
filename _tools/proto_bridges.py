#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prototipo: as 'pontes' = relevo radial da variancia sobre a esfera (Sparse PCA, n=3,k=2).
Cada circulo de coordenadas e levantado por r(theta)=1+alpha*(f-1); a esfera (raio 1) fica
por baixo como dominio. Valida o look antes de portar para a s2lanim (canvas 3D)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ACCENT="#3b54c4"; PURPLE="#7a3fc4"; GREEN="#1f9a55"; RED="#b23b3b"; GREY="#9aa0aa"; DARK="#1f3b6e"
Q = np.array([[2.0,1.2,0.8],[1.2,2.2,1.0],[0.8,1.0,1.6]])
ALPHA=0.22

az, el = np.radians(32), np.radians(24)
Rz=np.array([[np.cos(az),-np.sin(az),0],[np.sin(az),np.cos(az),0],[0,0,1]])
Rx=np.array([[1,0,0],[0,np.cos(el),-np.sin(el)],[0,np.sin(el),np.cos(el)]])
R=Rx@Rz
def proj(p):
    v=R@p; return v[0], v[2], v[1]   # X, Y, depth
def fcolor(val, lo, hi):
    tt=np.clip((val-lo)/(hi-lo+1e-9),0,1)
    c0=np.array([0.23,0.33,0.77]); c1=np.array([0.76,0.47,0.04])
    c=(1-tt)*c0+tt*c1; return (c[0],c[1],c[2])

pairs=[((0,1),ACCENT),((0,2),GREEN),((1,2),PURPLE)]
fall=[]
for (i,j),_ in pairs:
    for t in np.linspace(0,2*np.pi,180):
        x=np.zeros(3); x[i]=np.cos(t); x[j]=np.sin(t); fall.append(x@Q@x)
flo,fhi=min(fall),max(fall)

fig, ax = plt.subplots(figsize=(7.6,7.0), dpi=200)
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.7,1.7); ax.set_ylim(-1.7,1.7)

# esfera (dominio) faint
th=np.linspace(0,2*np.pi,200)
ax.plot(np.cos(th),np.sin(th), color="#dfe3e9", lw=1.2, zorder=1)
# circulos sobre a esfera (dominio) - bem leves
for (i,j),col in pairs:
    pts=[]
    for t in np.linspace(0,2*np.pi,160):
        x=np.zeros(3); x[i]=np.cos(t); x[j]=np.sin(t); X,Y,d=proj(x); pts.append((X,Y,d))
    for k in range(len(pts)-1):
        a=0.5 if pts[k][2]>=0 else 0.18
        ax.plot([pts[k][0],pts[k+1][0]],[pts[k][1],pts[k+1][1]], color="#c8ccd4", lw=0.8, alpha=a, zorder=2)

# pontes: circulos levantados por r=1+alpha*(f-1), colorido por f, com oclusao
segs=[]
for (i,j),col in pairs:
    tt=np.linspace(0,2*np.pi,200)
    for k in range(len(tt)-1):
        x0=np.zeros(3); x0[i]=np.cos(tt[k]); x0[j]=np.sin(tt[k])
        x1=np.zeros(3); x1[i]=np.cos(tt[k+1]); x1[j]=np.sin(tt[k+1])
        f0=x0@Q@x0; f1=x1@Q@x1
        r0=1+ALPHA*(f0-1); r1=1+ALPHA*(f1-1)
        X0,Y0,d0=proj(r0*x0); X1,Y1,d1=proj(r1*x1)
        segs.append(((X0,Y0),(X1,Y1),0.5*(d0+d1),0.5*(f0+f1)))
        # stems (haste) ligando esfera->ponte, esparsos
        if k%20==0:
            Xs,Ys,ds=proj(x0)
            ax.plot([Xs,X0],[Ys,Y0], color=GREY, lw=0.7, alpha=0.4 if d0>=0 else 0.15, zorder=3)
segs.sort(key=lambda s:s[2])
for (A,B,d,f) in segs:
    a=0.97 if d>=0 else 0.28; lw=4.0 if d>=0 else 2.2
    ax.plot([A[0],B[0]],[A[1],B[1]], color=fcolor(f,flo,fhi), lw=lw, alpha=a, solid_capstyle="round", zorder=5)

# quinas levantadas (axis points)
for sgn in (1,-1):
    for e in range(3):
        p=np.zeros(3); p[e]=sgn; fq=p@Q@p; r=1+ALPHA*(fq-1)
        X,Y,d=proj(r*p)
        ax.scatter([X],[Y], s=52 if d>=0 else 24, color=RED, zorder=6,
                   edgecolor="white", linewidth=1.2, alpha=1 if d>=0 else 0.4)

ax.set_title("As 'pontes': a variância como relevo radial sobre a esfera\n(alto = âmbar/para fora · baixo = azul/para dentro · esfera = domínio)",
             fontsize=11.5, color=DARK)
fig.savefig("/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools/proto_bridges.png",
            dpi=200, facecolor="white", bbox_inches="tight")
print("flo,fhi=",round(flo,3),round(fhi,3),"| salvo")
