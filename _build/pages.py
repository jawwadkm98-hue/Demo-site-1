"""Page registry: URL, output file, <title>, meta description, breadcrumb and schema options.
Titles aim for <=60 characters, descriptions for <=155."""

SERVE_MD = ["Maryland", "Prince George's County, MD", "Montgomery County, MD", "Anne Arundel County, MD", "Charles County, MD"]

PAGES = [
    dict(path="/", file="index.html", content="index.html", nav="/", priority="1.0", business_ld=True,
         title="Demolition Contractor in Maryland | Beltway Demolition",
         description="Maryland demolition contractor for houses, commercial buildings and interior gut-outs. "
                     "A division of WMB LLC, MHIC #{{MHIC}}. Free quotes: {{PHONE}}."),
    dict(path="/services", file="services.html", content="services.html", nav="/services", priority="0.9",
         crumbs=[("Services", "/services")],
         title="Demolition Services in Maryland | Beltway Demolition",
         description="House teardowns, commercial and interior demolition, concrete removal, site clearing and "
                     "hauling across Maryland. Fixed written quotes."),
    dict(path="/residential-demolition", file="residential-demolition.html", content="residential-demolition.html",
         nav="/services", priority="0.9", crumbs=[("Services", "/services"), ("Residential Demolition", "/residential-demolition")],
         service=dict(type="Residential demolition", name="House and residential demolition", areas=SERVE_MD),
         title="House Demolition Contractor in Maryland | Beltway Demolition",
         description="Full house teardowns, garage, shed, deck and pool removal across Maryland. Permits, utility "
                     "disconnects and hauling handled. MHIC #{{MHIC}}."),
    dict(path="/interior-demolition", file="interior-demolition.html", content="interior-demolition.html",
         nav="/services", priority="0.9", crumbs=[("Services", "/services"), ("Interior Demolition", "/interior-demolition")],
         service=dict(type="Interior demolition", name="Interior and selective demolition", areas=SERVE_MD),
         title="Interior & Selective Demolition in Maryland | Beltway Demolition",
         description="Interior gut-outs, tenant strip-outs, kitchen and bath tear-outs and selective demolition in "
                     "occupied buildings across Maryland. MHIC #{{MHIC}}."),
    dict(path="/commercial-demolition", file="commercial-demolition.html", content="commercial-demolition.html",
         nav="/services", priority="0.9", crumbs=[("Services", "/services"), ("Commercial Demolition", "/commercial-demolition")],
         service=dict(type="Commercial demolition", areas=SERVE_MD),
         title="Commercial Demolition in Maryland | Beltway Demolition",
         description="Commercial building demolition, retail and office strip-outs and site clearing for owners, "
                     "developers and general contractors across Maryland."),
    dict(path="/concrete-removal", file="concrete-removal.html", content="concrete-removal.html",
         nav="/services", priority="0.8", crumbs=[("Services", "/services"), ("Concrete Removal", "/concrete-removal")],
         service=dict(type="Concrete removal", name="Concrete, slab and foundation removal", areas=SERVE_MD),
         title="Concrete, Slab & Foundation Removal in MD | Beltway Demolition",
         description="Slab, foundation, footing, driveway and patio removal across Maryland, with concrete "
                     "hauled to recycling where practical. Written quotes."),
    dict(path="/areas-we-serve", file="areas-we-serve.html", content="areas-we-serve.html", nav="/areas-we-serve",
         priority="0.8", crumbs=[("Areas We Serve", "/areas-we-serve")],
         title="Maryland Demolition Service Areas | Beltway Demolition",
         description="Demolition contractor based in National Harbor, MD serving Prince George's, Montgomery, Charles "
                     "and Anne Arundel counties and across Maryland."),
    dict(path="/demolition-prince-georges-county-md", file="demolition-prince-georges-county-md.html",
         content="demolition-prince-georges-county-md.html", nav="/areas-we-serve", priority="0.9",
         crumbs=[("Areas We Serve", "/areas-we-serve"), ("Prince George's County, MD", "/demolition-prince-georges-county-md")],
         service=dict(type="Demolition", name="Demolition in Prince George's County, MD",
                      areas=["Prince George's County, MD"]),
         title="Demolition Contractor in Prince George's County, MD | Beltway",
         description="House, commercial and interior demolition in Prince George's County, MD, from our base in "
                     "National Harbor. DPIE permits and WSSC disconnects coordinated."),
    dict(path="/demolition-montgomery-county-md", file="demolition-montgomery-county-md.html",
         content="demolition-montgomery-county-md.html", nav="/areas-we-serve", priority="0.8",
         crumbs=[("Areas We Serve", "/areas-we-serve"), ("Montgomery County, MD", "/demolition-montgomery-county-md")],
         service=dict(type="Demolition", name="Demolition in Montgomery County, MD", areas=["Montgomery County, MD"]),
         title="Demolition Contractor in Montgomery County, MD | Beltway",
         description="Teardowns for new builds, interior and commercial demolition in Silver Spring, Bethesda, "
                     "Rockville and across Montgomery County, MD. MHIC #{{MHIC}}."),
    dict(path="/demolition-anne-arundel-county-md", file="demolition-anne-arundel-county-md.html",
         content="demolition-anne-arundel-county-md.html", nav="/areas-we-serve", priority="0.8",
         crumbs=[("Areas We Serve", "/areas-we-serve"), ("Anne Arundel County, MD", "/demolition-anne-arundel-county-md")],
         service=dict(type="Demolition", name="Demolition in Anne Arundel County, MD", areas=["Anne Arundel County, MD"]),
         title="Demolition Contractor in Anne Arundel County, MD | Beltway",
         description="House, commercial and interior demolition and concrete removal in Annapolis, Glen Burnie, "
                     "Severna Park, Odenton and across Anne Arundel County, MD."),
    dict(path="/faq", file="faq.html", content="faq.html", nav="/faq", priority="0.7", faq_ld=True,
         crumbs=[("FAQ", "/faq")],
         title="Demolition FAQ: Permits, Costs & Process | Beltway Demolition",
         description="Answers to common demolition questions in Maryland: permits, utility disconnects, "
                     "asbestos surveys, timelines, pricing and what to expect."),
    dict(path="/about", file="about.html", content="about.html", nav="/about", priority="0.6",
         crumbs=[("About", "/about")],
         title="About Beltway Demolition | Licensed MD Contractor (WMB LLC)",
         description="Beltway Demolition is the demolition division of WMB LLC, licensed in Maryland "
                     "(MHIC #{{MHIC}}, MD HBR #{{HBR}}). How we work and what we put in writing."),
    dict(path="/contact", file="contact.html", content="contact.html", nav=None, priority="0.8", business_ld=True,
         crumbs=[("Contact", "/contact")],
         title="Get a Free Demolition Quote | Beltway Demolition",
         description="Send your address and a few photos for a free, written demolition quote anywhere in Maryland. "
                     "Call {{PHONE}} or request a site visit online."),
    dict(path="/privacy-policy", file="privacy-policy.html", content="privacy-policy.html", nav=None, priority="0.2",
         crumbs=[("Privacy Policy", "/privacy-policy")],
         title="Privacy Policy | Beltway Demolition",
         description="How the Beltway Demolition website collects, uses and protects the information you send us."),
    dict(path="/404", file="404.html", content="404.html", nav=None, noindex=True,
         title="Page Not Found | Beltway Demolition",
         description="The page you were looking for could not be found."),
]
