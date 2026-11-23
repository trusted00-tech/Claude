// usage: node render.js <html> <outdir> [stills t1,t2,...]
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const [html, out, stills] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(html));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  const ts = stills ? stills.split(',').map(Number)
    : [...Array(Math.round(await p.evaluate(() => DUR * FPS))).keys()].map(i => i / 30);
  for (let i = 0; i < ts.length; i++) {
    await p.evaluate(t => seek(t), ts[i]);
    await p.screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 93 });
  }
  await b.close(); console.log('frames', ts.length);
})();
