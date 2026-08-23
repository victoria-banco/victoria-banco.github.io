#!/usr/bin/env python3
"""Generate the multi-page, multi-language site from shared blocks."""
import json, re, pathlib, html as _h
from locales import LOCALES, DEFAULT, ROUTES, OFFER_MAP

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / '.build'
SITE = 'https://victoriaswart.com'
NAME = 'Victoria Clara Swart'

BLOCK_NAMES = ['cookie','nav','overlay','hero','cred','intro','services','statement',
               'about','work','editorial','consulting','journal','faq','testimonials',
               'contact','footer','privacy']

def blocks_for(loc):
    """Locale blocks fall back to English when a translation isn't present yet."""
    out = {}
    for n in BLOCK_NAMES:
        p = B / loc / f'{n}.html'
        if not p.exists():
            p = B / f'{n}.html'
        out[n] = p.read_text()
    return out

BLOCKS = blocks_for(DEFAULT)   # back-compat for the English build

def depth_of(url):
    """Directory depth of a page URL, used for relative asset paths."""
    return len([s for s in url.strip('/').split('/') if s])

def rel(depth):
    return '' if depth == 0 else '../' * depth

def lang_switcher(loc, route_key):
    """Dropdown offering every locale's equivalent of the current page."""
    cur = LOCALES[loc]
    opts = []
    for code, L in LOCALES.items():
        if route_key not in L.get('built', set(L['routes'])):
            continue
        href = L['routes'][route_key]
        sel = ' aria-current="true"' if code == loc else ''
        opts.append(f'      <a role="option" href="{href}" hreflang="{L["hreflang"]}" lang="{L["lang"]}"{sel}>{L["native"]}</a>')
    return f'''  <div class="lang-switch">
    <button class="lang-current" aria-haspopup="listbox" aria-expanded="false" aria-label="{cur['ui']['lang_label']}">
      <span>{cur['native']}</span>
      <svg width="9" height="6" viewBox="0 0 9 6" aria-hidden="true"><path d="M1 1l3.5 3.5L8 1" fill="none" stroke="currentColor" stroke-width="1"/></svg>
    </button>
    <div class="lang-menu" role="listbox">
{chr(10).join(opts)}
    </div>
  </div>'''

def nav_html(loc, route_key):
    L = LOCALES[loc]
    items = []
    for key in ['home','services','about','work','consulting','journal','contact']:
        href = L['routes'][key]
        cur = ' aria-current="page"' if key == route_key else ''
        items.append(f'    <li><a href="{href}"{cur}>{L["nav"][key]}</a></li>')
    return f'''<!-- NAV -->
<header>
<nav aria-label="{L['ui']['nav_aria']}">
  <a href="{L['routes']['home']}" class="nav-logo">{NAME}</a>
  <ul class="nav-links">
{chr(10).join(items)}
  </ul>
{lang_switcher(loc, route_key)}
  <button class="hamburger" aria-label="{L['ui']['menu_open']}">
    <span></span><span></span><span></span>
  </button>
</nav>
</header>'''

def overlay_html(loc):
    L = LOCALES[loc]
    items = '\n'.join(f'  <a href="{L["routes"][k]}">{L["nav"][k]}</a>'
                      for k in ['services','about','work','consulting','journal','contact'])
    return f'''<!-- MOBILE OVERLAY -->
<div class="nav-overlay">
  <span class="nav-overlay-label">{L['ui']['navigation']}</span>
  <a class="nav-overlay-home" href="{L['routes']['home']}">{L['nav']['home']}</a>
{items}
  <p class="nav-overlay-foot">{L['ui']['nav_foot']}</p>
</div>'''

