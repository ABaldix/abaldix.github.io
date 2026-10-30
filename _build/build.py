#!/usr/bin/env python3
"""
VivaVoltia static site builder.

Source files:
  _src/articles/<slug>.html   one article per file (front matter + HTML body)
  _src/pages/<name>.html      static pages (about, contact, privacy, terms, quote)

Generated (do not edit by hand, they are overwritten on every build):
  articles/<slug>.html, guides/<category>.html, index.html, the static pages,
  sitemap.xml

Run:  python3 _build/build.py
"""
import datetime as dt
import html
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src"
BASE = "https://vivavoltia.com"
SITE = "VivaVoltia"
ADSENSE = "ca-pub-8681391761083035"
GA = "G-1EFYE3P537"
CMP = "xmscxn1pEWkIXc"

CATEGORIES = {
    "panels": {
        "name": "Solar Panels",
        "slug": "solar-panels",
        "icon": "panel",
        "blurb": "Panel types, brands, sizing, lifespan, and how solar performs in real-world weather.",
    },
    "batteries": {
        "name": "Home Batteries",
        "slug": "home-batteries",
        "icon": "battery",
        "blurb": "Battery costs, backup power, off-grid sizing, and how storage changes your savings.",
    },
    "inverters": {
        "name": "Solar Inverters",
        "slug": "solar-inverters",
        "icon": "inverter",
        "blurb": "String inverters, microinverters, hybrids, and how to handle shade.",
    },
    "costs": {
        "name": "Costs & Incentives",
        "slug": "costs-and-incentives",
        "icon": "money",
        "blurb": "System prices, payback, financing, tax credits, state incentives, and net metering.",
    },
    "installation": {
        "name": "Installation & Maintenance",
        "slug": "installation-and-maintenance",
        "icon": "house",
        "blurb": "Roofs, HOAs, permits, insurance, cleaning, and what happens after installation.",
    },
}
CAT_ORDER = ["costs", "panels", "batteries", "inverters", "installation"]

# ---------------------------------------------------------------- helpers

def esc(s):
    return html.escape(str(s), quote=True)


def parse_source(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        raise SystemExit(f"{path}: missing front matter")
    meta, body = {}, m.group(2)
    for line in m.group(1).splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if key in ("takeaway", "source", "related"):
            meta.setdefault(key + "s", []).append(val)
        else:
            meta[key] = val
    return meta, body


def slugify(text):
    text = re.sub(r"<[^>]+>", "", text).lower()
    text = re.sub(r"&[a-z]+;", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:60].strip("-")


def add_heading_ids(body):
    toc, seen = [], set()

    def repl(m):
        attrs, inner = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        hid = idm.group(1) if idm else slugify(inner)
        while hid in seen:
            hid += "-2"
        seen.add(hid)
        toc.append((hid, re.sub(r"<[^>]+>", "", inner)))
        if idm:
            return m.group(0)
        return f'<h2{attrs} id="{hid}">{inner}</h2>'

    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, body, flags=re.S)
    return body, toc


def word_count(body):
    return len(re.sub(r"<[^>]+>", " ", body).split())


def fmt_date(d):
    return d.strftime("%B %-d, %Y")


def parse_date(s):
    return dt.date.fromisoformat(s)

# ---------------------------------------------------------------- icons

