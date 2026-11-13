# DAILY GLOBAL WORK AUDIT — 13 ноября 2026

**Фактическое время:** 03:06:44–04:07:05 America/New_York  
**Режим:** DAILY GLOBAL WORK AUDIT  
**Результат:** **UPDATE / INCOMPLETE**. Подтверждённое изменение опубликовано; GitHub Actions, deploy, production-файлы и живой поиск USA/Japan прошли. Вся очередь обработана; полное подтверждение INCOMPLETE — внешние пробелы по 161 источнику.

## Новые исследования

**0.** Новых исследований с достаточным текущим protocol-level evidence для добавления нет.

Новый сигнал AVMA `VCT26005992` не является новым trial: это точное совпадение с существующей записью `csu-feline-scgl-radiotherapy-iacuc8528`. Пять страниц Instituto VOC прочитаны отдельно, но опубликованы в 2013–2014 годах и не подтверждают текущий набор; сохранённая страница сама по себе не считалась доказательством открытого набора.

## Что исправлено

1. В существующей карточке CSU по лучевой терапии кошек с small-cell gastrointestinal lymphoma текущий статус AVMA повторно подтверждён как recruiting на 13 ноября 2026 года.
2. Финансирование уточнено по текущей registry-карточке: **fully funded after initial screening**; диагностический screening и помощь вне исследования остаются за владельцем. Полная клиническая дата `verified` не переносилась на сегодня, потому что весь протокол сегодня заново не перечитывался.
3. В inventory добавлен официальный источник Instituto Veterinario de Oncología Comparada (Испания) с master-страницей и всеми пятью опубликованными protocol pages. Его старые страницы не добавлены в текущий каталог без свежего подтверждения набора.

## Закрыто или скрыто

**0 новых закрытий или скрытий в canonical catalog.** В discovery отдельно подтверждены 6 уже закрытых сигналов; они не требовали нового изменения каталога.

**Новые источники: 1.** `spain-instituto-voc-clinical-trials` — https://www.institutovoc.com/seccion/ensayos-clinicos/abiertos/

## Поиск и охват

- **Обработка очереди:** 162/162 источников; 12/12 регионов; незавершённая работа исполнителя: **0**.
- Исходный frozen inventory: 161 источник. Фактически выполнены 137 master-запросов; 24 master routes имели сохранённые exact restrictions и не запрашивались повторно. Выполнены 96 разрешённых запросов к записанным fallback routes; ещё 24 fallback routes были exact-restricted. Для нового Instituto VOC открыты master и 5 индивидуальных protocol pages. Восемь неудачных shell-URL дополнительно проверены через Web.
- Global discovery: **96 отдельных country/language searches** во всех 12 регионах — 32 current/undated, 32 углубляющих при слабой выдаче и 32 fresh signals с семидневным перекрытием. Использованы английский и соответствующие местные языки.
- Разобран 181 выбранный discovery URL: 109 `NOT_TREATMENT`, 36 `SOURCE_INDEX_REVIEWED`, 27 `VERIFIED_EXISTING`, 6 `CLOSED_CONFIRMED`, 3 `PENDING_EVIDENCE`.
- Все лечебные сигналы сопоставлялись с exact canonical IDs по фактическому протоколу. Знакомый домен не использовался как основание для дубля.
- **Полностью заново перечитано сегодня 0/154 публичных протокола.** Это не скрывается под ежедневной проверкой страниц: 143/154 имеют завершённую независимую protocol/selection-проверку из текущего цикла, 11 остаются pending. Сегодняшняя проверка статусов, источников и сроков выполнена отдельно для всех 321 canonical records.
- Сроки набора: 18 `FUTURE_OR_TODAY`; 5 прошедших дат уже nonmatchable; 29 дат не удалось подтвердить свежим evidence сегодня; для 107 в текущем прочитанном evidence cutoff не опубликован; 162 nonmatchable-записи не имеют известного cutoff. **Активных публичных карточек с уже прошедшей подтверждённой датой набора нет.**

## Что осталось нерешённым

| Результат источника | Число | Что это означает |
|---|---:|---|
| Fully reconciled | 1 | Свежий текущий официальный roster/protocol evidence достаточен |
| Partial | 134 | Разрешённые маршруты обработаны, но полный текущий roster не установлен |
| Unreachable | 4 | Разрешённые попытки не дали usable current content |
| Not checked — exact restriction | 23 | Все записанные маршруты имели действующий точный запрет повторной попытки; прежние даты evidence сохранены |

