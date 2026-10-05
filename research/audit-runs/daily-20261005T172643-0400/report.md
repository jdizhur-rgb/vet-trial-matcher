2026-10-05 17:46 America/New_York
Режим: DAILY GLOBAL WORK AUDIT

Run ID: `daily-20261005T172643-0400`

**Общий статус: НЕ ЗАВЕРШЁН (INCOMPLETE).** Все 76 исходных обязательных trial sources и 2 новых источника были фактически попытаны, даты сохранены и подтверждены из remote `main`, но доказанный текущий roster/status получен только для 8 из 78 источников. По Execution and report gate остальные 63 доступны лишь частично, 7 недоступны; поэтому проход нельзя называть завершённым.

Care-directory scope сознательно не выполнялся: клиники, онкологи, ACVIM/VetSpecialists, BluePearl/VCA/Ethos care rosters, ECT и teleconsultations относятся к отдельному субботнему аудиту.

## Health-gate

- Core/data/production: **PASS** — canonical JSON читается; `299` уникальных IDs; sanitation не выявил новых partial records; semantic duplicate candidates `0`; compile/import PASS; static build PASS; matcher regression PASS; production synchronization PASS.
- Local Streamlit harness: **INCONCLUSIVE / NON-BLOCKING** — пакет `streamlit` отсутствует в текущей среде.
- Production: **PASS** для `https://vettrialfinder.com/` и `/matcher/`; homepage показывает `158` текущих treatment opportunities. Отдельный Streamlit URL и прямой JSON route не удалось независимо прочитать внешним retriever, поэтому этот ancillary signal остаётся INCONCLUSIVE.

## 1) Known-source coverage

- Inventory до запуска: `76`; после добавления новых официальных trial sources: `78`.
- Фактически предприняты попытки: `78/78`.
- Достаточный roster/status evidence: `8`.
- Partial: `63`.
- Unreachable: `7`.
- Fresh normalized-content fingerprint записан для `70`; для 7 полностью недоступных маршрутов сохранён прежний fingerprint без утверждения `unchanged`.
- Fingerprint changed против предыдущего `main`: `30` (изменение fingerprint само по себе не трактовалось как медицинское изменение).

### Источники с достаточным roster evidence

| Source | Result | Protocols seen | Candidates | Protocol pages | Official route |
|---|---:|---:|---:|---:|---|
| `registry-uk-vcsr` | unchanged | 1 | 1 | 0 | `www.veterinarystudiesregistry.co.uk/studies` |
| `usa-auburn-vet-clinical-trials` | changed | 1 | 0 | 0 | `www.vetmed.auburn.edu/research/clinical-trials/` |
| `usa-minnesota-current-clinical-trials` | changed | 4 | 0 | 0 | `vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials` |
| `usa-illinois-clinical-trials` | changed | 7 | 0 | 0 | `vetmed.illinois.edu/research/clinical-trials/` |
| `usa-utsw-vroc-clinical-trials` | changed | 8 | 0 | 0 | `www.utsouthwestern.edu/departments/radiation-oncology/veterinary-research-oncology-clinic/clinical-trials.html` |
| `switzerland-zurich-clinical-studies` | changed | 4 | 0 | 0 | `www.tierspital.uzh.ch/kleintiere/onkologie/krebs-tumore-klinische-studien/` |
| `usa-kansas-state-vhc-oncology` | changed | 2 | 2 | 2 | `www.ksvhc.org/services/clinical-trials/current-trials/index.html` |
| `usa-petcure-oncology-clinical-trials` | changed | 0 | 0 | 0 | `petcureoncology.com/clinical-trials/` |

Примечание: `protocols_seen` — число текущих oncology-study rows, реально перечисленных на официальном roster; treatment-only решение применено отдельно. UK-VCSR показал один AI-generated sample, K-State — два oncology studies, но оба исключены из Main Trial Finder (observational monitoring и supportive-care probiotic arm).

### Fallback cases

