# Before this site goes live

Everything on the site is either true or deliberately left blank. Nothing is
invented. This file lists what still needs a real value, and where it lives.

Edit the sources under `partials/` and `pages/` — never the built HTML at the
repo root — then run `./tools/build-pages.sh`.

## Must fix — these are placeholders that look real

| What | Placeholder now | Where |
| --- | --- | --- |
| Company name | "Meridian Industrial Group" | everywhere — see **Renaming** in README.md |
| Maryland licence number | `#000000` | `partials/footer.html`, `pages/about.html` |
| Phone | `+1 (555) 010-4400` | `partials/header.html`, `partials/footer.html`, `pages/index.html`, `pages/contact.html` |
| Email | `hello@example.com` | `partials/footer.html`, `pages/contact.html` |
| Privacy contact | `privacy@example.com` | `pages/privacy-policy.html` |

`555-01xx` numbers and `example.com` addresses are reserved for fiction, so
they are safe to ship by accident — but they are useless to a customer.

## Check before publishing — claims a client could verify

- **Licence wording.** The site says the company "is backed by WMB LLC, which
  holds a construction contractor licence in the State of Maryland." Confirm
  that describes the arrangement correctly, and name the issuing body if the
  licence type should be stated (MHIC, or a county/trade licence).
- **Insurance.** The site says certificates are issued before mobilisation and
  available on request. Make sure that is operationally true.
- **Services.** Six are listed in `pages/services.html`. **Delete any the
  company does not actually perform** — particularly asbestos and lead
  abatement, which require separate licensing in Maryland.
- **Service area.** `pages/areas-we-serve.html` lists six regions and a dozen
  towns. Trim to where you will genuinely travel.
- **Privacy policy.** `pages/privacy-policy.html` is generic boilerplate, not
  legal advice. Have it reviewed or replaced.

## Worth adding once you have it

These were deliberately left out rather than guessed at. Each is a strong
credibility signal *when true*:

- Years in business, and the founding year
- Number of staff and crews
- Completed project count, or a handful of named jobs with photos
- Real project photography (see `assets/img/photos/` guidance in README.md)
- Client references or testimonials
- Bonding capacity, if bonded
- Trade association memberships, if held
- Safety record (EMR / TRIR), if tracked

## Deliberately removed

An earlier draft of this site presented the company as a multi-billion-dollar
listed group. All of it was invented and none of it is recoverable as fact, so
it was removed: a stock listing and share price, SEC filings, an investor
relations page with financial statements, ENR rankings, ISO and OSHA
accreditations, twenty-four operating companies, a board of directors and
executive team, employee and revenue figures, and an international footprint.

Those pages still exist in git history if you want to look at the layouts, but
do not reinstate the claims. Published capability and financial claims are
exactly what clients, prequalification bodies and licensing boards check.
