# VivaVoltia.com

Static site for [vivavoltia.com](https://vivavoltia.com), a US residential solar guide, hosted on GitHub Pages behind Cloudflare.

- Write articles in `_src/articles/`; static pages in `_src/pages/`.
- `_build/build.py` generates `articles/`, `guides/`, `index.html`, the static pages, `sitemap.xml` and `feed.xml`. The **Build site** GitHub Action runs it on every push and pings IndexNow.
- Images live in `images/articles/` (article photos), `images/og/` (share images) and `images/brand/`; WebP variants in `images/opt/` are generated.
- Full publishing guide (Spanish): [`_build/LEEME.md`](../_build/LEEME.md).
