#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integra na doc 02: expande a caixa 'O que a quina faz com o gradiente' +
figura de relevo (2 paineis) + animacao interativa em canvas. embed + integrity + checagens."""
import re, sys, unicodedata
sys.path.insert(0, "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools")
from al_template import embed, integrity

DOC = "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/02_sparse_pca_o_problema.html"
FIG = "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools/fig_quina_gradiente.png"

NEW = r"""<div class="box deep">
        <span class="tag">O que a quina faz com o gradiente</span>
        <p><strong>Primeiro, o que "seguir o gradiente" quer dizer.</strong> Numa superfície <em>lisa</em> (sem
        cantos), em cada ponto existe <em>uma</em> direção de subida mais íngreme — o gradiente. O método é
        simples: olhe ao redor dos pés, ache essa direção, dê um passo nela, repita. Você sobe até um
        <strong>topo</strong>, onde não há mais para onde subir (o gradiente zera). É uma máquina de achar o
        alto de <em>um</em> morro liso.</p>
        <p><strong>Cenário 1 — dentro de um pedaço (suporte fixo).</strong> Escolha um conjunto de \(k\)
        variáveis e <em>não mexa nele</em> — digamos \(\{x_1,x_2\}\). Os vetores permitidos são só os unitários
        nessas duas coordenadas: um circulozinho liso. O gradiente nesse círculo funciona perfeitamente e te
        leva ao <strong>pico daquele pedaço</strong> — o autovetor de cima da submatriz \(2\times2\)
        \(Q_{\{1,2\}}\). E aqui está o detalhe que costuma escapar: esse pico fica no <strong>meio do
        arco</strong>, usando <em>as duas</em> variáveis — é um ponto <em>interior</em>, <strong>não uma
        quina</strong>. O gradiente sobe e <strong>para ali</strong>; ele <em>nunca</em> caminha até um ponto de
        eixo. (Painel A da figura.)</p>
        <p><strong>Então por que o gradiente falha?</strong> Não é que ele "chega na quina e fica em dúvida". O
        problema é <strong>aprisionamento</strong>. Cada pedaço tem o seu pico, e os picos têm <strong>alturas
        diferentes</strong> — o melhor global mora em <em>um</em> pedaço só. A subida local te entrega, com
        perfeição, o pico do pedaço <em>em que você caiu</em> — que pode ser o errado. Sentado no topo de um
        pedaço, o gradiente não tem como enxergar que existe um pico mais alto num pedaço vizinho. (Painel B: a
        bolinha sobe e fica <strong>presa</strong> no pico subótimo.)</p>
        <p><strong>O papel da quina.</strong> A quina é onde dois pedaços se cruzam — e ali a superfície
        <strong>não é lisa</strong>: passam dois arcos, cada um com a sua tangente, então não existe "a" direção
        de subida; existem <em>duas</em>. Disso saem duas consequências para o gradiente: <em>(i)</em> o fluxo
        suave dentro de um pedaço nem <strong>chega</strong> à quina — ele para antes, no pico interior; e
        <em>(ii)</em> para ir do pico de um pedaço ao pico de um pedaço melhor, seria preciso
        <strong>descer</strong> até a quina e <strong>subir</strong> o outro arco — e subida nunca desce de
        propósito. Por isso o gradiente fica trancado no pedaço onde começou.</p>
        <p><strong>E o truque de "dar o passo e depois consertar"?</strong> Há uma tentativa esperta de pular
        entre pedaços: dê o passo do gradiente no espaço inteiro \(\mathbb{R}^n\) (ignorando a esparsidade) e
        depois <strong>trunque</strong> de volta para \(k\) variáveis (mantenha as \(k\) maiores em módulo, zere
        o resto, renormalize). O problema é que esse truncar é <strong>descontínuo</strong>: quando duas
        componentes quase empatam em módulo — o que acontece justamente <em>perto das quinas</em> — um passinho
        minúsculo troca qual delas sobrevive, e o suporte <strong>salta</strong> de um pedaço para outro. O
        processo não <em>desliza</em> entre pedaços; ele <em>pula</em>, e onde para depende de onde começou.</p>
        <p><strong>Moral.</strong> De um jeito (preso num pedaço) ou de outro (saltos descontínuos), não existe
        uma subida lisa que <em>percorra todos os pedaços</em>. É exatamente isso que torna "qual suporte usar?"
        uma pergunta de tentar conjuntos — e não uma conta fechada.</p>
      </div>
      <figure>
        <img src="" alt="quina gradiente relevo">
        <figcaption><strong>Esquerda (A) — dentro de um pedaço.</strong> O pedaço \(\{x_1,x_2\}\) é um
        circulozinho liso, aqui "desenrolado" (eixo horizontal = ângulo ao longo do círculo; altura = variância
        \(f=x^\top Q x\)). O gradiente sobe pelos dois lados até o <strong>pico interior</strong> (âmbar) — o
        autovetor da submatriz, que usa as duas variáveis — e para ali. Os pontos de eixo \(e_1,e_2\) (vermelho)
        são onde, <em>na união</em>, se colam outros pedaços (as quinas); mas neste pedaço <em>sozinho</em> a
        curva passa por eles <strong>lisa</strong>. O vale lá pelos 135° é a direção do <em>menor</em> autovetor
        da mesma submatriz. <strong>Direita (B) — a união.</strong> Percorrendo a borda do triângulo
        \(e_1\to e_2\to e_3\to e_1\), os três pedaços aparecem emendados: três "morros" (um por par de
        variáveis) de <strong>alturas diferentes</strong>, separados por <strong>quinas</strong> (vermelho), onde
        a curva tem um <strong>vinco</strong> — duas inclinações no mesmo ponto. A bolinha preta, solta na
        encosta do pedaço \(\{x_2,x_3\}\), sobe e fica <strong>presa</strong> no pico daquele pedaço (subótimo).
        O melhor global (pico do pedaço \(\{x_1,x_2\}\)) está do outro lado de uma quina: para alcançá-lo a
        bolinha teria que <em>descer</em> até a quina e subir o outro morro — coisa que a subida local nunca
        faz.</figcaption>
      </figure>
      <div class="anim-wrap" id="s2anim">
        <div class="anim-head">
          <span class="anim-title">Animação interativa — o gradiente preso num pedaço</span>
          <span class="anim-sub">arraste para escolher o ponto de partida e solte a bolinha · tente vários: a maioria leva a um pico subótimo</span>
        </div>
        <canvas id="s2anim-cv" width="700" height="430" aria-label="Animacao do gradiente subindo o relevo dos pedacos e ficando preso no pico subotimo"></canvas>
        <div class="anim-ctrl">
          <button id="s2anim-drop" class="anim-btn" type="button">▶ Soltar bolinha</button>
          <input id="s2anim-slider" type="range" min="0" max="1000" value="430" aria-label="Ponto de partida da bolinha">
          <span id="s2anim-pos" class="anim-tval">partida</span>
        </div>
        <div class="anim-hud">
          <div><span class="hud-k">altura atual f</span><span id="s2anim-f" class="hud-v">—</span></div>
          <div><span class="hud-k">melhor global f</span><span id="s2anim-best" class="hud-v">3,30</span></div>
          <div><span class="hud-k">situação</span><span id="s2anim-stat" class="hud-v">solte a bolinha</span></div>
        </div>
      </div>
      <style>
        #s2anim{border:1px solid var(--line);border-radius:16px;background:#fff;
          padding:14px 14px 16px;margin:20px 0;box-shadow:0 3px 14px rgba(20,30,60,.07)}
        #s2anim .anim-head{display:flex;flex-direction:column;gap:2px;margin-bottom:10px}
        #s2anim .anim-title{font-weight:800;color:#1a2230;font-size:15px}
        #s2anim .anim-sub{font-size:12.5px;color:var(--muted);font-style:italic}
        #s2anim canvas{display:block;width:100%;max-width:700px;height:auto;margin:0 auto;
          background:#fcfcfa;border:1px solid var(--line);border-radius:12px}
        #s2anim .anim-ctrl{display:flex;align-items:center;gap:12px;margin:12px 2px 0}
        #s2anim .anim-btn{appearance:none;border:1px solid var(--accent);background:var(--accent);
          color:#fff;font-weight:700;font-size:13.5px;padding:7px 14px;border-radius:9px;cursor:pointer;
          white-space:nowrap;font-family:inherit}
        #s2anim .anim-btn:hover{filter:brightness(1.06)}
        #s2anim input[type=range]{flex:1;accent-color:var(--accent);cursor:pointer}
        #s2anim .anim-tval{font-variant-numeric:tabular-nums;color:#37414f;font-weight:700;
          font-size:13.5px;min-width:74px;text-align:right}
        #s2anim .anim-hud{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px}
        #s2anim .anim-hud>div{background:var(--slate-bg);border:1px solid var(--line);border-radius:10px;
          padding:8px 10px;display:flex;flex-direction:column;gap:3px}
        #s2anim .hud-k{font-size:11.5px;color:var(--muted);letter-spacing:.01em}
        #s2anim .hud-v{font-size:18px;font-weight:800;color:#1a2230;font-variant-numeric:tabular-nums}
        @media(max-width:560px){#s2anim .anim-hud{grid-template-columns:1fr}}
      </style>
      <script>
      (function(){
        var cv=document.getElementById('s2anim-cv'); if(!cv) return;
        var ctx=cv.getContext('2d'); var dpr=window.devicePixelRatio||1;
        var CSSW=700, CSSH=430;
        cv.width=CSSW*dpr; cv.height=CSSH*dpr; ctx.scale(dpr,dpr);
        var ML=46, MR=18, MT=26, MB=46;
        var PW=CSSW-ML-MR, PH=CSSH-MT-MB;
        var SLO=0, SHI=3, YLO=1.35, YHI=3.55;
        // Q de exemplo (mesma da figura)
        var Q00=2.0,Q11=2.2,Q22=1.6,Q01=1.2,Q02=0.8,Q12=1.0;
        var COL=['#3b54c4','#7a3fc4','#1f9a55']; var RED='#b23b3b';
        var BEST=3.304;
        function fperim(s){ s=((s%3)+3)%3; var t,c,n;
          if(s<1){t=s*Math.PI/2;c=Math.cos(t);n=Math.sin(t);return Q00*c*c+Q11*n*n+2*Q01*c*n;}
          else if(s<2){t=(s-1)*Math.PI/2;c=Math.cos(t);n=Math.sin(t);return Q11*c*c+Q22*n*n+2*Q12*c*n;}
          else{t=(s-2)*Math.PI/2;c=Math.cos(t);n=Math.sin(t);return Q22*c*c+Q00*n*n+2*Q02*c*n;} }
        function grad(s){var h=2e-4;return (fperim(s+h)-fperim(s-h))/(2*h);}
        function X(s){return ML+(s-SLO)/(SHI-SLO)*PW;}
        function Yv(f){return MT+(1-(f-YLO)/(YHI-YLO))*PH;}
        function fmt(v){return v.toFixed(2).replace('.',',');}
        // picos por amostragem
        var peaks=[];
        for(var sid=0;sid<3;sid++){var bf=-1e9,bs=sid+0.5;
          for(var u=0.001;u<0.999;u+=0.001){var ss=sid+u,ff=fperim(ss);if(ff>bf){bf=ff;bs=ss;}}
          peaks.push([bs,bf]);}
        var CORN=[[0,'e1'],[1,'e2'],[2,'e3'],[3,'e1']];
        function drawCurve(){
          // eixo de base
          ctx.strokeStyle='#cfd2d8';ctx.lineWidth=1;
          ctx.beginPath();ctx.moveTo(ML,Yv(YLO));ctx.lineTo(ML+PW,Yv(YLO));ctx.stroke();
          ctx.beginPath();ctx.moveTo(ML,MT-4);ctx.lineTo(ML,Yv(YLO));ctx.stroke();
          // tres curvas coloridas
          for(var sid=0;sid<3;sid++){ctx.strokeStyle=COL[sid];ctx.lineWidth=3;ctx.beginPath();
            var first=true;
            for(var u=0;u<=1.0001;u+=0.004){var ss=sid+u;var px=X(ss),py=Yv(fperim(ss));
              if(first){ctx.moveTo(px,py);first=false;}else ctx.lineTo(px,py);}
            ctx.stroke();}
          // picos
          for(var sid=0;sid<3;sid++){ctx.fillStyle=COL[sid];ctx.beginPath();
            ctx.arc(X(peaks[sid][0]),Yv(peaks[sid][1]),5.5,0,2*Math.PI);ctx.fill();}
          // melhor global (anel + rotulo)
          ctx.strokeStyle='#1f3b6e';ctx.lineWidth=2.4;ctx.beginPath();
          ctx.arc(X(peaks[0][0]),Yv(peaks[0][1]),9,0,2*Math.PI);ctx.stroke();
          ctx.fillStyle='#1f3b6e';ctx.font='700 12.5px -apple-system,Segoe UI,Arial';ctx.textAlign='center';
          ctx.fillText('melhor global',X(peaks[0][0]),Yv(peaks[0][1])-15);
          // quinas
          ctx.font='700 12px -apple-system,Segoe UI,Arial';
          for(var i=0;i<CORN.length;i++){var sc=CORN[i][0];var fv=fperim(sc===3?2.9999:sc);
            ctx.fillStyle=RED;ctx.beginPath();ctx.arc(X(sc),Yv(fv),5,0,2*Math.PI);ctx.fill();
            ctx.fillStyle=RED;
            var sub=CORN[i][1]==='e1'?'e₁':(CORN[i][1]==='e2'?'e₂':'e₃');
            ctx.fillText(sub,X(sc),Yv(YLO)+18);}
          // rotulos dos pedacos
          ctx.font='600 11px -apple-system,Segoe UI,Arial';
          var labs=['{x₁,x₂}','{x₂,x₃}','{x₁,x₃}'];
          for(var sid=0;sid<3;sid++){ctx.fillStyle=COL[sid];
            ctx.fillText(labs[sid],X(sid+0.5),Yv(YLO)+34);}
        }
        function drawStart(s){ctx.strokeStyle='#b8bcc4';ctx.lineWidth=1.2;ctx.setLineDash([4,4]);
          ctx.beginPath();ctx.moveTo(X(s),MT-2);ctx.lineTo(X(s),Yv(YLO));ctx.stroke();ctx.setLineDash([]);}
        function drawBall(s){ctx.fillStyle='#111';ctx.beginPath();
          ctx.arc(X(s),Yv(fperim(s)),7,0,2*Math.PI);ctx.fill();
          ctx.strokeStyle='#fff';ctx.lineWidth=1.6;ctx.stroke();}
        function render(){ctx.clearRect(0,0,CSSW,CSSH);drawCurve();drawStart(startS);drawBall(curS);
          fEl.textContent=fmt(fperim(curS));}
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
              var sid=piecePos(curS);var labs=['{1,2}','{2,3}','{1,3}'];
              var fv=fperim(curS);
              if(fv>BEST-0.04){setStat('chegou ao MELHOR (pedaço '+labs[sid]+')');}
              else{setStat('PRESO no pedaço '+labs[sid]+' — subótimo');}
              dropBtn.textContent='↺ Soltar de novo';}
          }
          render(); requestAnimationFrame(frame);}
        slider.addEventListener('input',function(){running=false;startS=sliderToS();curS=startS;
          posEl.textContent='partida';setStat('solte a bolinha');dropBtn.textContent='▶ Soltar bolinha';});
        dropBtn.addEventListener('click',function(){startS=sliderToS();curS=startS;running=true;
          setStat('subindo…');dropBtn.textContent='▶ Soltar bolinha';});
        requestAnimationFrame(frame);
      })();
      </script>"""

h = open(DOC, encoding="utf-8").read()
pat = re.compile(r'<div class="box deep">\s*<span class="tag">O que a quina faz com o gradiente</span>.*?</div>', re.DOTALL)
h2, n = pat.subn(lambda m: NEW, h)
assert n == 1, "replace box -> %d (esperado 1)" % n

h2 = embed(h2, {"quina gradiente relevo": FIG})

ok, rep = integrity(h2, 7)
print("integrity:", ok, rep)

# checagem de diacriticos perdidos (formas erradas reais)
bad = re.findall(r'\b(variancia|projecao|funcao|restricao|combinatoria|otimo|subotimo|pedaco|tangencia|nao|tambem|porem|alturas?|esferica)\b', h2)
# checagem de cirilico
cyr = re.findall(r'[Ѐ-ӿ]', h2)
print("cirilico:", len(cyr))
# perdas reais especificas (apenas formas claramente sem acento que deveriam ter)
losses = re.findall(r'\b(variancia|projecao|funcao|restricao|combinatoria|subotimo|pedaco|gradiente?s? travad|inclinacao|direcao|esparsidad|deslizar?)\b', h2)
print("possiveis perdas:", sorted(set(losses)))

if ok and len(cyr)==0:
    open(DOC,"w",encoding="utf-8").write(h2)
    print("ESCRITO:", DOC)
else:
    print("NAO ESCRITO — corrigir antes")
