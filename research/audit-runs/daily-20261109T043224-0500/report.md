# DAILY GLOBAL WORK AUDIT — daily-20261109T043224-0500

**Итог: INCOMPLETE по клинической полноте; обработка всей доступной работы — PASS.**

**Фактическое время:** 9 ноября 2026 года, 04:32:34–05:18:12 America/New_York.  
**Режим:** DAILY GLOBAL WORK AUDIT, плановый запуск.  
**Результат:** UPDATE опубликован в `main`; production и отображаемый поиск проверены.

## Новые исследования

**0.** Global discovery не дал нового лечебного lead, подтверждённого отдельным официальным protocol-level документом и не представленного в canonical catalog.

## Что исправлено

1. Для `ncsu-feline-cancer-legacy-tissue` исправлен срок: официальный текущий протокол NC State указывает **Enrollment Finish 09/18/2027**. Статус изменён с «Recruiting through September 30, 2026» на «Recruiting for tissue donation through September 18, 2027»; `recruitment_end` — `2027-09-18`. Это observational/nonmatching запись, поэтому число публичных matching-возможностей не изменилось.
2. Полностью перечитаны и сверены по текущим первичным документам шесть протоколов: `uf-osa-vaccine`, `uf-osa-mrna`, `purdue-bladder-pdl1-vinblastine-deracoxib`, `ch-zurich-canine-meningioma-genomic-rt`, `ch-zurich-sts-fluorescence-guided-surgery`, `osu-oral-melanoma`. Для них проверены identity, sites, eligibility, funding и contacts; обновлены даты верификации, а для Zurich meningioma добавлены подтверждённые funding-поля.

## Закрыто или скрыто

**0.** Ни один активный matching-протокол не пересёк подтверждённый срок набора.  
**Новые источники: 0.**

## Поиск и охват

- Обработка очереди: **161/161 источников, 12/12 регионов; недоделанная работа исполнителя: 0**.
- Фактически запрошены 138 источников. Для 23 источников сохранены точные ранее документированные access restrictions; запрещённые маршруты повторно не обходились, даты проверки им не обновлялись.
- Разобраны 516 route-decisions: 389 retrieved, 51 insufficient, 76 exact restriction. После недостаточного shell-чтения выполнено 47 записанных Web-fallback чтений тех же официальных URL.
- Global discovery: 48 отдельных начальных запросов и 24 углубляющих запроса для слабой выдачи. Выполнены оба прохода — current/undated и свежие сигналы с семидневным перекрытием.
- Охвачены США, Канада, Великобритания, континентальная Европа, Латинская Америка/Карибы, Австралия/Новая Зеландия, Восточная, Южная и Юго-Восточная Азия, Ближний Восток, Северная Африка и Африка южнее Сахары. Использовались английский, французский, немецкий, итальянский, нидерландский, испанский, португальский, японский, корейский, китайский, хинди, индонезийский, вьетнамский, тайский, иврит, арабский, турецкий и суахили.
- Care/services directories не включались. Клинические trial pages BluePearl, VCA и Ethos входили в обход.

## Ежедневная проверка сроков набора

Проверены **318/318 canonical records** независимо от cadence глубокого перечитывания. Найдено 19 известных cutoff-дат; активных записей с уже прошедшим подтверждённым cutoff — **0**. Четыре прошедшие даты относятся к неактивным либо неоднозначным historical records и не показываются как действующий набор. Срок NC State исправлен на 18 сентября 2027 года по свежему официальному evidence.

## Что осталось нерешённым

| Итог источника | Количество | Причина |
|---|---:|---|
| Fully reconciled | 0 | Ни один source-level roster не получил достаточное свежее evidence по всем обязательным фактам источника |
| Partial | 138 | Источник прочитан, но полный текущий roster/primary evidence недостаточен |
| Unreachable | 0 | Весь источник не объявлялся недоступным из-за отдельного маршрута |
| Not checked | 23 | Запрос не повторялся из-за точного сохранённого access restriction |

Strict receipt: **INCOMPLETE — 161 evidence gaps, 0 schema errors**. Gap validator: **PASS / EXTERNAL_GAPS_ONLY**. Причины: `roster_unestablished` — 124, `discovery_source_not_trial_roster` — 11, `source_unavailable` — 26; все квалифицированы как `external_blocker`, а не скрытая недоделанная работа.

