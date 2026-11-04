# DAILY GLOBAL WORK AUDIT — 2026-11-04

**Итог: INCOMPLETE.** Вся разрешённая очередь обработана; полное подтверждение INCOMPLETE — внешние пробелы.

**Фактическое время America/New_York:** 2026-11-04 03:00:07–03:41:32 EST  
**Режим:** DAILY GLOBAL WORK AUDIT  
**run_id:** `daily-20261104T030007-0500`  
**Результат данных:** NO CHANGE в составе публичного каталога; обновлены подтверждённые даты двух полных клинических перечитываний и сегодняшний source/audit accounting.  
**Публикация:** PASS — canonical/data commit `3596f02f746e042126f9a830b5b43ca4b4cd7e96` опубликован в `main`; GitHub Pages deploy завершён успешно; live-файлы совпадают с пересобранным сайтом.

## Новые исследования

**0.** Новых лечебных исследований с достаточным protocol-level подтверждением не найдено. Все выявленные сигналы сопоставлены с существующими canonical IDs либо оставлены как закрытые, нетерапевтические, вторичные или нерешённые leads.

## Что исправлено

1. Полностью перечитаны по текущим официальным документам два протокола, у которых наступил 28-дневный срок глубокой проверки:
   - `jp-nvlu-survivin-peptide-vaccine-2026`: подтверждены identity, единственный сайт NVLU, eligibility, вмешательство, контакт и опубликованное окно исследования до 2027-03-31; публичной суммы покрытия расходов владельца нет.
   - `uf-boxer-glioma-autogenic-vaccine`: официальная страница говорит **NOW RECRUITING**; подтверждены Boxer/MRI eligibility, biopsy + autogenic tumor-RNA vaccine, три дозы, Gainesville, funding и контакты.
2. Для этих двух записей обновлены только подтверждённые `verified`, `funding_verified` и `protocol_reviewed_at`; клинические поля и публичный состав каталога не изменились.
3. Выполнена ежедневная независимая проверка сроков набора всех 315 canonical records. Опубликованная дата окончания исследования использовалась как дата окончания набора, когда источник одновременно показывал продолжающийся набор и отдельной recruitment date не было.

## Закрыто или скрыто

**0.** Сегодня не закрыто и не скрыто ни одной canonical записи. В текущем AVMA JSON 856 записей, как и вчера; новых/удалённых записей нет, oncology Recruiting остаётся 56. Единственное изменение объекта AVMA — служебный `status_color` у уже Completed записи — не меняет статус каталога.

**Новые источники: 0.** Inventory сохранён полностью: 157 → 157.

Дополнительные сигналы:
- форма UNLP показывает `Inscripción cerrada`; соответствующая возможность не была добавлена в canonical catalog;
- Purdue M029 остаётся exact existing `purdue-m029-shp1-inhibitor` и требует медицинского решения о treatment inclusion, новый ID не создан;
- Saskatchewan RT pages описывают imaging/planning comparisons для животных, уже получающих RT, и квалифицированы как NOT_TREATMENT;
- BluePearl HSA, PetTrials AU, PetCura и Akston сопоставлены с существующими exact canonical families/IDs; знакомый домен сам по себе дублем не считался.

## Поиск и охват

**Обработка очереди: 157/157 источников, 12/12 регионов; недоделанная работа исполнителя: 0.**

- Master routes: 127 получены, 24 exact сохранённых access restrictions обработаны без запрещённого запроса, 6 запросов завершились ошибкой.
- Official fallbacks: проверены 112 URL у 61 источника, включая фактически выполненные 11 маршрутов, обнаруженные строгим валидатором после первого прохода.
- Очевидные официальные protocol-child routes: 74 URL у 31 источника.
- Все 154 публичных primary protocol routes получили сегодняшнее индивидуальное решение по доступу, статусу и сроку: 116 получены, 37 exact restricted routes проверены по сохранённому ограничению без обхода, 1 route дал 503.
- Это **не** означает 154 полных клинических перечитывания. Полный пятифакторный reread сегодня: **2/154**; остальные **152/154** получили маршрутное/status/deadline решение, но не новый полный reread.
- Независимые source-derived selection cases: текущая полная проверка 2/154; сохранённое достаточное покрытие 141/154, pending 13; 758 cases, 1461 matcher checks и 18 480 parity checks прошли.
- Global discovery: два прохода, 48 отдельных country/language searches — current/undated и recent seven-day overlap — по США, Канаде, Великобритании, континентальной Европе, Латинской Америке/Карибам, Австралии/Новой Зеландии, Восточной, Южной и Юго-Восточной Азии, Ближнему Востоку, Северной Африке и Африке южнее Сахары. Использованы английский и местные языки; слабые выдачи углублены до первичных страниц либо честного unresolved/secondary disposition.
- Сроки набора: 315/315 records рассмотрены; 14 имеют известную recruitment/end cutoff, из них 13 будущих активных и 1 прошедший уже inactive. Новых истёкших сроков: 0; продлений: 0; новых исключений: 0.

## Что осталось нерешённым

