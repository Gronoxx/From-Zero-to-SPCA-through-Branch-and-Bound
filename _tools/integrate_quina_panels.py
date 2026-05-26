#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""(1) Reconstroi a #s2qanim como DOIS paineis acoplados: esquerda = as duas subidas
de variancia f(theta) ao longo de cada arco (mesma altura no canto, tangentes que se
inclinam ao mover o slider); direita = a vista de cima (retangulo/gradiente). Aterra a
'inclinacao' numa paisagem que realmente muda de subida.
(2) Caixa de contra-intuicao: remove o paragrafo de precisao infinita e aprofunda o
porque do circulo de raio 1 e de a normalizacao NAO forcar simetria (recipiente x conteudo)."""
import re, sys
sys.path.insert(0, "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools")
from al_template import integrity

DOC = "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/02_sparse_pca_o_problema.html"
html = open(DOC, encoding="utf-8").read()

# =================================================================== op1: animacao dois paineis
NEW_ANIM = r"""<div class="anim-wrap" id="s2qanim">
        <div class="anim-head">
          <span class="anim-title">Animação interativa — a subida de cada arco (esq.) e o garfo (dir.)</span>
          <span class="anim-sub">à esquerda, as duas <em>subidas</em> de variância \(f\) ao longo de cada arco: ambas partem da mesma altura no canto, e o que muda com o slider é a <em>inclinação no canto</em> (a reta tangente). À direita, essa mesma inclinação vira o lado do retângulo, e o gradiente é a diagonal — só vira 45° quando as duas subidas se igualam. O círculo \(\|x\|=1\) (direita) é fixo.</span>
        </div>
        <canvas id="s2qanim-cv" width="760" height="430" aria-label="Dois paineis: a esquerda as duas subidas de variancia ao longo de cada arco com suas tangentes no canto, a direita a vista de cima com retangulo e gradiente"></canvas>
        <div class="anim-ctrl">
          <button id="s2qanim-sweep" class="anim-btn" type="button">▶ Varrer assimetria</button>
          <input id="s2qanim-slider" type="range" min="0" max="1000" value="500" aria-label="Assimetria entre as duas inclinacoes">
          <span id="s2qanim-lab" class="anim-tval">assimétrico</span>
        </div>
        <div class="anim-hud">
          <div><span class="hud-k">inclinação {x₁,x₂} (subida azul)</span><span id="s2qanim-sa" class="hud-v">2,4</span></div>
          <div><span class="hud-k">inclinação {x₁,x₃} (subida roxa)</span><span id="s2qanim-sb" class="hud-v">1,6</span></div>
          <div><span class="hud-k">ângulo do gradiente</span><span id="s2qanim-ang" class="hud-v">33,7°</span></div>
        </div>
      </div>
      <style>
        #s2qanim{border:1px solid var(--line);border-radius:16px;background:#fff;
          padding:14px 14px 16px;margin:20px 0;box-shadow:0 3px 14px rgba(20,30,60,.07)}
        #s2qanim .anim-head{display:flex;flex-direction:column;gap:2px;margin-bottom:10px}
        #s2qanim .anim-title{font-weight:800;color:#1a2230;font-size:15px}
        #s2qanim .anim-sub{font-size:12.5px;color:var(--muted);font-style:italic}
        #s2qanim canvas{display:block;width:100%;max-width:760px;height:auto;margin:0 auto;
          background:#fcfcfa;border:1px solid var(--line);border-radius:12px}
        #s2qanim .anim-ctrl{display:flex;align-items:center;gap:12px;margin:12px 2px 0}
        #s2qanim .anim-btn{appearance:none;border:1px solid var(--accent);background:var(--accent);
          color:#fff;font-weight:700;font-size:13.5px;padding:7px 14px;border-radius:9px;cursor:pointer;
          white-space:nowrap;font-family:inherit}
        #s2qanim .anim-btn:hover{filter:brightness(1.06)}
        #s2qanim input[type=range]{flex:1;accent-color:var(--accent);cursor:pointer}
        #s2qanim .anim-tval{font-variant-numeric:tabular-nums;color:#37414f;font-weight:700;
          font-size:13.5px;min-width:92px;text-align:right}
        #s2qanim .anim-hud{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px}
        #s2qanim .anim-hud>div{background:var(--slate-bg);border:1px solid var(--line);border-radius:10px;
          padding:8px 10px;display:flex;flex-direction:column;gap:3px}
        #s2qanim .hud-k{font-size:11.5px;color:var(--muted);letter-spacing:.01em}
        #s2qanim .hud-v{font-size:18px;font-weight:800;color:#1a2230;font-variant-numeric:tabular-nums}
        @media(max-width:560px){#s2qanim .anim-hud{grid-template-columns:1fr}}
      </style>
      <script>
      (function(){
        var cv=document.getElementById('s2qanim-cv'); if(!cv) return;
        var ctx=cv.getContext('2d'); var dpr=window.devicePixelRatio||1;
        var CSSW=760, CSSH=430;
        cv.width=CSSW*dpr; cv.height=CSSH*dpr; ctx.scale(dpr,dpr);
        var ACC='#3b54c4', PUR='#7a3fc4', GREY='#9aa0aa', DARK='#1f3b6e', RED='#b23b3b', GRN='#1f9a55', AMB='#c2790a';
        var Q11=2.0, Q22=2.2, Q33=1.6, TH=Math.PI/2;
        var saEl=document.getElementById('s2qanim-sa'), sbEl=document.getElementById('s2qanim-sb'),
            angEl=document.getElementById('s2qanim-ang'), slider=document.getElementById('s2qanim-slider'),
            sweepBtn=document.getElementById('s2qanim-sweep'), labEl=document.getElementById('s2qanim-lab');
        var t=0.5, sweeping=false, dir=1;
        function f1(v){return v.toFixed(1).replace('.',',');}
        function fA(th,q){var c=Math.cos(th),s=Math.sin(th);return Q11*c*c+Q22*s*s+2*q*c*s;}
        function fB(th,q){var c=Math.cos(th),s=Math.sin(th);return Q11*c*c+Q33*s*s+2*q*c*s;}
        function arrow(x0,y0,x1,y1,color,w,dash){
          ctx.save(); ctx.strokeStyle=color; ctx.fillStyle=color; ctx.lineWidth=w;
          if(dash){ctx.setLineDash(dash);}
          ctx.beginPath(); ctx.moveTo(x0,y0); ctx.lineTo(x1,y1); ctx.stroke(); ctx.setLineDash([]);
          var a=Math.atan2(y1-y0,x1-x0), h=9;
          ctx.beginPath(); ctx.moveTo(x1,y1);
          ctx.lineTo(x1-h*Math.cos(a-0.42), y1-h*Math.sin(a-0.42));
          ctx.lineTo(x1-h*Math.cos(a+0.42), y1-h*Math.sin(a+0.42));
          ctx.closePath(); ctx.fill(); ctx.restore();
        }
        function label(txt,x,y,color,size,align){
          ctx.save(); ctx.fillStyle=color;
          ctx.font='700 '+(size||13)+'px -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif';
          ctx.textAlign=align||'left'; ctx.textBaseline='middle'; ctx.fillText(txt,x,y); ctx.restore();
        }
        // ----- painel esquerdo: perfis de altura (subidas) -----
        var Lx0=60, Lx1=348, Ly0=66, Ly1=372, FLO=1.0, FHI=3.55;
        function hx(th){return Lx0+(th/TH)*(Lx1-Lx0);}
        function hy(f){return Ly1-(f-FLO)/(FHI-FLO)*(Ly1-Ly0);}
        function drawHills(q12,q13){
          ctx.strokeStyle='#e2e5ea'; ctx.lineWidth=1;
          ctx.beginPath(); ctx.moveTo(Lx0,Ly1); ctx.lineTo(Lx1+6,Ly1); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(Lx0,Ly0-8); ctx.lineTo(Lx0,Ly1); ctx.stroke();
          // linha-guia da altura comum no canto
          ctx.strokeStyle='#edeff3'; ctx.setLineDash([2,3]);
          ctx.beginPath(); ctx.moveTo(Lx0,hy(Q11)); ctx.lineTo(Lx1,hy(Q11)); ctx.stroke(); ctx.setLineDash([]);
          // curvas
          function plot(fn,q,color){ ctx.strokeStyle=color; ctx.lineWidth=2.6; ctx.beginPath();
            for(var th=0;th<=TH+1e-9;th+=0.02){var x=hx(th),y=hy(fn(th,q)); if(th===0)ctx.moveTo(x,y); else ctx.lineTo(x,y);} ctx.stroke(); }
          plot(fA,q12,ACC); plot(fB,q13,PUR);
          // tangentes no canto: inclinacao = 2*Q1j por radiano
          var sA=2*q12, sB=2*q13, d=0.45;
          arrow(hx(0),hy(Q11),hx(d),hy(Q11+sA*d),ACC,2.4,[5,3]);
          arrow(hx(0),hy(Q11),hx(d),hy(Q11+sB*d),PUR,2.4,[5,3]);
          label('inclinação '+f1(sA), hx(d)+5, hy(Q11+sA*d), ACC, 12);
          label('inclinação '+f1(sB), hx(d)+5, hy(Q11+sB*d), PUR, 12);
          // ponto de canto (altura comum)
          ctx.fillStyle=RED; ctx.beginPath(); ctx.arc(hx(0),hy(Q11),5.5,0,2*Math.PI); ctx.fill();
          ctx.strokeStyle='#fff'; ctx.lineWidth=1.5; ctx.stroke();
          label('canto e1 (mesma altura)', hx(0)+8, hy(Q11)+16, RED, 11);
          // nomes das curvas
          label('subida {x1,x2}', hx(1.02), hy(fA(1.02,q12))-12, ACC, 11.5);
          label('subida {x1,x3}', hx(1.24), hy(fB(1.24,q13))+13, PUR, 11.5);
          // titulo + eixos
          label('como a variância sobe ao longo de cada arco', Lx0, Ly0-16, DARK, 12);
          label('ao longo do arco →', Lx1-118, Ly1+18, GREY, 10.5);
          ctx.save(); ctx.translate(Lx0-16,(Ly0+Ly1)/2); ctx.rotate(-Math.PI/2);
          label('variância f', 0,0, GREY, 10.5, 'center'); ctx.restore();
        }
        // ----- painel direito: vista de cima -----
        var OX=482, OY=372, SC=66;
        function ex(u){return OX+u*SC;}
        function ey(v){return OY-v*SC;}
        function drawTop(q12,q13){
          var sA=2*q12, sB=2*q13, ang=Math.atan2(sB,sA), deg=ang*180/Math.PI, bis=Math.abs(deg-45)<0.4;
          ctx.strokeStyle='#e2e5ea'; ctx.lineWidth=1;
          ctx.beginPath(); ctx.moveTo(OX-42,OY); ctx.lineTo(CSSW-14,OY); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(OX,46); ctx.lineTo(OX,CSSH-26); ctx.stroke();
          ctx.lineWidth=2.2; ctx.strokeStyle=ACC; ctx.beginPath();
          for(var u=-0.4;u<=2.7;u+=0.05){var yy=-0.06*u*u; if(u<=-0.4)ctx.moveTo(ex(u),ey(yy)); else ctx.lineTo(ex(u),ey(yy));}
          ctx.stroke();
          ctx.strokeStyle=PUR; ctx.beginPath();
          for(var v=-0.4;v<=2.5;v+=0.05){var xx=-0.06*v*v; if(v<=-0.4)ctx.moveTo(ex(xx),ey(v)); else ctx.lineTo(ex(xx),ey(v));}
          ctx.stroke();
          ctx.strokeStyle=GREY; ctx.lineWidth=1.1; ctx.setLineDash([3,3]);
          ctx.beginPath(); ctx.arc(OX,OY,2.0*SC,-Math.PI/2,0); ctx.stroke(); ctx.setLineDash([]);
          label('||x||=1 (fixo)', ex(0.5), ey(1.95), GREY, 10.5);
          arrow(ex(0),ey(0),ex(1.78),ey(1.78),AMB,1.5,[2,4]);
          label('45°', ex(1.58),ey(1.8), AMB, 11.5);
          ctx.strokeStyle=GREY; ctx.lineWidth=1; ctx.setLineDash([2,3]);
          ctx.beginPath(); ctx.moveTo(ex(sA),ey(0)); ctx.lineTo(ex(sA),ey(sB)); ctx.lineTo(ex(0),ey(sB)); ctx.stroke();
          ctx.setLineDash([]);
          arrow(ex(0),ey(0),ex(sA),ey(0),ACC,3.2);
          arrow(ex(0),ey(0),ex(0),ey(sB),PUR,3.2);
          arrow(ex(0),ey(0),ex(sA),ey(sB),(bis?GRN:DARK),2.8,[6,4]);
          ctx.strokeStyle=DARK; ctx.lineWidth=1.4; ctx.beginPath(); ctx.arc(OX,OY,30,-ang,0); ctx.stroke();
          label(f1(deg)+'°', OX+42*Math.cos(-ang/2), OY+42*Math.sin(-ang/2), DARK, 12);
          label(f1(sA), ex(sA/2), ey(0)+18, ACC, 12, 'center');
          label(f1(sB), ex(0)-18, ey(sB/2), PUR, 12, 'center');
          label(bis?'bissecta':'pende', ex(sA)+8, ey(sB)-6, (bis?GRN:RED), 12.5);
          ctx.fillStyle=RED; ctx.beginPath(); ctx.arc(OX,OY,5.5,0,2*Math.PI); ctx.fill();
          ctx.strokeStyle='#fff'; ctx.lineWidth=1.5; ctx.stroke();
          label('vista de cima: o garfo', OX-42, 58, DARK, 12);
          return {sA:sA,sB:sB,deg:deg,bis:bis};
        }
        function draw(){
          ctx.clearRect(0,0,CSSW,CSSH);
          var q12=1.0+0.4*t, q13=1.0-0.4*t;
          drawHills(q12,q13);
          ctx.strokeStyle='#eceef2'; ctx.lineWidth=1;
          ctx.beginPath(); ctx.moveTo(404,52); ctx.lineTo(404,CSSH-26); ctx.stroke();
          var r=drawTop(q12,q13);
          saEl.textContent=f1(r.sA); sbEl.textContent=f1(r.sB);
          angEl.textContent=f1(r.deg)+'°'; angEl.style.color=(r.bis?GRN:DARK);
          labEl.textContent=r.bis?'simétrico':'assimétrico';
        }
        function frame(){
          if(sweeping){ t+=dir*0.006; if(t>=1){t=1;dir=-1;} if(t<=0){t=0;dir=1;} slider.value=Math.round(t*1000); }
          draw(); requestAnimationFrame(frame);
        }
        slider.addEventListener('input', function(){ t=slider.value/1000; sweeping=false; sweepBtn.textContent='▶ Varrer assimetria'; });
        sweepBtn.addEventListener('click', function(){ sweeping=!sweeping; sweepBtn.textContent=sweeping?'⏸ Pausar':'▶ Varrer assimetria'; });
        requestAnimationFrame(frame);
      })();
      </script>"""
pat1 = re.compile(r'<div class="anim-wrap" id="s2qanim">.*?</script>', re.DOTALL)
html, n1 = pat1.subn(lambda m: NEW_ANIM, html)
assert n1 == 1, ("op1 anim", n1)

# =================================================================== op2: caixa contra-intuicao (deepen + remove precisao)
NEW_WARN = r"""<span class="tag">Contra-intuição: a normalização NÃO simetriza o garfo</span>
        <p>Tentador: a esfera \(\|x\|=1\) é simétrica em <em>toda</em> direção — então ela não deveria igualar os
        dois arcos e forçar a bissecção? <strong>Não — e vale entender exatamente por quê.</strong> A normalização
        mexe no <strong>conjunto onde você pode estar</strong> (o domínio), não na <strong>função que você mede</strong>
        em cima dele.</p>
        <p><strong>Por que um círculo de raio 1, afinal?</strong> A variância é \(x^\top Q x\); se você não amarra o
        tamanho de \(x\), basta esticá-lo para a variância crescer sem limite — a pergunta viraria "quão grande?", e
        não "em qual direção?". Fixar \(\|x\|=1\) tira o tamanho da jogada e deixa só a <strong>direção</strong> (é a
        mesma razão da §2.1; o raio exato é convenção — \(2\) ou \(5\) dariam a mesma direção ótima, só reescalariam o
        valor). E esse círculo é <strong>isotrópico</strong>: é idêntico em todas as direções, então de fato trata
        \(e_2\) e \(e_3\) <em>do mesmo jeito</em>.</p>
        <p><strong>Então por que a inclinação não fica simétrica?</strong> Porque a inclinação não é uma propriedade do
        <em>círculo</em> — é da <strong>função</strong> \(f=x^\top Q x\) que vive em cima dele. E \(f\) <em>não</em> é
        isotrópica: \(Q\) não é um múltiplo da identidade, então ela sobe em <strong>ritmos diferentes</strong> em
        direções diferentes — esse é justamente o trabalho do \(Q\), guardar quanta variância existe em cada direção. O
        círculo iguala o <strong>comprimento</strong> dos passos (as tangentes têm norma 1); quem decide a
        <strong>taxa de subida</strong> de cada passo é o \(Q\). Resultado: passos do mesmo tamanho, subidas diferentes
        — \(2{,}4\) contra \(1{,}6\). A bissecção só voltaria se \(Q\) fosse isotrópico nesses dois acoplamentos
        (\(Q_{12}=Q_{13}\)), isto é, se a própria função subisse igual pelos dois arcos — nada que a esfera possa
        causar. Em uma frase: <strong>a normalização simetriza o recipiente, não o conteúdo.</strong></p>
      </div>"""
pat2 = re.compile(r'<span class="tag">Contra-intuição: a normalização NÃO simetriza o garfo</span>.*?</div>', re.DOTALL)
html, n2 = pat2.subn(lambda m: NEW_WARN, html)
assert n2 == 1, ("op2 warning", n2)

# =================================================================== integrity + write
ok, rep = integrity(html, 10)
print("integrity:", ok)
for k, v in rep.items():
    print("  ", k, v)
assert ok, rep
open(DOC, "w", encoding="utf-8").write(html)
print("OK: anim 2-paineis + caixa contra-intuicao atualizadas.")
