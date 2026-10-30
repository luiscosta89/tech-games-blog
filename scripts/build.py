#!/usr/bin/env python3
from pathlib import Path
import html
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DEK = "Análises, opiniões e descobertas sobre tecnologia, games e cultura."
ASSET_VERSION = "20261029-wide-articles"

ARTICLES = [
    {
        "slug": "o-que-aconteceu-com-o-php",
        "source": "o-que-aconteceu-com-o-php.md",
        "title": "MOMENTO TECH | O que aconteceu com o PHP?",
        "card_title": "O que aconteceu com o PHP?",
        "category": "Momento Tech",
        "topic": "Tecnologia",
        "date": "29 out. 2026",
        "reading": "8 min de leitura",
        "dek": "Da popularização da Web às vulnerabilidades críticas de 2026: como o PHP evoluiu e por que sua segurança voltou ao centro do debate.",
        "card_dek": "A história, a evolução e as falhas recentes que recolocaram o PHP no centro das discussões sobre segurança.",
        "cover": "assets/images/o-que-aconteceu-com-o-php/cover.png",
        "cover_alt": "Logotipo do PHP sobre fundo azul",
        "tags": ["Momento Tech", "PHP", "Segurança"],
        "images": ["image-01.jpg", "image-02.jpg", "image-03.jpg", "image-04.jpg", "image-05.jpg", "image-06.jpg", "image-07.jpg"],
    },
    {
        "slug": "10-jogos-2026",
        "source": "10-jogos-2026.md",
        "title": "OPINIÃO | 10 jogos de 2026 que você deveria jogar",
        "card_title": "10 jogos de 2026 que você deveria jogar",
        "category": "Opinião",
        "date": "14 out. 2026",
        "reading": "7 min de leitura",
        "dek": "De trens que fazem manobras a fotógrafos perdidos em mundos espirituais: dez jogos independentes que merecem entrar no seu radar.",
        "card_dek": "Uma seleção de experiências independentes que ficaram fora do radar — mas não deveriam.",
        "cover": "assets/images/10-jogos-2026-cover.png",
        "cover_alt": "Montagem colorida com personagens dos dez jogos selecionados",
        "tags": ["Opinião", "Indie games", "2026"],
        "images": [],
    },
    {
        "slug": "1000xresist",
        "source": "1000xresist.md",
        "title": "REVIEW | 1000xResist é um jogo que permanece e permanece e permanece",
        "card_title": "1000xResist permanece e permanece e permanece",
        "category": "Review",
        "date": "20 fev. 2026",
        "reading": "6 min de leitura",
        "dek": "Memória, identidade e resistência se entrelaçam em uma das narrativas de ficção científica mais marcantes dos games.",
        "card_dek": "Uma ficção científica sobre memória, diáspora e os ciclos que insistimos em repetir.",
        "cover": "assets/images/1000xresist/cover.png",
        "cover_alt": "Arte de capa de 1000xResist",
        "tags": ["Review", "Ficção científica", "Indie games"],
        "images": ["image-01.jpg", "image-02.jpg", "image-03.jpg", "image-04.jpg", "image-05.jpg", "image-06.jpg"],
    },
    {
        "slug": "sword-of-the-sea",
        "source": "sword-of-the-sea.md",
        "title": "OPINIÃO | Sword of the Sea surfa na onda da pura beleza",
        "card_title": "Sword of the Sea surfa na onda da pura beleza",
        "category": "Opinião",
        "date": "27 ago. 2025",
        "reading": "4 min de leitura",
        "dek": "Uma aventura contemplativa que transforma areia, água e movimento em um espetáculo visual.",
        "card_dek": "Uma jornada breve e contemplativa, conduzida por beleza, movimento e uma trilha sublime.",
        "cover": "assets/images/sword-of-the-sea/cover.png",
        "cover_alt": "Arte de capa de Sword of the Sea",
        "tags": ["Opinião", "Indie games", "PS5"],
        "images": ["image-01.jpg", "image-02.jpg", "image-03.jpg", "image-04.jpg"],
    },
]


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def inline_markdown(value: str) -> str:
    value = html.escape(value.strip())
    # Keep internal Medium references as plain text; preserve other editorial credits.
    value = re.sub(r"\[([^]]+)\]\(https?://(?:[^)]*\.)?medium\.com/[^)]+\)", r"\1", value)
    value = re.sub(r"\[([^]]+)\]\((https?://[^)]+)\)", r'<a href="\2" rel="noopener noreferrer">\1</a>', value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"_(.+?)_", r"<em>\1</em>", value)
    return value