ICONS = {
    "panel": '<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="48" cy="14" r="7" fill="#F59E0B"/><g stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round"><path d="M48 2v3M48 23v3M36 14h3M57 14h3M39.5 5.5l2 2M54.5 20.5l2 2M56.5 5.5l-2 2"/></g><path d="M8 50l8-24h32l-8 24z" fill="#065F46"/><path d="M16 26l-8 24M24.5 26l-5 24M33 26l-2.5 24M41.5 26l0 0M12.5 38h31.5M10 44.5h31" stroke="#A7F3D0" stroke-width="1.6"/><path d="M28 50v8M20 58h16" stroke="#374151" stroke-width="3" stroke-linecap="round"/></svg>',
    "battery": '<svg viewBox="0 0 64 64" aria-hidden="true"><rect x="16" y="10" width="32" height="48" rx="6" fill="#065F46"/><rect x="26" y="5" width="12" height="6" rx="2" fill="#374151"/><rect x="21" y="40" width="22" height="12" rx="2" fill="#34D399"/><rect x="21" y="26" width="22" height="11" rx="2" fill="#34D399"/><rect x="21" y="15" width="22" height="8" rx="2" fill="#A7F3D0" opacity=".5"/><path d="M34 27l-6 9h5l-3 8 8-11h-5l3-6z" fill="#FBBF24"/></svg>',
    "inverter": '<svg viewBox="0 0 64 64" aria-hidden="true"><rect x="10" y="8" width="44" height="48" rx="6" fill="#065F46"/><rect x="17" y="15" width="30" height="16" rx="3" fill="#ECFDF5"/><path d="M20 23h7M37 19c2.5 0 2.5 8 5 8" stroke="#059669" stroke-width="2" fill="none" stroke-linecap="round"/><path d="M30 23c1.5-5 3-5 4.5 0" stroke="#059669" stroke-width="2" fill="none"/><circle cx="22" cy="43" r="4" fill="#34D399"/><circle cx="34" cy="43" r="4" fill="#FBBF24"/><rect x="42" y="39" width="6" height="8" rx="1.5" fill="#A7F3D0"/></svg>',
    "money": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M8 54h48" stroke="#374151" stroke-width="3" stroke-linecap="round"/><rect x="12" y="38" width="8" height="16" rx="2" fill="#A7F3D0"/><rect x="25" y="30" width="8" height="24" rx="2" fill="#34D399"/><rect x="38" y="20" width="8" height="34" rx="2" fill="#059669"/><path d="M10 30L24 20l10 6 18-16" stroke="#F59E0B" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M46 10h6v6" stroke="#F59E0B" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "house": '<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M6 32L32 10l26 22" stroke="#374151" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M13 28v26h38V28" fill="#ECFDF5"/><path d="M13 28v26h38V28" stroke="#374151" stroke-width="3" fill="none"/><path d="M19 27l13-11 13 11z" fill="#065F46"/><path d="M24 23.5h16M21.5 25.5h21" stroke="#A7F3D0" stroke-width="1.2"/><rect x="27" y="40" width="10" height="14" rx="1.5" fill="#059669"/><rect x="40" y="36" width="7" height="7" rx="1" fill="#FBBF24"/></svg>',
}


def icon(name):
    return ICONS.get(name, ICONS["panel"])

# ---------------------------------------------------------------- layout

def head(title, description, canonical, prefix, og_type="website", image=None, extra=""):
    img = f"{BASE}/images/{image}" if image else f"{BASE}/images/panels-sun.jpg"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Consent banner (Usercentrics CMP) - must load first -->
    <script id="usercentrics-cmp" src="https://app.usercentrics.eu/browser-ui/latest/loader.js" data-settings-id="{CMP}" async></script>

    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GA}');
    </script>

    <!-- Google AdSense (Auto ads) -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE}" crossorigin="anonymous"></script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(description)}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:site_name" content="{SITE}">
    <meta property="og:type" content="{og_type}">
    <meta property="og:title" content="{esc(title)}">
    <meta property="og:description" content="{esc(description)}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{img}">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" type="image/png" href="/images/icono.png">
    <link rel="stylesheet" href="{prefix}style.css">
{extra}</head>
<body>
"""


def header(prefix):
    links = "\n".join(
        f'                <a href="{prefix}guides/{CATEGORIES[c]["slug"]}.html">{CATEGORIES[c]["name"].replace(" & Maintenance", "").replace("Home ", "")}</a>'
        for c in CAT_ORDER
    )
    return f"""    <header class="header">
        <div class="container navbar">
            <div class="logo"><a href="/">VivaVoltia</a></div>
            <nav class="nav-links" aria-label="Main">
{links}
            </nav>
            <a href="{prefix}quote.html" class="btn-cta-header">Solar Calculator</a>
        </div>
    </header>
