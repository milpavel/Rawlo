from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cairosvg, io, json, html
from datetime import date

ROOT=Path(__file__).resolve().parents[1]; PUB=ROOT/'public'; BASE='https://rawlo.eu'
META={
'en':('Camper Navigation & Trip Planner for Europe | RAWLO','Navigation and trip planning for motorhomes, campervans and caravans. RAWLO checks vehicle restrictions, traffic, ETA, route weather and crosswinds across Europe.','Camper navigation built around your vehicle.','Vehicle-aware routes · traffic · ETA · weather · camper places'),
'cs':('Navigace pro obytná auta a karavany v Evropě | RAWLO','Navigace a plánování cest pro obytná auta, obytné dodávky a karavany. RAWLO hlídá omezení dle rozměrů vozidla, dopravu, ETA, počasí i boční vítr.','Navigace vytvořená pro vaše obytné auto.','Rozměry vozidla · doprava · ETA · počasí · camper místa'),
'sk':('Navigácia pre obytné autá a karavany | RAWLO','Navigácia a plánovanie ciest pre obytné autá, campervany a karavany. RAWLO sleduje obmedzenia vozidla, dopravu, ETA, počasie na trase aj bočný vietor.','Navigácia vytvorená pre váš camper.','Rozmery vozidla · doprava · ETA · počasie · camper miesta'),
'pl':('Nawigacja dla kamperów i przyczep w Europie | RAWLO','Nawigacja i planowanie podróży dla kamperów, campervanów i przyczep. RAWLO uwzględnia wymiary pojazdu, ruch, ETA, pogodę na trasie i boczny wiatr.','Nawigacja stworzona dla Twojego kampera.','Wymiary pojazdu · ruch · ETA · pogoda · miejsca dla kamperów'),
'de':('Wohnmobil Navigation & Routenplaner Europa | RAWLO','Navigation und Reiseplanung für Wohnmobile, Campervans und Wohnwagen. RAWLO berücksichtigt Fahrzeugmaße, Verkehr, ETA, Streckenwetter und Seitenwind.','Navigation, die dein Wohnmobil versteht.','Fahrzeugmaße · Verkehr · ETA · Wetter · Stellplätze'),
'fr':('Navigation camping-car & itinéraires Europe | RAWLO','Navigation et planification pour camping-cars, vans aménagés et caravanes. RAWLO tient compte du gabarit, du trafic, de l’ETA, de la météo et du vent latéral.','La navigation pensée pour votre camping-car.','Gabarit · trafic · ETA · météo · aires camping-car'),
'es':('Navegación para autocaravanas en Europa | RAWLO','Navegación y planificación para autocaravanas, campers y caravanas. RAWLO considera dimensiones, tráfico, ETA, tiempo en ruta y viento lateral.','Navegación pensada para tu autocaravana.','Dimensiones · tráfico · ETA · tiempo · áreas camper'),
'pt':('Navegação para autocaravanas na Europa | RAWLO','Navegação e planeamento para autocaravanas, campervans e caravanas. RAWLO considera dimensões, trânsito, ETA, meteorologia na rota e vento lateral.','Navegação criada para a sua autocaravana.','Dimensões · trânsito · ETA · meteorologia · áreas camper'),
'it':('Navigazione camper e itinerari in Europa | RAWLO','Navigazione e pianificazione per camper, van e caravan. RAWLO considera dimensioni del veicolo, traffico, ETA, meteo lungo il percorso e vento laterale.','La navigazione pensata per il tuo camper.','Dimensioni · traffico · ETA · meteo · aree camper'),
'nl':('Campernavigatie & routeplanner voor Europa | RAWLO','Navigatie en reisplanning voor campers, campervans en caravans. RAWLO houdt rekening met voertuigafmetingen, verkeer, ETA, routeweer en zijwind.','Navigatie die jouw camper begrijpt.','Voertuigafmetingen · verkeer · ETA · weer · camperplaatsen'),
'hu':('Lakóautó navigáció és útvonaltervező | RAWLO','Navigáció és utazástervezés lakóautókhoz, campervanokhoz és lakókocsikhoz. RAWLO figyeli a járműméretet, forgalmat, ETA-t, útvonali időjárást és oldalszelet.','Navigáció, amely ismeri a lakóautódat.','Járműméret · forgalom · ETA · időjárás · lakóautóhelyek'),
'ro':('Navigație pentru autorulote în Europa | RAWLO','Navigație și planificare pentru autorulote, campervan-uri și rulote. RAWLO ține cont de dimensiuni, trafic, ETA, vremea pe traseu și vântul lateral.','Navigație creată pentru autorulota ta.','Dimensiuni · trafic · ETA · vreme · locuri pentru autorulote'),
'hr':('Navigacija za kampere i autodomove | RAWLO','Navigacija i planiranje putovanja za autodomove, campervane i kamp-prikolice. RAWLO prati dimenzije vozila, promet, ETA, vrijeme na ruti i bočni vjetar.','Navigacija napravljena za vaš kamper.','Dimenzije · promet · ETA · vrijeme · camper mjesta'),
'sl':('Navigacija za avtodome in prikolice | RAWLO','Navigacija in načrtovanje poti za avtodome, campervane in prikolice. RAWLO upošteva mere vozila, promet, ETA, vreme na poti in bočni veter.','Navigacija, ustvarjena za vaš avtodom.','Mere vozila · promet · ETA · vreme · postajališča'),
'bg':('Навигация за кемпери и каравани в Европа | RAWLO','Навигация и планиране за кемпери, кемперванове и каравани. RAWLO отчита размерите, трафика, ETA, времето по маршрута и страничния вятър.','Навигация, създадена за вашия кемпер.','Размери · трафик · ETA · време · места за кемпери'),
'fi':('Matkailuauton navigointi ja reittisuunnittelu | RAWLO','Navigointi ja matkojen suunnittelu matkailuautoille, campervaneille ja asuntovaunuille. RAWLO huomioi ajoneuvon mitat, liikenteen, ETA:n, reittisään ja sivutuulen.','Navigointi, joka tuntee matkailuautosi.','Ajoneuvon mitat · liikenne · ETA · sää · camper-paikat'),
'sv':('Husbilsnavigering & ruttplanerare i Europa | RAWLO','Navigering och reseplanering för husbilar, campervans och husvagnar. RAWLO tar hänsyn till fordonsmått, trafik, ETA, väder längs rutten och sidvind.','Navigering byggd för din husbil.','Fordonsmått · trafik · ETA · väder · ställplatser'),
'et':('Matkaauto navigatsioon ja marsruudiplaneerija | RAWLO','Navigatsioon ja reisiplaneerimine matkaautodele, campervanidele ja haagissuvilatele. RAWLO arvestab mõõte, liiklust, ETA-d, marsruudi ilma ja külgtuult.','Navigatsioon, mis tunneb sinu matkaautot.','Sõiduki mõõdud · liiklus · ETA · ilm · matkaautokohad'),
'lv':('Kempera navigācija un maršrutu plānotājs | RAWLO','Navigācija un ceļojumu plānošana kemperiem, campervaniem un treileriem. RAWLO ņem vērā izmērus, satiksmi, ETA, laikapstākļus maršrutā un sānvēju.','Navigācija, kas pazīst jūsu kemperi.','Izmēri · satiksme · ETA · laikapstākļi · kemperu vietas'),
'lt':('Kemperių navigacija ir maršrutų planavimas | RAWLO','Navigacija ir kelionių planavimas kemperiams, campervanams ir priekaboms. RAWLO vertina matmenis, eismą, ETA, orus maršrute ir šoninį vėją.','Navigacija, kuri pažįsta jūsų kemperį.','Matmenys · eismas · ETA · orai · kemperių vietos'),
'da':('Autocamper navigation & ruteplanlægger | RAWLO','Navigation og rejseplanlægning til autocampere, campervans og campingvogne. RAWLO tager højde for køretøjets mål, trafik, ETA, rutevejr og sidevind.','Navigation bygget til din autocamper.','Køretøjsmål · trafik · ETA · vejr · autocamperpladser'),
'el':('Πλοήγηση για camper και τροχόσπιτα | RAWLO','Πλοήγηση και σχεδιασμός ταξιδιού για αυτοκινούμενα, campervan και τροχόσπιτα. Το RAWLO λαμβάνει υπόψη διαστάσεις, κίνηση, ETA, καιρό διαδρομής και πλευρικό άνεμο.','Πλοήγηση σχεδιασμένη για το camper σας.','Διαστάσεις · κίνηση · ETA · καιρός · θέσεις camper'),
}
LOCALES={'en':'en_GB','cs':'cs_CZ','sk':'sk_SK','pl':'pl_PL','de':'de_DE','fr':'fr_FR','es':'es_ES','pt':'pt_PT','it':'it_IT','nl':'nl_NL','hu':'hu_HU','ro':'ro_RO','hr':'hr_HR','sl':'sl_SI','bg':'bg_BG','fi':'fi_FI','sv':'sv_SE','et':'et_EE','lv':'lv_LV','lt':'lt_LT','da':'da_DK','el':'el_GR'}
# Country targeting reuses the best matching language URL without creating duplicate pages.
COUNTRY_HREF={'cs-CZ':'cs','sk-SK':'sk','pl-PL':'pl','de-DE':'de','de-AT':'de','fr-FR':'fr','fr-BE':'fr','fr-LU':'fr','nl-NL':'nl','nl-BE':'nl','hr-HR':'hr','ro-RO':'ro','hu-HU':'hu','sl-SI':'sl','bg-BG':'bg','fi-FI':'fi','et-EE':'et','lv-LV':'lv','es-ES':'es','pt-PT':'pt','lt-LT':'lt','da-DK':'da','el-GR':'el','sv-SE':'sv','it-IT':'it','en-IE':'en'}
KEYWORDS={
'en':'camper navigation, motorhome navigation, campervan route planner, caravan navigation, motorhome trip planner, camper places Europe, route weather camper',
'cs':'navigace pro obytná auta, navigace pro karavany, obytná dodávka navigace, plánovač cest karavanem, stellplatz Evropa, počasí na trase, camper aplikace',
'de':'Wohnmobil Navigation, Camper Navigation, Wohnwagen Navigation, Routenplaner Wohnmobil, Stellplätze Europa, Streckenwetter Wohnmobil',
'fr':'navigation camping-car, GPS camping-car, itinéraire camping-car, van aménagé, aire camping-car Europe, météo trajet camping-car',
'es':'navegación autocaravana, GPS camper, rutas autocaravana, áreas camper Europa, tiempo en ruta autocaravana',
'it':'navigazione camper, navigatore camper, itinerari camper, aree sosta camper Europa, meteo percorso camper',
'pl':'nawigacja kamper, nawigacja dla kamperów, planer trasy kamper, miejsca dla kamperów Europa, pogoda na trasie kampera',
}

