# DAILY GLOBAL WORK AUDIT — 2026-11-07

**Итог: UPDATE опубликован; полное клиническое подтверждение INCOMPLETE — внешние пробелы.**

**Фактическое время America/New_York:** 2026-11-07 02:58:38–03:26:42 EST  
**Режим:** DAILY GLOBAL WORK AUDIT, плановый запуск  
**run_id:** `daily-20261107T025833-0500`

## 1. Краткий результат и публикация

Новых канонических исследований нет. Подтверждено одно существенное изменение статуса: протокол CSU по внутривенному карбоплатину при аппендикулярной остеосаркоме переведён из активного набора в **Enrollment on hold due to a national carboplatin shortage** и исключён из matcher до официального возобновления. Изменение и результаты аудита опубликованы в `main`; production readback — PASS.

## 2. Новые исследования

**0.** Global discovery не дал нового лечебного протокола, который одновременно имел бы текущий официальный protocol-level источник, достаточную идентичность исследования и подтверждённый доступ владельцев.

Четыре углублённых lead-разбора закончены так: текущая страница Missouri сопоставлена с уже существующими точными canonical IDs; программа UNAM Argovit сопоставлена с существующим мексиканским ID; Oniris BIOCERA сопоставлен с существующим watch-ID и не активирован без полной текущей multicenter roster; Calgary/Southwood STING оказался опубликованной серией из четырёх собак без текущего recruitment protocol и оставлен unresolved. genui{"citation":{"refs":["turn1597search2","turn1597search0","turn1573view3","turn1597search1"]}}

## 3. Что исправлено

1. `csu-osa-carboplatin-pain`: `available_for_matching true → false`; статус `confirmed_current → confirmed_paused`; сохранены прежние eligibility/cost facts и исходная дата полного клинического review 2026-10-10, добавлены текущие status evidence и timestamp 2026-11-07.
2. Полностью перечитаны и синхронизированы 5 текущих протоколов: `vt-canine-glioma-ced`, `mizzou-bcell-btk-bi705564`, `mizzou-feline-highgrade-lymphoma-wart`, `mizzou-pulmonary-carcinoma-gilvetmab`, `leah-bcell-cart-2026`.
3. Ежедневный deadline ledger выполнен для всех 316 canonical IDs: 13 активных структурированных сроков остаются в будущем; один прошедший срок относится к уже неактивному `ncsu-canine-ucc-il12`; новых пересечений срока активными записями нет.
4. Обновлены source attempts, current-evidence receipts, durable issue queue, selection provenance и production matcher data.

## 4. Закрыто или скрыто; новые источники

**Закрыто или скрыто: 1.** CSU carboplatin pain trial скрыт из публичного matcher из-за официального hold, а не отмечен завершённым.

**Новые источники: 0.** Inventory сохранён полностью: 159 → 159.

## 5. Поиск и охват

- **Обработка очереди:** 159/159 источников; 12/12 регионов; недоделанная доступная работа исполнителя: **0**.
- Реальные master-запросы выполнены для 136 источников; для 23 exact routes сохранён действующий запрет/ограничение и запрос не повторялся. Их даты проверки не обновлены.
- План содержал 415 решений: 159 master routes, 120 записанных official fallbacks и 136 уникальных публичных primary protocol URLs. Все 120 fallback routes получили фактическую попытку либо точное restriction decision.
- Shell использовал connect timeout 5 секунд, total timeout 20 секунд и один допустимый transient retry; недостаточные/неудачные официальные страницы дополнительно проверялись Web на тех же URL без обхода CAPTCHA/login/access gates.
- Global discovery: 60 реальных запросов — 36 current/undated и 24 recent с семидневным перекрытием; по 5 запросов на каждый из 12 регионов.
- Языки: Arabic, Chinese, English, French, German, Hebrew, Hindi, Italian, Japanese, Korean, Malay, Portuguese, Spanish, Thai.
- Deadline evidence: 14 структурированных дат обработаны отдельно; для 47 current-primary shells дата не установлена, в 76 прочитанных current primary documents семантический cutoff не найден, 179 inactive/history записей не выдаются за новую primary-проверку срока.

## 6. Что осталось нерешённым

| Результат источника | Количество |
|---|---:|
| Fully reconciled / content sufficient | 1 |
| Partial / roster unestablished | 128 |
| Unreachable / source unavailable | 30 |
| Not checked | 0 |

