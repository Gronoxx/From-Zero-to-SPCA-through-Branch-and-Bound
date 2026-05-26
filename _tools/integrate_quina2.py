#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reescreve a caixa 'O que a quina faz com o gradiente' em convencao de MINIMIZACAO,
adiciona subtopico 'na quina' (garfo) + figura, mecanismo 'passo+truncar' + figura + animacao,
e vira a animacao existente (s2anim) para descida. embed 3 figuras + integrity + checagens."""
import re, sys
sys.path.insert(0, "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools")
from al_template import embed, integrity

BASE="/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico"
DOC=BASE+"/02_sparse_pca_o_problema.html"
FIG_REL=BASE+"/_tools/fig_quina_gradiente.png"
FIG_FORK=BASE+"/_tools/fig_quina_fork.png"
FIG_TRUNC=BASE+"/_tools/fig_truncamento.png"

NEW = r"""<div class="box deep">
        <span class="tag">O que a quina faz com o gradiente</span>
        <p><strong>Uma convenção primeiro.</strong> Em otimização o padrão é <em>minimizar</em> (e descer o
        gradiente), e é assim que o curso trata tudo. Nosso problema <em>maximiza</em> variância; para deixá-lo
        na forma de minimização basta <strong>trocar o sinal</strong>: \(\min\,-x^\top Q x\). Não é
        \(\min\,x^\top Q x\) — esse seria a direção de <em>menor</em> variância, outro problema. Com a troca de
        sinal o relevo vira de cabeça para baixo: pense em <strong>descer</strong>, e o melhor componente é o
        <strong>vale mais fundo</strong> (mais variância). A §3 ainda escreve \(\max\); é a mesma coisa.</p>
        <p><strong>O que "descer o gradiente" quer dizer.</strong> Numa superfície <em>lisa</em>, em cada ponto
        há <em>uma</em> direção de descida mais íngreme. O método é uma bolinha rolando morro abaixo: ache essa
        direção, dê um passo, repita. Você para no <strong>fundo de um vale</strong> (um mínimo), onde o gradiente
        zera.</p>
        <p><strong>Cenário 1 — dentro de um pedaço (suporte fixo).</strong> Fixe \(k\) variáveis, digamos
        \(\{x_1,x_2\}\): os vetores permitidos formam um circulozinho liso. A descida funciona perfeitamente e
        te leva ao <strong>fundo da bacia daquele pedaço</strong> — o autovetor de cima da submatriz
        \(2\times2\) \(Q_{\{1,2\}}\) (mais variância usando essas duas variáveis). Esse fundo fica no
        <em>meio</em> do arco, usando <em>as duas</em> variáveis: é <strong>interior</strong>, <em>não</em> uma
        quina. A descida para ali; nunca chega a um ponto de eixo. (Painel A.)</p>
        <p><strong>Por que falha, então?</strong> Por <strong>aprisionamento</strong>. Cada pedaço é uma bacia, e
        as bacias têm <strong>profundidades diferentes</strong> — o melhor global é a mais funda. A descida te
        entrega o fundo da bacia <em>em que você caiu</em>, que pode ser a errada. Parado no fundo de uma bacia
        rasa, o gradiente não enxerga que existe uma bacia mais funda ao lado. (Painel B: a bolinha rola e fica
        <strong>presa</strong> num mínimo subótimo.)</p>
        <p><strong>O papel da quina.</strong> Na união, as bacias se encontram nas quinas — que agora são
        <strong>cristas</strong> (picos pontudos) entre as bacias. Na crista a superfície <strong>não é
        lisa</strong>: dois arcos se cruzam, cada um com a sua tangente, então não há "a" direção de descida —
        há duas. Consequências: <em>(i)</em> a descida dentro de uma bacia nem <strong>chega</strong> à crista
        (para antes, no fundo); e <em>(ii)</em> para trocar de bacia seria preciso <strong>subir</strong> a
        crista e descer do outro lado — e descida não sobe. Por isso o gradiente fica preso na bacia onde
        começou.</p>
      </div>
      <figure>
        <img src="" alt="quina gradiente relevo">
        <figcaption>Convenção de minimização: o eixo vertical é \(-x^\top Q x\) (quanto mais fundo, mais
        variância). <strong>Esquerda (A) — dentro de um pedaço.</strong> O pedaço \(\{x_1,x_2\}\) é um
        circulozinho liso, aqui "desenrolado"; a descida rola pelos dois lados até o <strong>fundo da bacia</strong>
        (âmbar) — o autovetor, que usa as duas variáveis — e para ali. Os pontos de eixo \(e_1,e_2\) (vermelho)
        são onde, <em>na união</em>, se colam outros pedaços; neste pedaço <em>sozinho</em> a curva passa por
        eles lisa. O morro lá pelos 135° é a direção de <em>menor</em> variância. <strong>Direita (B) — a
        união.</strong> Percorrendo a borda \(e_1\to e_2\to e_3\to e_1\), os três pedaços aparecem emendados:
        três <strong>bacias</strong> de profundidades diferentes, separadas por <strong>cristas</strong>
        (vermelho) onde a curva tem um vinco. A bolinha preta, solta na encosta do pedaço \(\{x_2,x_3\}\), rola e
        fica <strong>presa</strong> no fundo daquela bacia (subótima). O melhor global (bacia mais funda,
        \(\{x_1,x_2\}\)) está do outro lado de uma crista: para alcançá-lo a bolinha teria que <em>subir</em> a
        crista — coisa que a descida nunca faz.</figcaption>
      </figure>
      <div class="anim-wrap" id="s2anim">
        <div class="anim-head">
          <span class="anim-title">Animação interativa — o gradiente preso num mínimo local</span>
          <span class="anim-sub">arraste a partida e solte: a bolinha rola morro abaixo e para no fundo da bacia onde caiu · tente vários pontos</span>
        </div>
        <canvas id="s2anim-cv" width="700" height="430" aria-label="Animacao do gradiente descendo o relevo dos pedacos e ficando preso num minimo local subotimo"></canvas>
        <div class="anim-ctrl">
          <button id="s2anim-drop" class="anim-btn" type="button">▶ Soltar bolinha</button>
          <input id="s2anim-slider" type="range" min="0" max="1000" value="430" aria-label="Ponto de partida da bolinha">
          <span id="s2anim-pos" class="anim-tval">partida</span>
        </div>
        <div class="anim-hud">
          <div><span class="hud-k">objetivo −xᵀQx</span><span id="s2anim-f" class="hud-v">—</span></div>
          <div><span class="hud-k">melhor (mais fundo)</span><span id="s2anim-best" class="hud-v">−3,30</span></div>
          <div><span class="hud-k">situação</span><span id="s2anim-stat" class="hud-v">solte a bolinha</span></div>
        </div>
      </div>
      <div class="box deep">
        <span class="tag">E se conseguíssemos chegar — ou inicializar — na quina?</span>
        <p>Pergunta natural: se a crista é o ponto que liga as bacias, e se <em>começássemos</em> exatamente
        nela? Não resolve — e entender por quê esclarece o resto.</p>
        <p><strong>O gradiente continua bem-definido; quem não é liso é o conjunto.</strong> A função
        \(x^\top Q x\) é suave e seu gradiente na quina é um vetor perfeitamente normal. O problema está no
        <strong>conjunto viável</strong>: na quina passam <em>dois</em> arcos (dois pedaços), com <em>duas</em>
        tangentes. Projetar o gradiente "na direção permitida" dá então <strong>duas respostas</strong> — uma por
        pedaço (figura abaixo). É um <strong>garfo</strong>.</p>
        <p>E o garfo é justamente a decisão que queríamos evitar:</p>
        <ul>
          <li><strong>Escolher um ramo = escolher o suporte.</strong> Seguir por um arco te compromete com um
          pedaço; o outro fica inexplorado. A escolha combinatória voltou.</li>
          <li><strong>A quina usa menos que \(k\) variáveis.</strong> \(e_1\) tem só uma coordenada não-nula
          (menos que \(k=2\)). Para usar o orçamento de \(k\) você precisa "entrar" com mais variáveis — ou
          seja, decidir <em>quais</em>. De novo a mesma escolha.</li>
          <li><strong>É um equilíbrio instável.</strong> A crista é um fio de navalha: qualquer passo numérico
          escorrega para um lado. O método não fica na quina.</li>
        </ul>
        <p>Ou seja: inicializar na quina não dissolve a dificuldade — apenas a transfere para "qual ramo
        seguir?", que é escolher o pedaço.</p>
      </div>
      <figure>
        <img src="" alt="quina garfo">
        <figcaption>Zoom no canto \(e_1\), no plano das direções \(e_2\) e \(e_3\). Os dois arcos (pedaços
        \(\{x_1,x_2\}\) e \(\{x_1,x_3\}\)) se cruzam em \(e_1\) com tangentes diferentes. O gradiente (cinza,
        tracejado) é <em>um</em> vetor; projetado em cada pedaço dá <em>duas</em> direções de descida (azul e
        roxa) — o garfo. Escolher uma delas é escolher o suporte.</figcaption>
      </figure>
      <div class="box deep">
        <span class="tag">O truque "dar o passo e depois truncar" — e por que ele salta</span>
        <p>Há uma tentativa esperta de fazer a descida <em>pular</em> entre pedaços, em vez de ficar presa em
        um. Cada iteração tem duas etapas (figura abaixo):</p>
        <ol>
          <li><strong>Dê o passo no espaço inteiro \(\mathbb{R}^n\)</strong>, ignorando a esparsidade:
          \(x' = x + \eta\,\nabla\). Isso <strong>enche todas</strong> as variáveis — \(x'\) fica denso.</li>
          <li><strong>Trunque de volta para \(k\) variáveis:</strong> mantenha as \(k\) maiores em módulo, zere o
          resto e <strong>renormalize</strong> (para voltar à norma 1).</li>
        </ol>
        <p>O passo "espalha"; o truncamento "re-esparsa". Iterando, às vezes a descida realmente troca de pedaço
        — o que o gradiente puro, preso numa bacia, não fazia.</p>
        <p><strong>Mas o truncar é descontínuo — e é aí que mora o "salta".</strong> Manter "as \(k\) maiores"
        depende da <em>ordem</em> dos tamanhos. Quando duas componentes <strong>quase empatam</strong> em módulo,
        uma mudança minúscula em \(x'\) troca qual delas sobrevive — e o <strong>suporte salta</strong> de um
        pedaço para outro de uma vez. Não há meio-termo: ou a variável está, ou não está. (Animação: deslize
        \(\eta\); quando as componentes 2 e 3 cruzam, o suporte — e a posição no relevo — <strong>teleporta</strong>
        de uma bacia para outra.) Por isso a busca <em>pula</em>, não <em>desliza</em>; e onde ela para depende de
        onde começou.</p>
      </div>
      <figure>
        <img src="" alt="truncamento barras">
        <figcaption>Uma iteração do mecanismo, em barras (componentes \(x_1,x_2,x_3\)). (1) \(x\) atual,
        2-esparso. (2) o passo do gradiente enche todas as variáveis. (3) o truncamento mantém as \(k=2\) maiores
        em módulo e <em>zera</em> a menor (\(x_3\), tracejada em vermelho). (4) renormaliza para voltar à norma 1.
        Aqui o suporte continuou \(\{x_1,x_2\}\); a animação abaixo mostra quando ele <strong>salta</strong>.</figcaption>
      </figure>
      <div class="anim-wrap" id="s2tanim">
        <div class="anim-head">
          <span class="anim-title">Animação interativa — por que o truncamento salta</span>
          <span class="anim-sub">deslize o tamanho do passo \(\eta\) (ou use Varrer): quando as componentes 2 e 3 cruzam, o suporte teleporta de bacia</span>
        </div>
        <canvas id="s2tanim-cv" width="720" height="340" aria-label="Animacao do truncamento descontinuo: barras do vetor denso e teleporte do suporte no relevo"></canvas>
        <div class="anim-ctrl">
          <button id="s2tanim-sweep" class="anim-btn" type="button">▶ Varrer η</button>
          <input id="s2tanim-slider" type="range" min="0" max="1000" value="150" aria-label="Tamanho do passo eta">
          <span id="s2tanim-eta" class="anim-tval">η peq.</span>
        </div>
        <div class="anim-hud">
          <div><span class="hud-k">suporte mantido</span><span id="s2tanim-sup" class="hud-v">{1,2}</span></div>
          <div><span class="hud-k">componentes 2 e 3</span><span id="s2tanim-tie" class="hud-v">estável</span></div>
          <div><span class="hud-k">o que aconteceu</span><span id="s2tanim-jump" class="hud-v">—</span></div>
        </div>
      </div>
      <p><strong>Moral.</strong> Preso numa bacia (gradiente puro) ou pulando em saltos descontínuos (passo +
      truncamento), de nenhum jeito existe uma descida <em>lisa</em> que percorra todas as bacias e as compare. É
      isso que torna "qual suporte usar?" uma busca por tentativa — combinatória.</p>
      <style>
        #s2anim,#s2tanim{border:1px solid var(--line);border-radius:16px;background:#fff;
          padding:14px 14px 16px;margin:20px 0;box-shadow:0 3px 14px rgba(20,30,60,.07)}
        #s2anim .anim-head,#s2tanim .anim-head{display:flex;flex-direction:column;gap:2px;margin-bottom:10px}
        #s2anim .anim-title,#s2tanim .anim-title{font-weight:800;color:#1a2230;font-size:15px}
        #s2anim .anim-sub,#s2tanim .anim-sub{font-size:12.5px;color:var(--muted);font-style:italic}
        #s2anim canvas,#s2tanim canvas{display:block;width:100%;max-width:720px;height:auto;margin:0 auto;
          background:#fcfcfa;border:1px solid var(--line);border-radius:12px}
        #s2anim .anim-ctrl,#s2tanim .anim-ctrl{display:flex;align-items:center;gap:12px;margin:12px 2px 0}
        #s2anim .anim-btn,#s2tanim .anim-btn{appearance:none;border:1px solid var(--accent);background:var(--accent);
          color:#fff;font-weight:700;font-size:13.5px;padding:7px 14px;border-radius:9px;cursor:pointer;
          white-space:nowrap;font-family:inherit}
        #s2anim .anim-btn:hover,#s2tanim .anim-btn:hover{filter:brightness(1.06)}
        #s2anim input[type=range],#s2tanim input[type=range]{flex:1;accent-color:var(--accent);cursor:pointer}
        #s2anim .anim-tval,#s2tanim .anim-tval{font-variant-numeric:tabular-nums;color:#37414f;font-weight:700;
          font-size:13.5px;min-width:74px;text-align:right}
        #s2anim .anim-hud,#s2tanim .anim-hud{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px}
        #s2anim .anim-hud>div,#s2tanim .anim-hud>div{background:var(--slate-bg);border:1px solid var(--line);border-radius:10px;
          padding:8px 10px;display:flex;flex-direction:column;gap:3px}
        #s2anim .hud-k,#s2tanim .hud-k{font-size:11.5px;color:var(--muted);letter-spacing:.01em}
        #s2anim .hud-v,#s2tanim .hud-v{font-size:18px;font-weight:800;color:#1a2230;font-variant-numeric:tabular-nums}
        @media(max-width:560px){#s2anim .anim-hud,#s2tanim .anim-hud{grid-template-columns:1fr}}
      </style>
      <script>
      (function(){
        var cv=document.getElementById('s2anim-cv'); if(!cv) return;
        var ctx=cv.getContext('2d'); var dpr=window.devicePixelRatio||1;
        var CSSW=700, CSSH=430;
        cv.width=CSSW*dpr; cv.height=CSSH*dpr; ctx.scale(dpr,dpr);
        var ML=52, MR=18, MT=26, MB=46;
        var PW=CSSW-ML-MR, PH=CSSH-MT-MB;
        var SLO=0, SHI=3, VLO=-3.60, VHI=-1.25;   // V = -f ; mais fundo (mais negativo) embaixo
        var Q00=2.0,Q11=2.2,Q22=1.6,Q01=1.2,Q02=0.8,Q12=1.0;
        var COL=['#3b54c4','#7a3fc4','#1f9a55']; var RED='#b23b3b';
        var BEST=-3.304;
        function fperim(s){ s=((s%3)+3)%3; var t,c,n;
          if(s<1){t=s*Math.PI/2;c=Math.cos(t);n=Math.sin(t);return Q00*c*c+Q11*n*n+2*Q01*c*n;}
          else if(s<2){t=(s-1)*Math.PI/2;c=Math.cos(t);n=Math.sin(t);return Q11*c*c+Q22*n*n+2*Q12*c*n;}
          else{t=(s-2)*Math.PI/2;c=Math.cos(t);n=Math.sin(t);return Q22*c*c+Q00*n*n+2*Q02*c*n;} }
        function V(s){return -fperim(s);}
        function grad(s){var h=2e-4;return (fperim(s+h)-fperim(s-h))/(2*h);} // grad de f (subida em f = descida em V)
        function X(s){return ML+(s-SLO)/(SHI-SLO)*PW;}
        function Yv(v){return MT+(1-(v-VLO)/(VHI-VLO))*PH;}
        function fmt(v){return v.toFixed(2).replace('.',',');}
        var bots=[];
        for(var sid=0;sid<3;sid++){var bv=1e9,bs=sid+0.5;
          for(var u=0.001;u<0.999;u+=0.001){var ss=sid+u,vv=V(ss);if(vv<bv){bv=vv;bs=ss;}}
          bots.push([bs,bv]);}
        var CORN=[[0,'e1'],[1,'e2'],[2,'e3'],[3,'e1']];
        function drawCurve(){
          ctx.strokeStyle='#cfd2d8';ctx.lineWidth=1;
          ctx.beginPath();ctx.moveTo(ML,Yv(VHI));ctx.lineTo(ML,Yv(VLO));ctx.stroke();
          ctx.beginPath();ctx.moveTo(ML,Yv(VLO));ctx.lineTo(ML+PW,Yv(VLO));ctx.stroke();
          for(var sid=0;sid<3;sid++){ctx.strokeStyle=COL[sid];ctx.lineWidth=3;ctx.beginPath();var first=true;
            for(var u=0;u<=1.0001;u+=0.004){var ss=sid+u;var px=X(ss),py=Yv(V(ss));
              if(first){ctx.moveTo(px,py);first=false;}else ctx.lineTo(px,py);}
            ctx.stroke();}
          for(var sid=0;sid<3;sid++){ctx.fillStyle=COL[sid];ctx.beginPath();
            ctx.arc(X(bots[sid][0]),Yv(bots[sid][1]),5.5,0,2*Math.PI);ctx.fill();}
          ctx.strokeStyle='#1f3b6e';ctx.lineWidth=2.4;ctx.beginPath();
          ctx.arc(X(bots[0][0]),Yv(bots[0][1]),9,0,2*Math.PI);ctx.stroke();
          ctx.fillStyle='#1f3b6e';ctx.font='700 12.5px -apple-system,Segoe UI,Arial';ctx.textAlign='center';
          ctx.fillText('vale mais fundo',X(bots[0][0]),Yv(bots[0][1])+24);
          ctx.font='700 12px -apple-system,Segoe UI,Arial';
          for(var i=0;i<CORN.length;i++){var sc=CORN[i][0];var vv=V(sc===3?2.9999:sc);
            ctx.fillStyle=RED;ctx.beginPath();ctx.arc(X(sc),Yv(vv),5,0,2*Math.PI);ctx.fill();
            var sub=CORN[i][1]==='e1'?'e₁':(CORN[i][1]==='e2'?'e₂':'e₃');
            ctx.fillText(sub,X(sc),Yv(vv)-11);}
          ctx.fillStyle=RED;ctx.font='600 11px -apple-system,Segoe UI,Arial';
          ctx.fillText('cristas (quinas)',X(2.0),Yv(VHI)+12);
          ctx.font='600 11px -apple-system,Segoe UI,Arial';
          var labs=['{x₁,x₂}','{x₂,x₃}','{x₁,x₃}'];
          for(var sid=0;sid<3;sid++){ctx.fillStyle=COL[sid];
            ctx.fillText(labs[sid],X(sid+0.5),Yv(VLO)+18);}
        }
        function drawStart(s){ctx.strokeStyle='#b8bcc4';ctx.lineWidth=1.2;ctx.setLineDash([4,4]);
          ctx.beginPath();ctx.moveTo(X(s),MT-2);ctx.lineTo(X(s),Yv(VLO));ctx.stroke();ctx.setLineDash([]);}
        function drawBall(s){ctx.fillStyle='#111';ctx.beginPath();
          ctx.arc(X(s),Yv(V(s)),7,0,2*Math.PI);ctx.fill();ctx.strokeStyle='#fff';ctx.lineWidth=1.6;ctx.stroke();}
        function render(){ctx.clearRect(0,0,CSSW,CSSH);drawCurve();drawStart(startS);drawBall(curS);
          fEl.textContent=fmt(V(curS));}
        var slider=document.getElementById('s2anim-slider');
        var dropBtn=document.getElementById('s2anim-drop');
        var posEl=document.getElementById('s2anim-pos');
        var fEl=document.getElementById('s2anim-f');
        var statEl=document.getElementById('s2anim-stat');
        function sliderToS(){return 0.06+(slider.value/1000)*2.88;}
        var startS=sliderToS(), curS=startS, running=false;
        function setStat(t){statEl.textContent=t;}
        function piecePos(s){var sid=Math.floor(((s%3)+3)%3);if(sid>2)sid=2;return sid;}
        function frame(){
          if(running){var g=grad(curS);var ds=0.0022*g;
            if(ds>0.014)ds=0.014; if(ds<-0.014)ds=-0.014;
            curS+=ds; if(curS<0)curS=0; if(curS>3)curS=3;
            if(Math.abs(g)<0.02){running=false;
              var sid=piecePos(curS);var labs=['{1,2}','{2,3}','{1,3}'];var vv=V(curS);
              if(vv<BEST+0.04){setStat('chegou ao MELHOR (vale '+labs[sid]+')');}
              else{setStat('PRESO no mínimo '+labs[sid]+' — subótimo');}
              dropBtn.textContent='↺ Soltar de novo';}
          }
          render(); requestAnimationFrame(frame);}
        slider.addEventListener('input',function(){running=false;startS=sliderToS();curS=startS;
          posEl.textContent='partida';setStat('solte a bolinha');dropBtn.textContent='▶ Soltar bolinha';});
        dropBtn.addEventListener('click',function(){startS=sliderToS();curS=startS;running=true;
          setStat('descendo…');dropBtn.textContent='▶ Soltar bolinha';});
        requestAnimationFrame(frame);
      })();
      </script>
      <script>
      (function(){
        var cv=document.getElementById('s2tanim-cv'); if(!cv) return;
        var ctx=cv.getContext('2d'); var dpr=window.devicePixelRatio||1;
        var CSSW=720, CSSH=340;
        cv.width=CSSW*dpr; cv.height=CSSH*dpr; ctx.scale(dpr,dpr);
        var ACC='#3b54c4',AMB='#c2790a',GRN='#1f9a55',PUR='#7a3fc4',RED='#b23b3b',GREY='#b9bec6',DARK='#1f3b6e';
        var Q00=2.0,Q11=2.2,Q22=1.6,Q01=1.2,Q02=0.8,Q12=1.0;
        function fperim(s){ s=((s%3)+3)%3; var t,c,n;
          if(s<1){t=s*Math.PI/2;c=Math.cos(t);n=Math.sin(t);return Q00*c*c+Q11*n*n+2*Q01*c*n;}
          else if(s<2){t=(s-1)*Math.PI/2;c=Math.cos(t);n=Math.sin(t);return Q11*c*c+Q22*n*n+2*Q12*c*n;}
          else{t=(s-2)*Math.PI/2;c=Math.cos(t);n=Math.sin(t);return Q22*c*c+Q00*n*n+2*Q02*c*n;} }
        function comps(eta){return [0.90, 0.78-0.50*eta, 0.18+0.55*eta];}
        function dropped(c){return (c[1]>=c[2])?2:1;}   // qual e zerado
        function suppName(c){return (c[1]>=c[2])?'{1,2}':'{1,3}';}
        function sTrunc(eta){var c=comps(eta);
          if(c[1]>=c[2]){return Math.atan2(c[1],c[0])/(Math.PI/2);}        // pedaco {1,2}, seg0
          else{return 2+Math.atan2(c[0],c[2])/(Math.PI/2);}}              // pedaco {1,3}, seg2
        // regiao das barras (esquerda)
        var BX=[95,170,245], BY0=292, BTOP=66, BW=44;
        // regiao do relevo (direita)
        var RX0=420,RX1=702,RY0=66,RY1=292, VLO=-3.55,VHI=-1.30;
        function Xr(s){return RX0+(s/3)*(RX1-RX0);}
        function Yr(v){return RY0+(1-(v-VLO)/(VHI-VLO))*(RY1-RY0);}
        function draw(eta){
          ctx.clearRect(0,0,CSSW,CSSH);
          var c=comps(eta), drop=dropped(c), cols=[ACC,AMB,GRN];
          // --- esquerda: barras ---
          ctx.fillStyle=DARK;ctx.font='700 12px -apple-system,Segoe UI,Arial';ctx.textAlign='center';
          ctx.fillText("vetor denso x' — corta a MENOR de 2 e 3",170,46);
          ctx.strokeStyle='#cfd2d8';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(56,BY0);ctx.lineTo(296,BY0);ctx.stroke();
          for(var i=0;i<3;i++){var h=c[i]*(BY0-BTOP)/1.05;var col=(i===drop)?GREY:cols[i];
            ctx.fillStyle=col;ctx.fillRect(BX[i]-BW/2,BY0-h,BW,h);
            if(i===drop){ctx.strokeStyle=RED;ctx.setLineDash([4,3]);ctx.lineWidth=2;
              ctx.strokeRect(BX[i]-BW/2,BY0-h,BW,h);ctx.setLineDash([]);
              ctx.fillStyle=RED;ctx.font='700 11px -apple-system,Segoe UI,Arial';ctx.fillText('zera',BX[i],BY0-h-7);}
            ctx.fillStyle='#37414f';ctx.font='600 12px -apple-system,Segoe UI,Arial';
            ctx.fillText(['x₁','x₂','x₃'][i],BX[i],BY0+16);}
          // --- direita: relevo -f ---
          ctx.fillStyle=DARK;ctx.font='700 12px -apple-system,Segoe UI,Arial';
          ctx.fillText("onde o truncamento te joga (relevo)",561,46);
          var segCols=[ACC,PUR,GRN];
          for(var sid=0;sid<3;sid++){ctx.strokeStyle=segCols[sid];ctx.lineWidth=2.6;ctx.beginPath();var f=true;
            for(var u=0;u<=1.0001;u+=0.01){var ss=sid+u,v=-fperim(ss),px=Xr(ss),py=Yr(v);
              if(f){ctx.moveTo(px,py);f=false;}else ctx.lineTo(px,py);}ctx.stroke();}
          var nm=['e₁','e₂','e₃','e₁'];
          for(var k=0;k<=3;k++){var vv=-fperim(k===3?2.9999:k);ctx.fillStyle=RED;
            ctx.beginPath();ctx.arc(Xr(k),Yr(vv),4,0,2*Math.PI);ctx.fill();
            ctx.fillStyle=RED;ctx.font='600 10.5px -apple-system,Segoe UI,Arial';ctx.fillText(nm[k],Xr(k),Yr(vv)-9);}
          var s=sTrunc(eta),vm=-fperim(s);
          ctx.fillStyle='#111';ctx.beginPath();ctx.arc(Xr(s),Yr(vm),7,0,2*Math.PI);ctx.fill();
          ctx.strokeStyle='#fff';ctx.lineWidth=1.6;ctx.stroke();
          ctx.fillStyle=(c[1]>=c[2])?ACC:GRN;ctx.font='700 11.5px -apple-system,Segoe UI,Arial';
          ctx.fillText('suporte '+suppName(c),Xr(s),Yr(vm)+20);
        }
        var slider=document.getElementById('s2tanim-slider');
        var sweepBtn=document.getElementById('s2tanim-sweep');
        var etaEl=document.getElementById('s2tanim-eta');
        var supEl=document.getElementById('s2tanim-sup');
        var tieEl=document.getElementById('s2tanim-tie');
        var jumpEl=document.getElementById('s2tanim-jump');
        var prevSup=null, flash=0, sweeping=false, dir=1;
        function update(){
          var eta=slider.value/1000; var c=comps(eta); var sup=suppName(c);
          draw(eta);
          etaEl.textContent='η = '+eta.toFixed(2).replace('.',',');
          supEl.textContent=sup; supEl.style.color=(c[1]>=c[2])?'#3b54c4':'#1f9a55';
          var d=Math.abs(c[1]-c[2]);
          tieEl.textContent = d<0.05 ? '≈ EMPATE' : 'estável';
          tieEl.style.color = d<0.05 ? '#b23b3b' : '#1a2230';
          if(prevSup!==null && sup!==prevSup){flash=70;}
          prevSup=sup;
          if(flash>0){jumpEl.textContent='↯ SALTOU de bacia!';jumpEl.style.color='#b23b3b';flash--;}
          else{jumpEl.textContent='—';jumpEl.style.color='#1a2230';}
        }
        function frame(){
          if(sweeping){var v=parseInt(slider.value,10)+dir*7;
            if(v>=1000){v=1000;dir=-1;} if(v<=0){v=0;dir=1;}
            slider.value=v;}
          update(); requestAnimationFrame(frame);}
        slider.addEventListener('input',function(){sweeping=false;sweepBtn.textContent='▶ Varrer η';});
        sweepBtn.addEventListener('click',function(){sweeping=!sweeping;
          sweepBtn.textContent=sweeping?'⏸ Pausar':'▶ Varrer η';});
        requestAnimationFrame(frame);
      })();
      </script>"""

h = open(DOC, encoding="utf-8").read()
pat = re.compile(r'<div class="box deep">\s*<span class="tag">O que a quina faz com o gradiente</span>.*?</script>', re.DOTALL)
h2, n = pat.subn(lambda m: NEW, h)
assert n == 1, "replace -> %d (esperado 1)" % n

h2 = embed(h2, {"quina gradiente relevo": FIG_REL,
                "quina garfo": FIG_FORK,
                "truncamento barras": FIG_TRUNC})

ok, rep = integrity(h2, 9)
print("integrity:", ok, rep)
import re as _re
cyr = _re.findall(r'[Ѐ-ӿ]', h2)
print("cirilico:", len(cyr))
# perdas de acento reais (formas claramente erradas)
loss = _re.findall(r'\b(variancia|projecao|funcao|restricao|combinatoria|subotimo|otimizacao|direcao|inclinacao|equilibrio|esparsidad)\b', h2)
print("possiveis perdas (checar se sao ASCII de alt/aria):", sorted(set(loss)))
# < cru seguido de letra em math inline \( ... \)
raw_lt = _re.findall(r'\\\([^\)]*<[a-zA-Z][^\)]*\\\)', h2)
print("'<letra' em math inline:", len(raw_lt))

if ok and len(cyr)==0 and len(raw_lt)==0:
    open(DOC,"w",encoding="utf-8").write(h2)
    print("ESCRITO:", DOC)
else:
    print("NAO ESCRITO — corrigir")
