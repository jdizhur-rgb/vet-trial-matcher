#!/usr/bin/env python3
"""Generate the About page for Vet Trial Finder."""
import base64
import urllib.request
from pathlib import Path
import generate_seo as g
from site_config import SITE


def _write_embedded_about_assets(root: Path) -> None:
    src = Path(__file__).resolve().parent / "assets_embedded"
    dest = root / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    mapping = {
        "senya-about.b64": (
            "senya-about.jpg",
            "https://raw.githubusercontent.com/jdizhur-rgb/vet-trial-matcher/0c20d174267460d846495db27e937eb233a12d09/seo/assets_embedded/senya-about.b64",
        ),
        "yasha-about.b64": (
            "yasha-about.jpg",
            "https://raw.githubusercontent.com/jdizhur-rgb/vet-trial-matcher/0a1b7fb3cbb2626994fe043a74004d14e494435e/seo/assets_embedded/yasha-about.b64",
        ),
    }
    for source_name, (output_name, fallback_url) in mapping.items():
        source = src / source_name
        if source.exists():
            payload = source.read_text(encoding="ascii")
        else:
            with urllib.request.urlopen(fallback_url, timeout=20) as response:
                payload = response.read().decode("ascii")
        data = base64.b64decode(payload)
        if len(data) < 50000:
            raise RuntimeError(f"about image too small: {output_name} ({len(data)} bytes)")
        (dest / output_name).write_bytes(data)


def generate_about_page(root: Path) -> None:
    _write_embedded_about_assets(root)
    body = '''
<style>
.about-story{max-width:920px;margin:0 auto;color:#24364a}
.about-story>h1{color:#315f7d!important;font-weight:650!important;letter-spacing:-.02em;margin-bottom:24px!important}
.about-story p{font-size:17px;line-height:1.68;margin:0 0 20px}
.story-intro,.story-break{display:grid;grid-template-columns:minmax(280px,.78fr) minmax(0,1.22fr);gap:30px;align-items:start;margin:6px 0 26px}
.story-break{margin:30px 0 24px}
.story-media{margin:0;background:#fff;border:1px solid #dce5ec;border-radius:14px;overflow:hidden;box-shadow:0 4px 16px rgba(23,36,59,.05)}
.story-media img{display:block;width:100%;aspect-ratio:3/2;object-fit:cover}
.story-media figcaption{padding:8px 12px 10px;color:#60788e;font-size:14px;line-height:1.2;text-align:left}
.story-intro .story-text p:last-child,.story-break .story-text p:last-child{margin-bottom:0}
.story-close{margin:28px 0 24px!important;padding:18px 20px;border-left:4px solid #8ab6cf;background:#f1f7fa;border-radius:0 10px 10px 0;color:#31536b}
.founder-signoff{display:flex;align-items:center;gap:14px;margin-top:26px;padding-top:20px;border-top:1px solid #dce5ec}
.founder-signoff img{width:72px;height:72px;object-fit:cover;border-radius:50%;border:1px solid #d9e2ea}
.founder-signoff strong,.founder-signoff span{display:block}.founder-signoff strong{color:#315f7d}.founder-signoff span{color:#60788e;font-size:14px;margin-top:2px}
@media(max-width:800px){
.about-story{max-width:none}.about-story>h1{font-size:31px!important;line-height:1.12!important;margin:20px 0 20px!important;color:#315f7d!important}.about-story p{font-size:16px;line-height:1.58;margin-bottom:18px}.story-intro,.story-break{display:block;margin:0 0 22px}.story-media{margin:0 0 18px;border-radius:12px}.story-media img{aspect-ratio:16/10;object-fit:cover}.story-media figcaption{padding:7px 10px 9px;font-size:13px}.story-break{margin-top:28px}.story-close{margin:24px 0 22px!important;padding:15px 16px}.founder-signoff{margin-top:22px}.founder-signoff img{width:60px;height:60px}
}
</style>
<article class="about-story">
<h1>Why This Project Exists</h1>
<div class="story-intro">
<figure class="story-media"><img src="/assets/senya-about.jpg" alt="Senya, a Miniature Schnauzer"><figcaption>Senya</figcaption></figure>
<div class="story-text">
<p>I lost my soulmate dog, Senya, a Miniature Schnauzer, to cancer. It started with a small lump. We went to the vet, who felt it and said it was a lipoma and there was nothing to worry about. So I didn’t worry, for a while.</p>
<p>The lump grew quickly. We went to another vet. They did a fine needle aspiration and said the result was inconclusive, but if we wanted, they could remove it. We scheduled surgery. After the surgery, the surgeon came out and said that “it was something different.” Pathology showed a soft tissue sarcoma.</p>
</div>
</div>
<p>Apparently, the surgeon was not experienced with cancer surgery and did not take the recommended wide margins. The margins were dirty, meaning that some cancer cells had been left behind.</p>
<p>We tried to get an appointment with an oncologist. The earliest available appointment was four months away. Cancer doesn’t wait, so we flew to Europe for surgery. The second surgery was successful, the margins were clean, and the prognosis was excellent. We continued seeing an oncologist and had full staging done every two months.</p>
<p>A year later, during one of those routine checks, they found a 6 cm tumor in his lung. The next day it ruptured. Senya crossed the rainbow bridge. I was completely unprepared for it. It seemed that we had done everything right, so why did this happen? I blame myself. I should not have simply believed that the lump was harmless. I should have had it checked right away. Things might have gone differently.</p>
<div class="story-break">
<figure class="story-media"><img src="/assets/yasha-about.jpg" alt="Yasha"><figcaption>Yasha</figcaption></figure>
<div class="story-text">
<p>A year later, during an exam, a small lump was found under the leg of our other dog, Yasha. I immediately asked for an aspiration. The test showed sarcoma. We were lucky to get in with an oncologist quickly because we were already patients at the hospital. A board-certified surgeon performed the surgery beautifully. Pathology showed histiocytic sarcoma, a very aggressive form of cancer.</p>
<p>Yasha is undergoing treatment now. I don’t know what is ahead of us, but this time I want to be prepared. I searched through the internet looking for information. I learned about the standard treatment protocols and prognosis and read several papers about newer treatments.</p>
</div>
</div>
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
