# DAILY GLOBAL WORK AUDIT — 10 ноября 2026

**Фактическое время:** клиническая обработка 03:02:37–03:36:59; публикация и remote readback завершены в 03:47:39 America/New_York  
**Режим:** DAILY GLOBAL WORK AUDIT  
**Run ID:** `daily-20261110T030237-0500`  
**Итог:** **NO CHANGE / INCOMPLETE**. Доступная обязательная работа завершена; полное клиническое подтверждение ограничено внешними пробелами публикации. Аудит и обновлённые даты источников опубликованы в `main`. Канонический каталог и production payload не изменялись.

## Новые исследования

**0 подтверждённых новых исследований.**

Два сигнала оставлены unresolved и не добавлены в каталог:

- FCV-UNLP, Аргентина: лечебное исследование актинического кератоза / плоскоклеточного рака кожи in situ у собак и кошек, с заявленным бесплатным обследованием и лечением. Найдена только вторичная публикация VetMarket; актуальный официальный protocol-level документ или официальный набор не установлен.
- UPM/NUS: найден меморандум 2023 года, но не найден актуальный официальный лечебный протокол с набором владельческих животных.

## Что исправлено

Клинических изменений в каталоге: **0**.

Технически:

- обновлены `source_inventory`, `audit_source_coverage`, `audit_state` и durable execution queue по фактическому сегодняшнему выполнению;
- сохранены индивидуальные решения по 161 источнику, 80 прежним вопросам, 24 discovery-проверкам и 8 разобранным leads;
- удалены найденные в загруженном HTML следы Google API keys; финальный `check_evidence_keys.py` — PASS;
- крупные текстовые извлечения ограничены с явной отметкой, при этом URL, timestamps, fingerprints, SHA и paired JSON evidence сохранены.

## Закрыто или скрыто

**0 записей закрыто или скрыто сегодня.**

AVMA сегодня перевёл два Penn Vet протокола из Recruiting в Suspended:

- `penn-osa-carinkt` — CAR-iNKT для метастатической остеосаркомы, VCT24005853;
- `penn-osa-car-inkt-newly-diagnosed` — CAR-iNKT для впервые диагностированной остеосаркомы, VCT26005954.

Обе записи уже были недоступны для matching до этого запуска, поэтому новое изменение каталога не потребовалось.

**Новые источники:** 0.

## Сроки набора

Проверено 320 канонических записей:

- 18 — опубликованная дата набора сегодня или в будущем;
- 4 — дата уже прошла, и запись уже не участвует в matching;
- 298 — в канонической записи нет опубликованного recruitment cutoff.

Активных записей с уже прошедшим опубликованным сроком не найдено. FAM010 по текущему официальному материалу остаётся в состоянии **ENROLLING SOON**, без подтверждённой даты открытия следующей когорты.

## Поиск и охват

**Обработка очереди: 161/161 источников, 12/12 регионов; недоделанная доступная работа исполнителя: 0.**

- master routes открыты для всех 161 источника;
- выполнено 120 официальных fallback-запросов там, где master был недостаточен;
- использованы 12 Web-проверок того же официального URL или официального fallback при недостаточном shell-ответе;
- выполнены два discovery-прохода: current/undated и свежие сигналы за 7 дней;
- проведены отдельные региональные запросы на английском, французском, немецком, итальянском, испанском, португальском, японском, китайском, корейском, арабском, иврите, турецком, малайском и тайском языках.

Во время первого этапа 24 URL с ранее сохранёнными exact access restrictions были ошибочно запрошены один раз из-за неверного ключа lookup. Повторов не было, результаты не использованы как evidence, ограничения не обходились; отклонение сохранено отдельно. После исправления restricted issue URLs не запрашивались.

## Что осталось нерешённым

| Результат источника | Число | Смысл |
|---|---:|---|
| Fully reconciled | 3 | Сегодняшний официальный roster/primary evidence достаточен по строгому receipt |
| Partial | 158 | Обработка завершена, но полный текущий roster или protocol-level факт не опубликован либо недоступен разрешёнными маршрутами |
| Unreachable | 0 | Источник целиком не классифицирован как недоступный |
| Not checked | 0 | Непосещённых обязательных источников нет |

Внешние причины: **158 source-specific evidence gaps**. Durable issues: **80** — 72 `BLOCKED`, 8 `OWNER_DECISION`. Доступных незавершённых шагов в execution gate: **0**. Новых unresolved discovery leads: **2**. Подтверждённых дублей или rejected clinical additions сегодня нет.

Историческая independent-selection матрица покрывает **141/153** публичных matcher-записей; **12** остаются pending из-за сохранённых exact access restrictions. Обычный regression-тест этой матрицы прошёл. Отдельный жёсткий fresh gate с порогом начала сегодняшнего запуска честно показал **0/153** полностью перечитанных сегодня individual protocols и завершился INCOMPLETE. Это не означает, что 153 протокола не проверялись по сегодняшним roster/master routes; это означает, что сегодня не выполнялся новый полный независимый reread каждого individual protocol. Неизменившиеся протоколы остаются на действующем цикле углублённой перепроверки, а сроки набора проверены отдельно сегодня.

Ручное действие Юли сейчас не требуется для подтверждённых data/technical изменений. Восемь `OWNER_DECISION` сохранены как спорные клинические/редакционные вопросы и не закрыты автоматически.

## Каталог до → после

