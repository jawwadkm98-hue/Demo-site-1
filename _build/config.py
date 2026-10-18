"""
ONE PLACE FOR BUSINESS DETAILS.
Change a value here, then run:  python3 _build/build.py
Every page, the footer, the header phone link, the contact page and the
JSON-LD structured data are regenerated from these values.
"""

BUSINESS_NAME = "Beltway Demolition"
PARENT_COMPANY = "WMB LLC"
PARENT_URL = "https://wmbre.com/"

# --- Public phone -----------------------------------------------------------
# Current public number (per owner, Oct 18 2026). To change it, edit BOTH lines
# (display format and +1 E.164 format), then rebuild.
PHONE_DISPLAY = "(703) 861-5354"
PHONE_E164 = "+17038615354"

# --- Public email -----------------------------------------------------------
# Public site email (per owner). Alternative: "jawwad@beltwaydemo.com"
EMAIL = "info@beltwaydemo.com"

# --- Address & licensing (from the WMB LLC Maryland license record) ---------
STREET = "145 Fleet St #142"
CITY = "National Harbor"
REGION = "MD"
POSTAL = "20745"
MHIC = "154299"          # Maryland Home Improvement Commission license
MD_HBR = "9597"          # Maryland Home Builder Registration

# --- Contact form -----------------------------------------------------------
# Create a form at https://formspree.io (free tier is fine), then paste its
# endpoint here (have it deliver to the EMAIL above), e.g. "https://formspree.io/f/abcdwxyz".
# While this still says FORM_ENDPOINT the form shows a "call or email us"
# message instead of pretending to submit.
FORM_ENDPOINT = "FORM_ENDPOINT"

SITE_URL = "https://beltwaydemo.com"
ASSET_VERSION = "20261018"   # bump when styles.css / main.js change (cache-busting)
