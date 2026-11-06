// Renders a story-style TikTok (1080x1920, 30 fps) from a JSON script.
// Usage: node make_tiktok.js script.json out.mp4
// Each scene is drawn in Chromium, its frames are piped to ffmpeg (one mp4 per scene),
// then the scenes are joined with the concat demuxer.
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const W = 1080, H = 1920, FPS = 30;
const [, , scriptPath, outPath, onlyFrames] = process.argv;
const S = JSON.parse(fs.readFileSync(scriptPath, 'utf8'));
const ASSETS = path.resolve(path.dirname(scriptPath), S.assets || 'assets');
const tmp = path.resolve(path.dirname(outPath), '.parts-' + path.basename(outPath, '.mp4'));
fs.mkdirSync(tmp, { recursive: true });

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
// *word* -> highlighted word
const fmt = s => esc(s).replace(/\*([^*]+)\*/g, '<em>$1</em>');

const CSS = `
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:${W}px;height:${H}px;overflow:hidden;background:#0B1220;font-family:Inter,'Inter Display',sans-serif}
.bg{position:absolute;inset:-40px;background-size:cover;background-position:center;animation:zoom var(--d) linear forwards}
.bg.blur{filter:blur(18px) brightness(.55);inset:-80px}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,12,24,.6) 0%,rgba(6,12,24,.62) 30%,rgba(6,12,24,.78) 60%,rgba(6,12,24,.92) 100%)}
.solid{position:absolute;inset:0}
@keyframes zoom{from{transform:scale(1)}to{transform:scale(1.08)}}
.top{position:absolute;top:120px;left:80px;right:80px;display:flex;justify-content:space-between;align-items:center}
.brand{font-weight:900;font-size:40px;color:#fff;letter-spacing:-1px}
.brand b{color:#34D399}
.chip{font-weight:800;font-size:28px;letter-spacing:2px;text-transform:uppercase;color:#0B1220;background:#FBBF24;padding:12px 22px;border-radius:12px}
.prog{position:absolute;top:80px;left:80px;right:80px;display:flex;gap:8px}
.prog i{flex:1;height:8px;border-radius:4px;background:rgba(255,255,255,.28)}
.prog i.on{background:#fff}
.box{position:absolute;left:80px;right:140px;top:50%;transform:translateY(-50%)}
.kicker{font-size:52px;font-weight:700;color:#FBBF24;margin-bottom:28px;opacity:0;animation:pop .45s ease-out forwards}
.line{font-size:96px;line-height:1.05;font-weight:900;color:#fff;letter-spacing:-2.5px;opacity:0;animation:pop .5s cubic-bezier(.2,.9,.3,1.3) forwards;text-shadow:0 6px 30px rgba(0,0,0,.45)}
.line + .line{margin-top:18px}
.line.small{font-size:58px;line-height:1.2;font-weight:700;letter-spacing:-1px;color:#E5E7EB}
em{font-style:normal;color:#FBBF24}
em.g{color:#34D399}
@keyframes pop{from{opacity:0;transform:translateY(40px) scale(.96)}to{opacity:1;transform:none}}
.item{display:flex;gap:30px;align-items:center;background:rgba(255,255,255,.12);border:2px solid rgba(255,255,255,.22);border-radius:30px;padding:30px 34px;margin-top:26px;opacity:0;animation:pop .5s cubic-bezier(.2,.9,.3,1.3) forwards;backdrop-filter:blur(6px)}
.num{flex:none;width:88px;height:88px;border-radius:24px;background:#FBBF24;color:#0B1220;font-weight:900;font-size:52px;display:flex;align-items:center;justify-content:center}
.item span{font-size:52px;font-weight:800;color:#fff;line-height:1.12;letter-spacing:-1px}
.cta{position:absolute;left:80px;right:140px;top:50%;transform:translateY(-50%);text-align:left}
.url{display:inline-block;margin-top:40px;background:#fff;color:#065F46;font-weight:900;font-size:76px;letter-spacing:-2px;padding:26px 40px;border-radius:28px;opacity:0;animation:pop .5s cubic-bezier(.2,.9,.3,1.3) forwards;box-shadow:0 20px 50px rgba(0,0,0,.35)}
.bio{margin-top:34px;font-size:50px;font-weight:800;color:#FBBF24;opacity:0;animation:pop .45s ease-out forwards}
.flash{position:absolute;inset:0;background:#fff;opacity:0;animation:flash 1.2s linear .9s forwards;pointer-events:none}
@keyframes flash{0%{opacity:0}8%{opacity:.85}16%{opacity:0}26%{opacity:.6}34%{opacity:0}100%{opacity:0}}
.listshade{position:absolute;inset:0;background:rgba(6,12,24,.45)}
.wm{position:absolute;left:80px;bottom:450px;z-index:5;display:flex;align-items:center;gap:14px;background:rgba(255,255,255,.95);color:#065F46;font-weight:900;font-size:44px;letter-spacing:-1px;padding:16px 28px;border-radius:999px;box-shadow:0 10px 30px rgba(0,0,0,.3)}
.wm i{width:18px;height:18px;border-radius:50%;background:#F59E0B;display:block}
.fadein{position:absolute;inset:0;background:#000;animation:fade .3s linear forwards;pointer-events:none}
@keyframes fade{from{opacity:1}to{opacity:0}}
`;

