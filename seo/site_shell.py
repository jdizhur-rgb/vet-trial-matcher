#!/usr/bin/env python3
"""Give the generated SEO site one shared navigation, homepage and section pages."""
from __future__ import annotations
import re, shutil
from pathlib import Path
import generate_seo as g
from site_config import SITE

FINDER=g.FINDER

NAV=f'''<header class="site-header"><div class="site-nav"><a class="brand" href="{SITE}/">Vet Trial Finder</a><nav><a href="{SITE}/">Home</a><a href="{FINDER}">Find Trials</a><a href="{SITE}/cancer-types/">Cancer Types</a><a href="{SITE}/centers/">Oncology Centers</a><a href="{SITE}/other-treatments/">Other Treatments</a><a href="{SITE}/help/">Help</a></nav></div></header>'''

SHELL_CSS='''
.site-header{background:#fff;border-bottom:1px solid #dfe6ec;position:sticky;top:0;z-index:20;margin:0 -20px 24px;padding:0 20px}.site-nav{max-width:1040px;margin:auto;display:flex;align-items:center;justify-content:space-between;gap:20px;min-height:64px}.brand{font-size:1.08rem;font-weight:800;color:#17324d;text-decoration:none;white-space:nowrap}.site-nav nav{display:flex;gap:18px;align-items:center;flex-wrap:wrap;justify-content:flex-end}.site-nav nav a{text-decoration:none;font-weight:650;color:#40546a}.site-nav nav a:hover{color:#175b8c}.site-footer{margin-top:46px;padding:24px 0 4px;border-top:1px solid #dce4ec;color:#607086;font-size:.9rem}.site-footer a{margin-right:14px}.home-hero{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(230px,.65fr);gap:36px;align-items:center;padding:42px 0 26px}.home-hero h1{margin:0 0 14px;max-width:760px}.home-hero .lead{max-width:700px}.eyebrow{font-weight:750;color:#567188;margin:0 0 9px}.hero-actions{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}.secondary-cta{display:inline-block;border:1px solid #b8c8d6;background:#fff;color:#175b8c!important;text-decoration:none;font-weight:750;padding:11px 17px;border-radius:9px}.pet-panel{display:grid;grid-template-columns:1fr 1fr;gap:14px}.pet-tile{background:#fff;border:1px solid #d9e2ea;border-radius:20px;min-height:150px;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 28px rgba(23,36,59,.08)}.pet-tile span{font-size:4.6rem;line-height:1}.site-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:18px 0 34px}.site-card{display:block;background:#fff;border:1px solid #d9e2ea;border-radius:14px;padding:20px;text-decoration:none;color:inherit}.site-card:hover{border-color:#9db7cc;box-shadow:0 4px 16px rgba(23,36,59,.06)}.site-card h3{margin:0 0 7px;color:#17324d}.site-card p{margin:0;color:#607086}.how{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.how div{background:#edf4f8;border-radius:14px;padding:18px}.how strong{display:block;margin-bottom:5px}.section-index{columns:2;column-gap:30px}.section-index li{break-inside:avoid;margin:0 0 7px}.share-panel{display:grid;grid-template-columns:minmax(0,.85fr) minmax(260px,1.15fr);gap:26px;align-items:center;background:#fff;border:1px solid #d9e2ea;border-radius:16px;padding:22px;margin:34px 0}.share-panel img{display:block;width:100%;max-width:430px;border-radius:12px;border:1px solid #e4e9ee}.share-panel h2{margin-top:0}.share-panel p{color:#52677b}@media(max-width:800px){.site-header{position:static}.site-nav{display:block;padding:14px 0}.site-nav nav{justify-content:flex-start;margin-top:10px;gap:12px 16px}.home-hero{grid-template-columns:1fr;padding-top:24px}.pet-panel{max-width:360px}.site-grid,.how{grid-template-columns:1fr 1fr}.share-panel{grid-template-columns:1fr}}@media(max-width:560px){.site-header{margin-left:-15px;margin-right:-15px;padding:0 15px}.site-nav nav{font-size:.92rem}.site-grid,.how{grid-template-columns:1fr}.section-index{columns:1}.pet-tile{min-height:120px}.pet-tile span{font-size:3.8rem}}
'''

FOOTER=f'''<footer class="site-footer"><p><a href="{SITE}/help/">Help</a><a href="{SITE}/centers/">Oncology Centers</a><a href="{SITE}/cancer-types/">Cancer Types</a></p><p>Vet Trial Finder is free to use. Final eligibility and enrollment decisions are made by each research or treatment team.</p></footer>'''


def wrap_html(text:str)->str:
    text=re.sub(r'<header>.*?</header>',NAV,text,count=1,flags=re.S)
    if NAV not in text:
        text=text.replace('<main>',NAV+'<main>',1)
    text=text.replace('</style>',SHELL_CSS+'</style>',1)
    text=re.sub(r'<footer>.*?</footer>',FOOTER,text,count=1,flags=re.S)
    if FOOTER not in text:
        text=text.replace('</main>','</main>'+FOOTER,1)
    return text


