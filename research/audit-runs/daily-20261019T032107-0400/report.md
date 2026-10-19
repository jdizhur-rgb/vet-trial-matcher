19 октября 2026, 03:21–04:20 EDT, America/New_York. **Режим: DAILY GLOBAL WORK AUDIT.** NEW — 0, UPDATE — 1. Подтверждённое исправление опубликовано; deploy и production — PASS. Общий итог — **INCOMPLETE**.

**Новые исследования — 0.**

**Что исправлено — 1.** Исправлен ошибочно активный статус Penn/Vetigenics VGS-002: полностью собачье anti-PD-1 при уротелиальном раке. Сегодня установлено точное соответствие существующей записи AVMA VCT23005729 со статусом Completed и протоколу спонсора, у которого Ethos и BARC обозначены Closed. Это не новый переход статуса AVMA, а завершённое сопоставление идентичности. [Официальный список спонсора](https://vetigenics.com/technology-pipeline/pipeline-and-clinical-trials/). genui{"citation":{"ref":"turn939view0"}}

**Закрыто или скрыто — 1:** VGS-002 исключён из поиска. Страница VSH North County по-прежнему показывает OPEN; противоречие сохранено, прежние клинические и финансовые даты не обновлялись. Остальные прежние скрытия, включая три UTSW и шесть европейских, сохранены.

**Новые источники — 1:** официальный pipeline/clinical-trials Vetigenics. Все исходные 119 источников сохранены; теперь их 120.

**Поиск и охват.** Обработка очереди: **119/120 источников, 12/12 регионов; недоделанная работа исполнителя по обходу — 1 действие**. Фактические визиты — 105/120; 15 источников не открывались из-за сохранённых ограничений. Из 80 записанных fallback-маршрутов: 48 имеют подтверждённую попытку, 15 ограничены, 16 не требовались при достаточном master, 1 — NOT VERIFIED.

Выполнены оба мировых прохода: текущие/недатированные возможности и свежие сигналы за **12–19 октября**, всего 85 запросов. Использованы английский и местные языки, включая французский, немецкий, испанский, португальский, японский, китайский, корейский, хинди, тайский и арабский. Шумная выдача и слабая региональная индексация не позволяют утверждать отсутствие других исследований.

**Что осталось нерешённым.**

| Результат источника | Число |
|---|---:|
| fully reconciled | 56 |
| partial | 47 |
| unreachable | 2 |
| not checked — сохранённые ограничения | 15 |

Из 64 недостаточно подтверждённых источников у 63 зафиксированы внешние пробелы: доступ, свежесть, текущий набор или отдельные сведения о протоколах. Справочники и новости отдельно квалифицированы как discovery, от них не требовался полный recruiting roster.

Отдельная недоделка исполнителя: Cambridge /node/2971 — NOT VERIFIED после отказа для смешанного запроса и 403 master. Маршрут не повторялся; отклонённый ответ не использован. Поэтому **вся очередь не объявлена завершённой**.

Полная свежая проверка клинических условий с отсечкой 16 октября: **121/154, остаётся 33 записи**. Сегодня новых полных клинических перепроверок — 0; закрытие VGS-002 не выдано за такую проверку. В discovery остаются 7 URL-сигналов, объединённых в 6 вопросов; 340 URL отклонены по предмету проверки, 38 повторных сигналов сопоставлены. Вероятных дублей публичного лечебного каталога — 0. Новых ручных действий от тебя не требуется; прежние нерешённые предложения сохранены.

**Каталог до → после.**

| Показатель | До → после |
|---|---:|
| Canonical | 311 → 311 |
| Public matchable | 155 → 154 |
| Treatment trials | 151 → 150 |
| Other treatment access | 4 → 4 |
| Sources | 119 → 120 |

**Технический результат.** Среда — PASS: Python 3.12.14, Git 2.51.1, Node 24.19.0. Schema, sanitation, semantic dedupe, source inventory, чистая сборка, matcher logic, selection/parity и production sync — PASS. Loading regression — PASS: ранний поиск, задержанная загрузка USA/Japan и отказ загрузки не дают ложного нуля. Строгий receipt — INCOMPLETE, структурных ошибок 0; gap-review — PASS. Необязательный Streamlit-тест — NOT VERIFIED: модуль не установлен.

После успешной первой сборки повторная сборка в рабочем каталоге дала ошибку согласованности страниц. Две сборки тех же исходников в отдельном чистом каталоге и оба deploy прошли; код сайта, UI и validators не менялись ради прохождения проверки.

Клиническая публикация: [99d76c53](https://github.com/jdizhur-rgb/vet-trial-matcher/commit/99d76c53051bda21c88da3bd46dd46caff250a39). Данные и итоговые receipts в main: [e28fb3c3](https://github.com/jdizhur-rgb/vet-trial-matcher/commit/e28fb3c3a49e5b9f2373d0ef5648db631e851c1b). [Deploy](https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/39221415576) — success.

Live HTML, JS и каталог побайтно совпали со сборкой. В HTML новая версия каталога — 8f3a5cd9d77775cb; script — target-scope-20261018, он не менялся. Реальный поиск Dog / Cancer — any type, diagnosis I don't know, пустые age/weight/ZIP, все лечения, Any approach: **USA 100, Japan 10 — PASS**, включая весь состав карточек.

**Даты проверки источников:** у 104 посещённых прежних источников 18 октября → фактические timestamps 19 октября; у одного нового — первая проверка. У 15 непосещённых даты и сохранённый last_result не изменены. Local/remote-main readback — PASS на e28fb3c3; SHA-256 inventory: bde5182cbf8d0b41d0a999c72095db5df559a69a64e610a8e6be67d622427546.

**Итог обработки очереди — INCOMPLETE: 1 действие NOT VERIFIED. Достаточность доказательств — INCOMPLETE: внешние пробелы и 33 клинические перепроверки остаются открытыми.**

[report.md](sandbox:/workspace/scratch/7a43f0b7d905/vet-trial-audit-20261019/research/audit-runs/daily-20261019T032107-0400/report.md) · [Receipts, evidence и hashes](https://github.com/jdizhur-rgb/vet-trial-matcher/tree/main/research/audit-runs/daily-20261019T032107-0400) · [Пробелы](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261019T032107-0400/gap-review.json) · [Команды и проверки](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261019T032107-0400/validators.json) · [Live-поиск](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261019T032107-0400/live-search-evidence-final.json) · [Даты и SHA](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261019T032107-0400/remote-main-readback.json)