"""


def footer(prefix):
    cats = "\n".join(
        f'                    <li><a href="{prefix}guides/{CATEGORIES[c]["slug"]}.html">{CATEGORIES[c]["name"]}</a></li>'
        for c in CAT_ORDER
    )
    return f"""    <footer class="footer">
        <div class="container footer-grid">
            <div class="footer-brand">
                <div class="logo footer-logo">VivaVoltia</div>
                <p>Independent, plain-English guides to residential solar energy for US homeowners.</p>
            </div>
            <div>
                <h4>Guides</h4>
                <ul>
{cats}
                    <li><a href="{prefix}articles/home-solar-guide.html">Complete Home Solar Guide</a></li>
                </ul>
            </div>
            <div>
                <h4>Company</h4>
                <ul>
                    <li><a href="{prefix}about.html">About Us</a></li>
                    <li><a href="{prefix}contact.html">Contact</a></li>
                    <li><a href="{prefix}privacy.html">Privacy Policy</a></li>
                    <li><a href="{prefix}terms.html">Terms &amp; Disclaimer</a></li>
                </ul>
            </div>
        </div>
        <div class="container footer-bottom">
            <p>© {dt.date.today().year} VivaVoltia.com · VivaVoltia is supported by advertising. Content is for general information only and is not financial, tax, or legal advice.</p>
        </div>
    </footer>
</body>
</html>
"""


def card(a, prefix, compact=False):
    cat = CATEGORIES[a["category"]]
    if a.get("image"):
        media = f'<div class="card-media" style="background-image:url(\'{prefix}images/{a["image"]}\')" role="img" aria-label="{esc(a.get("image_alt", a["title"]))}"></div>'
    else:
        media = f'<div class="card-media card-media--icon cat-{a["category"]}">{icon(cat["icon"])}</div>'
    return f"""            <a href="{prefix}articles/{a['slug']}.html" class="card">
                {media}
                <div class="card-body">
                    <span class="card-cat">{cat['name']}</span>
                    <h3>{esc(a['title'])}</h3>
                    <p>{esc(a['description'])}</p>
                    <span class="card-meta">{a['minutes']} min read</span>
                </div>
            </a>"""

# ---------------------------------------------------------------- articles

def load_articles():
    arts = []
    for p in sorted((SRC / "articles").glob("*.html")):
        meta, body = parse_source(p)
        meta["slug"] = p.stem
        for req in ("title", "description", "category", "published"):
            if req not in meta:
                raise SystemExit(f"{p}: missing '{req}'")
        if meta["category"] not in CATEGORIES:
            raise SystemExit(f"{p}: unknown category {meta['category']}")
        meta["published_d"] = parse_date(meta["published"])
        meta["updated_d"] = parse_date(meta.get("updated", meta["published"]))
        meta["body"] = body
        meta["minutes"] = max(3, math.ceil(word_count(body) / 230))
        meta["order"] = int(meta.get("order", 0))
        arts.append(meta)
    # newest first; within a day, higher "order" first
    arts.sort(key=lambda a: (a["published_d"], a["order"], a["title"]), reverse=True)
    return arts


def related_for(a, arts, n=3):
    by_slug = {x["slug"]: x for x in arts}
    picked = [by_slug[s] for s in a.get("relateds", []) if s in by_slug and s != a["slug"]]
    for x in arts:
        if len(picked) >= n:
            break
        if x["slug"] != a["slug"] and x["category"] == a["category"] and x not in picked:
            picked.append(x)
    for x in arts:
        if len(picked) >= n:
            break
        if x["slug"] != a["slug"] and x not in picked:
            picked.append(x)
    return picked[:n]


def render_article(a, arts):
    prefix = "../"
    cat = CATEGORIES[a["category"]]
    url = f"{BASE}/articles/{a['slug']}.html"
    body, toc = add_heading_ids(a["body"])

    takeaways = ""
    if a.get("takeaways"):
        items = "\n".join(f"                <li>{t}</li>" for t in a["takeaways"])
        takeaways = f"""            <aside class="takeaways">
                <h2 class="takeaways-title">Key Takeaways</h2>
                <ul>
{items}
                </ul>
            </aside>
"""
    toc_html = ""
    if len(toc) >= 4:
        items = "\n".join(f'                    <li><a href="#{h}">{esc(t)}</a></li>' for h, t in toc)
        toc_html = f"""            <nav class="toc" aria-label="Table of contents">
                <details open>
                    <summary>In this guide</summary>
                    <ol>
{items}
                    </ol>
                </details>
            </nav>
