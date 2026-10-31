# VivaVoltia.com

Static site for [vivavoltia.com](https://vivavoltia.com), a US residential solar guide, served by GitHub Pages behind Cloudflare.

| Folder | What it is |
|---|---|
| `content/` | Articles, static pages and the article template (what you edit) |
| `static/` | Copied as-is to the site root: images, `style.css`, `CNAME`, `ads.txt`, verification files |
| `tools/` | `build.py` (site generator), Pinterest and hero-image scripts |
| `branding/` | Brand assets that are not published |

Every push to `main` runs **Build and deploy site**: `tools/build.py` writes the full website to `_site/`, which is deployed to GitHub Pages, then changed URLs are sent to IndexNow. Generated HTML is never committed.

Publishing guide (Spanish): [`LEEME.md`](../LEEME.md).
