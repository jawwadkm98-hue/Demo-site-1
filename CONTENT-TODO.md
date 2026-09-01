# Before this site goes live

Everything on the site is either true or deliberately left blank. Nothing is
invented. This file lists what still needs a real value, and where it lives.

Edit the sources under `partials/` and `pages/` — never the built HTML at the
repo root — then run `./tools/build-pages.sh`.

## Live details — set

| What | Value |
| --- | --- |
| Domain | `https://beltwaydemo.com` (`SITE_URL` in `tools/build-pages.sh`) |
| Phone | `+1 (703) 861-5354` |
| Email | `info@beltwaydemo.com` — also used for privacy enquiries |
| Maryland licence number | **Not published**, by request. The site states the WMB LLC backing and offers licence documentation on request. |

Make sure `info@beltwaydemo.com` actually receives mail — the site sends every
enquiry there, and the contact form's mail wiring is still outstanding (below).

## Check before publishing — claims a client could verify

- **Licence wording.** The site says the company "is backed by WMB LLC, which
  holds a construction contractor licence in the State of Maryland", and that
  licence documentation is available on request. No licence number is
  published. Confirm that wording describes the arrangement correctly.
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
- **Real project photography.** The images on the site now are generated
  placeholder illustrations, not photographs — see
  `assets/img/photos/README.md` for the six slots, what to shoot for each and
  how to swap them in. Before/after pairs of your own jobs are the single most
  persuasive thing you can add.
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