| Source | Master result | Fallback outcome |
|---|---|---|
| `registry-avma-veterinary-clinical-trials` | HTTP 200 / insufficient | `veterinaryclinicaltrials.org/studies/` → HTTP 200 / insufficient |
| `usa-penn-vet-clinical-trials` | HTTP 404 / unreachable | `www.vet.upenn.edu/clinical-trial/` → HTTP 200 / fetched; `www.vet.upenn.edu/veterinary_specialty/oncology/` → HTTP 200 / fetched; `www.vet.upenn.edu/ryan-hospital/clinical-trials/` → HTTP 200 / fetched |
| `usa-ethos-clinical-studies` | HTTP 404 / unreachable | `www.ethosvet.com/medical-professionals/` → HTTP 200 / fetched; `www.ethosvet.com/faqs-clinical-studies-at-ethos/` → HTTP 200 / fetched |
| `usa-ethos-discovery-studies` | HTTP 404 / unreachable | `www.ethosdiscovery.org/scientific-programs/` → HTTP 200 / fetched; `www.ethosdiscovery.org/scientific-programs/page/2/` → HTTP 200 / fetched |
| `usa-anivive-trials` | HTTP 525 / unreachable | `anivivelifesciences.com/treatments` → HTTP 525 / unreachable |
| `uk-rvc-clinical-investigation-centre` | HTTP 403 / unreachable | `www.rvc.ac.uk/research/facilities-and-resources/clinical-investigation-centre/projects` → HTTP 403 / unreachable |
| `usa-kansas-state-vhc-oncology` | HTTP 200 / fetched | `www.ksvhc.org/services/clinical-trials/` → HTTP 200 / sufficient; `www.ksvhc.org/services/clinical-trials/current-trials/index.html` → HTTP 200 / sufficient |
| `usa-wsu-vth-clinical-studies` | HTTP 403 / unreachable | `hospital.vetmed.wsu.edu/small-animal/cats-and-dogs/oncology/` → HTTP 403 / unreachable |
| `japan-kamogawa-oncology-news` | HTTP 200 / insufficient | `www.kamogawa-ac.jp/2026/09/30/24722/` → HTTP 200 / fetched |
| `japan-yamaguchi-vmc-clinical-trials` | HTTP 200 / insufficient | `ds.cc.yamaguchi-u.ac.jp/~yuamec1/` → HTTP 200 / insufficient |
| `japan-jvcog-current-clinical-trials` | HTTP 200 / insufficient | `www.jvcog.jp/clinical/03rinsho.html` → HTTP 200 / insufficient |
| `sponsor-paccal-vet-owner-trials` | HTTP 200 / sufficient | `www.paccalvet.com/hemangiosarcoma-study` → HTTP 200 / sufficient; `www.paccalvet.com/cat-cancer-study` → HTTP 200 / sufficient |

