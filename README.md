# Meridian Industrial Group — marketing site

A static, dependency-free marketing site for a heavy-industrial group:
liability risk transfer, demolition, environmental remediation, asset recovery
and industrial redevelopment.

> **The name is a placeholder.** "Meridian Industrial Group" is a stand-in until
> the real brand is decided — see [Renaming](#renaming) below. All copy, figures,
> addresses, phone numbers and email addresses are illustrative.

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
| `index.html` | Home — hero, figures, capabilities, risk-transfer feature, process, projects, coverage |
| `about.html` | Company story, figures, operating principles, bonding & compliance |
| `services.html` | Eight capability blocks, plus the three ways clients engage |
| `areas-we-serve.html` | Regional coverage, region-by-region detail, mobilisation timeline |
| `news.html` | Featured release plus a grid of project and company updates |
| `contact.html` | Enquiry form, direct contact lines, regional offices |
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
grep -rl "Meridian Industrial Group" . --include="*.html" --include="*.md" \
  | xargs sed -i 's/Meridian Industrial Group/Your Company Name/g'
grep -rl "Meridian" . --include="*.html" | xargs sed -i 's/Meridian/YourCo/g'
```

Then update, in order:

1. `partials/header.html` and `partials/footer.html` — the `MI` monogram in the
   inline logo SVG, and `.brand__name` / `.brand__sub`.
2. `assets/img/favicon.svg` — same monogram.
3. `tools/build-pages.sh` — the page titles and descriptions.
4. `partials/footer.html` and `pages/contact.html` — phone numbers, email
   addresses and the office address.
5. Rebuild with `./tools/build-pages.sh`.

## Notes

- **The contact form has no backend.** It validates in the browser and shows a
  confirmation, but sends nothing. Point it at a form service (Formspree, Basin,
  a Lambda, …) in the `data-contact-form` handler at the bottom of
  `assets/js/main.js`.
- **Artwork is all inline SVG** — industrial silhouettes, plant elevations, site
  plans and an abstract coverage map. Nothing is loaded from a CDN, so the site
  works offline and has no licensing questions. Swap in photography by replacing
  the `<img>` sources in `pages/`.
- **Fonts** are Oswald and Inter from Google Fonts, with full system fallbacks —
  the site degrades cleanly if they are blocked or unavailable.
- **Accessibility**: skip link, landmark regions, `aria-current` on the active
  nav item, visible focus rings, and all motion disabled under
  `prefers-reduced-motion`.
- The site is fully readable and navigable with JavaScript disabled.
