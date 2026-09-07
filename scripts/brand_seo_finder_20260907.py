from pathlib import Path

p = Path('seo/generate_seo.py')
s = p.read_text(encoding='utf-8')

replacements = {
    "'en':('Clinical Trials and Cancer Treatment Studies','Current treatment-focused opportunities','Search current treatment opportunities'),": "'en':('Clinical Trials and Cancer Treatment Studies','Current treatment-focused opportunities','Search the Vet Cancer Trial Finder'),",
    '<strong>Cancer Trial Finder For Dogs And Cats</strong>': '<strong>Vet Cancer Trial Finder</strong>',
    '<main>{body}<p><a class="cta" href="{FINDER}">{esc(LANGS[lang][2])}</a></p><p><small>': '<main>{body}<p><a class="cta" href="{FINDER}">{esc(LANGS[lang][2])}</a></p><p>Answer a few questions about your pet to find potentially matching clinical trials and other cancer treatment options.</p><p><small>',
    "page('Cancer Treatment Options & Clinical Trials for Dogs and Cats'": "page('Vet Cancer Trial Finder | Treatment Options & Clinical Trials for Dogs and Cats'",
}

for old, new in replacements.items():
    if old not in s:
        raise SystemExit(f'Expected marker not found: {old}')
    s = s.replace(old, new)

p.write_text(s, encoding='utf-8')
print('Applied consistent Vet Cancer Trial Finder branding to SEO pages.')
