# RAWLO · rawlo.eu · premium redesign v16 · 2026-10-12

Grafit a tyrkysová, velká typografie, nepravidelná síť obsahových bloků,
horské a pobřežní scenérie a skutečné obrazovky aktuální aplikace.
Web navazuje na repozitář `milpavel/Rawlo` a nasazení Cloudflare Pages.

## Sestavení a nasazení

- Build command: `python3 scripts/generate_site.py` nebo `npm run build`.
- Output directory: `public`.
- Python 3.9 nebo novější; sestavení nevyžaduje instalaci balíčků.
- Zachované kompatibilní vstupy `enhance_seo.py` a `finalize_social_seo.py` umožňují i původní build command.
- Doména: `rawlo.eu`. Angličtina `/`, čeština `/cs/`, další jazyky dle kódu. `/en/` přesměruje na `/`.
- `_headers` a `_redirects` zachovávají stávající Cloudflare konfiguraci.

## Lokální náhled

```sh
python3 scripts/generate_site.py
python3 scripts/verify_site.py
python3 -m http.server 8788 -d public
```

Otevřete `http://localhost:8788/cs/`. HTML nelze spolehlivě zobrazit dvojklikem:
odkazy na assety začínají `/` stejně jako na produkční doméně.

## Obsah a dostupnost

Pět sekcí aplikace: Na cestu, Plánovač, Navigace, Mapa, Komunita. Profil navazuje samostatně.
Galerie obsahuje 12 nezměněných uživatelem dodaných obrazovek v češtině. Titulky jsou lokalizované.
Web uvádí vývojovou verzi iPhonu; neobsahuje neexistující odkaz do App Store ani termín vydání.
eSIM je v testování, trajekty a cestovní pojištění se připravují.
Prezentace dálničních známek neuvádí produkční platební garanci ani pevné ceny.
Offline dostupnost celé Evropy, rezervace kempů, PRO nákupy a další nedoložené funkce nejsou slibovány.

22 jazyků je zachováno. Nové texty jsou v `scripts/current_copy.py` a `scripts/marketing_copy.py`;
z původního katalogu se používají lokalizované nadpisy a informace o trase.
Výběr jazyka pamatuje ruční volbu; na `/` použije jazyk prohlížeče.
Po zavření náhledu obrázku se fokus vrací přes nativní HTML dialog.
CSS respektuje omezení pohybu a má responzivní rozložení pro malé telefony.

Interaktivní ukázka přepíná čtyři skutečné obrazovky (plán, navigace, mapa,
komunita), vysvětluje přínos a propojuje je s galerií. Abstraktní SVG trasa
je ilustrační motiv; není to webová navigace ani kalkulace skutečné cesty.
Ovládání funguje i šipkami, Home a End a používá semantiku ARIA tabů.
Scroll animace jsou jednorázové, průběh stránky je v horním panelu.
Lehký prostorový pohyb telefonu funguje pouze s přesným ukazatelem.

Akce „Chci vědět o spuštění“ otevře předvyplněný e-mail na support@rawlo.eu;
stránka jasně uvádí, že otevře poštovní aplikaci. Nejde o automaticky uloženou
registraci nebo funkční placený nákup. Při vydání se CTA může změnit na odkaz
do App Store. Texty neobsahují vymyšlená hodnocení nebo počty uživatelů RAWLO.

## Obrazové podklady

Logo: původní SVG RAWLO. Ikony: SVG přímo v kódu.
Pozadí `alpine-journey.png` bylo vytvořeno vestavěným ImageGen jako ilustrační fotografie.
Prompt: Alpine valley, Dolomite mountain peaks, dark pine forest on the left,
lake and winding road on the right, small unbranded camper, muted cool slate palette,
photorealistic editorial adventure photography; no text, logo, phones or UI.
Fotografie nepředstavuje konkrétní rezervovatelné místo.

Pobřežní fotografie `coastal-escape.png`: vestavěný ImageGen, prompt:
Mediterranean coastal overlook at blue hour, small unbranded campervan on a
gravel turnout among pines, calm sea to the left, mountain coast and winding
road, naturally turquoise water, golden horizon, editorial travel photography;
no text, logos, screens, phones or graphics. Opět ilustrační místo.

Design se inspiroval způsobem prezentace u Roadtrippers, Wanderlog,
Campercontact, park4night a Sygic, nikoli jejich značkou či grafickými assety.
Podrobnosti jsou v INSPIRACE_A_KONCEPCE.md v balíčku.

## Ověření

Generátor, kompatibilní build vstupy a strukturální kontrola všech 22 stránek prošly.
Kontrolují se soubory, kotvy, galerie, jazykové varianty, canonical a hreflang.
JavaScript prochází `node --check`; změny `git diff --check`.
V tomto prostředí nebylo dostupné ověření renderu a interakcí v prohlížeči.
Před publikací zkontrolujte desktop a mobil v lokálním náhledu nebo Cloudflare preview.
Produkční web nebyl z tohoto prostředí nasazen.

Staré assety v existujícím repozitáři mohou zůstat: nové stránky je nepoužívají.
Nové soubory mají verzi v názvu, aby dlouhá cache Cloudflare nevracela původní vzhled.