def url_for(code): return BASE+'/' if code=='en' else f'{BASE}/{code}/'
def font(path,size): return ImageFont.truetype(path,size)
FONT='/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'; BOLD='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'

def fit(draw,text,maxw,start=58,minsize=34):
    for s in range(start,minsize-1,-2):
        f=font(BOLD,s)
        if draw.textbbox((0,0),text,font=f)[2] <= maxw: return f
    return font(BOLD,minsize)

def social_image(code):
    title,desc,headline,strap=META[code]
    im=Image.new('RGB',(1200,630),(9,15,20)); d=ImageDraw.Draw(im)
    # subtle teal glows
    glow=Image.new('RGBA',im.size,(0,0,0,0)); gd=ImageDraw.Draw(glow)
    gd.ellipse((760,-220,1350,370),fill=(0,210,196,55)); gd.ellipse((-250,420,450,1050),fill=(0,150,145,35)); glow=glow.filter(ImageFilter.GaussianBlur(90)); im=Image.alpha_composite(im.convert('RGBA'),glow); d=ImageDraw.Draw(im)
    # brand mark from SVG
    try:
        png=cairosvg.svg2png(url=str(PUB/'assets/brand/rawlo_logo_white.svg'),output_width=290)
        logo=Image.open(io.BytesIO(png)).convert('RGBA'); im.alpha_composite(logo,(64,58))
    except Exception:
        d.text((64,58),'RAWLO',font=font(BOLD,54),fill='white')
    d.rounded_rectangle((64,154,168,192),18,fill=(8,73,72)); d.text((85,163),'EUROPE',font=font(BOLD,17),fill=(0,222,207))
    hf=fit(d,headline,610,54,34); # wrap manually to 2 lines
    words=headline.split(); lines=[]; cur=''
    for w in words:
        test=(cur+' '+w).strip()
        if d.textbbox((0,0),test,font=hf)[2] > 610 and cur: lines.append(cur); cur=w
        else: cur=test
    if cur: lines.append(cur)
    y=220
    for line in lines[:3]: d.text((64,y),line,font=hf,fill='white'); y+=hf.size+10
    sf=font(FONT,25); sw=[]; cur=''
    for w in strap.split():
        test=(cur+' '+w).strip()
        if d.textbbox((0,0),test,font=sf)[2]>610 and cur: sw.append(cur); cur=w
        else: cur=test
    if cur: sw.append(cur)
    y+=14
    for line in sw[:2]: d.text((64,y),line,font=sf,fill=(160,172,181)); y+=35
    # phone screenshots
    for i,name in enumerate(['navigation.webp','weather.webp']):
        p=PUB/'assets/screens/localized'/code/name
        ph=Image.open(p).convert('RGBA'); ph.thumbnail((255,520),Image.Resampling.LANCZOS)
        x=785+i*190; yy=105 if i==0 else 145
        shadow=Image.new('RGBA',im.size,(0,0,0,0)); sd=ImageDraw.Draw(shadow); sd.rounded_rectangle((x-8,yy-8,x+ph.width+8,yy+ph.height+8),34,fill=(0,0,0,120)); shadow=shadow.filter(ImageFilter.GaussianBlur(14)); im=Image.alpha_composite(im,shadow); im.alpha_composite(ph,(x,yy))
    d=ImageDraw.Draw(im); d.text((64,566),'rawlo.app',font=font(BOLD,22),fill=(0,222,207)); d.text((1015,566),code.upper(),font=font(BOLD,18),fill=(130,142,150))
    out=PUB/'assets/social'; out.mkdir(exist_ok=True); im.convert('RGB').save(out/f'og-{code}.jpg',quality=91,optimize=True)

