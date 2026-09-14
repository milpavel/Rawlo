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
- Open Graph + X/Twitter large-image cards on every language page.
- One unified 1200x630 RAWLO social preview used across all 22 localized URLs.
- JSON-LD for Organization, WebSite and Travel SoftwareApplication.
- Multilingual sitemap with hreflang alternates.
- Re-run `python3 scripts/enhance_seo.py` after regenerating pages.

## SEO + social preview deployment notes (2026-09-14)
- Production website origin used by SEO is `https://rawlo.eu`.
- Open Graph / WhatsApp / Facebook / LinkedIn metadata is static in every localized HTML `<head>`; it does not depend on JavaScript.
- All 22 language pages use `public/assets/social/rawlo-social-share-v14.jpg` for a consistent RAWLO visual identity.
- The social filename is versioned so old WhatsApp/Facebook/Messenger cache does not keep the previous image.
- The root `/` and `/cs/`, `/de/`, etc. use the same artwork while title/description remain localized.
- Deploy the CONTENTS of `public/` as the site root. If `public/` is deployed as a subfolder, crawler URLs will 404 and previews will fail.

## Unified social share card — V14
- WhatsApp, Messenger, Facebook, LinkedIn and other Open Graph consumers now receive one shared RAWLO visual: `public/assets/social/rawlo-social-share-v14.jpg`.
- The card is exactly 1200×630 px and clearly combines RAWLO branding, camper travel, route navigation and travel services.
- Every localized URL uses the same image for a consistent brand identity; `og:title`, `og:description`, locale and canonical URL remain localized.
- `twitter:card=summary_large_image`, `twitter:image`, `link rel=image_src`, `thumbnail` and JSON-LD `primaryImageOfPage` point at the same V14 asset.
- The editable source visual is stored in `design/social/rawlo-social-master-v14.png` and `npm run build` recreates all pages and final social metadata.