### Недоступные источники (7)
- `directory-veterinary-cancer-society`: [vetcancersociety.org/resources/clinical-trials/](https://vetcancersociety.org/resources/clinical-trials/) — HTTP 403
- `usa-missouri-oncology-clinical-trials`: [vhc.missouri.edu/small-animal-hospital/oncology/clinical-trials/current-clinical-trials/](https://vhc.missouri.edu/small-animal-hospital/oncology/clinical-trials/current-clinical-trials/) — HTTP timeout
- `usa-anivive-trials`: [anivivelifesciences.com/trials](https://anivivelifesciences.com/trials) — HTTP 525; [anivivelifesciences.com/treatments](https://anivivelifesciences.com/treatments) — HTTP 525
- `uk-rvc-clinical-investigation-centre`: [www.rvc.ac.uk/research/facilities-and-resources/clinical-investigation-centre](https://www.rvc.ac.uk/research/facilities-and-resources/clinical-investigation-centre) — HTTP 403; [www.rvc.ac.uk/research/facilities-and-resources/clinical-investigation-centre/projects](https://www.rvc.ac.uk/research/facilities-and-resources/clinical-investigation-centre/projects) — HTTP 403
- `usa-wsu-vth-clinical-studies`: [hospital.vetmed.wsu.edu/appointments/](https://hospital.vetmed.wsu.edu/appointments/) — HTTP 403; [hospital.vetmed.wsu.edu/small-animal/cats-and-dogs/oncology/](https://hospital.vetmed.wsu.edu/small-animal/cats-and-dogs/oncology/) — HTTP 403
- `usa-nci-comparative-oncology-trials`: [ccr.cancer.gov/comparative-oncology-program/trials](https://ccr.cancer.gov/comparative-oncology-program/trials) — HTTP 403
- `usa-veterinary-cancer-care-clinical-trials`: [vetcancercare.com/clinical-trials/](https://vetcancercare.com/clinical-trials/) — HTTP 403

### Частично проверенные источники (63)

У этих источников маршрут открылся полностью или частично, но текущий roster/status не был доказан в форме, требуемой repaired gate (`protocols_seen` integer + roster evidence). Они не засчитаны как successfully checked:

- `registry-avma-veterinary-clinical-trials`, `usa-colorado-state-vth-clinical-trials`, `usa-cornell-vet-clinical-trials`, `usa-iowa-state-vmc-clinical-trials`, `usa-johns-hopkins-cigat`, `usa-lsu-vet-clinical-trials`, `usa-michigan-state-oncology-trials`
- `usa-nc-state-clinical-trials`, `usa-ohio-state-current-trials`, `usa-oregon-state-oncology-trials`, `usa-penn-vet-clinical-trials`, `usa-purdue-wcorc-clinical-trials`, `usa-tennessee-vet-clinical-trials`, `usa-tufts-clinical-trials`
- `usa-uc-davis-vcct`, `usa-florida-oncology-trials`, `usa-florida-feline-oncology-trials`, `usa-georgia-clinical-trials`, `usa-bluepearl-science-clinical-studies`, `usa-virginia-tech-current-studies`, `usa-wisconsin-oncology-studies`
- `usa-ethos-clinical-studies`, `usa-ethos-discovery-studies`, `usa-medvet-clinical-studies`, `usa-castr-alliance-studies`, `canada-ovc-active-oncology-trials`, `europe-esvonc-ongoing-trials`, `europe-oncowaf-clinical-trials`
- `netherlands-utrecht-interventional-oncology`, `italy-milan-veterinary-studies`, `usa-sage-veterinary-clinical-trials`, `usa-amcny-current-clinical-trials`, `usa-penn-comparative-immunotherapy-trials`, `australia-uq-school-veterinary-clinical-trials`, `australia-uq-vets-clinical-research-trials`
- `australia-gamgee-cancer-vaccine-trial`, `australia-pettrials-directory`, `australia-sash-clinical-research`, `australia-caninecancer-state-research-guide`, `australia-medipaws-clinical-research`, `australia-bvsc-foundation`, `australia-anzcvs-science-week-oncology`
- `usa-barc-clinical-trials`, `sponsor-vivesto-paccal-status`, `usa-penn-atherton-laboratory`, `usa-canine-cancer-alliance-research`, `usa-vrcco-clinical-trials`, `usa-tamu-hayburn-oncology-studies`, `china-dongjun-oncology-trials`
- `china-petcura-mrna-iit`, `spain-puchol-reachglio`, `japan-university-of-tokyo-vmc-clinical-research`, `japan-kamogawa-oncology-news`, `japan-yamaguchi-vmc-clinical-trials`, `japan-veterinary-cancer-society-clinical-trials`, `japan-jsamc-current-clinical-trials`
- `global-vettrials-directory`, `canada-saskatchewan-wcvm-research-requests`, `japan-jvcog-current-clinical-trials`, `brazil-usp-loct-oncolytic-virus-program`, `japan-nvlu-vmc-clinical-research`, `sponsor-paccal-vet-owner-trials`, `brazil-estima-coe-clinical-studies`

## 2) Global new-source discovery

Проверены: USA; Canada; UK; continental Europe (английский/французский/немецкий); Mexico/Central America/Caribbean и South America (испанский/португальский); Australia/New Zealand; East/South/Southeast Asia (японский/корейский/китайский + English); Middle East; Africa. Использовались свежие сигналы и недатированные/current страницы.

Результат слоя: **COMPLETE для запланированного регионального query pass**, но не компенсирует incomplete known-source roster audit.

## 3) NEW

- **Confirmed trial additions: 0.**
- `data/trials_base.json`: **NO CHANGE**.

## 4) UPDATE

- Trial records: `0`.
- Обновлена только audit/source metadata и unresolved evidence.

## 5) CLOSE/HIDE

- `0` trial records. Paccal Vet остаётся скрытым: owner pages предлагают участие, но Vivesto сообщил о завершении recruitment и результатах; новый cohort не подтверждён.

## 6) NEW SOURCES

- [`sponsor-paccal-vet-owner-trials`](https://www.paccalvet.com/) — официальный owner-facing master с canine splenic hemangiosarcoma и feline solid-tumor pages. Добавлен как `partial`: текущая participation language конфликтует с sponsor completion reports.
- [`brazil-estima-coe-clinical-studies`](https://estima.com.br/coe/) — официальный Centro de Oncologia Estima; программа и screening route подтверждены, но named current roster не опубликован, поэтому `partial`.

Дополнительно для K-State сохранены два official fallback routes: `/services/clinical-trials/` и `/services/clinical-trials/current-trials/index.html`.

## 7) UNRESOLVED

- **Новый:** `pettrials-murdoch-checkpoint-combination-20261005` — PetTrials показывает recruiting Murdoch checkpoint-inhibitor combination, но текущая primary Murdoch protocol page с intervention, eligibility, costs и owner access не найдена; `recheck_after: 2026-10-12`.
- **Обновлён:** `bluepearl-paccal-status-conflict-20260930` — теперь явно включает конфликт с текущими Paccal Vet owner pages; record остаётся non-matchable, `recheck_after: 2026-10-07`.

## 8) REJECTED / DUPLICATES

- UK-VCSR canine lymphoma immunotherapy — отвергнут как явно `Sample study (AI-generated)`.
- K-State radiation pain/activity monitoring — observational/monitoring only.
- K-State probiotic during CHOP — supportive-care intervention only; anticancer treatment (CHOP) не является исследуемым treatment arm.
- Paccal canine/feline pages — existing protocol/cohort evidence, не новые trials; новые записи не создавались.
- Semantic duplicate detector: `0` probable duplicates.

## 9) ТРЕБУЕТ РУЧНОЙ ПРОВЕРКИ ЮЛИ

Нет. Неоднозначные находки оставлены в unresolved и не опубликованы как trials.

## 10) Exact counts before → after

| Metric | Before | After |
|---|---:|---:|
| Canonical records | 299 | 299 |
| Public opportunities | 163 | 163 |
| Strict treatment opportunities | 158 | 158 |
| Other treatment access | 5 | 5 |
| Treatment countries | 15 | 15 |
| Treatment centers/programs | 87 | 87 |
| Trial source inventory | 76 | 78 |
| Unresolved items | 21 | 22 |

Strict treatment opportunities by country (unchanged): Australia 3; Belgium 2; Canada 3; China 4; Denmark 1; France 5; Italy 2; Japan 8; Mexico 1; Portugal 3; Spain 1; Switzerland 7; Taiwan 2; UK 5; USA 111.

Species counts (one Dog/Cat record contributes to both species): Dog 146; Cat 17.

## 11) Изменённые файлы и exact data diff

- `data/trials_base.json`: **без изменений**.
- `data/source_inventory.json`: timestamps/results/attempt receipts/fingerprints для 78 фактически попытанных источников; +2 sources; +2 K-State fallbacks.
- `data/audit_source_coverage.json`: новый latest receipt.
- `data/audit_state.json`: новый trial-only run state; care counters не переносились.
- `data/audit_unresolved.json`: +1 unresolved; уточнён Paccal conflict.
- `research/audit-runs/daily-20261005T172643-0400/`: immutable receipt, evidence, checkpoints, discovery log, before-date snapshot, exact data diff и этот report.

Полный exact patch сохранён как [`exact-data.diff`](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261005T172643-0400/exact-data.diff). Substantive trial-data diff: **none**.

## Даты проверки источников

- Всего sources: `78`; фактически предприняты попытки: `78`; timestamps подтверждены из remote `main`: `78`.
- Successfully roster-checked: `8`; partial: `63`; unreachable: `7`.
- Сохранённый диапазон `last_checked_at`: `2026-10-05T17:30:12-04:00` → `2026-10-05T17:36:39-04:00`.
- Same-day rerun: все 76 прежних sources получили новый `last_checked_at` после утреннего `06:45:26-04:00`; два новых sources прошли `null → current-run timestamp`.
- Старые/отсутствующие/несовпадающие current-run dates после remote readback: **0**.
- Remote data commit: [`db0426309419f14ca4230284791441d0209a6ea0`](https://github.com/jdizhur-rgb/vet-trial-matcher/commit/db0426309419f14ca4230284791441d0209a6ea0).
- Remote inventory blob SHA: `99c86cc2b7ebbd3b5c4f38b6bb9af08b48fd7445`.
- Remote immutable receipt blob SHA: `3f073eb26b844eaeb6bc8237052567571258e081`.
- Persisted-date verification: **PASS**. Fresh date означает попытку, а не успешный roster review.

## 12) Validators, commit, deploy и production

PASS:

- `scripts/validate_audit_receipt.py` (latest и immutable receipt)
- `scripts/validate_source_inventory.py` (`78` sources)
- `scripts/validate_trials_catalog.py` (`299` records, `299` unique IDs, `163` active)
- `scripts/validate_catalog_sanitation.py` (no new partial records)
- `scripts/semantic_dedupe_catalog.py` (`0` probable duplicates)
- `scripts/full_catalog_audit.py`
- `scripts/build_static_site.py`
- `scripts/test_matcher_logic.js` (`163` opportunities)
- `scripts/validate_production_sync.py` (`163 = 158 treatment + 5 access`)

Remote workflows for the audit data commit:

- [Full catalog integrity audit](https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/37377728186) — success.
- [Build and deploy static site](https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/37377728220) — success.

Production readback: homepage and matcher reachable; homepage count `158` matches the strict treatment build count. Streamlit session signal remains INCONCLUSIVE, not FAIL.

## 13) NO CHANGE

Clinical trial catalog: **NO CHANGE**. Новых treatment-only opportunities, подтверждённых protocol-level primary source и current owner access, в этом проходе не добавлено.

**Итог: НЕ ЗАВЕРШЁН.** Metadata persistence, commit, CI/deploy и production checks прошли, но repaired roster-evidence gate не позволяет считать 70 источников покрытыми. Никаких данных trials на основании partial/unreachable источников не изменено.
