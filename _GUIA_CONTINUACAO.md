# Guia de continuação — Material didático de Sparse PCA (AL)

> Leia isto + `coursework/AL/CLAUDE.md` antes de continuar. Este guia existe para uma **nova sessão** retomar o
> trabalho sem perder contexto.

## 1. O que é este projeto
Série de **documentos HTML didáticos** que ensinam, do zero, tudo o que o Gustavo precisa para fazer o **trabalho
da Lista** (`coursework/AL/amalo-lista1 (2).pdf`): implementar o **Branch-and-Bound para Sparse PCA**
(Optimal-SPCA, Berk & Bertsimas 2019). Decisão do aluno: **aprender cada passo > prazo**.

Os documentos são para **estudar** (entender cada peça antes de codar). A implementação em si (Fases 1–7) é a etapa
seguinte — ainda não começou.

## 2. Arquivos (pasta `coursework/AL/material_didatico/`)
- `index.html` — landing/trilha de estudo (links 01→05).
- `01_pca_classico.html` — PCA clássico (cópia idêntica à de `~/Downloads/PCA_documento_didatico.html`).
- `02_sparse_pca_o_problema.html` — Sparse PCA: o problema (ℓ0, NP-difícil, relaxação convexa).
- `03_primitivas_espectrais_power_method.html` — método da potência, RQI, Trunc.
- `04_branch_and_bound_sparse_pca.html` — B&B: árvore, 5 cotas, poda, gap.
- `05_deflacao_variancia_qr.html` — deflação, variância acumulada via QR, critério 70%.
- `_tools/al_template.py` — **template reutilizável** (CSS + `build()` + `embed()` + `integrity()`). Use sempre.
- `_GUIA_CONTINUACAO.md` — este arquivo.

**Fontes para aterrar conteúdo:** a Lista (`amalo-lista1 (2).pdf`, 4 págs), o artigo Berk & Bertsimas
(`Module 2/Certifiably optimal sparse principal component analys.pdf`, 40 págs — extraia texto com pypdf para
grep, evite ler como imagem), e `coursework/AL/cobertura_al.md` (gaps de conhecimento do aluno).

## 3. Estado atual (o que já foi revisado COM o usuário)
O usuário revisa **seção por seção** e dá feedback; eu aplico. Até agora:
- **01 (PCA clássico): completo e muito refinado.** Inclui: prova intuitiva da melhor projeção (§4.4.3), figura
  ρ=0 vs ρ alto (§4.6), animação canvas da transformação Σ (§4.4.1), SVD (§6.3), §7 reestruturado (mudança de
  base → projeção → redução) + §7.5 (representação 1D), §8 (exemplo 4D→2D estilo Íris + problema do PCA denso),
  §8.5 (trade-off do sparse: o "botão" da esparsidade).
- **02 (Sparse PCA o problema): §1, §2 e §2.1 já refinados** — caixa Lasso reescrita (intuição sem jargão + caixa
  que define regularização/Lasso/convexo/relaxação do zero, §1.1 com a figura convexo-vs-não-convexo e os números
  da Tabela 6 do artigo); norma ℓ0 explicada devagar (§2); §2.1 com figura per-k (pontos→círculos→esfera), a
  distinção ‖·‖₂ (magnitude) vs ‖·‖₀ (contagem), por que vetor unitário, e a caixa "por que é difícil" (figura das
  quinas + gradiente + disjunção + força bruta ingênua → gancho do B&B). **§3–§8 ainda NÃO foram revistos com o
  usuário.**
- **03, 04, 05, index: gerados, mas NÃO revisados com o usuário.** Provavelmente terão ajustes parecidos.

**Próximo passo natural:** continuar a revisão do documento 02 a partir da **§3** (a formulação), depois 03 → 04 →
05, no mesmo modo (usuário aponta, você ajusta).

## 4. Convenções de FIGURAS (lições aprendidas — siga à risca)
- matplotlib, **dpi=200**, paleta: accent `#3b54c4`, blue `#2f53c0`, amber `#c2790a`, purple `#7a3fc4`,
  green `#1f9a55`, slate `#5b6573`, dark `#1f3b6e`, grey `#9aa0aa`, red `#b23b3b`.
- Embuta como **base64** via `embed(html, {alt: png_path})`. As âncoras `alt="..."` são **ASCII de propósito**
  (sem acento) — não "corrija" os acentos delas; são chaves do embed.
