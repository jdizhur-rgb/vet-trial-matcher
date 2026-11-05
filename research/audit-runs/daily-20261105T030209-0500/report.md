# DAILY GLOBAL WORK AUDIT — 2026-11-05

**Статус: INCOMPLETE по клинической полноте; обработка очереди, технические проверки и публикация — PASS.**

- Фактическое время: **2026-11-05 03:02:09–03:55:32 America/New_York**.
- Режим: **DAILY GLOBAL WORK AUDIT**, плановый запуск.
- Run ID: `daily-20261105T030209-0500`.
- Результат: **1 NEW, 4 подтверждённых UPDATE, 1 новый источник, публикация PASS**.
- Вся доступная очередь обработана; полное подтверждение остаётся INCOMPLETE из-за 157 документированных внешних пробелов и 6 строк OWNER_DECISION. Несделанной доступной работы исполнителя: **0**.

## Новые исследования

**1 — LASEIT photodynamic therapy before surgery for canine liver tumors**, Virginia Tech, Blacksburg, Virginia, USA.

- Животные/опухоли: собаки с резектабельной опухолью печени.
- Лечение: КТ-направленная фотодинамическая терапия verteporfin LASEIT-PDT, затем стандартное хирургическое удаление опухоли через два дня.
- Расходы: исследование покрывает PDT, контрольные КТ и двухдневную госпитализацию и даёт **$2,000** на операцию. Владелец оплачивает диагностику до включения, дорогу, остаток стоимости операции и лечение осложнений PDT.
- Срок набора: на текущей официальной странице дата окончания набора не опубликована.
- Официальный протокол: https://research.vetmed.vt.edu/clinical-trials/current-studies/liver-tumor-pdt.html
- Canonical ID: `vt-liver-laseit-pdt`.

## Что исправлено

1. `tufts-hsa-liquid`: удалено неподтверждённое отдельное возмещение $1,500 за спленэктомию. Текущий протокол подтверждает покрытие лечения HSA до $5,000, бесплатные исследуемые препараты и лечение связанных с исследованием побочных эффектов; несвязанная помощь оплачивается владельцем.
2. Полностью перечитаны и подтверждены текущие первичные протоколы `msu-hs-quasiorganelle`, `msu-feline-mammary-met` и `eu-ch-pnst-plexus-fluorescence-surgery`.
3. Добавлен официальный Liverpool DOG-FIGhT source. Страница подтверждает текущий проект, ferumoxytol/биопсию/послеоперационную лучевую терапию и контакт, но не публикует полную eligibility и все расходы; clinical issue оставлен BLOCKED.
4. Исправлен `scripts/audit_execution_gate.py`: `seed_queue()` теперь принимает и прежний список, и актуальный wrapped `progress_receipt.rows`. Добавлен regression test; 22 теста проходят.
5. Первая публикация `source_inventory.json` через connector была повреждена на уровне байтов; CI это обнаружил. Файл повторно опубликован из точного локального UTF-8, удалённый SHA прочитан обратно, после чего integrity workflow и deploy прошли.

## Закрыто или скрыто

- **0** исследований закрыто или скрыто: новых подтверждённых переходов срока набора или точных current-closure сигналов сегодня не было.
- AVMA: текущий полный roster не удалось подтвердить. Доступный JSON `skip=500` совпал с 4 ноября; `skip=0` и Web-маршрут не дали полного roster. Новое закрытие не выводилось из неполных данных.
- **Новые источники: 1** — `uk-liverpool-dogfight-glioma-trial`.

## Поиск и охват

- Обработка очереди: **158/158 источников, 12/12 регионов; недоделанная работа исполнителя: 0**.
- Master routes исходного inventory: **157/157** — 121 retrieved, 24 exact access restrictions, 12 request failures.
- Official fallbacks: **118 маршрутов у 63 источников** — 63 retrieved, 24 restrictions, 31 failures.
- Очевидные официальные protocol routes: **74** — 64 retrieved, 10 failures.
- Individual primary routes исходного публичного каталога: **154/154** — 114 retrieved, 37 exact restrictions, 3 failures; дополнительно прочитаны новый Virginia Tech protocol, Liverpool и доступные Web-fallbacks.
- Global discovery: **48 фактических country/language searches**, по два прохода для каждого из 12 регионов: current/undated и свежие сигналы за 7 дней.
- Языки: английский, французский, немецкий, итальянский, испанский, португальский, японский, корейский, китайский, тайский, индонезийский, иврит, турецкий и арабский.
- Из четырёх квалифицированных discovery leads: 1 добавлен; 3 отклонены как не относящиеся к лечебным dog/cat oncology trials (Cambridge CTVT — диагностика, UK-VCSR-2026-00013 — equine allergy, испанская melanoma news — human phase 3). Новых дублей: **0**; unresolved discovery leads: **0**.

### Текущие протоколы и сроки набора

