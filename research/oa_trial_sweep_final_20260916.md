# OA / chronic joint pain trial sweep — final pass 2026-09-16

Research-only. Not connected to live matcher or cancer data. This pass expands discovery beyond explicit `osteoarthritis` pages to chronic pain, joint pain, mobility, lameness, sports medicine/rehab, private general practices, specialty hospitals, sponsor/CRO programs, and broad web search. Counting is protocol-level, not site-level.

## Current unique treatment protocols — high confidence

1. NC State — GOS prebiotic / gut-health study for canine OA pain. Current university page explicitly enrolling.
2. University of Minnesota — FEHI / soluble epoxide hydrolase inhibition for feline OA. Current status Open and enrolling.
3. Cornell — platelet-rich plasma for dogs with arthritis/lameness in one knee. Listed on Cornell current recruiting trials page.
4. University of Tennessee — collar intervention for canine lameness/OA. Listed under Active Clinical Trials.
5. University of Tennessee — intra-articular polymer beads ± hyaluronic acid for canine hip OA secondary to dysplasia. Listed under Active Clinical Trials.
6. Wisconsin Veterinary Referral Center / NVA — therapeutic vaccine targeting canine OA pain receptors. Current page says OPEN; radiographic OA and stable pain/lameness ≥3 months; prior Librela excludes.
7. Gallant — investigational stem-cell therapy for feline OA. Sponsor says Enrolling Now; multisite protocol.
8. Clinaxel CX25/011 — North American feline OA field study. CRO project list says Actively recruiting. Exact intervention/sites still need sponsor-level expansion before matcher import.
9. Large canine joint-supplement study — Schwarzman Animal Medical Center + Wizard of Paws are confirmed sites for the same apparent protocol. Dogs ≥3 years, 10–100 lb, ≥3 months mobility disorder/arthritis symptoms, radiographic non-severe OA, 90-day supplement/placebo study. AMC criteria add no Librela within 2 months, no glucocorticoids within 30 days, no intra-articular injection within 90 days, no joint surgery within 180 days. Count ONCE as multicenter protocol.
10. CARE feline OA medication study — private-practice multicenter recruitment signal. Coastal Sunrise and Family Friends both advertise a current feline OA medication study with long follow-up; Coastal explicitly calls it CARE Cat OA Study and offers up to 9 months of study-related care. Count ONCE pending sponsor/protocol ID.
11. Private-practice canine OA once-daily oral medication study — Coastal Sunrise explicitly enrolling dogs with moderate-to-severe OA in an approximately 1-month trial, once-daily tablet, 4 clinic visits + 2 phone calls. Family Friends separately advertises a current canine OA treatment study; until protocol identity is exposed, do not create a second record from that site. Count ONE protocol for now.

## Current treatment candidate — keep RECONFIRM flag

12. Cornell — radiofrequency/pulsed radiofrequency for chronic stifle/knee OA pain difficult to control with other treatments. Current Cornell trial page exists, but explicit current enrollment wording is weaker than the PRP study. Do not expose as confirmed matcher result until direct status reconfirmation.

## Probable duplicates / protocol identity unresolved — do not increase count

- Falls Village Veterinary Hospital (Raleigh) currently enrolls cats in a 7-month, 8-visit study of a new injectable arthritis treatment. This may overlap an already counted feline sponsor/CRO protocol (Ethos/NVA investigational product, Clinaxel CX25/011, or another multisite field study). Keep as a SITE/IDENTITY LEAD until sponsor or protocol ID is known.
- Ethos feline OA investigational veterinary product: current Ethos page says Now Enrolling, cat ≥6 months, ≥4.4 lb, diagnosed OA, 6–8 months and 8 visits. Because intervention/sponsor identity is not public enough to rule out overlap with Clinaxel/private-practice feline field studies, do not blindly add another unique protocol.
- Family Friends canine OA study: current, but public description lacks enough protocol details to determine whether it is the same once-daily oral study seen at Coastal Sunrise. Treat as possible second site, not a new trial.
- Gallant feline OA: multiple participating clinics are sites of one sponsor protocol.

