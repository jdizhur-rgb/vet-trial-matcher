# DAILY GLOBAL WORK AUDIT — 24 ноября 2026

**Итог: INCOMPLETE по строгой клинической полноте; подтверждённые изменения опубликованы и production проверен.** Accounting gate прошёл, но это не означает полного сегодняшнего roster/status/five-fact подтверждения всех источников.

## 1. Запуск и восстановление remote-main

- Run ID: `daily-20261124T030358-0500`; плановый запуск, deadline 06:00 America/New_York.
- Фактически выполнено: `pwd` → `/workspace/scratch/713cddbf2188`; Python 3.12.14; git 2.56.1.
- До внешних запросов обнаружена повреждённая `data/source_inventory.json` в remote-main: JSON обрывался на byte 393216. Восстановлен последний валидный blob, проверены 168 source identities, repair опубликован коммитом `5d3423052f29e4d52ac2d14d8047897d3731fa2c`. После этого scheduled gate init прошёл; только затем начались внешние запросы.

## 2. Основной обход источников и протоколов

- 168/168 источников получили индивидуальные текущие решения; 303 native route attempts дали 251 transport error и 52 сохранённых exact restrictions. Разрешённый proxy fallback дал 234 успешных ответа, 10 HTTP errors, 7 thin/JS shells; 52 exact restrictions не обходились.
- Читаемый текущий материал получен для 140/168 источников. Ни один источник не доказал исчерпывающий текущий roster по строгому стандарту.
- Для замороженных 153 публичных протоколов проверены 177 маршрутов: 130 success, 8 thin/JS shell, 1 HTTP error, 38 exact restrictions. Читаемый текущий материал получен для 114/153.
- Source-level links и web leads разобраны индивидуально; знакомый домен не считался дублем без exact canonical comparison.
- Oncology care/services directories не проверялись и не изменялись. Клинические trial pages BluePearl и Ethos вошли в обход; сохранённые точные ограничения не обходились. VCA в текущем inventory не дал отдельного лечебного protocol-level кандидата.

## 3. Global discovery

- Выполнены 60 реальных поисков: 48 current/undated и 12 за последние 7 дней, отдельно по 12 регионам и языкам; 64 выбранных URL получили индивидуальные dispositions.
- Подтверждены два новых лечебных протокола:
  1. `ch-zurich-heart-base-sbrt-monitoring-2026` — собаки с опухолями основания сердца/хемодектомой; пять фракций SBRT и кардиомониторинг. Исследование покрывает кардиологические обследования; стоимость RT и staging не опубликована.
  2. `tufts-cotc034-osa-funded-amputation-2026` — собаки ≥25 кг с неметастатической appendicular osteosarcoma; исследование оплачивает ампутацию и плановый follow-up, но не предоставляет химиотерапию или экспериментальный противоопухолевый препарат.
- Обновлён canonical URL `ch-zurich-oral-vinorelbine-phase1-2026` по текущей официальной странице Zürich; five-fact review и исходные evidence dates сохранены.
- UFPel electrochemotherapy/calcium-electroporation project оставлен unresolved: действующий проект подтверждён, но публичного owner enrollment route и условий оплаты нет.
- UK-VCSR «Novel immunotherapy for canine lymphoma» отклонён: страница прямо помечена как AI-generated demo, не реальное исследование.
- Zürich PET-CT sarcoma и hormone-monitoring after RT отклонены как diagnostic/observational; Kansas probiotic lymphoma — supportive, не отдельное funded anticancer treatment; Cornell SINE OSA остаётся blocked из-за current 404.

## 4. Клиническая и независимая проверка

- Source-derived matcher cases есть для 155/155 публичных записей; production gate `SOURCE_DERIVED_SELECTION_OK` прошёл.
- Два новых протокола получили полную сегодняшнюю независимую protocol-level проверку и отдельные positive/contradiction/unknown cases. Диагностический `--reviewed-since` gate честно показал 2/155 same-day и 153 без повторной сегодняшней независимой рецензии; сегодняшние route/content решения для них не переименованы в full clinical rereview.
- 63 унаследованных issue получили свежие индивидуальные current decisions. Resolved: 0; remaining: 63; state `BLOCKED`; доступных незавершённых permitted steps не осталось.

## 5. Сроки набора

- Проверены все 323 frozen canonical IDs независимо от глубины reread. Сохранённые recruitment deadlines были у 43 записей.
- Три даты пересечены, но все три записи уже inactive/nonmatching: `ucd-urinary-stent`, `ncsu-canine-ucc-il12`, `penn-osa-carinkt`.
- Active deadlines crossed: 0; подтверждённых extensions: 0; изменений matching из-за сроков: 0.

## 6. Data/technical изменения и тесты

- Добавлены 2 canonical/public trials, обновлён 1 официальный URL, добавлены адресные aliases для Tufts и Zürich. Итог: 325 canonical records; 155 public opportunities = 152 treatment + 3 access.
- `source_inventory.json` компактно нормализован без потери 168 identities, master/fallback URLs, exact restrictions, route outcomes, timestamps и fingerprints; это устраняет риск повторной публикационной обрезки большого blob.
- PASS: matcher data build, static site build, address preflight 0 missing, sanitation, source inventory, evidence-key scan, `test_matcher_selection.js`, `test_matcher_selection.py`, `test_matcher_protocol_sources.js`, `test_matcher_catalog_loading.js`, `test_matcher_logic.js`, `validate_production_sync.py`, `git diff --check`.
- Preflight: PASS_WITH_INCONCLUSIVE только из-за отсутствующего локального `streamlit`; блокирующих ошибок нет.

## 7. Validators и честный остаток

- Strict receipt: **INCOMPLETE**, errors 0, coverage gaps 168. Причины: roster unestablished 140; source unavailable/exactly restricted 28.
- Gap validator: **PASS** по структуре и индивидуальным решениям; 168 rows, все сохранены как внешние evidence gaps. Это не превращает клиническую полноту в PASS.
- Accounting gate: **PASS**; sources sufficient 0/168, issues before 63, resolved 0, remaining 63, available_remaining пуст, clinical reconciliation INCOMPLETE, discovery INCOMPLETE.
- Причина окончания: `completed_available_work`. Разрешённые текущие маршруты, finite link/lead queue, discovery matrix, deadline check, сборка, тесты, публикация и readback завершены; остались непубликуемые факты, exact restrictions и будущие signal-based rechecks.

## 8. Публикация и production readback

- Data commit в `main`: `e9b07c55f9c62826726f55065e815318e648fc78`. Повторный `git fetch` и full-tree diff подтвердили точное совпадение remote-main с протестированным локальным пакетом.
- Production `trials.json`: 411288 bytes, SHA-256 `3a1d891faa92b416d635f1240d12a16c6bfa2ff8dad90d096aef29f0368ccd11`, точное совпадение с локальной сборкой; 155 records; оба новых IDs присутствуют.
- Живая форма отрисовала карточку Tufts COTC034 с funded amputation/follow-up и карточку Zürich heart-base SBRT с five-fraction treatment, cardiac-monitoring funding и текущими адресами.
- GitHub combined status на момент readback не публиковал отдельных status checks; production byte/UI readback — PASS.

Никакого outreach не выполнялось. Пользовательский текст, статьи, UI/CSS/navigation и спорные медицинские решения не менялись.
