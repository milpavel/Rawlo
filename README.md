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
