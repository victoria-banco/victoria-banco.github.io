#!/usr/bin/env python3
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gen import page, BLOCKS, rel, SITE, NAME
import json as _json, pathlib as _pl
_B = _pl.Path(__file__).resolve().parent
SCHEMA_BLOG = _json.loads((_B/'schema_Blog.json').read_text())
SCHEMA_FAQ  = _json.loads((_B/'schema_FAQPage.json').read_text())

def h1(html, heading_html, h1_text=None):
    """Promote the page's leading section heading to an <h1>."""
    old = '<h2 class="section-heading">' + heading_html + '</h2>'
    new = '<h1 class="section-heading">' + heading_html + '</h1>'
    assert old in html, 'heading not found: ' + heading_html[:40]
    return html.replace(old, new, 1)

ASSETS = ['victoriahero.jpg','victoria-swart-speaking.jpg','victoria-swart-networking.jpg',
          'victoria-swart-editorial.jpg','detailshot.jpg','ladolcevita-walkthrough.mp4',
          'ladolcevita-poster.jpg']

ANCHOR_MAP = {
    '#services':'/services/', '#about':'/about/', '#work':'/work/',
    '#consulting':'/consulting/', '#journal':'/journal/', '#contact':'/contact/',
    '#home':'/', '#faq':'/services/#faq',
}

def fix(html, depth, *, keep_anchors=()):
    r = rel(depth)
    if r:
        for a in ASSETS:
            html = html.replace(f'src="{a}"', f'src="{r}{a}"')
            html = html.replace(f'poster="{a}"', f'poster="{r}{a}"')
    for frm, to in ANCHOR_MAP.items():
        if frm in keep_anchors:
            continue
        html = html.replace(f'href="{frm}"', f'href="{to}"')
    return html

def strip_reveal_ids(html):
    return html

# ─────────────────────────────────────────── HOME
services_preview = BLOCKS['services']
# home shows the services list but sends detail-seekers to /services/
services_preview = services_preview.replace(
    '<h2 class="section-heading">Services</h2>',
    '<h2 class="section-heading">Services</h2>')

home_body = '\n\n'.join([
    fix(BLOCKS['hero'], 0),
    fix(BLOCKS['cred'], 0),
    fix(BLOCKS['intro'], 0),
    fix(services_preview, 0),
    fix(BLOCKS['statement'], 0),
    fix(BLOCKS['editorial'], 0),
    fix(BLOCKS['testimonials'], 0),
])

page(path='index.html', depth=0, current='/',
     title=f'{NAME} — Multilingual Brand Strategist &amp; SEO Copywriter | Rome, Italy',
     desc='Victoria Clara Swart — multilingual brand strategist and SEO copywriter based in Rome. Native English and German, fluent Italian, Spanish and Danish. Brand positioning, content strategy, and creative direction for international clients.',
     canonical='/', body=home_body)

# ─────────────────────────────────────────── ABOUT
about_body = '\n\n'.join([
    h1(fix(BLOCKS['about'], 1), 'About<br><em>Victoria</em>'),
    fix(BLOCKS['cred'], 1),
    fix(BLOCKS['intro'], 1),
    fix(BLOCKS['statement'], 1),
])
page(path='about/index.html', depth=1, current='/about/',
     title=f'About {NAME} — Brand Strategist in Rome, Five Languages',
     desc='Victoria Clara Swart is a multilingual brand strategist based in Rome, working in English, German, Italian, Spanish and Danish across more than fifteen markets.',
     canonical='/about/', body=about_body,
     og_image='victoria-swart-networking.jpg',
     trail=[('Home','/'), ('About','/about/')])

# ─────────────────────────────────────────── SERVICES
services_body = '\n\n'.join([
    h1(fix(BLOCKS['services'], 1), 'Services'),
    fix(BLOCKS['faq'], 1),
])
page(path='services/index.html', depth=1, current='/services/',
     title=f'Services — Brand Strategy, SEO Copywriting &amp; Creative Direction | {NAME}',
     desc='Brand positioning, multilingual copywriting, social media strategy, SEO, web design and creative direction — for international businesses that sell on judgement rather than price.',
     canonical='/services/', body=services_body,
     og_image='victoria-swart-speaking.jpg', extra_schema=[SCHEMA_FAQ],
     trail=[('Home','/'), ('Services','/services/')])

# ─────────────────────────────────────────── WORK (index)
work_intro = BLOCKS['work']
work_body = '\n\n'.join([
    h1(fix(work_intro, 1), 'Selected<br><em>Work</em>'),
    fix(BLOCKS['editorial'], 1),
])
page(path='work/index.html', depth=1, current='/work/',
     title=f'Selected Work — Brand &amp; Digital Projects | {NAME}',
     desc='Selected projects across brand strategy, communication and digital presence — including a full brand and website concept for an ultra-luxury Italian concierge service.',
     canonical='/work/', body=work_body,
     og_image='victoria-swart-editorial.jpg',
     trail=[('Home','/'), ('Work','/work/')])

