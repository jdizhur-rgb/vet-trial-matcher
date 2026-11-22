# DAILY GLOBAL WORK AUDIT — 22 ноября 2026

**Итог: INCOMPLETE / NO CHANGE.** Учёт исполнения — **PASS**; доступная работа закончена. Клиническая полнота — **INCOMPLETE** из-за 165 текущих внешних пробелов в evidence. Подтверждённых изменений состава каталога нет. Техническое исправление опубликовано, все обязательные remote workflows и production readback прошли.

## 1. Запуск и публикация

- Дата и время America/New_York: **22 ноября 2026, 03:35:44–04:05:00 EST**.
- Режим: **DAILY GLOBAL WORK AUDIT**.
- Run ID: `daily-20261122T033544-0500`; запуск инициализирован как плановый с `--scheduled` до внешних запросов.
- Baseline remote-main: `74a8706de9babe725ba5061cb714aa515d28edad`.
- NEW: **0** исследований и **0** источников. UPDATE/CLOSE/HIDE каталога: **0/0/0**.
- Опубликован технический repair commit `d61e8b167a8833b46842c210df1740d56ab7bec0`; data/clinical catalog остался без содержательных изменений.

## 2. Новые исследования

**0 безопасно добавляемых новых исследований.** Мировой поиск дал 242 уникальных candidate URL; 23 лечебных лида разобраны индивидуально. Из них 13 точно сопоставлены существующим canonical IDs, 5 оказались уже известными source/index pages, 1 подтвердил закрытый протокол, 1 не являлся лечением и 3 оставлены `PENDING_EVIDENCE`:

- University of Florida, кошки с oral carcinoma, LSD1 inhibitor после лучевой терапии: официальный protocol-level текст одновременно говорит «currently recruiting» и «Enrollment Paused». Включение без уточнённого официального статуса небезопасно.
- Paccal Vet feline cancer study: exact official page возвращает 401; тип опухоли, площадки, текущий набор и связь с завершёнными sponsor cohorts не установлены.
- JVCOG, Япония: старая страница описывает неназванный anticancer drug без достаточного protocol identity; exact canonical ID не установлен.

Для этих трёх лидов не выдуманы ни canonical ID, ни статус. Outreach не выполнялся.

## 3. Что исправлено

1. Исправлена техническая порча `data/source_inventory.json`, возникшая при публикации большого blob: файл пересериализован компактно без изменения JSON-данных. Remote blob посимвольно совпадает с локальным; SHA-256 `a33595fc384dace7e6536207c13c964c594088a84c9bffb4cb293b0b8ade6123`.
2. Workflow `.github/workflows/full-catalog-audit.yml` теперь устанавливает Python 3.12 и зависимости из `requirements.txt`, поэтому remote full catalog audit действительно запускает Streamlit checks. Повторный GitHub Actions run — PASS.

Медицинские, eligibility, funding, site и matcher-data записи не менялись.

## 4. Закрыто, скрыто и новые источники

- Закрыто: **0** новых записей.
- Скрыто: **0** новых записей.
- Новые источники: **0**.
- Один discovery lead подтвердил уже закрытый протокол; это не потребовало новой правки каталога.
- Сроки набора пересчитаны для **323/323** canonical records. Опубликованный `recruitment_end` имеется у 43; 3 срока уже прошли, но **0** из этих записей остались matchable. Подтверждённых продлений — **0**; результат deadline review — **NO CHANGE**.

## 5. Поиск и охват

- Очередь: **168/168** источников получили индивидуальное текущее решение; незавершённых разрешённых действий исполнителя — **0**.
- Strict current evidence: **3 complete**, **135 partial**, **30 unreachable/not opened because of exact saved restriction**; у 165 источников полный текущий roster/status не доказан.
- Native source retrieval: 303 URL jobs, 251 transport errors, 52 exact restriction skips. Same-URL Web fallback: 251 route, 222 успешных чтения, 29 Web errors.
- Native protocol retrieval: 177 jobs, 139 transport errors, 38 exact restriction skips. Web fallback: 139 route, 122 успешных чтения, 17 Web errors.
- Global discovery: **12/12 регионов**, 36 отдельных country/language queries, две поисковые проверки, 242 уникальных candidate URL, 23 selected treatment leads reviewed.
- BluePearl clinical trials, VCA clinical studies и Ethos clinical studies были в scope; oncology care/services directories исключены. BluePearl current item точно сопоставлен существующему `bluepearl-hsa-paccal`; VCA clinical route не дал полного roster; прямые Ethos study pages, найденные через discovery, проверены без обхода сохранённых exact restrictions.
- Независимые source-derived eligibility cases: **142/153** public records reviewed, **11** остаются pending в независимом клиническом gate. Техническая матрица matcher/selection прошла, но она не заменяет медицинскую полноту.

