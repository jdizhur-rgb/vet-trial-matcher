#!/usr/bin/env python3
"""Generate the owner-facing article about cancer clinical trials for pets."""
from __future__ import annotations

import json
from pathlib import Path

import generate_seo as g
from site_config import SITE
from site_shell import wrap_html

g.SITE = SITE
g.FINDER = f"{SITE}/matcher/"


def generate_clinical_trials_for_pets_article(root: Path) -> None:
    url = f"{SITE}/articles/clinical-trials-for-pets-with-cancer/"
    finder = g.FINDER.rstrip('/') + '/'

    body = f'''<article class="article-page">
<h1>Clinical Trials for Pets with Cancer</h1>
<p>A veterinary cancer clinical trial may provide access to a treatment that is not otherwise available. That does not make experimental treatment better than standard care. It means the answer is not known yet.</p>
<p>The first question is therefore not whether a new treatment sounds promising. It is what standard treatment can realistically accomplish for this particular animal. Is the goal a cure, durable control, more time, or relief of symptoms? A proven treatment should not be abandoned casually for an experiment.</p>
<p>Early results can be worth taking seriously without being treated as promises. A response in a small group of animals is not proof that the same proportion of future patients will benefit. A laboratory result may provide a good reason to test a treatment in dogs, but it does not show that the treatment improves survival. The difficult part is making a decision before those answers exist.</p>

<h2>How veterinary cancer clinical trials work</h2>
<p>A clinical trial is a study in which a treatment is tested in real patients under a defined protocol. It may involve a new drug, vaccine, immunotherapy, cell therapy, or a new combination of treatments that already exist.</p>
<p>Experimental does not necessarily mean completely unknown. Sometimes dozens of animals have already received the treatment and there are preliminary results, but there may not yet be enough evidence to consider it standard treatment. That is also why early numbers need to be viewed carefully. If five out of ten animals respond well, that is interesting, but it does not mean that half of all pets with the same diagnosis will have the same result. A promising early result is a reason to pay attention, not a guarantee.</p>

<h2>Finding cancer clinical trials for pets</h2>
<p>Vet Trial Finder brings together current studies and treatment-access programs in which a dog or cat may actually receive an anticancer treatment. The catalog includes universities, private specialty hospitals, multicenter studies and participating sites outside the United States.</p>
<p>We are not trying to collect everything that happens to be called research. Observational studies, sample-collection studies and diagnostic-only research are not presented as treatment options.</p>
<p>The service is free. It does not require registration, an email address or a paid report. Our sources, inclusion rules and status-checking process are explained on the <a href="{SITE}/how-we-verify/">How we verify</a> page.</p>

<h2>Eligibility for a clinical trial</h2>
<p>The diagnosis alone is not enough. A study may consider the stage of the cancer, whether the primary tumor has been removed, whether metastases are present, current and previous treatments, and other medical conditions. Having the “right” cancer does not automatically mean that a pet qualifies.</p>

<h2>Placebo-controlled cancer trials</h2>
<p>Some cancer trials do include a placebo group. Vet Trial Finder does not present a study as a treatment option if a pet could receive only placebo instead of necessary anticancer treatment.</p>
<p>The placebo-controlled studies that remain in our treatment matcher still provide real cancer treatment; the placebo is used to compare an additional experimental component. Before enrolling, it is still important to understand exactly what each group receives and what happens if your pet’s cancer progresses.</p>

<h2>Evaluating an experimental option</h2>
<p>The starting point is what standard treatment can realistically accomplish: the chance of a cure or durable control, the likely amount of additional time, the side effects, the cost and what the animal would have to go through.</p>
<p>The experimental option can then be judged against that baseline. Useful details include how many animals have received it, whether results exist in dogs or cats rather than only in a laboratory, what actually improved, which side effects occurred and whether participation would require delaying or giving up a proven treatment.</p>
<p>An experimental treatment can be worth trying. But the possible benefit has to be weighed against what may be lost if it does not work, including time in which another treatment could have been given.</p>

<h2>When a clinical trial may be worth considering</h2>
<p>Experimental treatment is not automatically better than standard treatment. Usually, the evidence is not yet strong enough to know whether it is better.</p>
<p>A trial may still be worth considering when standard treatment has little to offer, the cancer has returned, or the study has a reasonable scientific basis and fits the animal’s particular situation. Sometimes the best choice is the proven treatment. Sometimes taking the additional uncertainty may be reasonable.</p>
<p>A clinical trial is not a promise. But sometimes this is how a treatment begins before, years later, it is no longer considered experimental.</p>
<div class="article-cta"><a href="{finder}">Search current cancer treatment trials for your pet</a></div>
<div class="article-byline"><p><strong>Reviewed and edited by:</strong> <a href="{SITE}/about/" rel="author">Yuliia Dizhur</a>, Founder of Vet Trial Finder</p><p><strong>Published:</strong> September 14, 2026</p><p><strong>Last updated:</strong> September 26, 2026</p><p>Yuliia Dizhur is the founder of Vet Trial Finder and a dog owner with extensive firsthand experience of canine cancer. She edits practical guides using peer-reviewed research, published clinical guidance and information from veterinary hospitals and research teams.</p><p><strong>Editorial disclosure:</strong> Prepared with AI assistance and reviewed by Yuliia Dizhur. It has not been independently reviewed by a veterinarian and does not replace veterinary advice.</p></div>
</article>'''

    directory = root / 'articles' / 'clinical-trials-for-pets-with-cancer'
    directory.mkdir(parents=True, exist_ok=True)
    page = g.page(
        'Clinical Trials for Pets with Cancer | Vet Trial Finder',
        'A practical owner guide to cancer clinical trials for dogs and cats: experimental treatment, eligibility, placebo and treatment decisions.',
        body,
        url,
    )
    schema = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": 'Clinical trials for pets with cancer', "datePublished": '2026-09-14', "dateModified": '2026-09-26',
        "author": {"@type": "Person", "name": "Yuliia Dizhur", "url": f"{SITE}/about/"},
        "publisher": {"@id": f"{SITE}/#organization"},
        "mainEntityOfPage": url,
    }
    page = page.replace("</head>", '<script type="application/ld+json">' + json.dumps(schema) + '</script></head>', 1)
    rendered = wrap_html(page)
    (directory / 'index.html').write_text(rendered, encoding='utf-8')

    index = root / 'articles' / 'index.html'
    if not index.exists():
        raise AssertionError('Articles index is required before adding the clinical-trials article')
    text = index.read_text(encoding='utf-8')
    if url not in text:
        card = (
            f'<a class="directory-card" href="{url}">'
            '<strong>Clinical Trials for Pets with Cancer</strong>'
            '<span>What experimental treatment really means, how to weigh the risk, and what a trial match can — and cannot — tell you.</span>'
            '</a>'
        )
        if '<div class="directory-grid">' not in text:
            raise AssertionError('Articles index is missing the directory-grid container')
        text = text.replace('<div class="directory-grid">', '<div class="directory-grid">' + card, 1)
        index.write_text(text, encoding='utf-8')

    article = (directory / 'index.html').read_text(encoding='utf-8')
    checks = (
        '<h1 class="page-title">Clinical Trials for Pets with Cancer</h1>',
        'How veterinary cancer clinical trials work',
        'does not present a study as a treatment option if a pet could receive only placebo',
        'We are not trying to collect everything that happens to be called research.',
        'Reviewed and edited by:',
        'Yuliia Dizhur',
        'Editorial disclosure:',
        'Search current cancer treatment trials for your pet',
        finder,
        f'<link rel="canonical" href="{url}">',
    )
    missing = [marker for marker in checks if marker not in article]
    if missing:
        raise AssertionError(f'Clinical-trials article validation failed: {missing}')
    if url not in index.read_text(encoding='utf-8'):
        raise AssertionError('Clinical-trials article card was not added to Articles')


def main() -> None:
    generate_clinical_trials_for_pets_article(Path(__file__).resolve().parent / 'site')


if __name__ == '__main__':
    main()