# Generate all localized social previews.
for code in META: social_image(code)

# hreflang set: language pages + regional country targeting + x-default.
alts=[('x-default',url_for('en'))]+[(c,url_for(c)) for c in META]+[(h,url_for(c)) for h,c in COUNTRY_HREF.items()]

for code in META:
    path=PUB/'index.html' if code=='en' else PUB/code/'index.html'
    soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser'); head=soup.head
    title,desc,headline,strap=META[code]; canonical=url_for(code); image=f'{BASE}/assets/social/og-{code}.jpg'
    soup.title.string=title
    # remove SEO/social tags and alternates to rebuild cleanly
    for tag in list(head.find_all(['meta','link'])):
        if tag.name=='meta' and (tag.get('name') in ['description','keywords','robots','author','twitter:card','twitter:title','twitter:description','twitter:image','twitter:image:alt'] or tag.get('property','').startswith('og:')): tag.decompose()
        elif tag.name=='link' and tag.get('rel') and ('canonical' in tag.get('rel') or 'alternate' in tag.get('rel')): tag.decompose()
    def meta(**attrs): head.append(soup.new_tag('meta',attrs=attrs))
    meta(name='description',content=desc); meta(name='keywords',content=KEYWORDS.get(code, f'RAWLO, camper navigation, motorhome navigation, campervan, caravan, route planner Europe'))
    meta(name='robots',content='index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1'); meta(name='author',content='RAWLO')
    can=soup.new_tag('link',rel='canonical',href=canonical); head.append(can)
    for h,u in alts: head.append(soup.new_tag('link',rel='alternate',hreflang=h,href=u))
    meta(property='og:type',content='website'); meta(property='og:site_name',content='RAWLO'); meta(property='og:locale',content=LOCALES[code]); meta(property='og:url',content=canonical); meta(property='og:title',content=title); meta(property='og:description',content=desc); meta(property='og:image',content=image); meta(property='og:image:secure_url',content=image); meta(property='og:image:type',content='image/jpeg'); meta(property='og:image:width',content='1200'); meta(property='og:image:height',content='630'); meta(property='og:image:alt',content=headline)
    for c,l in LOCALES.items():
        if c!=code: meta(property='og:locale:alternate',content=l)
    meta(name='twitter:card',content='summary_large_image'); meta(name='twitter:title',content=title); meta(name='twitter:description',content=desc); meta(name='twitter:image',content=image); meta(name='twitter:image:alt',content=headline)
    # structured data
    schema={"@context":"https://schema.org","@graph":[
      {"@type":"Organization","@id":BASE+"/#organization","name":"RAWLO","url":BASE+"/","logo":{"@type":"ImageObject","url":BASE+"/assets/brand/rawlo_icon.svg"}},
      {"@type":"WebSite","@id":BASE+"/#website","url":BASE+"/","name":"RAWLO","publisher":{"@id":BASE+"/#organization"},"inLanguage":code},
      {"@type":"SoftwareApplication","@id":BASE+"/#app","name":"RAWLO","applicationCategory":"TravelApplication","operatingSystem":"iOS","url":canonical,"description":desc,"isAccessibleForFree":False,"audience":{"@type":"Audience","audienceType":"Motorhome, campervan and caravan travellers"},"featureList":["Vehicle-aware routing","Traffic and road restriction monitoring","ETA based on vehicle speed settings","Route weather warnings","Crosswind alerts","Camper places and travel planning"]}
    ]}
    sc=soup.new_tag('script',type='application/ld+json'); sc.string=json.dumps(schema,ensure_ascii=False); head.append(sc)
    path.write_text(str(soup),encoding='utf-8')

