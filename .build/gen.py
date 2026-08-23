#!/usr/bin/env python3
"""Generate the multi-page site from shared blocks."""
import json, os, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / '.build'
SITE = 'https://victoriaswart.com'
NAME = 'Victoria Clara Swart'

def block(n): return (B / f'{n}.html').read_text()

BLOCKS = {n: block(n) for n in [
    'cookie','nav','overlay','hero','cred','intro','services','statement',
    'about','work','editorial','consulting','journal','faq','testimonials',
    'contact','footer','privacy']}

NAV = [('Services','/services/'), ('About','/about/'), ('Work','/work/'),
       ('Consulting','/consulting/'), ('Journal','/journal/'), ('Contact','/contact/')]

def nav_html(depth, current):
    home = '/'
    def li(label, href):
        cur = ' aria-current="page"' if href == current else ''
        return f'    <li><a href="{href}"{cur}>{label}</a></li>'
    items = '\n'.join(li(l, h) for l, h in NAV)
    return f'''<!-- NAV -->
<header>
<nav aria-label="Primary">
  <a href="{home}" class="nav-logo">{NAME}</a>
  <ul class="nav-links">
{items}
  </ul>
  <button class="hamburger" aria-label="Open menu">
    <span></span><span></span><span></span>
  </button>
</nav>
</header>'''

def overlay_html(current):
    items = '\n'.join(f'  <a href="{href}">{label}</a>' for label, href in NAV)
    return f'''<!-- MOBILE OVERLAY -->
<div class="nav-overlay">
  <span class="nav-overlay-label">Navigation</span>
{items}
  <p class="nav-overlay-foot">Rome, Italy &nbsp;·&nbsp; Working Internationally</p>
</div>'''

def rel(depth):
    return '' if depth == 0 else '../' * depth

ONWARD = {
  '/services/':    ('Services',   'What I do — brand strategy, copywriting, SEO and creative direction'),
  '/about/':       ('About',      'Who I am, the five languages, and how the practice works'),
  '/work/':        ('Selected work', 'Projects across brand, communication and digital presence'),
  '/work/la-dolce-vita/': ('Case study', 'A full brand and website concept for Italian luxury travel'),
  '/consulting/':  ('Consulting', 'Strategy sessions, project consulting and ongoing partnership'),
  '/journal/':     ('The Journal','Essays on brand, language, psychology and culture'),
  '/contact/':     ('Contact',    'Start a conversation about your brand'),
}

def onward_html(hrefs, depth):
    cards = []
    for h in hrefs:
        label, blurb = ONWARD[h]
        cards.append(
            f'    <a class="onward-card" href="{h}">\n'
            f'      <span class="onward-label">{label}</span>\n'
            f'      <span class="onward-blurb">{blurb}</span>\n'
            f'      <span class="onward-go">Read on &rarr;</span>\n'
            f'    </a>')
    return ('<!-- ONWARD -->\n<section class="onward reveal" aria-label="Continue reading">\n'
            '  <span class="section-label">Continue</span>\n'
            '  <div class="onward-grid">\n' + '\n'.join(cards) + '\n  </div>\n</section>')

ORG_SCHEMA = json.loads(re.search(
    r'<script type="application/ld\+json">\s*(\{.*?"@type": "ProfessionalService".*?\})\s*</script>',
    (ROOT/'index.html').read_text(), re.S).group(1))

def breadcrumbs(trail):
    return {"@context":"https://schema.org","@type":"BreadcrumbList",
            "itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+u}
                               for i,(n,u) in enumerate(trail)]}

def page(*, path, depth, title, desc, canonical, body, extra_schema=None,
         trail=None, og_image='victoriahero.jpg', current='', onward=None):
    r = rel(depth)
    import html as _h
    plain_t = _h.unescape(re.sub('<[^>]+>', '', title))
    plain_d = _h.unescape(desc)
    assert len(plain_t) <= 60, f'{path}: title {len(plain_t)} chars (max 60): {plain_t}'
    assert len(plain_d) <= 158, f'{path}: description {len(plain_d)} chars (max 158)'
    if onward:
        body = body + '\n\n' + onward_html(onward, depth)
    schemas = []
    if depth == 0:
        schemas.append(ORG_SCHEMA)
    if trail:
        schemas.append(breadcrumbs(trail))
    for s in (extra_schema or []):
        schemas.append(s)
    schema_html = '\n'.join(
        '<script type="application/ld+json">\n' + json.dumps(s, ensure_ascii=False, indent=2) + '\n</script>'
        for s in schemas)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="{NAME}">
<link rel="canonical" href="{SITE}{canonical}">
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
<meta property="og:locale" content="en_GB">

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
<body>

<div class="scroll-progress"></div>
<div class="cursor-ring"></div>

{BLOCKS['cookie']}
{nav_html(depth, current)}

{overlay_html(current)}

<main id="main">
{body}
</main>

{BLOCKS['footer']}
{BLOCKS['privacy']}
<script src="{r}site.js"></script>
</body>
</html>
'''
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    return path
