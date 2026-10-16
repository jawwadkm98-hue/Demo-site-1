#!/usr/bin/env bash
# Assembles the static pages from partials/ + pages/.
#
#   partials/head.html    <head> + opening <body>   ({{TITLE}}, {{DESC}})
#   partials/header.html  sticky site header + nav
#   pages/<slug>.html     the unique body of one page
#   partials/footer.html  footer + script tags
#
# Output is plain HTML at the repo root — the built site needs no server,
# no build tooling and no dependencies. Run this after editing a partial
# or a page body, then commit the regenerated HTML.
#
# Usage: ./tools/build-pages.sh
set -euo pipefail
cd "$(dirname "$0")/.."

# ---------------------------------------------------------------------------
# The live origin, no trailing slash. Canonical URLs, og:url, the social-card
# URL, robots.txt and sitemap.xml are all derived from this — set it once when
# the domain is live and rebuild.
SITE_URL="${SITE_URL:-https://beltwaydemo.com}"
# ---------------------------------------------------------------------------

# Literal search-and-replace. Deliberately avoids sed and ${var//p/r}: both
# treat "&" in the replacement as the matched text (the latter since bash 5.2),
# which mangles titles like "News & Projects". Prefix/suffix removal has no
# such special characters.
replace_all() {
  local s=$1 pat=$2 rep=$3 out=""
  while [[ $s == *"$pat"* ]]; do
    out+="${s%%"$pat"*}$rep"
    s="${s#*"$pat"}"
  done
  printf '%s' "$out$s"
}

# Titles and descriptions land in <title> and in attribute values, so escape
# the characters that would otherwise be parsed as markup.
html_escape() {
  local s
  s=$(replace_all "$1" '&' '&amp;')
  s=$(replace_all "$s" '<' '&lt;')
  s=$(replace_all "$s" '>' '&gt;')
  replace_all "$s" '"' '&quot;'
}

# slug|title|description|breadcrumb name (index has none)
PAGES=(
"index|Demolition Contractor in Maryland, DC & Virginia — Beltway Demolition|Demolition, site clearance and environmental work across Maryland, Washington DC and Virginia. Fixed written quotes. Backed by WMB LLC, a licensed Maryland contractor.|"
"about|About Beltway Demolition — DMV Demolition & Site Clearance Contractor|A demolition and site clearance contractor in Maryland, DC and Virginia, backed by WMB LLC, a licensed Maryland construction contractor.|About"
"services|Demolition, Site Clearance & Hauling Services — Beltway Demolition|Residential, commercial and interior demolition, site clearance and grading, abatement, asset recovery, permits and hauling across Maryland, DC and Virginia.|Services"
"areas-we-serve|Areas We Serve: Baltimore, DC & Northern Virginia — Beltway Demolition|Demolition across Maryland, Washington DC and Virginia: Baltimore, Annapolis, Montgomery and Prince George's, Northern Virginia, Frederick and the Eastern Shore.|Areas We Serve"
"contact|Get a Demolition Quote — Beltway Demolition|Send the address and a few photos for a fixed written demolition quote. Call +1 (703) 861-5354 or email info@beltwaydemo.com.|Contact"
"privacy-policy|Privacy Policy — Beltway Demolition|How this site collects, uses and protects personal information.|Privacy Policy"
)

