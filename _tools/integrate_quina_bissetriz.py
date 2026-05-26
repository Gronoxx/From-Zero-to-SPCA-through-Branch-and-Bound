#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Expande a secao da quina na doc 02: anota a figura do garfo, adiciona a caixa
'intuicao do meio' (bissecao), a animacao interativa #s2qanim (garfo x bissetriz),
a figura comparativa simetrico-vs-assimetrico, a caixa 'normalizacao nao simetriza'
(+ precisao infinita), a sutileza 'ingreme != fundo' e um cheque socratico.
Usa regex tolerante + lambda (nao mistura escapes de MathJax) + embed + integrity."""
import re, sys
sys.path.insert(0, "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools")
from al_template import embed, integrity

DOC = "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/02_sparse_pca_o_problema.html"
FIG_FORK = "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools/fig_quina_fork.png"
FIG_BISS = "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools/fig_quina_bissetriz.png"

html = open(DOC, encoding="utf-8").read()

# ---------------------------------------------------------------- op1: figura do garfo (re-embed anotada)
NEW_FORK = r"""<figure>
        <img src="" alt="garfo quina anotado">
        <figcaption>Zoom no canto \(e_1\), no plano das direções \(e_2\) e \(e_3\). Os dois arcos (pedaços
        \(\{x_1,x_2\}\) e \(\{x_1,x_3\}\)) cruzam \(e_1\) com tangentes \(e_2\) e \(e_3\) — um ângulo de 90°. O
        gradiente (cinza, tracejado) é <em>um</em> vetor; suas projeções nos dois pedaços (azul e roxa) são as
        <strong>inclinações</strong> ao longo de cada arco: \(2Q_{12}=2{,}4\) e \(2Q_{13}=1{,}6\). Ele é a
        <strong>diagonal</strong> do retângulo com esses lados — como o retângulo é mais largo que alto, a
        diagonal <strong>pende</strong> para \(\{x_1,x_2\}\) (\(\approx 33{,}7^\circ\)) e <em>não</em> coincide
        com a bissetriz de 45° (âmbar). Escolher um ramo é escolher o suporte.</figcaption>
      </figure>"""
pat1 = re.compile(r'<figure>\s*<img [^>]*data:image/png;base64[^>]*>\s*<figcaption>\s*Zoom no canto.*?</figcaption>\s*</figure>', re.DOTALL)
html, n1 = pat1.subn(lambda m: NEW_FORK, html)
assert n1 == 1, ("op1 figura garfo", n1)

# ---------------------------------------------------------------- op3: bloco novo ANTES da caixa "O truque"
NEW_CHUNK = r"""      <div class="box intuition">
        <span class="tag">A intuição do meio — quase certa (e por que falha)</span>
        <p>Falta uma pergunta: para onde, <em>exatamente</em>, esse gradiente aponta — ele divide o ângulo do
        garfo <strong>ao meio</strong>? A tentação é dizer que sim, e o raciocínio parece sólido: dê um zoom
        enorme na quina; os dois arcos viram suas <strong>retas tangentes</strong> (\(e_2\) e \(e_3\), a 90°); o
        gradiente seria "a combinação das duas tangentes" — logo cairia bem no meio, a 45°.</p>
        <p><strong>Onde escorrega.</strong> "Combinação das tangentes" não significa combinação <em>com pesos
        iguais</em>. Num referencial ortonormal \(\{e_2,e_3\}\), as componentes do gradiente <strong>são</strong>
        as inclinações (derivadas direcionais) ao longo de cada arco:</p>
        <div class="formula">\[ \nabla_{\!\text{tan}} f \;=\; \underbrace{2Q_{12}}_{\text{inclinação em }\{x_1,x_2\}}\, e_2 \;+\; \underbrace{2Q_{13}}_{\text{inclinação em }\{x_1,x_3\}}\, e_3 \;=\; 2{,}4\,e_2 \;+\; 1{,}6\,e_3 . \]</div>
        <p>Ou seja: o gradiente é a <strong>diagonal de um retângulo</strong> cujos lados são as duas inclinações.
        A diagonal só corta o ângulo reto ao meio se o retângulo for um <strong>quadrado</strong> — isto é, se
        \(2Q_{12}=2Q_{13}\). Como aqui \(2{,}4 \gt 1{,}6\), ela <strong>pende</strong> para o arco mais íngreme
        \(\{x_1,x_2\}\), fazendo \(\arctan(1{,}6/2{,}4)\approx 33{,}7^\circ\) com \(e_2\) — não 45°. Bissecta
        <em>só</em> no caso simétrico \(Q_{12}=Q_{13}\). Arraste o controle abaixo para ver a transição.</p>
      </div>
      <div class="anim-wrap" id="s2qanim">
        <div class="anim-head">
          <span class="anim-title">Animação interativa — o garfo e a bissetriz</span>
          <span class="anim-sub">arraste a assimetria (ou use Varrer): o gradiente é a diagonal do retângulo · só vira 45° quando os lados (as inclinações) se igualam · o círculo \(\|x\|=1\) é o mesmo o tempo todo</span>
        </div>
        <canvas id="s2qanim-cv" width="700" height="440" aria-label="Animacao do gradiente na quina pendendo para o arco mais ingreme e bissectando so no caso simetrico"></canvas>
        <div class="anim-ctrl">
          <button id="s2qanim-sweep" class="anim-btn" type="button">▶ Varrer assimetria</button>
          <input id="s2qanim-slider" type="range" min="0" max="1000" value="500" aria-label="Assimetria entre as duas inclinacoes">
          <span id="s2qanim-lab" class="anim-tval">assimétrico</span>
        </div>
        <div class="anim-hud">
          <div><span class="hud-k">inclinação {x₁,x₂}</span><span id="s2qanim-sa" class="hud-v">2,4</span></div>
          <div><span class="hud-k">inclinação {x₁,x₃}</span><span id="s2qanim-sb" class="hud-v">1,6</span></div>
          <div><span class="hud-k">ângulo do gradiente</span><span id="s2qanim-ang" class="hud-v">33,7°</span></div>
        </div>
      </div>
      <style>
        #s2qanim{border:1px solid var(--line);border-radius:16px;background:#fff;
          padding:14px 14px 16px;margin:20px 0;box-shadow:0 3px 14px rgba(20,30,60,.07)}
        #s2qanim .anim-head{display:flex;flex-direction:column;gap:2px;margin-bottom:10px}
        #s2qanim .anim-title{font-weight:800;color:#1a2230;font-size:15px}
        #s2qanim .anim-sub{font-size:12.5px;color:var(--muted);font-style:italic}
        #s2qanim canvas{display:block;width:100%;max-width:700px;height:auto;margin:0 auto;
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
        var CSSW=700, CSSH=440;
        cv.width=CSSW*dpr; cv.height=CSSH*dpr; ctx.scale(dpr,dpr);
        var OX=150, OY=372, SCALE=92;
        var ACC='#3b54c4', PUR='#7a3fc4', GREY='#9aa0aa', DARK='#1f3b6e', RED='#b23b3b', GRN='#1f9a55', AMB='#c2790a';
        var saEl=document.getElementById('s2qanim-sa'), sbEl=document.getElementById('s2qanim-sb'),
            angEl=document.getElementById('s2qanim-ang'), slider=document.getElementById('s2qanim-slider'),
            sweepBtn=document.getElementById('s2qanim-sweep'), labEl=document.getElementById('s2qanim-lab');
        var t=0.5, sweeping=false, dir=1;
        function ex(u){return OX+u*SCALE;}
        function ey(v){return OY-v*SCALE;}
        function f1(v){return v.toFixed(1).replace('.',',');}
        function slopes(tt){return [2.0+0.8*tt, 2.0-0.8*tt];}
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
        function draw(){
          ctx.clearRect(0,0,CSSW,CSSH);
          var sp=slopes(t), sA=sp[0], sB=sp[1];
          var ang=Math.atan2(sB,sA), deg=ang*180/Math.PI, bis=Math.abs(deg-45)<0.4;
          ctx.strokeStyle='#e2e5ea'; ctx.lineWidth=1;
          ctx.beginPath(); ctx.moveTo(40,OY); ctx.lineTo(CSSW-20,OY); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(OX,28); ctx.lineTo(OX,CSSH-26); ctx.stroke();
          // arcos viaveis (tangentes e2, e3), levemente curvos
          ctx.lineWidth=2.4; ctx.strokeStyle=ACC; ctx.beginPath();
          for(var u=-0.4;u<=2.7;u+=0.05){var yy=-0.06*u*u; if(u<=-0.4)ctx.moveTo(ex(u),ey(yy)); else ctx.lineTo(ex(u),ey(yy));}
          ctx.stroke();
          ctx.strokeStyle=PUR; ctx.beginPath();
          for(var v=-0.4;v<=2.4;v+=0.05){var xx=-0.06*v*v; if(v<=-0.4)ctx.moveTo(ex(xx),ey(v)); else ctx.lineTo(ex(xx),ey(v));}
          ctx.stroke();
          // quarto de circulo ||x||=1 (FIXO)
          ctx.strokeStyle=GREY; ctx.lineWidth=1.2; ctx.setLineDash([3,3]);
          ctx.beginPath(); ctx.arc(OX,OY,2.0*SCALE,-Math.PI/2,0); ctx.stroke(); ctx.setLineDash([]);
          label('||x|| = 1 (fixo)', ex(0.62), ey(1.86), GREY, 12);
          // bissetriz 45
          arrow(ex(0),ey(0),ex(1.72),ey(1.72),AMB,1.6,[2,4]);
          label('bissetriz 45°', ex(1.5), ey(1.78), AMB, 12.5);
          // retangulo (lados = inclinacoes)
          ctx.strokeStyle=GREY; ctx.lineWidth=1; ctx.setLineDash([2,3]);
          ctx.beginPath(); ctx.moveTo(ex(sA),ey(0)); ctx.lineTo(ex(sA),ey(sB)); ctx.lineTo(ex(0),ey(sB)); ctx.stroke();
          ctx.setLineDash([]);
          // projecoes (os lados do retangulo)
          arrow(ex(0),ey(0),ex(sA),ey(0),ACC,3.4);
          arrow(ex(0),ey(0),ex(0),ey(sB),PUR,3.4);
          // gradiente (diagonal)
          arrow(ex(0),ey(0),ex(sA),ey(sB),(bis?GRN:DARK),3.0,[6,4]);
          // arco do angulo
          ctx.strokeStyle=DARK; ctx.lineWidth=1.5;
          ctx.beginPath(); ctx.arc(OX,OY,34,-ang,0); ctx.stroke();
          label(f1(deg)+'°', OX+46*Math.cos(-ang/2), OY+46*Math.sin(-ang/2), DARK, 13);
          // rotulos das inclinacoes (lados)
          label(f1(sA), ex(sA/2), ey(0)+20, ACC, 13, 'center');
          label(f1(sB), ex(0)-22, ey(sB/2), PUR, 13, 'center');
          // status
          label(bis?'bissecta (45°)':'pende p/ {x1,x2}', ex(sA)+10, ey(sB)-8, (bis?GRN:RED), 13.5);
          // e1
          ctx.fillStyle=RED; ctx.beginPath(); ctx.arc(OX,OY,6,0,2*Math.PI); ctx.fill();
          ctx.strokeStyle='#fff'; ctx.lineWidth=1.6; ctx.stroke();
          label('quina e1', OX-2, OY+24, RED, 12.5, 'center');
          // HUD
          saEl.textContent=f1(sA); sbEl.textContent=f1(sB);
          angEl.textContent=f1(deg)+'°'; angEl.style.color=(bis?GRN:DARK);
          labEl.textContent=bis?'simétrico':'assimétrico';
        }
        function frame(){
          if(sweeping){ t+=dir*0.006; if(t>=1){t=1;dir=-1;} if(t<=0){t=0;dir=1;} slider.value=Math.round(t*1000); }
          draw(); requestAnimationFrame(frame);
        }
        slider.addEventListener('input', function(){ t=slider.value/1000; sweeping=false; sweepBtn.textContent='▶ Varrer assimetria'; });
        sweepBtn.addEventListener('click', function(){ sweeping=!sweeping; sweepBtn.textContent=sweeping?'⏸ Pausar':'▶ Varrer assimetria'; });
        requestAnimationFrame(frame);
      })();
      </script>
      <figure>
        <img src="" alt="bissetriz simetrico vs assimetrico">
        <figcaption>O gradiente é a <strong>diagonal</strong> de um retângulo cujos lados são as inclinações ao
        longo de cada arco. <strong>Esquerda</strong> (simétrico, \(Q_{12}=Q_{13}\)): lados iguais → quadrado →
        a diagonal cai a <strong>45°</strong> e <em>bissecta</em>. <strong>Direita</strong> (assimétrico,
        \(Q_{12}\gt Q_{13}\); o nosso caso, \(2{,}4\) e \(1{,}6\)): retângulo deitado → a diagonal
        <strong>pende</strong> para \(\{x_1,x_2\}\) (\(\approx 33{,}7^\circ\)). O quarto de círculo \(\|x\|=1\) é
        <strong>idêntico</strong> nos dois painéis — quem cria a assimetria é o \(Q\), não a normalização.</figcaption>
      </figure>
      <div class="box warning">
        <span class="tag">Contra-intuição: a normalização NÃO simetriza o garfo</span>
        <p>Tentador: a esfera \(\|x\|=1\) é simétrica em <em>toda</em> direção — então ela não deveria igualar os
        dois arcos e forçar a bissecção? <strong>Não.</strong> A normalização torna as duas tangentes
        <em>vetores de comprimento 1</em> (uma comparação justa "por passo unitário"), mas a <strong>inclinação
        por passo</strong> continua \(2{,}4\) contra \(1{,}6\). A esfera é isotrópica: trata \(e_2\) e \(e_3\)
        igualzinho, então não <em>cria</em> nem <em>desfaz</em> assimetria. A assimetria vem inteira do \(Q\) (dos
        acoplamentos \(Q_{12}\) vs \(Q_{13}\)). Em uma frase: a normalização iguala o <strong>comprimento do
        passo</strong>, não a <strong>inclinação</strong>.</p>
        <p><strong>E a precisão infinita?</strong> Também não fecha o garfo — porque o garfo não é erro numérico.
        Mesmo com aritmética exata, o gradiente aponta <em>estritamente entre</em> os dois arcos: segui-lo encheria
        \(x_1\), \(x_2\) <em>e</em> \(x_3\) ao mesmo tempo — três coordenadas não-nulas, inviável para \(k=2\). Não
        dá para segui-lo; é preciso <strong>projetar</strong> em um dos arcos. O garfo é a <strong>não-suavidade do
        conjunto</strong> (um ponto singular, onde dois pedaços se colam), não falta de casas decimais. Zoom nenhum
        muda a direção do gradiente — ela continua \(33{,}7^\circ\).</p>
      </div>
      <p>Então o método guloso "desce pelo arco mais íngreme" — o de maior inclinação, que é a <strong>maior
      componente do gradiente</strong>. E essa é <em>exatamente</em> a variável que o truncamento mantém: é o que
      a próxima caixa mostra.</p>