"""
    hero = ""
    if a.get("image"):
        hero = f"""        <figure class="article-hero">
            <img src="{prefix}images/{a['image']}" alt="{esc(a.get('image_alt', ''))}" width="1600" height="900" loading="eager">
        </figure>
"""
    sources = ""
    if a.get("sources"):
        lis = []
        for s in a["sources"]:
            title, _, link = s.partition("|")
            lis.append(f'                    <li><a href="{esc(link.strip())}" target="_blank" rel="noopener">{esc(title.strip())}</a></li>')
        sources = f"""            <section class="sources">
                <h2 class="sources-title">Sources</h2>
                <ul>
{chr(10).join(lis)}
                </ul>
            </section>
"""
    disclaimer = ""
    if a["category"] == "costs" or a.get("disclaimer") == "yes":
        disclaimer = """            <p class="disclaimer">This guide is general information, not financial, tax, or legal advice. Prices are national estimates and incentive rules change; confirm details for your situation with a licensed professional.</p>
"""
    rel = related_for(a, arts)
    rel_cards = "\n".join(card(x, prefix) for x in rel)

    updated_line = f'Updated <time datetime="{a["updated_d"].isoformat()}">{fmt_date(a["updated_d"])}</time>'
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": a["title"],
                "description": a["description"],
                "datePublished": a["published_d"].isoformat(),
                "dateModified": a["updated_d"].isoformat(),
                "author": {"@type": "Organization", "name": "VivaVoltia Editorial Team", "url": f"{BASE}/about.html"},
                "publisher": {"@type": "Organization", "name": SITE, "logo": {"@type": "ImageObject", "url": f"{BASE}/images/icono.png"}},
                "mainEntityOfPage": url,
                "image": f"{BASE}/images/{a.get('image', 'panels-sun.jpg')}",
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": cat["name"], "item": f"{BASE}/guides/{cat['slug']}.html"},
                    {"@type": "ListItem", "position": 3, "name": a["title"], "item": url},
                ],
            },
        ],
    }
    extra = f'    <meta property="article:published_time" content="{a["published_d"].isoformat()}">\n    <meta property="article:modified_time" content="{a["updated_d"].isoformat()}">\n    <script type="application/ld+json">{json.dumps(ld)}</script>\n'

    out = head(a.get("seo_title", a["title"]) + " | VivaVoltia", a["description"], url, prefix, "article", a.get("image"), extra)
    out += header(prefix)
    out += f"""
    <main class="article-wrap">
        <article class="article">
            <header class="article-header">
                <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span>›</span> <a href="{prefix}guides/{cat['slug']}.html">{cat['name']}</a></nav>
                <span class="eyebrow">{cat['name']}</span>
                <h1 class="article-title">{esc(a['title'])}</h1>
                <p class="article-dek">{esc(a['description'])}</p>
                <div class="byline">
                    <span class="byline-avatar">{icon('panel')}</span>
                    <div>
                        <strong>VivaVoltia Editorial Team</strong>
                        <span>{updated_line} · {a['minutes']} min read</span>
                    </div>
                </div>
            </header>
{hero}
            <div class="article-content">
{takeaways}{toc_html}
{body}
{sources}{disclaimer}            </div>
        </article>

        <aside class="cta-box">
            <div>
                <h2>Estimate your own numbers</h2>
                <p>Use our free calculator to estimate system size, upfront cost, and payback for your home with 2026 prices.</p>
            </div>
            <a href="{prefix}quote.html" class="btn-cta-main">Open the Solar Calculator</a>
        </aside>

        <div class="author-box">
            <span class="author-img">{icon('panel')}</span>
            <div class="author-info">
                <h4>About VivaVoltia</h4>
                <p>VivaVoltia publishes independent guides for US homeowners considering solar panels and home batteries. We base our articles on public sources such as the IRS, the U.S. Department of Energy, NREL, the EIA, and manufacturer specifications, and we update them when rules change. <a href="{prefix}about.html">How we research our guides</a>.</p>
            </div>
        </div>
    </main>

    <section class="container related">
        <h2 class="section-title">Related Guides</h2>
        <div class="card-grid">
{rel_cards}
        </div>
    </section>
