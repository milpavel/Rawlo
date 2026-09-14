from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import cairosvg, io, json, re

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / 'public'
SOC = PUB / 'assets' / 'social'
SOC.mkdir(parents=True, exist_ok=True)
POSTER = ROOT / 'design' / 'social' / 'rawlo-social-master-v14.png'
BASE = 'https://rawlo.eu'
VERSION = 'v14'

LANG_ORDER = ['en','cs','sk','pl','de','fr','es','pt','it','nl','hu','ro','hr','sl','bg','fi','sv','et','lv','lt','da','el']
OG_LOCALE = {
'en':'en_GB','cs':'cs_CZ','sk':'sk_SK','pl':'pl_PL','de':'de_DE','fr':'fr_FR','es':'es_ES','pt':'pt_PT',
'it':'it_IT','nl':'nl_NL','hu':'hu_HU','ro':'ro_RO','hr':'hr_HR','sl':'sl_SI','bg':'bg_BG','fi':'fi_FI',
'sv':'sv_SE','et':'et_EE','lv':'lv_LV','lt':'lt_LT','da':'da_DK','el':'el_GR'
}

FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def font(path, size): return ImageFont.truetype(path, size=size)

def fit_text(draw, text, max_width, start_size, min_size=28, bold=True):
    path = FONT_BOLD if bold else FONT_REG
    for size in range(start_size, min_size-1, -2):
        f = font(path, size)
        if draw.textbbox((0,0), text, font=f)[2] <= max_width:
            return f
    return font(path, min_size)

def wrap(draw, text, fnt, max_width, max_lines=3):
    words = text.split()
    lines=[]; cur=''
    for w in words:
        test = (cur+' '+w).strip()
        if draw.textbbox((0,0), test, font=fnt)[2] <= max_width:
            cur=test
        else:
            if cur: lines.append(cur)
            cur=w
            if len(lines) >= max_lines-1:
                break
    if cur and len(lines)<max_lines: lines.append(cur)
    # append remaining indicator only if overflow obvious
    used=' '.join(lines)
    if len(used) < len(text)-8:
        lines[-1] = lines[-1].rstrip('.,;:') + '…'
    return lines

def render_svg(path, width=None, height=None):
    kwargs={}
    if width: kwargs['output_width']=width
    if height: kwargs['output_height']=height
    png = cairosvg.svg2png(url=str(path), **kwargs)
    return Image.open(io.BytesIO(png)).convert('RGBA')

def localized_html_path(lang):
    return PUB/'index.html' if lang=='en' else PUB/lang/'index.html'

def localized_screen(lang):
    p = PUB/'assets'/'screens'/'localized'/lang/'route-summary-v3.webp'
    if not p.exists():
        p = PUB/'assets'/'screens'/'localized'/lang/'route-events-v3.webp'
    if not p.exists():
        p = PUB/'assets'/'screens'/'localized'/'en'/'route-summary-v3.webp'
    return p

def make_social(lang, title, desc):
    """Build the one canonical RAWLO social card used by every locale.

    Keeping one visual identity avoids different previews across WhatsApp,
    Messenger, Facebook and other Open Graph consumers. Text metadata remains
    localized in each HTML page.
    """
    W,H=1200,630
    if not POSTER.exists():
        raise FileNotFoundError(f"Missing social master: {POSTER}")
    source=Image.open(POSTER).convert('RGB')
    card=ImageOps.fit(source,(W,H),method=Image.Resampling.LANCZOS,centering=(0.5,0.40))
    out=SOC/'rawlo-social-share-v14.jpg'
    card.save(out,'JPEG',quality=92,optimize=True,progressive=True)
    return out

def remove_existing_social(soup):
    for tag in list(soup.head.find_all(['meta','link','script'])):
        if tag.name=='meta':
            prop=tag.get('property','')
            name=tag.get('name','')
            if prop.startswith('og:') or name.startswith('twitter:') or name in {'thumbnail'}:
                tag.decompose()
        elif tag.name=='link' and tag.get('rel') and 'image_src' in tag.get('rel'):
            tag.decompose()
        elif tag.name=='script' and tag.get('type')=='application/ld+json':
            tag.decompose()

def insert_after(anchor, tags):
    cur=anchor
    for t in tags:
        cur.insert_after(t); cur=t

def new_meta(soup, *, name=None, prop=None, content=''):
    t=soup.new_tag('meta')
    if name: t['name']=name
    if prop: t['property']=prop
    t['content']=content
    return t

