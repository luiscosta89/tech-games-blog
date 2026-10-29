# Sagitta Tech — GitHub Pages template

Template estático, responsivo e sem dependências de build para um blog de tecnologia e games. A primeira publicação adapta, com autorização do autor, o artigo do Medium **“OPINIÃO | 10 jogos de 2026 que você deveria jogar”**.

## Estrutura

- `index.html` — capa do blog
- `articles/10-jogos-2026.html` — artigo completo
- `assets/style.css` — tema editorial escuro
- `assets/site.js` — vídeos sob demanda e sumário ativo
- `_source/10-jogos-2026.md` — texto-fonte importado do Medium
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
