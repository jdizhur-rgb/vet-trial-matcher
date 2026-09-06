# Social-first veterinary oncology discovery layer

Added 2026-09-06 after gap analysis showed that active recruitment is often announced as owner-facing posts/newsletters before or instead of a well-indexed clinical-trials page.

## Priority geography
1. USA
2. UK + Europe
3. Canada
4. Rest of world opportunistically

## Discovery phrases
Search both web-indexed social posts and center/news pages for combinations of dog/cat/canine/feline + cancer/oncology plus:
- dogs wanted / cats wanted
- dogs needed / cats needed
- seeking dogs / seeking cats
- patients wanted / call for patients
- does your dog have / does your cat have
- now enrolling / currently enrolling / recruiting
- study opportunity / treatment study
- free treatment / treatment covered / study covers
- clinical research / clinical study / clinical trial

Also run disease-specific versions for lymphoma, osteosarcoma, hemangiosarcoma, histiocytic sarcoma, mast cell tumor, melanoma, soft tissue sarcoma, oral SCC, mammary carcinoma, FISS, urothelial/TCC, glioma/brain tumor, and broad solid tumors.

## Social/source surfaces
- Facebook pages/posts/groups that are publicly indexed
- Instagram public posts
- LinkedIn posts from veterinary schools, oncologists, specialty hospitals, CROs and sponsors
- university newsletters/news releases
- specialty/referral hospital news and clinical-trial pages
- CRO/sponsor recruitment announcements

## Verification rule
A social post is a lead, not sufficient evidence by itself when a primary source can be found. Trace each lead to the study center, PI, hospital, CRO or sponsor. Promote to matching only when current recruitment and an actual anticancer intervention can be supported. Exclude diagnostic-only, biomarker/sample collection, observational and supportive-only studies. Preserve social-only leads in watch/audit notes when current recruitment is plausible but primary confirmation is unavailable.

## Dedup rule
Deduplicate by protocol: center/network + disease + intervention + protocol/source. Do not create separate records merely because the same multisite study is promoted by several hospitals or social accounts.

## Findings from first social-first pass
- Veterinary Referral Center of Central Oregon (VRCCO): current `CALL FOR PATIENTS` for intratumoral T-cell engager immunotherapy followed by surgery for canine soft tissue sarcoma. This appears to be the same protocol family already represented in the catalog through the TCE/B7-H3/PD-L1 STS study, so do not duplicate without protocol-level evidence that it is distinct.
- UW Wisconsin owner newsletter: `Wanted: Dogs for cancer blood test research study` is diagnostic-only and excluded.
- UW Wisconsin owner newsletter: AGASACA PET/CT study is diagnostic imaging before surgery and excluded as a treatment opportunity.
- Ethos `Canine Oncology Sample Study`: now enrolling but diagnostic/sample-platform development only and excluded.
- Tufts Z-007 and HSA precision-treatment studies surface strongly under owner/recruitment wording but are already known/current catalog protocols; no duplicate insertion.
- University of Florida oral melanoma vaccine + gilvetmab remains currently recruiting but is an existing UF protocol; no duplicate insertion.
- Johns Hopkins current owner-facing recruitment page confirms OSA cryo/immunotherapy, brain cancer, and mammary cryotherapy protocols already added in the prior center-gap pass; no duplicate insertion.

Conclusion: first social-first pass found useful recruitment evidence and several tempting false positives, but no protocol-level new treatment record that could safely be added without duplicating the current catalog. Keep this discovery layer in future audits.