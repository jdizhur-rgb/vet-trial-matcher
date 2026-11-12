# DAILY GLOBAL WORK AUDIT — 12 ноября 2026

**Фактическое время:** 03:06:46–03:54:28 America/New_York  
**Режим:** DAILY GLOBAL WORK AUDIT  
**Результат:** **UPDATE / INCOMPLETE**. Подтверждённое изменение опубликовано; техническая публикация и production-поиск прошли. Клиническая полнота остаётся INCOMPLETE из-за 160 источников без достаточного свежего roster/protocol evidence.

## Новые исследования

**1. University of Illinois, USA — кошки с плоскоклеточным раком ротовой полости: SBRT + olaparib + metformin.**

- **Животные и опухоль:** кошки старше одного года с цитологически или гистологически подтверждённым oral squamous cell carcinoma; опухоль должна быть доступна для биопсии и подходить для лучевой терапии.
- **Лечение:** стереотаксическая лучевая терапия три дня подряд, затем olaparib и metformin внутрь.
- **Расходы:** исследование покрывает лучевую терапию, установку feeding tube, предусмотренные протоколом анализы/КТ и исследуемые препараты. Владелец оплачивает первичную консультацию, eligibility-диагностику, обычные осмотры на recheck, дополнительное наблюдение/поддерживающую помощь и лечение, не связанное с протоколом. Для части протокольных нежелательных явлений может быть доступна дополнительная поддержка.
- **Срок набора:** на прочитанном текущем протоколе дата окончания набора не опубликована.
- **Официальный протокол:** https://vetmed.illinois.edu/wp-content/uploads/2026/11/OSCC-RT-Olap-and-Metformin-Trial.pdf

Это отдельный протокол, а не обновление старой записи Illinois с bexagliflozin: третий препарат materially differs, и опубликован новый protocol-level PDF за ноябрь 2026 года. Новый canonical ID: `illinois-feline-oscc-sbrt-olaparib-metformin-2026`.

## Что исправлено

1. Добавлена отдельная подтверждённая карточка Illinois и соответствующие matcher selection cases.
2. Полностью перечитан текущий протокол CSU по feline oral SCC immunotherapy; статус, funding и дата protocol review обновлены, durable issue закрыт.

## Закрыто или скрыто

**0 новых закрытий/скрытий в каталоге.** Сигнал Paccal повторно квалифицирован как `CLOSED_CONFIRMED`; соответствующая карточка уже была исключена из matching до этого запуска.

**Новые источники:** 0. Inventory сохранён полностью: 161 источник.

## Поиск и охват

- **Обработка очереди:** 161/161 источников; 12/12 регионов; незавершённая работа исполнителя: **0**.
- Фактически открыто сегодня: 138 источников. Для 23 источников все записанные маршруты имеют сохранённый exact access restriction; новые запросы к ним не выполнялись и прежние даты evidence сохранены.
- Проверено 161 master URL и 120 записанных fallback routes: разрешённые маршруты открывались native transport и, при недостаточном результате, Web. Exact restrictions, CAPTCHA/login/access gates не обходились.
- Global discovery: два прохода, 48 отдельных country/language queries — current/undated и fresh signals с семидневным перекрытием. Использованы английский и местные языки по всем 12 регионам.
- Leads: 1 добавлен; 5 сопоставлены с exact существующими canonical IDs; 1 подтверждён закрытым; 2 оставлены unresolved из-за недостаточного primary evidence.
- Полностью перечитано сегодня 2/154 публичных протокола. Независимая protocol/selection-проверка завершена для 142/154; 12 остаются pending independent review. Остальные записи получили сегодняшнее решение по status/deadline route, но не названы полностью перечитанными.
- Сроки набора проверены для всех 321 canonical records независимо от возраста страницы: 19 — будущая/сегодняшняя подтверждённая дата; 4 прошедшие даты уже nonmatchable; 68 — текущая страница не дала достаточного подтверждения даты; 68 — в текущем прочитанном evidence дата не опубликована; 162 — nonmatchable без известного cutoff. Активных карточек с уже прошедшей подтверждённой датой набора нет.

## Что осталось нерешённым

| Результат источника | Число | Что это означает |
|---|---:|---|
| Fully reconciled | 1 | Свежий текущий roster/protocol evidence достаточен |
| Partial | 128 | Маршруты обработаны, но полный текущий roster не установлен |
| Unreachable после разрешённых попыток | 9 | Разрешённые маршруты открывались, usable content получить не удалось |
| Not checked из-за exact restriction | 23 | Все записанные маршруты имели действующий точный запрет повторной попытки; новых визитов и новых дат не заявлено |

