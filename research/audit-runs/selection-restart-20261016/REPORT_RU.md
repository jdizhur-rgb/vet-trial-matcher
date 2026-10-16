# Повторная проверка выдачи — 16 октября 2026

**Полная повторная верификация НЕ завершена.** Рассмотрены156 публичных записей; для116 заново составлены проверки по свежеполученным первичным материалам. У40 остаются конкретные пробелы. Это не118 полностью доказанных медицинских допусков и не новый полный аудит набора.

Внесены49 подтверждённых исправлений канонических записей. Исправления охватывают ложные совпадения и ошибочное скрытие подходящих пациентов. Статусы, финансирование, статьи, навигация и CSS не менялись.

Ключевые исправления: AML вместо любого лейкоза; только оральный SCC в Zurich FLASH; пропущенные обязательные облучение/химиотерапия/операции; строгие границы возраста и веса; критерии двух Penn OSA-когорт; послеоперационный доступ Tufts HSA,NVLU vaccine и Vaxleukin; молекулярная/МРТ/клиническая диагностика вместо ошибочного универсального требования предварительной патологии.

Код теперь учитывает структурированное поле treatments при фильтрации предпочтений. Предшествующая операция может удовлетворять хирургическому стандартному лечению, когда это прямо допускает источник. Исключение MedVet для длиннокостной OSA не распространяется на неподтверждённый рак мочевого пузыря или осевую OSA.

Базовая таксономия и все широкие диагностические группы не переписывались по названию опухоли. Текущий Tokyo протокол полимерного пирарубицина прямо перечисляет ХС; эту возможность нельзя убрать как случайное широкое совпадение. Tufts Z007 требует отдельного решения по ХС.

## Контроль качества

До изменений прежние тесты проходили, хотя перечисленные ошибки воспроизводились. Исходная база:310 канонических/156 публичных записей,58 сохранённых независимых reviews. После исправлений:135 сохранённых reviews,134 относятся к текущей публичной базе,116 обновлены в этом проходе. Полный свежий gate остаётся FAIL из-за40 записей; обычный regression PASS не заменяет этот результат.

## Даты проверки источников

Нативный план:202 URL, фактических запросов201,146 полученных ответов,55 ошибок,1 унаследованный запрет без запроса. Время фактических сохранённых попыток UTC: 2026-10-16T18:59:47.653454+00:00 — 2026-10-16T19:20:45.417676+00:00. Web-чтения записаны отдельно с точностью до даты, без выдуманного времени. Это проверка протоколов; даты глобального source inventory не обновлялись и не представлены как новый полный обход111 источников. Полный payload и посторонняя конфигурация сайтов не публикуются.

## Нерешённые40 записей

