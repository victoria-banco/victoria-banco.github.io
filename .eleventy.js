const routes = require('./src/_data/routes.json');
const site   = require('./src/_data/site.json');

module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ 'src/assets': 'assets' });
  eleventyConfig.addPassthroughCopy({ 'src/static': '.' });

  // URL for a route key in a given language
  eleventyConfig.addFilter('route', (key, lang) => {
    const r = routes[key];
    if (!r) throw new Error(`Unknown route key: ${key}`);
    const url = r[lang];
    if (!url) throw new Error(`Route ${key} missing language ${lang}`);
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
  const copyBlock = (data) => {
    const all = data && data.allCopy;
    const lang = data && data.lang;
    const key = data && data.copyKey;
    if (!all || !lang || !key) return null;
    const forLang = all[lang];
    return forLang ? forLang[key] || null : null;
  };

  eleventyConfig.addGlobalData('eleventyComputed', {
    t:    (data) => (data && data.lang && data.i18n ? data.i18n[data.lang] : undefined),
    copy: (data) => (data && data.lang && data.allCopy ? data.allCopy[data.lang] : undefined),
    // Taken straight from the copy object, never through a Nunjucks string, so
    // ampersands are escaped exactly once.
    title: (data) => {
      if (data && data.pageTitle) return data.pageTitle;
      const b = copyBlock(data);
      return b && b.title ? b.title : '';
    },
    description: (data) => {
      if (data && data.pageDescription) return data.pageDescription;
      const b = copyBlock(data);
      return b && b.description ? b.description : '';
    },
    schemaJobTitle: (data) => {
      const all = data && data.allCopy;
      const lang = data && data.lang;
      if (!all || !lang || !all[lang]) return '';
      return all[lang].jobTitle || '';
    },
  });

  return {
    dir: { input: 'src', output: '_site', includes: '_includes', data: '_data' },
    markdownTemplateEngine: 'njk',
    htmlTemplateEngine: 'njk',
    templateFormats: ['njk', 'md', 'html'],
  };
};