В raw receipt 32 строки имеют `master_result=unreachable`; таблица выше отдельно выделяет 23 restriction-only строки, чтобы они не выглядели как сегодняшние сетевые попытки.

- **Внешние пробелы:** 160 — 128 `roster_unestablished`, 32 `source_unavailable`; все имеют source-specific question, URLs/evidence, следующий допустимый шаг и completion decision в `gap-review.json`.
- **Executor incomplete:** 0. Доступной несделанной работы по сегодняшней очереди не осталось.
- **Durable issues:** 78 — 70 `BLOCKED`, 8 `OWNER_DECISION`. Сегодня закрыт 1 issue.
- **Discovery unresolved:** UQ Enzistat — news-сигнал отсутствует в сегодняшнем current UQ roster; VRCCO T-cell engager — нет общего exact protocol/sponsor ID, достаточного для решения старого WSU/multicenter identity question.
- **Rejected:** 0. **Semantic duplicates:** 0 новых; пять discovery signals квалифицированы как уже существующие exact protocols, а не как новые записи.

Восемь вопросов Юле сохранены без автоматического медицинского/редакционного решения: Wisconsin FLASH consent path; две UC Davis liver identities; First Coast в ePUSH; JHU cryotherapy/immunotherapy identity; Fort Worth HSA arms; Tufts/CSU FAP branches; Virginia Tech histotripsy funding threshold; классификация UC Davis palliative-amputation access.

## Каталог до → после

| Показатель | До | После |
|---|---:|---:|
| Canonical records | 320 | 321 |
| Public matchable | 153 | 154 |
| Treatment trials | 149 | 150 |
| Other treatment access | 4 | 4 |
| Sources | 161 | 161 |

## Технический результат

- **Среда:** PASS — Python 3.12.14, git 2.52.0, рабочая директория `/workspace/scratch/c446bd545bf3`.
- **Validators:** sanitation, schema/catalog, semantic duplicates, source inventory, matcher build, Python/JS selection, protocol sources, static build, production sync, source evidence keys, gap review и execution gate — PASS. Strict receipt — ожидаемый **INCOMPLETE**, 160 evidence gaps, structural errors 0.
- **Loading regression:** PASS. Ранний поиск до загрузки, задержанная загрузка USA/Japan и отказ загрузки не дали ложный ноль; локальные ожидаемые результаты после загрузки — USA 96, Japan 14.
- **Публикация данных:** PASS. Data commit в remote-main: `c7915be0876eb563a508dce795788b1fd32be835`. GitHub Actions: catalog integrity PASS, evidence-key check PASS, build/deploy PASS.
- **Production readback:** PASS. Live `trials.json` SHA-256 `44c1b8719bc71caf8f1f0f2a14a68d809014d0b496781282052443be58bf1e63` совпадает со сборкой и содержит новый Illinois ID. HTML загружает `matcher.js?v=clinical-audit-20261103-owner-rules-r1`; deployed build, live script version и функциональный поиск согласованы.
- **Live USA search:** PASS — Dog / Cancer — any type / I don't know / пустые age, weight и ZIP / все варианты лечения / Any approach: **96** отображаемых результатов, как в текущем каталоге.
- **Live Japan search:** PASS — тот же профиль: **14** отображаемых результатов, как в текущем каталоге.
- **Даты проверки источников:** до запуска — 138 источников с датой 2026-11-11, 16 с 2026-11-06, 7 с 2026-11-08; после — 138 фактически посещённых источников получили 2026-11-12, 23 restriction-only сохранили исходные даты (16 с 2026-11-06, 7 с 2026-11-08).
- **Локальные hashes:** `trials_base.json` `a100530e…78ca`; `source_inventory.json` `71c8e4cb…9113`; live matcher catalog `44c1b871…1e63`.
- **Итог очереди:** PASS, executor incomplete 0. **Итог достаточности evidence:** INCOMPLETE — 160 внешних пробелов. PASS учёта не означает клиническую полноту.

## Подробные артефакты

- `receipt-final.json` — per-source processing/evidence result
- `execution-review.json` и `execution-validation.json` — source/issue/lead decisions и gate
- `gap-review.json` — точные причины partial/unreachable и следующие допустимые шаги
- `deadline-review.json` — ежедневная проверка recruitment dates
- `trial-review-ledger.json` — 154 публичных протокола и уровень сегодняшней проверки
- `discovery-current-undated.json`, `discovery-recent-7d.json` — оба discovery-прохода
- `validation-results.json`, `production-readback.json`, `git-readback.json` — validators, deploy и readback

**Причина окончания:** доступная работа сегодняшнего scheduled run завершена; остались только документированные внешние пробелы и восемь owner decisions. Runtime failure и установленный предел не были причиной остановки.