# Escape a string for a JSON value (the FAQ files contain no double quotes or
# backslashes, but titles might one day).
json_escape() {
  local s
  s=$(replace_all "$1" '\' '\\')
  replace_all "$s" '"' '\"'
}

# ------------------------------------------------- structured data (JSON-LD) --
# schema.org data for search engines and AI assistants: who the company is,
# what it does and where. Built into every page's <head> as {{SCHEMA}}.
PHONE_E164="+17038615354"
EMAIL="info@beltwaydemo.com"
ORG_ID="$SITE_URL/#org"
service_offer() { printf '{"@type":"Offer","itemOffered":{"@type":"Service","name":"%s","url":"%s/services.html#%s"}}' "$1" "$SITE_URL" "$2"; }
ORG_JSON='{"@type":"GeneralContractor","@id":"'"$ORG_ID"'","name":"Beltway Demolition","url":"'"$SITE_URL"'/",'\
'"logo":"'"$SITE_URL"'/assets/brand/logo-emblem-v2.png","image":"'"$SITE_URL"'/assets/brand/social-card.jpg",'\
'"description":"Demolition and site clearance contractor working across Maryland, Washington DC and Virginia: demolition, environmental and abatement work, site clearance and grading, asset recovery, permits and hauling.",'\
'"telephone":"'"$PHONE_E164"'","email":"'"$EMAIL"'",'\
'"areaServed":[{"@type":"State","name":"Maryland"},{"@type":"AdministrativeArea","name":"Washington, DC"},{"@type":"State","name":"Virginia"}],'\
'"parentOrganization":{"@type":"Organization","name":"WMB LLC","url":"https://wmbre.com"},'\
'"knowsAbout":["Demolition","Selective demolition","Interior strip-outs","Site clearance","Grading","Asbestos abatement","Tank removal","Asset recovery","Debris hauling"],'\
'"hasOfferCatalog":{"@type":"OfferCatalog","name":"Demolition and site clearance services","itemListElement":['\
"$(service_offer 'Demolition' demolition),$(service_offer 'Environmental and abatement' environmental),$(service_offer 'Site clearance and grading' clearance),"\
"$(service_offer 'Asset recovery and recycling' recovery),$(service_offer 'Permits and project management' management),$(service_offer 'Hauling and disposal' hauling)"\
']}}'
WEBSITE_JSON='{"@type":"WebSite","@id":"'"$SITE_URL"'/#website","url":"'"$SITE_URL"'/","name":"Beltway Demolition","publisher":{"@id":"'"$ORG_ID"'"},"inLanguage":"en-US"}'

ALL_FAQS=""   # every Q and A, for llms.txt

for entry in "${PAGES[@]}"; do
  IFS='|' read -r slug title desc crumb <<<"$entry"
  body="pages/${slug}.html"
  [ -f "$body" ] || { echo "missing $body" >&2; exit 1; }

  # index lives at the origin root; every other page at /<slug>.html
  if [ "$slug" = "index" ]; then page_url="$SITE_URL/"; else page_url="$SITE_URL/${slug}.html"; fi

  head_html=$(replace_all "$(cat partials/head.html)" '{{TITLE}}' "$(html_escape "$title")")
  head_html=$(replace_all "$head_html" '{{DESC}}' "$(html_escape "$desc")")
  head_html=$(replace_all "$head_html" '{{CANONICAL}}' "$page_url")
  head_html=$(replace_all "$head_html" '{{SITE_URL}}' "$SITE_URL")

  # FAQ: pages/<slug>.faq holds "Q:" / "A:" lines. It becomes the visible
  # section at <!-- FAQ --> in the page and FAQPage structured data.
  content=$(cat "$body")
  faq_items="" faq_json=""
  if [ -f "pages/${slug}.faq" ]; then
    [[ $content == *"<!-- FAQ -->"* ]] || { echo "pages/${slug}.faq exists but ${body} has no <!-- FAQ --> marker" >&2; exit 1; }
    q=""
    while IFS= read -r line || [ -n "$line" ]; do
      case $line in
        "Q: "*) q=${line#Q: } ;;
        "A: "*)
          a=${line#A: }
          faq_items+="        <details class=\"faq__item\"><summary>$(html_escape "$q")</summary><p>$(html_escape "$a")</p></details>"$'\n'
          faq_json+="${faq_json:+,}{\"@type\":\"Question\",\"name\":\"$(json_escape "$q")\",\"acceptedAnswer\":{\"@type\":\"Answer\",\"text\":\"$(json_escape "$a")\"}}"
          ALL_FAQS+="### ${q}"$'\n\n'"${a}"$'\n\n'
          ;;
      esac
    done < "pages/${slug}.faq"
    faq_section="  <section class=\"section section--dark\" id=\"faq\">
    <div class=\"wrap\">
      <div class=\"section-head\">
        <p class=\"eyebrow\">Questions</p>
        <h2 class=\"h-lg\">Frequently asked questions</h2>
      </div>
      <div class=\"faq\">
${faq_items}      </div>
    </div>
  </section>"
    content=$(replace_all "$content" "<!-- FAQ -->" "$faq_section")
  fi

  page_type='"WebPage"'
  [ -n "$faq_json" ] && page_type='["WebPage","FAQPage"]'
  webpage='{"@type":'"$page_type"',"@id":"'"$page_url"'#webpage","url":"'"$page_url"'","name":"'"$(json_escape "$title")"'","description":"'"$(json_escape "$desc")"'",'\
'"isPartOf":{"@id":"'"$SITE_URL"'/#website"},"about":{"@id":"'"$ORG_ID"'"},"inLanguage":"en-US"'
  graph="$ORG_JSON,$WEBSITE_JSON"
  if [ -n "$crumb" ]; then
    webpage+=',"breadcrumb":{"@id":"'"$page_url"'#breadcrumb"}'
    graph+=',{"@type":"BreadcrumbList","@id":"'"$page_url"'#breadcrumb","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"'"$SITE_URL"'/"},{"@type":"ListItem","position":2,"name":"'"$(json_escape "$crumb")"'","item":"'"$page_url"'"}]}'
  fi
  [ -n "$faq_json" ] && webpage+=',"mainEntity":['"$faq_json"']'
  graph+=",$webpage}"
  schema='<script type="application/ld+json">{"@context":"https://schema.org","@graph":['"$graph"']}</script>'
  head_html=$(replace_all "$head_html" '{{SCHEMA}}' "$schema")

  # Mark the nav link for the current page, then drop the marker attribute.
  header_html=$(replace_all "$(cat partials/header.html)" \
    "data-nav href=\"${slug}.html\"" "href=\"${slug}.html\" aria-current=\"page\"")
  header_html=$(replace_all "$header_html" 'data-nav ' '')

  {
    printf '%s\n' "$head_html"
    printf '%s\n' "$header_html"
    printf '%s\n' "$content"
    cat partials/footer.html
  } > "${slug}.html"

  echo "built ${slug}.html"
done

# --------------------------------------------------------------- sitemap ---
{
  printf '%s\n' '<?xml version="1.0" encoding="UTF-8"?>'
  printf '%s\n' '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
  for entry in "${PAGES[@]}"; do
    IFS='|' read -r slug _ <<<"$entry"
    if [ "$slug" = "index" ]; then loc="$SITE_URL/"; else loc="$SITE_URL/${slug}.html"; fi
    printf '  <url><loc>%s</loc></url>\n' "$loc"
  done
  printf '%s\n' '</urlset>'
} > sitemap.xml
echo "built sitemap.xml"

cat > robots.txt <<EOF
# Search engines and AI assistants are welcome to read the site.
User-agent: *
Allow: /

# AI search and assistant crawlers, listed explicitly so answers about
# Beltway Demolition in ChatGPT, Claude, Perplexity, Gemini and Copilot stay current.
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: Bingbot
Allow: /

Sitemap: $SITE_URL/sitemap.xml
EOF
echo "built robots.txt"

# ---------------------------------------------------------------- llms.txt ---
# A plain-text summary for AI assistants (llmstxt.org), from the same page list
# and FAQ files as the site so it never drifts.
{
  cat <<EOF
# Beltway Demolition

> Beltway Demolition is a demolition and site clearance contractor working across Maryland, Washington DC and Virginia. It takes structures down, clears what is left and hands back a site ready for its next use. It is backed by WMB LLC, which holds a construction contractor licence in the State of Maryland.

## Company facts

- Name: Beltway Demolition
- Website: $SITE_URL/
- Business type: demolition and site clearance contractor
- Backing and licensing: backed by WMB LLC (https://wmbre.com), which holds a construction contractor licence in the State of Maryland; licence documentation and certificates of insurance available on request
- Service area: Maryland, Washington DC, Virginia and the surrounding Mid-Atlantic
- Services: demolition (full, selective and interior); environmental and abatement; site clearance and grading; asset recovery and recycling; permits and project management; hauling and disposal
- Typical clients: property owners, general contractors, commercial and industrial clients, municipal and institutional clients
- Phone: +1 (703) 861-5354
- Email: $EMAIL

## Pages

EOF
  for entry in "${PAGES[@]}"; do
    IFS='|' read -r slug title desc _ <<<"$entry"
    if [ "$slug" = "index" ]; then loc="$SITE_URL/"; else loc="$SITE_URL/${slug}.html"; fi
    printf -- '- [%s](%s): %s\n' "$title" "$loc" "$desc"
  done
  printf '\n## Frequently asked questions\n\n%s' "$ALL_FAQS"
} > llms.txt
echo "built llms.txt"
