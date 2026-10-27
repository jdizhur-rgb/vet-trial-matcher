# Wyoming care discovery — 2026-10-26

Completed the documented systematic discovery pass, with source-specific exceptions retained. This is not an independently verified census of every Wyoming general practice. Primary pages were actually read during the October 26 pass; catalog generation does not refresh source dates.

## Published result

The catalog moves from 3 Wyoming locations to 23 physical locations plus one visiting surgical service: 20 physical additions, one mobile addition and evidence updates to the three existing locations. All 21 additions have distinct identities and current primary treatment/contact/clinician evidence. No unrelated record changes were accepted.

Five physical locations explicitly offer chemotherapy. The two additions are Lifetime Animal Hospital (Cody) and Jackson Animal Hospital (Jackson); the three existing locations are Altitude Veterinary Hospital, Casper Animal Medical Center and VCA Spring Creek Animal Care Hospital. This does not establish five specialist oncologists or current appointment availability.

Of the 20 new physical locations, Lifetime offers chemotherapy and surgery, Jackson chemotherapy, 17 additional locations explicit tumor/mass/lump surgery, and Salt Creek a limited local cancer-treatment offering with the specific modality unconfirmed. Ace Mobile Veterinary Surgery is one visiting service covering Wyoming, without a fabricated Wyoming office or distance pin. Jayce Lineberger's ACVS credential is surgical, not medical oncology certification. No new board-certified medical oncologist, radiation service or electrochemotherapy service was established by this pass.

The existing three chemotherapy records retain their modalities and receive current supporting evidence. Generic references to radiation are not treated as proof of equipment or a locally delivered service. New physical addresses are retained, but unverified coordinates stay null.

## Coverage and limits

The 50 secondary locality routes and 132 profile/category screening rows are retained in the coverage ledgers. They include duplicate, historical and nonclinical entries and cannot be counted as verified clinics. Explicit treatment findings were then corroborated on owned primary pages. Current roster and contact checks are documented per accepted record.

Named unresolved sources: Gem City (Laramie), Cheyenne Pet Clinic, Alpine (Laramie), Best Friends (Casper), Bear River (Evanston), Moxey Schreiber (Sheridan), and Western Veterinary Service (Big Piney/Kemmerer). Access failures, generic copy, current clinician uncertainty or branch allocation prevent stronger claims. Tharp's historical domain now contains unrelated content; this does not establish clinic closure. Torrington and Wilson secondary directory routes remained unavailable. Full exceptions and exact URLs are in remaining.json. No absence of local treatment is inferred from these gaps.

Regional options in Colorado, Montana, Utah and Idaho are documented separately in regional-options.json, without creating Wyoming branches. No new state landing page, navigation, UI or outreach was part of this work.

## Verification

The production static build and catalog/source/sanitation/evidence validations passed. The historical European exact-hash regression remains intact through an exact inverse projection of only this accepted Wyoming delta. A/B/C, mobile, network, country-filter and other applicable regressions passed.

One ancillary E-package test fails at its pre-existing street requirement for network contacts without a physical office. Baseline 6254ff7 contains the same offending records. This is documented in validation.json; no test assertion was weakened to hide the failure.

See evidence.json, published-records.json and existing-updates.json for accepted facts; baseline-projection.json for exact changes; request-receipts.json for actual request timestamps/statuses; validation.json for checks; and publication-proof.json for the deployment/readback result once published.

## Publication status

The checked candidate commit is 8cab273b8e47e37caf3e985c85dbd0dcd962cde8, rebased on the latest main e35835d. The full post-rebase static build passed. Automatic approval review rejected the push to main because publication authorization was not explicit enough. No alternate publication was attempted and no live deployment is claimed. The complete local change is ready for explicit publication approval.
