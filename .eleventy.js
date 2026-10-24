const routes = require('./src/_data/routes.json');
const site   = require('./src/_data/site.json');

module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ 'src/assets': 'assets' });
  eleventyConfig.addPassthroughCopy({ 'src/static': '.' });
  // src/static is copied verbatim. Without this, Eleventy ALSO treats the
  // .html files in there as templates and builds a second, stray page for
  // each one (/static/hero-check/ and so on), which then fails the hreflang
  // check because it has no language siblings.
  eleventyConfig.ignores.add('src/static/**/*.html');

  // URL for a route key in a given language
  eleventyConfig.addFilter('route', (key, lang) => {
    const r = routes[key];
    if (!r) throw new Error(`Unknown route key: ${key}`);
    const url = r[lang];
    if (!url) throw new Error(`Route ${key} missing language ${lang} (type ${typeof lang})`);
    return url;
  });

  // All language alternates for a route key, for hreflang
  eleventyConfig.addFilter('alternates', (key) => {
    const r = routes[key];
    return site.locales.map(l => ({ lang: l, url: r[l] }));
  });

  // Absolute URL
  eleventyConfig.addFilter('abs', (path) => site.url + path);

  // Current year, for copyright lines
  eleventyConfig.addFilter('year', () => new Date().getFullYear());

  // Price formatting per locale: EN "€1,500" · DE/IT/ES "1.500 €"
  eleventyConfig.addFilter('price', (n, lang) => {
    if (n === null || n === undefined) return '';
    const grouped = String(n).replace(/\B(?=(\d{3})+(?!\d))/g, lang === 'en' ? ',' : '.');
    return lang === 'en' ? `€${grouped}` : `${grouped} €`;
  });

  eleventyConfig.addFilter('json', (v) => JSON.stringify(v, null, 2));

  // Shared across every generated page. `lang` comes from each template's
  // pagination alias, so t and copy resolve to the right language on their own.
  // Shared across every generated page. `lang` comes from each template's
  // pagination alias, so t and copy resolve to the right language on their own.
  // Every accessor is defensive: Eleventy probes these with partial data while
  // it works out computed-value ordering.
  // The language of the page being rendered. Simple templates get it from their
  // pagination alias; paginated-over-objects templates carry it on the item.
  const langOf = (data) => {
    if (!data) return null;
    if (typeof data.lang === 'string' && data.lang) return data.lang;
    if (data.cp && data.cp.lang) return data.cp.lang;
    if (data.lp && data.lp.lang) return data.lp.lang;
    return null;
  };

  // Case pages get their title and description from the case itself.
  const caseOf = (data) => {
    if (!data || !data.cp || !data.cases) return null;
    const c = data.cases[data.cp.key];
    if (!c) return null;
    const ct = c[data.cp.lang];
    if (!ct) return null;
    const named = !c.flag || (data.flags && data.flags[c.flag]);
    return { c, ct, shownName: named ? ct.name : ct.nameFallback };
  };

  const copyBlock = (data) => {
    const all = data && data.allCopy;
    const lang = langOf(data);
    const key = (data && data.copyKey) || (data && data.lp && data.lp.key);
    if (!all || !lang || !key) return null;
    const forLang = all[lang];
    return forLang ? forLang[key] || null : null;
  };

  eleventyConfig.addGlobalData('eleventyComputed', {
    L:    (data) => langOf(data),
    t:    (data) => { const l = langOf(data); return l && data.i18n ? data.i18n[l] : undefined; },
    copy: (data) => { const l = langOf(data); return l && data.allCopy ? data.allCopy[l] : undefined; },
    // Taken straight from the copy object, never through a Nunjucks string, so
    // ampersands are escaped exactly once.
    title: (data) => {
      if (data && data.pageTitle) return data.pageTitle;
      const cs = caseOf(data);
      if (cs) return `${cs.shownName}: ${cs.c.stack} \u00b7 Victoria Swart`;
      const b = copyBlock(data);
      return b && b.title ? b.title : '';
    },
    description: (data) => {
      if (data && data.pageDescription) return data.pageDescription;
      const cs = caseOf(data);
      if (cs) return cs.ct.brief.slice(0, 155);
      const b = copyBlock(data);
      return b && b.description ? b.description : '';
    },
    schemaJobTitle: (data) => {
      const all = data && data.allCopy;
      const l = langOf(data);
      if (!all || !l || !all[l]) return '';
      return all[l].jobTitle || '';
    },
    routeKey: (data) => (data && data.routeKey) || (data && data.cp && data.cp.key) || (data && data.lp && data.lp.key) || null,
  });

  return {
    dir: { input: 'src', output: '_site', includes: '_includes', data: '_data' },
    markdownTemplateEngine: 'njk',
    htmlTemplateEngine: 'njk',
    templateFormats: ['njk', 'md', 'html'],
  };
};
