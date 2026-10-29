# Sagitta Tech — GitHub Pages template

Template estático, responsivo e sem dependências de build para um blog de tecnologia e games. O site organiza as publicações nas categorias **Review** e **Opinião**.

## Estrutura

- `index.html` — capa do blog
- `articles/` — artigos completos
- `categories/` — páginas de Review e Opinião
- `assets/style.css` — tema editorial escuro
- `assets/site.js` — vídeos sob demanda e sumário ativo
- `_source/` — textos-fonte dos artigos
- `scripts/build.py` — recompõe as páginas estáticas

## Visualização local

```bash
python3 -m http.server 8000
```

Abra `http://localhost:8000`.

## Publicação no GitHub Pages

1. Envie este diretório para um repositório público.
2. Em **Settings → Pages**, escolha **Deploy from a branch**.
3. Selecione `main` e `/ (root)`.

O projeto usa caminhos relativos e funciona em um site de projeto como `https://USUARIO.github.io/tech-games-blog/`.
