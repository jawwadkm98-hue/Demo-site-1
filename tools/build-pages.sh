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

# slug|title|description
PAGES=(
"index|Beltway Demolition — Demolition & Site Clearance in Maryland, DC & Virginia|A construction and demolition contractor serving Maryland, Washington DC and Virginia. Backed by WMB LLC, a licensed Maryland construction contractor."
"about|About Us — Beltway Demolition|Who we are, how we work, and the licensing and backing behind the company."
"services|Services — Beltway Demolition|Demolition, environmental remediation, site clearance, asset recovery and construction management."
"areas-we-serve|Areas We Serve — Beltway Demolition|Serving Maryland, Washington DC, Virginia and the surrounding Mid-Atlantic."
"contact|Contact — Beltway Demolition|Talk to us about a shuttered facility, an environmental liability or a redevelopment opportunity."
"privacy-policy|Privacy Policy — Beltway Demolition|How this site collects, uses and protects personal information."
)

for entry in "${PAGES[@]}"; do
  IFS='|' read -r slug title desc <<<"$entry"
  body="pages/${slug}.html"
  [ -f "$body" ] || { echo "missing $body" >&2; exit 1; }

  head_html=$(replace_all "$(cat partials/head.html)" '{{TITLE}}' "$(html_escape "$title")")
  head_html=$(replace_all "$head_html" '{{DESC}}' "$(html_escape "$desc")")

  # Mark the nav link for the current page, then drop the marker attribute.
  header_html=$(replace_all "$(cat partials/header.html)" \
    "data-nav href=\"${slug}.html\"" "href=\"${slug}.html\" aria-current=\"page\"")
  header_html=$(replace_all "$header_html" 'data-nav ' '')

  {
    printf '%s\n' "$head_html"
    printf '%s\n' "$header_html"
    cat "$body"
    cat partials/footer.html
  } > "${slug}.html"

  echo "built ${slug}.html"
done
