# DAILY GLOBAL WORK AUDIT — 14 ноября 2026

**Фактическое время:** 03:00:14–03:34:29 America/New_York  
**Режим:** DAILY GLOBAL WORK AUDIT  
**Результат:** **UPDATE / INCOMPLETE**. Подтверждённое изменение опубликовано и проверено на production. Вся очередь обработана; полное клиническое подтверждение остаётся INCOMPLETE из-за 157 внешних пробелов.

## Новые исследования

**0.** Новых лечебных исследований собак или кошек с достаточным текущим protocol-level evidence для добавления нет.

Свежий мировой поиск не подтвердил отдельный новый открытый протокол. K-State сохраняет две индивидуальные страницы назальных radiosensitizer studies, но текущий официальный список clinical trials их не показывает, поэтому они оставлены `PENDING_EVIDENCE`. Свежая публикация о STING-терапии сарком описывает завершённую серию из четырёх собак и призывает к будущему исследованию; текущего owner-facing набора нет.

## Что исправлено

1. **Experimental EGFR/HER2 tumor vaccine** (`medvet-egfr-her2-vaccine-2026`) — текущий multicenter roster сверён по официальной CCA status page и individual site pages.
2. Добавлена активная площадка **Treeline Veterinary Cancer Care, Boulder, Colorado**. Теперь подтверждено **10 активных площадок**.
3. **Veterinary Cancer Care, Santa Fe** не добавлена в matching: CCA показывает новую площадку, но собственная текущая страница клиники говорит, что сейчас никакие trials не набирают. Она сохранена как inactive до разрешения конфликта.
4. У VCCS исправлена обязательная консультация для собаки без собственного онколога: **$595**, а не $495. Два vaccine visits остаются по **$995 каждый**; обязательные тесты и follow-up оплачивает владелец.
5. В source inventory добавлены два официальных fallback routes: текущий список K-State clinical trials и CCA EGFR/HER2 status page.

## Закрыто или скрыто

**0** новых закрытий или скрытий canonical records. Ежедневная проверка сроков не нашла активных публичных карточек с уже прошедшей подтверждённой датой набора.

**Новые источники: 0.** Число источников осталось 162. Добавлены только два официальных fallback URL к существующим источникам.

## Поиск и охват

- **Обработка очереди:** 162/162 источников; 12/12 регионов; незавершённая работа исполнителя: **0**.
- 139 master routes фактически открыты сегодня; 23 exact access restrictions сохранены и не обходились. Для недостаточных master pages обработаны все записанные официальные fallbacks; всего сохранено 128 fallback decisions, включая два новых официальных маршрута.
- Выполнено **96 реальных country/language discovery searches**: 32 current/undated, 32 углубляющих по слабой выдаче и 32 fresh-signal searches с семидневным перекрытием. Использованы английский и местные языки во всех 12 регионах.
- Индивидуально классифицированы 102 discovery leads: 47 `SOURCE_INDEX_REVIEWED`, 23 `VERIFIED_EXISTING`, 17 `PENDING_EVIDENCE`, 14 `NOT_TREATMENT`, 1 `CLOSED_CONFIRMED`.
- Каждый лечебный lead сопоставлялся с exact canonical ID по фактическому протоколу. Знакомый домен не считался дублем.
- **Полный текущий protocol reread сегодня: 1/154 публичных протокола.** Независимый protocol/selection cycle завершён для 143/154; 11 остаются pending. Это отдельно от ежедневного source/status/deadline traversal.
- Сроки набора проверены по всем **321/321 canonical IDs**: 18 `FUTURE_OR_TODAY`, 3 `CROSSED_NONMATCHABLE`, 164 `NO_KNOWN_CUTOFF_NONMATCHABLE`, 95 `NO_PUBLISHED_CUTOFF_FOUND_IN_CURRENT_READ`, 41 `DATE_EVIDENCE_NOT_VERIFIED_TODAY`. Для этих 41 сохранён прежний evidence date; `NOT VERIFIED` не превращён в отсутствие trials.

