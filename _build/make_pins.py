#!/usr/bin/env python3
"""Generate Pinterest pin images (1000x1500) for every article.

Usage (needs Playwright + Chromium, run locally):
    python3 _build/make_pins.py        -> writes /tmp/pins.html and /tmp/pins.json
    node _build/render_pins.js         -> renders images/pins/<slug>-a.jpg and -b.jpg
"""
import html, json, importlib.util, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("b", ROOT / "_build" / "build.py")
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
sys.path.insert(0, str(ROOT / "_build"))
from pins_data import PINS

GRAD = {"panels": "#ECFDF5,#FEF3C7", "batteries": "#D1FAE5,#ECFEFF", "inverters": "#F0FDF4,#E0F2FE",
        "costs": "#FFFBEB,#ECFDF5", "installation": "#F5F5F4,#ECFDF5"}
DARK = {"panels": "#064E3B", "batteries": "#0F3D3E", "inverters": "#0B3B4A", "costs": "#14352A", "installation": "#1F2937"}

e = html.escape
arts = b.load_articles()
missing = [a["slug"] for a in arts if a["slug"] not in PINS]
if missing:
    raise SystemExit(f"Missing pin copy for: {missing}")

blocks, keys = [], []
for a in arts:
    hA, sA, hB, sB, _, _ = PINS[a["slug"]]
    cat = b.CATEGORIES[a["category"]]
    ic = b.icon(cat["icon"])
    if a.get("image"):
        media = f'<div class="media" style="background-image:url(\'file://{ROOT}/images/{a["image"]}\')"></div>'
    else:
        media = f'<div class="media iconmedia" style="background:linear-gradient(135deg,{GRAD[a["category"]]})"><div class="bigicon">{ic}</div></div>'
    blocks.append(f'''
<div class="pin pinA" id="{a["slug"]}-a">
  {media}
  <div class="panel">
    <div class="eyebrow">{e(cat["name"])} · 2026 Guide</div>
    <h1>{e(hA)}</h1>
    <p>{e(sA)}</p>
    <div class="cta">Read the free guide →</div>
  </div>
  <div class="bar"><span class="logo">VivaVoltia</span><span>vivavoltia.com</span></div>
</div>
<div class="pin pinB" id="{a["slug"]}-b" style="background:{DARK[a["category"]]}">
  <div class="topline"><span class="chip">{e(cat["name"])}</span></div>
  <div class="bmid">
    <div class="smallicon">{ic}</div>
    <h1>{e(hB)}</h1>
    <p>{e(sB)}</p>
  </div>
  <div class="bcta">Free 2026 guide at <b>vivavoltia.com</b></div>
</div>''')
    keys += [f"{a['slug']}-a", f"{a['slug']}-b"]

css = """
body{margin:0;font-family:system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif}
.pin{width:1000px;height:1500px;position:relative;overflow:hidden;box-sizing:border-box}
.pinA{background:#fff;display:flex;flex-direction:column}
.media{height:760px;background-size:cover;background-position:center;flex-shrink:0}
.iconmedia{display:flex;align-items:center;justify-content:center}
.bigicon{width:380px;height:380px;background:#fff;border-radius:60px;padding:55px;box-sizing:border-box;box-shadow:0 30px 60px rgba(0,0,0,.12)}
.panel{flex:1;padding:56px 70px 0}
.eyebrow{font-size:30px;font-weight:800;letter-spacing:3px;text-transform:uppercase;color:#047857}
.pinA h1{font-size:86px;line-height:1.04;letter-spacing:-2.5px;color:#0F172A;margin:22px 0 22px;font-weight:850}
.pinA p{font-size:40px;line-height:1.3;color:#374151;margin:0}
.cta{display:inline-block;margin-top:36px;background:#F59E0B;color:#111827;font-weight:800;font-size:36px;padding:20px 34px;border-radius:18px}
.bar{height:110px;background:#047857;color:#ECFDF5;display:flex;align-items:center;justify-content:space-between;padding:0 70px;font-size:34px;font-weight:600}
.logo{font-weight:900;font-size:44px;color:#fff;letter-spacing:-1px}
.pinB{color:#fff;display:flex;flex-direction:column;padding:80px 80px 70px}
.topline{display:flex}
.chip{background:rgba(255,255,255,.14);border:2px solid rgba(255,255,255,.35);border-radius:999px;padding:14px 30px;font-size:30px;font-weight:700;letter-spacing:2px;text-transform:uppercase}
.bmid{flex:1;display:flex;flex-direction:column;justify-content:center}
.smallicon{width:190px;height:190px;background:#fff;border-radius:40px;padding:30px;box-sizing:border-box;margin-bottom:56px}
.pinB h1{font-size:118px;line-height:1.0;letter-spacing:-3.5px;margin:0 0 36px;font-weight:900;color:#fff}
.pinB p{font-size:48px;line-height:1.28;color:#FDE68A;margin:0;font-weight:600}
.bcta{font-size:38px;color:#D1FAE5;border-top:3px solid rgba(255,255,255,.25);padding-top:36px}
.bcta b{color:#fff}
svg{width:100%;height:100%;display:block}
"""
pathlib.Path("/tmp/pins.html").write_text(f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(blocks)}</body></html>")
pathlib.Path("/tmp/pins.json").write_text(json.dumps({"keys": keys, "out": str(ROOT / "images" / "pins")}))
print(len(keys), "pins prepared")
