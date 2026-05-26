#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""#s2tanim v4: ajustes no relevo pedidos pelo Gustavo.
(1) Q13=0 (x1,x3 exatamente descorrelacionados) -> arco {x1,x3} vira RAMPA LIMPA (sem
    a 'senoide' do Q13<0); rotulado: nao ha morro porque o melhor de {x1,x3} eh so x1.
(2) QUINAS explicitas (cantos e1/e2/e3 = x puro, marcados como quinas).
(3) cada ARCO colorido com as cores do PAR (gradiente entre as 2 variaveis; cores das barras:
    x1=azul, x2=roxo, x3=verde). As quinas sao os x puros nessas cores.
Demonstracao preservada (verificado): trava {x1,x3}->{x1,x2}, 14% abaixo, otimo {x2,x3} nunca."""
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
          <span class="anim-title">Animação interativa — passo+trunca, passo a passo: barras (mecanismo) + relevo (bacias)</span>
          <span class="anim-sub">Clique <strong>próximo passo</strong>. ESQUERDA: o <em>passo denso</em> \(x+\eta\,2Qx\) enche as barras (a de \(x_1\) <em>dispara</em> — maior variância — por isso sempre sobrevive ao truncamento) e depois o <em>truncamento</em> zera a menor. DIREITA: o relevo, colorido pelas cores das variáveis (as <strong>quinas</strong> e1/e2/e3 são os \(x\) puros). Cada suporte tem um único ótimo: vira <em>morro</em> no meio do arco se o par for <strong>correlacionado</strong> (\(\{x_2,x_3\}\), \(\{x_1,x_2\}\)); mas \(x_1\) e \(x_3\) são <strong>descorrelacionados</strong>, então \(\{x_1,x_3\}\) não tem morro — é uma <strong>rampa</strong> (o melhor é só \(x_1\), no canto). O iterado salta entre \(\{x_1,x_3\}\) e \(\{x_1,x_2\}\) e trava, <strong>sem nunca subir o morro \(\{x_2,x_3\}\)</strong> (o ótimo), pois isso exigiria largar \(x_1\).</span>
        </div>
        <canvas id="s2tanim-cv" width="820" height="392" aria-label="Dois paineis: barras do passo denso e truncamento a esquerda; relevo colorido das bacias com quinas explicitas, arco x1x3 como rampa, e o iterado saltando entre dois suportes sem alcancar o morro otimo x2x3 a direita"></canvas>
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
        var ACC='#3b54c4', PUR='#7a3fc4', GREEN='#1f9a55', GREY='#b9bec6', DARK='#1f3b6e', RED='#b23b3b';
        var Q=[[3.219,0.875,0.0],[0.875,1.768,1.236],[0.0,1.236,2.952]];   // Q13=0: x1,x3 descorrelacionados
        var ETA=0.4, NAMES=['x1','x2','x3'], COLS=[ACC,PUR,GREEN];
        function mv(x){var r=[0,0,0];for(var i=0;i<3;i++){for(var j=0;j<3;j++){r[i]+=Q[i][j]*x[j];}}return r;}
        function norm(x){var s=Math.hypot(x[0],x[1],x[2]);return [x[0]/s,x[1]/s,x[2]/s];}
        function top2(v){var idx=[0,1,2].sort(function(a,b){return Math.abs(v[b])-Math.abs(v[a]);});return [idx[0],idx[1]].sort(function(a,b){return a-b;});}
        function fmt(x){return x.toFixed(2).replace('.',',');}
        function supName(k){return '{'+NAMES[k[0]]+','+NAMES[k[1]]+'}';}
        function hx(h){return [parseInt(h.substr(1,2),16),parseInt(h.substr(3,2),16),parseInt(h.substr(5,2),16)];}
        function lerpCol(c1,c2,t){var a=hx(c1),b=hx(c2);return 'rgb('+Math.round(a[0]+(b[0]-a[0])*t)+','+Math.round(a[1]+(b[1]-a[1])*t)+','+Math.round(a[2]+(b[2]-a[2])*t)+')';}
        // relevo: perimetro e2->e3->e1->e2 (e1 no centro)
        function fperim(s){ s=((s%3)+3)%3; var t,c,n;
          if(s<1){ t=s*Math.PI/2; c=Math.cos(t); n=Math.sin(t); return Q[1][1]*c*c+Q[2][2]*n*n+2*Q[1][2]*c*n; }
          if(s<2){ t=(s-1)*Math.PI/2; c=Math.cos(t); n=Math.sin(t); return Q[2][2]*c*c+Q[0][0]*n*n+2*Q[0][2]*c*n; }
          t=(s-2)*Math.PI/2; c=Math.cos(t); n=Math.sin(t); return Q[0][0]*c*c+Q[1][1]*n*n+2*Q[0][1]*c*n; }
        function arcCol(s){ s=((s%3)+3)%3; var seg=Math.floor(s), fr=s-seg;
          if(seg<=0) return lerpCol(PUR,GREEN,fr); if(seg===1) return lerpCol(GREEN,ACC,fr); return lerpCol(ACC,PUR,fr); }
        function sOf(x){var k=top2(x);
          if(k[0]===1&&k[1]===2) return Math.atan2(Math.abs(x[2]),Math.abs(x[1]))/(Math.PI/2);
          if(k[0]===0&&k[1]===2) return 1+Math.atan2(Math.abs(x[0]),Math.abs(x[2]))/(Math.PI/2);
          return 2+Math.atan2(Math.abs(x[1]),Math.abs(x[0]))/(Math.PI/2); }
        function lmaxPair(i,j){var a=Q[i][i],b=Q[j][j],c=Q[i][j];return (a+b)/2+Math.sqrt(((a-b)/2)*((a-b)/2)+c*c);}
        var LOPT=lmaxPair(1,2);
        // morros (so dos pares correlacionados): seg0={x2,x3}, seg2={x1,x2}; seg1={x1,x3} eh rampa
        function morro(seg){var bf=-1,bs=seg+0.5; for(var u=0.001;u<0.999;u+=0.002){var ss=seg+u,ff=fperim(ss); if(ff>bf){bf=ff;bs=ss;}} return [bs,bf];}
        var M0=morro(0), M2=morro(2);
        var BX=[112,205,298], BW=66, BY0=300, FULL=3.85;
        var RX0=420, RX1=792, RY0=96, RY1=300, FLO=1.5, FHI=3.95;
        function X(s){return RX0+(s/3)*(RX1-RX0);}
        function Yv(f){return RY1-(f-FLO)/(FHI-FLO)*(RY1-RY0);}
        function label(t,x,y,col,sz,al){ctx.save();ctx.fillStyle=col;ctx.font=(sz||13)+'px -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif';ctx.textAlign=al||'left';ctx.textBaseline='alphabetic';ctx.fillText(t,x,y);ctx.restore();}
        function labelB(t,x,y,col,sz,al){ctx.save();ctx.fillStyle=col;ctx.font='700 '+(sz||13)+'px -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif';ctx.textAlign=al||'left';ctx.fillText(t,x,y);ctx.restore();}
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
          var vec=(phase===0?x:xp), showDrop=(phase===2), dropIdx=-1, dense=(phase>=1);
          if(showDrop) dropIdx=(kept.indexOf(0)<0?0:(kept.indexOf(1)<0?1:2));
          labelB('Barras: o mecanismo (1 passo)', 52, 40, DARK, 14);
          var phn=(phase===0?'estado atual (2 variáveis)':(phase===1?'passo denso: x + η·2Qx (enche tudo)':'trunca: mantém as 2 maiores, zera a menor'));
          label(phn, 52, 60, (phase===1?'#c2790a':(phase===2?RED:DARK)), 12.5);
          ctx.strokeStyle='#cfd2d8'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(72,BY0); ctx.lineTo(338,BY0); ctx.stroke();
          for(var b=0;b<3;b++){
            var h=Math.abs(vec[b])/FULL*(BY0-96), drop=(showDrop&&b===dropIdx);
            var col=drop?GREY:(dense?COLS[b]:(Math.abs(vec[b])<1e-6?GREY:COLS[b]));
            ctx.fillStyle=col; ctx.fillRect(BX[b]-BW/2,BY0-h,BW,h);
            if(drop){ ctx.strokeStyle=RED; ctx.setLineDash([4,3]); ctx.strokeRect(BX[b]-BW/2,BY0-h,BW,h); ctx.setLineDash([]); labelB('zera',BX[b],BY0-h-7,RED,11.5,'center'); }
            labelB(NAMES[b],BX[b],BY0+18,DARK,14,'center'); label('var '+fmt(Q[b][b]),BX[b],BY0+34,'#6b7280',11.5,'center');
          }
          if(phase>=1){ labelB('x1 dispara',BX[0],BY0-Math.abs(vec[0])/FULL*(BY0-96)-10,ACC,12,'center'); label('(maior variância → ∇f grande)',195,82,ACC,11,'center'); }
        }
        function drawRelief(){
          labelB('Relevo: as bacias (a consequência)', 412, 40, DARK, 14);
          ctx.strokeStyle='#cfd2d8'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(RX0-8,RY1); ctx.lineTo(RX1+4,RY1); ctx.stroke();
          // curva colorida pelo par (gradiente entre as cores das 2 variaveis)
          ctx.lineWidth=3.2;
          for(var s=0;s<3.0;s+=0.02){ ctx.strokeStyle=arcCol(s+0.01); ctx.beginPath(); ctx.moveTo(X(s),Yv(fperim(s))); ctx.lineTo(X(s+0.02),Yv(fperim(s+0.02))); ctx.stroke(); }
          // QUINAS (cantos = x puro), explicitas: diamante na cor da variavel
          var corn=[[0,'x2',PUR],[1,'x3',GREEN],[2,'x1',ACC],[3,'x2',PUR]];
          for(var ci=0;ci<corn.length;ci++){ var cs=corn[ci][0], cx=X(cs), cy=Yv(fperim(cs));
            ctx.fillStyle=corn[ci][2]; ctx.save(); ctx.translate(cx,cy); ctx.rotate(Math.PI/4); ctx.fillRect(-4.5,-4.5,9,9); ctx.restore();
            ctx.strokeStyle='#fff'; ctx.lineWidth=1; ctx.save(); ctx.translate(cx,cy); ctx.rotate(Math.PI/4); ctx.strokeRect(-4.5,-4.5,9,9); ctx.restore();
            label('quina '+corn[ci][1], cx, RY1+15, corn[ci][2], 10.5, 'center'); }
          // morro otimo {x2,x3} (seg0, par correlacionado)
          ctx.fillStyle=GREEN; ctx.beginPath(); ctx.arc(X(M0[0]),Yv(M0[1]),6,0,2*Math.PI); ctx.fill();
          ctx.strokeStyle=GREEN; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(X(M0[0]),Yv(M0[1]),10,0,2*Math.PI); ctx.stroke();
          labelB('ótimo {x2,x3}',X(M0[0]),Yv(M0[1])-17,GREEN,12,'center'); label('(correlacionadas → morro · NUNCA)',X(M0[0]),Yv(M0[1])-4,GREEN,10,'center');
          // morro {x1,x2} (seg2, correlacionado)
          ctx.fillStyle='#7a8088'; ctx.beginPath(); ctx.arc(X(M2[0]),Yv(M2[1]),4,0,2*Math.PI); ctx.fill();
          label('morro {x1,x2}',X(M2[0])+4,Yv(M2[1])-8,'#5b6573',10.5,'left');
          // {x1,x3} = RAMPA (seg1): rotulo curto (explicacao completa no anim-sub)
          label('{x1,x3}: rampa',X(1.4),Yv(fperim(1.4))-19,'#5b6573',11,'center');
          label('(sem morro — só x1)',X(1.4),Yv(fperim(1.4))-6,'#5b6573',10,'center');
          // trilha (posicoes passadas)
          for(var hI=0;hI<hist.length-1;hI++){ ctx.fillStyle='rgba(178,59,59,.22)'; ctx.beginPath(); ctx.arc(X(hist[hI]),Yv(fperim(hist[hI])),3.2,0,2*Math.PI); ctx.fill(); }
          // marcador atual
          var cur=(phase===2?xnext:x), cs2=sOf(cur), cf=fperim(cs2);
          if(phase===2 && top2(cur).join()!==top2(x).join()){ var prev=hist[hist.length-1];
            ctx.strokeStyle=RED; ctx.lineWidth=1.6; ctx.setLineDash([3,3]); ctx.beginPath(); ctx.moveTo(X(prev),Yv(fperim(prev))-12); ctx.lineTo(X(cs2),Yv(cf)-12); ctx.stroke(); ctx.setLineDash([]);
            labelB('↯ saltou',(X(prev)+X(cs2))/2,Yv(cf)-20,RED,11.5,'center'); }
          ctx.fillStyle=RED; ctx.beginPath(); ctx.arc(X(cs2),Yv(cf),6.5,0,2*Math.PI); ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=1.8; ctx.stroke();
        }
        function updHUD(){
          var cur=(phase===2?xnext:x), k=top2(cur), lam=lmaxPair(k[0],k[1]), gap=Math.round(100*(LOPT-lam)/LOPT);
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

ok, rep = integrity(html, 11)
print("integrity:", ok)
for k, v in rep.items(): print("  ", k, v)
assert ok, rep
open(DOC, "w", encoding="utf-8").write(html)
print("OK: relevo colorido por par + quinas explicitas + {x1,x3} rampa explicada (Q13=0).")
