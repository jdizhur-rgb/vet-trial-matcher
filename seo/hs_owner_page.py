"""Practical owner-facing page section for canine histiocytic sarcoma."""
from __future__ import annotations


def canine_hs_section(label_html: str) -> str:
    return f'''<section class="disease hs-guide">
<h2>About {label_html}</h2>
<p>Histiocytic sarcoma (HS) is an uncommon but aggressive cancer in dogs. It can start as <strong>one tumor in one part of the body</strong> (localized HS), or it can involve <strong>several organs</strong> (disseminated HS). The first important question is whether the cancer is still localized or has spread, because that changes both treatment options and prognosis.</p>

<div class="hs-reality">
<h2>What does the prognosis look like?</h2>
<p>HS is serious, but the outlook varies a lot. In published groups of dogs, median survival has been roughly <strong>2–3 months for disseminated disease</strong> and about <strong>13–19 months in some dogs with localized HS treated aggressively</strong>. Some dogs do much better or worse than these numbers.</p>
<p><strong>No statistic can predict your dog.</strong> The practical point is that time matters. Waiting several months for an oncology appointment may mean losing useful treatment time or options.</p>
</div>

<h2>What should happen next?</h2>
<p>The next step is usually <strong>staging</strong> — checking whether cancer is present anywhere else in the body. This commonly includes chest imaging and abdominal imaging; other tests depend on where the original tumor was found. With HS, it makes sense to move the process along rather than simply wait for the next routine appointment.</p>

<div class="hs-path" aria-label="Typical next steps after a histiocytic sarcoma diagnosis">
<div><strong>HS diagnosis</strong><span>Know what the pathology found</span></div><b aria-hidden="true">→</b><div><strong>Staging</strong><span>Localized or spread?</span></div><b aria-hidden="true">→</b><div><strong>Plan</strong><span>Local + systemic options</span></div>
</div>

<h2>Where are you now?</h2>
<div class="hs-situations">
<div><h3>The tumor is still there</h3><p>If surgery is possible, ask whether it can realistically be removed with clean margins. Surgery is often the best local treatment for a removable localized tumor. If clean margins are unlikely, ask what other local-control options are reasonable.</p><p>It is also worth checking trials before surgery when there is time to do so safely: some studies require a measurable tumor, a biopsy, or direct treatment of the tumor. <strong>This is not a reason to delay surgery your veterinary team considers necessary.</strong></p></div>
<div><h3>The tumor has already been removed</h3><p>Get the pathology report and check the margin status. The next questions are whether staging shows disease elsewhere, whether the surgical site needs more local treatment, and whether systemic treatment is recommended because HS can spread microscopically.</p></div>
<div><h3>The cancer has spread or cannot be removed</h3><p>Surgery may no longer be the main decision. Ask about systemic treatment, local treatment for a tumor that is causing problems, and clinical trials that accept measurable or metastatic disease.</p></div>
<div><h3>Your dog is already in treatment</h3><p>You may still have trial options. Look specifically for studies that allow previous surgery, chemotherapy or radiation, and ask what options remain if the current treatment stops working.</p></div>
</div>

<div class="hs-waiting">
<h2>If you are waiting for oncology</h2>
<p>Waiting does not mean there is nothing to do. Ask about a cancellation list or another oncology center if the appointment is far away. Complete recommended staging if your veterinary team can arrange it, and <strong>check clinical trials before the next treatment decision</strong>.</p>
<p>Some trials require a tumor to still be measurable or exclude certain previous chemotherapy or radiation. Checking early does not commit you to a trial — it simply shows you what options exist before one of them is accidentally closed.</p>
</div>

<h2>At the first oncology appointment, ask</h2>
<ul class="hs-questions">
<li>Is this localized HS or is there evidence that it has spread?</li>
<li>Is the staging we have enough, or is anything important still missing?</li>
<li>If surgery was done, are the margins adequate and does the site need more local treatment?</li>
<li>Do you recommend systemic treatment now, and what are the realistic options?</li>
<li>Could treatment we start now affect eligibility for a clinical trial later?</li>
</ul>

<h2>Tests worth asking about</h2>
<p>There is no single cancer test that tells every dog with HS which treatment will work. If additional tumor testing or genomic profiling is available, ask one practical question before paying for it: <strong>will the result change treatment or trial eligibility now?</strong> If testing may be useful later, ask whether the pathology lab can retain the tumor block or slides from surgery.</p>

<h2>How it is usually treated</h2>
<p>For localized disease, surgery or radiation may be used for local control. Because HS has a meaningful risk of microscopic or distant spread, systemic chemotherapy is often discussed even after local treatment; lomustine (CCNU) is one commonly used drug in dogs. For disseminated disease, systemic treatment becomes the main focus. Clinical trials may offer additional approaches.</p>

<h2>What can affect treatment choices</h2>
<p>The biggest factors are whether HS is localized or disseminated, where it started, whether a tumor can be completely removed, surgical margins, measurable disease, metastasis, previous treatment and your dog’s overall health.</p>
</section>'''


HS_CSS = r'''
.hs-guide h2{margin-top:26px}.hs-reality,.hs-waiting{margin:20px 0;padding:16px 18px;border:1px solid #d9e2ea;border-radius:14px;background:#f8fafc}.hs-reality h2,.hs-waiting h2{margin-top:0}.hs-path{display:grid;grid-template-columns:1fr auto 1fr auto 1fr;gap:10px;align-items:center;margin:18px 0 24px}.hs-path>div{min-height:92px;padding:13px;border:1px solid #d9e2ea;border-radius:12px;background:#fff;text-align:center;display:flex;flex-direction:column;justify-content:center}.hs-path strong{display:block}.hs-path span{display:block;margin-top:4px;color:#607086;font-size:.88rem;line-height:1.3}.hs-path>b{color:#718096;font-size:1.25rem}.hs-situations{display:grid;grid-template-columns:1fr 1fr;gap:12px}.hs-situations>div{padding:15px 16px;border:1px solid #d9e2ea;border-radius:12px;background:#fff}.hs-situations h3{margin:0 0 7px;font-size:1.02rem}.hs-situations p{margin:.45rem 0}.hs-questions{padding-left:21px}.hs-questions li{margin:.45rem 0}@media(max-width:600px){.hs-guide h2{font-size:1.16rem;margin-top:22px}.hs-guide p{line-height:1.52}.hs-reality,.hs-waiting{padding:14px 15px;margin:16px 0}.hs-path{grid-template-columns:1fr;gap:6px;margin:14px 0 20px}.hs-path>div{min-height:0;text-align:left;padding:11px 13px}.hs-path>b{transform:rotate(90deg);justify-self:center;font-size:1rem;line-height:1}.hs-situations{grid-template-columns:1fr;gap:9px}.hs-situations>div{padding:13px 14px}.hs-situations h3{font-size:1rem}.hs-questions{padding-left:19px}}
'''.strip()
