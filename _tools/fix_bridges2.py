#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s2lanim: cor das pontes 3D passa a ser POR PEDACO (igual ao 2D) em vez de por variancia;
variancia fica codificada so pela altura (raio). Aplica as 2 ressalvas do especialista nas legendas."""
import re, sys
sys.path.insert(0, "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools")
from al_template import integrity

DOC="/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/02_sparse_pca_o_problema.html"
h=open(DOC, encoding="utf-8").read(); orig=h

reps = [
 # 1) seg carrega a cor do pedaco
 ("segs.push({a:sp0,b:sp1,d:0.5*(sp0[2]+sp1[2]),f:0.5*(f0+f1)});",
  "segs.push({a:sp0,b:sp1,d:0.5*(sp0[2]+sp1[2]),c:PCOL[pi]});"),
 # 2) desenha com a cor do pedaco (alpha via globalAlpha) em vez de fcol(variancia)
 ("ctx.strokeStyle=fcol(S.f, front?1:0.30); ctx.lineWidth=front?3.6:2.0; ctx.lineCap='round';",
  "ctx.globalAlpha=(front?1:0.30); ctx.strokeStyle=S.c; ctx.lineWidth=front?3.6:2.0; ctx.lineCap='round';"),
 # 3) legenda linha 1: cor = pedaco
 ("lab('Q levanta a variância → as PONTES sobre a esfera', L.cx, CSSH-28, AMB, 11);",
  "lab('Q levanta a variância → as PONTES (cor = pedaço, como no 2D)', L.cx, CSSH-28, DARK, 10.5);"),
 # 4) legenda linha 2: ressalva (dentro = ainda viavel; esfera = raio f=1)
 ("lab('fora/âmbar = mais variância · dentro/azul = menos · esfera = domínio', L.cx, CSSH-13, AMB, 9.3);",
  "lab('fora = mais variância · dentro = menos (ainda viável; esfera = raio f=1)', L.cx, CSSH-13, GREY, 9.0);"),
 # 5) sub: 'superficie' -> 'curvas (relevo radial)'
 ('levanta a superfície em "pontes" sobre a esfera',
  'levanta as curvas em "pontes" (relevo radial da variância)'),
]
for old,new in reps:
    c=h.count(old); assert c==1, "esperado 1 para %r, achei %d" % (old[:40], c)
    h=h.replace(old,new,1)

ok, rep = integrity(h, 11)
cyr=len(re.findall(r'[Ѐ-ӿ]',h)); raw_lt=len(re.findall(r'\\\([^\)]*<[a-zA-Z][^\)]*\\\)',h))
print("integrity:", ok, "| balance:", rep["balance"], "| dollars:", rep["dollars"], "| cir:", cyr, "| <letra:", raw_lt)
if ok and cyr==0 and raw_lt==0 and h!=orig:
    open(DOC,"w",encoding="utf-8").write(h); print("ESCRITO")
else:
    print("NAO ESCRITO")