"""
    out += footer(prefix)
    return out

# ---------------------------------------------------------------- category pages

def render_category(ckey, arts):
    prefix = "../"
    cat = CATEGORIES[ckey]
    url = f"{BASE}/guides/{cat['slug']}.html"
    items = [a for a in arts if a["category"] == ckey]
    cards = "\n".join(card(a, prefix) for a in items)
    out = head(f"{cat['name']} Guides | VivaVoltia", f"{cat['blurb']} Independent guides for US homeowners.", url, prefix)
    out += header(prefix)
    out += f"""
    <main class="container">
        <section class="page-hero">
            <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span>›</span> {cat['name']}</nav>
            <div class="page-hero-icon cat-{ckey}">{icon(cat['icon'])}</div>
            <h1>{cat['name']}</h1>
            <p>{cat['blurb']}</p>
            <p class="page-hero-count">{len(items)} guides · Start with our <a href="{prefix}articles/home-solar-guide.html">complete home solar guide</a> if you are new to solar.</p>
        </section>
        <div class="card-grid">
{cards}
        </div>
    </main>
"""
    out += footer(prefix)
    return out

# ---------------------------------------------------------------- homepage

def render_index(arts):
    prefix = ""
    featured = next((a for a in arts if a.get("featured") == "yes"), arts[0])
    latest = [a for a in arts if a is not featured][:6]
    latest_cards = "\n".join(card(a, prefix) for a in latest)

    silos = "\n".join(
        f"""            <a href="guides/{CATEGORIES[c]['slug']}.html" class="silo-card">
                <div class="silo-icon cat-{c}">{icon(CATEGORIES[c]['icon'])}</div>
                <h3>{CATEGORIES[c]['name']}</h3>
                <p>{CATEGORIES[c]['blurb']}</p>
                <span class="silo-count">{sum(1 for a in arts if a['category'] == c)} guides →</span>
            </a>"""
        for c in CAT_ORDER
    )

    groups = []
    for c in CAT_ORDER:
        lis = "\n".join(
            f'                <li><a href="articles/{a["slug"]}.html">{esc(a["title"])}</a></li>'
            for a in arts if a["category"] == c
        )
        groups.append(f"""            <div class="guides-group">
                <h3><a href="guides/{CATEGORIES[c]['slug']}.html">{CATEGORIES[c]['name']}</a></h3>
                <ul>
{lis}
                </ul>
            </div>""")

    fimg = (f'<div class="featured-media" style="background-image:url(\'images/{featured["image"]}\')" role="img" aria-label="{esc(featured.get("image_alt", ""))}"></div>'
            if featured.get("image") else f'<div class="featured-media card-media--icon cat-{featured["category"]}">{icon(CATEGORIES[featured["category"]]["icon"])}</div>')

    ld = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": f"{BASE}/"}
    out = head("VivaVoltia | Independent Guides to Home Solar in the US",
               "Independent, plain-English guides to residential solar in the US: panel and battery costs, payback, 2026 incentive rules, net metering, and installation.",
               f"{BASE}/", prefix, extra=f'    <script type="application/ld+json">{json.dumps(ld)}</script>\n')
    out += header(prefix)
    out += f"""
    <section class="home-hero">
        <div class="container home-hero-inner">
            <div>
                <span class="eyebrow">Updated for 2026 rules</span>
                <h1>Independent Guides to Home Solar in the US</h1>
                <p>Clear, sourced answers on solar panels, batteries, costs, and incentives, so you can compare options with confidence before you talk to an installer.</p>
                <div class="hero-actions">
                    <a href="articles/home-solar-guide.html" class="btn-cta-main">Start with the Complete Guide</a>
                    <a href="quote.html" class="btn-secondary">Estimate Your Savings</a>
                </div>
            </div>
            <ul class="hero-points">
                <li><strong>{len(arts)}</strong> in-depth guides</li>
                <li><strong>No sales pitch</strong> We don't sell or install solar</li>
                <li><strong>Sourced</strong> IRS, DOE, NREL, EIA data</li>
            </ul>
        </div>
    </section>

    <main class="container">
        <a href="articles/{featured['slug']}.html" class="featured">
            {fimg}
            <div class="featured-body">
                <span class="eyebrow">Featured guide</span>
                <h2>{esc(featured['title'])}</h2>
                <p>{esc(featured['description'])}</p>
                <span class="read-more">Read the guide →</span>
            </div>
        </a>

        <section class="home-section" id="latest">
            <div class="section-head">
                <h2 class="section-title">Latest Guides</h2>
                <a href="#guides">View all guides →</a>
            </div>
            <div class="card-grid">
{latest_cards}
            </div>
        </section>

        <section class="home-section">
            <h2 class="section-title">Explore by Topic</h2>
            <div class="silo-grid">
{silos}
            </div>
        </section>

        <section class="home-section tool-band">
            <div>
                <h2>How much would solar save you?</h2>
                <p>Our free calculator estimates system size, upfront cost, and payback using 2026 prices and your own electricity rate. Nothing you enter leaves your browser.</p>
            </div>
            <a href="quote.html" class="btn-cta-main">Open the Solar Calculator</a>
        </section>

        <section class="home-section" id="guides">
            <h2 class="section-title">All Solar Guides</h2>
            <div class="guides-index">
{chr(10).join(groups)}
            </div>
        </section>
    </main>
