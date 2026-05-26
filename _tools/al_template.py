# Reusable template for the AL "material_didatico" HTML series — identical styling to doc1 (PCA).
import re, base64

CSS = r"""
  :root{
    --bg:#fbfaf7; --paper:#ffffff; --ink:#1f2329; --muted:#6b7280; --line:#e7e3da;
    --accent:#3b54c4; --accent-soft:#eef1ff;
    --blue-b:#2f53c0; --blue-bg:#eef2ff;
    --amber-b:#c2790a; --amber-bg:#fff6e6;
    --purple-b:#7a3fc4; --purple-bg:#f5edff;
    --green-b:#1f9a55; --green-bg:#eafaf0;
    --slate-b:#5b6573; --slate-bg:#f3f4f6;
    --code:#f4f2ec;
    --maxw:820px;
  }
  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{
    margin:0; background:var(--bg); color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
    font-size:17px; line-height:1.7; -webkit-font-smoothing:antialiased;
  }
  a{color:var(--accent); text-decoration:none}
  a:hover{text-decoration:underline}

  .layout{
    display:grid; grid-template-columns:262px minmax(0,var(--maxw)); gap:46px;
    justify-content:center; align-items:start; padding:40px 28px 120px;
  }
  /* ---- TOC ---- */
  .toc{
    position:sticky; top:24px; align-self:start; max-height:calc(100vh - 48px);
    overflow-y:auto; font-size:14px; padding:20px 18px; background:var(--paper);
    border:1px solid var(--line); border-radius:14px;
  }
  .toc h2{font-size:12px; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); margin:0 0 12px}
  .toc ol{list-style:none; margin:0; padding:0; counter-reset:t}
  .toc li{margin:2px 0}
  .toc a{display:block; padding:5px 8px; border-radius:8px; color:#3a3f47; line-height:1.35}
  .toc a:hover{background:var(--accent-soft); text-decoration:none}
  .toc .sub{padding-left:18px; font-size:13px; color:var(--muted)}

  /* ---- content ---- */
  main{background:transparent}
  .hero{
    background:linear-gradient(135deg,#2c3e8f,#3b54c4 60%,#5a6fd6);
    color:#fff; border-radius:18px; padding:40px 38px; margin-bottom:14px;
    box-shadow:0 8px 30px rgba(43,62,143,.18);
  }
  .hero .kicker{font-size:13px; letter-spacing:.14em; text-transform:uppercase; opacity:.82}
  .hero h1{margin:.3em 0 .15em; font-size:34px; line-height:1.12; font-weight:800}
  .hero .sub{font-size:18px; opacity:.92; font-weight:500}
  .hero .meta{margin-top:14px; font-size:14px; opacity:.78}

  section{
    background:var(--paper); border:1px solid var(--line); border-radius:16px;
    padding:30px 34px; margin:18px 0; scroll-margin-top:20px;
  }
  h2.sec{font-size:25px; font-weight:800; margin:.1em 0 .7em; line-height:1.2; color:#1a2230}
  h2.sec .num{color:var(--accent); font-variant-numeric:tabular-nums}
  h3{font-size:19px; font-weight:700; margin:1.5em 0 .5em; color:#26303f}
  h4{font-size:16px; font-weight:700; margin:1.2em 0 .4em; color:#37414f}
  p{margin:.7em 0}
  strong{font-weight:700; color:#15191f}
  ul,ol{margin:.6em 0; padding-left:1.4em} li{margin:.3em 0}

  /* callouts */
  .box{border-left:4px solid var(--slate-b); background:var(--slate-bg);
       padding:14px 18px; border-radius:0 12px 12px 0; margin:16px 0}
  .box .tag{display:block; font-size:12px; font-weight:800; letter-spacing:.05em;
            text-transform:uppercase; margin-bottom:5px}
  .box p:first-of-type{margin-top:0} .box p:last-child{margin-bottom:0}
  .intuition{border-color:var(--blue-b); background:var(--blue-bg)} .intuition .tag{color:var(--blue-b)}
  .warning{border-color:var(--amber-b); background:var(--amber-bg)} .warning .tag{color:var(--amber-b)}
  .deep{border-color:var(--purple-b); background:var(--purple-bg)} .deep .tag{color:var(--purple-b)}
  .check{border-color:var(--green-b); background:var(--green-bg)} .check .tag{color:var(--green-b)}

  /* formula block */
  .formula{background:var(--code); border:1px solid var(--line); border-radius:12px;
           padding:6px 20px; margin:16px 0; overflow-x:auto}

  /* tables */
  table{border-collapse:collapse; width:100%; margin:18px 0; font-size:15.5px;
        background:#fff; border:1px solid var(--line); border-radius:10px; overflow:hidden}
  th,td{padding:9px 13px; text-align:left; border-bottom:1px solid var(--line); vertical-align:top}
  thead th{background:#eef0f6; font-weight:700; color:#2a3344; font-size:14px}
  tbody tr:nth-child(even){background:#faf9f6}
  td.c,th.c{text-align:center} td.r{text-align:right; font-variant-numeric:tabular-nums}
  .ans{color:var(--green-b); font-weight:700}

  /* figures */
  figure{margin:22px 0; text-align:center}
  figure img{max-width:100%; height:auto; border:1px solid var(--line);
             border-radius:12px; background:#fff; box-shadow:0 3px 14px rgba(20,30,60,.07)}
  figcaption{font-size:14px; color:var(--muted); font-style:italic; margin-top:9px;
             max-width:680px; margin-left:auto; margin-right:auto; line-height:1.5}

  .lead{font-size:18px; color:#33414f}
  .totop{position:fixed; right:22px; bottom:22px; background:var(--accent); color:#fff;
         width:46px; height:46px; border-radius:50%; display:flex; align-items:center;
         justify-content:center; font-size:20px; box-shadow:0 4px 14px rgba(43,62,143,.4);
         opacity:0; pointer-events:none; transition:opacity .25s}
  .totop.show{opacity:1; pointer-events:auto}
  .totop:hover{text-decoration:none}
  footer{max-width:var(--maxw); margin:20px auto 0; text-align:center; color:var(--muted); font-size:14px}
  .serielink{display:flex;justify-content:space-between;gap:12px;margin:18px 0 0;font-size:14.5px}
  .serielink a{background:var(--accent-soft);padding:8px 14px;border-radius:10px;font-weight:600}

  @media (max-width:980px){
    .layout{grid-template-columns:1fr; gap:0}
    .toc{position:static; max-height:none; margin-bottom:18px}
    section{padding:24px 20px}
    .hero{padding:30px 24px}
    .hero h1{font-size:27px}
    body{font-size:16px}
  }
  .steps3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:20px 0}
  .steps3 .step{background:#f6f8fd;border:1px solid var(--line);border-radius:12px;padding:14px 16px}
  .steps3 .step-h{font-weight:800;color:var(--accent);font-size:14px;margin-bottom:8px;
                  border-bottom:2px solid var(--accent-soft);padding-bottom:6px}
  .steps3 .step p{margin:.45em 0;font-size:15px}
  @media(max-width:760px){.steps3{grid-template-columns:1fr}}
"""

HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<script>
  MathJax = {{
    tex: {{ inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']] }},
    svg: {{ fontCache: 'global' }}
  }};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
<style>{css}</style>
</head>
<body>

<div class="layout">

  <nav class="toc">
    <h2>Índice</h2>
    <ol>
{toc}
    </ol>
  </nav>

  <main>
    <header class="hero">
      <div class="kicker">{kicker}</div>
      <h1>{h1}</h1>
      <div class="sub">{sub}</div>
      <div class="meta">{meta}</div>
    </header>

{body}

    <footer>
{footer}
    </footer>
  </main>
</div>

<a href="#" class="totop" aria-label="Voltar ao topo">↑</a>
<script>
  const btn = document.querySelector('.totop');
  addEventListener('scroll', () => btn.classList.toggle('show', scrollY > 600));
</script>
</body>
</html>
"""

def build(title, kicker, h1, sub, meta, toc, body, footer):
    return HEAD.format(title=title, css=CSS, kicker=kicker, h1=h1, sub=sub, meta=meta,
                       toc=toc, body=body, footer=footer)

def embed(html, mapping):
    """mapping: {alt_text: png_path}. Replaces empty/placeholder src in <img ... alt="ALT"> with base64."""
    for alt, png in mapping.items():
        b64 = base64.b64encode(open(png, "rb").read()).decode()
        pat = re.compile(r'(<img[^>]*\bsrc=")[^"]*("[^>]*\balt="' + re.escape(alt) + r'")')
        html, n = pat.subn(lambda m: m.group(1) + "data:image/png;base64," + b64 + m.group(2), html)
        assert n == 1, "embed %r -> %d (expected 1)" % (alt, n)
    return html

def integrity(html, expect_imgs):
    import re as _r
    checks = {
        "sections": (html.count("<section"), html.count("</section>")),
        "divs": (html.count("<div"), html.count("</div>")),
        "figures": (html.count("<figure>"), html.count("</figure>")),
        "scripts": (len(_r.findall(r'<script\b', html)), html.count("</script>")),
    }
    imgs = len(_r.findall(r'<img ', html)); b64 = html.count("data:image/png;base64,")
    empty = len(_r.findall(r'<img[^>]*src=""', html)) + len(_r.findall(r'src="data:image/png;base64,"', html))
    dollars = html.count("$")
    ok = all(a == b for a, b in checks.values()) and imgs == expect_imgs == b64 and empty == 0 and dollars == 0
    return ok, {"balance": checks, "imgs": imgs, "b64": b64, "empty_src": empty, "dollars": dollars}
