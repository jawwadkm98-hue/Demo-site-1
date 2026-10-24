"""Page registry: URL, output file, <title>, meta description, breadcrumb and schema options.
Titles aim for <=60 characters, descriptions for <=155."""

SERVE_MD = ["Maryland", "Prince George's County, MD", "Montgomery County, MD", "Anne Arundel County, MD", "Charles County, MD"]

PAGES = [
    dict(path="/", file="index.html", content="index.html", nav="/", priority="1.0", business_ld=True,
         title="Demolition Contractor in Maryland | Beltway Demolition",
         description="Full-service demolition contractor in Maryland for house teardowns, commercial buildings "
                     "and structural work. MHIC #{{MHIC}}. Free quotes: {{PHONE}}."),
    dict(path="/services", file="services.html", content="services.html", nav="/services", priority="0.9",
         crumbs=[("Services", "/services")],
         title="Demolition Services in Maryland | Beltway Demolition",
         description="House teardowns, commercial building demolition, structural and exterior work, concrete "
                     "removal and debris haul-off across Maryland."),
    dict(path="/residential-demolition", file="residential-demolition.html", content="residential-demolition.html",
         nav="/services", priority="0.9", crumbs=[("Services", "/services"), ("Residential Demolition", "/residential-demolition")],
         service=dict(type="Residential demolition", name="House and residential demolition", areas=SERVE_MD),
         title="House Demolition Contractor in Maryland | Beltway Demolition",
         description="House demolition in Maryland: full teardowns, structural removal, garages, sheds, decks "
                     "and pools. Permits and haul-off. MHIC #{{MHIC}}."),
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
         description="Commercial building demolition for owners, developers and general contractors across "
                     "Maryland. Structural teardown, site clearing and debris haul-off."),
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
         description="House teardowns and commercial building demolition in Prince George's County, MD, from "
                     "National Harbor. Structural work, concrete removal and haul-off."),
    dict(path="/demolition-montgomery-county-md", file="demolition-montgomery-county-md.html",
         content="demolition-montgomery-county-md.html", nav="/areas-we-serve", priority="0.8",
         crumbs=[("Areas We Serve", "/areas-we-serve"), ("Montgomery County, MD", "/demolition-montgomery-county-md")],
         service=dict(type="Demolition", name="Demolition in Montgomery County, MD", areas=["Montgomery County, MD"]),
         title="Demolition Contractor in Montgomery County, MD | Beltway",
         description="House teardowns and commercial building demolition in Silver Spring, Bethesda, Rockville "
                     "and across Montgomery County, MD. MHIC #{{MHIC}}."),
    dict(path="/demolition-anne-arundel-county-md", file="demolition-anne-arundel-county-md.html",
         content="demolition-anne-arundel-county-md.html", nav="/areas-we-serve", priority="0.8",
         crumbs=[("Areas We Serve", "/areas-we-serve"), ("Anne Arundel County, MD", "/demolition-anne-arundel-county-md")],
         service=dict(type="Demolition", name="Demolition in Anne Arundel County, MD", areas=["Anne Arundel County, MD"]),
         title="Demolition Contractor in Anne Arundel County, MD | Beltway",
         description="House teardowns and commercial building demolition in Annapolis, Glen Burnie, Severna "
                     "Park, Odenton and across Anne Arundel County, MD."),
    dict(path="/faq", file="faq.html", content="faq.html", nav="/faq", priority="0.7", faq_ld=True,
         crumbs=[("FAQ", "/faq")],
         title="Demolition FAQ: Permits, Costs & Process | Beltway Demolition",
         description="Answers to common demolition questions in Maryland: permits, utility disconnects, "
                     "asbestos surveys, timelines, pricing and what to expect."),
    dict(path="/about", file="about.html", content="about.html", nav="/about", priority="0.6",
         crumbs=[("About", "/about")],
         title="About Beltway Demolition | Licensed MD Contractor (WMB LLC)",
         description="Full-service demolition division of WMB LLC, licensed in Maryland "
                     "(MHIC #{{MHIC}}, MD HBR #{{HBR}}). House and commercial teardowns."),
    dict(path="/contact", file="contact.html", content="contact.html", nav=None, priority="0.8", business_ld=True,
         crumbs=[("Contact", "/contact")],
         title="Get a Free Demolition Quote | Beltway Demolition",
         description="Free written quote for a house teardown, commercial building or other demolition anywhere "
                     "in Maryland. Call {{PHONE}} or request a site visit online."),
    dict(path="/privacy-policy", file="privacy-policy.html", content="privacy-policy.html", nav=None, priority="0.2",
         crumbs=[("Privacy Policy", "/privacy-policy")],
         title="Privacy Policy | Beltway Demolition",
         description="How the Beltway Demolition website collects, uses and protects the information you send us."),
    dict(path="/404", file="404.html", content="404.html", nav=None, noindex=True,
         title="Page Not Found | Beltway Demolition",
         description="The page you were looking for could not be found."),
]
