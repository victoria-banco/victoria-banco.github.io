// The date the site was generated, for <lastmod> in the sitemap.
//
// Note the .mjs extension. Eleventy 3.0 loads files in src/_data through the
// ESM loader even though this project is CommonJS, so a .js or .cjs file
// written with module.exports arrives in templates as the module namespace
// object, { default: ..., "module.exports": ... }, rather than the export
// itself. Nothing errors: the template just renders nothing, or prints
// [object Object]. A .mjs file with export default resolves correctly, and a
// function export is actually called. tools/check.mjs fails the build if a
// .js or .cjs file appears in this directory.
export default new Date().toISOString().slice(0, 10);
