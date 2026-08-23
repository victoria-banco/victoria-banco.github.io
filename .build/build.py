#!/usr/bin/env python3
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gen import page, BLOCKS, blocks_for, rel, SITE, NAME, depth_of
from locales import LOCALES
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
    '#services':'services', '#about':'about', '#work':'work',
    '#consulting':'consulting', '#journal':'journal', '#contact':'contact',
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


def showcase_html(depth, title, note='Brand, copy, design and build by Victoria Clara Swart'):
    r = rel(depth)
    return f"""<!-- FULL-VIEWPORT WALKTHROUGH -->
<div class="showcase" id="showcase">
  <video id="showcaseVideo" poster="{r}ladolcevita-poster.jpg" preload="none"
         autoplay muted loop playsinline disablepictureinpicture
         aria-label="Walkthrough of the Italian luxury concierge website concept designed by Victoria Clara Swart">
    <source src="{r}ladolcevita-walkthrough.mp4" type="video/mp4">
  </video>
  <div class="showcase-caption">
    <span class="showcase-eyebrow">Selected work &middot; In motion</span>
    <p class="showcase-title">{title}</p>
    <span class="showcase-note">{note}</span>
  </div>
</div>"""


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

page(loc='en', route_key='home', out_path='index.html',
     title='Victoria Clara Swart — Brand Strategist, Rome',
     desc='Multilingual brand strategist and SEO copywriter in Rome. Brand positioning, content strategy and creative direction, delivered in five languages.',
     body=home_body,
     onward=['services','work','consulting'])

# ─────────────────────────────────────────── ABOUT
about_body = '\n\n'.join([
    h1(fix(BLOCKS['about'], 1), 'About<br><em>Victoria</em>'),
    fix(BLOCKS['cred'], 1),
    fix(BLOCKS['intro'], 1),
    fix(BLOCKS['statement'], 1),
])
page(loc='en', route_key='about', out_path='about/index.html',
     title='About — Victoria Clara Swart, Strategist in Rome',
     desc='Brand strategist based in Rome, working in English, German, Italian, Spanish and Danish across more than fifteen international markets.',
     body=about_body,
     og_image='victoria-swart-networking.jpg',
     onward=['services','work','contact'],
     trail=[('Home','/'), ('About','about')])

# ─────────────────────────────────────────── SERVICES
services_body = '\n\n'.join([
    h1(fix(BLOCKS['services'], 1), 'Services'),
    fix(BLOCKS['faq'], 1),
])
page(loc='en', route_key='services', out_path='services/index.html',
     title='Services — Brand Strategy &amp; SEO Copywriting',
     desc='Brand positioning, multilingual copywriting, social media strategy, SEO, web design and creative direction for international businesses.',
     body=services_body,
     og_image='victoria-swart-speaking.jpg', extra_schema=[SCHEMA_FAQ],
     onward=['consulting','work','contact'],
     trail=[('Home','/'), ('Services','services')])

# ─────────────────────────────────────────── WORK (index)
work_intro = BLOCKS['work']
# On the index the featured card must lead INTO the case study, not off-site.
work_intro = work_intro.replace(
    '''onclick="window.open('https://victoriaswart.com/ladolcevitaluxuryexperience/','_blank')"''',
    '''onclick="location.href='casestudy'"''', 1)
work_intro = re.sub(
    r'<a href="https://victoriaswart\.com/ladolcevitaluxuryexperience/"[^>]*class="cs-live-link"[^>]*>[^<]*</a>',
    '<a href="/work/la-dolce-vita/" class="cs-live-link">View the case study \u2192</a>',
    work_intro, count=1)
work_body = '\n\n'.join([
    showcase_html(1, 'Italian Luxury Concierge &mdash; the concept, in motion.'),
    h1(fix(work_intro, 1), 'Selected<br><em>Work</em>'),
    fix(BLOCKS['editorial'], 1),
])
page(loc='en', route_key='work', out_path='work/index.html',
     title='Selected Work — Brand &amp; Digital Projects',
     desc='Projects across brand strategy, communication and digital presence, including a full brand and website concept for Italian luxury travel.',
     body=work_body,
     og_image='victoria-swart-editorial.jpg',
     onward=['casestudy','services','contact'],
     trail=[('Home','/'), ('Work','work')])

# ─────────────────────────────────────────── CONSULTING
page(loc='en', route_key='consulting', out_path='consulting/index.html',
     title='Consulting &amp; Advisory — Sessions from €150',
     desc='Strategy sessions at €150, project consulting from €800, and ongoing strategic partnership at €2,000 a month. Direct support for founders.',
     body=h1(fix(BLOCKS['consulting'], 1), 'Consulting &amp;<br><em>Advisory</em>'),
     onward=['services','about','contact'],
     trail=[('Home','/'), ('Consulting','consulting')])