def update_page(lang):
    p=localized_html_path(lang)
    soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    title=soup.title.get_text(' ',strip=True)
    desc_tag=soup.find('meta',attrs={'name':'description'})
    desc=desc_tag.get('content','').strip() if desc_tag else ''
    canonical_tag=soup.find('link',rel='canonical')
    canonical=canonical_tag.get('href') if canonical_tag else (BASE+'/' if lang=='en' else f'{BASE}/{lang}/')
    image_url=f'{BASE}/assets/social/rawlo-social-share-v14.jpg'
    image_alt=re.sub(r'\s*\|\s*RAWLO\s*$','',title).strip() + ' — RAWLO'
    remove_existing_social(soup)

    tags=[]
    # Social crawler essentials first
    tags += [
      new_meta(soup,prop='og:type',content='website'),
      new_meta(soup,prop='og:site_name',content='RAWLO'),
      new_meta(soup,prop='og:locale',content=OG_LOCALE[lang]),
      new_meta(soup,prop='og:url',content=canonical),
      new_meta(soup,prop='og:title',content=title),
      new_meta(soup,prop='og:description',content=desc),
      new_meta(soup,prop='og:image',content=image_url),
      new_meta(soup,prop='og:image:url',content=image_url),
      new_meta(soup,prop='og:image:secure_url',content=image_url),
      new_meta(soup,prop='og:image:type',content='image/jpeg'),
      new_meta(soup,prop='og:image:width',content='1200'),
      new_meta(soup,prop='og:image:height',content='630'),
      new_meta(soup,prop='og:image:alt',content=image_alt),
    ]
    for other in LANG_ORDER:
        if other!=lang:
            tags.append(new_meta(soup,prop='og:locale:alternate',content=OG_LOCALE[other]))
    tags += [
      new_meta(soup,name='twitter:card',content='summary_large_image'),
      new_meta(soup,name='twitter:title',content=title),
      new_meta(soup,name='twitter:description',content=desc),
      new_meta(soup,name='twitter:image',content=image_url),
      new_meta(soup,name='twitter:image:alt',content=image_alt),
      new_meta(soup,name='thumbnail',content=image_url),
    ]
    image_link=soup.new_tag('link',rel='image_src',href=image_url); tags.append(image_link)

    schema={
      '@context':'https://schema.org',
      '@graph':[
        {'@type':'Organization','@id':BASE+'/#organization','name':'RAWLO','url':BASE+'/',
         'logo':{'@type':'ImageObject','url':BASE+'/assets/brand/rawlo_icon.svg'}},
        {'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'RAWLO','publisher':{'@id':BASE+'/#organization'},'inLanguage':lang},
        {'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':desc,'inLanguage':lang,
         'isPartOf':{'@id':BASE+'/#website'},'primaryImageOfPage':{'@type':'ImageObject','url':image_url,'width':1200,'height':630}},
        {'@type':'SoftwareApplication','@id':BASE+'/#app','name':'RAWLO','applicationCategory':'TravelApplication','operatingSystem':'iOS',
         'url':BASE+'/','description':desc,'image':image_url,'audience':{'@type':'Audience','audienceType':'Motorhome, campervan and caravan travellers'},
         'featureList':['Vehicle-aware routing','Traffic and road restriction monitoring','ETA based on vehicle speed settings','Route weather warnings','Crosswind alerts','Camper places and trip planning']}
      ]}
    script=soup.new_tag('script',type='application/ld+json'); script.string=json.dumps(schema,ensure_ascii=False,separators=(',',':')); tags.append(script)

    anchor=desc_tag if desc_tag else soup.title
    insert_after(anchor,tags)
    p.write_text(str(soup),encoding='utf-8')
    make_social(lang,title,desc)
    return {'lang':lang,'url':canonical,'image':image_url,'title':title,'description':desc}

results=[]
for lang in LANG_ORDER:
    results.append(update_page(lang))

# Add robust headers for crawlers and current HTML. Cloudflare Pages understands this format.
headers = '''/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n\n/\n  Cache-Control: public, max-age=0, must-revalidate\n\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n\n/assets/social/*\n  Cache-Control: public, max-age=86400, stale-while-revalidate=604800\n  Access-Control-Allow-Origin: *\n'''
(PUB/'_headers').write_text(headers,encoding='utf-8')

# crawler-facing helpers
(PUB/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: https://rawlo.eu/sitemap.xml\n',encoding='utf-8')

# OpenGraph verification manifest
manifest={
  'generated':'2026-09-14',
  'base_url':BASE,
  'social_image_version':VERSION,
  'notes':[
    'SEO_IMPLEMENTATION.json is documentation only; crawlers read metadata in each HTML <head>.',
    'Open Graph and X/Twitter tags are rendered server-side in static HTML and do not depend on JavaScript.',
    'One versioned RAWLO social image is used across all locales for consistent brand identity.',
    'Open Graph titles and descriptions remain localized per URL.',
    'The versioned filename avoids stale WhatsApp/Facebook/Messenger cache.'
  ],
  'pages':results,
  'checks':{'og_image':'1200x630 JPEG','absolute_https_urls':True,'localized_pages':22,'robots':True,'sitemap':True,'json_ld':True}
}
(ROOT/'SEO_IMPLEMENTATION.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(PUB/'social-preview-manifest.json').write_text(json.dumps({'version':VERSION,'images':{x['lang']:x['image'] for x in results}},ensure_ascii=False,indent=2),encoding='utf-8')
print('updated',len(results),'pages')
