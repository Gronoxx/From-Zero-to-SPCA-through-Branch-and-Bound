#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige a falha apontada pelo Gustavo: a versao n=4 ACHAVA o otimo com eta grande
(otimo alcancavel -> nao provava a falha). Troca pelo Example J (3 variaveis), onde o
passo+trunca NUNCA acha o otimo {x2,x3} para nenhum eta: agarra x1 (maior variancia),
salta a 2a vaga entre {x1,x3}(14% abaixo) e {x1,x2}(3% abaixo), mas chegar em {x2,x3}
exigiria largar x1 (o corte por modulo nunca faz). Salta E erra, robustamente."""
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

def lit(old, new):
    global html
    assert html.count(old) == 1, ("ancora nao-unica (%d): %s" % (html.count(old), old[:55]))
    html = html.replace(old, new)

# 1) paragrafo do erro: troca a versao 4-var (alcancavel) pela 3-var J (inalcancavel)
PAR = r"""<p><strong>E o salto não salva — ele nunca acha o ótimo.</strong> Tome 3 variáveis em que \(x_1\)
        tem a <em>maior variância individual</em>, mas \(x_2\) e \(x_3\) são <em>fortemente correlacionadas</em>
        (e juntas rendem mais variância que qualquer par contendo \(x_1\)). O passo+trunca <strong>agarra
        \(x_1\)</strong> — a "mais alta" — e, ao variar \(\eta\), só troca a 2ª vaga entre \(\{x_1,x_3\}\) e
        \(\{x_1,x_2\}\): <strong>nunca tenta o ótimo \(\{x_2,x_3\}\)</strong>, porque chegar nele exigiria
        <em>largar a variável de maior variância</em> \(x_1\), e o corte por módulo nunca faz isso. Ele salta
        entre suportes errados (de 14% a 3% abaixo) e jamais certifica o melhor — deslize \(\eta\) do início ao
        fim e veja: o ótimo nunca aparece. É a falha conhecida — o truncamento/greedy é subótimo [Cadima &amp;
        Jolliffe, 1995; Berk &amp; Bertsimas, 2019] — e o motivo de o Branch-and-Bound (§5) existir.</p>"""
rep1(r'<p><strong>E não é só instabilidade.*?Branch-and-Bound \(§5\) existir\.</p>', PAR, flags=re.DOTALL)

# 2) figcaption: aponta para o exemplo (3 var) que salta entre errados e nunca acha o otimo
lit('a animação abaixo mostra, num exemplo de 4 variáveis, quando ele <strong>salta</strong> — e por que <strong>erra</strong>.',
    'a animação abaixo mostra quando ele <strong>salta</strong> entre suportes errados — e por que <strong>nunca acha o ótimo</strong>.')

# 3) markup do #s2tanim (3 variaveis)
MARKUP = r"""<div class="anim-wrap" id="s2tanim">
        <div class="anim-head">
          <span class="anim-title">Animação interativa — salta entre suportes errados e nunca acha o ótimo</span>
          <span class="anim-sub">3 variáveis: \(x_1\) tem a maior variância, mas \(x_2,x_3\) são correlacionadas (o melhor par). Deslize \(\eta\): o passo denso <em>fiel</em> \(x+\eta\,2Qx\) enche as barras e o truncamento mantém as 2 maiores. Ele <strong>agarra \(x_1\)</strong> e só troca a 2ª vaga (\(x_3\leftrightarrow x_2\)) — <strong>nunca tenta o ótimo \(\{x_2,x_3\}\)</strong> (exigiria largar \(x_1\)). Salta entre 14% e 3% abaixo, sem nunca acertar.</span>
        </div>
        <canvas id="s2tanim-cv" width="720" height="360" aria-label="Animacao: 3 barras, passo do gradiente fiel, x1 sempre mantida, a 2a vaga salta entre x3 e x2, otimo x2x3 nunca alcancado"></canvas>
        <div class="anim-ctrl">
          <button id="s2tanim-sweep" class="anim-btn" type="button">▶ Varrer η</button>
          <input id="s2tanim-slider" type="range" min="0" max="1000" value="150" aria-label="Tamanho do passo eta">
          <span id="s2tanim-eta" class="anim-tval">η peq.</span>
        </div>
        <div class="anim-hud">
          <div><span class="hud-k">suporte (passo+trunca)</span><span id="s2tanim-sup" class="hud-v">{x1,x3}</span></div>
          <div><span class="hud-k">λ vs ótimo {x2,x3}=3,73</span><span id="s2tanim-var" class="hud-v">3,23</span></div>
          <div><span class="hud-k">o que aconteceu</span><span id="s2tanim-jump" class="hud-v">14% abaixo</span></div>
        </div>
      </div>
      """
rep1(r'<div class="anim-wrap" id="s2tanim">.*?</div>\s*(?=<p><strong>Moral\.)', MARKUP, flags=re.DOTALL)

# 4) JS do #s2tanim (3 variaveis, Q de Example J)
JS = r"""<script>
      (function(){
        var cv=document.getElementById('s2tanim-cv'); if(!cv) return;
        var ctx=cv.getContext('2d'); var dpr=window.devicePixelRatio||1;
        var CSSW=720, CSSH=360;
        cv.width=CSSW*dpr; cv.height=CSSH*dpr; ctx.scale(dpr,dpr);
        var ACC='#3b54c4', PUR='#7a3fc4', GREEN='#1f9a55', GREY='#b9bec6', DARK='#1f3b6e', RED='#b23b3b';
        // Q 3x3 (Example J): x1 maior variancia (sempre mantida); x2,x3 correlacionadas = otimo {x2,x3}
        var Q=[[3.219,0.875,-0.043],[0.875,1.768,1.236],[-0.043,1.236,2.952]];
        var LOPT=3.73;                       // otimo {x2,x3}
        var names=['x1','x2','x3'], cols=[ACC,PUR,GREEN];
        function matvec(x){var r=[0,0,0];for(var i=0;i<3;i++){for(var j=0;j<3;j++){r[i]+=Q[i][j]*x[j];}}return r;}
        function lmaxPair(i,j){var a=Q[i][i],b=Q[j][j],c=Q[i][j];return (a+b)/2+Math.sqrt(((a-b)/2)*((a-b)/2)+c*c);}
        // x0 = autovetor de cima do par {x1,x3} (as 2 maiores variancias) -> dominado por x1
        function topvec13(){var a=3.219,b=2.952,c=-0.043;var lam=(a+b)/2+Math.sqrt(((a-b)/2)*((a-b)/2)+c*c);
          var vx=c,vy=lam-a,n=Math.hypot(vx,vy);return [vx/n,0,vy/n];}
        var x0=topvec13();
        function step(eta){var g=matvec(x0),xp=[0,0,0];for(var i=0;i<3;i++){xp[i]=x0[i]+eta*2*g[i];}return xp;}
        function top2(v){var idx=[0,1,2].sort(function(a,b){return Math.abs(v[b])-Math.abs(v[a]);});
          return [idx[0],idx[1]].sort(function(a,b){return a-b;});}
        function fmt(x){return x.toFixed(2).replace('.',',');}
        var BX=[180,360,540], BW=92, BY0=298, BTOP=84;
        var slider=document.getElementById('s2tanim-slider'), sweepBtn=document.getElementById('s2tanim-sweep'),
            etaEl=document.getElementById('s2tanim-eta'), supEl=document.getElementById('s2tanim-sup'),
            varEl=document.getElementById('s2tanim-var'), jumpEl=document.getElementById('s2tanim-jump');
        var sweeping=false, prevSup=null, flash=0;
        function draw(eta){
          ctx.clearRect(0,0,CSSW,CSSH);
          var xp=step(eta), keep=top2(xp);
          var maxv=0; for(var i=0;i<3;i++){if(Math.abs(xp[i])>maxv)maxv=Math.abs(xp[i]);} if(maxv<1e-6)maxv=1;
          ctx.strokeStyle='#cfd2d8'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(110,BY0); ctx.lineTo(620,BY0); ctx.stroke();
          for(var b=0;b<3;b++){
            var h=Math.abs(xp[b])/maxv*(BY0-BTOP), inK=(keep.indexOf(b)>=0);
            ctx.fillStyle=inK?cols[b]:GREY; ctx.fillRect(BX[b]-BW/2,BY0-h,BW,h);
            if(!inK){ctx.strokeStyle=RED; ctx.setLineDash([4,3]); ctx.strokeRect(BX[b]-BW/2,BY0-h,BW,h); ctx.setLineDash([]);
              ctx.fillStyle=RED; ctx.font='700 12px sans-serif'; ctx.textAlign='center'; ctx.fillText('zera',BX[b],BY0-h-8);}
            ctx.fillStyle=DARK; ctx.font='700 15px sans-serif'; ctx.textAlign='center'; ctx.fillText(names[b],BX[b],BY0+18);
            ctx.fillStyle='#6b7280'; ctx.font='12px sans-serif'; ctx.fillText('var '+fmt(Q[b][b]),BX[b],BY0+34);
            if(b===0){ctx.fillStyle=ACC; ctx.font='italic 11px sans-serif'; ctx.fillText('(sempre mantida)',BX[b],BY0+50);}
          }
          var sup='{'+keep.map(function(i){return names[i];}).join(',')+'}';
          var lam=lmaxPair(keep[0],keep[1]), gap=Math.round(100*(LOPT-lam)/LOPT);
          ctx.textAlign='left'; ctx.font='700 14.5px sans-serif'; ctx.fillStyle=RED;
          ctx.fillText('passo+trunca: '+sup+'  (λ='+fmt(lam)+')  →  '+gap+'% abaixo', 110, 40);
          ctx.fillStyle=GREEN; ctx.font='700 13.5px sans-serif';
          ctx.fillText('ótimo {x2,x3}: λ=3,73  — exige largar x1: NUNCA tentado', 110, 60);
          supEl.textContent=sup; varEl.textContent=fmt(lam);
          if(prevSup!==null && sup!==prevSup){flash=70;} prevSup=sup;
          if(flash>0){jumpEl.textContent='↯ SALTOU (2ª vaga)'; jumpEl.style.color=RED; flash--;}
          else {jumpEl.textContent=gap+'% abaixo'; jumpEl.style.color=DARK;}
          etaEl.textContent=(eta<0.1?'η peq.':'η='+fmt(eta));
        }
        function frame(){ if(sweeping){var v=(+slider.value)+6; if(v>1000){v=0;} slider.value=v;} draw(slider.value/1000*1.0); requestAnimationFrame(frame); }
        slider.addEventListener('input', function(){ sweeping=false; sweepBtn.textContent='▶ Varrer η'; });
        sweepBtn.addEventListener('click', function(){ sweeping=!sweeping; sweepBtn.textContent=sweeping?'⏸ Pausar':'▶ Varrer η'; });
        requestAnimationFrame(frame);
      })();
      </script>"""
rep1(r'<script>(?:(?!</script>).)*?s2tanim-cv(?:(?!</script>).)*?</script>', JS, flags=re.DOTALL)

ok, rep = integrity(html, 10)
print("integrity:", ok)
for k, v in rep.items(): print("  ", k, v)
assert ok, rep
open(DOC, "w", encoding="utf-8").write(html)
print("OK: #s2tanim agora usa Example J (3 var) — salta entre errados, NUNCA acha o otimo.")