## 6. Что осталось нерешённым

| Evidence-состояние | Количество | Причина |
|---|---:|---|
| Fully reconciled current roster | 3 | UK VCSR, BluePearl и Vetigenics дали достаточное текущее roster evidence |
| Partial / roster unestablished | 135 | Страница прочитана, но полного текущего oncology-treatment roster/status она не доказывает |
| Unreachable / exact restriction | 30 | Текущая разрешённая route недоступна либо сохранено точное ограничение доступа |
| Not checked by executor | 0 | Доступных разрешённых шагов не осталось |

Все **165** gaps имеют individual external-blocker decision; automatic-review и exact access restrictions не обходились и не расширялись на учреждение целиком. Все **74** унаследованных issue получили текущее индивидуальное решение и остаются durable `BLOCKED`; закрытых без evidence вопросов нет. Candidate dispositions: 13 existing exact matches, 5 source indexes reviewed, 3 pending evidence, 1 closed confirmed, 1 not treatment. Вопрос Юле требуется только для UF, если она решит редакционно показывать противоречивый recruiting/paused протокол; автоматическое включение отклонено как небезопасное.

Причина окончания: `completed_available_work`. Не выполненных разрешённых действий нет; остаток требует нового publisher signal, доступного official protocol evidence либо разрешения противоречия UF. Это не основание объявлять клиническую полноту.

## 7. Каталог до → после

| Показатель | До | После |
|---|---:|---:|
| Canonical records | 323 | 323 |
| Public matchable records | 153 | 153 |
| Treatment trials | 150 | 150 |
| Other treatment access | 3 | 3 |
| Source inventory | 168 | 168 |

ADD/UPDATE/CLOSE/HIDE/NEW SOURCE: **0/0/0/0/0**. Effective catalog и production JSON содержат 153 уникальных ID без дублей.

## 8. Технический результат и даты проверки источников

- Среда: `pwd`, Python 3.12.14 и Git 2.56.1 — PASS. Локальный preflight — `PASS_WITH_INCONCLUSIVE` только потому, что в локальной среде не установлен Streamlit; GitHub workflow после установки `requirements.txt` — PASS.
- Accounting gate — **PASS**: 168/168 source decisions, 74/74 issue decisions, `available_remaining=[]`; `EXECUTION=PASS`, `CLINICAL_RECONCILIATION=INCOMPLETE`, `DISCOVERY=INCOMPLETE`.
- Strict receipt — ожидаемый **INCOMPLETE**, ошибок структуры нет, 165 coverage gaps. Gap validator — **PASS**, `EXTERNAL_GAPS_ONLY`.
- Source inventory, canonical catalog, sanitation, repository hygiene, evidence keys, git diff, matcher build, JS/Python matcher selection, catalog loading regression, static build и production sync — **PASS**. Первый matcher-logic вызов до генерации SEO-файла честно завершился ENOENT; после обязательного static build повторный запуск — PASS.
- Full catalog GitHub Actions: **PASS**, run 45005295555. Evidence keys: **PASS**, run 45005295543. Build/deploy: **PASS**, run 45005295537.
- Production: live JSON — 153 records, 153 unique IDs, 150 treatment + 3 other treatment access. Dog / Cancer — any type / I don't know / пустые age-weight-ZIP / all treatments / Any approach: USA **96/96 PASS**, Japan **14/14 PASS**; полные упорядоченные списки совпали с локальной сборкой по длине и FNV-1a-64.
- Даты проверки источников: processing metadata записана для **168/168** rows; `last_checked_at` фактически продвинут у **138**, где Web evidence имел label `today`, в диапазоне 03:37:15–03:40:05 EST. У 30 exact-restriction/unavailable rows прежние даты сохранены, а попытка/ограничение отражены в receipt; исходные clinical evidence dates не переписаны. Remote readback source inventory — **PASS** на SHA `d61e8b167a8833b46842c210df1740d56ab7bec0`.

**Финальный статус: INCOMPLETE / NO CHANGE.** Очередь доступной работы полностью обработана и опубликована; доказательств недостаточно для заявления о клинической полноте. Production и техническая публикация — PASS.
