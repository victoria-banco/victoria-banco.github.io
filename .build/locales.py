#!/usr/bin/env python3
"""Locale configuration: routes, nav labels, and UI strings per language."""

# Route keys are language-independent; each locale maps them to its own URL.
ROUTES = ['home', 'services', 'about', 'work', 'casestudy', 'consulting', 'journal', 'contact']

LOCALES = {
    'en': {
        'lang': 'en',
        'hreflang': 'en',
        'label': 'English',
        'native': 'English',
        'dir': '',                       # site root
        'routes': {
            'home': '/', 'services': '/services/', 'about': '/about/',
            'work': '/work/', 'casestudy': '/work/la-dolce-vita/',
            'consulting': '/consulting/', 'journal': '/journal/', 'contact': '/contact/',
        },
        'built': set(ROUTES),
        'nav': {'home':'Home','services':'Services','about':'About','work':'Work',
                'consulting':'Consulting','journal':'Journal','contact':'Contact'},
        'ui': {
            'nav_aria': 'Primary',
            'menu_open': 'Open menu',
            'navigation': 'Navigation',
            'nav_foot': 'Rome, Italy &nbsp;·&nbsp; Working Internationally',
            'continue': 'Continue',
            'read_on': 'Read on',
            'lang_label': 'Language',
            'switch_prompt': 'It looks like you prefer {lang}. Switch to the {lang} version?',
            'switch_yes': 'Switch to {lang}',
            'switch_no': 'Stay in English',
            'skip': 'Skip to content',
        },
        'onward': {
            'services':   ('Services', 'What I do — brand strategy, copywriting, SEO and creative direction'),
            'about':      ('About', 'Who I am, the five languages, and how the practice works'),
            'work':       ('Selected work', 'Projects across brand, communication and digital presence'),
            'casestudy':  ('Case study', 'A full brand and website concept for Italian luxury travel'),
            'consulting': ('Consulting', 'Strategy sessions, project consulting and ongoing partnership'),
            'journal':    ('The Journal', 'Essays on brand, language, psychology and culture'),
            'contact':    ('Contact', 'Start a conversation about your brand'),
        },
    },
    'de': {
        'lang': 'de',
        'hreflang': 'de',
        'label': 'German',
        'native': 'Deutsch',
        'dir': '/de',
        'routes': {
            'home': '/de/', 'services': '/de/leistungen/', 'about': '/de/ueber-mich/',
            'work': '/de/arbeiten/', 'casestudy': '/de/arbeiten/la-dolce-vita/',
            'consulting': '/de/beratung/', 'journal': '/de/journal/', 'contact': '/de/kontakt/',
        },
        # Only these routes have a real translation yet; hreflang, the sitemap and
        # the language switcher must not point at pages that don't exist.
        'built': set(ROUTES),
        'nav': {'home':'Start','services':'Leistungen','about':'Über mich','work':'Arbeiten',
                'consulting':'Beratung','journal':'Journal','contact':'Kontakt'},
        'ui': {
            'nav_aria': 'Hauptnavigation',
            'menu_open': 'Menü öffnen',
            'navigation': 'Navigation',
            'nav_foot': 'Rom, Italien &nbsp;·&nbsp; International tätig',
            'continue': 'Weiter',
            'read_on': 'Ansehen',
            'lang_label': 'Sprache',
            'switch_prompt': 'Sie scheinen Deutsch zu bevorzugen. Möchten Sie zur deutschen Fassung wechseln?',
            'switch_yes': 'Auf Deutsch ansehen',
            'switch_no': 'Auf Deutsch bleiben',
            'skip': 'Zum Inhalt springen',
        },
        'onward': {
            'services':   ('Leistungen', 'Markenstrategie, Text, SEO und Creative Direction'),
            'about':      ('Über mich', 'Wer ich bin, welche fünf Sprachen ich spreche und wie ich arbeite'),
            'work':       ('Arbeiten', 'Projekte aus Marke, Kommunikation und digitaler Präsenz'),
            'casestudy':  ('Fallstudie', 'Ein komplettes Marken- und Websitekonzept für den italienischen Luxusreisemarkt'),
            'consulting': ('Beratung', 'Strategiegespräche, Projektberatung und laufende Zusammenarbeit'),
            'journal':    ('Das Journal', 'Essays über Marke, Sprache, Psychologie und Kultur'),
            'contact':    ('Kontakt', 'Sprechen wir über Ihre Marke'),
        },
    },
}

DEFAULT = 'en'

# Browser language prefixes that should be offered a switch, mapped to the
# locale we can actually serve. Only languages with a real translation appear.
OFFER_MAP = {
    'de': 'de',   # Germany, Austria, Switzerland
}

# Languages we intend to add; kept here so the prompt copy is ready when they land.
PLANNED = ['it', 'es', 'da', 'nl']
