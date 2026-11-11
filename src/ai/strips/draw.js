// Draws the arc strips for the AI Evolution stage pages, in the hand of Dan Roam's codex page:
// thin pen line, simple symbols, lowercase lettering, one accent.
// For each stage in specs.json it writes ai/<slug>/arc.png and ai/<slug>/f1.png ... f6.png,
// plus a review sheet in the folder named by SHEETS (optional).
const rough = require('roughjs/bundled/rough.cjs.js');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '../../..');
const specs = JSON.parse(fs.readFileSync(path.join(__dirname, 'specs.json'), 'utf8'));
const font = fs.readFileSync(path.join(__dirname, 'node_modules/@fontsource/patrick-hand/files/patrick-hand-latin-400-normal.woff2')).toString('base64');
const INK = '#1a1a1a', RED = '#c8372d', GREY = '#777';
const FW = 480, FH = 380;

function pen(seed) {
  const gen = rough.generator({ options: { roughness: 1.1, bowing: 1.2, stroke: INK, strokeWidth: 2.6, seed } });
  const o = [];
  const add = (d, c = INK, w, dash) => { for (const p of gen.toPaths(d)) o.push(`<path d="${p.d}" stroke="${c}" stroke-width="${w || p.strokeWidth}" fill="none" stroke-linecap="round" stroke-linejoin="round"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`); };
  const k = {
    o,
    line: (x1, y1, x2, y2, c, w, dash) => add(gen.line(x1, y1, x2, y2), c, w, dash),
    rect: (x, y, w, h, c, sw, dash) => add(gen.rectangle(x, y, w, h), c, sw, dash),
    circ: (x, y, d, c, sw) => add(gen.circle(x, y, d), c, sw),
    text: (s, x, y, size, c = INK, anchor = 'middle') => o.push(`<text x="${x}" y="${y}" font-size="${size}" fill="${c}" text-anchor="${anchor}">${s.replace(/&/g, '&amp;').replace(/</g, '&lt;')}</text>`),
    raw: (s) => o.push(s),
  };
  k.arrow = (x1, y1, x2, y2, c, w, dash) => { k.line(x1, y1, x2, y2, c, w, dash); const a = Math.atan2(y2 - y1, x2 - x1), L = 14; k.line(x2, y2, x2 - L * Math.cos(a - 0.5), y2 - L * Math.sin(a - 0.5), c, w); k.line(x2, y2, x2 - L * Math.cos(a + 0.5), y2 - L * Math.sin(a + 0.5), c, w); };
  return k;
}
const tw = (s, size) => s.length * size * 0.47;      // rough text width for Patrick Hand

