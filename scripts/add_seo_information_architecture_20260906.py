from pathlib import Path
p=Path('seo/generate_seo.py')
s=p.read_text(encoding='utf-8')
old="body='<h1>Cancer Treatment Options and Clinical Trials for Dogs and Cats</h1><p>Find current canine and feline cancer treatment options, clinical trials, advanced treatments and experimental therapies by diagnosis and region.</p><ul>'+''.join(f'<li><a href=\"{SITE}/{p}\">{esc(n)}</a></li>' for n,p in sorted(index))+'</ul>'"
new="""body='''<h1>Cancer Treatment Options and Clinical Trials for Dogs and Cats</h1>
<p>Find current canine and feline cancer treatment options, clinical trials, advanced treatments and experimental therapies by diagnosis and region.</p>
<h2>Find Cancer Treatment Options</h2><p>Start with your pet's cancer type and location. The live finder screens current treatment-focused opportunities and links to the treating or research program.</p>
<h2>Clinical Trials</h2><p>We track treatment trials for client-owned dogs and cats and remove observational, sample-only and diagnostic studies from treatment matching.</p>
<h2>More Treatment Options</h2><p>Beyond clinical trials, the finder also highlights selected advanced or less-common oncology treatments when a real patient access route can be verified.</p>
<h2>Electrochemotherapy</h2><p>Search veterinary centers offering electrochemotherapy, a local cancer treatment used for selected tumors in dogs and cats.</p>
<h2>Cancer Types</h2><p>Browse current treatment opportunities by diagnosis, including lymphoma, osteosarcoma, mast cell tumor, melanoma, soft tissue sarcoma, squamous cell carcinoma and other cancers represented in the live catalog.</p>
<h2>How It Works</h2><p>The catalog is built from current university, veterinary hospital, research-center and treatment-program sources. Listings are checked regularly, but the treating team always makes the final eligibility and enrollment decision.</p>
<h2>Current Treatment Pages</h2><ul>'''+''.join(f'<li><a href=\"{SITE}/{p}\">{esc(n)}</a></li>' for n,p in sorted(index))+'</ul>'"""
if old not in s: raise SystemExit('index body marker not found')
s=s.replace(old,new)
# Add concise explanatory copy to English diagnosis pages without creating doorway pages.
old2="body=f'<h1>{esc(h1)}</h1><p>{esc(LANGS[lang][1])}: <strong>{len(hit)}</strong>.</p>{cards(hit)}'"
new2="body=f'<h1>{esc(h1)}</h1><p>{esc(LANGS[lang][1])}: <strong>{len(hit)}</strong>.</p>'+((f'<p>This page brings together current treatment-focused options for {label} in {sname.lower()}s, including clinical trials and investigational or advanced treatment programs represented in our live catalog. Use the finder to review location and eligibility details.</p>' if lang=='en' else ''))+cards(hit)"
if old2 not in s: raise SystemExit('diagnosis body marker not found')
s=s.replace(old2,new2)
p.write_text(s,encoding='utf-8')
