# beltwaydemo.com — SEO rebuild (October 2026)

A static, framework-free rebuild of beltwaydemo.com. It keeps the existing logo, the ink/steel/amber
palette and the Oswald + Inter type, adds a visual refresh, rewrites the on-page SEO, and adds 8 new
pages. **Nothing has been deployed or pushed.**

## Layout (mirrors the live site, so it drops straight into the repo)

```
index.html, about.html, services.html, areas-we-serve.html, contact.html, privacy-policy.html   (existing URLs)
residential-demolition.html, interior-demolition.html, commercial-demolition.html, concrete-removal.html,
demolition-prince-georges-county-md.html, demolition-montgomery-county-md.html,
demolition-anne-arundel-county-md.html, faq.html                                                    (new)
404.html, sitemap.xml, robots.txt, site.webmanifest
assets/css/styles.css   original stylesheet + a "2026 refresh" block appended at the end
assets/js/main.js       original script; contact-form handler rewritten
assets/img/..., assets/brand/...   original images, plus .webp and -800.webp copies
firebase.json           hosting config (cleanUrls, trailingSlash:false, cache headers, a few redirects)
_build/                 page sources + build script (ignored by Firebase, not deployed)
```

The live site's GitHub repo (jawwadkm98-hue/Demo-site-1) auto-deploys to Firebase. I could not see
the repo's own `firebase.json`, so I don't know its `public` directory. This package assumes the site
files sit in the same folder as `firebase.json` (`"public": "."`). If the repo uses a subfolder (for
example `public/`), copy the site files into that folder and merge the `cleanUrls`, `trailingSlash`,
`headers`, `redirects` and `ignore` keys into the repo's existing `firebase.json`. Keep the repo's own
GitHub Actions workflow as it is.

## Change business details in ONE place

All phone, email, address, license numbers and the form endpoint live in **`_build/config.py`**:

