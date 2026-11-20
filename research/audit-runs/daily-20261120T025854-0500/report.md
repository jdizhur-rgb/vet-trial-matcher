# DAILY GLOBAL WORK AUDIT — daily-20261120T025854-0500

**Итог аудита: INCOMPLETE.** Учёт исполнения и публикация прошли; строгая клиническая полнота не доказана для всех источников из-за 167 документированных внешних пробелов.

## Параметры запуска

- Часовой пояс: America/New_York.
- Начало: 2026-11-20T02:58:54.490431-05:00.
- Окончание: 2026-11-20T03:34:22.457769-05:00.
- Режим: scheduled; предел 06:00 ET не достигнут.
- Причина остановки: `completed_available_work` — все доступные разрешённые маршруты, текущие протоколы, региональные поиски, сроки и lead decisions обработаны; оставшиеся факты зависят от новых публикаций или сохранённых точечных ограничений доступа.

## Текущие источники и протоколы

- 168/168 source decisions; 143 источника реально открыты/запрошены, 25 обработаны по точечным сохранённым access restrictions без обхода.
- Source requests: 302 (233 success, 52 exact restriction skips, 10 HTTP errors, 7 thin/JS).
- Protocol requests: 176 (127 success, 38 exact restriction skips, 9 thin/JS, 1 transport error, 1 HTTP error).
- AVMA: 859 уникальных записей, 446 oncology, 58 recruiting oncology; изменений состава против 2026-11-19 нет.
- Strict receipt: INCOMPLETE, потому что complete current roster доказан только для 1/168 источников.
- Gap validator: PASS; 167 внешних пробелов — roster_unestablished 131, discovery_source_not_trial_roster 11, source_unavailable 25. Доступных невыполненных executor steps нет.

## Global discovery

- Выполнено 24 отдельных запроса: по два прохода для 12 регионов (текущая/недатированная выдача и последние 7 дней), с отдельными странами и языками и углублением слабых результатов.
- Добавлен один новый канонический лечебный протокол: `penn-flash-metastatic-osa-gilvetmab-2026`.
- Официальный протокол Penn: https://www.vet.upenn.edu/clinical-trial/proton-flash-rt-in-canine-metastatic-osteosarcoma/
- Суть: собаки после ампутации по поводу подтверждённой аппендикулярной остеосаркомы, с измеримым метастазом в лёгком, получают одну дозу proton FLASH RT на лёгочный очаг и три внутривенных инфузии gilvetmab; наблюдение 48 недель. Скрининг и ампутацию оплачивает владелец, перечисленные post-enrollment процедуры и лечение покрывает исследование.
- CaniVax/CaniVive сохранён как `PENDING_EVIDENCE`: текущий британский сигнал есть, но нет индивидуального протокола, полного списка центров, критериев и стоимости; каноническая карточка не выдумана.
- Остальные лиды получили индивидуальные решения: WCVM staging — NOT_TREATMENT; UQ Enzistat, Peninsula STS и UFPel electroporation — PENDING_EVIDENCE; VCSR AI sample — не лечебный протокол.

## Сроки набора

- Проверены все 322 frozen canonical ID независимо от неизменности страниц.
- 43 записи имеют опубликованные даты; 3 даты уже прошли, и все три записи уже были нематчируемыми: `ucd-urinary-stent`, `ncsu-canine-ucc-il12`, `penn-osa-carinkt`.
- Перешедших срок при всё ещё активной выдаче: 0. Подтверждённых продлений: 0.

## Исправления и тесты

- Для Penn использованы существующие matcher-семантики `post_amputation`, `measurable_lung_metastases`, 21-дневные washout для chemotherapy и immunotherapy; добавлены независимые positive/negative selection cases.
- Catalog validation: 323 уникальных записи, 153 публичных/активных.
- Semantic dedupe: 0 вероятных дублей.
- Source inventory: PASS, 168 источников, digest `f6c7b28de899`.
- Matcher data/logic/selection/parity, source-derived selection, static build, production sync, sanitation и evidence-secret gate: PASS.
- Execution gate: PASS по учёту; 74/74 старых issue получили текущие индивидуальные решения и остаются BLOCKED (63 full_protocol, 11 independent_selection). Ни один не закрыт без новых доказательств.

## Публикация и production

- Клинические изменения опубликованы в `main`: `8ee08fdf22694b54a6c2cfe4099772b30bc9a22f`.
- Live `trials.json`: 153 записи, SHA-256 `5de4db11ac9ab7d78c39d926bcab7d7de5dadae4511064cb6d5064d625444edd`; новая Penn-карточка присутствует ровно один раз.
- Реальная browser-проверка matcher: Dog + Cancer — any type + все варианты лечения → США 96 карточек, Япония 14 карточек. Production readback: PASS.
- Outreach не выполнялся. Онкологические care/services directories не исследовались; clinical trial pages BluePearl/VCA/Ethos входили в проход.