def onward_html(loc, keys):
    L = LOCALES[loc]
    cards = []
    for k in keys:
        label, blurb = L['onward'][k]
        cards.append(
            f'    <a class="onward-card" href="{L["routes"][k]}">\n'
            f'      <span class="onward-label">{label}</span>\n'
            f'      <span class="onward-blurb">{blurb}</span>\n'
            f'      <span class="onward-go">{L["ui"]["read_on"]} &rarr;</span>\n'
            f'    </a>')
    return ('<!-- ONWARD -->\n<section class="onward reveal" aria-label="' + L['ui']['continue'] + '">\n'
            f'  <span class="section-label">{L["ui"]["continue"]}</span>\n'
            '  <div class="onward-grid">\n' + '\n'.join(cards) + '\n  </div>\n</section>')

def hreflang_tags(route_key):
    tags = [f'<link rel="alternate" hreflang="{L["hreflang"]}" href="{SITE}{L["routes"][route_key]}">'
            for L in LOCALES.values()
            if route_key in L.get('built', set(L['routes']))]
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{LOCALES[DEFAULT]["routes"][route_key]}">')
    return '\n'.join(tags)

ORG_SCHEMA = json.loads((B / 'schema_Org.json').read_text())

def breadcrumbs(trail):
    return {"@context":"https://schema.org","@type":"BreadcrumbList",
            "itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+u}
                               for i,(n,u) in enumerate(trail)]}

def page(*, loc, route_key, out_path, title, desc, body, extra_schema=None,
         trail=None, og_image='victoriahero.jpg', onward=None):
    L = LOCALES[loc]
    canonical = L['routes'][route_key]
    depth = depth_of(canonical)
    r = rel(depth)
    BL = blocks_for(loc)

    plain_t = _h.unescape(re.sub('<[^>]+>', '', title))
    plain_d = _h.unescape(desc)
    assert len(plain_t) <= 60, f'{out_path}: title {len(plain_t)} chars (max 60): {plain_t}'
    assert len(plain_d) <= 158, f'{out_path}: description {len(plain_d)} chars (max 158)'

    if onward:
        body = body + '\n\n' + onward_html(loc, onward)

    schemas = []
    if route_key == 'home' and loc == DEFAULT:
        schemas.append(ORG_SCHEMA)
    if trail:
        schemas.append(breadcrumbs(trail))
    schemas.extend(extra_schema or [])
    schema_html = '\n'.join(
        '<script type="application/ld+json">\n' + json.dumps(s, ensure_ascii=False, indent=2) + '\n</script>'
        for s in schemas)

    html = f'''<!DOCTYPE html>
<html lang="{L['lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="{NAME}">
<link rel="canonical" href="{SITE}{canonical}">
{hreflang_tags(route_key)}
<link rel="preload" as="image" href="{r}{og_image}" fetchpriority="high">

<!-- Favicon -->
<link rel="icon" type="image/png" sizes="32x32" href="{r}favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{r}favicon-16.png">
<link rel="icon" type="image/png" sizes="192x192" href="{r}favicon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="{r}apple-touch-icon.png">
<link rel="manifest" href="{r}site.webmanifest">
<meta name="theme-color" content="#18160E">

<!-- Crawling / indexing directives -->
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="geo.region" content="IT-RM">
<meta name="geo.placename" content="Rome, Italy">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:url" content="{SITE}{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/{og_image}">
<meta property="og:image:alt" content="{NAME}, multilingual brand strategist based in Rome">
<meta property="og:locale" content="{'de_DE' if loc=='de' else 'en_GB'}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/{og_image}">
<meta name="twitter:image:alt" content="{NAME}, multilingual brand strategist based in Rome">

<!-- Structured Data -->
{schema_html}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=Satoshi:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}styles.css">
</head>
<body data-locale="{loc}" data-route="{route_key}">

<div class="scroll-progress"></div>
<div class="cursor-ring"></div>

{BL['cookie']}
{nav_html(loc, route_key)}

{overlay_html(loc)}

<main id="main">
{body}
</main>

{BL['footer']}
{BL['privacy']}
<script src="{r}site.js"></script>
</body>
</html>
'''
    out = ROOT / out_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    return out_path
