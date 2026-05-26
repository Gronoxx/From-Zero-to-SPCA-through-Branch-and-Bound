#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Substitui a s2lanim por versao 2 paineis (3D esfera | 2D relevo) com DUAS etapas:
1) aplicar normalizacao (raio->1, forma os circulos) ; 2) aplicar Q (cor/relevo). integrity+checagens."""
import re, sys
sys.path.insert(0, "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools")
from al_template import integrity

DOC="/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/02_sparse_pca_o_problema.html"

NEW = r"""<p>Agora em <strong>duas etapas</strong> e <strong>dois olhares</strong>. <strong>1) Aplicar
      normalização</strong> leva todo vetor a comprimento 1: à esquerda, em <strong>3D</strong>, os pontos de
      vários raios pousam na esfera e formam os 3 círculos (os conjuntos-\(k\)); à direita, em <strong>2D</strong>,
      o domínio surge plano. <strong>2) Aplicar \(Q\)</strong> liga a variância: em 3D os círculos se colorem
      (azul = baixa, âmbar = alta) e em 2D o relevo cresce — o morfo exato \(f_t=(1-t)\cdot 1 + t\,x^\top Q x\).
      No fim, o garfo na quina \(e_1\).</p>
      <div class="anim-wrap" id="s2lanim">
        <div class="anim-head">
          <span class="anim-title">Animação interativa — as duas camadas, em 3D e 2D ao mesmo tempo</span>
          <span class="anim-sub">aplique uma etapa de cada vez: primeiro a normalização (forma o domínio), depois o \(Q\) (gera a inclinação) · arraste para revisar qualquer instante</span>
        </div>
        <canvas id="s2lanim-cv" width="860" height="430" aria-label="Dois paineis: a esquerda a esfera 3D com os 3 circulos formando-se pela normalizacao e colorindo-se pela variancia; a direita o relevo desenrolado em 2D"></canvas>
        <div class="anim-ctrl">
          <button id="s2lanim-bn" class="anim-btn" type="button">1 ▶ Aplicar normalização</button>
          <button id="s2lanim-bq" class="anim-btn" type="button">2 ▶ Aplicar Q</button>
          <input id="s2lanim-slider" type="range" min="0" max="2000" value="0" aria-label="Progresso das duas etapas">
          <span id="s2lanim-t" class="anim-tval">etapa 0</span>
        </div>
        <div class="anim-hud">
          <div><span class="hud-k">etapa</span><span id="s2lanim-fase" class="hud-v" style="font-size:13.5px">aguardando</span></div>
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
        #s2lanim canvas{display:block;width:100%;max-width:860px;height:auto;margin:0 auto;
          background:#fcfcfa;border:1px solid var(--line);border-radius:12px}
        #s2lanim .anim-ctrl{display:flex;align-items:center;gap:10px;margin:12px 2px 0;flex-wrap:wrap}
        #s2lanim .anim-btn{appearance:none;border:1px solid var(--accent);background:var(--accent);
          color:#fff;font-weight:700;font-size:13px;padding:7px 13px;border-radius:9px;cursor:pointer;
          white-space:nowrap;font-family:inherit}
        #s2lanim .anim-btn:hover{filter:brightness(1.06)}
        #s2lanim input[type=range]{flex:1;min-width:140px;accent-color:var(--accent);cursor:pointer}
        #s2lanim .anim-tval{font-variant-numeric:tabular-nums;color:#37414f;font-weight:700;
          font-size:13px;min-width:64px;text-align:right}
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
        var CSSW=860, CSSH=430;
        cv.width=CSSW*dpr; cv.height=CSSH*dpr; ctx.scale(dpr,dpr);
        var ACC='#3b54c4', PUR='#7a3fc4', GRN='#1f9a55', RED='#b23b3b', GREY='#9aa0aa', DARK='#1f3b6e', AMB='#c2790a';
        var Q11=2.0,Q22=2.2,Q33=1.6,Q12=1.2,Q13=0.8,Q23=1.0;
        function ffull(a,b,c){return Q11*a*a+Q22*b*b+Q33*c*c+2*Q12*a*b+2*Q13*a*c+2*Q23*b*c;}
        // ----- projecao 3D (orto, iso) -----
        var az=32*Math.PI/180, el=24*Math.PI/180;
        var ca=Math.cos(az),sa=Math.sin(az),ce=Math.cos(el),se=Math.sin(el);
        function proj(x,y,z){ var vx=ca*x - sa*y; var vy=ce*sa*x + ce*ca*y - se*z; var vz=se*sa*x + se*ca*y + ce*z;
          return [vx, vz, vy]; }   // X, Y, profundidade
        var L={cx:205, cy:212, RR:140};
        function L3(p){return [L.cx+p[0]*L.RR, L.cy-p[1]*L.RR, p[2]];}
        // escala de cor por f
        var FLO=0.85, FHI=3.31;
        function fcol(val,alpha){ var tt=Math.max(0,Math.min(1,(val-FLO)/(FHI-FLO)));
          var R=Math.round((1-tt)*59+tt*194), G=Math.round((1-tt)*84+tt*121), B=Math.round((1-tt)*196+tt*10);
          return 'rgba('+R+','+G+','+B+','+alpha+')'; }
        var PAIRS=[[0,1],[0,2],[1,2]]; var PCOL=[ACC,GRN,PUR];
        // pontos para a etapa de normalizacao (raio inicial deterministico)
        var NORMPTS=[];
        for(var pi=0; pi<3; pi++){ var ij=PAIRS[pi];
          for(var a=0; a<12; a++){ var ang=a/12*2*Math.PI;
            var r0=0.5+0.82*(((a*1.6180339887+pi*0.37)%1+1)%1);
            NORMPTS.push({i:ij[0], j:ij[1], ang:ang, r0:r0, col:PCOL[pi]}); }
        }
        // ----- 2D: relevo desenrolado (percurso e2->e1->e3->e2) -----
        var R2={x0:475, x1:846, y0:54, y1:356, flo:0.70, fhi:3.5};
        function fQ2(s){ s=((s%3)+3)%3; var t,c,n;
          if(s<1){t=s*Math.PI/2;c=Math.cos(t);n=Math.sin(t);return Q22*c*c+Q11*n*n+2*Q12*c*n;}
          else if(s<2){t=(s-1)*Math.PI/2;c=Math.cos(t);n=Math.sin(t);return Q11*c*c+Q33*n*n+2*Q13*c*n;}
          else{t=(s-2)*Math.PI/2;c=Math.cos(t);n=Math.sin(t);return Q33*c*c+Q22*n*n+2*Q23*c*n;} }
        function X2(s){return R2.x0+(s/3)*(R2.x1-R2.x0);}
        function Y2(f){return R2.y0+(1-(f-R2.flo)/(R2.fhi-R2.flo))*(R2.y1-R2.y0);}
        var COL2=[ACC,GRN,PUR], SEGLAB=['{x₁,x₂}','{x₁,x₃}','{x₂,x₃}'];
        var CORN2=[[0,'e₂'],[1,'e₁'],[2,'e₃'],[3,'e₂']];
        function lab(txt,x,y,color,size,al,baseline){ctx.fillStyle=color;
          ctx.font='700 '+(size||12)+'px -apple-system,Segoe UI,Arial';ctx.textAlign=al||'center';
          ctx.textBaseline=baseline||'alphabetic';ctx.fillText(txt,x,y);}
        function arrow(x0,y0,x1,y1,color,w){ctx.strokeStyle=color;ctx.fillStyle=color;ctx.lineWidth=w;
          ctx.beginPath();ctx.moveTo(x0,y0);ctx.lineTo(x1,y1);ctx.stroke();
          var aa=Math.atan2(y1-y0,x1-x0),h=8;ctx.beginPath();ctx.moveTo(x1,y1);
          ctx.lineTo(x1-h*Math.cos(aa-0.42),y1-h*Math.sin(aa-0.42));
          ctx.lineTo(x1-h*Math.cos(aa+0.42),y1-h*Math.sin(aa+0.42));ctx.closePath();ctx.fill();}

        function drawLeft(t){
          // t in [0,2]: [0,1]=normalizacao ; [1,2]=Q (s=t-1)
          var pnorm=Math.min(1,t), s=Math.max(0,t-1);
          // silhueta da esfera
          ctx.strokeStyle='#e3e6eb'; ctx.lineWidth=1.1; ctx.beginPath();
          ctx.arc(L.cx,L.cy,L.RR,0,2*Math.PI); ctx.stroke();
          lab('3D — a esfera e os 3 círculos (conjuntos-k)', L.cx, 28, DARK, 12.5);
          if(t<1){
            // etapa 1: pontos de varios raios -> raio 1
            for(var k=0;k<NORMPTS.length;k++){var P=NORMPTS[k];
              var r=P.r0+(1-P.r0)*pnorm; var x=[0,0,0]; x[P.i]=Math.cos(P.ang); x[P.j]=Math.sin(P.ang);
              var sp=L3(proj(r*x[0],r*x[1],r*x[2])); var front=sp[2]>=0;
              ctx.fillStyle=P.col; ctx.globalAlpha=front?0.95:0.32;
              ctx.beginPath(); ctx.arc(sp[0],sp[1], front?3.4:2.4, 0,2*Math.PI); ctx.fill(); }
            ctx.globalAlpha=1;
            lab('normalização: cada vetor → comprimento 1', L.cx, CSSH-16, (pnorm<1?DARK:GRN), 12);
          } else {
            // etapa 2 (ou normalizado): circulos lisos coloridos por f_s, com oclusao
            var segs=[];
            for(var pi=0; pi<3; pi++){ var ij=PAIRS[pi]; var N=72;
              for(var a=0;a<N;a++){ var t0=a/N*2*Math.PI, t1=(a+1)/N*2*Math.PI;
                var p0=[0,0,0]; p0[ij[0]]=Math.cos(t0); p0[ij[1]]=Math.sin(t0);
                var p1=[0,0,0]; p1[ij[0]]=Math.cos(t1); p1[ij[1]]=Math.sin(t1);
                var sp0=L3(proj(p0[0],p0[1],p0[2])), sp1=L3(proj(p1[0],p1[1],p1[2]));
                var fmid=(1-s)+s*0.5*(ffull(p0[0],p0[1],p0[2])+ffull(p1[0],p1[1],p1[2]));
                segs.push({a:sp0,b:sp1,d:0.5*(sp0[2]+sp1[2]),f:fmid}); } }
            segs.sort(function(p,q){return p.d-q.d;});
            for(var k=0;k<segs.length;k++){var S=segs[k]; var front=S.d>=0;
              ctx.strokeStyle=fcol(S.f, front?1:0.30); ctx.lineWidth=front?3.4:1.8; ctx.lineCap='round';
              ctx.beginPath(); ctx.moveTo(S.a[0],S.a[1]); ctx.lineTo(S.b[0],S.b[1]); ctx.stroke(); }
            // quinas
            for(var sgn=-1;sgn<=1;sgn+=2){ for(var e=0;e<3;e++){ var p=[0,0,0]; p[e]=sgn;
              var sp=L3(proj(p[0],p[1],p[2])); var front=sp[2]>=0;
              ctx.fillStyle=RED; ctx.globalAlpha=front?1:0.4;
              ctx.beginPath(); ctx.arc(sp[0],sp[1],front?4.6:3,0,2*Math.PI); ctx.fill();
              ctx.strokeStyle='#fff'; ctx.lineWidth=1.2; if(front)ctx.stroke(); } }
            ctx.globalAlpha=1;
            lab(s<0.02?'domínio pronto (variância ainda plana)':'Q colore: azul = baixa · âmbar = alta variância',
                L.cx, CSSH-16, (s<0.02?GRN:AMB), 12);
          }
        }

        function drawRight(t){
          var s=Math.max(0,Math.min(1,t-1));      // progresso do Q em 2D
          var alpha=Math.min(1,t);                // some/aparece durante a normalizacao
          ctx.save(); ctx.globalAlpha=alpha;
          // eixos
          ctx.strokeStyle='#cfd2d8';ctx.lineWidth=1;
          ctx.beginPath();ctx.moveTo(R2.x0,Y2(R2.fhi));ctx.lineTo(R2.x0,Y2(R2.flo));ctx.stroke();
          ctx.beginPath();ctx.moveTo(R2.x0,Y2(R2.flo));ctx.lineTo(R2.x1,Y2(R2.flo));ctx.stroke();
          lab('2D — o relevo desenrolado', (R2.x0+R2.x1)/2, 28, DARK, 12.5);
          ctx.save(); ctx.translate(R2.x0-30,(Y2(R2.fhi)+Y2(R2.flo))/2); ctx.rotate(-Math.PI/2);
          lab('variância f',0,0,GREY,10.5,'center'); ctx.restore();
          function fT2(ss){return (1-s)*1.0 + s*fQ2(ss);}
          for(var sid=0;sid<3;sid++){ctx.strokeStyle=COL2[sid];ctx.lineWidth=3;ctx.beginPath();var first=true;
            for(var u=0;u<=1.0001;u+=0.006){var ss=sid+u;var px=X2(ss),py=Y2(fT2(ss));
              if(first){ctx.moveTo(px,py);first=false;}else ctx.lineTo(px,py);}
            ctx.stroke(); lab(SEGLAB[sid],X2(sid+0.5),Y2(R2.flo)+30,COL2[sid],10.5);}
          for(var i=0;i<CORN2.length;i++){var sc=CORN2[i][0];var fv=fT2(sc===3?2.9999:sc);
            ctx.fillStyle=RED;ctx.beginPath();ctx.arc(X2(sc),Y2(fv),4.5,0,2*Math.PI);ctx.fill();
            ctx.strokeStyle='#fff';ctx.lineWidth=1.3;ctx.stroke(); lab(CORN2[i][1],X2(sc),Y2(R2.flo)+16,RED,11.5);}
          ctx.restore();
          // garfo no fim
          if(t>1.96){var y1=Y2(fT2(1.0));
            arrow(X2(1.0),y1,X2(0.86),Y2(fT2(0.86)),ACC,2.4);
            arrow(X2(1.0),y1,X2(1.14),Y2(fT2(1.14)),GRN,2.4);
            lab('garfo: 2,4 vs 1,6',(R2.x0+R2.x1)/2, Y2(R2.fhi)-2, DARK, 11.5);}
          function _t(){return s;}
        }
        function draw(t){ ctx.clearRect(0,0,CSSW,CSSH);
          // divisoria
          ctx.strokeStyle='#edeff2'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(430,40); ctx.lineTo(430,CSSH-26); ctx.stroke();
          drawLeft(t); drawRight(t); }

        var slider=document.getElementById('s2lanim-slider');
        var bN=document.getElementById('s2lanim-bn'), bQ=document.getElementById('s2lanim-bq');
        var tEl=document.getElementById('s2lanim-t'), faseEl=document.getElementById('s2lanim-fase');
        var saEl=document.getElementById('s2lanim-sa'), sbEl=document.getElementById('s2lanim-sb');
        var t=0, play=null;   // 'norm' | 'Q' | null
        function f1(v){return v.toFixed(1).replace('.',',');}
        function render(){ draw(t);
          var s=Math.max(0,t-1);
          saEl.textContent=f1(Math.min(1,s)*2.4); sbEl.textContent=f1(Math.min(1,s)*1.6);
          tEl.textContent = t<1 ? 'norm '+Math.round(t*100)+'%' : (t<2?'Q '+Math.round((t-1)*100)+'%':'pronto');
          if(t<0.02) faseEl.textContent='aguardando';
          else if(t<1) faseEl.textContent='1 · normalizando';
          else if(t<1.02) faseEl.textContent='domínio pronto';
          else if(t<1.98) faseEl.textContent='2 · aplicando Q';
          else faseEl.textContent='os dois juntos (garfo)';
        }
        function frame(){
          if(play==='norm'){ t+=0.009; if(t>=1){t=1;play=null;} slider.value=Math.round(t*1000); }
          else if(play==='Q'){ t+=0.009; if(t>=2){t=2;play=null;} slider.value=Math.round(t*1000); }
          render(); requestAnimationFrame(frame);
        }
        slider.addEventListener('input',function(){t=slider.value/1000;play=null;});
        bN.addEventListener('click',function(){t=0;slider.value=0;play='norm';});
        bQ.addEventListener('click',function(){ if(t<1){t=1;slider.value=1000;} play='Q'; });
        requestAnimationFrame(frame);
      })();
      </script>"""

h = open(DOC, encoding="utf-8").read()
pat = re.compile(r'<p>Para <em>ver</em> as duas camadas.*?</script>', re.DOTALL)
h2, n = pat.subn(lambda m: NEW, h)
print("substituicoes:", n)
assert n == 1, "esperado 1"

ok, rep = integrity(h2, 10)
cyr = len(re.findall(r'[Ѐ-ӿ]', h2))
raw_lt = len(re.findall(r'\\\([^\)]*<[a-zA-Z][^\)]*\\\)', h2))
print("integrity:", ok, "| balance:", rep["balance"], "| dollars:", rep["dollars"])
print("cirilico:", cyr, "| <letra em math:", raw_lt)
if ok and cyr==0 and raw_lt==0:
    open(DOC,"w",encoding="utf-8").write(h2); print("ESCRITO")
else:
    print("NAO ESCRITO")
