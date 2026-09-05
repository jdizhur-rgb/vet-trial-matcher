# Cancer Trial Finder SEO layer

This directory is the source for a static, crawlable discovery site that sends owners to the existing Streamlit Cancer Trial Finder.

Principles:
- Finder remains the application and source of truth.
- SEO pages are generated from the effective treatment-only catalog, not maintained by hand.
- Start with useful cancer pages and broad geography pages; do not generate thin cancer × country combinations with no useful content.
- Every indexable page must be linked from the site navigation/index.
- Generate canonical URLs, sitemap.xml and robots.txt.
- Pages must clearly say availability changes and link owners to the live Finder for current matching.
- Never imply trial eligibility or guaranteed enrollment.

Initial page families:
- Core dog/cat cancer clinical trial landing page
- Cancer-specific pages: lymphoma, osteosarcoma, hemangiosarcoma, histiocytic sarcoma, mast cell tumor, melanoma, soft tissue sarcoma, oral squamous cell carcinoma, bladder/urothelial carcinoma, brain tumors, mammary cancer
- Geography pages: USA, Canada, Europe, UK

Deployment is intentionally separate from the Streamlit app. GitHub Pages can host the generated static HTML once the first build is reviewed.