| Запись | Что осталось подтвердить |
|---|---|
| [eu-fr-hifu-urothelial](https://www.anicura.fr/cliniques/armonia/etudes-cliniques-en-cours-chv-anicura-armonia/) | Прямой протокол Armonia вернул403. Европейский список подтверждает диагноз/метод, но не полный актуальный набор критериев. |
| [eu-fr-oral-intratumoral-immunotherapy](https://www.vetagro-sup.fr/recherche-expertise/cicv-centre-investigation-clinique-veterinaire/etude-pour-developper-un-nouveau-medicament-pour-traiter-les-melanomes-et-carcinomes-epidermoides-buccaux/) | Свежая страница VetAgro подтверждает оральную меланому/SCC и доступ к лечению, но не публикует все сохранённые числовые ограничения и исключения. Нужен полный протокол/документ организатора. |
| [uk-edinburgh-oral-melanoma-tigilanol-tiglate](https://www.esvonc.com/clinical_trials/ongoing_eu_clinical_trials) | ESVONC больше не перечисляет эту запись. Официальная новость2024 и конференционная работа2026 подтверждают исследование, но не текущий приём и полный протокол. Не объявлять закрытым по отсутствию. |
| [ncsu-mammary-inspire](https://cvm.ncsu.edu/clinical-trial/inspire-therapy-for-canine-mammary-carcinoma/) | NCSU текущий онкологический индекс подтверждает INSPIRE и размеры1–3см; прямой протокол и листовка403. Остальные условия не удалось заново подтвердить. |
| [uga-bcell-ivp](https://vet.uga.edu/clinical-trial/dogs-diagnosed-with-b-cell-lymphoma/) | UGA прямой протокол403; клинический индекс не заменяет полного протокола BI705564 и местных условий набора. |
| [wsu-sts-local-immunotherapy](https://vrcvet.com/clinical-trials/) | VRCCO403; регистровый TCE-протокол получен, но клинические ограничения текущего VRCCO-когортного набора и статус WSU нельзя объединять без подтверждения. |
| [ethos-gilvetmab-melanoma](https://www.ethosvet.com/clinical-study/melanoma-treatment-study/) | Прямая страница Ethos403. Обход запрета не предпринимался; свежего полного протокола нет. |
| [ethos-bcell-oral](https://www.ethosvet.com/clinical-study/canine-b-cell-lymphoma-study/) | Прямая страница Ethos403. Похожая старая запись B-cell в AVMA не подтверждает идентичность текущего перорального препарата. |
| [ethos-osa-vaccine](https://www.ethosvet.com/clinical-study/osteosarcoma-vaccine-study/) | Прямая страница Ethos403. Свежего полного протокола вакцины и местного набора нет. |
| [tamu-mct-acid-suppressant](https://vetmed.tamu.edu/gilab/research/studies/) | Основной протокол TAMU GI Lab403. Условия резектабельного MCT и финансирования сохранены без новой даты подтверждения. |
| [mizzou-osa-carboplatin-timing](https://vhc.missouri.edu/small-animal-hospital/oncology/clinical-trials/current-clinical-trials/) | Свежая страница Missouri не содержит этого протокола и не даёт его критериев. Отсутствие само по себе не является закрытием; нужен прямой текущий протокол/ответ центра. |
| [mizzou-epitheliotropic-laverdia](https://vhc.missouri.edu/small-animal-hospital/oncology/clinical-trials/current-clinical-trials/) | Свежая страница Missouri не содержит Laverdia-когорту; AVMA показывает Completed для похожей/исторической записи. Нужна точная сверка текущей фазы, нельзя закрывать новую фазу по старой записи. |
| [ethos-solid-relapse](https://www.ethosdiscovery.org/clinical-study/stratification-of-outcomes-for-lymphoma-in-dogs-with-relapsed-lymphoma-solid-relapse/) | Прямая страница SOLID-RELAPSE и все сохранённые официальные маршруты Ethos Discovery403. Требуются актуальные правила relapse/refractory и предыдущего лечения. |
| [ethos-epush-hsa](https://www.ethosdiscovery.org/clinical-study/ethos-precision-medicine-umbrella-study-for-hemangiosarcoma-epush/) | AVMA Ethos-PUSH получен, но его предоперационная когорта с гемоперитонеумом не доказывает актуальные условия нынешней фазы. Прямой спонсорский протокол403. |
| [ethos-mimic-osa-lung](https://www.ethosdiscovery.org/clinical-study/minimally-invasive-metastasectomy-in-canines-mimic-2/) | AVMA MIMIC получен, но более общий протокол не устанавливает идентичность нынешней MIMIC2-когорты. Нельзя автоматически переносить диагнозы/ограничения между фазами. |
| [elias-eci-chemo-osa](https://eliasanimalhealth.com/clinical-studies/eci-combined-with-chemotherapy/) | Текущий прямой ELIAS ECI+chemotherapy протокол403. Не смешивать с закрытым ECIP-OSA-01 или коммерческим ECI. |
| [anivive-sine-osa-carboplatin](https://www.anitrial.com/trial/selective-inhibition-of-nuclear-export-sine-and-canine-osteosarcoma) | Прямая страница Anitrial SINE+carboplatin403. Свежего полного протокола нет. |
| [uk-ndsr-osa-rfil2-watch](https://www.ndsr.co.uk/information-sheets/osteosarcoma-2/) | NDSR osteosarcoma protocol403. Нет свежего полного подтверждения rFeIL2 и условий стандартного лечения. |
| [eu-uk-ndsr-high-grade-mammary-current](https://www.ndsr.co.uk/insights/canine-mammary-cancer/) | NDSR403; индексированный официальный текст подтверждает исследование high-grade mammary carcinoma, но не полный протокол/текущие условия. |
| [ca-ovc-oral-melanoma-palladia](https://ovcclinicaltrials.uoguelph.ca/evaluating-palladia-for-the-treatment-of-canine-oral-melanoma/) | OVC прямой Palladia протокол502 через shell и Web; сохранённый независимый review относится к утреннему проходу, а не к этому повторному запуску. Полный свежий текст не получен. |
| [ca-ovc-osa-hifu](https://ovcclinicaltrials.uoguelph.ca/evaluating-a-non-invasive-heat-therapy-for-the-treatment-of-bone-cancer-in-dogs-2/) | OVC прямой distal-radius HIFU протокол502 через shell и Web; утренний source-derived review не засчитан как новая проверка в этом запуске. |
| [ca-ovc-feline-oscc-porphysome-pdt](https://ovcclinicaltrials.uoguelph.ca/all-active-feline-clinical-trials-onco/) | OVC протокол и все актуальные общие страницы502, включая Web. Не удалось заново прочитать Porphysome/PDT критерии. |
| [ncsu-canine-sts-xcsgel](https://cvm.ncsu.edu/clinical-trial/now-recruiting-dogs-with-soft-tissue-sarcoma/) | Свежий NCSU индекс подтверждает XCSgel+облучение+операцию; прямой протокол403, все дополнительные критерии заново не подтверждены. |
| [ncsu-feline-oral-pivot-c](https://cvm.ncsu.edu/clinical-trial/pivot-c-pilot-intratumoral-vaccine-therapy-for-oral-tumors-in-cats/) | Свежий NCSU индекс подтверждает PIVOT-C и характер вмешательства; прямой протокол403, точные диагнозы/ограничения требуют полного текста. |
| [umn-feline-mammary-olaparib-meloxicam](https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/olaparib) | UMN протокол, текущий индекс, taxonomy и свежая официальная статья403. Найденный AVMA Mammary tumors in cats относится к OSU и отклонён как другой протокол. |
| [penn-flash-rt-extremity-sts](https://www.vet.upenn.edu/clinical-trial/evaluation-of-proton-flash-rt-in-naturally-occurring-canine-extremity-sarcoma/) | Прямой Penn FLASH-STS протокол и все официальные сохранённые индексы403. Нет свежей проверки локализации/гистологии/размеров. |
| [umn-canine-oral-melanoma-aav-vaccine](https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/new-vaccine) | UMN текущий клинический индекс и конкретная страница403; текущая AAV-вакцинная когорта не перечитана. |
| [ch-anicura-aoi-superficial-tumor-immunocytokines](https://www.anicura.ch/standorte/aoi/onkologie/weitere-therapien/) | Прямая AOI immunocytokine страница403. Нельзя считать подтверждённым допуск каждой гистологии только из поверхностной локализации. |
| [aurelius-lytix-bcell-lymphoma](https://aureliusbio.com/) | Aurelius403. Похожая AVMA инъекционная B-cell программа не идентифицирована как LTX315 и отклонена как источник текущих критериев. |
| [china-petcura-personalized-mrna-iit-2026](https://www.petcura.cn/zh/mrna-vaccine/study/) | PETcura прямой протокол403. Старый развёрнутый список диагнозов и исключения сохранены, но не представлены как заново проверенные. |
| [jhu-cigat-osa-cryo-immunotherapy-2026](https://www.hopkinsmedicine.org/radiology/veterinarians/clinical-trials) | JHU прямой индекс, VCTN и доступная сохранённая листовка403. Не удалось заново прочитать OSA cryo-immunotherapy. |
| [jhu-cigat-brain-rt-tmz-2026](https://www.hopkinsmedicine.org/radiology/veterinarians/clinical-trials) | JHU индекс/VCTN403. Нет свежего полного протокола glioma RT/TMZ. |
| [jhu-cigat-mammary-kubanda-cryo-2026](https://www.hopkinsmedicine.org/radiology/veterinarians/clinical-trials) | JHU индекс/VCTN/листовка403; старая AVMA Kubanda запись Completed не устанавливает текущую фазу нынешнего клинического доступа. |
| [mexico-ensenada-silver-nanoparticle-cancer-2026](https://zonanorte.mx/main/mozaico/nid/8542) | Единственный материал с доступом — новостная статья. Патент/лабораторные работы не устанавливают современный клинический протокол и допуск всех диагнозов. Нужен первичный протокол клиники/организатора. |
| [penn-anti-pd1-urothelial-carcinoma](https://www.vet.upenn.edu/research/research-programs/comparative-immunotherapy-program/clinical-trials/) | Penn CIP и все доступные сохранённые официальные маршруты403. Полный современный antiPD1 bladder протокол не подтверждён. |
| [umn-orbit-lymphoma](https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/orbit-vsv) | UMN ORBIT/VSV прямой протокол и индекс403. Нет свежей проверки агрессивной лимфомы/когорт и предыдущего лечения. |
| [penn-atherton-steap1-car-t-hs](https://www.vet.upenn.edu/research/research-laboratories/atherton-laboratory/) | Penn Atherton и другие индексы403. Пилотный STEAP1 HS набор и остаток мест заново не подтверждены. |
| [mizzou-vinorelbine-insulinoma](https://vhc.missouri.edu/small-animal-hospital/oncology/clinical-trials/current-clinical-trials/) | Свежий Missouri индекс не содержит vinorelbine-insulinoma; AVMA Completed может относиться к старой фазе. Нужна точная идентичность/текущий прямой протокол. |
| [au-melbourne-hsa-autologous-vaccine-multicenter](https://medipaws.com.au/clinical-research/dogs-with-splenic-haemangiosarcoma) | MediPaws403; найденный индексированный материал подтверждает UMelbourne35274 как проект, но не заменяет перечитанного текущего протокола набора. |
| [penn-glioma-flash-gilvetmab-2026](https://www.vet.upenn.edu/clinical-trial/flash-based-radioimmunotherapy-in-canine-glioma/) | Прямой Penn glioma FLASH/gilvetmab протокол и сохранённые индексы403. Полные современные ограничения не перечитаны. |

## Отдельные решения владельца

1. MSU quasiorganelle: первичный источник описывает первое исследование безопасности/режима дозирования у собак с естественным раком. Исключение для CMP002 на него не распространяется автоматически.
2. Mexico silver nanoparticles: временно скрыть до первичного клинического протокола, без маркировки «закрыто»?
3. Tufts Z007: требуется подтверждение клиники по ХС; общая группа сарком не является прямым подтверждением этого диагноза.
4. Penn B-cell CAR-T: текущий AVMA Suspended при недоступной странице учреждения; нужен текущий статус.
5. Текст причины для Other treatment-access opportunity: заменить неверное обещание funded/assisted на нейтральное описание доступа и отдельные расходы. Подготовленный точный before/after находится в owner-decisions.json; в публичный текст не внесён.

Полные дельты: verified-changes.json. Покарточный учёт: review-ledger.json. Подтверждение публикации будет записано отдельно после успешного deploy и сравнения production.

Утренние reviews OVC на той же календарной дате не засчитаны как новая проверка. Все прежние клинические regression cases сохранены; один MSU MCT case документированно заменён из-за семидневного washout, с явным новым тестом и superseded-cases.json. Итоговые независимые cases:604.