"""
pat3 = re.compile(r'( *)<div class="box deep">\s*<span class="tag">O truque .*?por que ele salta</span>', re.DOTALL)
html, n3 = pat3.subn(lambda m: NEW_CHUNK + m.group(0), html)
assert n3 == 1, ("op3 bloco intuicao/anim/warning", n3)

# ---------------------------------------------------------------- op4: sutileza + cheque DEPOIS do "Moral"
NEW_TAIL = r"""
      <div class="box deep">
        <span class="tag">Sutileza: "mais íngreme na quina" ≠ "bacia mais funda"</span>
        <p>Um último cuidado, porque é fácil tropeçar aqui. A <strong>inclinação na quina</strong> (o que decide o
        pendor do gradiente) é \(2Q_{1j}\) — depende <em>só</em> do acoplamento. Já a <strong>profundidade da
        bacia</strong> de cada pedaço (quanta variância dá para extrair ali) é \(\lambda_{\max}\) da submatriz
        \(2\times2\) \(Q_{\{1,j\}}\) — depende de \(Q_{11}\), \(Q_{jj}\) <em>e</em> \(Q_{1j}\) juntos. São coisas
        diferentes: o arco mais íngreme no canto <strong>pode levar à bacia menos funda</strong>.</p>
        <p>Veja num \(Q\) concreto (positivo-semidefinido, como toda matriz de covariância):</p>
        <div class="formula">\[ Q=\begin{pmatrix} 2 & 1{,}2 & 0{,}8\\ 1{,}2 & 1{,}0 & 0\\ 0{,}8 & 0 & 3 \end{pmatrix} \;\Rightarrow\; \begin{array}{l} \{x_1,x_2\}:\ \text{inclinação } 2{,}4\ (\text{mais íngreme}),\ \lambda_{\max}=2{,}80 \\[3pt] \{x_1,x_3\}:\ \text{inclinação } 1{,}6,\ \lambda_{\max}=3{,}44\ (\text{mais fundo}) \end{array} \]</div>
        <p>O guloso pegaria \(\{x_1,x_2\}\) (o mais íngreme) e cairia na bacia <em>menos</em> funda. No \(Q\) que
        usamos nas figuras os dois critérios por acaso <strong>coincidem</strong> (\(\lambda_{\max}=3{,}30\) contra
        \(2{,}63\)) — por isso ele parece "bem-comportado" ali; mas é coincidência. <strong>A moral da
        sutileza:</strong> nem a direção do gradiente, nem a maior componente, nem o truncamento garantem o melhor
        pedaço. É por isso que a escolha é mesmo <strong>combinatória</strong> — o que motiva o Branch-and-Bound
        (§5) em vez de confiar num passo guloso.</p>
      </div>
      <div class="box check">
        <span class="tag">Cheque rápido (responda antes de seguir)</span>
        <ol>
          <li>Se \(Q_{12}=Q_{13}\), o gradiente bissecta o ângulo do garfo? E se, <em>além disso</em>,
          \(Q_{22}\gg Q_{33}\): qual arco leva à bacia mais funda — o gradiente "sabe" disso?</li>
          <li>Por que aumentar a precisão numérica (mais casas decimais) <em>não</em> dissolve o garfo?</li>
          <li>Na figura do garfo, por que a seta azul (projeção em \(\{x_1,x_2\}\)) é mais comprida que a roxa?</li>
        </ol>
      </div>"""
pat4 = re.compile(r'uma busca por tentativa.{0,5}combinat\wria\.</p>')
html, n4 = pat4.subn(lambda m: m.group(0) + NEW_TAIL, html)
assert n4 == 1, ("op4 sutileza/cheque", n4)

# ---------------------------------------------------------------- embed + integrity
html = embed(html, {"garfo quina anotado": FIG_FORK,
                    "bissetriz simetrico vs assimetrico": FIG_BISS})
ok, rep = integrity(html, 10)
print("integrity:", ok)
for k, v in rep.items():
    print("  ", k, v)
assert ok, rep

open(DOC, "w", encoding="utf-8").write(html)
print("OK: doc 02 atualizada.")