- **Внешние причины:** 158 source-specific gaps; gap validator разделил их на 128 `roster_unestablished` и 30 `source_unavailable`. Для каждой строки сохранены вопрос, фактические URL/evidence, exhausted routes и следующий допустимый шаг.
- **Executor incomplete:** 0. Execution gate: PASS; доступных незавершённых действий нет.
- **Durable issues:** 57 было на входе, 1 resolved, 56 BLOCKED с будущим recheck/изменением primary evidence; старый остаток не закрыт автоматически.
- **Свежий полный protocol review:** 5/152 публичных записей; **147 не перечитаны полностью сегодня**. Это отдельная метрика от обработки 159 source masters. Normal independent-selection coverage остаётся 140/152, pending 12.
- **Discovery:** 4 lead decisions; 3 точных сопоставления с существующими canonical IDs, 1 unresolved completed case-series signal; новых добавлений 0. Semantic duplicate candidates: 0.
- **Ручные действия Юли:** сейчас не требуются. Спорные медицинские статусы не менялись без достаточного primary evidence.

Вся разрешённая очередь обработана; полное подтверждение INCOMPLETE — внешние пробелы и 147 публичных протоколов без сегодняшнего полного перечитывания.

## 7. Каталог до → после

| Метрика | До | После |
|---|---:|---:|
| Canonical records | 316 | 316 |
| Public matchable | 153 | 152 |
| Treatment trials | 149 | 148 |
| Other treatment access | 4 | 4 |
| Sources | 159 | 159 |

## 8. Технический результат

- **Среда:** PASS — `/workspace/scratch/fd10c0821871`, Python 3.12.14, git 2.52.0.
- **Execution gate:** PASS; clinical reconciliation INCOMPLETE; discovery clinical-completeness label INCOMPLETE. PASS учёта не трактуется как медицинская полнота.
- **Strict receipt:** INCOMPLETE, 158 coverage gaps, ошибок формата нет.
- **Gap review validator:** PASS; strict coverage INCOMPLETE.
- **Catalog/schema:** PASS — 316 IDs, 152 active/public.
- **Sanitation:** PASS — 4 known partial records, новых partial нет.
- **Semantic dedupe:** PASS — 0 probable duplicates.
- **Matcher selection JS/Python:** PASS; public 152; disease parity 18,240 checks.
- **Fresh full-review gate:** INCOMPLETE — 5/152, remaining 147.
- **Build:** PASS.
- **Loading regression:** PASS — ранний поиск, delayed load USA/Japan и load failure не дают ложный ноль; USA 98, Japan 12.
- **Matcher logic:** PASS — 152 trials.
- **Production sync:** PASS — total 152, treatment 148, other access 4, internal links 7,058.
- **Repository hygiene:** PASS.
- **Preflight:** PASS_WITH_INCONCLUSIVE — обязательные проверки прошли; отдельный Streamlit test NOT VERIFIED, потому что в runtime отсутствует модуль `streamlit`.
- **Публикация:** canonical data commit `f1914bde447df95fc8d16229ba1f1a9caaf23c6d`; production-verification commit/main `3e655256000c12dfc80382e3237f16e50f04b2a9`.
- **Deploy/production:** PASS. Live `trials.json` SHA-256 `0c2bb7a753b40ead234c86fe459102b5bc79c0f286d8225a37985956d2ac1773`; live `matcher.js` SHA-256 `a9b0a97ca943bb005fc4d5eea77839df43df2e220aaa15c43dd5af7210628375`; оба совпадают со сборкой. Production HTML загружает `./matcher.js?v=clinical-audit-20261103-owner-rules-r1`.
- **Live matcher UI:** PASS — Dog / Cancer — any type / diagnosis “I don't know” / пустые age, weight и ZIP / все варианты лечения / Any approach: USA 98, Japan 12; извлечённые браузером названия полностью совпали с текущим catalog render.
- **Даты проверки источников:** до запуска все 159 имели `last_checked=2026-11-06`; после запуска 136 фактически запрошенных sources получили `2026-11-07`, 23 restriction-only sources честно сохранили `2026-11-06`.
- **Local/remote readback:** PASS. Git blob SHA совпадают: `trials_base.json` `5f4193fa45c05065ddd029cab63343e6828fb030`; `source_inventory.json` `ea97b5f3d349cdd29d12c76d9890e37570ab9b29`; `audit_state.json` `2fc353f181af13234e9fb8d6024845c4e6282760`.
- **Причина окончания:** доступная разрешённая работа закончена; установленный предел не достигнут; runtime failure не было.

Подробные receipts, timestamps, hashes, команды, discovery evidence, deadline ledger, полные USA/Japan title lists и source-specific evidence сохранены в `research/audit-runs/daily-20261107T025833-0500/`.
