#!/usr/bin/env python3
"""
Static site builder for beltwaydemo.com.

    python3 _build/build.py

Reads _build/config.py (business details), src/pages.py (titles, descriptions,
breadcrumbs) and src/content/*.html (page bodies), and writes finished HTML
into the site root along with sitemap.xml. The site root is what Firebase deploys (_build/ is ignored).
Nothing here needs installing beyond Python 3.
"""
import datetime, html, json, pathlib, re, sys

SRC = pathlib.Path(__file__).resolve().parent
PUBLIC = SRC.parent  # deploy root = repo root, mirroring the live site
sys.path.insert(0, str(SRC))
import config as C          # noqa: E402
from pages import PAGES     # noqa: E402

TICK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true">'
        '<path d="M5 12.5l4.5 4.5L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
PHONE_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
              '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2" '
              'stroke-linejoin="round"/></svg>')
V = C.ASSET_VERSION
ADDRESS_ONE_LINE = f"{C.STREET}, {C.CITY}, {C.REGION} {C.POSTAL}"


def esc(s):
    return html.escape(s, quote=True)


# --------------------------------------------------------------- images ----
def picture(path, alt, w, h, priority=False, cls="", lazy=True):
    """<picture> with WebP (800px variant + full size) and the original file as fallback.
    path is relative to /assets/, e.g. "img/photos/teardown.jpg"."""
    w, h = int(w), int(h)
    stem = path.rsplit(".", 1)[0]
    srcset = []
    if (PUBLIC / "assets" / f"{stem}-800.webp").exists() and w > 800:
        srcset.append(f"/assets/{stem}-800.webp 800w")
    if (PUBLIC / "assets" / f"{stem}.webp").exists():
        srcset.append(f"/assets/{stem}.webp {w}w")
    if priority:
        load = 'fetchpriority="high" decoding="async"'
    elif lazy:
        load = 'loading="lazy" decoding="async"'
    else:
        load = 'decoding="async"'
    sizes = ' sizes="100vw"' if len(srcset) > 1 else ""
    source = f'<source type="image/webp" srcset="{", ".join(srcset)}"{sizes}>' if srcset else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<picture>{source}<img{c} src="/assets/{path}" alt="{esc(alt)}" '
            f'width="{w}" height="{h}" {load}></picture>')


