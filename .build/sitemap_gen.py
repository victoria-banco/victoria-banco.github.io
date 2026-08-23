import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from locales import LOCALES
SITE='https://victoriaswart.com'
PRIO={'home':'1.0','services':'0.9','consulting':'0.9','about':'0.8','work':'0.8','contact':'0.8','journal':'0.7','casestudy':'0.7'}
FREQ={'journal':'weekly','casestudy':'yearly','contact':'yearly'}
rows=[]
for code,L in LOCALES.items():
    for key,url in L['routes'].items():
        if key not in L.get('built', set(L['routes'])): continue
        alts='\n'.join(f'    <xhtml:link rel="alternate" hreflang="{o["hreflang"]}" href="{SITE}{o["routes"][key]}"/>'
                       for o in LOCALES.values()
                       if key in o.get('built', set(o['routes'])))
        rows.append(f'''  <url>
    <loc>{SITE}{url}</loc>
{alts}
    <lastmod>2026-08-23</lastmod>
    <changefreq>{FREQ.get(key,'monthly')}</changefreq>
    <priority>{PRIO[key]}</priority>
  </url>''')
rows.append(f'''  <url>
    <loc>{SITE}/ladolcevitaluxuryexperience/</loc>
    <lastmod>2026-08-23</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.6</priority>
  </url>''')
out='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'+'\n'.join(rows)+'\n</urlset>\n'
(pathlib.Path(__file__).resolve().parent.parent/'sitemap.xml').write_text(out)
print('sitemap:', out.count('<url>'), 'urls')
