**23 октября 2026, 03:05:10–04:25:24, America/New_York.**
Режим: **DAILY GLOBAL WORK AUDIT**. Итог: **INCOMPLETE**. NEW: 0 активных исследований, 2 официальных источника. UPDATE: evidence, даты фактических посещений и техническая сводка. Изменения опубликованы; deploy и production — PASS.

**1. Новые исследования**

В активном подборе — **0**.

Новый кандидат для наблюдения: **FAM-010, Familiar Therapeutics / University of Illinois, Urbana, США** — собаки с гемангиосаркомой селезёнки после операции; доксорубицин, связанный с альбумином. Индивидуальная [официальная страница](https://familiartx.com/studies/fam-010), обновлённая 15 октября, говорит **ENROLLING SOON**; открытый приём пока не подтверждён. Спонсор оплачивает исследовательское обследование, лечение и последующее наблюдение; проезд оплачивает владелец. Покрытие предшествующей спленэктомии не установлено. Запись в подбор не добавлена.

**2. Что исправлено**

- Изменений лечебных записей canonical — **0**. Исправлена техническая сводка `audit_state`: у сегодняшнего run_id оставались счётчики и ссылки на receipt от 20 октября; теперь она соответствует фактическому receipt 23 октября.
- PetTrials Australia разобран полностью: **7/7** объявлений; VetTrials — **293/293** объектов, включая 102 онкологических записи разных статусов. Будущий набор, диагностические исследования и обновления вторичного реестра не превращены в новые доступные лечебные trials.
- Для Calusa/UConn уточнено: исследование ASO при лимфоме собак; бесплатность опубликована для конкретного пациента. Открытый набор, точный препарат и общие расходы всех участников не подтверждены.
- Сбой AVMA зафиксирован как неизвестный текущий roster: ошибки страниц/API и недостаточный Web-readback. Отсутствие полученных объектов не принято за ноль исследований или закрытие прежних записей.

**3. Закрыто или скрыто; новые источники**

Закрыто или скрыто — **0**. Предыдущие решения о скрытии сохранены.

Новые источники — **2**: [Familiar Therapeutics](https://familiartx.com/) — США; [CimCure](https://cimcure.com/news/) — Нидерланды. У CimCure подтверждены исторические ветеринарные исследования вакцины eVim; текущий набор собак/кошек и расходы владельца не опубликованы. Нынешние сообщения о человеческих trials отдельно квалифицированы.

**4. Поиск и охват**

**Обработка очереди: 142/143 источника, 12/12 регионов; незавершённая или неподтверждённая работа исполнителя: 1.** Фактические посещения — **125/143**. Для 18 непосещённых источников сохранены прежние ограничения доступа и даты; один из них, Cambridge, не признан завершённым.

Проверены разрешённые master/fallback и необходимые индивидуальные протоколы. Сохранены **329 shell-запросов** к источникам/протоколам, включая 22 transient-повтора, и **37 Web-чтений**; обязательных незавершённых same-URL Web-проверок после обычных транспортных ошибок — **0**. Явные запреты доступа не обходились.

Выполнены оба discovery-прохода: текущие/недатированные возможности и свежие сигналы **16–23 октября**. Всего **97 запросов, 1 047 результатов, 777 уникальных нормализованных URL**. Охвачены США, Канада, Великобритания, континентальная Европа, Латинская Америка/Карибы, Австралия/Новая Зеландия, Восточная, Южная и Юго-Восточная Азия, Ближний Восток, Северная Африка и Африка южнее Сахары. Использованы английский и местные языки, включая японский, китайский, корейский, французский, немецкий, испанский, португальский, хинди, тайский, малайский, индонезийский, вьетнамский, иврит, турецкий, арабский и африкаанс. Это выполненная поисковая матрица, а не доказательство отсутствия иных мировых исследований.

**5. Что осталось нерешённым**

| Достаточность evidence | Источников |
|---|---:|
| fully reconciled | 55 |
| partial | 67 |
| unreachable | 3 |
| not checked | 18 |

Строгий receipt: **INCOMPLETE**, 0 ошибок структуры, **88 пробелов**. Из них **87 — external_blocker**, **1 — not_established**, учтённый в незавершённой работе исполнителя. Cambridge: не установлено, допускается ли обращение к alias `/node/2971` после прежнего запрета; маршрут не использован для обхода ограничения.

Категории пробелов: вопросы конкретных протоколов — **42**; источник discovery не является roster trials — **16**; недоступность официальных маршрутов — **23**; roster не установлен — **2**; свежесть не подтверждена — **5**. Для каждой строки сохранены вопрос, URLs/evidence и следующий допустимый шаг. Справочники, новости и pipeline не объявлены недоступными лишь потому, что не публикуют полный recruiting roster.

Отдельный клинический остаток: полная независимая проверка подтверждена для **119/151** публичной записи; прежние **32** незакрытых вопроса сохранены. Сегодня новых полных клинических sign-off — **0**. Всего unresolved — **127**: 117 прежних и 10 новых; прежние сроки повторной проверки сохранены. Отсеян **521 поисковый URL** как нерелевантный, исключённый тип материала или ссылка на собственный сайт. Вероятных семантических дублей в лечебном каталоге — **0**.

**6. Каталог до → после**

| Показатель | До | После |
|---|---:|---:|
| Canonical | 311 | 311 |
| Public matchable | 151 | 151 |
| Treatment trials | 147 | 147 |
| Other treatment access | 4 | 4 |
| Sources | 141 | 143 |

**7. Технический результат**

Среда — **PASS**: реально выполнены `pwd`, `python --version` — Python 3.12.14, `git --version` — Git 2.51.1. Schema, sanitation, semantic dedupe, source validator, сборка, matcher logic/selection и production-sync — **PASS**. Loading regression — **PASS**, включая ранний поиск, задержанную загрузку USA/Japan и отказ загрузки. Gap-review validator — **PASS**; подтверждение полноты обработки — **NOT VERIFIED**. Полный клинический gate — **INCOMPLETE**, отдельно от технических тестов.

Опубликованное состояние данных main: [`9e0d12a77c1b604839830b3203b4754387e39db8`](https://github.com/jdizhur-rgb/vet-trial-matcher/commit/9e0d12a77c1b604839830b3203b4754387e39db8); исходный main — `b9a12fe7ec54557108c01a36b9edcc25e2d00c2b`. [Deploy](https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/39923765520) и две сопутствующие проверки GitHub — **PASS**. Production HTML/JS/catalog совпали со сборкой побайтно. В HTML подтверждён `matcher.js?v=clinical-gi-20261022`; JS и публичный каталог сегодня не менялись, их версии сохранены.

Реальный поиск после deploy — **USA 97/97, Japan 10/10: PASS**. Проверены Dog / Cancer — any type, diagnosis certainty I don't know, пустые age/weight/ZIP, все шесть вариантов лечения, Any approach. Сравнены полные отображённые наборы карточек, а не только числа или наличие JSON; ожидаемые результаты рассчитаны из текущего каталога.

**8. Даты проверки источников и итог**

Для **123** посещённых прежних источников даты изменены **22 → 23 октября**; для двух новых — **нет → 23 октября**. У **18** непосещённых даты и timestamps сохранены. Неуспешные попытки не получили успешный результат. Local/remote-main readback — **PASS** на `9e0d12a77c1b604839830b3203b4754387e39db8`, все 143 строки дат/результатов совпали. SHA-256 inventory: `2d7233088f52c32d3d357affab63247636058cf59029999c1ae68828bdbf3860`.

**Итог обработки очереди — INCOMPLETE: 142/143, одно неподтверждённое действие. Итог достаточности доказательств — INCOMPLETE: 88 пробелов источников; клинический остаток указан отдельно.**

Подробности: [receipt](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261023T030510-0400/receipt-final.json), [gap-review](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261023T030510-0400/gap-review.json), [поиск и языки](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261023T030510-0400/discovery-matrix.json), [квалификация результатов](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261023T030510-0400/discovery-ledger.json), [primary-проверки](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261023T030510-0400/primary-lead-review.json), [клинический остаток](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261023T030510-0400/clinical-pending-review.json), [изменения и hashes](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261023T030510-0400/change-manifest.json), [исправление сводки](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261023T030510-0400/state-summary-correction.json), [команды и validators](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261023T030510-0400/validator-summary.json), [финальные проверки](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261023T030510-0400/final-validation.json), [даты local/remote](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261023T030510-0400/remote-main-readback.json), [production bytes](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261023T030510-0400/production-byte-readback.json), [живые USA/Japan](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261023T030510-0400/live-search-evidence.json), [timestamps и итог](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261023T030510-0400/run-result.json).

Точный текст: [report.md](sandbox:/workspace/scratch/7a43f0b7d905/vet-trial-audit-20261023/research/audit-runs/daily-20261023T030510-0400/report.md).