def article_body(article, markdown: str):
    chunks, toc = [], []
    image_index = 0
    quote_open = False

    def close_quote():
        nonlocal quote_open
        if quote_open:
            chunks.append("</blockquote>")
            quote_open = False

    for raw in markdown.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(">"):
            if not quote_open:
                chunks.append("<blockquote>")
                quote_open = True
            text = line[1:].strip()
            if text:
                chunks.append(f"<p>{inline_markdown(text)}</p>")
            continue
        close_quote()
        if line.startswith(("### ", "#### ")):
            title = re.sub(r"^#{3,4}\s+", "", line).replace("\u00a0", " ")
            anchor = slugify(title)
            toc.append((anchor, title))
            chunks.append(f'<h2 id="{anchor}">{html.escape(title)}</h2>')
        elif line.startswith("[iframe]"):
            match = re.search(r"embed%2F([^%&]+)", line)
            if match:
                video_id = match.group(1)
                chunks.append(
                    '<div class="video">'
                    f'<button type="button" data-video="{html.escape(video_id)}" aria-label="Reproduzir vídeo no YouTube">'
                    f'<img loading="lazy" src="https://i.ytimg.com/vi/{html.escape(video_id)}/hqdefault.jpg" alt="Miniatura do vídeo">'
                    '</button></div>'
                )
        elif line.startswith("![]("):
            if image_index < len(article["images"]):
                image_name = article["images"][image_index]
                image_index += 1
                chunks.append(
                    f'<figure class="article-image"><img loading="lazy" src="../assets/images/{article["slug"]}/{image_name}" '
                    f'alt="Imagem do artigo {html.escape(article["card_title"])}"></figure>'
                )
        elif line.startswith("**ATENÇÃO:"):
            chunks.append(f'<p class="notice">{inline_markdown(line)}</p>')
        elif line.startswith("_Por Luís"):
            chunks.append('<p class="byline"><em>Por Luís Antônio Costa.</em></p>')
        else:
            chunks.append(f'<p>{inline_markdown(line)}</p>')
    close_quote()
    return "\n".join(chunks), toc


def header(prefix=""):
    return f'''<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
<header class="site-header">
  <nav class="nav" aria-label="Principal">
    <a class="brand" href="{prefix}index.html"><img src="{prefix}assets/images/sagitta-tech.png" alt=""><span>Sagitta<span class="brand-mark">Tech</span></span></a>
    <div class="nav-links"><a href="{prefix}index.html#artigos">Artigos</a><a href="{prefix}categories/momento-tech.html">Momento Tech</a><a href="{prefix}categories/review.html">Review</a><a href="{prefix}categories/opiniao.html">Opinião</a></div>
  </nav>
</header>'''


def footer(prefix=""):
    return '''<footer class="site-footer"><div class="container footer-inner"><span>© 2026 Sagitta Tech · Luís Antônio Costa</span><span>Publicado com GitHub Pages</span></div></footer>'''


def page(title, body, prefix="", description=DEFAULT_DEK, image="assets/images/10-jogos-2026-cover.png", page_type="website"):
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#08090b">
  <meta name="description" content="{html.escape(description)}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:type" content="{page_type}">
  <meta property="og:image" content="{prefix}{image}">
  <title>{html.escape(title)} · Sagitta Tech</title>
  <link rel="icon" href="{prefix}assets/images/sagitta-tech.png">
  <link rel="stylesheet" href="{prefix}assets/style.css?v={ASSET_VERSION}">
