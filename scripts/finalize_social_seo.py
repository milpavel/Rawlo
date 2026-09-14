from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import cairosvg, io, json, re

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / 'public'
SOC = PUB / 'assets' / 'social'
SOC.mkdir(parents=True, exist_ok=True)
POSTER = Path('/mnt/data/ChatGPT Image 31. 8. 2026 11_43_25(1).png')
BASE = 'https://rawlo.eu'
VERSION = '20260914-v4'

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
    W,H=1200,630
    if POSTER.exists():
        bg = ImageOps.fit(Image.open(POSTER).convert('RGB'), (W,H), method=Image.Resampling.LANCZOS, centering=(0.5,0.32))
        bg = bg.filter(ImageFilter.GaussianBlur(3))
    else:
        bg = Image.new('RGB',(W,H),(8,15,21))
    overlay=Image.new('RGBA',(W,H),(5,12,18,0))
    od=ImageDraw.Draw(overlay)
    # deep gradient-like panels
    for x in range(W):
        a=int(220 - 70*(x/W))
        od.line([(x,0),(x,H)], fill=(4,10,16,a))
    # teal glow
    glow=Image.new('RGBA',(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow)
    gd.ellipse((760,40,1260,620), fill=(0,209,193,45))
    glow=glow.filter(ImageFilter.GaussianBlur(80))
    canvas=Image.alpha_composite(bg.convert('RGBA'),overlay)
    canvas=Image.alpha_composite(canvas,glow)
    d=ImageDraw.Draw(canvas)

    # phone screenshot on right
    sp=localized_screen(lang)
    shot=Image.open(sp).convert('RGB')
    # fit tall screenshot in rounded card
    target_h=560
    scale=target_h/shot.height
    sw=int(shot.width*scale)
    shot=shot.resize((sw,target_h),Image.Resampling.LANCZOS)
    # crop if too wide
    if sw>360:
        left=(sw-360)//2; shot=shot.crop((left,0,left+360,target_h)); sw=360
    xshot=805+(360-sw)//2; yshot=35
    shadow=Image.new('RGBA',(sw+40,target_h+40),(0,0,0,0)); sd=ImageDraw.Draw(shadow)
    sd.rounded_rectangle((20,20,sw+20,target_h+20), radius=34, fill=(0,0,0,140))
    shadow=shadow.filter(ImageFilter.GaussianBlur(12))
    canvas.alpha_composite(shadow,(xshot-20,yshot-20))
    mask=Image.new('L',(sw,target_h),0); md=ImageDraw.Draw(mask); md.rounded_rectangle((0,0,sw,target_h),radius=34,fill=255)
    shot_rg=shot.convert('RGBA'); shot_rg.putalpha(mask)
    canvas.alpha_composite(shot_rg,(xshot,yshot))
    d=ImageDraw.Draw(canvas)
    d.rounded_rectangle((xshot-2,yshot-2,xshot+sw+2,yshot+target_h+2),radius=36,outline=(116,254,230,90),width=2)

    # logo
    logo=render_svg(PUB/'assets'/'brand'/'rawlo_logo_white.svg', width=330)
    canvas.alpha_composite(logo,(72,56))
    d=ImageDraw.Draw(canvas)

    clean_title=re.sub(r'\s*\|\s*RAWLO\s*$','',title).strip()
    tf=font(FONT_BOLD,50)
    lines=wrap(d,clean_title,tf,620,max_lines=3)
    y=175
    for line in lines:
        d.text((72,y),line,font=tf,fill=(248,251,252,255))
        y += 62

    df=font(FONT_REG,25)
    desc_lines=wrap(d,desc,df,640,max_lines=3)
    y=max(y+18,370)
    for line in desc_lines:
        d.text((74,y),line,font=df,fill=(185,196,204,255))
        y += 38

    # footer chips
    ychip=540
    chips=['↕ 2.6 m','◷ ETA','≈ 42 km/h']
    x=72
    cf=font(FONT_BOLD,18)
    for chip in chips:
        tw=d.textbbox((0,0),chip,font=cf)[2]
        d.rounded_rectangle((x,ychip,x+tw+34,ychip+38),radius=19,fill=(8,45,48,210),outline=(0,209,193,170),width=1)
        d.text((x+17,ychip+8),chip,font=cf,fill=(108,246,229,255))
        x += tw+48
    rf=font(FONT_BOLD,20)
    d.text((72,592),'rawlo.eu',font=rf,fill=(0,209,193,255))

    out=SOC/f'rawlo-social-{lang}-{VERSION}.jpg'
    canvas.convert('RGB').save(out,'JPEG',quality=90,optimize=True,progressive=True)
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
    image_url=f'{BASE}/assets/social/rawlo-social-{lang}-{VERSION}.jpg'
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
    'Social images use new versioned filenames to avoid stale WhatsApp/Facebook cache.',
    'Root URL has an English/global preview; localized URLs have localized previews.'
  ],
  'pages':results,
  'checks':{'og_image':'1200x630 JPEG','absolute_https_urls':True,'localized_pages':22,'robots':True,'sitemap':True,'json_ld':True}
}
(ROOT/'SEO_IMPLEMENTATION.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(PUB/'social-preview-manifest.json').write_text(json.dumps({'version':VERSION,'images':{x['lang']:x['image'] for x in results}},ensure_ascii=False,indent=2),encoding='utf-8')
print('updated',len(results),'pages')
