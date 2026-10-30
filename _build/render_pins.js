// Renders the pins prepared by make_pins.py into JPG files.
const { chromium } = require('playwright');
const fs = require('fs');
const cfg = JSON.parse(fs.readFileSync('/tmp/pins.json', 'utf8'));
(async () => {
  fs.mkdirSync(cfg.out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1000, height: 1500 } });
  await page.goto('file:///tmp/pins.html');
  for (const k of cfg.keys) {
    const el = await page.$('#' + k);
    await el.screenshot({ path: `${cfg.out}/${k}.jpg`, type: 'jpeg', quality: 86 });
  }
  await browser.close();
  console.log('rendered', cfg.keys.length);
})();