| Setting | Current value |
|---|---|
| `PHONE_DISPLAY` / `PHONE_E164` | (703) 861-5354 / +17038615354 (owner's choice, Oct 18) |
| `EMAIL` | info@beltwaydemo.com |
| `INSTAGRAM_URL` | https://www.instagram.com/beltwaydemolition/ |
| Address | 145 Fleet St #142, National Harbor, MD 20745 |
| `MHIC` / `MD_HBR` | 154299 / 9597 |
| `FORM_ENDPOINT` | https://formspree.io/f/xbgdbpol |

To change the phone number, edit both phone lines (the display format and the +1 format) and rebuild:

```
python3 _build/build.py            # regenerates every .html page, sitemap.xml and robots.txt
python3 _build/optimize_images.py  # only if you add or replace images (needs Pillow)
```

Page bodies are in `_build/content/*.html`, and titles and meta descriptions are in
`_build/pages.py`. Edit those, not the generated .html files.

## What changed

**SEO and content**
- Titles, meta descriptions, H1s and H2s are rewritten on every page around target searches such as
  "demolition contractor Maryland", "house demolition Maryland" and county-level searches. One H1 per page,
  with no skipped heading levels.
- US spelling throughout (license, neighboring, program, inquiry).
- New pages (main content is about 610–720 words each, plus the FAQ):
  - `/residential-demolition`, `/interior-demolition`, `/commercial-demolition`, `/concrete-removal`
  - `/demolition-prince-georges-county-md`, `/demolition-montgomery-county-md`, `/demolition-anne-arundel-county-md`
  - `/faq` (17 Q&As, with FAQPage schema)
- Copy guardrails:
  - No invented stats, reviews, project claims or years in business. "Since 2008" from wmbre.com is
    **not** used.
  - No asbestos or lead abatement licensing is claimed. The copy says hazardous materials are
    surveyed and abated by licensed partners.
  - **Maryland only.** Beltway Demolition is currently licensed only in Maryland, so the copy, titles,
    schema (`areaServed`), trust strip, areas page, FAQ and footer mention Maryland only. The DC page
    was removed, and `/demolition-washington-dc` 301-redirects to `/areas-we-serve` in case it was
    indexed. The old service-area map image was removed because its baked-in text named DC and Virginia.
  - The old "Environmental & Abatement / abatement by licensed personnel" service is now
    "Hazardous Materials Coordination".
- Structured data:
  - GeneralContractor JSON-LD (NAP, MHIC/HBR credentials, parent organization WMB LLC, service areas)
    on Home and Contact.
  - Service schema on the service and area pages.
  - BreadcrumbList on all inner pages.
  - FAQPage on /faq. Google now shows FAQ rich results only for a few site types, but the markup
    does no harm.
- Internal links:
  - The nav is now Home, Services, Areas We Serve, FAQ, About, plus a "Get a Free Quote" button.
  - The footer links to every service and area page.
  - Service cards, area chips and region rows link to the new pages, and the pages link to each other.
- The footer on every page carries the full details: Beltway Demolition, a division of WMB LLC ·
  145 Fleet St #142, National Harbor, MD 20745 · MHIC #154299 · MD HBR #9597 · phone · email.

**Conversion**
- Contact form:
  - It posts to Formspree (`action="https://formspree.io/f/xbgdbpol" method="POST"`), with a honeypot
    field, a `_subject` field, and the visitor's `email` field as the reply-to.
  - With JavaScript it submits by `fetch` and shows inline success and error messages. Without
    JavaScript the browser posts the same form.
- "Call (703) 861-5354" tap links in the hero of every page and in every call-to-action block.
- A sticky call / free-quote bar on phones (screen width 760px or less).
- A branded `404.html` (Firebase serves it automatically for unknown URLs).

**Visual refresh** (CSS layer appended to `styles.css`; same brand identity)
- Bigger hero headline with Free Quote and Call buttons.
- A trust strip: MHIC #154299 · Insured · Serving Maryland · Free written quotes.
- Rounder service-card icons, outlined process numbers, link-styled area chips, an FAQ accordion,
  a 5-column footer, better line-height and contrast.
- The "Before" and "After" badges on photos were removed, because they implied the photos show our
  own jobs. They are illustrative, and the alt text describes them neutrally.

**Technical**
- `firebase.json`:
  - `cleanUrls: true` and `trailingSlash: false`. Old `/about.html`-style URLs automatically
    301-redirect to `/about`.
  - Long cache headers on `/assets/**`, with `?v=` cache-busting on the CSS and JS.
  - A few short-URL redirects, plus the redirect for the removed DC page.
- Images:
  - WebP copies were generated (originals kept), and `<picture>` serves an 800px WebP to phones.
  - The hero images are about 35–80% smaller, and the logo dropped from 125 KB to 30 KB.
  - Every content image has alt text, and the hero images have `fetchpriority="high"`.
- The home hero text no longer waits for the scroll-reveal animation, which helps LCP.
- `sitemap.xml` now lists all 14 indexable URLs (Maryland pages only) with `<lastmod>`, and `robots.txt` points to it.
- All asset paths are root-relative, so the 404 page works at any depth.

## Open items for Jawwad
1. **Deploy access.** Either push these files to the GitHub repo, which auto-deploys (so pushing
   puts it live), or run `firebase deploy --only hosting` from this folder with an account that has
   access to the Firebase project. `"site": "beltway-demo"` comes from the domain's
   `hosting-site=beltway-demo` DNS record. If the CLI asks for a project, run `firebase use --add`
   and pick the project that owns that site.
2. **Formspree endpoint.** Wired to `https://formspree.io/f/xbgdbpol`. Confirm that form delivers to
   info@beltwaydemo.com, then publish with `firebase deploy --only hosting`.
3. **Fix www.** In the Firebase console, go to Hosting → Add custom domain → `www.beltwaydemo.com`
   and choose "Redirect to beltwaydemo.com". Then follow the DNS steps it shows at IONOS. This can't
   be done in `firebase.json`, because host-level redirects are set per domain in the console. Today,
   www gives an SSL error and then a 404.
4. **Google Business Profile.** Create and verify it as "Beltway Demolition", primary category
   "Demolition contractor", using the same phone as the site. If 145 Fleet St #142 is a mailbox or
   virtual office, hide the address and set service areas instead.
5. **Phone consistency.** The site uses (703) 861-5354 and info@beltwaydemo.com. The license record
   shows (703) 626-7861 and wmbre.com shows (443) 267-4049. Use one number on the GBP, directories,
   proposals and wmbre.com.
6. **Check SDAT.** Bizapedia lists a "BELTWAY DEMOLITION" in Owings Mills, MD. Check Maryland SDAT
   to see whether it's an unrelated entity using the name, and consider registering "Beltway
   Demolition" as a trade name of WMB LLC.
7. **Confirm these claims before going live:**
   - "Insured, certificates on request" (carried over from the old site).
   - "Free written quotes" (added at your request).
   - If you later get licensed outside Maryland, new area pages can be added then; the site makes no
     such claim now.
   - That the abatement partners exist.
8. **Photos.** The site photos are illustrative, not our jobs. Replace them with real job photos when
   you have them (same filenames, then rerun `optimize_images.py`), and add a projects page then.
9. **Afterwards:**
   - Add GA4 or Plausible with form and call conversion tracking. Not included, because there is no
     tracking ID yet.
   - Submit `sitemap.xml` in Search Console and Bing Webmaster Tools.
   - Ask whoever runs wmbre.com to say "Beltway Demolition" instead of "WMB Demolition".

## Local check
`python3 /workspace/seo/serve.py` starts a local server on port 8765 that mimics Firebase cleanUrls.
`python3 /workspace/seo/validate.py` checks each page for a 200 status, the right title, one H1,
JSON-LD that parses, broken internal links, missing assets and banned strings (licence, 703, info@).
