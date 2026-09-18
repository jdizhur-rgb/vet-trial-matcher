#!/usr/bin/env python3
"""Generate the owner-facing article about diagnosing a new lump before surgery."""
from __future__ import annotations

import shutil
from pathlib import Path

import generate_seo as g
from site_config import SITE
from site_shell import wrap_html

g.SITE = SITE


def generate_lump_before_surgery_article(root: Path) -> None:
    url = f"{SITE}/articles/pet-lump-diagnosis-before-surgery/"
    image = f"{SITE}/assets/nyura-lump-diagnosis.jpg"
    senya_image = f"{SITE}/assets/senya-second-surgery.jpg"

    source_assets = Path(__file__).resolve().parent / "assets"
    built_assets = root / "assets"
    built_assets.mkdir(parents=True, exist_ok=True)
    for name in ("nyura-lump-diagnosis.jpg", "senya-second-surgery.jpg"):
        source = source_assets / name
        if not source.exists():
            raise RuntimeError(f"missing article image: {source}")
        shutil.copy2(source, built_assets / name)

    body = f'''<article class="article-page">
<h1>Diagnosis first, surgery second: what to do when you find a lump</h1>
<figure class="article-hero"><img src="{image}" alt="Nyura, a senior dog whose new lump was diagnosed as a lipoma" loading="eager"><figcaption>Nyura. Her lump was checked with a fine-needle aspirate and identified as a lipoma.</figcaption></figure>
<p>Not every lump on a dog or cat is cancer. But it is usually impossible to know what a lump is just by looking at it or feeling it. There is no need to panic, but there is a reason to check.</p>
<p>I have several senior dogs, so I examine them regularly. Recently I found a lump on Nyura. We had a fine-needle aspirate performed. It was a lipoma. Now I know what it is, and I am not worried about it. That is what early diagnosis should do: it does not always uncover something frightening. Sometimes it simply ends the guessing.</p>
<p>A fine-needle aspirate, or FNA, is usually the simplest first test and is available at most veterinary hospitals. A thin needle is inserted into the lump, cells are collected, and the sample is sent for cytology. Anesthesia is often unnecessary, and the procedure itself usually takes only a few minutes. An aspirate may confirm a lipoma, identify a mast cell tumor or certain other tumors, or show that a biopsy is needed for a diagnosis.</p>
<p>Sometimes the sample contains too few cells or the result is inconclusive. That does not mean the lump is safe. It means only that the aspirate did not provide an answer. The next step may be another aspirate, a biopsy, or removal, but now with a plan.</p>
<p>The easiest mistake to make sounds completely reasonable: “Let’s just remove it and send it to pathology.” The problem is that different tumors require different surgical margins. Some can be removed with a small amount of surrounding tissue. Others require the first surgery to be considerably wider and deeper. If the surgeon learns the diagnosis only after removal, pathology may show tumor cells at the margins and a second operation may be needed.</p>
<p>That happened with one of my dogs, Senya. His lump was removed, and pathology showed a sarcoma with inadequate margins. He then needed another, wider surgery. At the time, I did not know that we should first gather as much information as possible and discuss the plan with an oncologist. With Yasha, I handled it differently.</p>
<figure class="article-figure"><img src="{senya_image}" alt="Senya recovering at home after a second, wider surgery for a soft tissue sarcoma" loading="lazy"><figcaption>Senya after his second, wider surgery. Pathology after the first operation showed a sarcoma with inadequate margins.</figcaption></figure>
<p>If an aspirate shows cancer, raises suspicion of cancer, or simply does not provide a clear answer, I would schedule a veterinary oncologist before definitive surgery. Owners can contact an oncology center directly; many hospitals do not require a referral from a primary veterinarian. Depending on the tumor and its location, the oncologist may recommend a biopsy, CT, chest imaging, ultrasound, lymph-node sampling, or consultation with a surgical oncologist before the operation.</p>
<p>If the first available appointment is several weeks away, take it and ask to be placed on the cancellation list. Explain that you can come the same day or the next day if another client cancels. This worked twice for Yasha, and we received much earlier appointments. It can also help to call periodically and ask whether an opening has appeared.</p>
<p>There is another reason to consult an oncologist first. Some clinical trials require a measurable tumor, and some protocols deliver treatment directly into the tumor before it is removed. That opportunity may disappear after surgery. This does not mean delaying standard treatment for the sake of a trial. It means deciding on the right sequence before the tumor is gone.</p>
<p>The first surgery often offers the best chance to remove a tumor correctly. A second operation is not always possible: the original tumor boundaries have been disturbed, scar tissue changes the area, and wider re-excision may require removing more tissue. Speed matters, but surgery tomorrow without a diagnosis or plan is not always better than a properly planned operation a little later.</p>
<p>A lump is not a reason to assume the worst. Owners cannot diagnose a mass with their fingers, and veterinarians cannot always do so by touch either. Knowledge gives you something useful to act on: measure the lump, obtain an aspirate, get the result, and then decide. Sometimes that result leads to a difficult conversation with an oncologist. Sometimes, as it did with Nyura, it is a lipoma and life goes on without that uncertainty.</p>
<div class="article-byline"><p><strong>Reviewed and edited by:</strong> <a href="{SITE}/about/" rel="author">Yuliia Dizhur</a>, Founder of Vet Trial Finder</p><p><strong>Published:</strong> September 18, 2026</p><p><strong>Last updated:</strong> September 18, 2026</p><p>Yuliia Dizhur is the founder of Vet Trial Finder and a dog owner with extensive firsthand experience of canine cancer. She edits practical guides using peer-reviewed research, published clinical guidance and information from veterinary hospitals and research teams.</p><p><strong>Editorial disclosure:</strong> Prepared with AI assistance from the sources listed below and reviewed by Yuliia Dizhur. It has not been independently reviewed by a veterinarian and does not replace veterinary advice.</p></div>
<h2>Sources</h2>
<ul>
<li><a href="https://www.aaha.org/resources/2026-aaha-oncology-guidelines-for-dogs-and-cats/" rel="noopener">2026 AAHA Oncology Guidelines for Dogs and Cats</a></li>
<li><a href="https://www.vet.cornell.edu/departments-centers-and-institutes/riney-canine-health-center/canine-health-information/soft-tissue-sarcomas-dogs" rel="noopener">Soft tissue sarcomas in dogs, Cornell University College of Veterinary Medicine</a></li>
<li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC8283129/" rel="noopener">Surgical margins in canine cutaneous soft-tissue sarcomas: a systematic review</a></li>
</ul>
</article>'''

    directory = root / 'articles' / 'pet-lump-diagnosis-before-surgery'
    directory.mkdir(parents=True, exist_ok=True)
    page = g.page(
        'Diagnosis first, surgery second: what to do when you find a lump | Vet Trial Finder',
        'What dog and cat owners should do after finding a new lump: fine-needle aspiration, oncology consultation, surgical planning, and cancellation lists.',
        body,
        url,
    )
    (directory / 'index.html').write_text(wrap_html(page), encoding='utf-8')

    index = root / 'articles' / 'index.html'
    if not index.exists():
        raise AssertionError('Articles index is required before adding the lump article')
    text = index.read_text(encoding='utf-8')
    if url not in text:
        card = (
            f'<a class="directory-card" href="{url}">'
            '<strong>Diagnosis first, surgery second</strong>'
            '<span>What to do when you find a lump, and why the first operation should begin with a diagnosis and a plan.</span>'
            '</a>'
        )
        if '<div class="directory-grid">' not in text:
            raise AssertionError('Articles index is missing the directory-grid container')
        text = text.replace('<div class="directory-grid">', '<div class="directory-grid">' + card, 1)
        index.write_text(text, encoding='utf-8')

    article = (directory / 'index.html').read_text(encoding='utf-8')
    checks = (
        '<h1>Diagnosis first, surgery second: what to do when you find a lump</h1>',
        'I have several senior dogs',
        'fine-needle aspirate',
        'cancellation list',
        'Reviewed and edited by:',
        'Yuliia Dizhur',
        image,
        senya_image,
        f'<link rel="canonical" href="{url}">',
    )
    missing = [marker for marker in checks if marker not in article]
    if missing:
        raise AssertionError(f'Lump article validation failed: {missing}')


def main() -> None:
    generate_lump_before_surgery_article(Path(__file__).resolve().parent / 'site')


if __name__ == '__main__':
    main()
