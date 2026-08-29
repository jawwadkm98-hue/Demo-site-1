# Beltway Demolition — marketing site

A static, dependency-free marketing site for a demolition and site clearance
contractor working in Maryland, Washington DC and Virginia, backed by WMB LLC.

> **The name is a placeholder.** "Beltway Demolition" is a stand-in until
> the real brand is decided — see [Renaming](#renaming) below. Contact details
> and the licence number are placeholders too; see
> [`CONTENT-TODO.md`](CONTENT-TODO.md).

## Running it

There is no build toolchain and no dependencies. Open `index.html` in a browser,
or serve the folder:

```bash
python3 -m http.server 8000
# → http://localhost:8000
```

Deploy by uploading the repository root to any static host (GitHub Pages,
Netlify, Cloudflare Pages, S3 — anything that serves files).

## Pages

| File | Purpose |
| --- | --- |
| `index.html` | Home — services, how we work, licensing and backing, service area |
| `about.html` | Who we are, how we operate, licensing and backing |
| `services.html` | Six services, and the clients they are for |
| `areas-we-serve.html` | Service area by region, and what happens after you call |
| `contact.html` | Quote request form and direct contact details |
| `privacy-policy.html` | Placeholder privacy policy |

## Layout

```
├── index.html …            built pages (commit these — they are what ships)
├── partials/
│   ├── head.html           <head> + opening <body>   ({{TITLE}}, {{DESC}})
│   ├── header.html         sticky header and primary nav
│   └── footer.html         footer + script tags
├── pages/                  the unique body of each page
├── tools/build-pages.sh    assembles partials/ + pages/ into the root HTML
└── assets/
    ├── css/styles.css      all styling; design tokens live in :root
    ├── js/main.js          sticky header, mobile nav, scroll reveals, counters
    └── img/*.svg           all artwork — hand-drawn SVG, no external images
```

### Editing

- **Page content** → edit `pages/<slug>.html`, then run `./tools/build-pages.sh`
  and commit the regenerated root HTML.
- **Header, footer, nav, meta** → edit the matching file in `partials/`, rebuild.
- **Page titles and meta descriptions** → the `PAGES` array in
  `tools/build-pages.sh`.
- **Colors, type, spacing** → the `:root` token block at the top of
  `assets/css/styles.css`.

The build script is a convenience, not a requirement: the root `.html` files are
complete on their own, so you can also edit them directly and keep the sources
in sync afterwards.

## Renaming

Two find-and-replace passes cover the whole site:

```bash
grep -rl "Beltway Demolition" . --include="*.html" --include="*.md" \
  | xargs sed -i 's/Beltway Demolition/Your Company Name/g'
grep -rl "Beltway Demolition" . --include="*.html" | xargs sed -i 's/Beltway Demolition/YourCo/g'
```

Then update, in order:

1. `partials/header.html` and `partials/footer.html` — the `MI` monogram in the
   inline logo SVG, and `.brand__name` / `.brand__sub`.
2. `assets/img/favicon.svg` — same monogram.
3. `tools/build-pages.sh` — the page titles and descriptions.
4. `partials/footer.html` and `pages/contact.html` — phone numbers, email
   addresses and the office address.
5. Rebuild with `./tools/build-pages.sh`.

## Logo

The mark is a heavy ring with a segment broken out of the upper right, the
piece kicked clear of the gap it left: the Beltway is a ring road, and
demolition takes a piece out of things. No letterforms, which is what lets it
survive at favicon size.

`tools/make-logo.py` generates the whole kit from computed geometry — change
`R`, `W` or the gap angles at the top of that file and every variant stays
concentric:

| File | Use |
| --- | --- |
| `logo-mark.svg` | Inline use; the broken piece inherits `currentColor` |
| `logo-mark-dark.svg` | On dark grounds (amber ring, white piece) |
| `logo-mark-light.svg` | On light grounds (amber ring, ink piece) |
| `logo-mark-mono.svg` | One colour — vinyl, embroidery, stamps, single-plate print |
| `logo-lockup-dark.svg` / `-light.svg` / `-mono.svg` | Mark plus wordmark, for letterhead, signage and email |
| `favicon.svg` | Browser tab; carries its own dark ground |

The header and footer inline the mark rather than linking it, so the broken
piece picks up the surrounding text colour.

## Accuracy

**Everything on this site is either true or deliberately left blank.** The only
factual claims it makes are that the company is backed by WMB LLC, which holds
a construction contractor licence in the State of Maryland, and that it does
demolition and site clearance work in Maryland, Washington DC and Virginia.

Figures that would normally appear on a contractor's site — years in business,
headcount, project counts, bonding capacity, safety record, accreditations —
are **absent rather than estimated**. Add them when you have them.

**See [`CONTENT-TODO.md`](CONTENT-TODO.md)** for everything that still needs a
real value before launch, what to double-check, and what is worth adding later.

## Notes

- **Ownership and licensing.** The site states that the company is backed by
  **WMB LLC**, which holds a construction contractor licence in the State of
  Maryland. The licence number is a deliberate placeholder — `#000000` — in
  `partials/footer.html` and `pages/about.html`. **Replace it with the real
  number before launch**, and check the wording against how the licence is
  actually held.
- **No invented figures.** Headcount, years in business, project counts,
  bonding and accreditations are absent rather than estimated, because
  published capability claims are exactly what clients, prequalification
  bodies and licensing boards check. `CONTENT-TODO.md` lists what to add once
  you can substantiate it.
- **The contact form has no backend.** It validates in the browser and shows a
  confirmation, but sends nothing. Point it at a form service (Formspree, Basin,
  a Lambda, …) in the `data-contact-form` handler at the bottom of
  `assets/js/main.js`.
- **Artwork is all inline SVG** — an industrial silhouette, a building
  elevation, a site plan and a stylised map of the Maryland / DC / Virginia
  service area. Nothing loads from a CDN, so the site works offline and raises
  no image-licensing questions. The map is deliberately schematic, not a survey
  drawing. Swap in real project photography by replacing the `<img>` sources in
  `pages/`.
- **Fonts** are Oswald and Inter from Google Fonts, with full system fallbacks —
  the site degrades cleanly if they are blocked or unavailable.
- **Accessibility**: skip link, landmark regions, `aria-current` on the active
  nav item, visible focus rings, and all motion disabled under
  `prefers-reduced-motion`.
- The site is fully readable and navigable with JavaScript disabled.