# ─────────────────────────────────────────── CONSULTING
page(path='consulting/index.html', depth=1, current='/consulting/',
     title=f'Consulting &amp; Advisory — Strategy Sessions from €150 | {NAME}',
     desc='Direct strategic support for founders and businesses. One-off 60-minute strategy sessions at €150, project consulting from €800, and ongoing strategic partnership at €2,000 per month.',
     canonical='/consulting/', body=h1(fix(BLOCKS['consulting'], 1), 'Consulting &amp;<br><em>Advisory</em>'),
     trail=[('Home','/'), ('Consulting','/consulting/')])

# ─────────────────────────────────────────── JOURNAL
page(path='journal/index.html', depth=1, current='/journal/',
     title=f'The Journal — Essays on Brand, Language &amp; Culture | {NAME}',
     desc='Essays on brand strategy, language, psychology and culture — the thinking behind how businesses are seen and remembered.',
     canonical='/journal/', body=h1(fix(BLOCKS['journal'], 1), 'The<br><em>Journal</em>'),
     og_image='detailshot.jpg', extra_schema=[SCHEMA_BLOG],
     trail=[('Home','/'), ('Journal','/journal/')])

# ─────────────────────────────────────────── CONTACT
page(path='contact/index.html', depth=1, current='/contact/',
     title=f'Contact — Start a Conversation | {NAME}',
     desc='Get in touch about brand strategy, multilingual communication, SEO content, speaking or event hosting. Based in Rome, working internationally.',
     canonical='/contact/', body=h1(fix(BLOCKS['contact'], 1), "Let's Work<br><em>Together</em>"),
     trail=[('Home','/'), ('Contact','/contact/')])

print('pages written')

# ─────────────────────────────────────────── CASE STUDY (+ full-viewport video)
cs = fix(BLOCKS['work'], 2)
# keep only the featured card, drop the grid of secondary studies
import re as _re
m = _re.search(r'<div class="case-study case-study--live".*?\n    </div>\n', cs, _re.S)
featured = m.group(0) if m else ''

showcase = '''<!-- FULL-VIEWPORT WALKTHROUGH -->
<div class="showcase" id="showcase">
  <video id="showcaseVideo" poster="../../ladolcevita-poster.jpg" preload="none"
         autoplay muted loop playsinline disablepictureinpicture
         aria-label="Walkthrough of the Italian luxury concierge website concept designed by Victoria Clara Swart">
    <source src="../../ladolcevita-walkthrough.mp4" type="video/mp4">
  </video>
  <div class="showcase-caption">
    <span class="showcase-eyebrow">Selected work &middot; In motion</span>
    <p class="showcase-title">The concept, in motion.</p>
    <span class="showcase-note">Brand, copy, design and build by Victoria Clara Swart</span>
  </div>
</div>'''

cs_body = (showcase +
  '\n\n<section id="work">\n'
  '  <div class="reveal" style="max-width:820px;margin-bottom:48px;">\n'
  '    <span class="section-label">Case study</span>\n'
  '    <h1 class="section-heading">Italian Luxury<br><em>Concierge</em></h1>\n'
  '    <div class="divider"></div>\n'
  '  </div>\n'
  '  <div class="case-studies reveal">\n' + featured + '  </div>\n</section>')

cs_schema = {
  "@context":"https://schema.org","@type":"CreativeWork",
  "name":"Italian Luxury Concierge — Brand & Web Concept",
  "url":SITE+"/work/la-dolce-vita/",
  "description":"An independently developed brand and digital concept for an ultra-luxury Italian concierge service: brand positioning, copy direction, multilingual communication, and a complete website.",
  "creator":{"@type":"Person","name":NAME,"url":SITE},
  "author":{"@type":"Person","name":NAME,"url":SITE},
  "copyrightHolder":{"@type":"Person","name":NAME,"url":SITE},
  "copyrightYear":2026,
  "copyrightNotice":"© 2026 Victoria Clara Swart. All rights reserved. Not licensed for commercial use or reproduction by any third party.",
  "creditText":"Concept, strategy, copy and design by Victoria Clara Swart",
  "video":{"@type":"VideoObject","name":"Italian Luxury Concierge — concept walkthrough",
           "description":"Screen walkthrough of the concept website.",
           "thumbnailUrl":SITE+"/ladolcevita-poster.jpg",
           "contentUrl":SITE+"/ladolcevita-walkthrough.mp4",
           "uploadDate":"2026-08-23"},
  "keywords":"brand strategy, luxury travel branding, multilingual copywriting, web design concept"
}

page(path='work/la-dolce-vita/index.html', depth=2, current='/work/',
     title='Italian Luxury Concierge — Brand &amp; Web Concept | ' + NAME,
     desc='A full brand and digital concept for an ultra-luxury Italian concierge service: positioning, copy direction, multilingual communication and a complete website, developed independently by Victoria Clara Swart.',
     canonical='/work/la-dolce-vita/', body=cs_body,
     extra_schema=[cs_schema], og_image='ladolcevita-poster.jpg',
     trail=[('Home','/'), ('Work','/work/'), ('Italian Luxury Concierge','/work/la-dolce-vita/')])

print('case study written')
