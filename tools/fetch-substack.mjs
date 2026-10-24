// Pulls the Substack feed into src/_data/journalPosts.json.
//
// Deliberately a separate script rather than an Eleventy data file that
// fetches on every build. Two reasons: a build should not fail because the
// network is down or Substack is slow, and the posts should land in a commit
// where they can be reviewed, not appear silently. Run it when something new
// is published:
//
//   node tools/fetch-substack.mjs
//
// Nothing is fetched by the visitor's browser. Substack's feed sends no CORS
// headers, so a client-side fetch would need a third-party proxy, and that
// would make the privacy page untrue.

import { writeFileSync, readFileSync } from 'node:fs';

const FEED = 'https://victoriaclaraswart.substack.com/feed';
const OUT = 'src/_data/journalPosts.json';
const MAX = 12;

const pick = (block, tag) => {
  const m = block.match(new RegExp(`<${tag}>([\\s\\S]*?)</${tag}>`));
  if (!m) return '';
  return m[1]
    .replace(/^<!\[CDATA\[/, '')
    .replace(/\]\]>$/, '')
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&nbsp;/g, ' ')
    // Substack sends numeric entities (&#8217; &#8212; and friends). Decode
    // them BEFORE the em-dash rule below, or an encoded em dash slips through
    // as &#8212; and the site check fails on it.
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)))
    .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)))
    // House style: no em or en dashes in anything the site renders.
    .replace(/\s*[—–]\s*/g, ', ')
    .trim();
};

const res = await fetch(FEED, { headers: { 'user-agent': 'victoriaswart.com build' } });
if (!res.ok) throw new Error(`Substack feed returned ${res.status}`);
const xml = await res.text();

const posts = [...xml.matchAll(/<item>([\s\S]*?)<\/item>/g)]
  .slice(0, MAX)
  .map((m) => {
    const b = m[1];
    const d = new Date(pick(b, 'pubDate'));
    return {
      title: pick(b, 'title'),
      summary: pick(b, 'description'),
      url: pick(b, 'link'),
      date: isNaN(d) ? null : d.toISOString().slice(0, 10),
    };
  })
  .filter((p) => p.title && p.url);

const previous = (() => {
  try { return JSON.parse(readFileSync(OUT, 'utf8')).length; } catch { return 0; }
})();

writeFileSync(OUT, JSON.stringify(posts, null, 2) + '\n');
console.log(`${OUT}: ${previous} -> ${posts.length} post(s)`);
for (const p of posts) console.log(`  ${p.date}  ${p.title}`);
