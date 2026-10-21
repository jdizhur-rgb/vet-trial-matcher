**21 октября 2026, 03:00:35–04:14:23, America/New_York**
**Режим: DAILY GLOBAL WORK AUDIT**
**Итог: INCOMPLETE. NEW: 0 исследований; UPDATE: 1 запись. Изменения опубликованы, production проверен.**

**Новые исследования:** 0 добавлено в активный матчинг. У Midwestern найдено приглашение с бесплатной химиотерапией для собак, но препарат и полный протокол не названы. Это сохранено как кандидат для проверки, без новой активной записи.

**Что исправлено:** у эдинбургского исследования tigilanol tiglate общий европейский список заменён [официальным описанием исследования](https://vet.ed.ac.uk/news/latest-news/2024/drug-trial-studies-plant-based-oral-cancer-therapy-dogs). Критерии, статус и прежняя дата клинической проверки сохранены. У CSU текущая пагинация сошлась: 37/37 объектов; прежнее расхождение счётчика устранено на стороне источника.

**Закрыто или скрыто:** 0. Отсутствие на странице не использовано как доказательство закрытия.

**Новые источники: 10**, все добавлены для наблюдения, без автоматического включения исследований:

| Страна | Источники |
|---|---|
| США | Midwestern University; TheraJan |
| Испания | Aúna; Complutense University veterinary hospital |
| Бразилия | USP / FAPESP — ONVEX |
| Япония | VMDP; лаборатория Mizuno, Yamaguchi; лаборатория Maeda, University of Tokyo |
| Австралия | The Kids Research Institute; University of Adelaide — FiDo |

**Поиск и охват:** обработка очереди — **132/133 источника, 12/12 регионов; незавершённых или неподтверждённых действий исполнителя: 1**. Фактические визиты выполнены для **116/133** источников; 17 не посещены из-за прежних ограничений и не получили новых дат. Единственное неподтверждённое действие — определение допустимости Cambridge alias, без повторения запрещённого маршрута.

Выполнены оба мировых прохода: текущие/недатированные возможности и свежие сигналы за 14–21 октября. Сохранены 86 запросов, 1 174 поисковых ответа и 898 уникальных URL. Использованы английский и местные языки, включая японский, китайский, испанский, португальский, французский и арабский. Выполнены 62 запланированных чтения официальных fallback; ещё 19 маршрутов отмечены как ограниченные. Всего сохранены 330 native-запросов, включая 27 разрешённых transient-повторов, и 44 Web-чтения. Невыполненных обязательных same-URL Web-восстановлений не осталось.

**Что осталось нерешённым:**

| Достаточность evidence | Источников |
|---|---:|
| fully reconciled | 57 |
| partial | 56 |
| unreachable | 3 |
| not checked | 17 |

Из 76 пробелов 75 классифицированы как внешние, 1 — `not_established` по обработке исполнителем. Причины: недостающие сведения о протоколах — 33; ограничения/недоступность источника — 19; исследовательские или навигационные страницы вместо trial roster — 16; неподтверждённая свежесть — 6; неустановленный roster — 2. Три недоступных источника: Anivive, Oklahoma State и Veterinary Oncology Services; разрешённые native/Web-маршруты испробованы.

Отдельные вопросы: у **Kv9** изменились формулировки критериев и исчезла таблица центров; это не подтверждает совместимость с химиотерапией или закрытие площадок. У **TheraJan** одобрение Manassas не подтверждает текущий набор; также сохранён конфликт адресов Stamford. Старые объявления, лабораторные, диагностические и поддерживающие исследования не добавлены как новые лечебные trials. Новых вероятных дублей canonical: 0. Ledger содержит 109 вопросов: 87 унаследованных и 22 новых/уточнённых.

Полная независимая клиническая перепроверка остаётся **INCOMPLETE: 32 записи исходного остатка** — 28 с ограниченным primary-маршрутом и 4 с недостающими опубликованными сведениями. Сегодня новых полных клинических заключений: 0. Ранее выполненные проверки не выданы за сегодняшние. Ручные действия Юли сейчас не требуются.

**Каталог до → после:**

| Показатель | До | После |
|---|---:|---:|
| canonical | 311 | 311 |
| public matchable | 152 | 152 |
| treatment trials | 148 | 148 |
| other treatment access | 4 | 4 |
| sources | 123 | 133 |

**Технический результат:** среда PASS — Python 3.12.14, Git 2.51.1; обязательные команды реально выполнены. Schema, sanitation, semantic dedupe, matcher logic/selection, build, production-sync, source inventory и проверка evidence keys — PASS. Строгий audit receipt — **INCOMPLETE**, 76 пробелов; gap-review validator — **PASS**, завершение обработки **NOT VERIFIED**. Накопительный полный клинический gate: 120/152; строго за этот запуск — 0/152 новых полных проверок. Дополнительный legacy Streamlit smoke — NOT VERIFIED: модуль не установлен.

Loading regression — **PASS**. Живой поиск Dog / Cancer — any type — **USA PASS: 98; Japan PASS: 10**. Проверены неизвестная достоверность диагноза, пустые age/weight/ZIP, все шесть вариантов лечения и Any approach. Полные отображённые списки совпали с расчётом по текущему каталогу.

Commit публикации в main: [b5966992](https://github.com/jdizhur-rgb/vet-trial-matcher/commit/b596699282c7dd4323344d426838f17b69a01d21). [Deploy](https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/39566247681) — PASS. Живые HTML, JS и каталог побайтно совпали со сборкой. HTML использует новый каталог `9d048dea595a4a9d`; неизменённый JS сохраняет версию `target-scope-20261018`.

**Даты проверки источников:** previous — 14/17/18/19/20 октября; new — 21 октября только для 116 посещённых источников. У 17 непосещённых даты и результаты сохранены. Например, AVMA: `2026-10-20T03:14:39-04:00` → `2026-10-21T03:11:05-04:00`, результат остаётся partial. Local и remote-main readback — **PASS для всех 133 строк**; SHA-256 inventory: `e3aa53b2684504be25328a0bac85463429040f5fc79b949b08209a078f55c309`.

**Обработка очереди INCOMPLETE: 132/133, одно неподтверждённое действие. Достаточность доказательств INCOMPLETE: 57/133 полностью сверены. Техническая публикация и живой поиск PASS.**

Подробности: [receipt](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261021T030035-0400/receipt-final.json), [gap-review](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261021T030035-0400/gap-review.json), [поиск и primary-проверки](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261021T030035-0400/primary-lead-review.json), [все поисковые ответы](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261021T030035-0400/discovery-ledger.json), [клинический остаток](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261021T030035-0400/clinical-pending-review.json), [изменённые данные и hashes](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261021T030035-0400/change-manifest.json), [команды и validators](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261021T030035-0400/validator-summary.json), [даты local/remote](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261021T030035-0400/remote-main-readback.json), [production bytes](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261021T030035-0400/production-byte-readback.json), [живые USA/Japan](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261021T030035-0400/live-search-evidence.json).