def crumbs(page):
    trail = page.get("crumbs", [])
    if not trail:
        return ""
    parts = ['<a href="/">Home</a>']
    for label, href in trail[:-1]:
        parts.append(f'<span aria-hidden="true">/</span> <a href="{href}">{esc(label)}</a>')
    parts.append(f'<span aria-hidden="true">/</span> <span>{esc(trail[-1][0])}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " ".join(parts) + "</nav>"


def cta(eyebrow, heading, text):
    return f'''<section class="cta section section--tight">
    <div class="wrap">
      <div class="cta__inner">
        <div data-reveal>
          <p class="eyebrow">{eyebrow}</p>
          <h2 class="h-md">{heading}</h2>
          <p class="muted">{text}</p>
        </div>
        <div class="btn-row" data-reveal="80">
          <a class="btn btn--primary" href="/contact">Get a Free Quote {ARROW}</a>
          <a class="btn btn--ghost btn--call" href="tel:{C.PHONE_E164}">{PHONE_ICON} Call {C.PHONE_DISPLAY}</a>
        </div>
      </div>
    </div>
  </section>'''


def trust():
    """Trust strip: license, insurance, service area, free quote."""
    I = lambda d: f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">{d}</svg>'
    items = [
        (I('<path d="M12 3l7 3v6c0 4.5-3 7.6-7 9-4-1.4-7-4.5-7-9V6z" stroke-linejoin="round"/><path d="M9 12l2 2 4-4" stroke-linecap="round" stroke-linejoin="round"/>'),
         f"MHIC #{C.MHIC}", "Maryland licensed &middot; WMB LLC"),
        (I('<path d="M7 3h7l4 4v14H7z" stroke-linejoin="round"/><path d="M14 3v4h4M10 13l2 2 3-3.5" stroke-linecap="round" stroke-linejoin="round"/>'),
         "Insured", "Certificates on request"),
        (I('<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11z" stroke-linejoin="round"/><circle cx="12" cy="10" r="2.6"/>'),
         "Serving Maryland", "Based in National Harbor, MD"),
        (I('<path d="M5 4h14v16l-3-2-2 2-2-2-2 2-2-2-3 2z" stroke-linejoin="round"/><path d="M9 9h6M9 13h4" stroke-linecap="round"/>'),
         "Free written quotes", "Fixed scope, fixed price"),
    ]
    lis = "".join(f'<li class="trust__item"><span class="trust__icon">{i}</span><span><span class="trust__title">{t}</span>'
                  f'<span class="trust__sub">{sub}</span></span></li>' for i, t, sub in items)
    return f'<section class="trust" aria-label="Licensing and coverage"><div class="wrap"><ul class="trust__list">{lis}</ul></div></section>'


IG_ICON = (
    '<svg class="ig-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/>'
    '<circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/>'
    '<circle cx="17.4" cy="6.6" r="1.1" fill="currentColor"/>'
    '</svg>'
)


def instagram_link():
    return (
        f'<a class="ig-link" href="{esc(C.INSTAGRAM_URL)}" target="_blank" rel="noopener" '
        f'aria-label="Beltway Demolition on Instagram">'
        f'{IG_ICON}<span>{esc(C.INSTAGRAM_HANDLE)}</span></a>'
    )


def expand(text, page):
    text = text.replace('href="tel:{{TEL}}">Call {{PHONE}}', 'href="tel:{{TEL}}">{{PHONE_ICON}} Call {{PHONE}}')
    text = text.replace('class="btn btn--ghost" href="tel:', 'class="btn btn--ghost btn--call" href="tel:')
    text = text.replace('class="btn btn--primary" href="tel:', 'class="btn btn--primary btn--call" href="tel:')
    text = text.replace("{{TRUST}}", trust())
    text = text.replace("{{PHONE}}", C.PHONE_DISPLAY).replace("{{TEL}}", C.PHONE_E164)
    text = text.replace("{{EMAIL}}", C.EMAIL).replace("{{TICK}}", TICK).replace("{{ARROW}}", ARROW)
    text = text.replace("{{PHONE_ICON}}", PHONE_ICON)
    text = text.replace("{{MHIC}}", C.MHIC).replace("{{HBR}}", C.MD_HBR)
    text = text.replace("{{ADDRESS}}", esc(ADDRESS_ONE_LINE)).replace("{{FORM_ENDPOINT}}", C.FORM_ENDPOINT)
    text = text.replace("{{INSTAGRAM_LINK}}", instagram_link())
    text = text.replace("{{CRUMBS}}", crumbs(page))
    text = re.sub(r"\{\{PIC:([^|]+)\|([^|]+)\|(\d+)\|(\d+)(\|hero)?\}\}",
                  lambda m: picture(m[1], m[2], m[3], m[4], priority=bool(m[5])), text)
    text = re.sub(r"\{\{CTA:([^|]+)\|([^|]+)\|([^}]+)\}\}", lambda m: cta(m[1], m[2], m[3]), text)
    left = re.findall(r"\{\{[^}]*\}\}", text)
    if left:
        raise SystemExit(f"Unexpanded tokens in {page['file']}: {left}")
    return text


# ----------------------------------------------------------- JSON-LD -------
def business_ld():
    return {
        "@context": "https://schema.org",
        "@type": "GeneralContractor",
        "@id": f"{C.SITE_URL}/#business",
        "name": C.BUSINESS_NAME,
        "url": f"{C.SITE_URL}/",
        "logo": f"{C.SITE_URL}/assets/brand/logo-emblem-v2.png",
        "image": f"{C.SITE_URL}/assets/brand/social-card.jpg",
        "description": "Full-service demolition contractor for house teardowns, commercial building "
                       "demolition, structural and exterior demolition, concrete removal and debris "
                       "haul-off across Maryland. A division of WMB LLC.",
        "telephone": C.PHONE_E164,
        "email": C.EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": C.STREET, "addressLocality": C.CITY,
                    "addressRegion": C.REGION, "postalCode": C.POSTAL, "addressCountry": "US"},
        "areaServed": [
            {"@type": "State", "name": "Maryland"},
            {"@type": "AdministrativeArea", "name": "Prince George's County, MD"},
            {"@type": "AdministrativeArea", "name": "Montgomery County, MD"},
            {"@type": "AdministrativeArea", "name": "Anne Arundel County, MD"},
            {"@type": "AdministrativeArea", "name": "Charles County, MD"},
        ],
        "parentOrganization": {"@type": "Organization", "name": C.PARENT_COMPANY, "url": C.PARENT_URL},
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "license",
             "name": f"Maryland Home Improvement Commission (MHIC) License #{C.MHIC}"},
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "license",
             "name": f"Maryland Home Builder Registration #{C.MD_HBR}"},
        ],
        "knowsAbout": ["House demolition", "Residential demolition", "Commercial demolition",
                       "Structural demolition", "Exterior demolition", "Concrete removal",
                       "Demolition debris hauling", "Site clearing", "Selective demolition",
                       "Interior demolition"],
        "sameAs": [C.PARENT_URL, C.INSTAGRAM_URL],
    }