- Все **155/155** публичных протоколов получили сегодняшнее индивидуальное решение по доступному current status/deadline route.
- Полный пятифакторный reread сегодня выполнен для **5/155**: статус, вмешательство, eligibility, sites и расходы. Это Virginia Tech liver PDT, Tufts HSA, два MSU и Zurich PNST.
- Остальные **150/155** не объявлены полностью перечитанными: для них выполнена текущая проверка статуса/срока, но полный протокол сегодня не перечитывался либо current primary был ограничен/недоступен.
- Из 155 публичных: 9 имеют текущую опубликованную дату набора без изменения, 106 current primary прочитаны и даты не публикуют, 40 получили `NOT VERIFIED` из-за точного ограничения или сбоя current route.
- Всего известных опубликованных дат: **14**; 13 будущих активных, 1 прошедшая у уже неактивной записи (`ncsu-canine-ucc-il12`, 2026-09-30). Новых пересечённых сроков: **0**.
- Применена owner-логика: exact AVMA `Completed` закрывает exact protocol; если исследование помечено recruiting и опубликована только study end date, она используется как конец набора. Неизвестные даты не выдумывались, исходные evidence dates сохранены.

## Что осталось нерешённым

| Результат источника | Число |
|---|---:|
| Fully reconciled / checked | 1 |
| Partial | 122 |
| Unreachable по разрешённым current routes | 35 |
| Not processed | 0 |

- Strict receipt: **INCOMPLETE**, 157 gaps, integrity errors 0.
- Gap review: **PASS**, 122 `roster_unestablished`, 35 `source_unavailable`; все 157 классифицированы как документированные `external_blocker`, а не executor unfinished.
- Durable issues: **63 → 4 RESOLVED → 59 остаются**: 53 BLOCKED, 6 OWNER_DECISION rows. Шесть строк соответствуют пяти разным вопросам/trials, потому что Mexico имеет full-protocol и independent-selection строки.
- OWNER_DECISION: WSU STS local immunotherapy; Missouri OSA carboplatin timing; Mexico silver nanoparticle treatment access; UC Davis liver TAE/TACE representation; MedVet/VCCS EGFR/HER2 site-specific exceptions.
- Ручное решение Юлии нужно только по этим пяти неоднозначным вопросам. Liverpool остаётся внешним BLOCKED вопросом, а не запросом на редакционное решение.

## Каталог до → после

| Метрика | До | После |
|---|---:|---:|
| Canonical records | 315 | 316 |
| Public matchable | 154 | 155 |
| Treatment trials | 150 | 151 |
| Other treatment access | 4 | 4 |
| Sources | 157 | 158 |

## Технический результат

- Среда: **PASS** — `/workspace/scratch/55af69f9810e`, Python 3.12.14, git 2.51.1.
- Execution gate init/check: **PASS**; accounting PASS не трактуется как клиническая полнота.
- Catalog sanitation/schema/source inventory/semantic dedupe/matcher build and parity/static build/production sync/evidence keys/trial links: **PASS**. Trial link check: 173 OK, 3 uncertain, 0 dead.
- `node scripts/test_matcher_catalog_loading.js`: **PASS** — ранний поиск, delayed load USA/Japan и отказ загрузки не дают ложный ноль; delayed results USA 100, Japan 12.
- `node scripts/test_matcher_logic.js`: **PASS**, 155 trials.
- Full fresh review gate: ожидаемо **INCOMPLETE — 5/155 reviewed, 150 pending**.
- Публикация: data/audit commit `20b94381559c8734d312bb4ff0ab88ffa18a4cd3`; repaired remote-main commit `9aceb4e152e743a6f7c077c3aa916511bba50da1`.
- Final GitHub Actions: full catalog integrity **PASS**; build/deploy **PASS**, workflow https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/41997222111.
- Production readback: live `index.html`, `matcher.js` и `trials.json` побайтно совпадают с локальной сборкой; HTML содержит `trials.json?v=6c8e53bee8ab5479` и `matcher.js?v=clinical-audit-20261103-owner-rules-r1`.
- Live matcher: **USA PASS — 100**, **Japan PASS — 12** при Dog / Cancer — any type / diagnosis certainty I don't know / пустых age, weight и ZIP / всех выбранных treatment options / Any approach.

## Даты проверки источников

- Previous inventory: 157 источников; у 134 `last_checked=2026-11-04`.
- New inventory: 158 источников; у 135 `last_checked=2026-11-05` (134 фактически посещённых прежних + новый Liverpool).
- У 23 exact restriction-only источников прежняя дата сохранена: новая успешная дата им не приписана.
- Local source inventory: **PASS**, 158, SHA-256 `6db295e3f36e7d60ef43152bc0dea9d53f20b73bcb7c15c2297f444618a41741`.
- Remote-main readback repaired inventory: **PASS**, тот же SHA-256.

**Итог обработки очереди:** PASS — 158/158 источников и 12/12 регионов, executor unfinished 0, доступной несделанной работы не осталось.

**Итог достаточности доказательств:** INCOMPLETE — один источник полностью reconciled; 157 источников имеют документированные внешние gaps, дополнительно остаются пять неоднозначных owner questions.

## Подробные материалы

- `receipt-final.json` — per-source receipt.
- `execution-review.json` и `execution-validation.json` — индивидуальные source/issue/lead decisions и gate result.
- `gap-review.json` — причины каждого partial/unreachable.
- `deadline-review.json` — ежедневные решения по срокам набора для 316 canonical records.
- `completed-clinical-reviews.json` — честный список 5 полных сегодняшних rereads.
- `production-readback.json`, `live-search-USA.json`, `live-search-Japan.json` — deploy/assets/live-search evidence.
- `final-postreadback-validation.log` — финальные команды и валидаторы.
- `retrieved-evidence.tar.xz` и `evidence-archive-sha256.txt` — архив фактически прочитанных документов и checksum.