Durable issue accounting: было 66, закрыто текущим evidence 6, осталось **60 BLOCKED**: 47 вопросов полного протокола и 13 независимых matcher-selection проверок. Доступных несделанных шагов в очереди нет.

Из 154 публичных протоколов полное текущее перечитывание всех clinical facts сегодня выполнено для **6**. Для остальных 148 выполнены применимые ежедневные проверки источника/roster и срока набора, но полный индивидуальный protocol reread в этом запуске не заявляется. Отдельная проверка независимых selection-cases дала **0/154 новых reviews после старта этого запуска**; сохранённая review-база покрывает 142/154, pending — 12. Эти две метрики не смешиваются.

Новых unresolved лечебных leads, rejected leads или semantic duplicates, требующих изменения canonical catalog, нет. Ручные действия Юлии сейчас не нужны.

## Каталог до → после

| Метрика | До | После |
|---|---:|---:|
| Canonical records | 318 | 318 |
| Public matchable | 154 | 154 |
| Treatment trials | 150 | 150 |
| Other treatment access | 4 | 4 |
| Sources | 161 | 161 |

## Технический результат

- Среда: **PASS** — Python 3.12.14, Git 2.52.0, рабочий репозиторий доступен.
- Execution gate: **PASS** по учёту; clinical reconciliation отдельно **INCOMPLETE**.
- PASS: source inventory, catalog/schema, sanitation, links, matcher selection JS/Python parity, matcher logic, loading regression, static build, production sync, evidence-key checks и gap-review.
- Loading regression: **PASS** — ранний поиск, delayed load USA/Japan и отказ загрузки не дают ложный ноль.
- Ожидаемый неполный validator: strict receipt `INCOMPLETE`; fresh independent protocol-source review `0/154` после старта запуска.
- Основной опубликованный data/audit commit `main`: `5fb93ed28803a83764d111f8d85d8c1a78c67b61`.
- Production assets: **PASS**, live HTML/JS/catalog побайтно совпадают со сборкой. Catalog SHA-256 `1a0e8fc242b02681db7de7f7499a84ebb36251b7052b31340f345a4b4eb27568`; matcher JS SHA-256 `a9b0a97ca943bb005fc4d5eea77839df43df2e220aaa15c43dd5af7210628375`; script version `clinical-audit-20261103-owner-rules-r1`.
- Live USA search: **PASS — 98** отображаемых возможностей, совпадает с текущим каталогом.
- Live Japan search: **PASS — 14** отображаемых возможностей, совпадает с текущим каталогом.

## Даты проверки источников и readback

Baseline inventory SHA-256: `842688f62a226eec94ea258398e7992ac28e5c035d511e420e248cebd5fa8ec2`; новый и remote SHA-256: `5dab38ac0db0db917ded7dcf9f2265441b1b1fb622c25d62e05e6bb46d940bca`.

Распределение `last_checked` до и после одинаково из-за повторного запуска в тот же день: 138 источников — 2026-11-09, 16 — 2026-11-06, 7 — 2026-11-08. При этом 138 фактически посещённым источникам записаны новые точные `last_checked_at`; 23 restricted-источникам даты не менялись. Local readback: **PASS**. Remote-main readback: **PASS** на `5fb93ed28803a83764d111f8d85d8c1a78c67b61`.

**Причина окончания:** вся разрешённая доступная работа завершена; остались только документированные внешние пробелы и запрещённые маршруты. Полное клиническое подтверждение остаётся **INCOMPLETE**.

## Подробные материалы

- [Receipt](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261109T043224-0500/receipt-final.json)
- [Gap review](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261109T043224-0500/gap-review.json)
- [Execution review](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261109T043224-0500/execution-review.json)
- [Deadline review](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261109T043224-0500/deadline-review.json)
- [Full protocol reviews](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261109T043224-0500/full-protocol-reviews.json)
- [Technical summary](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261109T043224-0500/technical-summary.json)
- [Production readback](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261109T043224-0500/production-readback.json)
- [Source-date readback](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261109T043224-0500/source-date-readback.json)
- [Request results](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261109T043224-0500/request-results.json)