def breadcrumb_ld(page):
    trail = page.get("crumbs", [])
    if not trail:
        return None
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{C.SITE_URL}/"}]
    for i, (label, href) in enumerate(trail, start=2):
        items.append({"@type": "ListItem", "position": i, "name": label, "item": C.SITE_URL + href})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def service_ld(page):
    s = page["service"]
    return {
        "@context": "https://schema.org", "@type": "Service",
        "serviceType": s["type"], "name": s.get("name", s["type"]),
        "url": C.SITE_URL + page["path"],
        "areaServed": [{"@type": "Place", "name": a} for a in s["areas"]],
        "provider": {"@type": "GeneralContractor", "@id": f"{C.SITE_URL}/#business",
                     "name": C.BUSINESS_NAME, "telephone": C.PHONE_E164, "url": f"{C.SITE_URL}/"},
    }


def faq_ld(body):
    """Build FAQPage from <details class="faq"><summary>Q</summary><div>A</div></details>."""
    qa = re.findall(r'<details class="faq"[^>]*>\s*<summary>(.*?)</summary>\s*<div class="faq__a">(.*?)</div>\s*</details>',
                    body, flags=re.S)
    def clean(x):
        x = re.sub(r"<[^>]+>", "", x)
        return " ".join(html.unescape(x).split())
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": clean(q),
                            "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in qa]}


def ld_script(obj):
    return ('<script type="application/ld+json">\n' +
            json.dumps(obj, indent=2, ensure_ascii=False).replace("</", "<\\/") + "\n</script>")


# ---------------------------------------------------------- template -------
NAV = [("Home", "/"), ("Services", "/services"), ("Areas We Serve", "/areas-we-serve"),
       ("FAQ", "/faq"), ("About", "/about")]


def head(page, body):
    url = C.SITE_URL + page["path"]
    tok = lambda x: x.replace("{{PHONE}}", C.PHONE_DISPLAY).replace("{{MHIC}}", C.MHIC).replace("{{HBR}}", C.MD_HBR)
    t, d = esc(tok(page["title"])), esc(tok(page["description"]))
    extra = []
    if page.get("noindex"):
        extra.append('<meta name="robots" content="noindex">')
    if page.get("preload"):
        extra.append(page["preload"])
    lds = []
    if page.get("business_ld"):
        lds.append(business_ld())
    if page.get("service"):
        lds.append(service_ld(page))
    if page.get("faq_ld"):
        lds.append(faq_ld(body))
    b = breadcrumb_ld(page)
    if b:
        lds.append(b)
    canonical = "" if page.get("noindex") else f'<link rel="canonical" href="{url}">\n'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
{chr(10).join(extra)}
<script>document.documentElement.classList.add("js");</script>
<meta name="theme-color" content="#0a0c0e">
<link rel="icon" href="/assets/img/favicon.ico" sizes="any">
<link rel="icon" href="/assets/img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="icon" href="/assets/img/favicon-16.png" type="image/png" sizes="16x16">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Oswald:wght@400;500;600&family=Russo+One&display=swap">
<link rel="stylesheet" href="/assets/css/styles.css?v={V}">
{canonical}<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{esc(C.BUSINESS_NAME)}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:image" content="{C.SITE_URL}/assets/brand/social-card.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{C.SITE_URL}/assets/brand/social-card.jpg">
{chr(10).join(ld_script(x) for x in lds)}
</head>'''


def header(page):
    items = []
    for label, href in NAV:
        cur = ' aria-current="page"' if page.get("nav") == href else ""
        items.append(f'<li><a class="nav__link" href="{href}"{cur}>{label}</a></li>')
    logo = picture("brand/logo-emblem-v2.png", "", 400, 176, cls="brand__mark", lazy=False)
    return f'''<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="utility">
    <div class="wrap utility__inner">
      <ul class="utility__facts">
        <li>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
            <path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11z" stroke-linejoin="round"/>
            <circle cx="12" cy="10" r="2.6"/>
          </svg>
          Serving Maryland &middot; National Harbor, MD
        </li>
        <li>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
            <path d="M12 3l7 3v6c0 4.5-3 7.6-7 9-4-1.4-7-4.5-7-9V6z" stroke-linejoin="round"/>
          </svg>
          A division of WMB LLC &middot; MD MHIC #{C.MHIC}
        </li>
      </ul>
      <ul class="utility__links">
        <li><a class="is-strong" href="tel:{C.PHONE_E164}">{C.PHONE_DISPLAY}</a></li>
      </ul>
    </div>
  </div>

  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="Beltway Demolition — home">
      {logo}
      <span class="brand__text">
        <span class="brand__name">Beltway</span>
        <span class="brand__sub">Demolition</span>
      </span>
    </a>

    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav"
            aria-label="Toggle navigation">
      <span></span><span></span><span></span>
    </button>

    <nav class="nav" id="primary-nav" aria-label="Primary">
      <ul class="nav__list">
        {"".join(items)}
      </ul>
      <a class="btn btn--primary" href="/contact">
        Get a Free Quote
        {ARROW}
      </a>
    </nav>
  </div>
