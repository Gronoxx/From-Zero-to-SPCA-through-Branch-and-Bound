#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s2lanim: no painel 3D, etapa Q passa a LEVANTAR os circulos pela variancia (as 'pontes'
sobre a esfera/dominio) em vez de so colorir. Tambem reduz RR p/ caber. integrity + checagens."""
import re, sys
sys.path.insert(0, "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools")
from al_template import integrity

DOC="/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/02_sparse_pca_o_problema.html"
h=open(DOC, encoding="utf-8").read()
orig=h

# 1) L: reduz RR e adiciona LIFT (as pontes saem ate ~1.46*raio)
h=h.replace("var L={cx:205, cy:212, RR:140};",
            "var L={cx:200, cy:208, RR:115}; var LIFT=0.20;", 1)

# 2) ramo-Q do drawLeft -> pontes (relevo radial), esfera+circulos como dominio, hastes, quinas levantadas
NEWQ = r"""} else {
            // dominio (referencia): circulos sobre a esfera, faint
            for(var pi=0; pi<3; pi++){ var ij=PAIRS[pi]; var N0=64; ctx.strokeStyle='#cbd0d8'; ctx.globalAlpha=0.5; ctx.lineWidth=1; ctx.beginPath(); var ff=true;
              for(var a=0;a<=N0;a++){ var th=a/N0*2*Math.PI; var p=[0,0,0]; p[ij[0]]=Math.cos(th); p[ij[1]]=Math.sin(th);
                var sp=L3(proj(p[0],p[1],p[2])); if(ff){ctx.moveTo(sp[0],sp[1]);ff=false;}else ctx.lineTo(sp[0],sp[1]); }
              ctx.stroke(); }
            ctx.globalAlpha=1;
            // pontes: circulos levantados r = 1 + LIFT*s*(f-1)
            var segs=[], stems=[];
            for(var pi=0; pi<3; pi++){ var ij=PAIRS[pi]; var N=72;
              for(var a=0;a<N;a++){ var t0=a/N*2*Math.PI, t1=(a+1)/N*2*Math.PI;
                var p0=[0,0,0]; p0[ij[0]]=Math.cos(t0); p0[ij[1]]=Math.sin(t0);
                var p1=[0,0,0]; p1[ij[0]]=Math.cos(t1); p1[ij[1]]=Math.sin(t1);
                var f0=ffull(p0[0],p0[1],p0[2]), f1=ffull(p1[0],p1[1],p1[2]);
                var r0=1+LIFT*s*(f0-1), r1=1+LIFT*s*(f1-1);
                var sp0=L3(proj(r0*p0[0],r0*p0[1],r0*p0[2])), sp1=L3(proj(r1*p1[0],r1*p1[1],r1*p1[2]));
                segs.push({a:sp0,b:sp1,d:0.5*(sp0[2]+sp1[2]),f:0.5*(f0+f1)});
                if(a%18===0){ var spb=L3(proj(p0[0],p0[1],p0[2])); stems.push({a:spb,b:sp0,d:sp0[2]}); } } }
            for(var k=0;k<stems.length;k++){var St=stems[k]; ctx.strokeStyle=GREY; ctx.globalAlpha=St.d>=0?0.45:0.16; ctx.lineWidth=1;
              ctx.beginPath(); ctx.moveTo(St.a[0],St.a[1]); ctx.lineTo(St.b[0],St.b[1]); ctx.stroke(); }
            ctx.globalAlpha=1;
            segs.sort(function(p,q){return p.d-q.d;});
            for(var k=0;k<segs.length;k++){var S=segs[k]; var front=S.d>=0;
              ctx.strokeStyle=fcol(S.f, front?1:0.30); ctx.lineWidth=front?3.6:2.0; ctx.lineCap='round';
              ctx.beginPath(); ctx.moveTo(S.a[0],S.a[1]); ctx.lineTo(S.b[0],S.b[1]); ctx.stroke(); }
            ctx.lineCap='butt';
            for(var sgn=-1;sgn<=1;sgn+=2){ for(var e=0;e<3;e++){ var p=[0,0,0]; p[e]=sgn;
              var fq=ffull(p[0],p[1],p[2]); var rq=1+LIFT*s*(fq-1);
              var sp=L3(proj(rq*p[0],rq*p[1],rq*p[2])); var front=sp[2]>=0;
              ctx.fillStyle=RED; ctx.globalAlpha=front?1:0.4;
              ctx.beginPath(); ctx.arc(sp[0],sp[1],front?4.4:2.8,0,2*Math.PI); ctx.fill();
              ctx.strokeStyle='#fff'; ctx.lineWidth=1.2; if(front)ctx.stroke(); } }
            ctx.globalAlpha=1;
            if(s<0.02){ lab('domínio pronto (variância ainda plana)', L.cx, CSSH-16, GRN, 11.5); }
            else { lab('Q levanta a variância → as PONTES sobre a esfera', L.cx, CSSH-28, AMB, 11);
                   lab('fora/âmbar = mais variância · dentro/azul = menos · esfera = domínio', L.cx, CSSH-13, AMB, 9.3); }
          }"""

pat=re.compile(r"\} else \{\s*var segs=\[\];.*?L\.cx, CSSH-16, \(s<0\.02\?GRN:AMB\), 11\.5\);\s*\}", re.DOTALL)
h, n = pat.subn(lambda m: NEWQ, h)
print("ramo-Q substituido:", n)

# 3) sub e aria-label: mencionar as pontes
h=h.replace(
  'aplique uma etapa de cada vez: primeiro a normalização (forma o domínio), depois o \\(Q\\) (gera a inclinação) · arraste para revisar qualquer instante',
  'duas etapas: normalização (forma o domínio) e aplicar \\(Q\\) (a variância) · no 3D o \\(Q\\) levanta a superfície em "pontes" sobre a esfera; no 2D, o mesmo relevo desenrolado', 1)
h=h.replace('a esfera 3D com os 3 circulos formando-se pela normalizacao e colorindo-se pela variancia',
            'a esfera 3D com os 3 circulos formando-se pela normalizacao e levantando-se em pontes pela variancia', 1)

assert n==1 and h!=orig, "alguma substituicao falhou"
ok, rep = integrity(h, 10)
cyr=len(re.findall(r'[Ѐ-ӿ]',h)); raw_lt=len(re.findall(r'\\\([^\)]*<[a-zA-Z][^\)]*\\\)',h))
print("integrity:", ok, "| balance:", rep["balance"], "| dollars:", rep["dollars"], "| cir:", cyr, "| <letra:", raw_lt)
if ok and cyr==0 and raw_lt==0:
    open(DOC,"w",encoding="utf-8").write(h); print("ESCRITO")
else:
    print("NAO ESCRITO")