## Что осталось нерешённым

| Результат источника | Число | Что это означает |
|---|---:|---|
| Fully reconciled | 5 | Свежий официальный roster/protocol evidence достаточен сегодня |
| Partial | 130 | Разрешённые маршруты обработаны, но полный текущий roster не установлен |
| Unreachable | 4 | Разрешённые попытки не дали usable current content |
| Not checked — exact restriction | 23 | Действующий точный запрет повторной попытки; прежние даты evidence сохранены |

- **Внешние пробелы: 157** — 110 `roster_unestablished`, 27 `source_unavailable`, 20 `discovery_source_not_trial_roster`. Для каждого записаны точный вопрос, сегодняшние URLs/evidence, следующий допустимый шаг и source-specific completion decision.
- **Executor incomplete: 0.** Непосещённых разрешённых маршрутов, доступной несделанной сверки и неразобранных выбранных leads не осталось.
- Durable issues: 75 до текущего review; 1 resolved — EGFR/HER2 roster/cost; 74 остаются `BLOCKED` до нового или изменившегося primary evidence. Доступных действий по ним сейчас нет.
- Trial-specific uncertainties: две K-State nasal-radiosensitizer pages отсутствуют в текущем institution roster; Santa Fe противоречит CCA; 11 independent protocol-selection reviews ждут достаточного primary evidence.
- Rejected discovery: 14 не являются текущими лечебными протоколами; 1 закрыт; 23 точно сопоставлены с существующими canonical IDs. **Новых semantic duplicates: 0.**
- Ручные действия Юли: **0**. Допустимые owner decisions приняты по опубликованным данным; неоднозначные medical/status факты не выдумывались.

## Каталог до → после

| Показатель | До | После |
|---|---:|---:|
| Canonical records | 321 | 321 |
| Public matchable | 154 | 154 |
| Treatment trials | 150 | 150 |
| Other treatment access | 4 | 4 |
| Sources | 162 | 162 |

## Технический результат

- **Среда:** PASS. Обязательные первые команды: `pwd` = `/workspace/scratch/c446bd545bf3`; Python 3.12.14; git 2.52.0.
- **Validators:** catalog sanitation, schema, semantic dedupe, source inventory, evidence-key check, repository hygiene, matcher build, JS/Python selection, protocol-source parity, static build, local production sync, execution gate и gap-review — PASS. Strict receipt — честный **INCOMPLETE** с 157 evidence gaps и без structural errors. Preflight — `PASS_WITH_INCONCLUSIVE` только потому, что в runtime отсутствует Python-пакет Streamlit; core build/matcher tests прошли.
- **Loading regression:** PASS. Ранний поиск до загрузки, delayed load для USA/Japan и отказ загрузки не дали ложного нуля. Текущие ожидаемые результаты: USA 96, Japan 14.
- **Публикация:** PASS. Base remote-main `8b8761a1bd3f6e14474eaf9ffa5e1875f5802104`; local audit commit `aec208e74ee6f7e292ff009958898729232ae3b6`; опубликованный data/main commit `430764dc22c268685f441b418ea56b89154bdd60`. Обычный `git push` не имел GitHub credentials, поэтому использован подключённый GitHub Git Data API; remote-main readback — PASS.
- **Deploy / production:** PASS. Live `matcher.js` SHA-256 `a9b0a97c…8375`; live `trials.json` `75acdca6…184a6`; оба byte-identical локальной сборке. Current/cached-busted HTML SHA-256 `a8655cc9…5788` и содержит `trials.json?v=75acdca6f1213fb3` и `matcher.js?v=clinical-audit-20261103-owner-rules-r1`. Один unbusted shell-read кратко вернул прежний HTML cache tag, но обычный live UI уже показывал Boulder и $595, а актуальные assets совпали со сборкой.
- **Live USA search:** PASS — Dog / Cancer — any type / I don't know / пустые age, weight и ZIP / все treatment options / Any approach: **96**, как в текущем каталоге.
- **Live Japan search:** PASS — тот же профиль: **14**, как в текущем каталоге.
- **Published change readback:** PASS — в живом matcher видны Treeline/Boulder, VCCS $595 и EGFR/HER2 protocol.
- **Даты проверки источников:** до запуска — 139 источников с `last_checked=2026-11-13`, 16 с 2026-11-06, 7 с 2026-11-08; после — 139 фактически посещённых источников с 2026-11-14, 16 exact-restricted с 2026-11-06 и 7 exact-restricted с 2026-11-08. Непосещённым даты не обновлялись.
- **Local/remote canonical readback:** PASS. `trials_base.json` SHA-256 `a883822c…6507`; `source_inventory.json` `be208e06…deec`; matcher catalog `75acdca6…184a6`. Опубликованное дерево построено из этих exact local blobs.
- **Итог очереди:** PASS — 162/162, 12/12, executor incomplete 0. **Итог достаточности evidence:** INCOMPLETE — 157 внешних пробелов. PASS учёта не означает клиническую полноту.

