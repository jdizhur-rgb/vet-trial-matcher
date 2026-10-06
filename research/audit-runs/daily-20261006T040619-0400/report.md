6 октября 2026, 05:32 America/New_York
Режим: DAILY GLOBAL WORK AUDIT

**Проверка среды: PASS.** Реально исполнены `pwd` → `/workspace/scratch/0856bb16a45a`, `python --version` → Python 3.12.14, `git --version` → git 2.51.1. Shell, локальные файлы, Python и Git доступны.

**Итог: INCOMPLETE. Подтверждённые изменения опубликованы и проверены в production.** Полностью сверены 39 из 91 источника; 52 сохраняют пробелы. Успешный deploy не означает завершённого аудита.

Run ID: `daily-20261006T040619-0400`. Начало: 04:06:19; окончание проверок: 05:32:27, America/New_York. Исходная версия remote main: `6f83f40fc30a7c2260d58a5ab3663e80b116ff7f`. Продолжение незакрытых вопросов предыдущего прохода сопровождалось новыми фактическими посещениями; старые evidence не засчитывались за сегодняшние.

**Known-source coverage и fallback.**

| Источники | Фактически предпринята проверка | Достаточная сверка | Partial | Unreachable |
|---|---:|---:|---:|---:|
| 82 исходных | 82 | 36 | 39 | 7 |
| 9 новых | 9 | 3 | 6 | 0 |
| Всего | 91 | 39 | 45 | 7 |

Посещены master всех исходных источников и все 27 официальных fallback из исходного inventory; в расширенном inventory — 31 fallback. Неиспользованных обязательных fallback нет. Receipt содержит 615 уникальных фактически запрошенных URL; число запросов не выдаётся за число проверенных протоколов.

Полная сверка включает свежий roster: 30 источников с подтверждённым неизменившимся набором и 9 с дополнительной сверкой. HTTP 200, старый fingerprint и `protocols_seen=null` не засчитывались как достаточный охват. VCS удалось прочитать через публичный page reader: его 41 ссылка ведёт к источникам trials, а не является списком 41 протокола. genui{"citation":{"ref":"turn46view0"}}

Недоступными остались Michigan State, Missouri, RVC, Washington State, NCI, Veterinary Cancer Care и Nippon Veterinary and Life Science University. По каждому сохранены URL, время, HTTP/error и результаты fallback.

Среди доступных источников основные пробелы: шестицентровый COTC033; идентичность и набор по FAP CAR-T; полные статусы центров вакцинных программ; расхождения институциональных и sponsor/registry страниц; старые приглашения Paccal Vet, Biokera и японских программ; закрытые профессиональные материалы. Все 52 source ID и точные основания сохранены в [pending-queue-final.json](sandbox:/workspace/scratch/0856bb16a45a/vet-trial-matcher/research/audit-runs/daily-20261006T040619-0400/pending-queue-final.json).

После часового checkpoint работа продолжалась. Причина INCOMPLETE — исчерпанные рассмотренные публичные официальные маршруты при сохраняющихся пробелах первичных данных, блокировках и противоречиях статусов. Это не остановка по часовому лимиту. Проверки care directory, онкологов и сервисных каталогов в этот аудит не включались.

**Global new-source discovery.**

Поиск выполнен для всех 12 обязательных групп: США; Канада; Великобритания; континентальная Европа; Мексика/Центральная Америка/Карибы; Южная Америка; Австралия/Новая Зеландия; Восточная Азия; Южная Азия; Юго-Восточная Азия; Ближний Восток; Африка.

Использовались английский и региональные запросы на французском, немецком, испанском, португальском, японском, китайском, корейском, хинди, тайском, иврите, арабском и африкаанс; проверялись также новости и публичные LinkedIn-сигналы. Это поиск новых возможностей, а не заявление об исчерпывающем отсутствии trials в регионе. Точные 12 запросов трёх итоговых региональных поисковых пакетов, результаты и ограничения сохранены в [global-discovery.json](sandbox:/workspace/scratch/0856bb16a45a/vet-trial-matcher/research/audit-runs/daily-20261006T040619-0400/global-discovery.json). Для ранних пакетов сохранены результаты, но утраченные формулировки запросов не реконструировались.

**NEW — 2.**