# Rich multilingual sitemap with regional alternates.
ns='http://www.sitemaps.org/schemas/sitemap/0.9'; xhtml='http://www.w3.org/1999/xhtml'
rows=['<?xml version="1.0" encoding="UTF-8"?>',f'<urlset xmlns="{ns}" xmlns:xhtml="{xhtml}">']
for code in META:
    u=url_for(code); rows.append('  <url>'); rows.append(f'    <loc>{u}</loc>'); rows.append(f'    <lastmod>{date.today().isoformat()}</lastmod>'); rows.append('    <changefreq>weekly</changefreq>'); rows.append('    <priority>1.0</priority>' if code=='en' else '    <priority>0.9</priority>')
    for h,href in alts: rows.append(f'    <xhtml:link rel="alternate" hreflang="{h}" href="{href}" />')
    rows.append('  </url>')
rows.append('</urlset>'); (PUB/'sitemap.xml').write_text('\n'.join(rows),encoding='utf-8')

# Extra crawler/security headers without changing hosting model.
headers=(PUB/'_headers').read_text(encoding='utf-8') if (PUB/'_headers').exists() else ''
if '/assets/social/*' not in headers: headers += '\n/assets/social/*\n  Cache-Control: public, max-age=604800\n'
(PUB/'_headers').write_text(headers,encoding='utf-8')

report={'languages':len(META),'localized_social_previews':len(META),'country_hreflang_targets':len(COUNTRY_HREF),'features':['localized title and meta description','canonical URLs','language + country hreflang','Open Graph','X/Twitter cards','1200x630 localized social images','JSON-LD Organization/WebSite/SoftwareApplication','multilingual sitemap','robots indexing directives']}
(ROOT/'SEO_IMPLEMENTATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
