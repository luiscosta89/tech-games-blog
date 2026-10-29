#!/usr/bin/env python3
from pathlib import Path
import html
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "_source" / "10-jogos-2026.md"
TITLE = "OPINIÃO | 10 jogos de 2026 que você deveria jogar"
DEK = "De trens que fazem manobras a fotógrafos perdidos em mundos espirituais: dez jogos independentes que merecem entrar no seu radar."


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def inline_markdown(value: str) -> str:
    value = html.escape(value.strip())
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"_(.+?)_", r"<em>\1</em>", value)
    return value


def article_body(markdown: str):
    chunks, toc = [], []
    for raw in markdown.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#### "):
            title = line[5:].replace("\u00a0", " ")
            anchor = slugify(title)
            toc.append((anchor, title))
            chunks.append(f'<h2 id="{anchor}">{html.escape(title)}</h2>')
        elif line.startswith("[iframe]"):
            match = re.search(r"embed%2F([^%&]+)", line)
            if match:
                video_id = match.group(1)
                chunks.append(
                    '<div class="video">'
                    f'<button type="button" data-video="{html.escape(video_id)}" aria-label="Reproduzir trailer no YouTube">'
                    f'<img loading="lazy" src="https://i.ytimg.com/vi/{html.escape(video_id)}/hqdefault.jpg" alt="Miniatura do trailer">'
                    '</button></div>'
                )
        elif line.startswith("**ATENÇÃO:"):
            chunks.append(f'<p class="notice">{inline_markdown(line)}</p>')
        elif line.startswith("_Por Luís"):
            chunks.append(f'<p><em>Por Luís Antônio Costa.</em></p>')
        else:
            chunks.append(f'<p>{inline_markdown(line)}</p>')
    return "\n".join(chunks), toc


def header(prefix=""):
    return f'''<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
<header class="site-header">
  <nav class="nav" aria-label="Principal">
    <a class="brand" href="{prefix}index.html"><img src="{prefix}assets/images/sagitta-tech.png" alt=""><span>Sagitta<span class="brand-mark">Tech</span></span></a>
    <div class="nav-links"><a href="{prefix}index.html#artigos">Artigos</a></div>
  </nav>
</header>'''


def footer(prefix=""):
    return '''<footer class="site-footer"><div class="container footer-inner"><span>© 2026 Sagitta Tech · Luís Antônio Costa</span><span>Publicado com GitHub Pages</span></div></footer>'''


def page(title, body, prefix="", description=DEK):
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#08090b">
  <meta name="description" content="{html.escape(description)}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{prefix}assets/images/10-jogos-2026-cover.png">
  <title>{html.escape(title)} · Sagitta Tech</title>
  <link rel="icon" href="{prefix}assets/images/sagitta-tech.png">
  <link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
{header(prefix)}
{body}
{footer(prefix)}
<script src="{prefix}assets/site.js"></script>
</body>
</html>'''


def build_article(markdown):
    prose, toc = article_body(markdown)
    toc_html = "\n".join(f'<a href="#{a}">{html.escape(t)}</a>' for a, t in toc)
    body = f'''<main id="conteudo" class="article-shell">
  <header class="article-header">
    <span class="eyebrow">Opinião · Games</span>
    <h1>{html.escape(TITLE)}</h1>
    <p class="dek">{html.escape(DEK)}</p>
    <div class="meta"><span class="author"><img src="../assets/images/sagitta-tech.png" alt="">Luís Antônio Costa</span><span>14 out. 2026</span><span>7 min de leitura</span></div>
  </header>
  <img class="cover" src="../assets/images/10-jogos-2026-cover.png" alt="Montagem colorida com personagens dos dez jogos selecionados">
  <div class="article-layout">
    <article class="prose">{prose}</article>
    <aside class="toc" aria-label="Neste artigo"><strong>Neste artigo</strong>{toc_html}</aside>
  </div>
</main>'''
    return page(TITLE, body, prefix="../")


def build_home():
    body = '''<main id="conteudo">
  <section class="container hero">
    <div><span class="eyebrow">Tecnologia · Games · Cultura</span><h1>Ideias que acertam o alvo.</h1><p class="hero-copy">Análises, opiniões e descobertas sobre os jogos e as tecnologias que merecem o seu tempo.</p></div>
    <aside class="hero-aside"><span class="label">Sobre o Sagitta Tech</span><p>Uma flecha certeira na direção do que há de mais interessante no mundo da tecnologia e dos games, por Luís Antônio Costa.</p></aside>
  </section>
  <section id="artigos" class="container section">
    <div class="section-head"><h2>Em destaque</h2><p>Reportagens e opiniões com contexto, personalidade e sem perder tempo com o óbvio.</p></div>
    <a class="feature-card" href="articles/10-jogos-2026.html">
      <div class="feature-media"><img src="assets/images/10-jogos-2026-cover.png" alt="Montagem colorida dos jogos selecionados"></div>
      <div class="feature-copy"><div class="tags"><span class="tag">Opinião</span><span class="tag">Indie games</span><span class="tag">2026</span></div><h3>10 jogos de 2026 que você deveria jogar</h3><p>Uma seleção de experiências independentes que ficaram fora do radar — mas não deveriam.</p><span class="read-more">Ler artigo <span aria-hidden="true">→</span></span></div>
    </a>
  </section>
</main>'''
    return page("Tecnologia e games", body, description="Sagitta Tech: análises, opiniões e descobertas sobre tecnologia e games.")


def main():
    markdown = SOURCE.read_text(encoding="utf-8")
    (ROOT / "articles" / "10-jogos-2026.html").write_text(build_article(markdown), encoding="utf-8")
    (ROOT / "index.html").write_text(build_home(), encoding="utf-8")
    print("Built index.html and articles/10-jogos-2026.html")


if __name__ == "__main__":
    main()