| Метрика | До | После |
|---|---:|---:|
| Canonical records | 320 | 320 |
| Public matcher records | 153 | 153 |
| Явно `available_for_matching=true` | 151 | 151 |
| Treatment trials в matcher build | 149 | 149 |
| Other treatment access | 4 | 4 |
| Sources | 161 | 161 |

## Технический результат

- Среда: **PASS** — Python 3.12.14, git 2.52.0.
- `validate_catalog_sanitation.py`: PASS — 320 записей, новых partial records нет.
- `validate_source_inventory.py`: PASS — 161 источник.
- `check_evidence_keys.py`: PASS.
- Matcher build: PASS — 153 записи, treatment 149, access 4.
- Historical independent-selection regression: PASS — 141/153 reviewed, 12 pending, 1082 retained cases.
- Fresh full-protocol gate: **INCOMPLETE — 0/153 reread after run start**.
- `test_matcher_selection.js`, `test_matcher_selection.py`, `test_matcher_catalog_loading.js`, `test_matcher_logic.js`: PASS.
- `build_static_site.py`: PASS.
- `validate_production_sync.py`: PASS.
- `audit_preflight.py`: PASS_WITH_INCONCLUSIVE — обязательные проверки прошли; необязательный Streamlit smoke-test не запускался, потому что модуль Streamlit отсутствует.
- Strict receipt: **INCOMPLETE — 3/161 sufficient, 158 gaps**.
- Gap review validator: PASS.
- Audit execution gate: PASS; clinical reconciliation INCOMPLETE; discovery accounting INCOMPLETE по двум неподтверждённым leads.
- Audit data commit: `8169ec67f4223dbb0e05d8ddf12828585f92fe89`; remote-main readback PASS, tree SHA `9833b576b9cc34cf0ec555e10d37c9ad0635acd0` совпал с локальным.
- Новый deploy не требовался: canonical и собранные production assets не изменились.
- Production readback: PASS. Live HTML, matcher JS и catalog JSON совпадают с локальной сборкой.
- Loading regression: PASS — ранний поиск, задержанная загрузка USA/Japan и ошибка загрузки не дают ложный ноль.
- Live search по обязательному сценарию: USA **96/96 PASS**, Japan **14/14 PASS**. Старая уже открытая вкладка показывала 97 USA из-за stale state; свежая вкладка загрузила текущий каталог и показала 96.

### Даты проверки источников

До запуска: 138 источников имели дату 2026-11-09, 7 — 2026-11-08, 16 — 2026-11-06. После запуска 135 источников получили фактическую дату 2026-11-10; даты 26 exact-restricted источников сохранены и не обновлены на основании запрещённого или недостаточного маршрута. Local readback PASS; remote-main readback PASS.

**Итог обработки очереди:** доступная очередь завершена, `stop_reason=completed_available_work`.  
**Итог достаточности evidence:** **INCOMPLETE** — строгая достаточность подтверждена для 3/161 источников; 158 пробелов документированы как внешние, без подмены на успешную проверку.

## Артефакты

- [receipt-final.json](sandbox:/workspace/scratch/f2b8764c4267/vet-trial-matcher/research/audit-runs/daily-20261110T030237-0500/receipt-final.json)
- [execution-review.json](sandbox:/workspace/scratch/f2b8764c4267/vet-trial-matcher/research/audit-runs/daily-20261110T030237-0500/execution-review.json)
- [gap-review.json](sandbox:/workspace/scratch/f2b8764c4267/vet-trial-matcher/research/audit-runs/daily-20261110T030237-0500/gap-review.json)
- [deadline-review.json](sandbox:/workspace/scratch/f2b8764c4267/vet-trial-matcher/research/audit-runs/daily-20261110T030237-0500/deadline-review.json)
- [discovery-evidence.json](sandbox:/workspace/scratch/f2b8764c4267/vet-trial-matcher/research/audit-runs/daily-20261110T030237-0500/discovery-evidence.json)
- [avma-delta.json](sandbox:/workspace/scratch/f2b8764c4267/vet-trial-matcher/research/audit-runs/daily-20261110T030237-0500/avma-delta.json)
- [access-restriction-deviations.json](sandbox:/workspace/scratch/f2b8764c4267/vet-trial-matcher/research/audit-runs/daily-20261110T030237-0500/access-restriction-deviations.json)
- [validation-results.json](sandbox:/workspace/scratch/f2b8764c4267/vet-trial-matcher/research/audit-runs/daily-20261110T030237-0500/validation-results.json)
- [production-readback.json](sandbox:/workspace/scratch/f2b8764c4267/vet-trial-matcher/research/audit-runs/daily-20261110T030237-0500/production-readback.json)
- [git-readback.json](sandbox:/workspace/scratch/f2b8764c4267/vet-trial-matcher/research/audit-runs/daily-20261110T030237-0500/git-readback.json)
- [checkpoint-final.json](sandbox:/workspace/scratch/f2b8764c4267/vet-trial-matcher/research/audit-runs/daily-20261110T030237-0500/checkpoint-final.json)

Автоматическая проверка отклонила общий `validate_trial_links.py`, потому что он мог обратиться к сохранённым запрещённым NCSU routes. Я не обходил этот запрет. Безопасные source, schema, build, matcher, execution, gap и production-sync проверки выполнены; общий link validator отмечен как NOT RUN / REJECTED.
