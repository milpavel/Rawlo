"""RAWLO v15: dependency-free, multilingual static site generator."""
from pathlib import Path
from html import escape
import json
from current_copy import COPY, SERVICES
ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / 'public'
CAT = json.loads((ROOT/'scripts/legacy-translations.json').read_text())
LANGS, LOCALES, OLD = CAT['languages'], CAT['locales'], CAT['translations']
ASSETS = '/assets/current-20261012/'
E = escape
ICONS = {
 'onroad':'<path d="M7 3h10l3 18H4L7 3Z"/><path d="M12 4v4m0 4v3m0 4v2"/>',
 'planner':'<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M7 3v4m10-4v4M3 11h18m-13 5h2m4 0h2"/>',
 'navigation':'<path d="m12 3 8 18-8-5-8 5 8-18Z"/>',
 'map':'<path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3V6Z"/><path d="M9 3v15m6-12v15"/>',
 'community':'<circle cx="9" cy="8" r="3"/><path d="M3 21v-3a6 6 0 0 1 12 0v3M17 5a3 3 0 0 1 0 6m1 4a5 5 0 0 1 3 5"/>',
 'profile':'<circle cx="12" cy="8" r="4"/><path d="M4 21v-2a8 8 0 0 1 16 0v2"/>',
 'weather':'<path d="M5 18a4 4 0 0 1 0-8 6 6 0 0 1 11-1 4.5 4.5 0 0 1 2 9H5Z"/><path d="M19 3v2m3 1-2 1"/>',
 'shield':'<path d="m12 3 8 3v6c0 4-4 8-8 10-4-2-8-6-8-10V6l8-3Z"/><path d="m8 12 3 3 5-6"/>',
 'arrow':'<path d="M4 12h16m-6-6 6 6-6 6"/>',
 'mobile':'<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M10 5h4m-3 14h2"/>',
 'ferry':'<path d="M4 13h16l-3 6H7l-3-6Zm4 0V7h8v6m-6-6V4h4v3M3 22c2-2 4-2 6 0s4 2 6 0 4-2 6 0"/>',
}
def icon(name):
 return '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'+ICONS[name]+'</svg>'
def url(code): return '/' if code=='en' else f'/{code}/'
def phone(name,label,cls='',eager=False):
 priority = 'fetchpriority="high"' if eager else ''
 return f'<div class="phone {cls}"><img src="{ASSETS}{name}.png" width="944" height="2048" alt="{E(label)} — RAWLO" loading="{"eager" if eager else "lazy"}" decoding="async" {priority}></div>'