- [Gifu: кошки с оральным SCC, лучевая терапия + Lavurchin/SQAP](https://www.animalhospital.gifu-u.ac.jp/cancer/clinical_trial/202508.html). Исследуемый препарат предоставляется; обычная лучевая терапия и стандартная помощь оплачиваются владельцем. Контакты и адрес проверены.
- [Hokkaido: anti-PD-L1 для собак с оральной меланомой и метастазами в лёгких](https://www.vetmed.hokudai.ac.jp/VMTH/aboutus/research/). Публичная стоимость не указана; запись требует prescreening команды. Это отдельный протокол от японского anti-PD-1 регистрационного исследования.

**UPDATE — 5.**

- CSU engineered T cells: текущий протокол относится к soft-tissue sarcoma; OSA исключена. Исправлены минимум 11 кг, washout, ограничения предыдущей иммунотерапии и пределы финансирования.
- Wisconsin lymphoma + CHOP: четыре фракции RT; вход после двух циклов CHOP при частичном ответе или полной ремиссии. Matcher исключает прогрессию и неподходящий этап лечения.
- Wisconsin FLASH OSA: уточнено покрытие RT/ампутации. Из-за противоречия краткой страницы и consent сохранено консервативное требование планируемой ампутации.
- [UC Davis CARE](https://studypages.com/s/novel-drug-combined-with-radiation-therapy-for-dogs-with-brain-tumors-glioma-353022/): указан BAQ-13; начальная диагностика оплачивается владельцем, $4,000 на RT предоставляются после завершения лечения, помощь при осложнениях в UC Davis ограничена $3,000. Добавлено работающее требование планируемой RT.
- [UC Davis PRISM](https://studypages.com/s/prism-trial-precision-research-integrating-symptoms-and-molecular-biology-in-canine-glioma-788706/): $3,000 относятся к продолжающемуся лечению; необоснованное обещание оплаты начальной диагностики убрано. В matcher оставлен только путь доступа к лучевой терапии.

**CLOSE/HIDE — 0.** Уже скрытые завершённые программы не открывались заново по старым приглашениям.

**NEW SOURCES — 9:** ACI Biosciences, EVVIVAX, CureLab, The Cancer Vet, Dog Cancer Foundation, Gifu, Hokkaido, Benno Therapeutics, Seoul National University. Достаточная сверка получена для ACI, Gifu и Hokkaido; остальные шесть имеют честный partial.

**UNRESOLVED / REJECTED / DUPLICATES.** В AVMA перечислены 850 карточек, среди них 62 со статусом Recruiting и oncology. Из этих 62: 51 сопоставлена с известной canonical identity; 3 отклонены как диагностические исследования; 8 сохраняют неопределённую идентичность или неподтверждённый текущий primary enrollment. Эти восемь входят в проблемы охвата и не прибавляются к 52 источникам как отдельный счётчик источников.

Отклонены blood-test/relapse biomarker study, диагностическое картирование лимфоузлов AGASACA и PS-OCT после удаления feline mammary tumors. Возможные повторные ECT-карточки не превращены в новые trials без первичной сверки. Semantic dedupe: 0 probable duplicate pairs. Шесть ранее известных неполных исторических записей остались в существующей unresolved-очереди; новых неполных canonical rows нет.

**Точные counts before/after.**

| Показатель | До | После |
|---|---:|---:|
| Canonical records | 299 | 301 |
| Public matchable opportunities | 161 | 163 |
| Treatment trials в public matcher | 156 | 158 |
| Other treatment access | 5 | 5 |
| Trial sources | 82 | 91 |

**Даты проверки источников — PASS по сохранению, INCOMPLETE по содержательному охвату.**

У исходных 82 источников предыдущий `last_checked` — 2026-10-05; предыдущие `last_checked_at` — от 18:33:57 до 19:29:05 America/New_York. У девяти новых источников прежних дат не было.

Новые `last_checked` — 2026-10-06, реальные timestamps — от 04:06:19.575037 до 05:24:22. Результаты: 30 unchanged, 9 reachable, 45 partial, 7 unreachable. Неудачная попытка получает дату, но не статус успешной сверки.

Local readback: **PASS 91/91**. Remote-main readback: **PASS 91/91**, проверены даты, timestamps, result, run_id, protocols_seen и coverage_gap. Remote SHA данных: `92550ec1d6241ec249a3af6631a9c740d6e1f4ce`. Remote latest receipt и immutable receipt сегмента 2 также прочитаны и совпали с локальными байтами. Предыдущие/новые значения каждого источника находятся в [local-readback.json](sandbox:/workspace/scratch/0856bb16a45a/vet-trial-matcher/research/audit-runs/daily-20261006T040619-0400/local-readback.json).

**Validators, commit/deploy/production.**

Sanitation, schema/unique IDs, source inventory, semantic dedupe, matcher regression, build, production sync, full catalog integrity и repository hygiene — PASS. `python scripts/validate_audit_receipt.py` — **INCOMPLETE: errors=[]; 52 coverage gaps; обязательные fallback не пропущены**. Необязательный Streamlit smoke не выполнен из-за отсутствующего модуля; основные проверки прошли.

Публикация в main: первый сегмент `39c783e5fc9c8b58406f54ddd7f1c9ff0b32c0ed`, окончательные изменения данных — [92550ec](https://github.com/jdizhur-rgb/vet-trial-matcher/commit/92550ec1d6241ec249a3af6631a9c740d6e1f4ce). Все пять GitHub workflows завершились успешно. [Deploy 37443285004](https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/37443285004) — success.

Production проверен в 05:32:07: `/matcher/trials.json`, `/matcher/matcher.js` и `/matcher/` отвечают HTTP 200 и побайтно совпадают с соответствующими собранными артефактами. Первая попытка сравнения HTML использовала исходный шаблон вместо собранной страницы; ошибка проверки исправлена, отдельный результат той попытки сохранён.

Изменены `data/trials_base.json`, `data/source_inventory.json`, `data/audit_source_coverage.json`, `data/audit_state.json`, `seo/static/matcher/trials.json`, `seo/static/matcher/matcher.js`, `scripts/test_matcher_logic.js`, `PROJECT_OPERATIONS.md` и файлы этого run в `research/audit-runs/`. В operations убрано оставшееся противоречие про часовой cutoff. Сегментные receipts, checkpoints и архивы evidence сохранены отдельно.

[Финальный receipt](sandbox:/workspace/scratch/0856bb16a45a/vet-trial-matcher/research/audit-runs/daily-20261006T040619-0400/receipt.json) содержит текущий статус INCOMPLETE; [production proof](sandbox:/workspace/scratch/0856bb16a45a/vet-trial-matcher/research/audit-runs/daily-20261006T040619-0400/production-readback.json) — PASS. Настройки push/email этим проходом не проверялись.

[report.md](sandbox:/workspace/scratch/0856bb16a45a/vet-trial-matcher/research/audit-runs/daily-20261006T040619-0400/report.md)
