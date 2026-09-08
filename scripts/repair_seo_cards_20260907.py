from pathlib import Path
import re
p=Path('seo/generate_seo.py')
s=p.read_text()
start=s.index('def page(')
end=s.index('\ndef main():', start)
replacement=r'''def page(title,desc,body,canonical,lang='en',alternates=None):
 alts=''.join(f'<link rel="alternate" hreflang="{k}" href="{v}">' for k,v in (alternates or {}).items())
 css='''body{font-family:system-ui,-apple-system,sans-serif;max-width:860px;margin:auto;padding:24px 20px;line-height:1.55;color:#17243b;background:#fff}header{margin-bottom:28px}header a{font-size:1.05rem}h1{font-size:clamp(2rem,6vw,3.2rem);line-height:1.12;margin:.35em 0 .55em}a{color:#175b8c}article{border:1px solid #d9e2ea;border-radius:14px;padding:20px;margin:18px 0;background:#fff}article h3{font-size:1.35rem;line-height:1.25;margin:0 0 12px}.meta{margin:6px 0}.status{font-weight:650}.detail{margin:10px 0}.label{font-weight:700}.source{display:inline-block;margin-top:8px}.cta{display:inline-block;padding:11px 16px;background:#17243b;color:white;text-decoration:none;border-radius:8px;font-weight:650;max-width:100%;box-sizing:border-box}@media(max-width:600px){body{padding:18px 16px}article{padding:16px}h1{font-size:2.25rem}.cta{display:block;width:100%;text-align:center}}'''
 return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canonical}">{alts}<style>{css}</style></head><body><header><a href="{SITE}/"><strong>Cancer Trial Finder For Dogs And Cats</strong></a><p>Free. No registration, email or paywall.</p></header><main>{body}<p><a class="cta" href="{FINDER}">{esc(LANGS[lang][2])}</a></p><p>Answer a few questions about your pet to find potentially matching clinical trials and other cancer treatment options.</p><p><small>Listings change. Final eligibility and enrollment decisions are made by each research team.</small></p></main></body></html>'''

def _text(v):
 if isinstance(v,list): return '; '.join(str(x) for x in v if x)
 return str(v or '').strip()

def cards(rows):
 out=[]
 for r in rows:
  parts=[f'<article><h3>{esc(r.get("title"))}</h3>',f'<p class="meta"><strong>{esc(r.get("center"))}</strong> · {esc(r.get("country"))}</p>']
  if r.get('status'): parts.append(f'<p class="status">{esc(r.get("status"))}</p>')
  treatment=_text(r.get('intervention') or r.get('treatment') or r.get('notes'))
  if treatment: parts.append(f'<p class="detail"><span class="label">Treatment:</span> {esc(treatment)}</p>')
  req=_text(r.get('requires'))
  if req: parts.append(f'<p class="detail"><span class="label">Key eligibility:</span> {esc(req)}</p>')
  exc=_text(r.get('excludes'))
  if exc: parts.append(f'<p class="detail"><span class="label">Important exclusions:</span> {esc(exc)}</p>')
  funding=_text(r.get('funding'))
  if funding: parts.append(f'<p class="detail"><span class="label">Funding / cost:</span> {esc(funding)}</p>')
  contacts=_text(r.get('contacts'))
  if contacts: parts.append(f'<p class="detail"><span class="label">Contact:</span> {esc(contacts)}</p>')
  if r.get('url'): parts.append(f'<a class="source" href="{esc(r.get("url"))}" rel="noopener">Official study / treatment page</a>')
  parts.append('</article>'); out.append(''.join(parts))
 return ''.join(out)
'''
s=s[:start]+replacement+s[end:]
p.write_text(s)