# ─────────────────────────────────────────── JOURNAL
page(loc='en', route_key='journal', out_path='journal/index.html',
     title='The Journal — Essays on Brand &amp; Language',
     desc='Essays on brand strategy, language, psychology and culture — the thinking behind how businesses are seen and remembered.',
     body=h1(fix(BLOCKS['journal'], 1), 'The<br><em>Journal</em>'),
     og_image='detailshot.jpg', extra_schema=[SCHEMA_BLOG],
     onward=['about','services','contact'],
     trail=[('Home','/'), ('Journal','journal')])

# ─────────────────────────────────────────── CONTACT
page(loc='en', route_key='contact', out_path='contact/index.html',
     title='Contact — Victoria Clara Swart, Rome',
     desc='Get in touch about brand strategy, multilingual communication, SEO content, speaking or event hosting. Based in Rome, working internationally.',
     body=h1(fix(BLOCKS['contact'], 1), "Let's Work<br><em>Together</em>"),
     onward=['services','consulting','work'],
     trail=[('Home','/'), ('Contact','contact')])

print('pages written')

# ─────────────────────────────────────────── CASE STUDY (+ full-viewport video)
cs = fix(BLOCKS['work'], 2)
# keep only the featured card, drop the grid of secondary studies
import re as _re
m = _re.search(r'<div class="case-study case-study--live".*?\n    </div>\n', cs, _re.S)
featured = m.group(0) if m else ''

showcase = showcase_html(2, 'The concept, in motion.')

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

page(loc='en', route_key='casestudy', out_path='work/la-dolce-vita/index.html',
     title='Italian Luxury Concierge — Brand Concept',
     desc='A full brand and website concept for an ultra-luxury Italian concierge service: positioning, copy direction, multilingual communication and build.',
     body=cs_body,
     extra_schema=[cs_schema], og_image='ladolcevita-poster.jpg',
     onward=['work','services','contact'],
     trail=[('Home','/'), ('Work','work'), ('Italian Luxury Concierge','casestudy')])

print('case study written')

# ─────────────────────────────────────────── 404
notfound = '''<section style="min-height:58svh;display:flex;align-items:center;">
  <div style="max-width:560px;">
    <span class="section-label">Error 404</span>
    <h1 class="section-heading">This page<br><em>doesn't exist.</em></h1>
    <div class="divider"></div>
    <p style="font-size:16px;font-weight:300;line-height:1.85;color:var(--stone);margin-bottom:32px;">
      The link may be out of date, or the address slightly off. Everything on the site is one click away below.
    </p>
    <a href="/" class="btn-primary">Back to the homepage</a>
  </div>
</section>'''

page(loc='en', route_key='home', out_path='404.html',
     title='Page not found — Victoria Clara Swart',
     desc='That page could not be found. Browse services, selected work, consulting or get in touch.',
     body=notfound,
     onward=['services','work','contact'])
print('404 written')

# ═══════════════════════════════════════════ GERMAN
DE = blocks_for('de')
de_faq_schema = _json.loads((_B/'schema_FAQPage_de.json').read_text()) if (_B/'schema_FAQPage_de.json').exists() else None

def de_fix(html, depth):
    """German blocks already carry ../ paths for depth 1; deepen for depth 2."""
    if depth == 2:
        html = html.replace('src="../', 'src="../../').replace('poster="../', 'poster="../../')
    return html

de_home = '\n\n'.join([
    DE['hero'], DE['cred'], DE['intro'], DE['services'],
    DE['statement'], DE['editorial'], DE['testimonials'],
])
page(loc='de', route_key='home', out_path='de/index.html',
     title='Victoria Clara Swart — Markenstrategin, Rom',
     desc='Mehrsprachige Markenstrategin und SEO-Texterin in Rom. Markenpositionierung, Content-Strategie und Creative Direction in fünf Sprachen.',
     body=de_home,
     onward=['services','work','consulting'],
     trail=[('Start','/de/')])

page(loc='de', route_key='services', out_path='de/leistungen/index.html',
     title='Leistungen — Markenstrategie &amp; SEO-Texte',
     desc='Markenpositionierung, mehrsprachige Texte, Social-Media-Strategie, SEO, Webdesign und Creative Direction für international tätige Unternehmen.',
     body='\n\n'.join([h1(DE['services'], 'Leistungen'), DE['faq']]),
     og_image='victoria-swart-speaking.jpg', extra_schema=[de_faq_schema] if de_faq_schema else [],
     onward=['consulting','work','contact'],
     trail=[('Start','/de/'), ('Leistungen','/de/leistungen/')])


page(loc='de', route_key='about', out_path='de/ueber-mich/index.html',
     title='Über mich — Victoria Clara Swart, Rom',
     desc='Markenstrategin mit Sitz in Rom, tätig auf Deutsch, Englisch, Italienisch, Spanisch und Dänisch in mehr als fünfzehn internationalen Märkten.',
     body='\n\n'.join([h1(DE['about'], 'Über<br><em>Victoria</em>'), DE['cred'], DE['intro'], DE['statement']]),
     og_image='victoria-swart-networking.jpg',
     onward=['services','work','contact'],
     trail=[('Start','/de/'), ('Über mich','/de/ueber-mich/')])