</header>'''


def footer():
    yr = datetime.date.today().year
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid footer-grid--5">
      <div class="footer-col footer-about">
        <a class="brand" href="/" aria-label="Beltway Demolition — home">
          {picture("brand/logo-emblem-v2.png", "", 400, 176, cls="brand__mark")}
          <span class="brand__text">
            <span class="brand__name">Beltway</span>
            <span class="brand__sub">Demolition</span>
          </span>
        </a>
        <p>
          Full-service demolition across Maryland: house and commercial
          teardowns, structural and exterior work, concrete removal and
          debris haul-off.
        </p>
      </div>

      <div class="footer-col">
        <h4>Services</h4>
        <ul>
          <li><a href="/residential-demolition">Residential Demolition</a></li>
          <li><a href="/commercial-demolition">Commercial Demolition</a></li>
          <li><a href="/interior-demolition">Interior Demolition</a></li>
          <li><a href="/concrete-removal">Concrete Removal</a></li>
          <li><a href="/services">All Services</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Areas</h4>
        <ul>
          <li><a href="/demolition-prince-georges-county-md">Prince George's County</a></li>
          <li><a href="/demolition-montgomery-county-md">Montgomery County</a></li>
          <li><a href="/demolition-anne-arundel-county-md">Anne Arundel County</a></li>
          <li><a href="/areas-we-serve">All Areas</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="/about">About Us</a></li>
          <li><a href="/faq">FAQ</a></li>
          <li><a href="/contact">Contact</a></li>
          <li><a href="/privacy-policy">Privacy Policy</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:{C.PHONE_E164}">{C.PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></li>
          <li>{instagram_link()}</li>
          <li>{esc(C.STREET)}<br>{esc(C.CITY)}, {C.REGION} {C.POSTAL}</li>
        </ul>
      </div>
    </div>

    <p class="footer-legal">
      <strong>{esc(C.BUSINESS_NAME)}</strong>, a division of <strong>{esc(C.PARENT_COMPANY)}</strong>
      &middot; {esc(ADDRESS_ONE_LINE)}
      &middot; Maryland Home Improvement Commission <strong>MHIC #{C.MHIC}</strong>
      &middot; Maryland Home Builder Registration <strong>MD HBR #{C.MD_HBR}</strong>.
      Certificates of insurance available on request.
    </p>

    <div class="footer-bottom">
      <p>&copy; <span data-year>{yr}</span> {esc(C.BUSINESS_NAME)}, a division of {esc(C.PARENT_COMPANY)}.</p>
      <nav aria-label="Legal">
        <a href="/privacy-policy">Privacy Policy</a>
        <a href="/contact">Contact</a>
      </nav>
    </div>
  </div>
</footer>

<div class="mobile-cta" aria-label="Quick contact">
  <a class="btn btn--primary btn--call" href="tel:{C.PHONE_E164}">{PHONE_ICON} Call {C.PHONE_DISPLAY}</a>
  <a class="btn btn--ghost" href="/contact">Free Quote</a>
</div>

<script src="/assets/js/main.js?v={V}" defer></script>
</body>
</html>
'''


def build():
    urls = []
    for page in PAGES:
        body = (SRC / "content" / page["content"]).read_text()
        body = expand(body, page)
        out = head(page, body) + "\n" + header(page) + '\n<main id="main">\n' + body + "\n</main>\n" + footer()
        out = re.sub(r"\n{3,}", "\n\n", out)
        (PUBLIC / page["file"]).write_text(out)
        if not page.get("noindex"):
            urls.append((C.SITE_URL + page["path"], page.get("priority", "0.7")))
        print(f"built {page['file']}")
    today = datetime.date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, pr in urls:
        sm.append(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    (PUBLIC / "sitemap.xml").write_text("\n".join(sm) + "\n")
    (PUBLIC / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {C.SITE_URL}/sitemap.xml\n")
    print(f"sitemap.xml: {len(urls)} URLs")


if __name__ == "__main__":
    build()