// each token: [width, draw(k, x, cy)] where x is the left edge and cy the row's centre line
function token(t) {
  const [kind, ...rest] = t.split(':'); const arg = rest.join(':');
  if (kind === 'me') return [62, (k, x, cy) => {
    const happy = arg === ')', cx = x + 31;
    k.circ(cx, cy, 58);
    k.raw(`<circle cx="${cx - 10}" cy="${cy - 6}" r="3" fill="${INK}"/><circle cx="${cx + 10}" cy="${cy - 6}" r="3" fill="${INK}"/>`);
    k.raw(happy ? `<path d="M ${cx - 12} ${cy + 8} Q ${cx} ${cy + 20} ${cx + 12} ${cy + 8}" stroke="${INK}" stroke-width="2.6" fill="none" stroke-linecap="round"/>`
                : `<path d="M ${cx - 12} ${cy + 16} Q ${cx} ${cy + 4} ${cx + 12} ${cy + 16}" stroke="${INK}" stroke-width="2.6" fill="none" stroke-linecap="round"/>`);
    k.text('me', cx, cy + 60, 24);
  }];
  if (kind === 'doc' || kind === 'doc?') return [Math.max(76, tw(arg, 26)), (k, x, cy) => {
    const w = Math.max(76, tw(arg, 26)), dx = x + (w - 76) / 2, dash = kind === 'doc?' ? '3 9' : null, c = dash ? '#999' : INK;
    k.rect(dx, cy - 47, 76, 94, c, 2.6, dash);
    for (let i = 0; i < 4; i++) k.line(dx + 12, cy - 25 + i * 17, dx + 64, cy - 25 + i * 17, c, 2, dash);
    k.text(arg, x + w / 2, cy - 58, 26, c);
  }];
  if (kind === 'docs') return [Math.max(96, tw(arg, 26)), (k, x, cy) => {
    const w = Math.max(96, tw(arg, 26)), dx = x + (w - 96) / 2;
    k.rect(dx + 20, cy - 57, 76, 94); k.rect(dx + 10, cy - 50, 76, 94);
    k.raw(`<rect x="${dx}" y="${cy - 43}" width="76" height="94" fill="#fff"/>`);
    k.rect(dx, cy - 43, 76, 94);
    for (let i = 0; i < 4; i++) k.line(dx + 12, cy - 21 + i * 17, dx + 64, cy - 21 + i * 17, INK, 2);
    k.text(arg, x + w / 2, cy - 68, 26);
  }];
  if (kind === 'box') { const w = Math.max(100, tw(arg, 28) + 30); return [w, (k, x, cy) => { k.rect(x, cy - 38, w, 76); k.text(arg, x + w / 2, cy + 9, 28); }]; }
  if (kind === '->') return [56, (k, x, cy) => k.arrow(x + 4, cy, x + 52, cy)];
  if (kind === 'eye->') return [84, (k, x, cy, red) => {
    k.arrow(x + 4, cy, x + 80, cy);
    const ex = x + 42, ey = cy - 44, c = red ? RED : INK;
    k.raw(`<path d="M ${ex - 34} ${ey} Q ${ex} ${ey - 30} ${ex + 34} ${ey} Q ${ex} ${ey + 30} ${ex - 34} ${ey} Z" stroke="${c}" stroke-width="3" fill="none" stroke-linejoin="round"/><circle cx="${ex}" cy="${ey}" r="9" fill="${c}"/>`);
  }];
  if (kind === '-x-') return [70, (k, x, cy) => { k.line(x + 2, cy, x + 68, cy, INK, 2.6, '3 10'); k.line(x + 19, cy - 16, x + 51, cy + 16, INK, 3.2); k.line(x + 51, cy - 16, x + 19, cy + 16, INK, 3.2); }];
  if (kind === 'x') return [50, (k, x, cy) => { k.line(x + 5, cy - 20, x + 45, cy + 20, INK, 3.4); k.line(x + 45, cy - 20, x + 5, cy + 20, INK, 3.4); }];
  if (kind === 'neq') return [60, (k, x, cy) => { k.line(x + 6, cy - 10, x + 54, cy - 10, INK, 3.2); k.line(x + 6, cy + 10, x + 54, cy + 10, INK, 3.2); k.line(x + 16, cy + 26, x + 44, cy - 26, INK, 3.2); }];
  if (kind === 'check') return [50, (k, x, cy) => k.raw(`<path d="M ${x + 4} ${cy + 2} l 14 16 l 28 -38" stroke="${INK}" stroke-width="3.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`)];
  if (kind === 'bulb') return [52, (k, x, cy) => { const cx = x + 26, by = cy - 62; k.circ(cx, by, 30); k.line(cx - 9, by + 18, cx + 9, by + 18); k.line(cx - 7, by + 25, cx + 7, by + 25); k.line(cx, by - 24, cx, by - 33); k.line(cx - 22, by - 14, cx - 30, by - 20); k.line(cx + 22, by - 14, cx + 30, by - 20); }];
  if (kind === 'pencil') return [100, (k, x, cy) => { k.raw(`<path d="M ${x + 8} ${cy + 36} l 70 -70 l 16 16 l -70 70 l -22 6 z" stroke="${INK}" stroke-width="2.6" fill="none" stroke-linejoin="round"/>`); k.text('written', x + 50, cy + 84, 26); }];
  if (kind === 'eyeb') return [96, (k, x, cy) => { const ex = x + 48; k.raw(`<path d="M ${ex - 44} ${cy} Q ${ex} ${cy - 36} ${ex + 44} ${cy} Q ${ex} ${cy + 36} ${ex - 44} ${cy} Z" stroke="${INK}" stroke-width="2.8" fill="none" stroke-linejoin="round"/><circle cx="${ex}" cy="${cy}" r="10" fill="${INK}"/>`); k.text('read', ex, cy + 84, 26); }];
  if (kind === 'bar') { const pct = arg.split(':')[0], label = arg.split(':').slice(1).join(':').trim(); const w = Math.max(70, tw(label, 24)); return [w, (k, x, cy) => { const h = Math.max(6, 150 * (+pct) / 100), bx = x + (w - 56) / 2; k.rect(bx, cy + 50 - h, 56, h); k.line(x - 6, cy + 50, x + w + 6, cy + 50); k.text(label, x + w / 2, cy + 82, 24); }]; }
  if (kind === 'txt') return [tw(arg, 34), (k, x, cy) => k.text(arg, x + tw(arg, 34) / 2, cy + 12, 34)];
  throw new Error('unknown token ' + t);
}

