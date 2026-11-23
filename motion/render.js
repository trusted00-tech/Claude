// node render.js <config.json> <framesDir>  -> writes frames + cues.json
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const [cfgPath, out, stills] = process.argv.slice(2);
  const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
  fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.addInitScript(c => { window.CFG = c; }, cfg);
  await p.goto('file://' + path.resolve(__dirname, 'template.html'));
  await p.evaluate(async () => { await document.fonts.ready;
    await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })));
    await Promise.all([...document.querySelectorAll('video')].map(v => v.readyState >= 2 ? 0 : new Promise(r => { v.onloadeddata = v.onerror = r; }))); });
  const dur = await p.evaluate(() => DUR);
  fs.writeFileSync(path.join(out, 'cues.json'), JSON.stringify(await p.evaluate(() => CUES)));
  const ts = stills ? stills.split(',').map(Number) : [...Array(Math.round(dur * 30)).keys()].map(i => i / 30);
  for (let i = 0; i < ts.length; i++) {
    await p.evaluate(t => seek(t), ts[i]);
    await p.screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 93 });
  }
  await b.close(); console.log('frames', ts.length, 'dur', dur);
})();
