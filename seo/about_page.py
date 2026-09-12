#!/usr/bin/env python3
"""Generate and validate the About page for Vet Trial Finder."""
import shutil
from pathlib import Path
import generate_seo as g
from site_config import SITE


def _write_embedded_about_assets(root: Path) -> None:
    """Copy the canonical About photos into the built site.

    The function name is kept for workflow compatibility. The page now uses
    only the canonical repository assets and never downloads fallback images.
    """
    src = Path(__file__).resolve().parent / "assets"
    dest = root / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    for name in ("senya-about.jpg", "yasha-about.jpg"):
        source = src / name
        if not source.exists():
            raise RuntimeError(f"missing canonical About image: {source}")
        shutil.copy2(source, dest / name)


def _validate_about_v2(root: Path) -> None:
    page_path = root / "about" / "index.html"
    html = page_path.read_text(encoding="utf-8")
    required = (
        'class="about-story-v2"',
        'class="story-intro"',
        'class="story-scene senya-scene"',
        'class="story-break"',
        'class="story-scene yasha"',
        'class="founder-signoff"',
        'Founder, Vet Trial Finder',
        'color:#315f7d!important',
        'second surgery to remove the dirty margins',
        'experimental treatments, looking for something that might give him better chances',
        'We don’t promise anything and we don’t give false hope.',
        '/assets/senya-about.jpg',
        '/assets/yasha-about.jpg',
        '/assets/yuliia-senya-about.jpg',
    )
    missing = [marker for marker in required if marker not in html]
    if missing:
        raise AssertionError(f"About v2 validation failed; missing: {missing}")
    for name in ("senya-about.jpg", "yasha-about.jpg"):
        asset = root / "assets" / name
        if not asset.exists() or asset.stat().st_size < 50000:
            raise AssertionError(f"About image missing or too small: {asset}")