- **Внешние пробелы:** 161 — 119 `roster_unestablished`, 27 `source_unavailable`, 14 `discovery_source_not_trial_roster`, 1 `freshness_uncertain`. Для каждой строки записаны точный вопрос, evidence/URLs, следующий допустимый шаг и source-specific completion decision.
- **Executor incomplete:** 0. Непосещённых разрешённых маршрутов, доступной несделанной сверки или неразобранного доступного lead не осталось.
- **Durable issues:** 77 до запуска; 13 независимых selection-вопросов закрыты текущими решениями, 64 full-protocol issues остаются `BLOCKED` до нового или изменившегося primary evidence. Owner decision: **0** — решения, допустимые по имеющимся данным, приняты без перекладывания на Юлю.
- **Неподтверждённые trial-specific leads:** старый SeineVet/OCRvet сигнал об unspecified monoclonal antibody без текущего primary protocol; аргентинский FCV-UNLP SCC/mTOR сигнал без текущего официального протокола и дат; свежая публикация UNAM об Argovit silver nanoparticles с восемью животными и планом расширения, но без owner-facing протокола, eligibility, sites и маршрута набора.
- **Instituto VOC:** пять старых страниц существуют, но текущая recruitment freshness не установлена. Следующий допустимый шаг — новый официальный status/protocol signal или изменение master, а не повторение той же глубокой проверки без сигнала.
- **Semantic duplicates:** 0 новых. AVMA 29260 квалифицирован как exact existing CSU protocol.

## Каталог до → после

| Показатель | До | После |
|---|---:|---:|
| Canonical records | 321 | 321 |
| Public matchable | 154 | 154 |
| Treatment trials | 150 | 150 |
| Other treatment access | 4 | 4 |
| Sources | 161 | 162 |

## Технический результат

- **Среда:** PASS. Первый обязательный запуск: `pwd` = `/workspace/scratch/c446bd545bf3`, Python 3.11.14, git 2.39.5. В чистом рабочем дереве репозитория: Python 3.12.14, git 2.52.0.
- **Validators:** sanitation, schema/catalog, semantic duplicates, matcher build, Python/JS selection, source inventory, evidence keys, repository hygiene, static build, local production sync, gap review и execution gate — PASS. Strict receipt — честный **INCOMPLETE**, 161 evidence gap, structural errors 0. Локальный preflight — `PASS_WITH_INCONCLUSIVE` только из-за отсутствующего пакета Streamlit; core checks прошли. GitHub Actions full catalog integrity, active links, catalog validation, evidence keys, semantic dedupe и deploy — PASS.
- **Loading regression:** PASS. Ранний поиск до загрузки, delayed loading для USA/Japan и отказ загрузки не дали ложный ноль; текущие ожидаемые значения — USA 96, Japan 14.
- **Публикация:** PASS. Base remote-main `682135f82fec9f3ad233903b0a4ce3672c6c001b`; локальный audit commit `4b676696c9e189fdff5229237707c6ca65eb12a5`; опубликованный data/main commit `f9e24c6869aaef2837df0efafc375d87745c9b6b`. Обычный `git push` не имел GitHub credentials, поэтому публикация выполнена через подключённый GitHub Git Data API; remote JSON readback и парсинг — PASS.
- **Production assets:** PASS. Live HTML SHA-256 `eb15c88d…55f467`, live `matcher.js` `a9b0a97c…8375`, live `trials.json` `a2ac77ec…96b41`; все три совпадают с локальной сборкой. HTML загружает `matcher.js?v=clinical-audit-20261103-owner-rules-r1`.
- **Live USA search:** PASS — Dog / Cancer — any type / I don't know / пустые age, weight и ZIP / все варианты лечения / Any approach: **96** отображаемых результатов, ровно как в текущем каталоге.
- **Live Japan search:** PASS — тот же профиль: **14** отображаемых результатов, ровно как в текущем каталоге.
- **Даты проверки источников:** до запуска — 138 источников с `last_checked=2026-11-12`, 16 с 2026-11-06, 7 с 2026-11-08; после — 139 фактически посещённых источников с 2026-11-13, 16 exact-restricted с 2026-11-06 и 7 exact-restricted с 2026-11-08. Непосещённым дат не приписано.
- **Canonical local SHA-256:** `trials_base.json` `b70afb61…1dae6`; `source_inventory.json` `5565454d…b1e1`; matcher catalog `a2ac77ec…96b41`. Remote canonical JSON опубликован в эквивалентной compact JSON serialization; GitHub Actions подтвердили его schema/content integrity.
- **Итог очереди:** PASS — 162/162, 12/12, executor incomplete 0. **Итог достаточности evidence:** INCOMPLETE — 161 внешний пробел. PASS учёта не означает клиническую полноту.

## Подробные артефакты

- `receipt-final.json` — индивидуальный processing/evidence result для 162 источников
- `execution-review.json` и `execution-validation.json` — индивидуальные source/issue/lead decisions и execution gate
- `gap-review.json` — причины каждого недостаточного результата, evidence, допустимый следующий шаг и completion decision
- `deadline-review.json` — ежедневное сравнение сроков для всех 321 canonical IDs
- `trial-review-ledger.json` и `protocol-selection-validation.json` — уровень фактической проверки каждого протокола
- `master-index.json`, `fallback-index.json`, `web-fallback-index.json`, `evidence/` — timestamps, методы, URLs, hashes и retrieved evidence
- `discovery/` и `evidence/web-discovery-review.json` — реальные поисковые ответы, primary review и решения по leads
- `validation-results.json`, `production-readback.json`, `git-readback.json`, `checkpoint-final.json` — validators, deploy, live readback и финальный checkpoint

**Причина окончания:** `completed_available_work`. Все доступные разрешённые действия выполнены до 180-минутного предела; остались документированные внешние пробелы, требующие нового или изменившегося primary evidence. Runtime failure и истечение времени не были причиной остановки.