| Итог источника | Число | Что это означает |
|---|---:|---|
| fully reconciled | 13 | Текущий roster/status достаточен по сегодняшнему evidence |
| partial | 115 | Источник обработан, но полный текущий roster или protocol evidence не установлен |
| unreachable / restriction-only | 29 | 23 exact сохранённых ограничения без обхода + 6 фактических ошибок запроса |
| not processed | 0 | Нет пропущенного источника в разрешённой очереди |

Strict receipt: **INCOMPLETE**, 144 evidence gaps: 106 `roster_unestablished`, 29 `source_unavailable`, 9 `discovery_source_not_trial_roster`. Gap-review schema/logic: **PASS**; все 144 строки классифицированы как `external_blocker`, не как скрытая незавершённая работа исполнителя.

Durable issue queue: 58 до запуска → 2 resolved → 56 остаются: 49 BLOCKED и 7 OWNER_DECISION rows. Семь строк OWNER_DECISION относятся к шести различным вопросам, потому что Mexico silver nanoparticle представлен отдельными full-protocol и independent-selection строками.

Решения Юли действительно нужны по шести вопросам:
1. WSU STS local immunotherapy — считать ли safety/biological-effect TCE protocol лечебным matching при неподтверждённом текущем intake.
2. Tufts HSA — удалить ли неподтверждённую оговорку о $1,500 reimbursement.
3. Missouri OSA carboplatin timing — оставить ли публичный matching без явного текущего intake.
4. Mexico silver nanoparticle — может ли запись оставаться публичной без текущего protocol-level intake/eligibility/costs treating institution.
5. UC Davis liver TAE/TACE — как сузить absolute exclusion и неподтверждённое покрытие diagnostic costs.
6. MedVet EGFR/HER2 vaccine — как представить VCCS-only diagnostic exceptions/local exclusions при отличающихся правилах других площадок.

Unresolved/rejected/duplicates: новых canonical unresolved additions — 0; rejected/not-treatment/secondary/closed leads сохранены индивидуально; probable semantic duplicates — 0.

## Каталог до → после

| Метрика | До | После |
|---|---:|---:|
| canonical records | 315 | 315 |
| public matchable | 154 | 154 |
| treatment trials | 150 | 150 |
| other treatment access | 4 | 4 |
| mandatory sources | 157 | 157 |

## Технический результат

- Среда: **PASS** — `pwd`, Python 3.12.14, git 2.51.1 реально выполнены.
- Execution gate: **PASS** для учёта выполнения; отдельно clinical reconciliation **INCOMPLETE**, discovery completeness **INCOMPLETE**. Accounting PASS не выдан за клиническую полноту.
- Strict receipt: **INCOMPLETE**; strict gap validator: **PASS / coverage INCOMPLETE**.
- Catalog/schema/sanitation/source inventory/semantic dedupe/evidence-key/repository hygiene: **PASS**; probable duplicates: 0.
- Matcher build и production sync: **PASS** — 154 public, 150 treatment, 4 other access.
- Loading regression: **PASS** — ранний поиск, delayed load USA/Japan и load failure не дают ложный ноль; delayed-load expectation USA 99, Japan 12.
- Matcher logic и Python parity: **PASS**.
- Deploy workflow: **PASS**, [GitHub Actions run](https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/41800270604).
- Production byte readback: **PASS** — matcher HTML, JS, trials JSON и CSS побайтно совпадают с новой локальной сборкой. HTML использует catalog version `0901eb911e7df45e` и script version `clinical-audit-20261103-owner-rules-r1`.
- Live UI search: **PASS** — USA показал 99 карточек, Japan 12, при Dog / Cancer — any type / I don't know / пустых age, weight, ZIP / всех treatment options / Any approach. Это сравнение с текущим каталогом, а не закреплённая константа.
- Публикация данных: local/remote `main` readback **PASS** для commit `3596f02f746e042126f9a830b5b43ca4b4cd7e96`. Финальный report/readback commit публикуется отдельно после формирования этого файла, поэтому его SHA не может быть самоссылкой внутри собственного содержимого.

## Даты проверки источников

- До запуска: 137 источников имели `last_checked=2026-11-03`; остальные сохраняли исходные даты 2026-10-14…2026-11-02.
- После запуска: 134 реально открытых master routes получили `last_checked=2026-11-04` и фактические `last_checked_at`; 23 exact restriction-only источника не получили выдуманную дату визита. Их сохранённые даты оставлены без изменения.
- Local canonical/data readback: **PASS**. Remote-main canonical/data readback: **PASS**, SHA `3596f02f746e042126f9a830b5b43ca4b4cd7e96`. Production: **PASS**.

**Итог обработки:** вся разрешённая очередь обработана, executor_incomplete = 0, stop reason = `completed_available_work`.  
**Итог достаточности evidence:** **INCOMPLETE** — 13/157 источников fully reconciled, 144 имеют документированные внешние пробелы; 2/154 публичных протокола полностью перечитаны сегодня, 152/154 не выдаются за полный текущий reread.
