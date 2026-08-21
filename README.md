# Beltway Demo — marketing site

A static, dependency-free marketing site for a heavy-industrial group:
liability risk transfer, demolition, environmental remediation, asset recovery
and industrial redevelopment.

> **The name is a placeholder.** "Beltway Demo" is a stand-in until
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
├── tools/
│   ├── build-pages.sh      assembles partials/ + pages/ into the root HTML
│   └── make-plates.py      regenerates the placeholder image plates
└── assets/
    ├── css/styles.css      all styling; design tokens live in :root
    ├── js/main.js          sticky header, mobile nav, scroll reveals, counters
    └── img/
        ├── *.svg           logo, site plan and coverage map (drawings)
        └── photos/         image slots + placeholder plates (see its README)
```

### Editing

- **Page content** → edit `pages/<slug>.html`, then run `./tools/build-pages.sh`
  and commit the regenerated root HTML.
- **Header, footer, nav, meta** → edit the matching file in `partials/`, rebuild.
- **Page titles and meta descriptions** → the `PAGES` array in
  `tools/build-pages.sh`.
- **Colors, type, spacing** → the `:root` token block at the top of
  `assets/css/styles.css`.
- **Imagery** → `assets/img/photos/` — see the README there for what each slot
  needs and how to swap in real photographs.

The build script is a convenience, not a requirement: the root `.html` files are
complete on their own, so you can also edit them directly and keep the sources
in sync afterwards.

## Renaming

The brand name appears in one form only, so a single pass covers the copy.
Edit the sources under `partials/` and `pages/`, never the built HTML at the
repo root — that gets regenerated:

```bash
grep -rl "Beltway Demo" partials pages tools README.md \
  | xargs sed -i 's/Beltway Demo/Your Company Name/g'
```

Then update, in order:

1. `partials/header.html` and `partials/footer.html` — the `DD` monogram in the
   inline logo SVG, and `.brand__name` / `.brand__sub` (currently "Beltway Demo"
   over "Industrial Group").
2. `assets/img/favicon.svg` — same monogram.
3. `tools/build-pages.sh` — the page titles and descriptions.
4. `partials/footer.html` and `pages/contact.html` — phone numbers, email
   addresses and the office address.
5. Rebuild with `./tools/build-pages.sh`.

## Design

A working-site palette rather than a corporate one: warm bitumen and asphalt
grounds, concrete and dust neutrals, **hi-vis safety orange** (`#FF5C00`) as the
single accent carrying every call to action, **hazard yellow** (`#FFC61A`)
rationed to the diagonal stripe motif that marks the transition into each page's
closing band, and rust oxide for the image duotones. Every value is a token in
`:root` — change the palette there and the whole site follows.

Structural devices are meant to be true rather than decorative: the oversized
stencil numerals appear only where the content genuinely is a sequence (the
four-step process, the mobilisation timeline) and deliberately not on the
Services page, where A/B/C are alternatives rather than steps.

## Notes

- **The contact form has no backend.** It validates in the browser and shows a
  confirmation, but sends nothing. Point it at a form service (Formspree, Basin,
  a Lambda, …) in the `data-contact-form` handler at the bottom of
  `assets/js/main.js`.
- **The images are placeholders, not photographs.** `assets/img/photos/` holds
  generated SVG scene plates cut to each slot's exact aspect ratio, so the
  layout is final and real photography drops straight in — that folder's README
  lists every slot and what to shoot for it. Regenerate the plates with
  `python3 tools/make-plates.py`.
- **The site plan and coverage map stay drawings** — they carry information a
  photograph could not, so they are not photo slots.
- **Fonts** are Oswald (signage headlines), Barlow (body) and IBM Plex Mono
  (labels, figures, stencil numerals) from Google Fonts, each with a full system
  fallback stack — the site degrades cleanly if they are blocked.
- **Accessibility**: skip link, landmark regions, `aria-current` on the active
  nav item, visible focus rings, and all motion disabled under
  `prefers-reduced-motion`.
- The site is fully readable and navigable with JavaScript disabled.
