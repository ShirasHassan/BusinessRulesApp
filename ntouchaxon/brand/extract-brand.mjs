// Extracts logo, colors and fonts from a website into brand.json + assets/.
// Usage: npm i -D playwright && node extract-brand.mjs [url]   (default https://nasneuron.com)
import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, join, extname } from 'node:path';
import { fileURLToPath } from 'node:url';

const url = process.argv[2] || 'https://nasneuron.com';
const out = dirname(fileURLToPath(import.meta.url));
const assets = join(out, 'assets');
await mkdir(assets, { recursive: true });

const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
await page.screenshot({ path: join(assets, 'reference-home.png') });

const data = await page.evaluate(() => {
  const abs = (u) => { try { return new URL(u, location.href).href; } catch { return null; } };
  const cs = (el) => el && getComputedStyle(el);
  const pick = (sel) => {
    const el = document.querySelector(sel); const s = cs(el);
    return s ? { color: s.color, bg: s.backgroundColor, font: s.fontFamily, size: s.fontSize, weight: s.fontWeight, radius: s.borderRadius } : null;
  };

  // Logo candidates: header/nav images, anything named/alt'd "logo", inline SVG in header.
  const imgs = [...document.querySelectorAll('img')].filter((i) =>
    /logo/i.test(i.src + i.alt + i.className + (i.parentElement?.className || '')) || i.closest('header,nav,.navbar,.header'));
  const logos = imgs.map((i) => ({ src: abs(i.currentSrc || i.src), alt: i.alt, w: i.naturalWidth, h: i.naturalHeight, inFooter: !!i.closest('footer') }));
  const svgLogos = [...document.querySelectorAll('header svg, nav svg, [class*=logo] svg')].slice(0, 3).map((s) => s.outerHTML);
  const icons = [...document.querySelectorAll('link[rel*=icon], meta[property="og:image"]')].map((l) => abs(l.href || l.content));

  // CSS custom properties declared on :root (same-origin sheets only).
  const vars = {};
  for (const sheet of document.styleSheets) {
    let rules; try { rules = sheet.cssRules; } catch { continue; }
    for (const r of rules) if (r.selectorText && /:root|^html$|^body$/.test(r.selectorText))
      for (const p of r.style) if (p.startsWith('--')) vars[p] = r.style.getPropertyValue(p).trim();
  }

  // Color frequency weighted by visible area, so brand colors outrank stray ones.
  const freq = {};
  const add = (c, w) => { if (c && !/rgba\(0, 0, 0, 0\)|transparent/.test(c)) freq[c] = (freq[c] || 0) + w; };
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    const s = cs(el); const area = Math.min(r.width * r.height, 2e5);
    add(s.backgroundColor, area); add(s.color, (el.textContent || '').trim().length ? 500 : 0);
    if (s.borderTopWidth !== '0px') add(s.borderTopColor, 50);
  }
  const palette = Object.entries(freq).sort((a, b) => b[1] - a[1]).slice(0, 16).map(([c]) => c);

  const fontLinks = [...document.querySelectorAll('link[href*="fonts."]')].map((l) => l.href);
  return {
    source: location.href, title: document.title,
    description: document.querySelector('meta[name=description]')?.content || '',
    logos, svgLogos, icons, cssVars: vars, palette, fontLinks,
    elements: {
      body: pick('body'), header: pick('header, .header, .navbar'), navLink: pick('header a, nav a'),
      h1: pick('h1'), h2: pick('h2'), button: pick('.btn, button, a[class*=btn]'), footer: pick('footer'),
    },
    nav: [...document.querySelectorAll('header nav a, nav a')].map((a) => a.textContent.trim()).filter(Boolean).slice(0, 15),
    hero: document.querySelector('h1')?.textContent.trim() || '',
  };
});

// Download raster/vector logo files and icons.
const toHex = (c) => { const m = c.match(/\d+(\.\d+)?/g); if (!m || (m[3] !== undefined && +m[3] === 0)) return c;
  return '#' + m.slice(0, 3).map((n) => (+n).toString(16).padStart(2, '0')).join(''); };
const saved = [];
const urls = [...new Set([...data.logos.map((l) => l.src), ...data.icons].filter(Boolean))].slice(0, 8);
for (const [i, u] of urls.entries()) {
  try {
    const res = await page.request.get(u); if (!res.ok()) continue;
    const ext = extname(new URL(u).pathname).split('?')[0] || '.png';
    const file = `logo-${i}${ext}`; await writeFile(join(assets, file), await res.body()); saved.push({ file, from: u });
  } catch {}
}
data.svgLogos.forEach((svg, i) => { writeFile(join(assets, `logo-inline-${i}.svg`), svg); saved.push({ file: `logo-inline-${i}.svg`, from: 'inline' }); });

data.paletteHex = [...new Set(data.palette.map(toHex))];
data.savedAssets = saved;
delete data.svgLogos;
await writeFile(join(out, 'brand.json'), JSON.stringify(data, null, 2));
console.log(`brand.json written: ${data.paletteHex.length} colors, ${saved.length} assets, fonts: ${data.elements.body?.font}`);
await browser.close();