</head>
<body>
{header(prefix)}
{body}
{footer(prefix)}
<script src="{prefix}assets/site.js"></script>
</body>
</html>'''


def article_card(article, prefix="", compact=True):
    tags = "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in article["tags"])
    klass = "story-card" if compact else "feature-card"
    if compact:
        return f'''<a class="story-card" href="{prefix}articles/{article["slug"]}.html">
      <div class="story-copy"><div class="story-meta"><span>{html.escape(article["category"])}</span><span>{html.escape(article["date"])}</span></div><h3>{html.escape(article["card_title"])}</h3><p>{html.escape(article["card_dek"])}</p></div>
      <div class="story-media"><img loading="lazy" src="{prefix}{article["cover"]}" alt="{html.escape(article["cover_alt"])}"></div>
    </a>'''
    return f'''<a class="{klass}" href="{prefix}articles/{article["slug"]}.html">
      <div class="feature-media"><img loading="lazy" src="{prefix}{article["cover"]}" alt="{html.escape(article["cover_alt"])}"></div>
      <div class="feature-copy"><div class="tags">{tags}</div><h3>{html.escape(article["card_title"])}</h3><p>{html.escape(article["card_dek"])}</p><span class="read-more">Ler artigo <span aria-hidden="true">→</span></span></div>
    </a>'''


def build_article(article):
    markdown = (ROOT / "_source" / article["source"]).read_text(encoding="utf-8")
    prose, toc = article_body(article, markdown)
    toc_html = "\n".join(f'<a href="#{a}">{html.escape(t)}</a>' for a, t in toc)
    aside = f'<aside class="toc" aria-label="Neste artigo"><strong>Neste artigo</strong>{toc_html}</aside>' if toc else ""
    body = f'''<main id="conteudo" class="article-shell">
  <header class="article-header">
    <a class="eyebrow category-link" href="../categories/{slugify(article["category"])}.html">{html.escape(article["category"])} · {html.escape(article.get("topic", "Games"))}</a>
    <h1>{html.escape(article["title"])}</h1>
    <p class="dek">{html.escape(article["dek"])}</p>
    <div class="meta"><span class="author"><img src="../assets/images/sagitta-tech.png" alt="">Luís Antônio Costa</span><span>{html.escape(article["date"])}</span><span>{html.escape(article["reading"])}</span></div>
  </header>
  <img class="cover" src="../{article["cover"]}" alt="{html.escape(article["cover_alt"])}">
  <div class="article-layout">
    <article class="prose">{prose}</article>
    {aside}
  </div>
</main>'''
    return page(article["title"], body, prefix="../", description=article["dek"], image=article["cover"], page_type="article")


def build_home():
    feature = article_card(ARTICLES[0], compact=False)
    recent = "\n".join(article_card(a) for a in ARTICLES[1:])
    body = f'''<main id="conteudo">
  <section class="container hero">
    <div><span class="eyebrow">Tecnologia · Games · Cultura</span><h1>Ideias que acertam o alvo.</h1><p class="hero-copy">Análises, opiniões e descobertas sobre os jogos e as tecnologias que merecem o seu tempo.</p></div>
    <aside class="hero-aside"><span class="label">Sobre o Sagitta Tech</span><p>Uma flecha certeira na direção do que há de mais interessante no mundo da tecnologia e dos games, por Luís Antônio Costa.</p></aside>
  </section>
  <section id="artigos" class="container section">
    <div class="section-head"><h2>Em destaque</h2><p>Tecnologia, reviews e opiniões com contexto, personalidade e sem perder tempo com o óbvio.</p></div>
    {feature}
    <div class="subsection-head"><h2>Mais artigos</h2><div class="category-pills"><a href="categories/momento-tech.html">Momento Tech</a><a href="categories/review.html">Review</a><a href="categories/opiniao.html">Opinião</a></div></div>
    <div class="article-grid">{recent}</div>
  </section>
</main>'''
    return page("Tecnologia e games", body, description="Sagitta Tech: análises, opiniões e descobertas sobre tecnologia e games.", image=ARTICLES[0]["cover"])


def build_category(category):
    selected = [a for a in ARTICLES if a["category"] == category]
    cards = "\n".join(article_card(a, prefix="../") for a in selected)
    body = f'''<main id="conteudo" class="container category-page">
  <header class="category-header"><span class="eyebrow">Categoria</span><h1>{html.escape(category)}</h1><p>{len(selected)} {'artigo' if len(selected) == 1 else 'artigos'} publicados.</p></header>
  <div class="article-grid">{cards}</div>
</main>'''
    return page(category, body, prefix="../", description=f"Artigos da categoria {category} no Sagitta Tech.")


def main():
    (ROOT / "articles").mkdir(exist_ok=True)
    (ROOT / "categories").mkdir(exist_ok=True)
    for article in ARTICLES:
        (ROOT / "articles" / f'{article["slug"]}.html').write_text(build_article(article), encoding="utf-8")
    categories = list(dict.fromkeys(article["category"] for article in ARTICLES))
    for category in categories:
        (ROOT / "categories" / f"{slugify(category)}.html").write_text(build_category(category), encoding="utf-8")
    (ROOT / "index.html").write_text(build_home(), encoding="utf-8")
    print(f"Built homepage, {len(ARTICLES)} articles, and {len(categories)} category pages")


if __name__ == "__main__":
    main()