"""
    out += footer(prefix)
    return out

# ---------------------------------------------------------------- static pages

def render_page(path):
    meta, body = parse_source(path)
    name = path.stem
    url = f"{BASE}/{name}.html"
    out = head(meta["title"], meta["description"], url, "", extra=meta.get("head", "").replace("\\n", "\n"))
    out += header("")
    out += body
    out += footer("")
    return out

# ---------------------------------------------------------------- sitemap

def render_sitemap(arts, pages):
    today = max(a["updated_d"] for a in arts).isoformat()
    rows = [(f"{BASE}/", today, "1.0")]
    for c in CAT_ORDER:
        rows.append((f"{BASE}/guides/{CATEGORIES[c]['slug']}.html", today, "0.7"))
    for a in arts:
        rows.append((f"{BASE}/articles/{a['slug']}.html", a["updated_d"].isoformat(), "0.8"))
    for p in pages:
        rows.append((f"{BASE}/{p}.html", today, "0.8" if p == "quote" else "0.3"))
    body = "\n".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{d}</lastmod>\n    <priority>{pr}</priority>\n  </url>" for u, d, pr in rows)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'

# ---------------------------------------------------------------- main

def main():
    arts = load_articles()
    slugs = {a["slug"] for a in arts}
    # internal link check
    problems = []
    for a in arts:
        for m in re.finditer(r'href="([a-z0-9-]+)\.html"', a["body"]):
            if m.group(1) not in slugs:
                problems.append(f"{a['slug']}: link to missing article {m.group(1)}.html")
    if problems:
        print("\n".join(problems))
        sys.exit(1)

    (ROOT / "articles").mkdir(exist_ok=True)
    (ROOT / "guides").mkdir(exist_ok=True)
    # remove generated articles whose source was deleted
    for old in (ROOT / "articles").glob("*.html"):
        if old.stem not in slugs:
            old.unlink()
    for a in arts:
        (ROOT / "articles" / f"{a['slug']}.html").write_text(render_article(a, arts), encoding="utf-8")
    for c in CAT_ORDER:
        (ROOT / "guides" / f"{CATEGORIES[c]['slug']}.html").write_text(render_category(c, arts), encoding="utf-8")
    (ROOT / "index.html").write_text(render_index(arts), encoding="utf-8")
    pages = []
    for p in sorted((SRC / "pages").glob("*.html")):
        (ROOT / f"{p.stem}.html").write_text(render_page(p), encoding="utf-8")
        pages.append(p.stem)
    (ROOT / "sitemap.xml").write_text(render_sitemap(arts, pages), encoding="utf-8")
    print(f"Built {len(arts)} articles, {len(CAT_ORDER)} category pages, {len(pages)} pages.")


if __name__ == "__main__":
    main()
