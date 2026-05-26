#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insere a animacao 'montagem por camadas' (normalizacao -> Q -> convivencia) logo apos a
caixa 'Contra-intuicao'. So adiciona conteudo. integrity + diacriticos + cirilico + <letra."""
import re, sys
sys.path.insert(0, "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools")
from al_template import integrity

DOC="/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/02_sparse_pca_o_problema.html"

BLOCK = r"""<p>Para <em>ver</em> as duas camadas se montando, a animação abaixo aplica uma de cada vez: primeiro só a
      normalização (o domínio fica plano), depois liga o \(Q\) aos poucos (o relevo — a inclinação — cresce), e
      no fim mostra os dois convivendo (o garfo na quina). O morfo é exato: \(f_t = (1-t)\cdot 1 + t\,x^\top Q x\),
      que vai da superfície plana (\(t=0\), pois com \(Q=I\) a variância é \(\lVert x\rVert^2=1\) em toda direção)
      até o relevo cheio (\(t=1\)).</p>
      <div class="anim-wrap" id="s2lanim">
        <div class="anim-head">
          <span class="anim-title">Animação interativa — montando as duas camadas, uma de cada vez</span>
          <span class="anim-sub">arraste \(t\) (ou use Aplicar \(Q\)): em \(t=0\) só o domínio (plano, isotrópico); subindo \(t\), o \(Q\) faz o relevo crescer; em \(t=1\), o garfo na quina \(e_1\)</span>
        </div>
        <canvas id="s2lanim-cv" width="720" height="420" aria-label="Animacao em camadas: as superficies dos conjuntos-k planas, depois o Q gerando o relevo, e o garfo na quina"></canvas>
        <div class="anim-ctrl">
          <button id="s2lanim-play" class="anim-btn" type="button">▶ Aplicar Q</button>
          <input id="s2lanim-slider" type="range" min="0" max="1000" value="0" aria-label="Quanto do Q aplicar">
          <span id="s2lanim-t" class="anim-tval">t = 0,00</span>
        </div>
        <div class="anim-hud">
          <div><span class="hud-k">fase</span><span id="s2lanim-fase" class="hud-v" style="font-size:14px">1 · só normalização</span></div>
          <div><span class="hud-k">inclinação {x₁,x₂}</span><span id="s2lanim-sa" class="hud-v">0,0</span></div>
          <div><span class="hud-k">inclinação {x₁,x₃}</span><span id="s2lanim-sb" class="hud-v">0,0</span></div>
        </div>
      </div>
      <style>
        #s2lanim{border:1px solid var(--line);border-radius:16px;background:#fff;
          padding:14px 14px 16px;margin:20px 0;box-shadow:0 3px 14px rgba(20,30,60,.07)}
        #s2lanim .anim-head{display:flex;flex-direction:column;gap:2px;margin-bottom:10px}
        #s2lanim .anim-title{font-weight:800;color:#1a2230;font-size:15px}
        #s2lanim .anim-sub{font-size:12.5px;color:var(--muted);font-style:italic}
        #s2lanim canvas{display:block;width:100%;max-width:720px;height:auto;margin:0 auto;
          background:#fcfcfa;border:1px solid var(--line);border-radius:12px}
        #s2lanim .anim-ctrl{display:flex;align-items:center;gap:12px;margin:12px 2px 0}
        #s2lanim .anim-btn{appearance:none;border:1px solid var(--accent);background:var(--accent);
          color:#fff;font-weight:700;font-size:13.5px;padding:7px 14px;border-radius:9px;cursor:pointer;
          white-space:nowrap;font-family:inherit}
        #s2lanim .anim-btn:hover{filter:brightness(1.06)}
        #s2lanim input[type=range]{flex:1;accent-color:var(--accent);cursor:pointer}
        #s2lanim .anim-tval{font-variant-numeric:tabular-nums;color:#37414f;font-weight:700;
          font-size:13.5px;min-width:74px;text-align:right}
        #s2lanim .anim-hud{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px}
        #s2lanim .anim-hud>div{background:var(--slate-bg);border:1px solid var(--line);border-radius:10px;
          padding:8px 10px;display:flex;flex-direction:column;gap:3px}
        #s2lanim .hud-k{font-size:11.5px;color:var(--muted);letter-spacing:.01em}
        #s2lanim .hud-v{font-size:18px;font-weight:800;color:#1a2230;font-variant-numeric:tabular-nums}
        @media(max-width:560px){#s2lanim .anim-hud{grid-template-columns:1fr}}
      </style>
      <script>
      (function(){
        var cv=document.getElementById('s2lanim-cv'); if(!cv) return;
        var ctx=cv.getContext('2d'); var dpr=window.devicePixelRatio||1;
        var CSSW=720, CSSH=420;
        cv.width=CSSW*dpr; cv.height=CSSH*dpr; ctx.scale(dpr,dpr);
        var ACC='#3b54c4', PUR='#7a3fc4', GRN='#1f9a55', RED='#b23b3b', GREY='#9aa0aa', DARK='#1f3b6e', AMB='#c2790a';
        var Q11=2.0,Q22=2.2,Q33=1.6,Q12=1.2,Q13=0.8,Q23=1.0;
        // percurso e2 -> e1 -> e3 -> e2 (e1 no meio, s=1). A:{1,2}  B:{1,3}  C:{2,3}
        function fQ(s){ s=((s%3)+3)%3; var t,c,n;
          if(s<1){t=s*Math.PI/2;c=Math.cos(t);n=Math.sin(t);return Q22*c*c+Q11*n*n+2*Q12*c*n;}
          else if(s<2){t=(s-1)*Math.PI/2;c=Math.cos(t);n=Math.sin(t);return Q11*c*c+Q33*n*n+2*Q13*c*n;}
          else{t=(s-2)*Math.PI/2;c=Math.cos(t);n=Math.sin(t);return Q33*c*c+Q22*n*n+2*Q23*c*n;} }
        function fT(s,tt){ return (1-tt)*1.0 + tt*fQ(s); }
        var ML=54,MR=16,MT=30,MB=52, PW=CSSW-ML-MR, PH=CSSH-MT-MB;
        var FLO=0.70, FHI=3.5;
        function X(s){return ML+(s/3)*PW;}
        function Y(f){return MT+(1-(f-FLO)/(FHI-FLO))*PH;}
        var COL=[ACC,GRN,PUR];                 // A {1,2}, B {1,3}, C {2,3}
        var SEGLAB=['{x₁,x₂}','{x₁,x₃}','{x₂,x₃}'];
        var CORN=[[0,'e₂'],[1,'e₁'],[2,'e₃'],[3,'e₂']];
        function lab(txt,x,y,color,size,al){ctx.fillStyle=color;
          ctx.font='700 '+(size||12)+'px -apple-system,Segoe UI,Arial';ctx.textAlign=al||'center';
          ctx.textBaseline='alphabetic';ctx.fillText(txt,x,y);}
        function arrow(x0,y0,x1,y1,color,w){ctx.strokeStyle=color;ctx.fillStyle=color;ctx.lineWidth=w;
          ctx.beginPath();ctx.moveTo(x0,y0);ctx.lineTo(x1,y1);ctx.stroke();
          var a=Math.atan2(y1-y0,x1-x0),h=8;ctx.beginPath();ctx.moveTo(x1,y1);
          ctx.lineTo(x1-h*Math.cos(a-0.42),y1-h*Math.sin(a-0.42));
          ctx.lineTo(x1-h*Math.cos(a+0.42),y1-h*Math.sin(a+0.42));ctx.closePath();ctx.fill();}
        function draw(tt){
          ctx.clearRect(0,0,CSSW,CSSH);
          // eixos
          ctx.strokeStyle='#cfd2d8';ctx.lineWidth=1;
          ctx.beginPath();ctx.moveTo(ML,Y(FHI));ctx.lineTo(ML,Y(FLO));ctx.stroke();
          ctx.beginPath();ctx.moveTo(ML,Y(FLO));ctx.lineTo(ML+PW,Y(FLO));ctx.stroke();
          ctx.save();ctx.translate(16,(Y(FHI)+Y(FLO))/2);ctx.rotate(-Math.PI/2);
          lab('variância  f = xᵀQx',0,0,GREY,11,'center');ctx.restore();
          // curva morfada, 3 segmentos
          for(var sid=0;sid<3;sid++){ctx.strokeStyle=COL[sid];ctx.lineWidth=3;ctx.beginPath();var first=true;
            for(var u=0;u<=1.0001;u+=0.004){var ss=sid+u;var px=X(ss),py=Y(fT(ss,tt));
              if(first){ctx.moveTo(px,py);first=false;}else ctx.lineTo(px,py);}
            ctx.stroke();
            lab(SEGLAB[sid],X(sid+0.5),Y(FLO)+34,COL[sid],11);}
          // quinas
          for(var i=0;i<CORN.length;i++){var sc=CORN[i][0];var fv=fT(sc===3?2.9999:sc,tt);
            ctx.fillStyle=RED;ctx.beginPath();ctx.arc(X(sc),Y(fv),5,0,2*Math.PI);ctx.fill();
            ctx.strokeStyle='#fff';ctx.lineWidth=1.4;ctx.stroke();
            lab(CORN[i][1],X(sc),Y(FLO)+18,RED,12);}
          // fase 1: rotulo "superficies planas"
          if(tt<0.04){
            lab('superfícies dos conjuntos-k — planas (isotrópico: toda direção igual)',
                ML+PW/2, Y(1.0)-14, DARK, 12.5);
          }
          // fase 3: garfo na quina e1 (s=1)
          if(tt>0.965){
            var s1=1.0, y1=Y(fT(s1,tt));
            // setas ao longo dos dois arcos (subindo dos dois lados de e1)
            var aL=0.86, aR=1.14;
            arrow(X(s1),y1, X(aL),Y(fT(aL,tt)), ACC, 2.6);   // sobe por {1,2} (esq.)
            arrow(X(s1),y1, X(aR),Y(fT(aR,tt)), GRN, 2.6);   // sobe por {1,3} (dir.)
            lab('sobe a 2,4', X(aL)-4, Y(fT(aL,tt))-9, ACC, 11.5, 'right');
            lab('sobe a 1,6', X(aR)+4, Y(fT(aR,tt))-9, GRN, 11.5, 'left');
            lab('GARFO em e₁: o gradiente pende para o arco mais íngreme  {x₁,x₂}',
                ML+PW/2, MT-12, DARK, 12.5);
          } else if(tt>=0.04){
            lab('ligando o Q: o relevo (a inclinação) cresce', ML+PW/2, MT-12, AMB, 12.5);
          }
        }
        var slider=document.getElementById('s2lanim-slider');
        var playBtn=document.getElementById('s2lanim-play');
        var tEl=document.getElementById('s2lanim-t');
        var faseEl=document.getElementById('s2lanim-fase');
        var saEl=document.getElementById('s2lanim-sa');
        var sbEl=document.getElementById('s2lanim-sb');
        var tt=0, playing=false;
        function f1(v){return v.toFixed(1).replace('.',',');}
        function render(){
          draw(tt);
          tEl.textContent='t = '+tt.toFixed(2).replace('.',',');
          saEl.textContent=f1(tt*2.4); sbEl.textContent=f1(tt*1.6);
          if(tt<0.04){faseEl.textContent='1 · só normalização';}
          else if(tt>0.965){faseEl.textContent='3 · os dois juntos (garfo)';}
          else{faseEl.textContent='2 · aplicando Q';}
        }
        function frame(){
          if(playing){ tt+=0.006; if(tt>=1){tt=1;playing=false;playBtn.textContent='↺ Recomeçar';}
            slider.value=Math.round(tt*1000); }
          render(); requestAnimationFrame(frame);
        }
        slider.addEventListener('input',function(){tt=slider.value/1000;playing=false;
          playBtn.textContent='▶ Aplicar Q';});
        playBtn.addEventListener('click',function(){
          if(tt>=1){tt=0;slider.value=0;} playing=!playing;
          playBtn.textContent=playing?'⏸ Pausar':(tt>=1?'↺ Recomeçar':'▶ Aplicar Q');});
        requestAnimationFrame(frame);
      })();
      </script>
      """

h = open(DOC, encoding="utf-8").read()
anchor = '<p>No fundo, o <strong>algoritmo do gradiente é guloso por natureza</strong>'
assert anchor in h, "ancora nao encontrada"
h2 = h.replace(anchor, BLOCK + anchor, 1)

ok, rep = integrity(h2, 10)
cyr = len(re.findall(r'[Ѐ-ӿ]', h2))
raw_lt = len(re.findall(r'\\\([^\)]*<[a-zA-Z][^\)]*\\\)', h2))
print("integrity:", ok, "| balance:", rep["balance"], "| dollars:", rep["dollars"])
print("cirilico:", cyr, "| <letra em math:", raw_lt)
if ok and cyr==0 and raw_lt==0:
    open(DOC,"w",encoding="utf-8").write(h2); print("ESCRITO")
else:
    print("NAO ESCRITO")
