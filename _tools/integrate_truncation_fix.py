#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Troca a animacao artificial #s2tanim por uma FIEL (passo denso real x+eta*2Qx) com um
exemplo REAL de 4 variaveis onde o passo+trunca ERRA (~40% abaixo do otimo) E SALTA
(suporte descontinuo em eta). Tambem ajusta a prosa da caixa (salta E erra) + citacao.
Substituicoes via regex contido + lambda (nao mistura escapes do MathJax)."""
import re, sys
sys.path.insert(0, "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools")
from al_template import integrity

DOC = "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/02_sparse_pca_o_problema.html"
html = open(DOC, encoding="utf-8").read()

def rep1(pattern, repl, flags=0):
    global html
    new, n = re.subn(pattern, lambda m: repl, html, flags=flags)
    assert n == 1, ("substituicao falhou (n=%d): %s" % (n, pattern[:60]))
    html = new

def lit(old, new):
    global html
    assert html.count(old) == 1, ("ancora nao-unica (%d): %s" % (html.count(old), old[:60]))
    html = html.replace(old, new)

# 1) titulo da caixa: salta -> salta E erra
lit('<span class="tag">O truque "dar o passo e depois truncar" — e por que ele salta</span>',
    '<span class="tag">O truque "dar o passo e depois truncar" — por que ele salta E erra</span>')

# 2) parentetico da descontinuidade: generico (nao "componentes 2 e 3"); ancora box-especifica
lit('quando as componentes 2 e 3 cruzam, o suporte — e a posição no relevo — <strong>teleporta</strong>',
    'quando uma componente de fora ultrapassa uma de dentro em módulo, o suporte <strong>teleporta</strong>')

# 3) paragrafo NOVO do "erra" (4 variaveis, ~40%, citacao) inserido ao fim da caixa
ERRA = r"""depende de
        onde começou.</p>
        <p><strong>E não é só instabilidade — ele pode parar no suporte errado.</strong> Tome 4 variáveis de
        variância parecida, mas com um par <em>fortemente correlacionado</em> (digamos \(x_1\) e \(x_4\),
        correlação \(0{,}84\)). A regra gulosa "as \(k\) maiores em módulo" agarra as duas de <em>maior
        variância</em> — aqui \(\{x_1,x_3\}\) — e o passo+trunca, com um passo prudente, <strong>converge ali,
        \(\approx\)40% abaixo</strong> do ótimo \(\{x_1,x_4\}\), que só vence porque explora a correlação. Só com
        um passo agressivo (que você não conhece de antemão) ele escaparia. É a falha que a literatura documenta
        — o truncamento/greedy é subótimo [Cadima &amp; Jolliffe, 1995; Berk &amp; Bertsimas, 2019, medem perdas
        de até \(\sim\)24% em dados reais] — e o motivo de o Branch-and-Bound (§5) existir.</p>"""
lit('depende de\n        onde começou.</p>', ERRA)

# 4) figcaption: aponta para o exemplo de 4 variaveis (salta E erra)
lit('a animação abaixo mostra quando ele <strong>salta</strong>.',
    'a animação abaixo mostra, num exemplo de 4 variáveis, quando ele <strong>salta</strong> — e por que <strong>erra</strong>.')

# 5) markup do #s2tanim (substitui o div inteiro ate o </div> antes do "Moral")
MARKUP = r"""<div class="anim-wrap" id="s2tanim">
        <div class="anim-head">
          <span class="anim-title">Animação interativa — o passo+trunca erra (e salta)</span>
          <span class="anim-sub">4 variáveis de variância parecida, mas \(x_1\) e \(x_4\) fortemente correlacionadas. Deslize \(\eta\): o passo denso <em>fiel</em> \(x+\eta\,2Qx\) faz as barras crescerem (a de \(x_4\) também), e o truncamento mantém as 2 maiores. Com passo prudente fica preso em \(\{x_1,x_3\}\) (as 2 de maior variância) — \(\approx\)40% abaixo do ótimo \(\{x_1,x_4\}\); e o suporte <strong>salta</strong> de uma vez quando \(x_4\) ultrapassa \(x_3\).</span>
        </div>
        <canvas id="s2tanim-cv" width="720" height="360" aria-label="Animacao: passo do gradiente fiel enche 4 barras, truncamento mantem 2, suporte preso em x1x3 abaixo do otimo x1x4 e salta para x1x4"></canvas>
        <div class="anim-ctrl">
          <button id="s2tanim-sweep" class="anim-btn" type="button">▶ Varrer η</button>
          <input id="s2tanim-slider" type="range" min="0" max="1000" value="120" aria-label="Tamanho do passo eta">
          <span id="s2tanim-eta" class="anim-tval">η peq.</span>
        </div>
        <div class="anim-hud">
          <div><span class="hud-k">suporte (passo+trunca)</span><span id="s2tanim-sup" class="hud-v">{x1,x3}</span></div>
          <div><span class="hud-k">λ do suporte (ótimo = 4,63)</span><span id="s2tanim-var" class="hud-v">2,77</span></div>
          <div><span class="hud-k">o que aconteceu</span><span id="s2tanim-jump" class="hud-v">40% abaixo</span></div>
        </div>
      </div>
      """
rep1(r'<div class="anim-wrap" id="s2tanim">.*?</div>\s*(?=<p><strong>Moral\.)', MARKUP, flags=re.DOTALL)

# 6) JS do #s2tanim: substitui o bloco <script>...s2tanim-cv...</script> por um FIEL
JS = r"""<script>
      (function(){
        var cv=document.getElementById('s2tanim-cv'); if(!cv) return;
        var ctx=cv.getContext('2d'); var dpr=window.devicePixelRatio||1;
        var CSSW=720, CSSH=360;
        cv.width=CSSW*dpr; cv.height=CSSH*dpr; ctx.scale(dpr,dpr);
        var ACC='#3b54c4', PUR='#7a3fc4', GREEN='#1f9a55', AMBER='#c2790a', GREY='#b9bec6', DARK='#1f3b6e', RED='#b23b3b';
        // Q 4x4 (covariancia real): x1,x4 fortemente correlacionadas (0.84); variancias parecidas
        var Q=[[2.70,0.15,0.14,2.11],[0.15,2.24,0.01,0.15],[0.14,0.01,2.47,0.14],[2.11,0.15,0.14,2.33]];
        var LOPT=4.63;                       // lambda_max do otimo {x1,x4}
        var names=['x1','x2','x3','x4'], cols=[ACC,PUR,GREEN,AMBER];
        function matvec(x){var r=[0,0,0,0];for(var i=0;i<4;i++){for(var j=0;j<4;j++){r[i]+=Q[i][j]*x[j];}}return r;}
        function lmaxPair(i,j){var a=Q[i][i],b=Q[j][j],c=Q[i][j];return (a+b)/2+Math.sqrt(((a-b)/2)*((a-b)/2)+c*c);}
        // x0 = autovetor de cima do par {x1,x3} (maiores variancias), em R^4
        function topvec13(){var a=2.70,b=2.47,c=0.14;var lam=(a+b)/2+Math.sqrt(((a-b)/2)*((a-b)/2)+c*c);
          var vx=c,vy=lam-a,n=Math.hypot(vx,vy);return [vx/n,0,vy/n,0];}
        var x0=topvec13();
        function step(eta){var g=matvec(x0),xp=[0,0,0,0];for(var i=0;i<4;i++){xp[i]=x0[i]+eta*2*g[i];}return xp;}
        function top2(v){var idx=[0,1,2,3].sort(function(a,b){return Math.abs(v[b])-Math.abs(v[a]);});
          return [idx[0],idx[1]].sort(function(a,b){return a-b;});}
        function fmt(x){return x.toFixed(2).replace('.',',');}
        var BX=[150,300,450,600], BW=80, BY0=300, BTOP=78;
        var slider=document.getElementById('s2tanim-slider'), sweepBtn=document.getElementById('s2tanim-sweep'),
            etaEl=document.getElementById('s2tanim-eta'), supEl=document.getElementById('s2tanim-sup'),
            varEl=document.getElementById('s2tanim-var'), jumpEl=document.getElementById('s2tanim-jump');
        var sweeping=false, prevSup=null, flash=0;
        function draw(eta){
          ctx.clearRect(0,0,CSSW,CSSH);
          var xp=step(eta), keep=top2(xp);
          var maxv=0; for(var i=0;i<4;i++){if(Math.abs(xp[i])>maxv)maxv=Math.abs(xp[i]);} if(maxv<1e-6)maxv=1;
          ctx.strokeStyle='#cfd2d8'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(95,BY0); ctx.lineTo(665,BY0); ctx.stroke();
          for(var b=0;b<4;b++){
            var h=Math.abs(xp[b])/maxv*(BY0-BTOP), inK=(keep.indexOf(b)>=0);
            ctx.fillStyle=inK?cols[b]:GREY; ctx.fillRect(BX[b]-BW/2,BY0-h,BW,h);
            if(!inK){ctx.strokeStyle=RED; ctx.setLineDash([4,3]); ctx.strokeRect(BX[b]-BW/2,BY0-h,BW,h); ctx.setLineDash([]);
              ctx.fillStyle=RED; ctx.font='700 12px sans-serif'; ctx.textAlign='center'; ctx.fillText('zera',BX[b],BY0-h-8);}
            ctx.fillStyle=DARK; ctx.font='700 14px sans-serif'; ctx.textAlign='center'; ctx.fillText(names[b],BX[b],BY0+18);
            ctx.fillStyle='#6b7280'; ctx.font='12px sans-serif'; ctx.fillText('var '+fmt(Q[b][b]),BX[b],BY0+34);
          }
          var sup='{'+keep.map(function(i){return names[i];}).join(',')+'}';
          var lam=lmaxPair(keep[0],keep[1]), gap=Math.round(100*(LOPT-lam)/LOPT), isOpt=(keep[0]===0&&keep[1]===3);
          ctx.textAlign='left'; ctx.font='700 14.5px sans-serif'; ctx.fillStyle=isOpt?GREEN:RED;
          ctx.fillText('suporte '+sup+'  (λ='+fmt(lam)+')'+(isOpt?'  = ÓTIMO':'  →  '+gap+'% abaixo do ótimo {x1,x4}'), 100, 42);
          supEl.textContent=sup; varEl.textContent=fmt(lam);
          if(prevSup!==null && sup!==prevSup){flash=70;} prevSup=sup;
          if(flash>0){jumpEl.textContent='↯ SALTOU de suporte!'; jumpEl.style.color=RED; flash--;}
          else {jumpEl.textContent=isOpt?'achou o ótimo':(gap+'% abaixo'); jumpEl.style.color=isOpt?GREEN:DARK;}
          etaEl.textContent = (eta<0.1?'η peq.':'η='+fmt(eta));
        }
        function frame(){ if(sweeping){var v=(+slider.value)+6; if(v>1000){v=0;} slider.value=v;} draw(slider.value/1000*0.9); requestAnimationFrame(frame); }
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
print("OK: #s2tanim agora eh fiel (erra+salta, 4 variaveis) e a caixa foi atualizada.")