def cancer_index(root:Path)->None:
    items=[]
    for key in sorted(g.DISEASE_INFO):
        label=g.display_name(key); slug=g.slugify(key)
        items.append(f'<li><a href="{SITE}/north-america/dogs/{slug}/">{g.esc(label)} in dogs</a> · <a href="{SITE}/north-america/cats/{slug}/">cats</a></li>')
    body='<h1>Cancer Types</h1><p class="lead">Choose a cancer type to see current treatment studies and a short treatment overview.</p><ul class="section-index">'+''.join(items)+'</ul>'
    d=root/'cancer-types';d.mkdir(parents=True,exist_ok=True)
    (d/'index.html').write_text(g.page('Cancer Types | Vet Trial Finder','Browse dog and cat cancer types with current treatment studies and clinical trial listings.',body,f'{SITE}/cancer-types/'),encoding='utf-8')


def other_treatments(root:Path)->None:
    body=f'''<h1>Other Cancer Treatment Options</h1><p class="lead">Clinical trials are only one part of the site. We also keep track of selected treatments that can be hard to find in one place.</p><div class="site-grid"><a class="site-card" href="{FINDER}"><h3>Electrochemotherapy</h3><p>Find centers that offer ECT and check whether it may be worth asking about for a local tumor.</p></a><a class="site-card" href="{FINDER}"><h3>Advanced Treatments</h3><p>Selected newer or less widely available oncology treatments.</p></a><a class="site-card" href="{FINDER}"><h3>Expanded Access</h3><p>Programs that may provide access to treatment outside a standard clinical trial.</p></a></div><p>These options are not appropriate for every cancer or every pet. Use the listings to find a center or program, then confirm details with the treating team.</p>'''
    d=root/'other-treatments';d.mkdir(parents=True,exist_ok=True)
    (d/'index.html').write_text(g.page('Other Veterinary Cancer Treatments | Vet Trial Finder','Electrochemotherapy, advanced treatment options and expanded access programs for dogs and cats with cancer.',body,f'{SITE}/other-treatments/'),encoding='utf-8')


def homepage(root:Path)->None:
    body=f'''<section class="home-hero"><div><p class="eyebrow">Clinical Trials &amp; Experimental Treatments for Dogs and Cats</p><h1>Find clinical trials and cancer treatment options for your pet</h1><p class="lead">Search current studies by diagnosis, check participating hospitals, and find other oncology options in one place. The site is free to use.</p><div class="hero-actions"><a class="cta" href="{FINDER}">Find Trials</a><a class="secondary-cta" href="{SITE}/help/">How it works</a></div></div><div class="pet-panel" aria-label="Dogs and cats"><div class="pet-tile"><span aria-hidden="true">🐕</span></div><div class="pet-tile"><span aria-hidden="true">🐈</span></div></div></section><h2>Start here</h2><div class="site-grid"><a class="site-card" href="{FINDER}"><h3>Find Clinical Trials</h3><p>Enter the diagnosis and what you know about your pet. See studies that are worth checking.</p></a><a class="site-card" href="{SITE}/cancer-types/"><h3>Browse Cancer Types</h3><p>See current studies and treatment information by diagnosis.</p></a><a class="site-card" href="{SITE}/centers/"><h3>Find Oncology Centers</h3><p>Universities, teaching hospitals, specialty hospitals and research centers.</p></a><a class="site-card" href="{SITE}/centers/"><h3>Not Just Universities</h3><p>Some studies and treatments are available through specialty hospitals and other research programs too.</p></a><a class="site-card" href="{SITE}/other-treatments/"><h3>Other Treatments</h3><p>ECT, advanced treatment options and expanded access programs.</p></a><a class="site-card" href="{SITE}/help/"><h3>Help</h3><p>What a match means, what records to prepare, costs, travel and who to contact.</p></a></div><h2>How the finder works</h2><div class="how"><div><strong>1. Enter the diagnosis</strong><span>Add the details you know. Leave anything unknown rather than guessing.</span></div><div><strong>2. Review possible matches</strong><span>Read the study requirements, location, contact details and official source.</span></div><div><strong>3. Confirm with the study team</strong><span>A match is not final eligibility. The research team makes that decision.</span></div></div><section class="share-panel"><div><h2>Share the finder</h2><p>If another pet owner may need it, send them the site or let them scan the code on this card.</p><p><strong>vettrialfinder.com</strong></p></div><img src="/assets/trial-finder-promo.jpg" alt="Cancer Trial Finder information card with QR code"></section>'''
    (root/'index.html').write_text(g.page('Vet Trial Finder | Cancer Clinical Trials for Dogs and Cats','Free finder for veterinary cancer clinical trials, research centers and other treatment options for dogs and cats.',body,f'{SITE}/'),encoding='utf-8')


def add_to_sitemap(root:Path,urls:list[str])->None:
    p=root/'sitemap.xml'
    if not p.exists():return
    text=p.read_text(encoding='utf-8')
    for url in urls:
        if url not in text:text=text.replace('</urlset>',f'<url><loc>{g.esc(url)}</loc></url>\n</urlset>')
    p.write_text(text,encoding='utf-8')


def copy_assets(root:Path)->None:
    source=Path(__file__).resolve().parent/'assets'/'trial-finder-promo.jpg'
    if source.exists():
        dest=root/'assets';dest.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,dest/'trial-finder-promo.jpg')


def apply_site_shell(root:Path)->None:
    copy_assets(root);homepage(root);cancer_index(root);other_treatments(root)
    add_to_sitemap(root,[f'{SITE}/cancer-types/',f'{SITE}/other-treatments/',f'{SITE}/help/',f'{SITE}/centers/'])
    for p in root.rglob('index.html'):
        p.write_text(wrap_html(p.read_text(encoding='utf-8')),encoding='utf-8')
    print('SITE_SHELL_OK',len(list(root.rglob('index.html'))))
