#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""#s2tanim v3: DOIS paineis lado a lado + passos discretos de IHT.
ESQUERDA: barras em etapas (estado -> passo denso x+eta*2Qx (x1 dispara) -> trunca).
DIREITA: relevo/bacia (3 morros, perimetro e2->e3->e1->e2 com e1 no centro); o marcador
salta entre {x1,x3} e {x1,x2} e trava no morro {x1,x2}, sem nunca subir o morro {x2,x3}
(o mais alto = otimo). Torna visivel POR QUE x1 nao eh largado (gradiente denso grande em x1)."""
import re, sys
sys.path.insert(0, "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools")
from al_template import integrity

DOC = "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/02_sparse_pca_o_problema.html"
html = open(DOC, encoding="utf-8").read()

def rep1(pattern, repl, flags=0):
    global html
    new, n = re.subn(pattern, lambda m: repl, html, flags=flags)
    assert n == 1, ("regex falhou (n=%d): %s" % (n, pattern[:55]))
    html = new

MARKUP = r"""<div class="anim-wrap" id="s2tanim">
        <div class="anim-head">
          <span class="anim-title">Animação interativa — passo+trunca, passo a passo: barras (mecanismo) + relevo (bacia)</span>
          <span class="anim-sub">Clique <strong>próximo passo</strong> para rodar o ciclo discreto. ESQUERDA: o <em>passo denso</em> \(x+\eta\,2Qx\) enche as barras (a de \(x_1\) <em>dispara</em>, pois sua variância é a maior — por isso ela sempre sobrevive ao truncamento) e depois o <em>truncamento</em> zera a menor. DIREITA: o relevo das bacias; o iterado <strong>salta</strong> entre os morros \(\{x_1,x_3\}\) e \(\{x_1,x_2\}\) e <strong>trava</strong> ali — nunca sobe o morro mais alto \(\{x_2,x_3\}\) (o ótimo), porque chegar nele exigiria largar \(x_1\).</span>
        </div>
        <canvas id="s2tanim-cv" width="820" height="392" aria-label="Dois paineis: barras do passo denso e truncamento a esquerda; relevo das bacias com o iterado saltando entre dois morros e travando sem alcancar o morro mais alto a direita"></canvas>
        <div class="anim-ctrl">
          <button id="s2tanim-step" class="anim-btn" type="button">▶ próximo passo</button>
          <button id="s2tanim-auto" class="anim-btn" type="button">▶▶ rodar</button>
          <button id="s2tanim-reset" class="anim-btn" type="button">↺ reiniciar</button>
          <span id="s2tanim-phase" class="anim-tval">rodada 1 · estado</span>
        </div>
        <div class="anim-hud">
          <div><span class="hud-k">suporte (passo+trunca)</span><span id="s2tanim-sup" class="hud-v">{x1,x3}</span></div>
          <div><span class="hud-k">λ vs ótimo {x2,x3}=3,73</span><span id="s2tanim-var" class="hud-v">3,17</span></div>
          <div><span class="hud-k">o que aconteceu</span><span id="s2tanim-jump" class="hud-v">14% abaixo</span></div>
        </div>
      </div>
      """
rep1(r'<div class="anim-wrap" id="s2tanim">.*?</div>\s*(?=<p><strong>Moral\.)', MARKUP, flags=re.DOTALL)

JS = r"""<script>
      (function(){
        var cv=document.getElementById('s2tanim-cv'); if(!cv) return;
        var ctx=cv.getContext('2d'); var dpr=window.devicePixelRatio||1;
        var CSSW=820, CSSH=392; cv.width=CSSW*dpr; cv.height=CSSH*dpr; ctx.scale(dpr,dpr);
        var ACC='#3b54c4', PUR='#7a3fc4', GREEN='#1f9a55', GREY='#b9bec6', DARK='#1f3b6e', RED='#b23b3b', AMBER='#c2790a';
        var Q=[[3.219,0.875,-0.043],[0.875,1.768,1.236],[-0.043,1.236,2.952]];
        var ETA=0.4, NAMES=['x1','x2','x3'], COLS=[ACC,PUR,GREEN];
        function mv(x){var r=[0,0,0];for(var i=0;i<3;i++){for(var j=0;j<3;j++){r[i]+=Q[i][j]*x[j];}}return r;}
        function norm(x){var s=Math.hypot(x[0],x[1],x[2]);return [x[0]/s,x[1]/s,x[2]/s];}
        function top2(v){var idx=[0,1,2].sort(function(a,b){return Math.abs(v[b])-Math.abs(v[a]);});return [idx[0],idx[1]].sort(function(a,b){return a-b;});}
        function fval(x){var r=mv(x);return x[0]*r[0]+x[1]*r[1]+x[2]*r[2];}
        function fmt(x){return x.toFixed(2).replace('.',',');}
        function supName(k){return '{'+NAMES[k[0]]+','+NAMES[k[1]]+'}';}
        // ---- RELEVO: perimetro e2->e3->e1->e2 (e1 no centro), s em [0,3] ----
        function fperim(s){ s=((s%3)+3)%3; var t,c,n;
          if(s<1){ t=s*Math.PI/2; c=Math.cos(t); n=Math.sin(t); return Q[1][1]*c*c+Q[2][2]*n*n+2*Q[1][2]*c*n; }      // e2->e3 {x2,x3}
          if(s<2){ t=(s-1)*Math.PI/2; c=Math.cos(t); n=Math.sin(t); return Q[2][2]*c*c+Q[0][0]*n*n+2*Q[0][2]*c*n; }  // e3->e1 {x1,x3}
          t=(s-2)*Math.PI/2; c=Math.cos(t); n=Math.sin(t); return Q[0][0]*c*c+Q[1][1]*n*n+2*Q[0][1]*c*n; }            // e1->e2 {x1,x2}
        function sOf(x){var k=top2(x);
          if(k[0]===1&&k[1]===2) return Math.atan2(Math.abs(x[2]),Math.abs(x[1]))/(Math.PI/2);        // {x2,x3} seg0
          if(k[0]===0&&k[1]===2) return 1+Math.atan2(Math.abs(x[0]),Math.abs(x[2]))/(Math.PI/2);      // {x1,x3} seg1
          return 2+Math.atan2(Math.abs(x[1]),Math.abs(x[0]))/(Math.PI/2); }                            // {x1,x2} seg2
        // morros (picos) por amostragem
        var peaks=[]; for(var seg=0;seg<3;seg++){var bf=-1,bs=seg+0.5; for(var u=0.001;u<0.999;u+=0.002){var ss=seg+u,ff=fperim(ss); if(ff>bf){bf=ff;bs=ss;}} peaks.push([bs,bf]);}
        // peaks[0]={x2,x3}(OTIMO), peaks[1]={x1,x3}, peaks[2]={x1,x2}
        var LOPT=peaks[0][1];
        // ---- layout ----
        var BX=[112,205,298], BW=66, BY0=300, FULL=3.85;     // barras (esq): escala fixa -> passo denso "incha"
        var RX0=420, RX1=792, RY0=96, RY1=300, FLO=1.5, FHI=3.95;
        function X(s){return RX0+(s/3)*(RX1-RX0);}
        function Yv(f){return RY1-(f-FLO)/(FHI-FLO)*(RY1-RY0);}
        function label(t,x,y,col,sz,al){ctx.save();ctx.fillStyle=col;ctx.font=(sz||13)+'px -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);ctx.restore();}
        function labelB(t,x,y,col,sz,al){ctx.save();ctx.fillStyle=col;ctx.font='700 '+(sz||13)+'px -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif';ctx.textAlign=al||'left';ctx.fillText(t,x,y);ctx.restore();}
        // ---- estado ----
        var X0=norm([1,0,0.35]), x=X0.slice(), it=1, phase=0, xp=null, kept=null, xnext=null, done=false, hist=[], auto=false, tlast=0;
        var stepBtn=document.getElementById('s2tanim-step'), autoBtn=document.getElementById('s2tanim-auto'),
            resetBtn=document.getElementById('s2tanim-reset'), phEl=document.getElementById('s2tanim-phase'),
            supEl=document.getElementById('s2tanim-sup'), varEl=document.getElementById('s2tanim-var'), jumpEl=document.getElementById('s2tanim-jump');
        function reset(){x=X0.slice();it=1;phase=0;xp=null;kept=null;xnext=null;done=false;hist=[sOf(x)];auto=false;autoBtn.textContent='▶▶ rodar';}
        function advance(){
          if(done) return;
          if(phase===0){ var g=mv(x); xp=[x[0]+ETA*2*g[0],x[1]+ETA*2*g[1],x[2]+ETA*2*g[2]]; phase=1; }
          else if(phase===1){ kept=top2(xp); var xt=[0,0,0]; xt[kept[0]]=xp[kept[0]]; xt[kept[1]]=xp[kept[1]]; xnext=norm(xt); phase=2; }
          else { x=xnext.slice(); hist.push(sOf(x)); it++; phase=0; if(it>6) done=true; }
        }
        function drawBars(){
          var vec, showDrop=false, dropIdx=-1, dense=(phase>=1);
          if(phase===0){ vec=x; } else { vec=xp; }
          if(phase===2){ showDrop=true; dropIdx=(kept.indexOf(0)<0?0:(kept.indexOf(1)<0?1:2)); }
          labelB('Barras: o mecanismo (1 passo)', 52, 40, DARK, 14);
          var phn=(phase===0?'estado atual (2 variáveis)':(phase===1?'passo denso: x + η·2Qx (enche tudo)':'trunca: mantém as 2 maiores, zera a menor'));
          label(phn, 52, 60, (phase===1?AMBER:(phase===2?RED:DARK)), 12.5);
          ctx.strokeStyle='#cfd2d8'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(72,BY0); ctx.lineTo(338,BY0); ctx.stroke();
          for(var b=0;b<3;b++){
            var h=Math.abs(vec[b])/FULL*(BY0-96), drop=(showDrop&&b===dropIdx);
            var col=drop?GREY:(dense?COLS[b]:(Math.abs(vec[b])<1e-6?GREY:COLS[b]));   // fase0: a componente nula fica cinza
            ctx.fillStyle=col; ctx.fillRect(BX[b]-BW/2,BY0-h,BW,h);
            if(drop){ ctx.strokeStyle=RED; ctx.setLineDash([4,3]); ctx.strokeRect(BX[b]-BW/2,BY0-h,BW,h); ctx.setLineDash([]); labelB('zera',BX[b],BY0-h-7,RED,11.5,'center'); }
            labelB(NAMES[b],BX[b],BY0+18,DARK,14,'center'); label('var '+fmt(Q[b][b]),BX[b],BY0+34,'#6b7280',11.5,'center');
          }
          if(phase>=1){ labelB('x1 dispara',BX[0],BY0-Math.abs(vec[0])/FULL*(BY0-96)-10,ACC,12,'center'); label('(maior variância → ∇f grande)',195,82,ACC,11,'center'); }
        }
        function drawRelief(){
          labelB('Relevo: as bacias (a consequência)', 412, 40, DARK, 14);
          // eixos
          ctx.strokeStyle='#cfd2d8'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(RX0-8,RY1); ctx.lineTo(RX1+4,RY1); ctx.stroke();
          // curva do relevo
          ctx.strokeStyle=ACC; ctx.lineWidth=2.4; ctx.beginPath();
          for(var s=0;s<=3.0001;s+=0.01){var xx=X(s),yy=Yv(fperim(s)); if(s===0)ctx.moveTo(xx,yy); else ctx.lineTo(xx,yy);} ctx.stroke();
          // cantos e2,e3,e1,e2
          var corners=[[0,'e2'],[1,'e3'],[2,'e1'],[3,'e2']];
          for(var ci=0;ci<corners.length;ci++){var cs=corners[ci][0]; ctx.fillStyle='#9aa0aa'; ctx.beginPath(); ctx.arc(X(cs),Yv(fperim(cs)),2.5,0,2*Math.PI); ctx.fill();
            label(corners[ci][1],X(cs),RY1+16,'#6b7280',11,'center');}
          // morros: {x2,x3}=otimo (verde, NUNCA), {x1,x3} e {x1,x2}
          var pnames=['{x2,x3}','{x1,x3}','{x1,x2}'];
          for(var p=0;p<3;p++){var ps=peaks[p][0],pf=peaks[p][1],isopt=(p===0);
            ctx.fillStyle=isopt?GREEN:'#7a8088'; ctx.beginPath(); ctx.arc(X(ps),Yv(pf),isopt?6:4,0,2*Math.PI); ctx.fill();
            if(isopt){ ctx.strokeStyle=GREEN; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(X(ps),Yv(pf),10,0,2*Math.PI); ctx.stroke();
              labelB('ótimo '+pnames[p],X(ps),Yv(pf)-16,GREEN,12,'center'); label('(exige largar x1: NUNCA)',X(ps),Yv(pf)-2,GREEN,10.5,'center'); }
            else { label(pnames[p]+' '+fmt(pf),X(ps),Yv(pf)-9,'#5b6573',10.5,'center'); }
          }
          // trilha (posicoes passadas)
          for(var hI=0;hI<hist.length;hI++){var hs=hist[hI]; ctx.fillStyle='rgba(178,59,59,.25)'; ctx.beginPath(); ctx.arc(X(hs),Yv(fperim(hs)),3,0,2*Math.PI); ctx.fill();}
          // marcador atual (no estado x; na fase trunca, ja no xnext)
          var cur=(phase===2?xnext:x), cs=sOf(cur), cf=fperim(cs);
          ctx.fillStyle=RED; ctx.beginPath(); ctx.arc(X(cs),Yv(cf),6.5,0,2*Math.PI); ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=1.8; ctx.stroke();
          // seta do salto (quando trunca muda o suporte)
          if(phase===2 && hist.length>=1){ var prev=hist[hist.length-1];
            if(top2(cur).join()!==(function(){var pk=top2(x);return pk.join();})()){
              ctx.strokeStyle=RED; ctx.lineWidth=1.6; ctx.setLineDash([3,3]);
              ctx.beginPath(); ctx.moveTo(X(prev),Yv(fperim(prev))-12); ctx.lineTo(X(cs),Yv(cf)-12); ctx.stroke(); ctx.setLineDash([]);
              labelB('↯ saltou',(X(prev)+X(cs))/2,Yv(cf)-20,RED,11.5,'center'); }
          }
        }
        function updHUD(){
          var cur=(phase===2?xnext:x), k=top2(cur), lam=fperim(sOf(cur)); // ~ aproxima; usa lambda do par:
          lam=(function(i,j){var a=Q[i][i],b=Q[j][j],c=Q[i][j];return (a+b)/2+Math.sqrt(((a-b)/2)*((a-b)/2)+c*c);})(k[0],k[1]);
          var gap=Math.round(100*(LOPT-lam)/LOPT);
          phEl.textContent='rodada '+it+' · '+(phase===0?'estado':(phase===1?'passo denso':'trunca'));
          supEl.textContent=supName(k); varEl.textContent=fmt(lam);
          if(done){ jumpEl.textContent='TRAVOU · '+gap+'% abaixo'; jumpEl.style.color=RED; }
          else { jumpEl.textContent=gap+'% abaixo (ótimo nunca)'; jumpEl.style.color=DARK; }
        }
        function draw(){ ctx.clearRect(0,0,CSSW,CSSH);
          ctx.strokeStyle='#eceef2'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(372,50); ctx.lineTo(372,CSSH-26); ctx.stroke();
          drawBars(); drawRelief(); updHUD(); }
        function frame(ts){ if(auto && !done){ if(ts-tlast>1050){ advance(); tlast=ts; } } draw(); requestAnimationFrame(frame); }
        stepBtn.addEventListener('click', function(){ auto=false; autoBtn.textContent='▶▶ rodar'; advance(); });
        autoBtn.addEventListener('click', function(){ if(done) reset(); auto=!auto; autoBtn.textContent=auto?'⏸ pausar':'▶▶ rodar'; });
        resetBtn.addEventListener('click', function(){ reset(); });
        reset(); requestAnimationFrame(frame);
      })();
      </script>"""
rep1(r'<script>(?:(?!</script>).)*?s2tanim-cv(?:(?!</script>).)*?</script>', JS, flags=re.DOTALL)

ok, rep = integrity(html, 10)
print("integrity:", ok)
for k, v in rep.items(): print("  ", k, v)
assert ok, rep
open(DOC, "w", encoding="utf-8").write(html)
print("OK: #s2tanim agora tem barras + relevo lado a lado, com passos discretos.")
