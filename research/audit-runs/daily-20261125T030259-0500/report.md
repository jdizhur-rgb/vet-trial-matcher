# DAILY GLOBAL WORK AUDIT — 25 ноября 2026

**Run ID:** `daily-20261125T030259-0500`  
**Режим:** scheduled, старт `2026-11-25 03:02:59 EST`, предел `06:00 EST`  
**Фактическое окончание доступной работы:** до предела; причина остановки `completed_available_work`  
**Итог:** **NO CHANGE / INCOMPLETE**. Gate учёта — **PASS**; клиническая сверка и global discovery — **INCOMPLETE**. Контроль соблюдения ограничений — **FAIL** из-за одной зафиксированной ошибки обхода, описанной ниже.

## Что изменено и опубликовано

- Новых canonical trials: **0**. В 24 текущих поисках не найден новый лечебный протокол, который можно было бы добавить с exact protocol-level подтверждением.
- Каталог: **325 → 325** canonical records; public matcher: **155 → 155**, из них **152 treatment** и **3 access**.
- Источники: **168 → 168**. Для каждого источника записана текущая попытка от 25 ноября, сохранены исходные даты старых evidence; сегодняшняя достаточность не наследовалась.
- Обновлены `data/source_inventory.json` и durable `data/audit_execution_queue.json`.
- Публичные статусы, sites, eligibility, funding, contacts и пользовательский текст не менялись в этом запуске: новых достаточных current-primary подтверждений не было.
- Remote `main` опубликован на commit `b21fe9c5281987be42c2ab92cf2b3c0ef56a6b06`.

## Основной обход и клиническая сверка

- Frozen source roster: **168/168** источников получили индивидуальное решение.
- Native source routes: **303** попытки — 251 transport error и 52 точных пропуска по сохранённым restrictions.
- Native protocol routes: **180** попыток — 142 transport error и 38 точных пропусков по restrictions; охвачены все **155** public trials.
- Strict receipt: **INCOMPLETE**, 168 roster gaps; `content_sufficient=0/168`, `processing_complete=168/168`.
- Gap review: **PASS**, все 168 пробелов классифицированы как `external_blocker`; это подтверждает учёт, но не клиническую полноту.
- Durable issues: **63 до → 63 после**. Все получили текущие индивидуальные решения; `available_remaining=[]`, все 63 остаются `BLOCKED` внешним или конфликтующим evidence.
- Отдельно сохранён конфликт COTC033: текущая страница Missouri пишет о наборе, а canonical record неактивен по прежнему protocol/status evidence. Автоматической реактивации не сделано; нужна exact multicenter/AVMA сверка.

## Global discovery

- Выполнено **24 отдельных запроса**: 12 регионов × discovery/status pass, со странами и локальными языками; слабые регионы проверялись локализованными формулировками.
- Разобрано **10 leads**. Девять exact-сопоставлены с существующими canonical IDs; COTC033 оставлен `PENDING_EVIDENCE` из-за конфликта статуса.
- Подтверждены как уже существующие, среди прочих: FAM-010, Penn FLASH+gilvetmab, Penn oral-SCC NIR, японский anti-PD-1 oral melanoma, Gamgee mRNA vaccine, ReachGlio, Zurich oral vinorelbine, BluePearl Paccal Vet и UNAM silver nanoparticle study.
- Вывод ограничен фактическим evidence: **новых квалифицируемых canonical protocols не найдено**, но exhaustive clinical completeness не заявляется.

## Сроки набора

- Проверены все **325** frozen IDs независимо от повторного deep-review графика.
- Записанных сроков: **43**; пересечённых: **3**, все уже inactive; active crossed deadlines: **0**; подтверждённых продлений: **0**.
- Для **282** записей нового current date evidence получить не удалось; прежние даты сохранены, новые не выдумывались.

## Тесты и validators

- PASS: repository hygiene, catalog validation, source inventory validation, full catalog audit, matcher data build, JS/Python selection parity, catalog loading, matcher logic после full build, production sync, static-site build, audit-execution regression и `git diff --check`.
- Full static build: 45 pages; matcher **155 total / 152 treatment / 3 access**; source-derived selection **155/155 pending=0**.
- Preflight: `PASS_WITH_INCONCLUSIVE`, потому что в среде нет пакета `streamlit`; остальные preflight checks прошли.
- Запрошенный путь `scripts/validate_protocol_selection_cases.py` в актуальном remote-main отсутствует; это не выдавалось за успешно выполненный validator.
- Execution gate: **PASS** только для accounting/evidence contract. Его собственные поля: clinical reconciliation **INCOMPLETE**, discovery **INCOMPLETE**.

## Ошибка исполнения

Во время Web master fallback один batch ошибочно включил **26 exact URLs**, ранее отмеченных `do_not_retry`. Ответы этого batch не были приняты как evidence, повторных запросов не было, полный список сохранён в `access-restriction-deviation.json`. Это не расширено до запрета учреждений, но сам факт попытки нарушает требование не обходить exact restrictions; поэтому compliance-результат этого запуска обозначен **FAIL**, а не скрыт за PASS gate.

## Публикация и production readback

- GitHub `main`: `b21fe9c5281987be42c2ab92cf2b3c0ef56a6b06`; независимый fetch подтвердил этот head.
- Production открыт после публикации по запросу dog / hemangiosarcoma / USA: отрисовано **10** возможностей.
- Карточка FAM-010 присутствует с University of Illinois и текущей формулировкой **“Enrollment is open”**; старой формулировки “Enrolling soon” в rendered page нет.
- Live-карточка сохраняет осторожное описание покрытия расходов: лечение и follow-up покрывает Familiar, travel оплачивает владелец, расхождение по screening costs предлагается уточнить у study team.

## Итоговый остаток

Доступная работа текущего запуска закончена до установленного предела. Остались 63 документированных внешних/конфликтных issue и 168 current-roster gaps; они не закрыты прошлым статусом или совпадением одной страницы. Outreach не выполнялся. Каталог не изменён, потому что ни один новый lead не получил достаточного exact protocol-level evidence.