- **SEMPRE renderize e VEJA cada figura** antes de declarar pronto. Sobreposição de rótulo é o problema nº 1
  recorrente — o usuário pega todas. Para ver: redimensione para ≤ ~1200px de largura e leia **uma por vez** (o
  leitor de imagem rejeita >2000px em requisição múltipla).
- mathtext do matplotlib: use `\leq`/`\geq` (não `\le`), `\binom` ok; decimais com vírgula via `.replace('.',',')`.
- Layout: rótulos em **regiões vazias distintas**; legendas/explicações longas vão na **figcaption**, não dentro do
  gráfico; para sequências, painéis grandes/empilhados são mais legíveis que muitos painéis estreitos.

## 5. Convenções de TEXTO
- PT-BR, intuição **geométrica primeiro**, formalização depois. Gramática **simples** (evite travessões ambíguos
  que tornam a frase confusa — o usuário reclamou disso).
- **Defina cada termo do zero** — não assuma nada além do que os documentos anteriores apresentaram.
- **Quebre passagens densas em passos pequenos**, ticados na figura ("painel k=1…").
- **Sem tom de errata/autocorreção** ("eu havia me confundido…") — só o usuário leu; explique certo de primeira.
- **Honesto sobre trade-offs**; **ancore números no artigo** (ex.: Tabela 6 de variância explicada).
- MathJax: inline `\(...\)`, display `\[...\]`. **NUNCA** `$...$` (conflito com R$). O único `$` legítimo é "R$"
  (moeda) no doc 01 — por isso `integrity` aceita `dollars==2` só lá; nos demais deve ser `0`.
- **NUNCA** use `<` cru seguido de letra dentro de math inline (`\(k<n\)`): o navegador interpreta `<n…` como tag
  e **engole o texto**. Use `\lt` (e `\gt`). `k<=` dentro de `<script>` (JS) é seguro.

## 6. Rotina de VERIFICAÇÃO (a cada edição)
Use `integrity(html, n_figs_esperado)` do template:
- tags balanceadas (`<section>/<div>/<figure>/<script>`), nº de `<img>` == nº de base64, nenhum `src` vazio,
  `dollars==0` (exceto doc 01 = 2, por causa de "R$").
- **Diacríticos:** grep por formas sem acento, mas lembre que muitas palavras são corretas sem acento
  (esfera, gradiente, comum, ortogonais, magnitude, geometria, ingênua→"ingenua"? não: tem acento). Só conte como
  erro perdas reais (variancia→variância, projecao→projeção, etc.).
- **Cirílico:** `grep [Ѐ-ӿ]` deve dar 0 (já houve um "caберia" acidental).
- Cole o doc atualizado de volta em `~/Downloads/...` só para o doc 01 (que o usuário abre dos dois lugares); os
  demais vivem só em `material_didatico/`.

## 7. Rigor matemático (o usuário PEGA erros — seja cuidadoso)
Erros já corrigidos nesta jornada, como alerta:
- função **simétrica** → dois mínimos iguais; não chame um de "ótimo" e outro de "armadilha" (use assimétrica).
- **relaxação convexa NÃO trava em mínimo local** (convexo = um vale só); quem trava são os métodos locais
  não-convexos. São duas famílias distintas.
- arredondamento de percentuais consistente (94+3 = 97, não 98).
- linguagem **genérica**: é "esfera" só em n=3; em geral é a esfera unitária de n dimensões.

## 8. Como invocar o template (exemplo)
```python
import sys; sys.path.insert(0, "/Users/gustavo/Claude Code/thesis/coursework/AL/material_didatico/_tools")
from al_template import build, embed, integrity
# build(title, kicker, h1, sub, meta, toc_html, body_html, footer_html) -> HTML completo
# embed(html, {"alt do <img>": "/caminho/fig.png"}) -> troca o src por base64
# integrity(html, n_figs) -> (ok, relatório)
```
Para EDITAR um doc existente: leia o HTML, ache o trecho (regex com `re.DOTALL` + `subn(lambda m: novo, h)` para
não quebrar com backslashes do LaTeX), troque, re-`embed` figuras novas, rode `integrity`, escreva.

## 9. Próximos passos
1. Continuar a revisão do **doc 02 a partir da §3** (e depois §4–§8) com o usuário.
2. Revisar **03, 04, 05, index** (provavelmente ajustes de figura/clareza semelhantes).
3. (Futuro) Implementar a Lista — Fases 1–7 (tasks #2–#8 no rastreador). Os documentos são a base conceitual.
