#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ajusta a ponte para a caixa do truncamento: corrige 'maior componente do gradiente'
(-> entre as que estao fora do suporte), torna explicito que o algoritmo do gradiente eh
guloso POR NATUREZA, e relaciona isso ao espaco cortado por k e ao truncamento."""
import re, sys
sys.path.insert(0, "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools")
from al_template import integrity

DOC = "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/02_sparse_pca_o_problema.html"
html = open(DOC, encoding="utf-8").read()

NEW_BRIDGE = r"""<p>No fundo, o <strong>algoritmo do gradiente é guloso por natureza</strong>: ele enxerga só o modelo de
      1ª ordem — a inclinação imediata — e a cada passo toma a direção localmente mais íngreme, sem nunca rever a
      escolha. Num espaço <em>liso</em> essa ganância ao menos te leva a um ótimo local. Mas o espaço
      <strong>cortado por \(k\)</strong> (a esparsidade) não é liso — é uma colcha de pedaços colados nas quinas —, e
      aí a ganância cobra o preço: ou o gradiente fica <strong>preso no pico de um pedaço</strong> (não cruza a crista
      até um melhor), ou, ao decidir numa quina <em>qual</em> pedaço entrar, ele só agarra a variável localmente mais
      íngreme — a <strong>maior componente do gradiente entre as que ainda estão fora do suporte</strong> (no nosso
      canto, \(x_2\), pois \(2{,}4\gt1{,}6\); não \(x_1\), que já está dentro).</p>
      <p>O <strong>truncamento</strong> é essa mesma ganância mecanizada: dá o passo do gradiente no espaço cheio e
      fica com as \(k\) maiores componentes — ou seja, aposta nas variáveis que o gradiente mais quer
      <em>localmente</em>. É o que a próxima caixa detalha; e, por ser uma aposta míope, ela pode sair errada (a
      sutileza logo adiante).</p>"""

pat = re.compile(r'<p>Então o método guloso.*?a próxima caixa mostra\.</p>', re.DOTALL)
html, n = pat.subn(lambda m: NEW_BRIDGE, html)
assert n == 1, ("ponte", n)

ok, rep = integrity(html, 10)
print("integrity:", ok, "| dollars:", rep["dollars"], "| divs:", rep["balance"]["divs"])
assert ok, rep
open(DOC, "w", encoding="utf-8").write(html)
print("OK: ponte ajustada (guloso por natureza + k-cut + truncamento).")
