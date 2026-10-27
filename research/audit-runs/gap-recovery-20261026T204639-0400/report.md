# Исправление результатов утреннего аудита — 26 октября 2026

Фактическая работа: 20:46:39–20:58:05 America/New_York. Режим: targeted gap recovery, дополнение к DAILY GLOBAL WORK AUDIT. Это отдельная работа по пропущенным шагам, а не повторный мировой обход.

**Результат: INCOMPLETE.** Подтверждённые исправления опубликованы в main и проверены на сайте. Прежние заявления «вся очередь обработана» и «недоделок 0» отозваны: утренний finalizer автоматически проставлял completion/external-blocker без индивидуальных решений; reviews.json был пуст.

## Новые исследования и изменения

Новых исследований: **0**. Новых источников: **0**.

Закрыто для нового набора / скрыто из trial-подбора: **1** — University of Tokyo, кошки с уротелиальным раком, лапатиниб. Официальный японский текст сообщает, что целевое число случаев набрано и исследование заканчивается 31 октября 2026. Отдельно университет предлагает применение препарата за счёт владельца; это не открытый набор в исследование. Уведомление было уже в утреннем native evidence и пропущено при сверке; свежее вечернее чтение его подтвердило. Web reader вернул отличающуюся старую версию без этого абзаца, конфликт свежести сохранён отдельно.

Официальная страница: https://www.vm.a.u-tokyo.ac.jp/vmc/aboutus/research/

Полностью перечитаны **16 протоколов**: Auburn — 1, Cornell — 2, Illinois — 8, Tokyo — 5, включая завершивший набор. У **15 остающихся публичными** записей обновлены реальные даты полного review; у закрытой сохранено решение по статусу. Funding dates обновлены только там, где финансирование действительно перечитано и подтверждено. Правила диагноза, лечения и расходов не расширялись.

## Охват и оставшаяся работа

Из 96 утренних пробелов индивидуально разобраны **6 источников**: Auburn, Cornell, Illinois, LSU, Gamgee и Tokyo. Выполнено **15 новых native-запросов** к протоколам, открытой oncology-навигации и пагинации, плюс один Web-readback конфликта Tokyo. Утренние master-visits сохранены с исходными timestamps и не названы новыми вечерними визитами. Два мировых поиска повторно не выполнялись.

Для остальных **90 источников** завершение сверки **не установлено**. Они больше не обозначены автоматически как внешние блокеры. У каждого сохранены исходные attempts и требуемые шаги: разбор содержимого и официальной навигации, идентификация протоколов и сверка с canonical. Точное число отдельных действий ещё не установлено; ноль не заявляется.

| Учёт | Количество |
|---|---:|
| Источники, индивидуально разобранные в этой работе | 6 |
| Неподтверждённое завершение из исходных 96 | 90 |
| Утренние достаточные источники, унаследованные без нового независимого разбора | 47 |
| Суммарный достаточный evidence в amended receipt, включая эти унаследованные 47 | 53/143 |

**53/143 не означает, что в этой работе заново проверены 53 источника.** Строгий receipt остаётся INCOMPLETE. Незавершённая работа исполнителя не спрятана среди внешних причин. Ручных действий Юлии для опубликованных исправлений не требуется.

## Каталог до → после

| Метрика | До | После |
|---|---:|---:|
| Canonical | 313 | 313 |
| Public matchable | 153 | 152 |
| Treatment trials | 149 | 148 |
| Other treatment access | 4 | 4 |
| Sources | 143 | 143 |

## Технический результат

Среда PASS: Python 3.12.14, Git 2.51.1. Sanitation, schema, source inventory, semantic dedupe, source-derived/matcher selection, static build, loading regression, matcher logic, production sync и evidence-key gate — PASS. У validator добавлены регрессии против generic route-coverage prose, массового одинакового completion и противоречивого processing_complete. Семь тестов PASS; прежний утренний gap-review теперь ожидаемо FAIL, исправленный review PASS с processing_completion=NOT_VERIFIED и 90 пробелами. Schema PASS не назван успешным аудитом.

Main data commit: `3abe1a1f61e78f13c79ac6bfdbdd8b830fc59d06`, remote readback PASS. Deploy `40429373103` завершён success. Live HTML, JS и JSON побайтно совпали со сборкой. Новый catalog version `45dd6a44f8df2fec`; script version `clinical-gi-20261022` не менялась, поскольку JS не менялся.

Live UI: Dog / Cancer — any type, unknown diagnosis, пустые age/weight/ZIP, все treatments, Any approach — USA **99**, Japan **10**, PASS. Cat / Japan / Urothelial carcinoma — **2** оставшихся broad-treatment результата; закрытый lapatinib trial отсутствует. Все результаты совпали с текущей сборкой.

Даты источников: шесть источников имеют новые фактические evening timestamps. Остальные source-visit dates не обновлялись. Local/remote canonical SHA-256 `0dc5aeb2ad2eef0ba9b17624fa2266c80f221bdff89678a5dba0fd9eda75c1f4`; inventory SHA-256 `4d147008d26c6c9bb4099b7fb03b720f842490b1bccd71ec0ea98e3c9f054949`. Полные hashes и source-by-source provenance находятся в local-hashes.json, remote-main-readback.json, reviews.json и trial-reviews.json.

Артефакты: recovery-plan.json, reviews.json, trial-reviews.json, receipt-final.json, gap-review.json, validation.log, old-blanket-claims-regression.json, production-readback.json, deploy-readback.json, web-freshness-conflict.json. Исходные утренние receipts и отчёт не переписаны; это отдельное исправление их выводов.