def page(code):
 c,t=COPY[code],OLD[code].copy(); labels=dict(c,planner=t['nav_planner'])
 # The retired catalog inherited English paragraphs in 20 languages.
 # Only use its genuinely localized headings and route intelligence copy.
 if code not in ('en','cs'):
  t.update(safety_t=c['navigation'],places_t=c['map'],preview_t=t['nav_preview'],services_t=c['onroad'],closing_t=t['hero_sub'])
 sections=[('navigation','navigation','navbody',t['safety_t']),('planner','itinerary','planbody',t['share_t']),('map','map','mapbody',t['places_t']),('community','community','communitybody',c['community'])]
 nav=''.join(f'<a href="#{name}">{E(labels[name])}</a>' for name in ['planner','navigation','community'])+f'<a href="#europe">{E(t["nav_europe"])}</a>'
 options=''.join(f'<option value="{key}" {"selected" if key==code else ""}>{LOCALES[key][0]} {E(value)}</option>' for key,value in LANGS.items())
 journey=''.join(f'<a class="journey-card" href="#{name}"><span class="icon">{icon(name)}</span><strong>{E(labels[name])}</strong><span class="card-arrow">↗</span></a>' for name in ['onroad','planner','navigation','map','community'])
 countries=''.join(f'<a class="europe-lang-card {"active" if key==code else ""}" href="{url(key)}" hreflang="{key}" data-language="{key}"><span class="europe-flag" aria-hidden="true">{LOCALES[key][0]}</span><span><strong>{E(name)}</strong><small>{E(LOCALES[key][1])}</small></span><span class="country-arrow">↗</span></a>' for key,name in LANGS.items())
 blocks=[]
 for i,(name,image,body,title) in enumerate(sections):
  extra=''
  if name=='navigation': extra='<div class="detail-grid">'+''.join(f'<article>{icon(ico)}<h3>{E(t[heading])}</h3><p>{E(t[desc])}</p></article>' for ico,heading,desc in [('weather','wx_t','wx_b'),('shield','traffic_t','traffic_b')])+'</div>'
  if name=='planner': extra='<div class="route-line"><span>01</span><i></i><span>02</span><i></i><span>03</span><i></i>'+icon('navigation')+'</div>'
  if name=='community': extra='<div class="community-symbols">'+icon('community')+icon('map')+icon('planner')+'</div>'
  companion={'planner':'planner','map':'map-clusters','community':'topics'}.get(name)
  art=phone(companion,labels[name],'phone-back') if companion else ''
  art+=phone(image,labels[name],'phone-front' if companion else '')
  blocks.append(f'<section class="section feature-section {name}-section" id="{name}"><div class="wrap feature-split {"reversed" if i%2 else ""}"><div class="copy"><span class="kicker">0{i+1} / {E(labels[name])}</span><h2>{E(title)}</h2><p>{E(c[body])}</p>{extra}<a class="text-link" href="#preview" data-show-category="{name}">{E(t["nav_preview"])} ↗</a></div><div class="feature-art {name}-art">{art}<span class="art-label">{icon(name)} {"Mapbox × RAWLO" if name=="navigation" else "RAWLO · "+E(labels[name])}</span></div></div></section>')
 filters=''.join(f'<button type="button" data-filter="{key}" aria-pressed="{"true" if key=="all" else "false"}">{E(c["all"] if key=="all" else labels[key])}</button>' for key in ['all','navigation','planner','map','community','onroad','profile'])
 shots=[('navigation','navigation'),('planner','planner'),('itinerary','planner'),('stops','planner'),('map','map'),('map-clusters','map'),('community','community'),('topics','community'),('on-the-road','onroad'),('vignettes','onroad'),('profile','profile'),('settings','profile')]
 gallery=''.join(f'<figure data-category="{category}"><button type="button" class="shot-button" data-shot="{ASSETS}{file}.png" data-caption="{E(labels[category])}" aria-label="{E(labels[category])} — RAWLO">{phone(file,labels[category])}<span class="zoom-icon" aria-hidden="true">↗</span></button><figcaption><span>{i+1:02}</span>{E(labels[category])}</figcaption></figure>' for i,(file,category) in enumerate(shots))
 services=''
 for i,index in enumerate([0,2,1,3]):
  status=f'<span class="service-status">{E(c["test"] if index==2 else c["soon"])}</span>' if index else f'<a class="text-link" href="#preview" data-show-category="onroad">{E(t["nav_preview"])} ↗</a>'
  services+=f'<article class="service-card"><span class="service-count">0{i+1}</span>{icon(["onroad","mobile","ferry","shield"][i])}<h3>{E(SERVICES[code].split("|")[i])}</h3>{status}</article>'
 alternates=''.join(f'<link rel="alternate" hreflang="{key}" href="https://rawlo.eu{url(key)}">' for key in LANGS)+'<link rel="alternate" hreflang="x-default" href="https://rawlo.eu/">'
 schema=json.dumps({'@context':'https://schema.org','@type':'WebSite','name':'RAWLO','url':'https://rawlo.eu/','inLanguage':code,'description':c['intro']},ensure_ascii=False).replace('<','\\u003c')
 detect='<script src="/assets/detect-v15.js"></script>' if code=='en' else ''
 return f'''<!doctype html><html lang="{code}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RAWLO — {E(t['hero_title'])}</title><meta name="description" content="{E(c['intro'])}"><meta name="theme-color" content="#111417"><link rel="canonical" href="https://rawlo.eu{url(code)}">{alternates}<link rel="icon" type="image/svg+xml" href="/assets/brand/rawlo_icon.svg">
<meta property="og:type" content="website"><meta property="og:site_name" content="RAWLO"><meta property="og:title" content="RAWLO — {E(t['hero_title'])}"><meta property="og:description" content="{E(c['intro'])}"><meta property="og:url" content="https://rawlo.eu{url(code)}"><meta property="og:image" content="https://rawlo.eu{ASSETS}alpine-journey.png"><meta property="og:image:alt" content="RAWLO — {E(t['eyebrow'])}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="RAWLO — {E(t['hero_title'])}"><meta name="twitter:description" content="{E(c['intro'])}"><meta name="twitter:image" content="https://rawlo.eu{ASSETS}alpine-journey.png"><link rel="stylesheet" href="/assets/styles-v15.css">{detect}<script type="application/ld+json">{schema}</script></head>
<body><a class="skip" href="#main">{E(t['nav_features'])} ↓</a><header class="site-header"><a class="brand" href="{url(code)}" aria-label="RAWLO"><img src="/assets/brand/rawlo_logo_white.svg" width="449" height="130" alt="RAWLO"></a><nav class="main-nav" id="main-nav" aria-label="RAWLO">{nav}</nav><div class="header-actions"><label class="language-label"><span class="sr-only">{E(t['nav_europe'])}</span><select data-language-select aria-label="{E(t['nav_europe'])}">{options}</select></label><a href="#preview" class="button small">{E(t['nav_preview'])}</a><button class="menu-toggle" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Menu"><span></span><span></span></button></div></header>
<main id="main"><section class="hero"><img class="hero-landscape" src="{ASSETS}alpine-journey.png" width="1672" height="941" alt="" fetchpriority="high"><div class="hero-shade"></div><div class="hero-layout wrap"><div class="hero-copy"><span class="eyebrow"><i></i>{E(t['eyebrow'])}</span><h1>{E(t['hero_title'])}</h1><p class="hero-sub">{E(t['hero_sub'])}</p><p class="lede">{E(c['intro'])}</p><div class="hero-actions"><a class="button" href="#preview">{E(t['nav_preview'])}{icon('arrow')}</a><a class="text-link" href="#journey">{E(t['nav_features'])} ↗</a></div><p class="build-note"><span class="status-dot"></span>{E(c['build'])}</p></div><div class="hero-phones">{phone('map',c['map'],'hero-back',True)}{phone('navigation',c['navigation'],'hero-main',True)}<span class="phone-caption">RAWLO · {E(c['navigation'])}</span></div></div><div class="hero-bottom wrap"><span>KNOW WHAT’S <b>AHEAD.</b></span><a href="#journey">{E(t['nav_features'])} ↓</a></div></section>
<section class="journey wrap" id="journey"><div class="section-caption"><span>RAWLO</span><span>01 / 05</span></div><div class="journey-grid">{journey}</div></section>{''.join(blocks)}
<section class="section wrap" id="onroad"><div class="section-heading"><div><span class="kicker">05 / {E(c['onroad'])}</span><h2>{E(t['services_t'])}</h2></div><p>{E(c['servicebody'])}</p></div><div class="service-layout"><div class="service-grid">{services}</div>{phone('on-the-road',c['onroad'])}</div></section>
<section class="profile-section wrap" id="profile"><img src="/assets/brand/rawlo_icon.svg" width="76" height="90" alt=""><div><span class="kicker">RAWLO / {E(c['profile'])}</span><h2>{E(c['profile'])}</h2><p>{E(c['profilebody'])}</p></div><a class="text-link" href="#preview" data-show-category="profile">{E(t['nav_preview'])} ↗</a></section>
<section class="section europe" id="europe"><div class="europe-orbit"></div><div class="wrap"><div class="section-heading"><div><span class="kicker">{E(t['europe_k'])}</span><h2>{E(t['europe_t'])}</h2></div><span class="language-count">22<span>{E(t['nav_europe'])}</span></span></div><div class="europe-lang-grid">{countries}</div></div></section>
<section class="section wrap preview" id="preview"><div class="section-heading"><div><span class="kicker">RAWLO / {E(t['nav_preview'])}</span><h2>{E(t['preview_t'])}</h2><p>{E(c['screens'])}</p></div><div class="gallery-arrows"><button type="button" data-gallery-prev aria-label="{E(c['previous'])}">←</button><button type="button" data-gallery-next aria-label="{E(c['next'])}">→</button></div></div><div class="gallery-filters">{filters}</div><div class="gallery" tabindex="0" aria-label="{E(t['nav_preview'])}">{gallery}</div></section>
<section class="closing"><div class="wrap"><span class="kicker">KNOW WHAT’S AHEAD.</span><h2>{E(t['closing_t'])}</h2><p>{E(c['build'])}</p><a href="mailto:support@rawlo.eu" class="button">{E(c['contact'])}{icon('arrow')}</a></div></section></main>
<footer class="wrap"><a class="brand" href="{url(code)}"><img src="/assets/brand/rawlo_logo_white.svg" width="449" height="130" alt="RAWLO"></a><span>© 2026 RAWLO</span><a href="mailto:support@rawlo.eu">support@rawlo.eu</a><a href="#europe">{LOCALES[code][0]} {E(LANGS[code])}</a></footer><dialog class="lightbox" aria-label="{E(t['nav_preview'])}"><div class="lightbox-header"><span data-lightbox-caption></span><button type="button" data-lightbox-close>{E(c['close'])} ×</button></div><img data-lightbox-image alt="" width="944" height="2048"></dialog><script src="/assets/app-v15.js" defer></script></body></html>'''
def build():
 if set(COPY)!=set(LANGS): raise ValueError('Language catalog incomplete')
 for code in LANGS:
  dest=PUB/('index.html' if code=='en' else f'{code}/index.html');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(page(code),encoding='utf-8')
 (PUB/'en/index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/"><link rel="canonical" href="https://rawlo.eu/"><title>RAWLO</title></head><body><a href="/">RAWLO</a></body></html>')
 (PUB/'i18n-manifest.json').write_text(json.dumps({'languages':LANGS},ensure_ascii=False,indent=2))
 (PUB/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://rawlo.eu/sitemap.xml\n')
 (PUB/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>https://rawlo.eu{url(code)}</loc></url>' for code in LANGS)+'</urlset>')
 (PUB/'social-preview-manifest.json').write_text(json.dumps({'image':'https://rawlo.eu'+ASSETS+'alpine-journey.png','version':'20261012'},indent=2))
 print(f'RAWLO v15: {len(LANGS)} languages, 12 current screenshots.')
if __name__=='__main__': build()
