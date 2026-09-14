# RAWLO web — modern localized build

Static multilingual RAWLO landing page prepared for deployment on `rawlo.app`.

## What is included
- 22 localized website routes: EN, CS, SK, PL, DE, FR, ES, PT, IT, NL, HU, RO, HR, SL, BG, FI, SV, ET, LV, LT, DA, EL.
- Automatic first-visit language detection from the browser (`navigator.languages`).
- Manual language selector remains available and the visitor's choice is remembered in `localStorage`.
- App preview screenshots follow the current website language; every supported language has its own localized preview set.
- Modernized dark RAWLO visual design, responsive layout, mobile menu, scroll reveal, active navigation, interactive app-preview controls and reduced-motion support.
- Static deployment: no framework or server runtime required.

## Deploy
Upload the contents of `public/` to the web root. The `/cs/`, `/de/`, etc. directories must stay intact.

`/` is the English canonical page and automatically redirects human visitors to their supported browser language when appropriate. Search engines still receive the canonical/hreflang HTML.

## Source
`python3 scripts/generate_site.py` regenerates all localized HTML pages.

## SEO & social sharing (2026-09-14)
- 22 localized SEO title/description sets focused on motorhome, campervan and caravan travel.
- Canonical URLs plus language and country-specific hreflang targeting for European markets.
- Open Graph + X/Twitter large-image cards per language.
- 22 localized 1200x630 social previews in `public/assets/social/`.
- JSON-LD for Organization, WebSite and Travel SoftwareApplication.
- Multilingual sitemap with hreflang alternates.
- Re-run `python3 scripts/enhance_seo.py` after regenerating pages.

## SEO + social preview deployment notes (2026-09-14)
- Production website origin used by SEO is `https://rawlo.eu`.
- Open Graph / WhatsApp / Facebook / LinkedIn metadata is static in every localized HTML `<head>`; it does not depend on JavaScript.
- Each of the 22 language pages has its own 1200x630 JPEG under `public/assets/social/rawlo-social-<lang>-20260914-v4.jpg`.
- Social image filenames are versioned so old WhatsApp/Facebook cache cannot keep a previously missing image URL.
- The root `/` page has the global English preview; share `/cs/`, `/de/`, etc. when you want a localized social card.
- Deploy the CONTENTS of `public/` as the site root. If `public/` is deployed as a subfolder, crawler URLs will 404 and previews will fail.
