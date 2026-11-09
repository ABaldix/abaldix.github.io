// Renders data-card hero images (1600x900) for state guides and comparisons.
// Usage: node tools/graphics/render_heroes.js   (needs Playwright + Chromium)
const { chromium } = require('playwright');
const path = require('path');
const OUT = path.join(__dirname, '..', '..', 'static', 'images', 'articles');

const STATES = [
  ['state-california', 'California', '29.8¢', '5.8', 'NEM 3.0 net billing', 'Batteries now drive the savings'],
  ['state-texas', 'Texas', '15.9¢', '5.3', 'Buyback plans', 'Your retail plan decides the payback'],
  ['state-florida', 'Florida', '15.0¢', '5.2', 'Full retail net metering', 'No sales or property tax on solar'],
  ['state-arizona', 'Arizona', '15.1¢', '6.3', 'Net billing (~6¢ exports)', 'The best sun in the country'],
  ['state-new-york', 'New York', '28.6¢', '3.9', 'Net metering + CBC charge', '25% state tax credit up to $5,000'],
  ['state-new-jersey', 'New Jersey', '24.6¢', '4.3', 'Full retail net metering', 'SREC-II payments for 15 years'],
  ['state-massachusetts', 'Massachusetts', '30.5¢', '4.1', 'Full retail net metering', 'SMART 3.0 pays per kWh for 20 years'],
  ['state-north-carolina', 'North Carolina', '14.9¢', '4.8', 'Duke Bridge Rate or TOU', 'PowerPair: up to $9,000 with a battery'],
  ['state-colorado', 'Colorado', '17.2¢', '5.4', 'Net metering (Xcel)', 'High-altitude sun, plan for hail'],
  ['state-illinois', 'Illinois', '19.3¢', '4.2', 'Supply-only net metering', 'Illinois Shines + $300/kW rebate'],
  ['state-nevada', 'Nevada', '12.7¢', '6.1', '75% net metering (NV Energy)', 'Desert sun, credit locked for 20 years'],
  ['state-georgia', 'Georgia', '15.9¢', '4.9', 'Instantaneous netting buyback', 'Size for self-use to make it pay'],
  ['state-pennsylvania', 'Pennsylvania', '21.8¢', '4.0', '1:1 retail net metering', 'High prices + SREC income'],
  ['state-maryland', 'Maryland', '21.4¢', '4.4', 'Full retail net metering', 'Net metering + SREC income'],
  ['state-south-carolina', 'South Carolina', '15.8¢', '4.9', 'Solar Choice (Duke, Dominion)', '25% state tax credit still active'],
  ['state-utah', 'Utah', '13.3¢', '5.5', 'Net billing (~4–6¢ exports)', 'Great sun, cheap power: size for self-use'],
  ['state-michigan', 'Michigan', '23.0¢', '3.9', 'Inflow/outflow billing', 'High prices offset modest sun'],
  ['state-connecticut', 'Connecticut', '24.5¢', '4.0', 'RRES Netting or Buy-All', 'Buy-All pays ~32.9¢ for 20 years'],
  ['state-hawaii', 'Hawaii', '47.2¢', '5.6', 'Smart DER export credits', '35% state tax credit up to $5,000'],
  ['state-ohio', 'Ohio', '19.4¢', '4.0', 'Monthly net metering', 'Regulators kept net metering in 2026'],
  ['state-washington', 'Washington', '14.6¢', '3.6', '1:1 net metering', 'No sales tax on solar through 2029'],
  ['state-indiana', 'Indiana', '17.0¢', '4.2', 'EDG net billing', 'Exports ~4–5.5¢ per kWh'],
  ['state-tennessee', 'Tennessee', '13.4¢', '4.6', 'No net metering (TVA)', 'Exports ~4¢ per kWh'],
  ['state-kentucky', 'Kentucky', '13.8¢', '4.3', 'Net metering, reduced exports', 'LG&E ~7.1¢ · KU ~7.5¢'],
  ['state-louisiana', 'Louisiana', '12.9¢', '4.9', 'Avoided-cost exports', '~2.8¢ per kWh outside New Orleans'],
  ['state-oklahoma', 'Oklahoma', '14.8¢', '5.2', 'Monthly net metering', 'Monthly surplus earns wholesale prices'],
  ['state-iowa', 'Iowa', '17.1¢', '4.3', 'Inflow-outflow at retail', 'Credit locked 20 years before 2027'],
  ['state-alabama', 'Alabama', '16.3¢', '4.8', 'No net metering', 'Alabama Power fee: $5.41/kW a month'],
  ['state-idaho', 'Idaho', '13.4¢', '4.8', 'Net billing (Idaho Power)', 'Exports ~3¢, or ~15.7¢ on summer peak'],
  ['state-arkansas', 'Arkansas', '14.4¢', '4.7', 'Net billing (Act 278)', 'Entergy exports ~3.3¢ per kWh'],
  ['state-minnesota', 'Minnesota', '17.2¢', '4.3', 'Retail-rate net metering', 'Every utility must offer it'],
  ['state-new-mexico', 'New Mexico', '16.5¢', '6.2', 'Net metering (PNM, EPE, Xcel)', '10% state tax credit up to $6,000'],
  ['state-wisconsin', 'Wisconsin', '19.4¢', '4.1', 'Monthly net metering', 'Focus on Energy rebate up to $2,400'],
  ['state-missouri', 'Missouri', '16.0¢', '4.6', 'Monthly net metering', 'Evergy vs Ameren credits differ'],
  ['state-oregon', 'Oregon', '15.9¢', '4.2', '1:1 net metering (PGE, Pacific)', 'Cash rebates still available'],
  ['state-virginia', 'Virginia', '17.6¢', '4.6', 'Annual net metering (NEM 2.0)', 'Regulators kept net metering in 2026'],
];
const VS = [
  ['vs-enphase-powerwall', 'Battery comparison', ['Enphase IQ Battery 5P', [['5.0 kWh', 'per unit'], ['3.84 kW', 'continuous'], ['15 yr', 'warranty']]],
    ['Tesla Powerwall 3', [['13.5 kWh', 'capacity'], ['11.5 kW', 'continuous'], ['10 yr', 'warranty']]]],
  ['vs-powerwall-franklin', 'Whole-home battery comparison', ['Tesla Powerwall 3', [['13.5 kWh', 'capacity'], ['11.5 kW', 'continuous'], ['10 yr', 'warranty']]],
    ['FranklinWH aPower 2', [['15 kWh', 'capacity'], ['10 kW', 'continuous'], ['15 yr', 'warranty']]]],
  ['vs-rec-qcells', 'Solar panel comparison', ['REC Alpha Pure-RX', [['470 W', 'max power'], ['22.6%', 'efficiency'], ['−0.24%/°C', 'heat loss']]],
    ['Qcells Q.TRON BLK M-G2+', [['440 W', 'max power'], ['22.5%', 'efficiency'], ['−0.30%/°C', 'heat loss']]]],
];
const e = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const sun = `<svg viewBox="0 0 24 24" width="64" height="64" fill="none" stroke="#F59E0B" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg>`;
const css = `
*{box-sizing:border-box;margin:0}
body{font-family:system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif}
.card{width:1600px;height:900px;position:relative;overflow:hidden;background:linear-gradient(135deg,#064E3B 0%,#047857 55%,#059669 100%);color:#fff;padding:104px 96px}
.card:after{content:"";position:absolute;right:-220px;top:-220px;width:760px;height:760px;border-radius:50%;background:radial-gradient(circle,rgba(245,158,11,.35),rgba(245,158,11,0) 65%)}
.eyebrow{display:flex;align-items:center;gap:18px;font-size:30px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#D1FAE5}
h1{font-size:92px;line-height:1.02;font-weight:800;margin:26px 0 16px;letter-spacing:-.02em;max-width:1300px}
.sub{font-size:38px;color:#ECFDF5;max-width:1200px}
.stats{position:absolute;left:96px;right:96px;bottom:138px;display:grid;grid-template-columns:1fr 1fr 1.5fr;gap:28px;z-index:2}
.stat{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);border-radius:22px;padding:28px 32px}
.stat b{display:block;font-size:60px;font-weight:800;line-height:1.05}
.stat.wide b{font-size:42px;line-height:1.2;padding-top:10px}
.stat span{display:block;font-size:26px;color:#D1FAE5;margin-top:8px}
.foot{position:absolute;left:96px;right:96px;bottom:68px;display:flex;justify-content:space-between;font-size:26px;color:#A7F3D0;z-index:2}
.foot b{color:#fff}
.vs{display:grid;grid-template-columns:1fr 120px 1fr;align-items:stretch;margin-top:40px;position:relative;z-index:2}
.col{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);border-radius:26px;padding:32px 44px}
.col h2{font-size:52px;line-height:1.1;font-weight:800;margin-bottom:28px;min-height:116px}
.row{display:flex;align-items:baseline;justify-content:space-between;border-top:1px solid rgba(255,255,255,.2);padding:16px 0}
.row b{font-size:50px;font-weight:800}
.row span{font-size:28px;color:#D1FAE5}
.mid{display:flex;align-items:center;justify-content:center;font-size:54px;font-weight:800;color:#FCD34D}
`;
function stateCard([id, name, price, sunh, policy, sub]) {
  return `<div class="card" id="${id}">
  <div class="eyebrow">${sun}<span>2026 state solar guide</span></div>
  <h1>Is solar worth it in ${e(name)}?</h1>
  <p class="sub">${e(sub)}</p>
  <div class="stats">
    <div class="stat"><b>${price}</b><span>avg. price per kWh</span></div>
    <div class="stat"><b>${sunh}</b><span>peak sun hours a day</span></div>
    <div class="stat wide"><b>${e(policy)}</b><span>how exports are credited</span></div>
  </div>
  <div class="foot"><span>Prices: EIA, Aug 2026 · Sun: NREL</span><b>vivavoltia.com</b></div>
</div>`;
}
function vsCard([id, eyebrow, a, b]) {
  const col = ([n, rows]) => `<div class="col"><h2>${e(n)}</h2>${rows.map(([v, l]) => `<div class="row"><b>${e(v)}</b><span>${e(l)}</span></div>`).join('')}</div>`;
  return `<div class="card" id="${id}" style="padding-top:92px">
  <div class="eyebrow">${sun}<span>${e(eyebrow)} · 2026</span></div>
  <div class="vs">${col(a)}<div class="mid">VS</div>${col(b)}</div>
  <div class="foot"><span>Manufacturer specifications</span><b>vivavoltia.com</b></div>
</div>`;
}
(async () => {
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${STATES.map(stateCard).join('')}${VS.map(vsCard).join('')}</body></html>`;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  await page.setContent(html);
  for (const id of [...STATES.map(s => s[0]), ...VS.map(v => v[0])]) {
    await (await page.$('#' + id)).screenshot({ path: path.join(OUT, id + '.jpg'), type: 'jpeg', quality: 86 });
  }
  await browser.close();
  console.log('rendered', STATES.length + VS.length);
})();
