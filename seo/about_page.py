#!/usr/bin/env python3
"""Generate the About page for Vet Trial Finder."""
from pathlib import Path
import generate_seo as g
from site_config import SITE


def generate_about_page(root: Path) -> None:
    body = '''
<article class="about-story">
<h1>Why This Project Exists</h1>
<div class="story-photo story-photo-right"><img src="/assets/senya-about.jpg" alt="Senya, a Miniature Schnauzer"><span>Senya</span></div>
<p>I lost my soulmate dog, Senya, a Miniature Schnauzer, to cancer. It started with a small lump. We went to the vet, who felt it and said it was a lipoma and there was nothing to worry about. So I didn’t worry, for a while.</p>
<p>The lump grew quickly. We went to another vet. They did a fine needle aspiration and said the result was inconclusive, but if we wanted, they could remove it. We scheduled surgery. After the surgery, the surgeon came out and said that “it was something different.” Pathology showed a soft tissue sarcoma.</p>
<p>Apparently, the surgeon was not experienced with cancer surgery and did not take the recommended wide margins. The margins were dirty, meaning that some cancer cells had been left behind.</p>
<p>We tried to get an appointment with an oncologist. The earliest available appointment was four months away. Cancer doesn’t wait, so we flew to Europe for surgery. The second surgery was successful, the margins were clean, and the prognosis was excellent. We continued seeing an oncologist and had full staging done every two months.</p>
<p>A year later, during one of those routine checks, they found a 6 cm tumor in his lung. The next day it ruptured. Senya crossed the rainbow bridge. I was completely unprepared for it. It seemed that we had done everything right, so why did this happen? I blame myself. I should not have simply believed that the lump was harmless. I should have had it checked right away. Things might have gone differently.</p>
<div class="story-photo story-photo-left"><img src="/assets/yasha-about.jpg" alt="Yasha"><span>Yasha</span></div>
<p>A year later, during an exam, a small lump was found under the leg of our other dog, Yasha. I immediately asked for an aspiration. The test showed sarcoma. We were lucky to get in with an oncologist quickly because we were already patients at the hospital. A board-certified surgeon performed the surgery beautifully. Pathology showed histiocytic sarcoma, a very aggressive form of cancer.</p>
<p>Yasha is undergoing treatment now. I don’t know what is ahead of us, but this time I want to be prepared. I searched through the internet looking for information. I learned about the standard treatment protocols and prognosis and read several papers about newer treatments.</p>
<p>Unfortunately, right now there is nothing that fits Yasha. But if something becomes available, I want to know about it the same day. That is why I created this finder.</p>
<p>Clinical trial information is updated daily. You can also find universities and specialty hospitals near you where board-certified veterinary oncologists practice. As I said, cancer doesn’t wait, and knowledge is power. I want to help confused and overwhelmed pet owners who have just heard the diagnosis and don’t know what to do get the information they need.</p>
<p>On this site, the main types of cancer and their standard treatments are explained in plain language. You can search for current clinical trials, see their basic eligibility requirements, locations and contacts, and find universities, specialty hospitals and oncology centers that may be able to help. We also collect information about treatments that are not available everywhere, such as electrochemotherapy, newer targeted and immunotherapy approaches, and expanded access programs.</p>
<p>Some of these options are experimental, some are already being used in veterinary oncology but can be difficult to find. None of them is right for every animal, but some may offer another option when standard treatment is not enough.</p>
<p class="story-close"><strong>We don’t promise anything and we don’t give false hope. But we provide information and help you find it when time matters.</strong></p>
<div class="founder-signoff"><img src="/assets/yuliia-senya-about.jpg" alt="Yuliia Dizhur with Senya"><div><strong>Yuliia Dizhur</strong><span>Founder, Vet Trial Finder</span></div></div>
</article>
'''
    d = root / 'about'
    d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(g.page(
        'Why This Project Exists | Vet Trial Finder',
        'The personal story behind Vet Trial Finder and why finding veterinary cancer information quickly matters.',
        body,
        f'{SITE}/about/'
    ), encoding='utf-8')
