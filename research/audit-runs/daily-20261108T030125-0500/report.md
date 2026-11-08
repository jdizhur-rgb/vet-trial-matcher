# DAILY GLOBAL WORK AUDIT — 8 ноября 2026

**Статус: UPDATE опубликован; учёт выполнения PASS; полное клиническое подтверждение INCOMPLETE из-за внешних пробелов.**  
**Режим:** DAILY GLOBAL WORK AUDIT  
**Run ID:** `daily-20261108T030125-0500`  
**Фактическое время America/New_York:** 2026-11-08 03:01:25 — 03:38:19 EST  
**Причина окончания:** доступная работа закончена; установленный предел не достигнут, runtime failure не было.

## Новые исследования

**2.**

1. **Photodynamic therapy with a novel photosensitizer for tumors in dogs and cats** — Tottori University Veterinary Medical Center, Япония. Собаки и кошки; поверхностные, носовые и опухоли мочевого пузыря; фотодинамическая терапия с новым фотосенсибилизатором. Официальная страница не публикует расходы владельца или покрытие: их нужно уточнять у центра. [Официальный протокол](https://vth-tottori-u.jp/clinical-research/3571/).
2. **Radiation therapy plus mogamulizumab for canine urothelial carcinoma** — VSEC Animal Medical Center, Япония. Собаки с уротелиальной карциномой; лучевая терапия плюс могамулизумаб или плацебо на фоне фирококсиба. Официальная страница не публикует покрытие препарата/плацебо, лучевой терапии, фирококсиба, диагностики или последующего наблюдения. [Официальный протокол](https://vsec.jp/hospital/clinical-research/).

Обе записи проверены по individual primary protocol, добавлены в canonical catalog, сборку и live-матчер.

## Что исправлено

- У `wisc-rpt-metastatic` текущий точный статус AVMA изменён на **Suspended**. Запись уже была недоступна для публичного подбора, поэтому число public matchable не уменьшилось.
- Полностью сверены 25 точных AVMA↔canonical совпадений из свежего AVMA JSON; новых переходов в `Completed` нет.
- В evidence удалены 74 публично отображавшихся Google API key-параметра, после чего пересчитаны 455 sidecar-хешей; проверка утечки ключей PASS.
- Исправлена первая неполная передача двух больших JSON-файлов через Git API. Неполный remote commit не был принят как публикация; исправленный remote tree полностью совпал с локальным и оба JSON читаются.
- Даты набора проверены отдельно от глубокой protocol-перепроверки для всех **318** canonical записей: 13 будущих активных сроков, 1 прошедший срок у уже неактивной записи, **0 активных записей с истёкшим сроком**, автоматических продлений нет.

## Закрыто или скрыто

- **Новых закрытых/скрытых записей: 0.**
- **Исправлен статус: 1** — Wisconsin `wisc-rpt-metastatic` → Suspended; запись уже не участвовала в публичном подборе.
- **Новые источники: 2** — Tottori University Veterinary Medical Center и VSEC Animal Medical Center.

## Поиск и охват

- **Обработка очереди: 161/161 источников, 12/12 регионов; недоделанная работа исполнителя: 0.**
- Физически открыты сегодня **145/161** источников. Для остальных 16 действуют сохранённые точные ограничения доступа/automatic-review; запрещённые маршруты не обходились, и даты этих источников не обновлялись как будто визит состоялся.
- Проверено 279 inventory master/fallback маршрутов; для 44 недостаточных shell-результатов выполнена проверка того же официального URL через Web.
- Выполнены два discovery-прохода — текущие/недатированные возможности и свежие сигналы за 7 дней — плюс 12 углубляющих поисков для слабой выдачи: всего **60 реальных запросов** по 12 регионам на английском и местных языках.
- Разобраны 83 уникальных discovery URL: 2 добавлены; 16 сопоставлены с точными существующими canonical IDs; 46 оказались не лечебными trial pages; 9 были источниками/индексами; 8 остались без достаточного protocol evidence; 2 заблокированы внешним доступом.
- Полный protocol reread сегодня выполнен для **2 новых протоколов**. Для всех 154 публичных записей отдельно выполнена ежедневная проверка сроков; это не выдаётся за полный повторный клинический разбор каждого протокола.

## Что осталось нерешённым

| Итог источника | Число | Что это означает |
|---|---:|---|
| Fully reconciled | 2 | Сегодняшний individual primary protocol достаточен для полного текущего вывода |
| Partial | 121 | Источник обработан, но полный текущий roster/protocol evidence не опубликован или недостаточен |
| Unreachable после разрешённых попыток | 22 | Сегодняшние разрешённые маршруты открывались, но пригодное текущее evidence не получено |
| Not checked из-за точного сохранённого запрета | 16 | Запрос не выполнялся, потому что конкретный маршрут запрещён access restriction/automatic review; старая дата не заменена новой |

Итого строгий receipt: **2/161 content-sufficient; 159 evidence gaps; структурных ошибок 0**. `gap-review` — PASS / EXTERNAL_GAPS_ONLY. Все 56 долговременных вопросов получили индивидуальный текущий разбор; состояние всех 56 — `BLOCKED`, доступных несделанных шагов нет. Это внешние пробелы опубликованных данных или доступа, а не скрытая очередь исполнителя. В discovery 8 лечебных leads оставлены `PENDING_EVIDENCE`, поскольку exact protocol-level подтверждения недостаточно; знакомый домен не считался дублем. Вероятных semantic duplicates в каталоге: **0**. Ручных действий Юлии сейчас не требуется.

Причины 159 пробелов: `protocol_uncertainty` — 59, `roster_unestablished` — 53, `discovery_source_not_trial_roster` — 9, `source_unavailable` — 38. Для каждой строки сохранены конкретный вопрос, evidence/URL, допустимый следующий шаг и source-specific completion decision.

## Каталог до → после

| Метрика | До | После |
|---|---:|---:|
| Canonical records | 316 | 318 |
| Public matchable | 152 | 154 |
| Treatment trials | 148 | 150 |
| Other treatment access | 4 | 4 |
| Sources | 159 | 161 |

## Технический результат

- **Среда:** PASS — Python 3.12.14, Git 2.52.0, рабочий каталог `/workspace/scratch/fd10c0821871/vet-trial-matcher`.
- **Validators:** source inventory PASS (161); trial catalog PASS (318/154 active); sanitation PASS; schema/selection PASS; semantic dedupe PASS; repository hygiene PASS; protocol-source validator PASS; production sync PASS. Preflight: PASS_WITH_INCONCLUSIVE только из-за необязательного отсутствующего модуля `streamlit`.
- **Strict audit:** execution gate PASS; strict receipt INCOMPLETE (159 внешних evidence gaps, 0 structural errors); gap review PASS / EXTERNAL_GAPS_ONLY. PASS учёта не означает клиническую полноту.
- **Matcher loading regression:** PASS — ранний поиск, delayed load Japan=14 и USA=98 и отказ загрузки не дают ложный ноль.
- **Matcher logic:** PASS; production sync: PASS — 154 public records = 150 treatment + 4 access.
- **Публикация данных:** PASS. Исправленный data commit и remote-main readback: `dde97b03469a157d2e125f7bcccc57416b65c990`; tree `83dd2dc9cf61d73207bb87567c62cb4a954de0d4`; local/remote tree и JSON readback совпали.
- **Deploy/production:** PASS. Live HTML, `matcher.js` и каталог побайтно совпадают со сборкой. Новый catalog version в HTML: `f0d92434affea060`. Версия script осталась `clinical-audit-20261103-owner-rules-r1`, потому что `matcher.js` не менялся; live JS побайтно совпадает со сборкой.
- **Live поиск:** PASS. На реально отрисованной production-странице для Dog / Cancer — any type / I don't know / пустые age, weight и ZIP / все treatment options / Any approach отображено USA **98**, Japan **14**. В японской выдаче видны обе новые карточки Tottori и VSEC.
- **Даты проверки источников:** до запуска — 136 источников с 2026-11-07 и 23 с 2026-11-06; после — 145 источников с фактической датой 2026-11-08 и 16 сохранённых restricted источников с 2026-11-06. Новая дата не назначалась без фактического разрешённого визита.

**Итог обработки очереди:** PASS — вся доступная очередь и discovery-матрица обработаны, executor incomplete = 0.  
**Итог достаточности доказательств:** INCOMPLETE — 159 источников имеют документированные внешние пробелы; они не превращены в ложное успешное подтверждение.

## Подробные материалы

- [receipt-final.json](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261108T030125-0500/receipt-final.json)
- [gap-review.json](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261108T030125-0500/gap-review.json)
- [execution-review.json](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261108T030125-0500/execution-review.json)
- [execution-validation.json](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261108T030125-0500/execution-validation.json)
- [deadline-review.json](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261108T030125-0500/deadline-review.json)
- [changed-document-reviews.json](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261108T030125-0500/changed-document-reviews.json)
- [selection-receipt.json](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261108T030125-0500/selection-receipt.json)
- [production-readback.json](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261108T030125-0500/production-readback.json)
- [technical-validation-summary.json](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261108T030125-0500/technical-validation-summary.json)
- [command-log.md](sandbox:/workspace/scratch/fd10c0821871/vet-trial-matcher/research/audit-runs/daily-20261108T030125-0500/command-log.md)
