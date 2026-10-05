5 октября 2026, America/New_York (EDT): 18:33:18–19:33:39.
Режим: DAILY GLOBAL WORK AUDIT

**Проверка среды: PASS.** Команды реально выполнены: `pwd` → `/workspace/scratch/5439e1fbe6ea/vet-trial-matcher`; `python --version` → Python 3.12.14; `git --version` → git 2.51.1.

**Статус: INCOMPLETE.** Посещены 82/82 источника, достаточная сверка подтверждена для 31/82. Остаток: 46 частично проверенных и 5 недоступных. Свежая дата попытки не означает успешной проверки. По достижении часового лимита обход остановлен; затем выполнены сохранение, публикация и readback.

Run ID: `daily-20261005T183318-0400`. Методика прочитана из remote main `2febca0b7e62296a02d4cf2f323f1d292c672eb6`; применён Execution and report gate — repaired 2026-10-05. Отдельный аудит oncology-care не проводился.

**Known-source coverage и fallbacks**

Посещены все 78 прежних master-источников и 4 новых. Все обязательные official fallback URLs покрыты: 25 в исходном inventory, 27 в итоговом с новым источником и сохранённым прежним адресом Anivive. Валидатор не обнаружил пропущенных обязательных fallback-маршрутов.

Достаточная сверка подтверждена для UK VCSR, Auburn, Cornell, Iowa, LSU, MSU, Minnesota, NC State, Ohio, Oregon, Tennessee, Illinois, CASTR, OVC, Milan, Kansas, PetCure, AMC, двух источников UQ, PetTrials, MediPaws, BARC, Vivesto, VRCCO, TAMU, PETcura, Puchol, Tokyo, Kamogawa и Saskatchewan. В эту группу входят источники с диагностическими/неподходящими исследованиями и подтверждённым отсутствием подходящего набора.

Основные пробелы:

- AVMA: извлечены 850 карточек, из них 62 помечены Recruiting/Oncology. Не все первичные протоколы и статусы площадок сверены; это не 62 подтверждённых лечебных предложения.
- CSU: 40 карточек, 20 онкологических кандидатов; UC Davis: 38 карточек, 15 онкологических кандидатов. Есть неполные страницы и противоречия между статусом и датами.
- Penn, Purdue, Tufts, Florida, Virginia Tech, MedVet, Ethos, ESVONC/Oncowaf и другие: осталась сверка отдельных протоколов, расходов владельца или полного multicenter roster.
- UTSW: прочитаны master и семь сканированных протоколов через OCR; расходы согласуются с каталогом. Статус отдельной HSA-когорты и применимость umbrella-протокола к кошкам остаются неясными.
- Zurich: перечислены семь протоколов и прочитаны их первичные страницы; исторические записи, площадки и часть условий требуют дальнейшей сверки.
- Недоступны: Veterinary Cancer Society, RVC, WSU, NCI Comparative Oncology и Veterinary Cancer Care. Получены ошибки доступа/тайм-аут; успешной проверки им не присвоено.
- Utrecht показывает access challenge; JVCOG — профессиональный access gate; ANZCVS не раскрывает необходимые материалы без членского доступа.

Anivive восстановлен через актуальный официальный `www.anivive.com/trials`; прежние адреса с HTTP 525 сохранены как fallbacks. Источник остаётся partial из-за сверки текущего статуса SINE-протокола с Cornell. genui{"citation":{"ref":"turn24view0"}}

**GLOBAL NEW-SOURCE DISCOVERY**

Поиск выполнен по всем 12 обязательным регионам, включая свежие объявления, текущие/недатированные страницы, публичные LinkedIn и Perseus/CRUSH leads. Использованы английский, французский, немецкий, испанский, португальский, японский, китайский, корейский, хинди, тайский, иврит, арабский и африкаанс.

| Регион | Результат и ограничения |
|---|---|
| США | Новые источники Ardent и Perseus; Ardent пока UNRESOLVED |
| Канада | Проверены OVC/WCVM; нового подтверждённого предложения не добавлено |
| Великобритания | AI-generated lymphoma sample исключён; RVC недоступен |
| Континентальная Европа | Добавлены Alfort и Oniris; текущий набор их кандидатов не подтверждён |
| Мексика / Центральная Америка / Карибы | Испаноязычный поиск; нового подтверждённого протокола нет, полнота поиска ограничена |
| Южная Америка | Португалоязычные LOCT/Estima leads; текущий набор и точные условия не установлены |
| Австралия / Новая Зеландия | Подтверждён существующий UQ-протокол; Murdoch coming soon не добавлен |
| Восточная Азия | Проверены японские протоколы и совместный PD1 roster; китайский/корейский поиск не дал подтверждённого нового добавления |
| Южная Азия | Английский/хинди; слабая поисковая выдача, отсутствие исследований не доказано |
| Юго-Восточная Азия | Английский/тайский; подтверждённого нового добавления нет |
| Ближний Восток | Иврит/арабский/английский; подтверждённого нового добавления нет |
| Африка | Английский/африкаанс; подтверждённого нового добавления нет |

Все регионы были включены в поиск, но исчерпывающая глобальная сверка не заявляется. Сохранены запросы и найденные URL; точный текст части дополнительных запросов не был сохранён.

**NEW — 0. UPDATE — 3. CLOSE/HIDE — 2.**