function sceneHTML(sc, i, n) {
  const d = sc.dur;
  let bg = '';
  if (sc.bg) bg = `<div class="bg ${sc.blur ? 'blur' : ''}" style="background-image:url('file://${ASSETS}/${sc.bg}')"></div><div class="shade"></div>`;
  else bg = `<div class="solid" style="background:${sc.color || 'linear-gradient(160deg,#064E3B,#0B1220)'}"></div>`;
  const prog = `<div class="prog">${Array.from({ length: n }, (_, k) => `<i class="${k <= i ? 'on' : ''}"></i>`).join('')}</div>`;
  const top = `<div class="top"><div class="brand">Viva<b>Voltia</b></div>${sc.chip ? `<div class="chip">${esc(sc.chip)}</div>` : ''}</div>`;
  let body = '';
  let t = 0.25;
  const step = sc.step || 0.6;
  if (sc.type === 'list') {
    if (sc.bg) bg += '<div class="listshade"></div>';
    body = `<div class="box">${sc.kicker ? `<div class="kicker" style="animation-delay:${t}s">${fmt(sc.kicker)}</div>` : ''}` +
      (sc.lines || []).map(l => { const h = `<div class="line" style="animation-delay:${t}s">${fmt(l)}</div>`; t += step; return h; }).join('') +
      (t = sc.itemStart || t, '') + sc.items.map((it, k) => { const h = `<div class="item" style="animation-delay:${t}s"><div class="num">${k + 1}</div><span>${fmt(it)}</span></div>`; t += sc.itemStep || 0.9; return h; }).join('') + '</div>';
  } else if (sc.type === 'cta') {
    body = `<div class="cta">` + (sc.lines || []).map(l => { const h = `<div class="line ${l.startsWith('~') ? 'small' : ''}" style="animation-delay:${t}s">${fmt(l.replace(/^~/, ''))}</div>`; t += step; return h; }).join('') +
      `<div class="url" style="animation-delay:${t}s">${esc(sc.url || 'vivavoltia.com')}</div>` +
      `<div class="bio" style="animation-delay:${t + 0.5}s">${fmt(sc.bio || 'Link in bio → free guide')}</div></div>`;
  } else {
    body = `<div class="box">${sc.kicker ? `<div class="kicker" style="animation-delay:${t}s">${fmt(sc.kicker)}</div>` : ''}` +
      sc.lines.map(l => { if (sc.kicker && t === 0.25) t += 0.35; const small = l.startsWith('~'); const h = `<div class="line ${small ? 'small' : ''}" style="animation-delay:${t}s">${fmt(l.replace(/^~/, ''))}</div>`; t += step; return h; }).join('') + '</div>';
  }
  return `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head><body style="--d:${d}s">${bg}${prog}${top}${body}${sc.type === 'cta' ? '' : '<div class="wm"><i></i>vivavoltia.com</div>'}${sc.flash ? '<div class="flash"></div>' : ''}${i > 0 ? '<div class="fadein"></div>' : ''}</body></html>`;
}

function encodeScene(file, frames) {
  return spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', String(FPS), file], { stdio: ['pipe', 'inherit', 'inherit'] });
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  const parts = [];
  for (let i = 0; i < S.scenes.length; i++) {
    const sc = S.scenes[i];
    const html = path.join(tmp, `s${i}.html`);
    fs.writeFileSync(html, sceneHTML(sc, i, S.scenes.length));
    await page.goto('file://' + html);
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(() => new Promise(r => { const imgs = [...document.querySelectorAll('.bg')]; if (!imgs.length) return r(); const u = getComputedStyle(imgs[0]).backgroundImage.slice(5, -2); const im = new Image(); im.onload = im.onerror = r; im.src = u; }));
    const n = Math.round(sc.dur * FPS);
    const setT = t => page.evaluate(ms => document.getAnimations().forEach(a => { a.pause(); a.currentTime = ms; }), t);
    if (onlyFrames) { // preview stills only
      for (const f of [0.5, 0.85]) { await setT(sc.dur * f * 1000); await page.screenshot({ path: path.join(tmp, `preview-s${i}-${Math.round(f * 100)}.jpg`), type: 'jpeg', quality: 85 }); }
      continue;
    }
    const part = path.join(tmp, `s${i}.part.mp4`), final = path.join(tmp, `s${i}.mp4`);
    const ff = encodeScene(part, n);
    for (let f = 0; f < n; f++) {
      await setT((f / FPS) * 1000);
      const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end();
    const code = await new Promise(r => ff.on('close', r));
    if (code !== 0) throw new Error('ffmpeg failed on scene ' + i);
    fs.renameSync(part, final);
    parts.push(final);
    process.stdout.write(`scene ${i + 1}/${S.scenes.length} `);
  }
  await browser.close();
  if (onlyFrames) return console.log('previews in', tmp);
  const list = path.join(tmp, 'list.txt');
  fs.writeFileSync(list, parts.map(p => `file '${p}'`).join('\n'));
  // add a silent stereo track so every platform treats it as a normal video
  const joined = path.join(tmp, 'joined.mp4');
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', joined]);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', joined, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-shortest', '-movflags', '+faststart', outPath + '.tmp.mp4']);
  fs.renameSync(outPath + '.tmp.mp4', outPath);
  console.log('\nwrote', outPath);
})();