## Active research / observational / biosample — separate from treatment matcher default

1. NC State / Duke — emotional and cognitive domains in dogs with/without chronic OA pain; active 2026 observational/assessment study.
2. Ohio State — OA pain, behavior and rehabilitation questionnaire study in dogs receiving rehab.
3. Basepaws — feline OA research cohort; enrolling cats with medical records confirming OA. Research/biomarker type, not established treatment trial.
4. Falls Village / BioIVT — biological-sample recruitment includes dogs with arthritis; not a treatment trial.

## Closed / completed / historical — explicitly excluded

- XT-550 multicenter canine OA gene-therapy study (NC State / Missouri / Minnesota): recruitment page remains online but explicitly says current program enrollment completed.
- Gallant canine OA stem-cell study: Enrollment Complete.
- University of Florida mitragynine canine OA trial: closed.
- Minnesota feline amantadine OA study: completed.
- Published 2026 Levagen+ canine/feline joint-pain trial: study occurred in 2024; completed.
- Published 2026 piclidenoson/VBX-2000 canine OA pilot: completed; later regulatory development is a discovery lead, not proof of current owner enrollment.
- Published 2026 bedinvetmab vs grapiprant and other completed OA trials: publications only, not recruiting.
- Animal Cell Therapies / Saint Francis 320-dog stem-cell pivotal trial: web page still says recruiting but appears stale/undated; not accepted as 2026-active without sponsor reconfirmation.

## Current program leads / watchlist — not counted as active unique protocols

- Colorado State orthopedic archive: allogeneic stromal cells and several OA pages; live archive alone is insufficient to prove current enrollment.
- University of Florida Integrative and Mobility Medicine: parent page says currently enrolling OA studies but does not expose protocol identities in indexed text; needs direct protocol expansion.
- Cornell FDA-authorized stem-cell musculoskeletal program including OA: current status requires reconfirmation.
- CANDO network: useful discovery network; individual protocols must be resolved against university/private/sponsor records.
- Clinaxel CX25/014 Europe canine OA: Coming up.
- Clinaxel CX26/027 North America canine OA: Coming up.
- University of Sydney canine OA pain-management study surfaced as Coming soon on PetTrials Australia; primary-source enrollment confirmation still needed.

## Matcher fields supported by the collected protocols

Core owner inputs: species; age; weight; ZIP/location; confirmed OA vs suspected mobility/joint pain; radiographic confirmation; affected joint(s); OA severity when known; duration/stability of pain or lameness; owner-observed mobility impairment; current NSAID/gabapentin/other analgesic use; Librela/Solensia exposure; steroids; joint supplements/prescription joint diet; prior intra-articular injection/PRP/stem cells; prior orthopedic surgery and timing; joint instability/CCL or other orthopedic disease; neurologic disease affecting gait; major systemic comorbidity; pregnancy/lactation/breeding; indoor-only status for cats when required; ability to attend visits/follow-up.

Study-team-confirmed rather than owner-required: formal LOAD/CBPI/FMPI scores; radiographic OA grade; muscle loss; objective gait/force-plate thresholds; laboratory eligibility; investigator assessment of clinically significant comorbidity.

Recommended result states: `potential_match`, `possible_match_needs_confirmation`, `likely_not_eligible`, with explicit reason rather than percentage match.

## Final count for this sweep

- 11 unique current treatment protocols at high confidence after site-level deduplication.
- +1 Cornell radiofrequency treatment candidate requiring explicit enrollment reconfirmation.
- 4 current observational/research/biosample opportunities kept separate.
- Several current site listings remain deliberately uncounted because protocol identity could overlap already counted multicenter sponsor studies.

This is intentionally conservative: a site is not a trial, a live page is not automatically active enrollment, and unknown sponsor identity is not grounds to create a duplicate.
