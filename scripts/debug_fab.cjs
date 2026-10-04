const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  page.on('console', m => console.log('[console]', m.text()));
  page.on('pageerror', e => console.log('[pageerror]', e.message));
  const file = 'file:///' + path.resolve(__dirname, '../os/comprehensive-report.html').replace(/\\/g, '/');
  await page.goto(file, { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 1500));

  const info = async (label) => {
    const r = await page.evaluate(() => {
      const q = s => document.querySelector(s);
      const box = el => { if (!el) return null; const b = el.getBoundingClientRect(); const cs = getComputedStyle(el);
        return { x: b.x|0, y: b.y|0, w: b.width|0, h: b.height|0, display: cs.display, opacity: cs.opacity, pe: cs.pointerEvents, pos: cs.position, z: cs.zIndex, vis: cs.visibility, cls: el.className }; };
      const btn = q('#fabMainBtn');
      let hit = null;
      if (btn) { const b = btn.getBoundingClientRect(); const el = document.elementFromPoint(b.x + b.width/2, b.y + b.height/2); hit = el ? (el.tagName + '.' + el.className + '#' + el.id) : null; }
      const tocItem = q('#fabMenu .fab-item');
      let hitToc = null;
      if (tocItem) { const b = tocItem.getBoundingClientRect(); const el = document.elementFromPoint(b.x + b.width/2, b.y + b.height/2); hitToc = el ? (el.tagName + '.' + el.className) : null; }
      return { container: box(q('.fab-container')), btn: box(btn), hitAtBtn: hit, menu: box(q('#fabMenu')), tocItem: box(tocItem), hitAtTocItem: hitToc, sidebar: box(q('.report-sidebar')), aiBtn: box(q('.ask-ai-btn')) };
    });
    console.log('=== ' + label + ' ===\n' + JSON.stringify(r, null, 1));
  };

  await info('initial');
  await page.tap('#fabMainBtn').catch(e => console.log('tap fab failed', e.message));
  await new Promise(r => setTimeout(r, 600));
  await info('after FAB tap');
  await page.tap('#fabMenu .fab-item').catch(e => console.log('tap toc failed', e.message));
  await new Promise(r => setTimeout(r, 600));
  await info('after TOC tap');
  await page.screenshot({ path: path.resolve(__dirname, '../fab_debug.png') });
  await browser.close();
})();
