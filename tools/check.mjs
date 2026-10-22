import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
const walk = (d, acc = []) => { for (const e of readdirSync(d)) { const p = join(d, e);
  statSync(p).isDirectory() ? walk(p, acc) : (p.endsWith('.html') && acc.push(p)); } return acc; };
const files = walk('_site');
const routes = JSON.parse(readFileSync('src/_data/routes.json', 'utf8'));
const valid = new Set(Object.values(routes).flatMap(r => Object.values(r)));
let problems = [];
// Redirect stubs are not content pages: no h1, no hreflang set, by design.
const isRedirect = (h) => /http-equiv="refresh"/.test(h) && /name="robots" content="noindex/.test(h);

for (const f of files) {
  const h = readFileSync(f, 'utf8');
  const url = '/' + f.replace(/^_site\//, '').replace(/index\.html$/, '');
  const h1 = (h.match(/<h1[\s>]/g) || []).length;
  if (isRedirect(h)) continue;
  if (h1 !== 1) problems.push(`${url} h1=${h1}`);
  if (!/<link rel="canonical"/.test(h)) problems.push(`${url} no canonical`);
  if ((h.match(/rel="alternate"/g) || []).length !== 5) problems.push(`${url} hreflang!=5`);
  if (/—/.test(h.replace(/<!--[\s\S]*?-->/g, ''))) problems.push(`${url} em dash`);
  if (/href="#"/.test(h)) problems.push(`${url} href-hash`);
  if (/imma__victoria/.test(h)) problems.push(`${url} old instagram`);
  if (/fonts\.googleapis/.test(h)) problems.push(`${url} google fonts`);
  if (/<title>\s*<\/title>/.test(h)) problems.push(`${url} empty title`);
  for (const m of h.matchAll(/href="(\/[^"#?]*)"/g)) {
    const t = m[1];
    if (!valid.has(t) && !t.startsWith('/assets') && t !== '/site.webmanifest') problems.push(`${url} -> ${t} unknown route`);
  }
  for (const m of h.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    try { JSON.parse(m[1]); } catch { problems.push(`${url} invalid JSON-LD`); }
  }
}
console.log(`pages: ${files.length}`);
const uniq = [...new Set(problems)];
console.log(uniq.length ? 'PROBLEMS:\n  ' + uniq.slice(0, 20).join('\n  ') : 'no problems');
console.log(`unique problems: ${uniq.length}`);
