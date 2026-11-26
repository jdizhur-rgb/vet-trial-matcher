# DAILY GLOBAL WORK AUDIT — 26 ноября 2026

**Run ID:** `daily-20261126T025951-0500`  
**Окно:** 03:00:51–03:35:49 EST  
**Итог:** **NO CHANGE / INCOMPLETE**

## Что изменено

- Новых канонических исследований: **0**.
- Каталог остался **325** записей; публичный matcher — **155** записей (**152 treatment + 3 access**).
- Пользовательский текст, UI/CSS и навигация не менялись.
- В `main` опубликованы текущие evidence, индивидуальные source/issue/lead decisions, durable queue и audit state: commit `20949067a3b713197f98834894530a277510a83b`.

## Основной обход источников

- Обработаны **168/168** source identities.
- Выполнено **303** маршрутных решения: **250** реальных HTTP-ответов, **52** точных access restrictions соблюдены без запроса, **1** transport error.
- Среди HTTP-ответов: **239 × 200**, **6 × 404**, **2 × 525**, по одному **503**, **500** и **202**.
- Web fallback выполнен для **29** целей из **20** источников.
- Строго достаточный текущий roster доказан только для **4/168** источников: UK VCSR, MSU Oncology, OVC Oncology и Veterinary Cancer Care.
- Для **164** источников текущая полнота roster/status не доказана. Все доступные маршруты и reconciliation выполнены; остаток классифицирован как внешний blocker, а не как проверенная клиническая полнота.
- BluePearl, VCA и Ethos clinical-trial pages входили в обход. Oncology care/services directories не включались.

## Клиническая и независимая проверка

- Покрыты **155/155** публичных protocol records.
- Выполнено **172** protocol-route решения: **138** реальных HTTP-ответов и **34** точных access restrictions, соблюдённых без запроса.
- Нативно читаемый текущий официальный текст получен для **85** записей; Web fallback выполнен по **50** целям; для **69** записей нативного читаемого маршрута не было.
- Все **63** наследуемых durable issues получили сегодняшние индивидуальные решения. Результат: **63 BLOCKED**, **0** ложно закрытых, доступных несделанных шагов **0**.
- Fresh full independent-case gate: **0/155**, pending **155**. Сегодняшние route reads не дают достаточных самостоятельных positive/negative/unknown cases по каждой записи. Поэтому клинический результат остаётся **INCOMPLETE**, даже при PASS учёта.

## Global discovery

- Выполнено **68** отдельных поисков: **48** исходных запросов по всем **12** обязательным регионам и **20** углублений по странам/языкам со слабой выдачей.
- **CaniVax / CaniVive, UK:** официальная новость от 3 ноября 2026 сообщает о первом исследовании у собак с поздним метастатическим раком в нескольких британских центрах. Публично не найдены protocol ID, список центров, полная eligibility, funding и enrollment contact. Решение: **PENDING_EVIDENCE**, в каталог не добавлено.
- **OCRvet / SeineVet:** обнаружен исторический сигнал о monoclonal-antibody study в 13 центрах Франции, Польши и Португалии. Источник примерно двухлетний, текущий первичный recruitment status не подтверждён. Решение: **PENDING_EVIDENCE**, в каталог не добавлено.
- **OVC canine porphysome/PDT oral-tumor trial:** текущая официальная страница указывает **ON HOLD**. Решение: **CLOSED_CONFIRMED**, в matcher не добавлено.
- Ещё **14** protocol-level leads сопоставлены с точными существующими canonical IDs; знакомый домен не использовался как признак дубля.
- Всего принято **20** индивидуальных lead decisions. Новых исследований, удовлетворяющих protocol-level требованиям, нет.

## Сроки набора

- Проверены все **325** canonical IDs независимо от глубины перечитывания страниц.
- Явные даты есть у **43** записей.
- Пересечены **3** срока, но все три записи уже неактивны: `ucd-urinary-stent`, `ncsu-canine-ucc-il12`, `penn-osa-carinkt`.
- Активных записей с пересечённым сроком: **0**. Подтверждённых продлений: **0**. Для **282** записей текущая дата окончания публично не доказана.

## Ограничения доступа

- Загружены **103** сохранённых exact restrictions.
- В фактическом обходе применены **86** restricted-route решений: **86/86** `skipped_exact_restriction`, отклонений **0**.
- Ограничения не расширялись на учреждение целиком и не обходились.

## Валидация и тесты

- `audit_execution_gate.py check`: **PASS** для учёта; clinical reconciliation и discovery — **INCOMPLETE**.
- Strict receipt validator: **INCOMPLETE**, ошибок структуры **0**, coverage gaps **164**.
- Gap validator: **PASS**, все **164** остатка — `external_blocker`, `EXTERNAL_GAPS_ONLY`.
- Source inventory validator: **PASS**, 168 sources, digest `8573ad3fe727`.
- Catalog validation: **PASS**, 325 records / 155 public.
- Build matcher data: **PASS**, 155 public / 152 treatment / 3 access.
- Matcher selection JS и Python parity: **PASS**, 18 600 disease checks.
- Обязательный delayed-loading regression: **PASS** — USA **97**, Japan **14**.
- Static build: **PASS**, 45 pages.
- Matcher logic, production sync, catalog sanitation и `git diff --check`: **PASS**.
- Audit gate tests: **29/29 PASS**.
- Preflight: **PASS_WITH_INCONCLUSIVE** только для отсутствующего в среде Python-модуля `streamlit`; остальные проверки прошли.

## Публикация и production readback

- `main` опубликован: `20949067a3b713197f98834894530a277510a83b`.
- GitHub Actions: Full catalog integrity audit — **success**; Check copied evidence keys — **success**; Build and deploy static site — **success**.
- Живой `https://vettrialfinder.com/matcher/` проверен в браузере после публикации.
- Рендерed search `Dog / Cancer — any type / USA / I don't know / all treatment options / Any approach`: **97** результатов.
- Такой же поиск для Japan: **14** результатов; первый результат — `Organoid-guided targeted therapy for canine and feline solid tumors`.
- Production readback: **PASS**.

## Причина завершения

`completed_available_work`: вся разрешённая и доступная работа этого запуска выполнена. Остались документированные внешние пробелы и недостаток свежих independent-case evidence; ожидание без новых доступных действий не продолжалось. Outreach не выполнялся.
