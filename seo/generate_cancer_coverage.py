#!/usr/bin/env python3
from __future__ import annotations

import generate_seo as g
import generate_seo_strict as s


def main():
    rows = s.load_effective()
    cancer_keys = [key for key, _aliases in g.CANONICAL_RULES]
    counts = {key: 0 for key in cancer_keys}
    for row in rows:
        for key in s.row_cancers(row):
            if key in counts:
                counts[key] += 1

    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], g.display_name(kv[0])))
    groups = []
    bands = (
        ('Many current options', lambda n: n >= 5),
        ('Several current options', lambda n: 2 <= n < 5),
        ('One current option', lambda n: n == 1),
        ('No current verified option', lambda n: n == 0),
    )
    for label, predicate in bands:
        items = [(key, n) for key, n in ranked if predicate(n)]
        if not items:
            continue
        cards = ''.join(
            '<div class="coverage-card"><strong>' + g.esc(g.display_name(key)) + '</strong>'
            '<span>' + str(n) + ' ' + ('opportunity' if n == 1 else 'opportunities') + '</span></div>'
            for key, n in items
        )
        groups.append(
            '<section class="coverage-group"><h2>' + g.esc(label) + '</h2>'
            '<div class="coverage-grid">' + cards + '</div></section>'
        )

    url = f'{g.SITE}/cancer-coverage/'
    body = (
        '<div class="coverage-page"><h1>Cancer Trial Coverage</h1>'
        '<p class="lead">A quick view of how many current verified treatment opportunities are in the database for each major cancer type. Counts change as studies open and close.</p>'
        + ''.join(groups)
        + '<p><a class="cta" href="' + g.FINDER + '">Check your pet against current trials</a></p></div>'
    )
    out = g.OUT / 'cancer-coverage'
    out.mkdir(parents=True, exist_ok=True)
    rendered = g.page(
        'Cancer Trial Coverage',
        'Current verified veterinary cancer treatment opportunities by cancer type.',
        body,
        url,
    )
    css = '.coverage-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px}.coverage-card{background:#fff;border:1px solid #d9e2ea;border-radius:12px;padding:13px 14px;display:flex;justify-content:space-between;gap:12px}.coverage-card span{color:#607086;font-size:.9rem;white-space:nowrap}.coverage-group h2{margin-top:26px}@media(max-width:600px){.coverage-card{align-items:flex-start}.coverage-card span{white-space:normal;text-align:right}}'
    rendered = rendered.replace('</style>', css + '</style>', 1)
    (out / 'index.html').write_text(rendered, encoding='utf-8')

    home = g.OUT / 'index.html'
    home_html = home.read_text(encoding='utf-8')
    link = '<p><a href="' + url + '"><strong>See cancer trial coverage by cancer type →</strong></a></p>'
    if link not in home_html:
        home_html = home_html.replace('<h2>Current treatment pages</h2>', link + '<h2>Current treatment pages</h2>', 1)
        home.write_text(home_html, encoding='utf-8')

    sitemap = g.OUT / 'sitemap.xml'
    sitemap_html = sitemap.read_text(encoding='utf-8')
    entry = f'<url><loc>{g.esc(url)}</loc></url>\n'
    if entry not in sitemap_html:
        sitemap.write_text(sitemap_html.replace('</urlset>', entry + '</urlset>'), encoding='utf-8')

    print('CANCER_COVERAGE_OK', len(counts), sum(n > 0 for n in counts.values()), sum(n == 0 for n in counts.values()))


if __name__ == '__main__':
    main()