- `leah-bcell-cart-2026`: Minnesota переведена из активных площадок в `inactive_sites` по официальному On hold. Missouri уже была приостановлена. Ohio сохранена по координаторскому roster с обязательным подтверждением текущего места; отсутствие в общем индексе не использовано как доказательство закрытия.
- `ill-osa-z007-current`: сверены официальный October 2026 PDF, критерии OSA с лёгочными метастазами, washout, восемь еженедельных введений и распределение расходов после screening.
- `tamu-feline-small-cell-gi-lymphoma-wart`: уточнены новые трудные для медикации и рецидивные случаи, семь дней без химиотерапии/стероидов, радиус поездки до шести часов, график RT и расходы. После включения study costs покрываются; screening и возможное ночное размещение остаются расходами владельца.
- `ethos-rapamycin-cancer` и `case-cosmyc-it` исключены из лечебного подбора по owner-benefit rule в PROJECT_OPERATIONS.md: PK/dose/tolerability/target-engagement research без определённой стандартной лечебной схемы или установленной терапевтической пользы. Записи сохранены; закрытие набора не утверждается.

Дополнительно скрыта **1 площадка** Minnesota; целые записи не удалялись.

**NEW SOURCES — 4**

Ardent K9-ACV checkpoint trial; Alfort innovative trials; Oniris BioceraVet OSA; Perseus clinical-trial discovery. Perseus используется как вторичный источник поиска. Новый источник сам по себе не означает новый matchable trial.

**UNRESOLVED — 4 новых, 1 разрешённый**

Новые: Ohio LEAH institutional confirmation; Ardent K9-ACV/CD200 — 19 площадок, несогласованность Illinois/Peoria и неопубликованные owner costs; UC Davis feline hypophysectomy — будущая дата начала 13 октября и неясная oncology applicability; Alfort TG6002 — недатированный протокол без подтверждения текущего набора. Ardent проверен по официальному источнику, но в подбор не добавлен. genui{"citation":{"ref":"turn20view0"}}

Разрешён прежний TAMU funding/eligibility gap. Общее число открытых записей в существующем unresolved-файле: **20 → 23**; прежние записи вне trial-задачи не пересматривались. Решение Юли для сделанных подтверждённых правок не требуется.

**REJECTED / DUPLICATES**

Не добавлены AI-generated sample, диагностические WCVM исследования, supportive-only Kansas, Murdoch coming soon, Alfort colorectal sampling/завершённый CarboPop PK и Zurich ADAM-12 phase-0 safety research. Дубликаты UQ/PetTrials и CASTR/VRCCO сопоставлены; повторные TAMU gallery cards относятся к одному существующему протоколу. Новых дублей, объединений или удалений — **0**. Полный tally всех отвергнутых discovery-кандидатов не завершён.

**Exact counts before → after**

| Показатель | До → после |
|---|---:|
| Канонические записи / уникальные ID | 299 → 299 |
| Публичный каталог | 163 → 161 |
| Strict treatment | 158 → 156 |
| Treatment access | 5 → 5 |
| Trial source inventory | 78 → 82 |
| Только собаки, strict treatment | 141 → 139 |
| Только кошки, strict treatment | 12 → 12 |
| Собаки и кошки, strict treatment | 5 → 5 |

Strict treatment по странам: США **111 → 109**; без изменения — Япония 8, Швейцария 7, Франция 5, UK 5, Китай 4, Канада 3, Португалия 3, Австралия 3, Италия 2, Бельгия 2, Тайвань 2, Дания 1, Мексика 1, Испания 1. Сумма после: **156**.

**Даты проверки источников**

- Local readback: **PASS, 82/82**.
- Remote-main readback: **PASS, 82/82**; stale/missing/mismatched дат — **0**.
- Дата проверок: 2026-10-05; сохранённые timestamps: **18:33:57.300157–19:29:05.980731 EDT**.
- Для 78 прежних источников сохранены предыдущие и новые даты/timestamps; same-day timestamps изменились. У четырёх новых предыдущие значения отсутствовали.
- Результаты: **31 достаточно проверенный, 46 partial, 5 unreachable**. У недоступных сохранена дата реальной попытки.
- Проверенный remote SHA: `3da5c0caa899339baa2dbc7a05f86d83c3db965f`.
- Immutable receipt сохранён отдельно; remote receipt совпал с локальными данными. Последующий файл readback содержит результат проверки публикации.

**Проверки и публикация**

Sanitation, schema, semantic duplicate audit, matcher, build, source inventory и production-sync — **PASS**. Sanitation: 6 известных неполных записей, новых — 0. `python scripts/validate_audit_receipt.py` — **INCOMPLETE: 51 coverage gap, 0 integrity errors**. Это запрещает объявлять аудит завершённым. Ancillary Streamlit-check — INCONCLUSIVE из-за отсутствия модуля; основные проверки прошли.

Подтверждённые данные и metadata опубликованы напрямую в main через GitHub-коннектор: обычный `git push` не имел авторизации. Последний catalog commit — `27e1cdb4ca62a7a8da221da306f9c990bd27a5ed`; metadata commit — указанный выше `3da5c0c…`. [Deploy каталога — SUCCESS](https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/37389081051). Production проверен в **19:35:23 EDT**: HTTP 200, все **161** записи полностью совпадают с текущей сборкой, включая TAMU и два исключения.

Изменены `data/trials_base.json`, `data/source_inventory.json`, `data/audit_unresolved.json`, `data/audit_source_coverage.json`, `data/audit_state.json`, `scripts/test_matcher_logic.js`, `seo/static/matcher/trials.json` и файлы этого запуска.

Checkpoint и очередь остатка сохранены. Один интервал **18:52:20–19:14:30** превысил правило 15 минут; задним числом checkpoint не создавался. Девять промежуточных fetch-записей восстановлены из реально сохранённых ответов с явным указанием времени сохранения ответа; повторного обхода ради дат не было.

[Точный отчёт](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261005T183318-0400/report.md) · [Immutable receipt и все per-source gaps](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261005T183318-0400/receipt.json) · [Remote readback](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261005T183318-0400/remote-readback.json)
