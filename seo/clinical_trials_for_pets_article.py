#!/usr/bin/env python3
"""Generate the owner-facing article about cancer clinical trials for pets."""
from __future__ import annotations

from pathlib import Path

import generate_seo as g
from site_config import SITE
from site_shell import wrap_html

g.SITE = SITE
g.FINDER = "https://c-trials.streamlit.app/"


def generate_clinical_trials_for_pets_article(root: Path) -> None:
    url = f"{SITE}/articles/clinical-trials-for-pets-with-cancer/"
    finder = g.FINDER.rstrip('/') + '/'

    body = f'''<article class="article-page">
<h1>Clinical Trials for Pets with Cancer</h1>
<p>Cancer is a frightening word. When we hear that diagnosis, at best we feel lost. At worst, we panic. I know this very well from my own experience: the anxiety, the rush to do something, the endless search for information in the hope of finding a miracle solution that may simply not exist.</p>
<p>That stage passes. When you can finally look at things a little more clearly, it helps to go back to the basic questions. What exactly did the doctor say? What is the real prognosis? What can treatment realistically achieve? Ask for honest answers. The truth, even when it is difficult, is more useful than false hope.</p>
<p>If a cancer has a well-established treatment that has been used for years and produces good results, there should be a very good reason to give up a proven approach for an experimental one. Established treatment protocols exist for a reason: they are usually backed by the strongest evidence currently available.</p>
<p>But sometimes there is a “but.”</p>
<p>My dog Yasha has histiocytic sarcoma. In his particular situation, standard treatment involves expensive procedures and may give him additional time, but it does not offer a realistic chance of a cure. I spent weeks reading everything I could find about histiocytic sarcoma. I even wrote to researchers with my very nonprofessional questions, and every one of them replied. I cannot express how grateful I am for that or how much I respect the people doing this work.</p>
<p>The main thing I learned is simple: experimental treatment can offer hope, but it cannot make promises. Sometimes a new treatment already has very interesting results in a small group of animals. Sometimes the results look wonderful only in a laboratory. If there were a clinical trial that truly fit Yasha, I would take the risk. But that is my decision in our particular situation, not advice for everyone.</p>
<p>The difficult part is that when we make the decision, we never know whether this experiment will be the one that actually helps. Ultimately, the decision is ours to make.</p>

<h2>What is a clinical trial?</h2>
<p>A clinical trial is a study in which a treatment is tested in real patients under a defined protocol. It may involve a new drug, vaccine, immunotherapy, cell therapy, or a new combination of treatments that already exist.</p>
<p>Experimental does not necessarily mean completely unknown. Sometimes dozens of animals have already received the treatment and there are preliminary results, but there may not yet be enough evidence to consider it standard treatment. That is also why early numbers need to be viewed carefully. If five out of ten animals respond well, that is interesting, but it does not mean that half of all pets with the same diagnosis will have the same result. A promising early result is a reason to pay attention, not a guarantee.</p>

<h2>Where can you find cancer clinical trials for pets?</h2>
<p>That is why we created Vet Trial Finder. We bring together current studies in which a pet may actually receive an anticancer treatment.</p>
<p>We are not trying to collect everything that happens to be called research. Observational studies, sample-collection studies, and diagnostic-only research are not presented as treatment options. In the matcher, you can enter your pet’s diagnosis and basic medical information and see studies that may fit based on the eligibility criteria that have been made public.</p>
<p>That does not mean your pet will be accepted into the trial. It simply helps remove clearly unsuitable options and shows you which study teams may actually be worth contacting.</p>
<div class="article-cta"><a href="{finder}">Search current cancer treatment trials for your pet</a></div>

<h2>Why might your pet not qualify?</h2>
<p>The diagnosis alone is not enough. A study may consider the stage of the cancer, whether the primary tumor has been removed, whether metastases are present, current and previous treatments, and other medical conditions. Having the “right” cancer does not automatically mean that a pet qualifies.</p>

<h2>What about placebo?</h2>
<p>Some cancer trials do include a placebo group. Vet Trial Finder does not present a study as a treatment option if a pet could receive only placebo instead of necessary anticancer treatment.</p>
<p>The placebo-controlled studies that remain in our treatment matcher still provide real cancer treatment; the placebo is used to compare an additional experimental component. Before enrolling, it is still important to understand exactly what each group receives and what happens if your pet’s cancer progresses.</p>

<h2>How would I make the decision?</h2>
<p>I would start by asking the oncologist what standard treatment can realistically accomplish. What are the chances? Is the goal a cure, long-term control, or simply a few additional months? What is the cost of treatment, not only financially but in terms of what the pet has to go through?</p>
<p>Only then would I look at the experimental option. What is already known about it? How many animals have received it? Are there actual results? What improved: tumor size, time before progression, or survival? What side effects were seen? Would participating mean giving up a proven treatment? And what could we lose if the experiment does not work?</p>
<p>For me, that last question matters most. An experimental treatment can be worth trying. But sometimes you cannot get the time back.</p>

<h2>What does “Match” mean on Vet Trial Finder?</h2>
<p>A Match means only one thing: <strong>this option is worth checking.</strong></p>
<p>It does not mean your pet has been accepted, that the treatment will work, or that your pet definitely meets every eligibility requirement. Our matcher compares the published study criteria with the information you provide and removes options that clearly do not fit. The final eligibility decision always belongs to the research team after they review the medical records.</p>

<h2>Is it worth looking for clinical trials at all?</h2>
<p>I think so. Not because experimental treatment is better than standard treatment. Usually, we simply do not know yet whether it is better.</p>
<p>But if standard treatment has little to offer, the cancer has returned, or there is an option that offers real hope in your pet’s particular situation, I would want to know that it exists. Sometimes the best choice is the proven treatment. Sometimes it makes sense to take the risk.</p>
<p>A clinical trial is not a promise. But sometimes this is how a treatment begins before, years later, it is no longer considered experimental.</p>
</article>'''

    directory = root / 'articles' / 'clinical-trials-for-pets-with-cancer'
    directory.mkdir(parents=True, exist_ok=True)
    page = g.page(
        'Clinical Trials for Pets with Cancer | Vet Trial Finder',
        'A practical owner guide to cancer clinical trials for dogs and cats: what experimental treatment means, eligibility, placebo, and what a match really means.',
        body,
        url,
    )
    rendered = wrap_html(page)
    (directory / 'index.html').write_text(rendered, encoding='utf-8')

    index = root / 'articles' / 'index.html'
    if not index.exists():
        raise AssertionError('Articles index is required before adding the clinical-trials article')
    text = index.read_text(encoding='utf-8')
    if url not in text:
        card = (
            f'<a class="site-card" href="{url}">'
            '<h3>Clinical Trials for Pets with Cancer</h3>'
            '<p>What experimental treatment really means, how to weigh the risk, and what a trial match can — and cannot — tell you.</p>'
            '</a>'
        )
        if '<div class="site-grid">' not in text:
            raise AssertionError('Articles index is missing the site-grid container')
        text = text.replace('<div class="site-grid">', '<div class="site-grid">' + card, 1)
        index.write_text(text, encoding='utf-8')

    article = (directory / 'index.html').read_text(encoding='utf-8')
    checks = (
        '<h1>Clinical Trials for Pets with Cancer</h1>',
        'My dog Yasha has histiocytic sarcoma.',
        'does not present a study as a treatment option if a pet could receive only placebo',
        'this option is worth checking.',
        finder,
        f'<link rel="canonical" href="{url}">',
    )
    missing = [marker for marker in checks if marker not in article]
    if missing:
        raise AssertionError(f'Clinical-trials article validation failed: {missing}')
    if url not in index.read_text(encoding='utf-8'):
        raise AssertionError('Clinical-trials article card was not added to Articles')