def generate_about_page(root: Path) -> None:
    _write_embedded_about_assets(root)
    body = '''
<style>
.about-story-v2{max-width:930px;margin:0 auto;color:#293b4d}
.about-story-v2>h1{color:#315f7d!important;font-weight:650!important;letter-spacing:-.02em;margin:16px 0 28px!important}
.about-story-v2 p{font-size:17px;line-height:1.67;margin:0 0 20px}
.about-lead{max-width:760px;color:#536b7f;font-size:18px!important;line-height:1.58!important;margin-bottom:30px!important}
.story-scene{display:grid;grid-template-columns:minmax(300px,.92fr) minmax(0,1.08fr);gap:34px;align-items:start;margin:0 0 28px}
.story-scene.yasha{grid-template-columns:minmax(0,1.08fr) minmax(300px,.92fr);margin-top:34px}
.story-scene.yasha .story-photo{order:2}.story-scene.yasha .story-copy{order:1}
.story-photo{margin:0;background:#f7fafc;border:1px solid #dce5ec;border-radius:16px;overflow:hidden;box-shadow:0 5px 18px rgba(23,36,59,.055)}
.story-photo img{display:block;width:100%;aspect-ratio:16/10;object-fit:cover}
.story-photo.senya img{object-position:50% 43%}
.story-photo.yasha img{object-position:center center}
.story-photo figcaption{padding:8px 12px 10px;color:#6b8193;font-size:13px;line-height:1.2}
.story-copy p:last-child{margin-bottom:0}
.story-divider{height:1px;background:#dfe7ed;margin:32px 0}
.story-purpose{margin-top:30px;padding:24px 26px;background:#f4f8fa;border:1px solid #dce8ee;border-radius:14px}
.story-purpose p:last-child{margin-bottom:0}
.story-close{margin:28px 0 24px!important;padding:18px 20px;border-left:4px solid #8ab6cf;background:#edf6fa;border-radius:0 10px 10px 0;color:#31536b}
.founder-signoff{display:flex;align-items:center;gap:14px;margin-top:28px;padding-top:20px;border-top:1px solid #dce5ec}
.founder-signoff img{width:72px;height:72px;object-fit:cover;border-radius:50%;border:1px solid #d9e2ea}
.founder-signoff strong,.founder-signoff span{display:block}.founder-signoff strong{color:#315f7d}.founder-signoff span{color:#60788e;font-size:14px;margin-top:2px}
@media(max-width:800px){
.about-story-v2{max-width:none}.about-story-v2>h1{font-size:31px!important;line-height:1.12!important;margin:18px 0 18px!important;color:#315f7d!important}.about-story-v2 p{font-size:16px;line-height:1.58;margin-bottom:18px}.about-lead{font-size:16.5px!important;line-height:1.5!important;margin-bottom:22px!important}.story-scene,.story-scene.yasha{display:flex;flex-direction:column;gap:0;margin:0 0 22px}.story-scene.yasha{margin-top:28px}.story-scene.yasha .story-photo,.story-scene.yasha .story-copy{order:initial}.story-photo{width:100%;margin:0 0 18px;border-radius:12px}.story-photo img{aspect-ratio:16/10}.story-photo.senya img{object-position:50% 42%}.story-photo.yasha img{object-position:center center}.story-divider{margin:24px 0}.story-purpose{margin-top:24px;padding:18px 17px}.story-close{margin:24px 0 22px!important;padding:15px 16px}.founder-signoff{margin-top:22px}.founder-signoff img{width:60px;height:60px}
}
</style>
<article class="about-story-v2">
<h1>Why This Project Exists</h1>
<p class="about-lead">This project started because two dogs taught me how much can depend on finding the right information at the right time.</p>
<section class="story-intro"><div class="story-scene senya-scene"><figure class="story-photo senya"><img src="/assets/senya-about.jpg" alt="Senya, a Miniature Schnauzer"><figcaption>Senya</figcaption></figure><div class="story-copy"><p>I lost my soulmate dog, Senya, a Miniature Schnauzer, to cancer. It started with a small lump. We went to the vet, who felt it and said it was a lipoma and there was nothing to worry about. So I didn’t worry, for a while.</p><p>The lump grew quickly. We went to another vet. They did a fine needle aspiration and said the result was inconclusive, but if we wanted, they could remove it. We scheduled surgery. After the surgery, the surgeon came out and said that “it was something else.” Pathology showed a soft tissue sarcoma.</p></div></div></section>
<p>Apparently, the surgeon was not experienced with cancer surgery and did not take the recommended wide margins. The margins were dirty, meaning that some cancer cells had been left behind.</p>
<p>We tried to get an appointment with an oncologist. The earliest available appointment was four months away. Cancer doesn’t wait, so we flew to Europe for a second surgery to remove the dirty margins. The surgery was successful, the margins were clean, and the prognosis was excellent. We continued seeing an oncologist and had full staging done every two months.</p>
<p>A year later, during one of those routine checks, they found a 6 cm tumor in his lung. The next day it ruptured. Senya crossed the rainbow bridge. I was completely unprepared for it. It seemed that we had done everything right, so why did this happen? I blame myself. I should not have simply believed that the lump was harmless. I should have had it checked right away. Things might have gone differently.</p>
<div class="story-divider"></div>
<section class="story-break"><div class="story-scene yasha"><figure class="story-photo yasha"><img src="/assets/yasha-about.jpg" alt="Yasha"><figcaption>Yasha</figcaption></figure><div class="story-copy"><p>A year later, during an exam, a small lump was found under the leg of our other dog, Yasha. I immediately asked for an aspiration. The test showed sarcoma. We were lucky to get in with an oncologist quickly because we were already patients at the hospital. A board-certified surgeon performed the surgery beautifully. Pathology showed histiocytic sarcoma, a very aggressive form of cancer.</p><p>Yasha is undergoing treatment now. I don’t know what is ahead of us, but this time I want to be prepared. I searched through the internet looking for information. I learned about the standard treatment protocols and prognosis and read several papers about experimental treatments, looking for something that might give him better chances.</p></div></div></section>
<p>Unfortunately, right now there is nothing that fits Yasha. But if something becomes available, I want to know about it the same day. That is why I created this finder.</p>
<section class="story-purpose"><p>Clinical trial information is updated daily. You can also find universities and specialty hospitals near you where board-certified veterinary oncologists practice. As I said, cancer doesn’t wait, and knowledge is power. I want to help confused and overwhelmed pet owners who have just heard the diagnosis and don’t know what to do get the information they need.</p><p>On this site, the main types of cancer and their standard treatments are explained in plain language. You can search for current clinical trials, see their basic eligibility requirements, locations and contacts, and find universities, specialty hospitals and oncology centers that may be able to help. We also collect information about treatments that are not available everywhere, such as electrochemotherapy, newer targeted and immunotherapy approaches, and expanded access programs.</p><p>Some of these options are experimental, some are already being used in veterinary oncology but can be difficult to find. None of them is right for every animal, but some may offer another option when standard treatment is not enough.</p></section>
<p class="story-close"><strong>We don’t promise anything and we don’t give false hope. But we provide information and help you find it when time matters.</strong></p>
<div class="founder-signoff"><img src="/assets/yuliia-senya-about.jpg" alt="Yuliia Dizhur with Senya"><div><strong>Yuliia Dizhur</strong><span>Founder, Vet Trial Finder</span></div></div>
</article>
'''
    d = root / 'about'
    d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(g.page('Why This Project Exists | Vet Trial Finder','The personal story behind Vet Trial Finder and why finding veterinary cancer information quickly matters.',body,f'{SITE}/about/'), encoding='utf-8')
    _validate_about_v2(root)
