7 октября 2026, 04:01:55–06:00:48 America/New_York  
Режим: DAILY GLOBAL WORK AUDIT

**Результат: 1 новое исследование, 3 исправления, 1 скрытая запись. Изменения опубликованы и проверены на сайте. Общий статус — INCOMPLETE.**

Проверка среды: **PASS**. Реально выполнены `pwd` → `/workspace/scratch/0856bb16a45a`, `python --version` → Python 3.12.14, `git --version` → Git 2.51.1.

**1. Новые исследования — 1**

**Персональная RNA-вакцина против глиомы — University of Florida, Gainesville, США.** Только собаки породы боксёр с подозрением на злокачественную глиому по MRI, без предыдущего лечения опухоли. После биопсии из опухолевой RNA готовят вакцину; предусмотрены три введения. Исследование оплачивает биопсию, удаление лимфоузла, связанную анестезию и восстановление, вакцину и исследовательские анализы. Остальные расходы обсуждаются при обследовании; полностью бесплатным лечение не обозначено. [Официальная страница](https://research.vetmed.ufl.edu/research-programs/clinical-trials/neurology-2/autogenic-vaccine-study-in-dogs-with-glioma/). genui{"citation":{"ref":"turn74view0"}}

**2. Что исправлено — 3**

- **SINE/Laverdia + карбоплатин при остеосаркоме:** актуальный центр — Cornell, Ithaca; подтверждён один центр. Обязательна предшествующая ампутация, предыдущая химиотерапия исключает участие. Laverdia предоставляется бесплатно; карбоплатин и анализы покрываются частично, остальные расходы остаются владельцу. [Протокол](https://www.anitrial.com/trial/selective-inhibition-of-nuclear-export-sine-and-canine-osteosarcoma).
- **Cornell, траметиниб при плоскоклеточном раке ротовой полости:** исправлен ответственный исследователь — Santiago Peralta вместо контакта другого исследования. [Протокол](https://www.vet.cornell.edu/hospitals/clinical-trials/new-drug-oral-squamous-cell-carcinoma-dogs).
- **UC Davis, флуоресцентная навигация операции на опухолях ротовой полости:** убраны ошибочно включённые саркомы. Текущий протокол принимает собак с оральной меланомой или плоскоклеточным раком. [Протокол](https://studypages.com/s/fluorescence-imaging-with-pdl1-irdye800-to-guide-surgical-treatment-of-oral-cancer-in-dogs-679907/).

**3. Закрыто или скрыто**

Закрыто: **0**. Скрыто из treatment-matcher: **1** — UF, исследование устойчивости мастоцитомы к тоцеранибу. Оно набирает участников для анализа образцов и биомаркеров; обычное лечение оплачивает владелец. Это не подтверждённая программа финансируемого противоопухолевого лечения, поэтому запись переклассифицирована в observational. genui{"citation":{"ref":"turn74view2"}}

**4. Новые источники — 6**

Cornell COOL; UF Neurology; LEAH Labs; Oklahoma State Clinical Trials; VSSO Open Research Trials; Veterinary Oncology Services. Последние источники сохранены и при отсутствии подтверждённого лечения или недоступности сайта.

**5. Поиск и охват**

Фактически предприняты проверки **91 исходного и 6 новых источников — 97/97**. Все обязательные inventory fallback при недостаточном master посещены. Это число попыток, а не число успешно сверенных источников.

Разобраны 62 recruiting oncology-записи AVMA, 106 leads VetTrials, 14 oncology-карточек собак/кошек UC Davis и все 41 ресурсная ссылка VCS.

Глобальный поиск: **40 запросов плюс адресные уточнения**, все 12 регионов — США, Канада, Великобритания, континентальная Европа, Мексика/Центральная Америка/Карибы, Южная Америка, Австралия/Новая Зеландия, Восточная Азия, Южная Азия, Юго-Восточная Азия, Ближний Восток, Африка. Использованы английский, испанский, португальский, французский, немецкий, итальянский, японский, китайский, корейский, хинди, тайский, индонезийский, иврит, турецкий и арабский.

**6. Что осталось нерешённым**

| Охват источника | Число |
|---|---:|
| Fully reconciled — полностью сверено | 42 |
| Partial — частичная сверка | 47 |
| Unreachable — недоступно | 8 |
| Not checked — не посещено | 0 |

Недоступные источники: MSU, RVC, WSU, NCI, Veterinary Cancer Care, Ethos Clinical Studies, Utrecht и Veterinary Oncology Services. Причины — 403, 404, 502 или защитная страница; официальные fallback не обеспечили достаточный roster.

У частичных источников остаются неопубликованные критерии, расходы или подтверждение набора. Например, LEAH объявляет открытый набор, а Minnesota/Missouri указывают паузу; два старых протокола UC Davis не отдают клинические детали. Отдельно **не доведена до полной сверки активации и условий каждого центра** часть общих программ FAP CAR-T, EGFR/HER2, COTC033 и Ethos. Это оставшаяся работа исполнителя; не обозначаю её словами «маршруты исчерпаны».

UNRESOLVED: AVMA — 8 leads; VetTrials — 3. Эти наборы могут пересекаться. REJECTED: AVMA — 1 diagnostic-only; VetTrials — 16 вне scope или без текущего набора. Уже существующие записи: 52 в AVMA и 87 в VetTrials; второй раз не добавлены. Выполненных объединений/удалений дублей — **0**. Новых дублей опубликовано **0**. Очередь остатка сохранена; продолжение не объявляю запущенным. Ручных действий Юли сейчас не требуется.

**7. Каталог до → после**

| Показатель | До | После |
|---|---:|---:|
| Canonical records | 301 | 302 |
| Public matchable | 163 | 163 |
| Treatment trials | 158 | 158 |
| Other treatment access | 5 | 5 |
| Trial sources | 91 | 97 |

**8. Технический результат**

Sanitation, schema, проверка дублей, matcher, сборка и production-sync — **PASS**. Receipt validator — **INCOMPLETE: 55 пробелов охвата, 0 ошибок evidence/date integrity**. В deploy исправлена устаревшая проверка удалённого профиля Anivive; после исправления сборка и публикация прошли.

Клинические изменения: commit `f528ca8`. Проверенный remote main: `4c15428e590fc498c4e6b45ba224952b03748204`. [Deploy — PASS](https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/37604077769). Production — **PASS**: каталог из 163 записей, matcher.js и страница matcher совпали с собранными файлами.

Изменённые файлы: `data/trials_base.json`, `data/source_inventory.json`, `data/audit_source_coverage.json`, `data/audit_state.json`, `seo/static/matcher/trials.json`, `scripts/test_matcher_logic.js`, `.github/workflows/deploy-static-site.yml` и артефакты текущего run.

**Даты проверки источников:** у 91 прежнего источника 06.10 → 07.10; у 6 новых — отсутствовала → 07.10. Фактические сохранённые timestamps: **04:02:34–05:52:47 EDT**; previous/new timestamps каждого источника сохранены отдельно. Local readback **97/97 PASS**, remote-main readback **97/97 PASS** на SHA `4c15428e590fc498c4e6b45ba224952b03748204`; устаревших, отсутствующих или несовпавших дат **0**. Свежая дата недоступного источника означает попытку, а не успешную сверку.

**Общий статус: INCOMPLETE. Подтверждённые изменения опубликованы; полный обязательный охват не достигнут.**

Run: `daily-20261007T040155-0400`. [Receipt](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261007T040155-0400/receipt-final.json) · [Остаток работы](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/main/research/audit-runs/daily-20261007T040155-0400/pending-queue-final-02.json) · [Отчёт](sandbox:/workspace/scratch/0856bb16a45a/vet-trial-matcher/research/audit-runs/daily-20261007T040155-0400/report.md)