de_work = DE['work'].replace(
    '''onclick="window.open('https://victoriaswart.com/ladolcevitaluxuryexperience/','_blank')"''',
    '''onclick="location.href='/de/arbeiten/la-dolce-vita/'"''', 1)
de_work = re.sub(r'<a href="https://victoriaswart\.com/ladolcevitaluxuryexperience/"[^>]*class="cs-live-link"[^>]*>[^<]*</a>',
                 '<a href="/de/arbeiten/la-dolce-vita/" class="cs-live-link">Fallstudie ansehen \u2192</a>', de_work, count=1)
page(loc='de', route_key='work', out_path='de/arbeiten/index.html',
     title='Arbeiten — Marken- und Digitalprojekte',
     desc='Projekte aus Markenstrategie, Kommunikation und digitaler Präsenz, darunter ein komplettes Marken- und Websitekonzept für italienische Luxusreisen.',
     body='\n\n'.join([showcase_html(1, 'Italienischer Luxus-Concierge &mdash; das Konzept in Bewegung.',
                        'Marke, Text, Gestaltung und Umsetzung von Victoria Clara Swart'),
                        h1(de_work, 'Ausgewählte<br><em>Arbeiten</em>'), DE['editorial']]),
     og_image='victoria-swart-editorial.jpg',
     onward=['casestudy','services','contact'],
     trail=[('Start','/de/'), ('Arbeiten','/de/arbeiten/')])

de_cs = de_fix(DE['work'], 2)
m_de = re.search(r'<div class="case-study case-study--live".*?\n    </div>\n', de_cs, re.S)
de_featured = m_de.group(0) if m_de else ''
de_cs_body = (showcase_html(2, 'Das Konzept in Bewegung.',
                            'Marke, Text, Gestaltung und Umsetzung von Victoria Clara Swart') +
  '\n\n<section id="work">\n'
  '  <div class="reveal" style="max-width:820px;margin-bottom:48px;">\n'
  '    <span class="section-label">Fallstudie</span>\n'
  '    <h1 class="section-heading">Italienischer<br><em>Luxus-Concierge</em></h1>\n'
  '    <div class="divider"></div>\n'
  '  </div>\n'
  '  <div class="case-studies reveal">\n' + de_featured + '  </div>\n</section>')
page(loc='de', route_key='casestudy', out_path='de/arbeiten/la-dolce-vita/index.html',
     title='Italienischer Luxus-Concierge — Markenkonzept',
     desc='Ein vollständiges Marken- und Websitekonzept für einen italienischen Luxus-Concierge-Service: Positionierung, Textrichtung, mehrsprachige Kommunikation.',
     body=de_cs_body, extra_schema=[cs_schema], og_image='ladolcevita-poster.jpg',
     onward=['work','services','contact'],
     trail=[('Start','/de/'), ('Arbeiten','/de/arbeiten/'), ('Fallstudie','/de/arbeiten/la-dolce-vita/')])

page(loc='de', route_key='consulting', out_path='de/beratung/index.html',
     title='Beratung &amp; Strategie — ab 150 €',
     desc='Strategiegespräche ab 150 €, Projektberatung ab 800 € und laufende Begleitung für 2.000 € im Monat. Direkte Unterstützung für Gründerinnen und Gründer.',
     body=h1(DE['consulting'], 'Beratung &amp;<br><em>Strategie</em>'),
     onward=['services','about','contact'],
     trail=[('Start','/de/'), ('Beratung','/de/beratung/')])

page(loc='de', route_key='journal', out_path='de/journal/index.html',
     title='Das Journal — Essays zu Marke und Sprache',
     desc='Essays über Markenstrategie, Sprache, Psychologie und Kultur — das Denken dahinter, wie Unternehmen wahrgenommen und erinnert werden.',
     body=h1(DE['journal'], 'Das<br><em>Journal</em>'),
     og_image='detailshot.jpg', extra_schema=[SCHEMA_BLOG],
     onward=['about','services','contact'],
     trail=[('Start','/de/'), ('Journal','/de/journal/')])

page(loc='de', route_key='contact', out_path='de/kontakt/index.html',
     title='Kontakt — Victoria Clara Swart, Rom',
     desc='Sprechen wir über Markenstrategie, mehrsprachige Kommunikation, SEO-Inhalte, Vorträge oder Moderation. Sitz in Rom, international tätig.',
     body=h1(DE['contact'], "Arbeiten wir<br><em>zusammen</em>"),
     onward=['services','consulting','work'],
     trail=[('Start','/de/'), ('Kontakt','/de/kontakt/')])

print('german pages written')