## Подробные артефакты

- [report.md](sandbox:/workspace/scratch/c446bd545bf3/vet-audit-nov14/research/audit-runs/daily-20261114T030014-0500/report.md)
- [receipt-final.json](sandbox:/workspace/scratch/c446bd545bf3/vet-audit-nov14/research/audit-runs/daily-20261114T030014-0500/receipt-final.json)
- [execution-review.json](sandbox:/workspace/scratch/c446bd545bf3/vet-audit-nov14/research/audit-runs/daily-20261114T030014-0500/execution-review.json)
- [gap-review.json](sandbox:/workspace/scratch/c446bd545bf3/vet-audit-nov14/research/audit-runs/daily-20261114T030014-0500/gap-review.json)
- [deadline-review.json](sandbox:/workspace/scratch/c446bd545bf3/vet-audit-nov14/research/audit-runs/daily-20261114T030014-0500/deadline-review.json)
- [trial-review-ledger.json](sandbox:/workspace/scratch/c446bd545bf3/vet-audit-nov14/research/audit-runs/daily-20261114T030014-0500/trial-review-ledger.json)
- [master-index.json](sandbox:/workspace/scratch/c446bd545bf3/vet-audit-nov14/research/audit-runs/daily-20261114T030014-0500/master-index.json) и [fallback-index.json](sandbox:/workspace/scratch/c446bd545bf3/vet-audit-nov14/research/audit-runs/daily-20261114T030014-0500/fallback-index.json)
- [discovered-results.json](sandbox:/workspace/scratch/c446bd545bf3/vet-audit-nov14/research/audit-runs/daily-20261114T030014-0500/discovery/discovered-results.json)
- [validation-results.json](sandbox:/workspace/scratch/c446bd545bf3/vet-audit-nov14/research/audit-runs/daily-20261114T030014-0500/validation-results.json)
- [production-readback.json](sandbox:/workspace/scratch/c446bd545bf3/vet-audit-nov14/research/audit-runs/daily-20261114T030014-0500/production-readback.json)
- [git-readback.json](sandbox:/workspace/scratch/c446bd545bf3/vet-audit-nov14/research/audit-runs/daily-20261114T030014-0500/git-readback.json)
- [commands-summary.md](sandbox:/workspace/scratch/c446bd545bf3/vet-audit-nov14/research/audit-runs/daily-20261114T030014-0500/commands-summary.md)

**Причина окончания:** `completed_available_work`. Все доступные разрешённые действия выполнены; предел времени и runtime failure не были причиной остановки. Остались только документированные внешние пробелы, для которых нужен новый/изменившийся primary evidence или окончание exact restriction.