function frameBody(k, spec, i, ox, oy) {
  const c = spec.red ? RED : INK;
  k.rect(ox, oy, FW, FH, spec.red ? RED : '#bbb', 2);
  k.text(`${i + 1}.  ${spec.cap[0]}`, ox + 22, oy + 48, 30, c, 'start');
  if (spec.cap[1]) k.text(spec.cap[1], ox + 56, oy + 84, 30, c, 'start');
  const toks = spec.t.map(token), gap = 14;
  const total = toks.reduce((s, t) => s + t[0], 0) + gap * (toks.length - 1);
  const scale = Math.min(1, (FW - 50) / total), cy = oy + 232;
  const start = ox + (FW - total * scale) / 2;
  k.raw(`<g transform="translate(${start} ${cy}) scale(${scale}) translate(0 ${-cy})">`);
  let x = 0;
  for (const [w, draw] of toks) { draw(k, x, cy, spec.red); x += w + gap; }
  k.raw('</g>');
}
function arcBody(k, spec, W, top) {
  const n = spec.arc.length, x0 = 230, x1 = W - 110;
  const xs = spec.arc.map((_, i) => x0 + (x1 - x0) * i / (n - 1)), ys = spec.arc.map(v => top + 160 - v * 150);
  for (let i = 0; i < n - 1; i++) k.line(xs[i], ys[i], xs[i + 1], ys[i + 1], i === n - 2 ? RED : INK, 3);
  xs.forEach((x, i) => { const c = i === n - 1 ? RED : INK; k.raw(`<circle cx="${x}" cy="${ys[i]}" r="16" fill="#fff" stroke="${c}" stroke-width="2.6"/>`); k.text(String(i + 1), x, ys[i] + 9, 26, c); });
  k.text('going well', 44, top + 22, 24, GREY, 'start'); k.text('going badly', 44, top + 166, 24, GREY, 'start');
}
const wrap = (o, W, H) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}"><style>@font-face{font-family:'PH';src:url(data:font/woff2;base64,${font}) format('woff2');}text{font-family:'PH',cursive}</style><rect width="100%" height="100%" fill="#fff"/>${o.join('\n')}</svg>`;

(async () => {
  const b = await chromium.launch();
  const shot = async (svg, W, H, file, dsf = 2) => { const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: dsf }); await p.setContent(`<body style="margin:0">${svg}</body>`); await p.evaluate(() => document.fonts.ready); await p.screenshot({ path: file }); await p.close(); };
  let seed = 3;
  for (const [slug, spec] of Object.entries(specs)) {
    const dir = path.join(ROOT, 'ai', slug); fs.mkdirSync(dir, { recursive: true });
    // the arc line
    let k = pen(seed++); k.text(spec.title, 550, 60, 44); arcBody(k, spec, 1100, 100);
    await shot(wrap(k.o, 1100, 300), 1100, 300, path.join(dir, 'arc.png'));
    // each frame on its own
    for (let i = 0; i < spec.frames.length; i++) { k = pen(seed++); frameBody(k, spec.frames[i], i, 4, 4); await shot(wrap(k.o, FW + 8, FH + 8), FW + 8, FH + 8, path.join(dir, `f${i + 1}.png`)); }
    // the review sheet
    if (process.env.SHEETS) {
      k = pen(seed++); k.text(spec.title, 550, 70, 46); arcBody(k, spec, 1100, 110);
      spec.frames.forEach((f, i) => frameBody(k, f, i, 50 + (i % 2) * 520, 330 + Math.floor(i / 2) * 410));
      k.text(spec.foot, 550, 1600, 24, GREY);
      await shot(wrap(k.o, 1100, 1640), 1100, 1640, path.join(process.env.SHEETS, `${slug}.png`), 1);
    }
  }
  await b.close();
})();
