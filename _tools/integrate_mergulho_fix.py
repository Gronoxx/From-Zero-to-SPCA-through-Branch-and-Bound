#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integra as 3 correcoes na caixa 'A profundidade e deterministica' (doc 02):
  C1: troca a prosa 'invisivel nas quinas' por pargrafo construtivo + figura; ajusta a frase-ligacao.
  C2: corrige o 'mata a armadilha' (a armadilha some por olhar UMA bacia; autovalor so e mais rapido).
  C3: troca a tabela de 3 linhas por uma de 4 linhas POR DOMINIO; ajusta a frase de introducao.
Depois embute a figura (base64) e roda integrity().
"""
import sys
sys.path.insert(0, "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools")
from al_template import embed, integrity

DOC = "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/02_sparse_pca_o_problema.html"
FIG = "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools/fig_mergulho_decomposicao.png"

html = open(DOC, encoding="utf-8").read()

def lit(old, new):
    global html
    n = html.count(old)
    assert n == 1, "ancora %d ocorrencias (esperado 1): %r" % (n, old[:70])
    html = html.replace(old, new)

# ---------------- C1a: pargrafo 'Mas tem um porem decisivo' -> construtivo + figura ----------
OLD1 = r"""        <p><strong>Mas tem um porém decisivo: o mergulho também precisa do acoplamento \(Q_{ij}\) — e ele é
        invisível nas quinas.</strong> As alturas das pontas dão <em>só</em> \(Q_{ii}\) e \(Q_{jj}\); \(Q_{ij}\)
        não aparece em canto nenhum. No \(Q\) do relevo desta seção:</p>"""
NEW1 = r"""        <p><strong>A profundidade é toda montada a partir de \(Q\) — nada fica de fora.</strong>
        As alturas das pontas dão \(Q_{ii}\) e \(Q_{jj}\); o <strong>mergulho</strong> traz o acoplamento
        \(Q_{ij}\), que está na matriz mas <em>não se lê nas alturas das pontas</em>. Por isso dois arcos com
        pontas idênticas podem ter fundos bem diferentes — é o que a figura constrói passo a passo:</p>
      <figure>
        <img src="" alt="mergulho decomposicao">
        <figcaption><strong>Esquerda (A).</strong> O relevo das três bacias (caminho
        \(e_1\!\to\!e_2\!\to\!e_3\!\to\!e_1\)), com cada quina rotulada em \(Q\): \(e_1\to Q_{11}=2{,}0\),
        \(e_2\to Q_{22}=2{,}2\), \(e_3\to Q_{33}=1{,}6\). Na bacia azul \(\{x_1,x_2\}\) a profundidade é
        <strong>construída</strong>: do <em>meio das pontas</em> \((Q_{11}+Q_{22})/2=2{,}10\) desce um
        <em>mergulho</em> de \(1{,}20\) (a raiz, com a assimetria das pontas e o acoplamento \(Q_{12}\)) até o
        <strong>fundo \(=\lambda_{\max}=3{,}30\)</strong>. <strong>Direita (B).</strong> Dois arcos com
        <strong>pontas idênticas</strong> \((2{,}0;\,2{,}0)\): com acoplamento \(0\) o fundo é \(2{,}00\) (arco
        plano); com acoplamento \(1{,}5\), \(3{,}50\). Mesmas alturas, fundos diferentes — o mergulho vem do
        <strong>acoplamento</strong>, que só sai da submatriz.</figcaption>
      </figure>"""
lit(OLD1, NEW1)

# ---------------- C1b: frase-ligacao depois da tabela numerica ---------------------------------
OLD2 = r"""        <p>No arco azul o mergulho ao quadrado é \(0{,}01\) (a assimetria das pontas) \(+\;1{,}44\) (o
        acoplamento): o acoplamento responde por <strong>\(99{,}3\%\)</strong>. A compensação de altura existe,
        mas aqui é desprezível — quem manda no fundo é o \(Q_{ij}\), que não se vê na figura. O golpe final são
        dois arcos com <strong>pontas idênticas</strong> (\(Q_{ii}=Q_{jj}=2\)): com acoplamento \(0\) o fundo é
        \(2{,}00\) (arco plano, sem mergulho); com acoplamento \(1{,}5\) o fundo é \(3{,}50\). Mesmas alturas,
        profundidades bem diferentes. <strong>Logo: as alturas das pontas, mesmo compensadas, não determinam o
        fundo</strong> — falta o acoplamento, que só sai da submatriz.</p>"""
NEW2 = r"""        <p>Na tabela, o mergulho ao quadrado do arco azul é \(0{,}01\) (assimetria das pontas) \(+\;1{,}44\)
        (acoplamento): o \(Q_{12}\) responde por <strong>\(99{,}3\%\)</strong> do mergulho. Ou seja, as alturas
        das pontas — mesmo "compensadas" pelo meio — <strong>não determinam o fundo</strong>; ele se completa
        com o acoplamento, exatamente como o painel B mostra.</p>"""
lit(OLD2, NEW2)

# ---------------- C2: 'Entao e so trocar o gradiente...' (corrige 'mata a armadilha') ----------
OLD3 = r"""        <p><strong>"Então é só trocar o gradiente pela conta do autovalor em cada conjunto?"</strong> É — e essa
        é a ideia <em>certa</em>. Ela tem duas vantagens reais sobre a descida: (i) <strong>mata a
        armadilha</strong>, porque \(\lambda_{\max}\) é o ótimo <em>exato</em> de cada suporte (Rayleigh num
        círculo não tem mínimo local que prenda) — nunca ficamos presos; e (ii) cada suporte vira <strong>uma
        conta determinística</strong> (um autovalor), não uma descida iterativa. Isso não é um truque qualquer: é
        o <strong>algoritmo exato ingênuo</strong> do Sparse PCA, e é <em>estritamente melhor</em> que o
        guloso/truncamento, que é rápido mas pode errar o suporte.</p>"""
NEW3 = r"""        <p><strong>"Então é só trocar o gradiente pela conta do autovalor em cada conjunto?"</strong> É — e essa
        é a ideia <em>certa</em>, mas é preciso situar de onde vem a vantagem. <strong>A armadilha some quando
        se olha uma bacia de cada vez</strong>, não por causa do autovalor: numa bacia fixa o quociente de
        Rayleigh no círculo é <em>unimodal</em> — não há mínimo local que prenda. Tanto a descida bacia a bacia
        quanto o autovalor encontram o mesmo fundo; a descida <strong>converge</strong> até ele (sem armadilha),
        e o autovalor <strong>já o dá</strong> por uma fórmula fechada \(2\times2\). Logo a única vantagem do
        autovalor sobre a descida bacia a bacia é <strong>custo por bacia</strong> (uma conta determinística no
        lugar de iterar), <em>não</em> correção de erro — as duas são exatas. É o <strong>algoritmo exato
        ingênuo</strong> do Sparse PCA, e é melhor que o guloso/truncamento, que é rápido mas pode errar o
        suporte porque desce a superfície inteira e cai na armadilha.</p>"""
lit(OLD3, NEW3)

# ---------------- C3a: frase final do 'O que ele nao resolve' -> introducao por dominio --------
OLD4 = """O resultado é exato sempre, e viável só enquanto \\(\\binom{n}{k}\\) for
        pequeno:</p>"""
NEW4 = """Vale exato sempre, mas viável só enquanto \\(\\binom{n}{k}\\) for pequeno. Lado a lado, separando bem o
        <strong>domínio</strong> de cada estratégia (superfície inteira × uma bacia por vez):</p>"""
lit(OLD4, NEW4)

# ---------------- C3b: tabela de 3 linhas -> tabela de 4 linhas (5 colunas) por dominio ---------
OLD5 = r"""        <table>
          <thead><tr><th>estratégia</th><th class="c">exata?</th><th>custo</th><th>quando funciona</th></tr></thead>
          <tbody>
            <tr><td>Heurística (guloso / truncamento)</td><td class="c">não — cai em armadilha</td><td>\(\approx\) 1 conta</td><td>sempre rápida, mas pode errar o suporte</td></tr>
            <tr><td><strong>Enumeração por autovalor</strong> (a ideia acima)</td><td class="c">sim</td><td>\(\binom{n}{k}\) autovalores</td><td>só com \(n,k\) pequenos</td></tr>
            <tr><td>Branch-and-Bound (§5)</td><td class="c">sim</td><td>autovalor + poda de famílias</td><td>instâncias grandes, na prática</td></tr>
          </tbody>
        </table>"""
NEW5 = r"""        <table>
          <thead><tr>
            <th>estratégia</th>
            <th>domínio (o que olha)</th>
            <th class="c">exata?</th>
            <th>custo</th>
            <th class="c">cai na armadilha?</th>
          </tr></thead>
          <tbody>
            <tr>
              <td>Gradiente único na superfície inteira</td>
              <td>todas as bacias por <em>uma</em> descida lisa na união desconexa</td>
              <td class="c">não</td>
              <td class="r">1 descida</td>
              <td class="c"><strong>sim</strong> (truncamento/guloso é a versão espectral)</td>
            </tr>
            <tr>
              <td>Gradiente bacia a bacia</td>
              <td>uma bacia fixa de cada vez</td>
              <td class="c">sim</td>
              <td class="r">descida iterativa \(\times\,\binom{n}{k}\)</td>
              <td class="c">não</td>
            </tr>
            <tr>
              <td><strong>Autovalor bacia a bacia</strong> (a ideia acima)</td>
              <td>uma bacia fixa de cada vez</td>
              <td class="c">sim</td>
              <td class="r">1 autovalor \(\times\,\binom{n}{k}\)</td>
              <td class="c">não</td>
            </tr>
            <tr>
              <td>Branch-and-Bound (§5)</td>
              <td>famílias de bacias (enumeração implícita)</td>
              <td class="c">sim</td>
              <td class="r">autovalor + poda de famílias</td>
              <td class="c">não — não desce, poda</td>
            </tr>
          </tbody>
        </table>"""
lit(OLD5, NEW5)

# ---------------- embute a figura e verifica --------------------------------------------------
html = embed(html, {"mergulho decomposicao": FIG})
ok, rep = integrity(html, 11)
print("integrity:", ok)
for k, v in rep.items():
    print("  ", k, v)

if ok:
    open(DOC, "w", encoding="utf-8").write(html)
    print("OK: doc 02 atualizado (10 -> 11 figuras).")
else:
    print("FALHA — nada escrito.")
    sys.exit(1)
