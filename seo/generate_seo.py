#!/usr/bin/env python3
"""Generate crawlable SEO pages from the effective veterinary oncology catalog."""
from __future__ import annotations
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "seo" / "site"
FINDER = "https://vet-cancer-trial-finder.streamlit.app/"
SITE = "https://jdizhur-rgb.github.io/vet-trial-matcher"

CANCERS = {
    "lymphoma": ["lymphoma"],
    "osteosarcoma": ["osteosarcoma"],
    "hemangiosarcoma": ["hemangiosarcoma"],
    "histiocytic-sarcoma": ["histiocytic sarcoma"],
    "mast-cell-tumor": ["mast cell"],
    "melanoma": ["melanoma"],
    "soft-tissue-sarcoma": ["soft tissue sarcoma"],
    "oral-squamous-cell-carcinoma": ["oral squamous", "oral scc"],
    "bladder-cancer": ["urothelial", "transitional cell", "bladder"],
    "brain-tumors": ["glioma", "meningioma", "brain tumor"],
    "mammary-cancer": ["mammary"],
}
GEOS = {"usa":"USA", "canada":"Canada", "europe":"Europe", "uk":"UK"}
EUROPE = {"Belgium","Denmark","France","Germany","Italy","Netherlands","Portugal","Spain","Sweden","Switzerland","UK","Ireland","Austria","Czechia","Poland","Finland","Norway","Hungary","Slovenia","Cyprus"}

def load_effective():
    base = json.loads((ROOT / "data" / "trials_base.json").read_text())
    upd = json.loads((ROOT / "data" / "trial_updates.json").read_text())
    rows = {r["id"]: r for r in base}
    for rid in upd.get("delete", []): rows.pop(rid, None)
    for patch in upd.get("upsert", []):
        rows[patch["id"]] = {**rows.get(patch["id"], {}), **patch}
    return [r for r in rows.values() if r.get("study_type") == "treatment" and r.get("available_for_matching") is True]

def esc(x): return html.escape(str(x or ""))
def cancer_text(r): return " ".join(r.get("cancers", [])).lower()
def title_slug(slug): return slug.replace("-", " ").title()
def cards(rows):
    if not rows: return "<p>No current matching opportunities are listed in this category. Check the live Finder because availability changes.</p>"
    parts=[]
    for r in rows:
        parts.append(f'<article><h3>{esc(r.get("title"))}</h3><p><strong>{esc(r.get("center"))}</strong> · {esc(r.get("country"))}</p><p>{esc(r.get("status"))}</p></article>')
    return "\n".join(parts)

def page(title, description, body, canonical, nav):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{canonical}"><style>body{{font-family:system-ui,sans-serif;max-width:900px;margin:auto;padding:28px;line-height:1.55;color:#17243b}}a{{color:#175b8c}}article{{border-top:1px solid #d9e2ea;padding:12px 0}}.cta{{display:inline-block;padding:12px 18px;background:#17243b;color:white;text-decoration:none;border-radius:8px}}nav a{{margin-right:12px}}</style></head><body><header><a href="{SITE}/"><strong>Cancer Trial Finder For Dogs And Cats</strong></a><p>Free. No registration, email or paywall.</p><nav>{nav}</nav></header><main>{body}<p><a class="cta" href="{FINDER}">Search current treatment opportunities</a></p><p><small>Listings change. The research team makes all final eligibility and enrollment decisions.</small></p></main></body></html>'''

def main():
    rows=load_effective(); OUT.mkdir(parents=True, exist_ok=True)
    links=[]
    cancer_pages=[]
    for slug, terms in CANCERS.items():
        hit=[r for r in rows if any(t in cancer_text(r) for t in terms)]
        label=title_slug(slug)
        path=f"cancer/{slug}/"; url=f"{SITE}/{path}"
        cancer_pages.append((label,path))
        body=f"<h1>{esc(label)} Clinical Trials and Treatment Studies for Dogs and Cats</h1><p>Current treatment-focused opportunities found in our veterinary oncology catalog: <strong>{len(hit)}</strong>.</p>{cards(hit)}"
        dest=OUT/path; dest.mkdir(parents=True,exist_ok=True); (dest/"index.html").write_text(page(f"{label} Clinical Trials for Dogs and Cats",f"Find current treatment-focused {label.lower()} clinical trials and advanced oncology studies for dogs and cats.",body,url,""),encoding="utf-8")
        links.append(url)
    geo_pages=[]
    for slug,country in GEOS.items():
        hit=[r for r in rows if (r.get("country") in EUROPE if country=="Europe" else r.get("country")==country)]
        label="United States" if country=="USA" else country
        path=f"location/{slug}/"; url=f"{SITE}/{path}"; geo_pages.append((label,path))
        body=f"<h1>Veterinary Cancer Clinical Trials in {esc(label)}</h1><p>Current treatment-focused opportunities in our catalog: <strong>{len(hit)}</strong>.</p>{cards(hit)}"
        dest=OUT/path; dest.mkdir(parents=True,exist_ok=True); (dest/"index.html").write_text(page(f"Veterinary Cancer Clinical Trials in {label}",f"Find current cancer treatment trials and advanced oncology studies for dogs and cats in {label}.",body,url,""),encoding="utf-8")
        links.append(url)
    nav=" ".join(f'<a href="{SITE}/{p}">{esc(n)}</a>' for n,p in cancer_pages[:6])
    body='<h1>Veterinary Cancer Clinical Trials for Dogs and Cats</h1><p>Search current treatment-focused clinical trials and advanced oncology opportunities. The Finder is free and does not require registration.</p><h2>Browse by cancer</h2><ul>'+''.join(f'<li><a href="{SITE}/{p}">{esc(n)}</a></li>' for n,p in cancer_pages)+'</ul><h2>Browse by location</h2><ul>'+''.join(f'<li><a href="{SITE}/{p}">{esc(n)}</a></li>' for n,p in geo_pages)+'</ul>'
    (OUT/"index.html").write_text(page("Cancer Trial Finder For Dogs And Cats","Free veterinary cancer clinical trial finder for dogs and cats.",body,SITE+"/",nav),encoding="utf-8")
    links.insert(0,SITE+"/")
    sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{u}</loc></url>\n' for u in links)+'</urlset>\n'
    (OUT/"sitemap.xml").write_text(sitemap,encoding="utf-8")
    (OUT/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n",encoding="utf-8")
    (OUT/".nojekyll").write_text("",encoding="utf-8")
    print(f"Generated {len(links)} indexable pages from {len(rows)} current treatment opportunities")
if __name__ == "__main__": main()
