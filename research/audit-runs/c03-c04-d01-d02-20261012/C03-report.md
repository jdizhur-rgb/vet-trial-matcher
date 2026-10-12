# C03 — проверка 25 филиалов Vet Trial Finder

Проверено 12 октября 2026. Это завершённая проверка назначенного пакета с сохранёнными неопределённостями, не национальный аудит сети. Все 25 филиалов сохранены. Общие файлы базы не изменены; коммитов, публикации и обращений в клиники не было.

Прочитаны актуальные AGENTS.md и PROJECT_OPERATIONS.md через GitHub. Найдены все 25 source IDs в inventory (`id` — фактическое имя ключа). В supplemental найдены 23 карточки; Northwest и PetCare East получены из `data/oncology_centers.json`. Исходные значения доступны; отсутствующие новые поля явно отмечены в JSON.

## Принятые решения

- Убрать неподтверждённую химиотерапию только из confirmed services у Highlands, Pahle, Roswell и Rutherford, сохранив клиники и вопросы. У Roswell/Highlands есть историческое вторичное положительное свидетельство, у Rutherford — агрегатор; это не доказательство отсутствия лечения.
- Добавить иммунотерапию Loomis Basin, Los Angeles Veterinary Specialists и Palm Beach из местных списков услуг; не присваивать конкретный препарат.
- Добавить ONCEPT MidWest; PetCare East — химиотерапию, иммунотерапию и ONCEPT.
- Northwest — химиотерапия, иммунотерапия, surgical oncology, radiation oncology/therapy, IMRT и SRT; подтверждение оборудования и квалификации приведено отдельно.
- Palm Beach — сохранить radiation oncology, добавить местную radiation therapy/IMRT; оборудование Varian 2100 EX. SRT не установлена.
- Rutherford — отдельная криохирургия кожных опухолей, ограниченная размером; не специализированная surgical oncology.
- Сохранить chemotherapy Metzger по совокупности официальной oncology услуги и описанного Penn State clinical case. Mountain View RT оставить как published-but-local-delivery-unconfirmed.
- Добавить отдельно доказательства нынешних oncology clinicians для пяти specialty филиалов, исправить основные service verification URLs Northwest/PetCare и HTTPS Northwest.

Уверенность: high — конкретное локальное описание/оборудование/квалификация; medium-high — опубликованная ветка услуги без конкретной схемы; medium — обоснованный вывод из косвенного случая. Низкая/историческая достаточность не становится подтверждённой услугой.

Общие ограничения: актуальная web-страница с нормальными часами — свидетельство работы, не независимая проверка лицензии или фактического расписания. Значок myVCA live chat не означает oncology teleconsultation. Фраза о недоступности online booking — не закрытие филиала. Общие FAQ о surgery/radiation/immunotherapy не используются как местное подтверждение. Отсутствие названного онколога не подавляет подтверждённую chemotherapy.

## Все назначенные записи

### 1. VCA Highlands Animal Hospital

`vca-highlands-animal-hospital`

Адрес: 25011 Lee Highway, Abingdon, VA 24211. Телефон: 276-628-4115. Официальный сайт: https://vcahospitals.com/highlands-va. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/highlands-va); фактическая проверка 2026-10-12T22:28:53.226573+00:00.

Принятый подтверждённый список: Local oncology care.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Joanne Davenport Veterinarian](https://vcahospitals.com/highlands-va/team/joanne-davenport).
- [Julie Dunnivant-Hahn Veterinarian](https://vcahospitals.com/highlands-va/team/julie-dunnivant-hahn).
- [John Graham Veterinarian](https://vcahospitals.com/highlands-va/team/john-graham).
- [Ben Haderer Veterinarian DVM](https://vcahospitals.com/highlands-va/team/ben-haderer).
- [Jay Hendley Veterinarian DVM](https://vcahospitals.com/highlands-va/team/jay-hendley).
- [Elizabeth Lewis-Graham Veterinarian](https://vcahospitals.com/highlands-va/team/elizabeth-lewis-graham).
- [Sarah Tidwell Veterinarian DVM](https://vcahospitals.com/highlands-va/team/sarah-tidwell).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-your-visit](https://vcahospitals.com/highlands-va/everyday-care/your-visit) — 2026-10-12T22:31:47.651407+00:00; HTTP 200.
- [home](https://vcahospitals.com/highlands-va/) — 2026-10-12T22:28:53.226573+00:00; HTTP 200.
- [service](https://vcahospitals.com/highlands-va/services/advanced-care/oncology) — 2026-10-12T22:28:53.227709+00:00; HTTP 200.
- [services](https://vcahospitals.com/highlands-va/services) — 2026-10-12T22:28:53.229065+00:00; HTTP 200.
- [team](https://vcahospitals.com/highlands-va/team) — 2026-10-12T22:28:53.228240+00:00; HTTP 200.

Решения по изменениям:

- `services`: Убрать химиотерапию из подтверждённого списка: текущие официальные Oncology/services/team/биографии не подтверждают конкретную модальность. Это не утверждение, что услугу не выполняют. Уверенность: high for evidence classification; actual absence not established. [Доказательство](https://vcahospitals.com/highlands-va/services/advanced-care/oncology); 2026-10-12T22:28:53.227709+00:00. Короткая цитата: «Oncology».
- `review_flags`: Сохранить конкретные нерешённые вопросы следующему проходу; статусы not confirmed не равны service unavailable. Уверенность: high for unresolved classification. [Доказательство](https://vcahospitals.com/highlands-va/services/advanced-care/oncology); 2026-10-12T22:28:53.227709+00:00. Короткая цитата: «Oncology».

Следующий проход:

- Химиотерапия: не подтверждено. Найти актуальное объявление об её проведении, локальный clinical case или протокол работы филиала; не считать отсутствие онколога отрицательным доказательством.
- Pet Cancer Center включает Abingdon в general-practice chemotherapy list; общий каталог датирован 2019-03-06. Современный официальный branch-level modality proof не найден.

### 2. VCA Jackson Animal Hospital

`vca-jackson-animal-hospital`

Адрес: 902 East Jackson, Medford, OR 97504. Телефон: 541-779-4893. Официальный сайт: https://vcahospitals.com/jackson. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/jackson); фактическая проверка 2026-10-12T22:28:53.230732+00:00.

Принятый подтверждённый список: Chemotherapy.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [David Harder Medical Director DVM](https://vcahospitals.com/jackson/team/david-harder).
- [Allison Schroeder Staff Veterinarian DVM](https://vcahospitals.com/jackson/team/allison-schroeder).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-your-visit](https://vcahospitals.com/jackson/everyday-care/your-visit) — 2026-10-12T22:31:28.822255+00:00; HTTP 200.
- [home](https://vcahospitals.com/jackson/) — 2026-10-12T22:28:53.230732+00:00; HTTP 200.
- [service](https://vcahospitals.com/jackson/services/advanced-care/chemotherapy) — 2026-10-12T22:28:53.231264+00:00; HTTP 200.
- [services](https://vcahospitals.com/jackson/services) — 2026-10-12T22:28:53.233330+00:00; HTTP 200.
- [team](https://vcahospitals.com/jackson/team) — 2026-10-12T22:28:53.231907+00:00; HTTP 200.

Решения по изменениям:

- Изменений не требуется: существующая chemotherapy подтверждена отдельной локальной веткой услуги; нет новых доказательств для специализированной surgery, radiation, ECT или именованного oncology сертификата.

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 3. VCA Knowles Central Animal Hospital

`vca-knowles-central-animal-hospital`

Адрес: 1000 NW 27th Ave, Miami, FL 33125. Телефон: 305-649-1234. Официальный сайт: https://vcahospitals.com/knowles-central. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/knowles-central); фактическая проверка 2026-10-12T22:28:53.236030+00:00.

Принятый подтверждённый список: Chemotherapy.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Dr. Juan Granado Emergency Veterinarian DVM](https://vcahospitals.com/knowles-central/team/juan-granado).
- [Dr. Yamilka Lago Alvarez Medical Director DVM](https://vcahospitals.com/knowles-central/team/yamilka-lago-alvarez).
- [Dr. Martha Moss Emergency Veterinarian DVM](https://vcahospitals.com/knowles-central/team/martha-moss).
- [Dr. Leonardo Ramírez Rubio Associate Veterinarian DVM](https://vcahospitals.com/knowles-central/team/leonardo-ramirez-rubio).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-your-visit](https://vcahospitals.com/knowles-central/everyday-care/your-visit) — 2026-10-12T22:31:54.507241+00:00; HTTP 200.
- [home](https://vcahospitals.com/knowles-central/) — 2026-10-12T22:28:53.236030+00:00; HTTP 200.
- [service](https://vcahospitals.com/knowles-central/services/advanced-care/chemotherapy) — 2026-10-12T22:28:53.238767+00:00; HTTP 200.
- [services](https://vcahospitals.com/knowles-central/services) — 2026-10-12T22:28:53.240468+00:00; HTTP 200.
- [team](https://vcahospitals.com/knowles-central/team) — 2026-10-12T22:28:53.239398+00:00; HTTP 200.

Решения по изменениям:

- Изменений не требуется: существующая chemotherapy подтверждена отдельной локальной веткой услуги; нет новых доказательств для специализированной surgery, radiation, ECT или именованного oncology сертификата.

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 4. VCA Kootenai Animal Hospital

`vca-kootenai-animal-hospital`

Адрес: 1704 E. Seltice Way, Post Falls, ID 83854. Телефон: 208-773-6000. Официальный сайт: https://vcahospitals.com/kootenai. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/kootenai); фактическая проверка 2026-10-12T22:28:59.216564+00:00.

Принятый подтверждённый список: Local oncology care, Chemotherapy.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Randall Gutting Associate Veterinarian DVM](https://vcahospitals.com/kootenai/team/randall-gutting).
- [Kyle Reijm Associate Veterinarian DVM](https://vcahospitals.com/kootenai/team/kyle-reijm).
- [Kevin Rogers Medical Director DVM](https://vcahospitals.com/kootenai/team/kevin-rogers).
- [Hallie Williams Associate Veterinarian DVM](https://vcahospitals.com/kootenai/team/hallie-williams).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-chemotherapy](https://vcahospitals.com/kootenai/services/advanced-care/chemotherapy) — 2026-10-12T22:31:43.181741+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/kootenai/everyday-care/your-visit) — 2026-10-12T22:31:43.202493+00:00; HTTP 200.
- [home](https://vcahospitals.com/kootenai/) — 2026-10-12T22:28:59.216564+00:00; HTTP 200.
- [service](https://vcahospitals.com/kootenai/services/advanced-care/oncology) — 2026-10-12T22:28:59.258590+00:00; HTTP 200.
- [services](https://vcahospitals.com/kootenai/services) — 2026-10-12T22:28:59.572582+00:00; HTTP 200.
- [team](https://vcahospitals.com/kootenai/team) — 2026-10-12T22:28:59.345311+00:00; HTTP 200.

Решения по изменениям:

- Изменений не требуется: существующая chemotherapy подтверждена отдельной локальной веткой услуги; нет новых доказательств для специализированной surgery, radiation, ECT или именованного oncology сертификата.

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 5. VCA Little Falls Animal Hospital

`vca-little-falls-animal-hospital`

Адрес: 418 Main Street, Little Falls, NJ 07424. Телефон: 973-785-8223. Официальный сайт: https://vcahospitals.com/little-falls. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/little-falls); фактическая проверка 2026-10-12T22:28:59.646433+00:00.

Принятый подтверждённый список: Local oncology care, Chemotherapy.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Loredana Briganti Veterinarian DVM](https://vcahospitals.com/little-falls/team/loredana-briganti).
- [Allison Micich Veterinarian BVMS](https://vcahospitals.com/little-falls/team/allison-micich).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-chemotherapy](https://vcahospitals.com/little-falls/services/advanced-care/chemotherapy) — 2026-10-12T22:31:28.823027+00:00; HTTP 200.
- [follow-cryosurgery](https://vcahospitals.com/little-falls/services/advanced-care/cryosurgery) — 2026-10-12T22:31:28.824571+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/little-falls/everyday-care/your-visit) — 2026-10-12T22:31:28.826007+00:00; HTTP 200.
- [home](https://vcahospitals.com/little-falls/) — 2026-10-12T22:28:59.646433+00:00; HTTP 200.
- [service](https://vcahospitals.com/little-falls/services/advanced-care/oncology) — 2026-10-12T22:29:00.300637+00:00; HTTP 200.
- [services](https://vcahospitals.com/little-falls/services) — 2026-10-12T22:29:00.483667+00:00; HTTP 200.
- [team](https://vcahospitals.com/little-falls/team) — 2026-10-12T22:29:00.457332+00:00; HTTP 200.

Решения по изменениям:

- Изменений не требуется: существующая chemotherapy подтверждена отдельной локальной веткой услуги; нет новых доказательств для специализированной surgery, radiation, ECT или именованного oncology сертификата.

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 6. VCA Loomis Basin Veterinary Clinic

`vca-loomis-basin-veterinary-clinic`

Адрес: 3901 Sierra College Blvd., Loomis, CA 95650. Телефон: 916-652-5816. Официальный сайт: https://vcahospitals.com/loomis-basin. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/loomis-basin); фактическая проверка 2026-10-12T22:29:00.768619+00:00.

Принятый подтверждённый список: Medical oncology, Chemotherapy, Immunotherapy.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Abigail Dimock Veterinary Specialist DVM, DACVR](https://vcahospitals.com/loomis-basin/specialty/team/abigail-dimock).
- [Shannon Heidorn Veterinarian Specialist - Surgery DVM, DACVS-SA](https://vcahospitals.com/loomis-basin/specialty/team/shannon-heidorn).
- [Kristen Hutchinson Specialty & Emergency Medical Director, Veterinarian Specialist - Emergency/Critical Care DVM, DACVECC](https://vcahospitals.com/loomis-basin/specialty/team/kristen-hutchinson).
- [Sunny Kao Veterinarian Specialist - Oncology DVM, DACVIM (Oncology)](https://vcahospitals.com/loomis-basin/specialty/team/sunny-kao).
- [Michele Laurenson Veterinary Specialist DVM, DACVR](https://vcahospitals.com/loomis-basin/specialty/team/michele-laurenson).
- [Michael Mazzei Veterinarian Specialist - Internal Medicine DVM, DACVIM (SAIM)](https://vcahospitals.com/loomis-basin/specialty/team/michael-mazzei).
- [Zachary Miller Veterinarian Specialist - Surgery DVM, DACVS-SA](https://vcahospitals.com/loomis-basin/specialty/team/zachary-miller).
- [Jon Stack Veterinarian Specialist - Cardiology DVM, DACVIM (Cardiology)](https://vcahospitals.com/loomis-basin/specialty/team/jon-stack).
- [Laura West Veterinarian Specialist - Internal Medicine DVM, DACVIM (SAIM)](https://vcahospitals.com/loomis-basin/specialty/team/laura-west).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический specialty приём: опубликован referral route — форма направления, передача medical records и запись звонком владельца/лечащего ветеринара. Не считать форму доказательством обязательности направления во всех случаях.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [deep-specialty-departments-oncology](https://vcahospitals.com/loomis-basin/specialty/departments/oncology) — 2026-10-12T22:30:56.295841+00:00; HTTP 200.
- [deep-specialty-services](https://vcahospitals.com/loomis-basin/specialty/services) — 2026-10-12T22:30:56.313130+00:00; попытка: HTTP Error 404: Not Found.
- [deep-specialty-team](https://vcahospitals.com/loomis-basin/specialty/team) — 2026-10-12T22:30:56.278402+00:00; HTTP 200.
- [follow-chemotherapy](https://vcahospitals.com/loomis-basin/specialty/departments/oncology/chemotherapy) — 2026-10-12T22:31:48.019656+00:00; HTTP 200.
- [follow-immunotherapy](https://vcahospitals.com/loomis-basin/specialty/departments/oncology/immunotherapy) — 2026-10-12T22:31:48.035320+00:00; HTTP 200.
- [follow-referral-forms](https://vcahospitals.com/loomis-basin/specialty/for-vets/referral-forms) — 2026-10-12T22:31:48.135714+00:00; HTTP 200.
- [follow-surgery-services-overview](https://vcahospitals.com/loomis-basin/specialty/departments/surgery/surgery-services-overview) — 2026-10-12T22:31:48.111290+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/loomis-basin/everyday-care/your-visit) — 2026-10-12T22:31:58.677376+00:00; HTTP 200.
- [home](https://vcahospitals.com/loomis-basin/) — 2026-10-12T22:29:00.768619+00:00; HTTP 200.
- [service](https://vcahospitals.com/loomis-basin/specialty/departments/oncology) — 2026-10-12T22:29:03.035849+00:00; HTTP 200.
- [services](https://vcahospitals.com/loomis-basin/services) — 2026-10-12T22:29:03.265156+00:00; попытка: HTTP Error 404: Not Found.
- [team](https://vcahospitals.com/loomis-basin/team) — 2026-10-12T22:29:03.217760+00:00; попытка: HTTP Error 404: Not Found.

Решения по изменениям:

- `services`: Добавить иммунотерапию из списка услуг отделения данного филиала. Не приписывать конкретный препарат. Уверенность: medium-high. [Доказательство](https://vcahospitals.com/loomis-basin/specialty/departments/oncology); 2026-10-12T22:29:03.035849+00:00. Короткая цитата: «Immunotherapy».
- `oncology_clinicians`: Сохранить текущих специалистов отдельно от услуг. Residency-trained не означает board-certified; диагностическая радиология не означает radiation oncology. Уверенность: high. [Доказательство](https://vcahospitals.com/loomis-basin/specialty/team); 2026-10-12T22:30:56.278402+00:00. Короткая цитата: «DVM, DACVIM (Oncology)».

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 7. VCA Los Angeles Veterinary Specialists

`vca-los-angeles-veterinary-specialists`

Адрес: 8723 Santa Monica Blvd., Los Angeles, CA 90069. Телефон: 310-659-5287. Официальный сайт: https://vcahospitals.com/los-angeles-veterinary-specialists. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/los-angeles-veterinary-specialists); фактическая проверка 2026-10-12T22:29:03.319961+00:00.

Принятый подтверждённый список: Medical oncology, Chemotherapy, Immunotherapy.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [David Feldman Medical Director DVM, DACVIM](https://vcahospitals.com/los-angeles-veterinary-specialists/team/david-feldman).
- [Whitney Topmiller Veterinarian Specialist - Internal Medicine](https://vcahospitals.com/los-angeles-veterinary-specialists/team/whitney-topmiller).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический specialty приём: опубликован referral route — форма направления, передача medical records и запись звонком владельца/лечащего ветеринара. Не считать форму доказательством обязательности направления во всех случаях.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-chemotherapy](https://vcahospitals.com/los-angeles-veterinary-specialists/departments/oncology/chemotherapy) — 2026-10-12T22:31:43.027226+00:00; HTTP 200.
- [follow-immunotherapy](https://vcahospitals.com/los-angeles-veterinary-specialists/departments/oncology/immunotherapy) — 2026-10-12T22:31:43.032576+00:00; HTTP 200.
- [follow-referral-forms](https://vcahospitals.com/los-angeles-veterinary-specialists/for-vets/referral-forms) — 2026-10-12T22:31:43.051366+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/los-angeles-veterinary-specialists/for-clients/your-visit) — 2026-10-12T22:31:43.064192+00:00; HTTP 200.
- [home](https://vcahospitals.com/los-angeles-veterinary-specialists/) — 2026-10-12T22:29:03.319961+00:00; HTTP 200.
- [service](https://vcahospitals.com/los-angeles-veterinary-specialists/departments/oncology) — 2026-10-12T22:29:03.453239+00:00; HTTP 200.
- [services](https://vcahospitals.com/los-angeles-veterinary-specialists/services) — 2026-10-12T22:29:04.428206+00:00; попытка: HTTP Error 404: Not Found.
- [team](https://vcahospitals.com/los-angeles-veterinary-specialists/team) — 2026-10-12T22:29:03.519055+00:00; HTTP 200.

Решения по изменениям:

- `services`: Добавить иммунотерапию из списка услуг отделения данного филиала. Не приписывать конкретный препарат. Уверенность: medium-high. [Доказательство](https://vcahospitals.com/los-angeles-veterinary-specialists/departments/oncology); 2026-10-12T22:29:03.453239+00:00. Короткая цитата: «Immunotherapy».
- `review_flags`: Сохранить конкретные нерешённые вопросы следующему проходу; статусы not confirmed не равны service unavailable. Уверенность: high for unresolved classification. [Доказательство](https://vcahospitals.com/los-angeles-veterinary-specialists/departments/oncology); 2026-10-12T22:29:03.453239+00:00. Короткая цитата: «Oncology».

Следующий проход:

- Медицинская онкология/химиотерапия опубликованы как услуги отделения; назначенный текущий medical oncologist не установлен. Не превращать интерниста, интерес к онкологии или radiation oncologist в сертификат medical oncology; сохранить услуги.

### 8. VCA Magnolia by the Gulf

`vca-magnolia-by-the-gulf`

Адрес: 19930 Oak Road W., Gulf Shores, AL 36542. Телефон: 251-968-7523. Официальный сайт: https://vcahospitals.com/magnolia-by-the-gulf. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/magnolia-by-the-gulf); фактическая проверка 2026-10-12T22:29:04.486945+00:00.

Принятый подтверждённый список: Local oncology care, Chemotherapy.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Dr. Doralee Donaldson Staff Veterinarian DVM](https://vcahospitals.com/magnolia-by-the-gulf/team/doralee-donaldson).
- [Dr. Jace Driskill Staff Veterinarian DVM](https://vcahospitals.com/magnolia-by-the-gulf/team/jace-driskill).
- [Dr. Amber Kostelansky Staff Veterinarian DVM](https://vcahospitals.com/magnolia-by-the-gulf/team/amber-kostelansky).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-chemotherapy](https://vcahospitals.com/magnolia-by-the-gulf/services/advanced-care/chemotherapy) — 2026-10-12T22:31:54.476225+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/magnolia-by-the-gulf/everyday-care/your-visit) — 2026-10-12T22:31:54.498602+00:00; HTTP 200.
- [home](https://vcahospitals.com/magnolia-by-the-gulf/) — 2026-10-12T22:29:04.486945+00:00; HTTP 200.
- [service](https://vcahospitals.com/magnolia-by-the-gulf/services/advanced-care/oncology) — 2026-10-12T22:29:04.586882+00:00; HTTP 200.
- [services](https://vcahospitals.com/magnolia-by-the-gulf/services) — 2026-10-12T22:29:08.017623+00:00; HTTP 200.
- [team](https://vcahospitals.com/magnolia-by-the-gulf/team) — 2026-10-12T22:29:08.008334+00:00; HTTP 200.

Решения по изменениям:

- Изменений не требуется: существующая chemotherapy подтверждена отдельной локальной веткой услуги; нет новых доказательств для специализированной surgery, radiation, ECT или именованного oncology сертификата.

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 9. VCA McKenzie Animal Hospital

`vca-mckenzie-animal-hospital`

Адрес: 5303 Main Street, Springfield, OR 97478. Телефон: 541-747-3859. Официальный сайт: https://vcahospitals.com/mckenzie-or. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/mckenzie-or); фактическая проверка 2026-10-12T22:29:08.103368+00:00.

Принятый подтверждённый список: Local oncology care, Chemotherapy.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Mary Arpaia Area Medical Director DVM](https://vcahospitals.com/mckenzie-or/team/mary-arpaia).
- [Matthew Fricke Staff Veterinarian DVM, CVA, ANT-C](https://vcahospitals.com/mckenzie-or/team/matthew-fricke).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-chemotherapy](https://vcahospitals.com/mckenzie-or/services/advanced-care/chemotherapy) — 2026-10-12T22:31:43.249840+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/mckenzie-or/everyday-care/your-visit) — 2026-10-12T22:31:43.253220+00:00; HTTP 200.
- [home](https://vcahospitals.com/mckenzie-or/) — 2026-10-12T22:29:08.103368+00:00; HTTP 200.
- [service](https://vcahospitals.com/mckenzie-or/services/advanced-care/oncology) — 2026-10-12T22:29:08.222432+00:00; HTTP 200.
- [services](https://vcahospitals.com/mckenzie-or/services) — 2026-10-12T22:29:08.310647+00:00; HTTP 200.
- [team](https://vcahospitals.com/mckenzie-or/team) — 2026-10-12T22:29:08.273609+00:00; HTTP 200.

Решения по изменениям:

- Изменений не требуется: существующая chemotherapy подтверждена отдельной локальной веткой услуги; нет новых доказательств для специализированной surgery, radiation, ECT или именованного oncology сертификата.

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 10. VCA Metzger Animal Hospital

`vca-metzger-animal-hospital`

Адрес: 1044 Benner Pike, State College, PA 16801. Телефон: 814-237-5333. Официальный сайт: https://vcahospitals.com/metzger. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/metzger); фактическая проверка 2026-10-12T22:29:08.349783+00:00.

Принятый подтверждённый список: Local oncology care, Chemotherapy.

Химиотерапию сохранить: дополнительный источник Penn State от 26 June 2026 описывает лечение пациента с HSA, включая splenectomy/chemotherapy. Вывод средней уверенности: clinical case поддерживает наличие лечения, но не публикует актуальный перечень схем, врача или route введения. Специализированную surgical oncology из одной спленэктомии не выводить.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Jamie Bean Veterinarian DVM](https://vcahospitals.com/metzger/team/jamie-bean).
- [Caitlin Ervine Veterinarian DVM](https://vcahospitals.com/metzger/team/caitlin-ervine).
- [Anne Granite Medical Director DVM](https://vcahospitals.com/metzger/team/anne-granite).
- [John Griffiths Veterinarian DVM](https://vcahospitals.com/metzger/team/john-griffiths).
- [Abigail Henning Veterinarian DVM](https://vcahospitals.com/metzger/team/abigail-henning).
- [Cassandra Janusz Veterinarian DVM](https://vcahospitals.com/metzger/team/cassandra-janusz).
- [Mark Koshko Veterinarian DVM, Diplomate ABVP](https://vcahospitals.com/metzger/team/mark-koshko).
- [Alejandro Martinez Veterinarian DVM](https://vcahospitals.com/metzger/team/alejandro-martinez).
- [Fred Metzger Veterinarian DVM, MRCVS, Diplomate ABVP](https://vcahospitals.com/metzger/team/fred-metzger).
- [Tasha Parks Veterinarian DVM](https://vcahospitals.com/metzger/team/tasha-parks).
- [Kelsey Perlino Veterinarian DVM](https://vcahospitals.com/metzger/team/kelsey-perlino).
- [Robert Rider Veterinarian DVM, CCRT](https://vcahospitals.com/metzger/team/robert-rider).
- [Taylor Wasson Veterinarian DVM](https://vcahospitals.com/metzger/team/taylor-wasson).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-your-visit](https://vcahospitals.com/metzger/everyday-care/your-visit) — 2026-10-12T22:31:28.826344+00:00; HTTP 200.
- [home](https://vcahospitals.com/metzger/) — 2026-10-12T22:29:08.349783+00:00; HTTP 200.
- [service](https://vcahospitals.com/metzger/services/advanced-care/oncology) — 2026-10-12T22:29:08.909420+00:00; HTTP 200.
- [services](https://vcahospitals.com/metzger/services) — 2026-10-12T22:29:09.713991+00:00; HTTP 200.
- [team](https://vcahospitals.com/metzger/team) — 2026-10-12T22:29:09.371909+00:00; HTTP 200.

Решения по изменениям:

- Изменений не требуется: существующая chemotherapy подтверждена отдельной локальной веткой услуги; нет новых доказательств для специализированной surgery, radiation, ECT или именованного oncology сертификата.

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 11. VCA MidWest Veterinary Referral & Emergency Center

`vca-midwest-veterinary-referral-emergency-center`

Адрес: 9706 Mockingbird Drive, Omaha, NE 68127. Телефон: 402-614-9000. Официальный сайт: https://vcahospitals.com/midwest. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/midwest); фактическая проверка 2026-10-12T22:29:12.570643+00:00.

Принятый подтверждённый список: Medical oncology, Chemotherapy, Immunotherapy, ONCEPT.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Christopher G. Byers Veterinarian Specialist - Emergency/Critical Care DVM, DACVECC, DACVIM (SAIM), CVJ](https://vcahospitals.com/midwest/team/christopher-byers).
- [Jessica Clemans Veterinary Specialist - Internal Medicine DVM, DACVIM (SAIM)](https://vcahospitals.com/midwest/team/jessica-clemans).
- [Crystal Cooley Veterinary Specialist - Internal Medicine DVM, MS, DACVIM (SAIM)](https://vcahospitals.com/midwest/team/crystal-cooley).
- [Logan Donaldson Veterinary Specialist - Neurology DVM, DACVIM (Small Animal Neurology)](https://vcahospitals.com/midwest/team/logan-donaldson).
- [Marissa Goodwin Veterinarian DVM (Oncology - Residency Trained)](https://vcahospitals.com/midwest/team/marissa-goodwin).
- [Tomika Haller Emergency Veterinarian DVM, MS](https://vcahospitals.com/midwest/team/tomika-haller).
- [Amey Jones Emergency Veterinarian DVM](https://vcahospitals.com/midwest/team/amey-jones).
- [Chelsea Kennedy Emergency Veterinarian DVM](https://vcahospitals.com/midwest/team/chelsea-kennedy).
- [Abby Jean Leonardi Veterinary Specialist - Oncology DVM, MS, DACVIM (O)](https://vcahospitals.com/midwest/team/abby-jean-leonardi).
- [Michelle Meyer Medical Director/Surgeon DACVS-SA](https://vcahospitals.com/midwest/team/michelle-meyer).
- [Maggie Peitzmeier Emergency Veterinarian DVM, DACVS(LA)](https://vcahospitals.com/midwest/team/maggie-peitzmeier).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический specialty приём: опубликован referral route — форма направления, передача medical records и запись звонком владельца/лечащего ветеринара. Не считать форму доказательством обязательности направления во всех случаях.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-chemotherapy](https://vcahospitals.com/midwest/departments/oncology/chemotherapy) — 2026-10-12T22:31:43.307149+00:00; HTTP 200.
- [follow-immunotherapy](https://vcahospitals.com/midwest/departments/oncology/immunotherapy) — 2026-10-12T22:31:43.876397+00:00; HTTP 200.
- [follow-referral-forms](https://vcahospitals.com/midwest/for-vets/referral-forms) — 2026-10-12T22:31:43.890105+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/midwest/for-clients/your-visit) — 2026-10-12T22:31:47.594478+00:00; HTTP 200.
- [home](https://vcahospitals.com/midwest/) — 2026-10-12T22:29:12.570643+00:00; HTTP 200.
- [service](https://vcahospitals.com/midwest/departments/oncology) — 2026-10-12T22:29:12.710093+00:00; HTTP 200.
- [services](https://vcahospitals.com/midwest/services) — 2026-10-12T22:29:12.933894+00:00; попытка: HTTP Error 404: Not Found.
- [team](https://vcahospitals.com/midwest/team) — 2026-10-12T22:29:12.857180+00:00; HTTP 200.

Решения по изменениям:

- `services`: Доступ ONCEPT заявлен непосредственно для данного отделения. Для PetCare также добавить опубликованную химиотерапию; иммунотерапия подтверждена конкретным ONCEPT. Уверенность: high. [Доказательство](https://vcahospitals.com/midwest/departments/oncology); 2026-10-12T22:29:12.710093+00:00. Короткая цитата: «ONCEPT is available through our hospital’s Oncology Department.».
- `oncology_clinicians`: Сохранить текущих специалистов отдельно от услуг. Residency-trained не означает board-certified; диагностическая радиология не означает radiation oncology. Уверенность: high. [Доказательство](https://vcahospitals.com/midwest/team); 2026-10-12T22:29:12.857180+00:00. Короткая цитата: «DVM (Oncology - Residency Trained)».

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 12. VCA Morris Animal Hospital

`vca-morris-animal-hospital`

Адрес: 1610 Sheridan Drive, Lancaster, OH 43130. Телефон: 740-653-4084. Официальный сайт: https://vcahospitals.com/morris. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/morris); фактическая проверка 2026-10-12T22:29:12.951819+00:00.

Принятый подтверждённый список: Local oncology care, Chemotherapy.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Dr. Susan Barrett Staff Veterinarian DVM](https://vcahospitals.com/morris/team/susan-barrett).
- [Dr. Alexa Bockelman Staff Veterinarian DVM](https://vcahospitals.com/morris/team/alexa-bockelman).
- [Dr. Lauren Elsea Medical Director DVM](https://vcahospitals.com/morris/team/lauren-elsea).
- [Dr. Rachel Labby Staff Veterinarian DVM](https://vcahospitals.com/morris/team/rachel-labby).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-chemotherapy](https://vcahospitals.com/morris/services/advanced-care/chemotherapy) — 2026-10-12T22:31:54.399057+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/morris/everyday-care/your-visit) — 2026-10-12T22:31:54.434827+00:00; HTTP 200.
- [home](https://vcahospitals.com/morris/) — 2026-10-12T22:29:12.951819+00:00; HTTP 200.
- [service](https://vcahospitals.com/morris/services/advanced-care/oncology) — 2026-10-12T22:29:13.009351+00:00; HTTP 200.
- [services](https://vcahospitals.com/morris/services) — 2026-10-12T22:29:13.372326+00:00; HTTP 200.
- [team](https://vcahospitals.com/morris/team) — 2026-10-12T22:29:13.023297+00:00; HTTP 200.

Решения по изменениям:

- Изменений не требуется: существующая chemotherapy подтверждена отдельной локальной веткой услуги; нет новых доказательств для специализированной surgery, radiation, ECT или именованного oncology сертификата.

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 13. VCA Mountain View Animal Hospital

`vca-mountain-view-animal-hospital`

Адрес: 9414 South Indian Ridge Drive, Sandy, UT 84092. Телефон: 801-523-1176. Официальный сайт: https://vcahospitals.com/mountain-view-ut. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/mountain-view-ut); фактическая проверка 2026-10-12T22:29:13.933908+00:00.

Принятый подтверждённый список: Local oncology care, Chemotherapy.

Химиотерапию сохранить по отдельной услуге. Radiation Therapy прямо заявлена филиалом, но общая страница не устанавливает местное оборудование/лечебную площадку. Не добавлять в подтверждённый местный RT-фильтр; не объявлять отсутствующей. Radioiodine при гипертиреозе не подтверждает противоопухолевое внешнее облучение.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Derek Hagan Staff Veterinarian DVM](https://vcahospitals.com/mountain-view-ut/team/derek-hagan).
- [Timothy Kirkland Medical Director DVM](https://vcahospitals.com/mountain-view-ut/team/timothy-kirkland).
- [Jessica Nielsen Staff Veterinarian DVM](https://vcahospitals.com/mountain-view-ut/team/jessica-nielsen).
- [Kelly Wiszynski Staff Veterinarian DVM](https://vcahospitals.com/mountain-view-ut/team/kelly-wiszynski).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-chemotherapy](https://vcahospitals.com/mountain-view-ut/services/advanced-care/chemotherapy) — 2026-10-12T22:31:47.728870+00:00; HTTP 200.
- [follow-radiation-therapy](https://vcahospitals.com/mountain-view-ut/services/advanced-care/radiation-therapy) — 2026-10-12T22:31:47.742096+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/mountain-view-ut/everyday-care/your-visit) — 2026-10-12T22:31:47.757488+00:00; HTTP 200.
- [home](https://vcahospitals.com/mountain-view-ut/) — 2026-10-12T22:29:13.933908+00:00; HTTP 200.
- [service](https://vcahospitals.com/mountain-view-ut/services/advanced-care/oncology) — 2026-10-12T22:29:14.157434+00:00; HTTP 200.
- [services](https://vcahospitals.com/mountain-view-ut/services) — 2026-10-12T22:29:17.429566+00:00; HTTP 200.
- [team](https://vcahospitals.com/mountain-view-ut/team) — 2026-10-12T22:29:16.966636+00:00; HTTP 200.

Решения по изменениям:

- `review_flags`: Сохранить конкретные нерешённые вопросы следующему проходу; статусы not confirmed не равны service unavailable. Уверенность: high for unresolved classification. [Доказательство](https://vcahospitals.com/mountain-view-ut/services/advanced-care/oncology); 2026-10-12T22:29:14.157434+00:00. Короткая цитата: «Oncology».

Следующий проход:

- Radiation Therapy: филиал пишет «Our hospital offers Radiation Therapy as part of our Oncology Services.» Место фактического облучения, установка и лечащий radiation oncologist не установлены. Проверить локальное оборудование/partner route.

### 14. VCA Mueller Pet Medical Center

`vca-mueller-pet-medical-center`

Адрес: 7625 Freeport Blvd., Sacramento, CA 95832. Телефон: 916-428-9202. Официальный сайт: https://vcahospitals.com/mueller. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/mueller); фактическая проверка 2026-10-12T22:29:17.454681+00:00.

Принятый подтверждённый список: Chemotherapy.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Brian Charn Staff Veterinarian DVM](https://vcahospitals.com/mueller/team/brian-charn).
- [Moira Goldie Staff Veterinarian BVSc](https://vcahospitals.com/mueller/team/moira-goldie).
- [Rebecca Harris Staff Veterinarian DVM](https://vcahospitals.com/mueller/team/rebecca-harris).
- [Quincy Kahn Assistant Medical Director DVM](https://vcahospitals.com/mueller/team/quincy-kahn).
- [Martha Klein Medical Director DVM](https://vcahospitals.com/mueller/team/martha-klein).
- [Bailey Krostoski Staff Veterinarian DVM](https://vcahospitals.com/mueller/team/bailey-krostoski).
- [Keidy Lisac Staff Veterinarian DVM](https://vcahospitals.com/mueller/team/keidy-lisac).
- [Jenna Ogden Staff Veterinarian DVM](https://vcahospitals.com/mueller/team/jenna-ogden).
- [Michael Reget Staff Veterinarian DVM](https://vcahospitals.com/mueller/team/michael-reget).
- [Andrew Sun Staff Veterinarian DVM](https://vcahospitals.com/mueller/team/andrew-sun).
- [Melissa Thurston Staff Veterinarian DVM](https://vcahospitals.com/mueller/team/melissa-thurston).
- [Julie White Staff Veterinarian DVM](https://vcahospitals.com/mueller/team/julie-white).
- [Brooke Zuidervaart Staff Veterinarian DVM](https://vcahospitals.com/mueller/team/brooke-zuidervaart).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-your-visit](https://vcahospitals.com/mueller/everyday-care/your-visit) — 2026-10-12T22:31:43.108199+00:00; HTTP 200.
- [home](https://vcahospitals.com/mueller/) — 2026-10-12T22:29:17.454681+00:00; HTTP 200.
- [service](https://vcahospitals.com/mueller/services/advanced-care/chemotherapy) — 2026-10-12T22:29:17.580372+00:00; HTTP 200.
- [services](https://vcahospitals.com/mueller/services) — 2026-10-12T22:29:17.740956+00:00; HTTP 200.
- [team](https://vcahospitals.com/mueller/team) — 2026-10-12T22:29:17.668617+00:00; HTTP 200.

Решения по изменениям:

- Изменений не требуется: существующая chemotherapy подтверждена отдельной локальной веткой услуги; нет новых доказательств для специализированной surgery, radiation, ECT или именованного oncology сертификата.

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 15. VCA Murphy Road Animal Hospital

`vca-murphy-road-animal-hospital`

Адрес: 4408 Murphy Road, Nashville, TN 37209. Телефон: 615-383-4241. Официальный сайт: https://vcahospitals.com/murphy-road. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/murphy-road); фактическая проверка 2026-10-12T22:29:18.185913+00:00.

Принятый подтверждённый список: Local oncology care, Chemotherapy.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Charles Coats Staff Veterinarian DVM](https://vcahospitals.com/murphy-road/team/charles-coats).
- [Allison Fields Staff Veteriinarian DVM](https://vcahospitals.com/murphy-road/team/allison-fields).
- [Sara LaHaie Staff Veterinarian DVM](https://vcahospitals.com/murphy-road/team/sara-lahaie).
- [Page Redden Staff Veterinarian DVM](https://vcahospitals.com/murphy-road/team/page-redden).
- [Amanda Turner Staff Veterinarian DVM](https://vcahospitals.com/murphy-road/team/amanda-cassetty).
- [Christine Widmann Medical Director DVM](https://vcahospitals.com/murphy-road/team/christine-widmann).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-chemotherapy](https://vcahospitals.com/murphy-road/services/advanced-care/chemotherapy) — 2026-10-12T22:31:54.522973+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/murphy-road/everyday-care/your-visit) — 2026-10-12T22:31:54.539419+00:00; HTTP 200.
- [home](https://vcahospitals.com/murphy-road/) — 2026-10-12T22:29:18.185913+00:00; HTTP 200.
- [service](https://vcahospitals.com/murphy-road/services/advanced-care/oncology) — 2026-10-12T22:29:18.510648+00:00; HTTP 200.
- [services](https://vcahospitals.com/murphy-road/services) — 2026-10-12T22:29:21.473292+00:00; HTTP 200.
- [team](https://vcahospitals.com/murphy-road/team) — 2026-10-12T22:29:19.008149+00:00; HTTP 200.

Решения по изменениям:

- Изменений не требуется: существующая chemotherapy подтверждена отдельной локальной веткой услуги; нет новых доказательств для специализированной surgery, radiation, ECT или именованного oncology сертификата.

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 16. VCA Northview Animal Hospital Specialty Referral Center

`vca-northview-animal-hospital-specialty-referral-center`

Адрес: 223 Siebert Road, Pittsburgh, PA 15237. Телефон: 412-364-5353. Официальный сайт: https://vcahospitals.com/northview. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/northview); фактическая проверка 2026-10-12T22:29:21.650219+00:00.

Принятый подтверждённый список: Chemotherapy.

Химиотерапию сохранить по локальной primary-care услуге. Lisa Assandri — DACVIM по internal medicine; Tara Enwiller — DACVS, не подтверждённый surgical-oncology fellow. Приём primary/specialty разделён на официальном сайте.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Lisa Assandri Veterinarian Specialist DVM, DACVIM](https://vcahospitals.com/northview/specialty/team/lisa-assandri).
- [Tara Enwiller Veterinarian Specialist DVM, DACVS](https://vcahospitals.com/northview/specialty/team/tara-enwiller).
- [Mohamed Hashem Veterinarian DVM](https://vcahospitals.com/northview/primary/team/mohamed-hashem).
- [Karen Hayworth Veterinarian DVM](https://vcahospitals.com/northview/primary/team/karen-hayworth).
- [Sherry Smalley Veterinarian DVM](https://vcahospitals.com/northview/primary/team/sherry-smalley).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический specialty приём: опубликован referral route — форма направления, передача medical records и запись звонком владельца/лечащего ветеринара. Не считать форму доказательством обязательности направления во всех случаях.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [deep-primary-departments-oncology](https://vcahospitals.com/northview/primary/departments/oncology) — 2026-10-12T22:30:56.397402+00:00; попытка: HTTP Error 404: Not Found.
- [deep-primary-services](https://vcahospitals.com/northview/primary/services) — 2026-10-12T22:30:56.431362+00:00; HTTP 200.
- [deep-primary-team](https://vcahospitals.com/northview/primary/team) — 2026-10-12T22:30:56.342502+00:00; HTTP 200.
- [deep-specialty-departments-oncology](https://vcahospitals.com/northview/specialty/departments/oncology) — 2026-10-12T22:30:57.027553+00:00; попытка: HTTP Error 404: Not Found.
- [deep-specialty-services](https://vcahospitals.com/northview/specialty/services) — 2026-10-12T22:31:00.868333+00:00; попытка: HTTP Error 404: Not Found.
- [deep-specialty-team](https://vcahospitals.com/northview/specialty/team) — 2026-10-12T22:30:56.855941+00:00; HTTP 200.
- [follow-referral-forms](https://vcahospitals.com/northview/specialty/for-vets/referral-forms) — 2026-10-12T22:31:58.579663+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/northview/everyday-care/your-visit) — 2026-10-12T22:31:58.720441+00:00; HTTP 200.
- [home](https://vcahospitals.com/northview/) — 2026-10-12T22:29:21.650219+00:00; HTTP 200.
- [service](https://vcahospitals.com/northview/primary/services/advanced-care/chemotherapy) — 2026-10-12T22:29:21.775516+00:00; HTTP 200.
- [services](https://vcahospitals.com/northview/services) — 2026-10-12T22:29:21.956961+00:00; попытка: HTTP Error 404: Not Found.
- [team](https://vcahospitals.com/northview/team) — 2026-10-12T22:29:21.940336+00:00; попытка: HTTP Error 404: Not Found.

Решения по изменениям:

- Изменений не требуется: существующая chemotherapy подтверждена отдельной локальной веткой услуги; нет новых доказательств для специализированной surgery, radiation, ECT или именованного oncology сертификата.

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 17. VCA Northwest Veterinary Specialists

`vca-northwest-veterinary-specialists`

Адрес: 16756 SE 82nd Dr, Clackamas, OR 97015. Телефон: 503.656.3999. Официальный сайт: https://vcahospitals.com/northwest-veterinary-specialists. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/northwest-veterinary-specialists); фактическая проверка 2026-10-12T22:29:22.005864+00:00.

Принятый подтверждённый список: Medical oncology, Chemotherapy, Immunotherapy, Surgical oncology, Radiation oncology, Radiation therapy, IMRT, SRT.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Jodie Anderson Veterinary Specialist DVM, DACVIM (Internal Medicine)](https://vcahospitals.com/northwest-veterinary-specialists/team/jodie-anderson).
- [Angela Banz Veterinary Specialist DVM, DACVS](https://vcahospitals.com/northwest-veterinary-specialists/team/angela-banz).
- [Genia Bercovitz Veterinary Specialist VMD, DACVO (Ophthalmology)](https://vcahospitals.com/northwest-veterinary-specialists/team/genia-bercovitz).
- [Seana Byron-Perry Associate Veterinarian DVM](https://vcahospitals.com/northwest-veterinary-specialists/team/seana-byron-perry).
- [Jose Carvajal Veterinarian Specialist - Surgery DVM, MS, DACVS-SA, ACVS (Fellow, Joint Replacement Surgery)](https://vcahospitals.com/northwest-veterinary-specialists/team/jose-carvajal).
- [Kristonn Colborn Emergency Veterinarian DVM](https://vcahospitals.com/northwest-veterinary-specialists/team/kristonn-colborn).
- [Rosemary Cullander Emergency Veterinarian DVM](https://vcahospitals.com/northwest-veterinary-specialists/team/rosemary-cullander).
- [Brittani D'Amico Veterinary Specialist DVM, DACVIM (Neurology)](https://vcahospitals.com/northwest-veterinary-specialists/team/brittani-damico).
- [Kevin de Moya Veterinarian Specialist - Surgery DVM, MS, DACVS (SA), ACVS Fellow Candidate (Joint Replacement Surgery)](https://vcahospitals.com/northwest-veterinary-specialists/team/kevin-de-moya).
- [Joan Dolance Emergency Veterinarian DVM](https://vcahospitals.com/northwest-veterinary-specialists/team/joan-dolance).
- [Matt Dowling Veterinary Specialist DVM, MS, DACVIM (Oncology)](https://vcahospitals.com/northwest-veterinary-specialists/team/matt-dowling).
- [Molly Doyle Veterinarian Specialist DVM (Practice Limited to Internal Medicine)](https://vcahospitals.com/northwest-veterinary-specialists/team/molly-doyle).
- [Heidi Houchen Emergency Veterinarian DVM](https://vcahospitals.com/northwest-veterinary-specialists/team/heidi-houchen).
- [Ben Im Emergency Veterinarian DVM](https://vcahospitals.com/northwest-veterinary-specialists/team/ben-im).
- [Brianna Im Emergency Veterinarian DVM](https://vcahospitals.com/northwest-veterinary-specialists/team/brianna-im).
- [Sam Katzung Associate Veterinarian DVM](https://vcahospitals.com/northwest-veterinary-specialists/team/sam-katzung).
- [Karen Kline Veterinary Specialist DVM, DACVIM (Neurology)](https://vcahospitals.com/northwest-veterinary-specialists/team/karen-kline).
- [Courtney Korff Veterinarian Specialist - Neurology DVM, DACVIM (Neurology)](https://vcahospitals.com/northwest-veterinary-specialists/team/courtney-korff).
- [Tracy Landreth Emergency Veterinarian DVM](https://vcahospitals.com/northwest-veterinary-specialists/team/tracy-landreth).
- [Jaime LaVelle Emergency Veterinarian DVM](https://vcahospitals.com/northwest-veterinary-specialists/team/jaime-lavelle).
- [Melissa Marquez Emergency Veterinarian DVM](https://vcahospitals.com/northwest-veterinary-specialists/team/melissa-marquez).
- [Catherine McDonald Veterinary Specialist DVM, DACVIM (O), DACVR (RO) (Oncology)](https://vcahospitals.com/northwest-veterinary-specialists/team/catie-mcdonald).
- [Emi Menzen Emergency Veterinarian DVM](https://vcahospitals.com/northwest-veterinary-specialists/team/emi-menzen).
- [Tingwei Ou Veterinary Specialist DVM, MS, DACVR (Diagnostic Imaging)](https://vcahospitals.com/northwest-veterinary-specialists/team/tingwei-ou).
- [Kelsey Owen Medical Director DVM](https://vcahospitals.com/northwest-veterinary-specialists/team/kelsey-owen).
- [Snig Paul Veterinarian Specialist - Surgery DVM, DACVS (Small Animal)](https://vcahospitals.com/northwest-veterinary-specialists/team/snig-paul).
- [Lauren Robertson Veterinarian Specialist - Lead Emergency/Critical Care VMD, Residency Trained in Critical Care](https://vcahospitals.com/northwest-veterinary-specialists/team/lauren-robertson).
- [Sarah Salyer Veterinarian Specialist - Surgery DVM, MS, DACVS-SA, ACVS (Fellow, Surgical Oncology)](https://vcahospitals.com/northwest-veterinary-specialists/team/sarah-salyer).
- [Gretchen Scheffe Emergency Veterinarian DVM](https://vcahospitals.com/northwest-veterinary-specialists/team/gretchen-scheffe).
- [Paul Scherlie Veterinary Specialist DVM, DACVO (Ophthalmology)](https://vcahospitals.com/northwest-veterinary-specialists/team/paul-scherlie).
- [Michelle Taylor Veterinary Specialist DVM, DACVO (Ophthalmology)](https://vcahospitals.com/northwest-veterinary-specialists/team/michelle-taylor).
- [Jennifer Tepavich Veterinary Specialist DVM, DACVR (Diagnostic Imaging)](https://vcahospitals.com/northwest-veterinary-specialists/team/jennifer-tepavich).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический specialty приём: опубликован referral route — форма направления, передача medical records и запись звонком владельца/лечащего ветеринара. Не считать форму доказательством обязательности направления во всех случаях.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [departments](https://vcahospitals.com/northwest-veterinary-specialists/departments) — 2026-10-12T22:31:00.999883+00:00; HTTP 200.
- [follow-chemotherapy](https://vcahospitals.com/northwest-veterinary-specialists/departments/oncology/chemotherapy) — 2026-10-12T22:31:28.828812+00:00; HTTP 200.
- [follow-immunotherapy](https://vcahospitals.com/northwest-veterinary-specialists/departments/oncology/immunotherapy) — 2026-10-12T22:31:28.830358+00:00; HTTP 200.
- [follow-radiation-oncology](https://vcahospitals.com/northwest-veterinary-specialists/departments/radiation-oncology) — 2026-10-12T22:31:28.831657+00:00; HTTP 200.
- [follow-referral-forms](https://vcahospitals.com/northwest-veterinary-specialists/for-vets/referral-forms) — 2026-10-12T22:31:28.833439+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/northwest-veterinary-specialists/for-clients/your-visit) — 2026-10-12T22:31:28.833933+00:00; HTTP 200.
- [home](https://vcahospitals.com/northwest-veterinary-specialists/) — 2026-10-12T22:29:22.005864+00:00; HTTP 200.
- [oncology](https://vcahospitals.com/northwest-veterinary-specialists/departments/oncology) — 2026-10-12T22:31:01.089757+00:00; HTTP 200.
- [service](https://www.vetspecialists.com/vet-detail/?animals=dog&specs=Onco&country=United%20States&page=46&id=3ff61324-92e8-47f4-b241-b813fc8f24d3) — 2026-10-12T22:29:22.040350+00:00; HTTP 200.
- [services](https://vcahospitals.com/northwest-veterinary-specialists/services) — 2026-10-12T22:29:22.357005+00:00; попытка: HTTP Error 404: Not Found.
- [team](https://vcahospitals.com/northwest-veterinary-specialists/team) — 2026-10-12T22:29:22.076178+00:00; HTTP 200.

Решения по изменениям:

- `services`: Список местного отделения подтверждает химиотерапию/иммунотерапию; дополнительные локальные radiation/surgery доказательства приведены отдельными полями. Уверенность: high for chemo/radiation/surgery; medium-high for generic immunotherapy. [Доказательство](https://vcahospitals.com/northwest-veterinary-specialists/departments/oncology); 2026-10-12T22:31:01.089757+00:00. Короткая цитата: «Our Oncology Services».
- `service_details.radiation`: Подтверждена собственная установка и обе техники в описании филиала. Уверенность: high. [Доказательство](https://vcahospitals.com/northwest-veterinary-specialists/departments/radiation-oncology); 2026-10-12T22:31:28.831657+00:00. Короткая цитата: «With our new radiation unit, we can now deliver radiation».
- `service_details.surgical_oncology`: Текущая команда, профиль fellow и участие хирурга в местной Oncology Team подтверждают специализированную хирургическую онкологию. Уверенность: medium-high: service conclusion from current roster plus dated-unspecified joining biography. [Доказательство](https://vcahospitals.com/northwest-veterinary-specialists/team/sarah-salyer); 2026-10-12T22:30:17.336416+00:00. Короткая цитата: «looking forward to starting a surgical oncology service at VCA Northwest».
- `website`: Использовать действующий официальный HTTPS URL вместо HTTP; номер телефона по цифрам совпадает. Уверенность: high. [Доказательство](https://vcahospitals.com/northwest-veterinary-specialists); 2026-10-12T22:29:22.005864+00:00. Короткая цитата: «VCA Northwest Veterinary Specialists».
- `verification_url`: Заменить ACVIM профиль как единственный источник услуг текущим отделением филиала. Уверенность: high. [Доказательство](https://vcahospitals.com/northwest-veterinary-specialists/departments/oncology); 2026-10-12T22:31:01.089757+00:00. Короткая цитата: «Our Oncology Services».
- `oncology_clinicians`: Сохранить текущих специалистов отдельно от услуг. Residency-trained не означает board-certified; диагностическая радиология не означает radiation oncology. Уверенность: high. [Доказательство](https://vcahospitals.com/northwest-veterinary-specialists/team); 2026-10-12T22:29:22.076178+00:00. Короткая цитата: «DVM, MS, DACVIM (Oncology)».

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 18. VCA Pahle Animal Hospital

`vca-pahle-animal-hospital`

Адрес: 10827 W. Oklahoma Avenue, West Allis, WI 53227. Телефон: 414-541-6440. Официальный сайт: https://vcahospitals.com/pahle. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/pahle); фактическая проверка 2026-10-12T22:29:22.654306+00:00.

Принятый подтверждённый список: Local oncology care.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Stephanie Brosky Staff Veterinarian](https://vcahospitals.com/pahle/team/stephanie-brosky).
- [Nadia Czajkowski Staff Veterinarian DVM](https://vcahospitals.com/pahle/team/nadia-czajkowski).
- [Clarisse Rebancos Associate Veterinarian DVM](https://vcahospitals.com/pahle/team/clarisse-rebancos).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-your-visit](https://vcahospitals.com/pahle/everyday-care/your-visit) — 2026-10-12T22:31:54.435629+00:00; HTTP 200.
- [home](https://vcahospitals.com/pahle/) — 2026-10-12T22:29:22.654306+00:00; HTTP 200.
- [service](https://vcahospitals.com/pahle/services/advanced-care/oncology) — 2026-10-12T22:29:25.221646+00:00; HTTP 200.
- [services](https://vcahospitals.com/pahle/services) — 2026-10-12T22:29:25.566744+00:00; HTTP 200.
- [team](https://vcahospitals.com/pahle/team) — 2026-10-12T22:29:25.562785+00:00; HTTP 200.

Решения по изменениям:

- `services`: Убрать химиотерапию из подтверждённого списка: текущие официальные Oncology/services/team/биографии не подтверждают конкретную модальность. Это не утверждение, что услугу не выполняют. Уверенность: high for evidence classification; actual absence not established. [Доказательство](https://vcahospitals.com/pahle/services/advanced-care/oncology); 2026-10-12T22:29:25.221646+00:00. Короткая цитата: «Oncology».
- `review_flags`: Сохранить конкретные нерешённые вопросы следующему проходу; статусы not confirmed не равны service unavailable. Уверенность: high for unresolved classification. [Доказательство](https://vcahospitals.com/pahle/services/advanced-care/oncology); 2026-10-12T22:29:25.221646+00:00. Короткая цитата: «Oncology».

Следующий проход:

- Химиотерапия: не подтверждено. Найти актуальное объявление об её проведении, локальный clinical case или протокол работы филиала; не считать отсутствие онколога отрицательным доказательством.

### 19. VCA Palm Beach Veterinary Specialists

`vca-palm-beach-veterinary-specialists`

Адрес: 3884 Forest Hill Blvd., West Palm Beach, FL 33406. Телефон: 561-434-5700. Официальный сайт: https://vcahospitals.com/palm-beach-vet-specialists. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/palm-beach-vet-specialists); фактическая проверка 2026-10-12T22:29:25.567613+00:00.

Принятый подтверждённый список: Medical oncology, Chemotherapy, Radiation oncology, Immunotherapy, Radiation therapy, IMRT.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Adrienne Balionis Associate Veterinarian DVM](https://vcahospitals.com/palm-beach-vet-specialists/team/adrienne-balionis).
- [Ayanna Brown Associate Veterinarian DVM](https://vcahospitals.com/palm-beach-vet-specialists/team/ayanna-brown).
- [Hannah Burchette Rhodes Veterinarian Specialist - Emergency/Critical Care DVM, DACVECC](https://vcahospitals.com/palm-beach-vet-specialists/team/hannah-burchette-rhodes).
- [Melody Chen Veterinarian Specialist - Internal Medicine DVM, DACVIM](https://vcahospitals.com/palm-beach-vet-specialists/team/melody-chen).
- [Rosa Elia Associate Veterinarian DVM](https://vcahospitals.com/palm-beach-vet-specialists/team/rosa-elia).
- [Ashley Felhofer Emergency Veterinarian DVM](https://vcahospitals.com/palm-beach-vet-specialists/team/ashley-felhofer).
- [Antara Finney Associate Veterinarian VMD](https://vcahospitals.com/palm-beach-vet-specialists/team/antara-finney).
- [Brandi Gallagher Veterinarian Specialist - Internal Medicine DVM, DACVIM](https://vcahospitals.com/palm-beach-vet-specialists/team/brandi-gallagher).
- [Mark Garny Associate Veterinarian DVM](https://vcahospitals.com/palm-beach-vet-specialists/team/mark-garny).
- [Ellen Gray Associate Veterinarian DVM](https://vcahospitals.com/palm-beach-vet-specialists/team/ellen-gray).
- [Lorelei Lanum Emergency Veterinarian DVM, MPH](https://vcahospitals.com/palm-beach-vet-specialists/team/lorelei-lanum).
- [Brent Megarry Associate Veterinarian DVM](https://vcahospitals.com/palm-beach-vet-specialists/team/brent-megarry).
- [Valerie Morales Coll Veterinarian Specialist - Radiation Oncology DVM, ACVR-RO](https://vcahospitals.com/palm-beach-vet-specialists/team/valerie-morales-coll).
- [Carolyn Nye Veterinarian Specialist - Neurology DVM, MS, DACVIM](https://vcahospitals.com/palm-beach-vet-specialists/team/carolyn-nye).
- [Charlotte Pfund Veterinarian Specialist - Surgery DVM, DACVS (SA)](https://vcahospitals.com/palm-beach-vet-specialists/team/charlotte-pfund).
- [Iohana Rocha Associate Veterinarian DVM](https://vcahospitals.com/palm-beach-vet-specialists/team/iohana-rocha).
- [Robert G. Roy Veterinarian Specialist - Surgery DVM, DACVS, MS, P.A.](https://vcahospitals.com/palm-beach-vet-specialists/team/robert-roy).
- [Laura Lee Sartor Veterinarian Specialist - Internal Medicine DVM, DACVIM](https://vcahospitals.com/palm-beach-vet-specialists/team/laura-lee-sartor).
- [Jason Tarricone Specialty Medical Director DVM, DACVS (SA)](https://vcahospitals.com/palm-beach-vet-specialists/team/jason-tarricone).
- [Taylor Thompson Emergency Veterinarian DVM](https://vcahospitals.com/palm-beach-vet-specialists/team/taylor-thompson).
- [Alissa Tumminia Associate Veterinarian DVM](https://vcahospitals.com/palm-beach-vet-specialists/team/alissa-tumminia).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический specialty приём: опубликован referral route — форма направления, передача medical records и запись звонком владельца/лечащего ветеринара. Не считать форму доказательством обязательности направления во всех случаях.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [departments](https://vcahospitals.com/palm-beach-vet-specialists/departments) — 2026-10-12T22:31:01.104940+00:00; HTTP 200.
- [follow-chemotherapy](https://vcahospitals.com/palm-beach-vet-specialists/departments/oncology/chemotherapy) — 2026-10-12T22:31:58.744716+00:00; HTTP 200.
- [follow-immunotherapy](https://vcahospitals.com/palm-beach-vet-specialists/departments/oncology/immunotherapy) — 2026-10-12T22:31:58.758895+00:00; HTTP 200.
- [follow-radiation-oncology](https://vcahospitals.com/palm-beach-vet-specialists/departments/radiation-oncology) — 2026-10-12T22:31:28.820972+00:00; HTTP 200.
- [follow-referral-forms](https://vcahospitals.com/palm-beach-vet-specialists/for-vets/referral-forms) — 2026-10-12T22:31:28.821501+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/palm-beach-vet-specialists/for-clients/your-visit) — 2026-10-12T22:31:28.821888+00:00; HTTP 200.
- [home](https://vcahospitals.com/palm-beach-vet-specialists/) — 2026-10-12T22:29:25.567613+00:00; HTTP 200.
- [oncology](https://vcahospitals.com/palm-beach-vet-specialists/departments/oncology) — 2026-10-12T22:31:01.162259+00:00; HTTP 200.
- [service](https://vcahospitals.com/palm-beach-vet-specialists/departments/oncology) — 2026-10-12T22:29:25.590144+00:00; HTTP 200.
- [services](https://vcahospitals.com/palm-beach-vet-specialists/services) — 2026-10-12T22:29:25.859610+00:00; попытка: HTTP Error 404: Not Found.
- [team](https://vcahospitals.com/palm-beach-vet-specialists/team) — 2026-10-12T22:29:25.607480+00:00; HTTP 200.

Решения по изменениям:

- `services`: Добавить иммунотерапию из списка услуг отделения данного филиала. Не приписывать конкретный препарат. Уверенность: medium-high. [Доказательство](https://vcahospitals.com/palm-beach-vet-specialists/departments/oncology); 2026-10-12T22:29:25.590144+00:00. Короткая цитата: «Immunotherapy».
- `service_details.radiation`: Местная лучевая терапия подтверждена оборудованием филиала. Не добавлять SRT без отдельного подтверждения. Уверенность: high. [Доказательство](https://vcahospitals.com/palm-beach-vet-specialists/departments/radiation-oncology); 2026-10-12T22:31:28.820972+00:00. Короткая цитата: «Varian 2100 EX Linear Accelerator».
- `oncology_clinicians`: Сохранить текущих специалистов отдельно от услуг. Residency-trained не означает board-certified; диагностическая радиология не означает radiation oncology. Уверенность: high. [Доказательство](https://vcahospitals.com/palm-beach-vet-specialists/team); 2026-10-12T22:29:25.607480+00:00. Короткая цитата: «DVM, ACVR-RO».
- `review_flags`: Сохранить конкретные нерешённые вопросы следующему проходу; статусы not confirmed не равны service unavailable. Уверенность: high for unresolved classification. [Доказательство](https://vcahospitals.com/palm-beach-vet-specialists/departments/oncology); 2026-10-12T22:29:25.590144+00:00. Короткая цитата: «Oncology».

Следующий проход:

- Медицинская онкология/химиотерапия опубликованы как услуги отделения; назначенный текущий medical oncologist не установлен. Не превращать интерниста, интерес к онкологии или radiation oncologist в сертификат medical oncology; сохранить услуги.

### 20. VCA PetCare East

`vca-petcare-east`

Адрес: 2425 Mendocino Ave, Santa Rosa, CA 95403. Телефон: 707-579-3900. Официальный сайт: https://vcahospitals.com/petcare-east. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/petcare-east); фактическая проверка 2026-10-12T22:29:26.016192+00:00.

Принятый подтверждённый список: Medical oncology, Chemotherapy, Immunotherapy, ONCEPT.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Tessa Anderson Emergency Veterinarian DVM](https://vcahospitals.com/petcare-east/specialty/team/tessa-anderson).
- [Leslie Angus Emergency Veterinarian DVM](https://vcahospitals.com/petcare-east/specialty/team/leslie-angus).
- [Kristan Bonnett Emergency Veterinarian DVM](https://vcahospitals.com/petcare-east/specialty/team/kristan-bonnett).
- [Kristy Bowles Emergency Veterinarian DVM](https://vcahospitals.com/petcare-east/specialty/team/kristy-bowles).
- [Jillian Brown Emergency Veterinarian DVM](https://vcahospitals.com/petcare-east/specialty/team/jillian-brown).
- [Nicole Bush Crispo Emergency Veterinarian DVM](https://vcahospitals.com/petcare-east/specialty/team/nicole-bush-crispo).
- [Mark Dosch Veterinary Specialist DVM, DACVS-SA (Surgery)](https://vcahospitals.com/petcare-east/specialty/team/mark-dosch).
- [Dan Famini Emergency Veterinarian DVM](https://vcahospitals.com/petcare-east/specialty/team/daniel-famini).
- [Cindy Fisher Veterinary Specialist DVM, MS, DACVIM (SAIM)](https://vcahospitals.com/petcare-east/specialty/team/cindy-fisher).
- [Katie Forsman Emergency Veterinarian DVM](https://vcahospitals.com/petcare-east/specialty/team/katie-forsman).
- [Kim Henry Medical Director DVM](https://vcahospitals.com/petcare-east/specialty/team/kim-henry).
- [Jordan Hewitt Emergency Veterinarian DVM](https://vcahospitals.com/petcare-east/specialty/team/jordan-hewitt).
- [Rebecca Kauer Emergency Veterinarian BVetMed](https://vcahospitals.com/petcare-east/specialty/team/rebecca-kauer).
- [Haylie Lawson Veterinary Specialist DVM, DACVIM (Oncology)](https://vcahospitals.com/petcare-east/specialty/team/haylie-lawson).
- [Suzanne Miller Emergency Veterinarian DVM](https://vcahospitals.com/petcare-east/specialty/team/suzanne-miller).
- [Mary Straub Emergency Veterinarian DVM](https://vcahospitals.com/petcare-east/specialty/team/mary-straub).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический specialty приём: опубликован referral route — форма направления, передача medical records и запись звонком владельца/лечащего ветеринара. Не считать форму доказательством обязательности направления во всех случаях.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [deep-specialty-departments-oncology](https://vcahospitals.com/petcare-east/specialty/departments/oncology) — 2026-10-12T22:31:00.932344+00:00; HTTP 200.
- [deep-specialty-services](https://vcahospitals.com/petcare-east/specialty/services) — 2026-10-12T22:31:00.985674+00:00; попытка: HTTP Error 404: Not Found.
- [deep-specialty-team](https://vcahospitals.com/petcare-east/specialty/team) — 2026-10-12T22:31:00.894883+00:00; HTTP 200.
- [follow-chemotherapy](https://vcahospitals.com/petcare-east/specialty/departments/oncology/chemotherapy) — 2026-10-12T22:31:35.308216+00:00; HTTP 200.
- [follow-referral-forms](https://vcahospitals.com/petcare-east/specialty/for-vets/referral-forms) — 2026-10-12T22:31:36.044516+00:00; HTTP 200.
- [follow-surgery-services-overview](https://vcahospitals.com/petcare-east/specialty/departments/surgery/surgery-services-overview) — 2026-10-12T22:31:36.023941+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/petcare-east/primary/your-visit) — 2026-10-12T22:31:58.634773+00:00; HTTP 200.
- [home](https://vcahospitals.com/petcare-east/) — 2026-10-12T22:29:26.016192+00:00; HTTP 200.
- [service](https://www.vetspecialists.com/vet-detail/?animals=dog&specs=Onco&country=United%20States&page=46&id=8082894f-00f7-4e41-8e20-b4bc849f1ad3) — 2026-10-12T22:29:26.672380+00:00; HTTP 200.
- [services](https://vcahospitals.com/petcare-east/services) — 2026-10-12T22:29:30.372790+00:00; попытка: HTTP Error 404: Not Found.
- [team](https://vcahospitals.com/petcare-east/team) — 2026-10-12T22:29:30.253673+00:00; попытка: HTTP Error 404: Not Found.

Решения по изменениям:

- `services`: Доступ ONCEPT заявлен непосредственно для данного отделения. Для PetCare также добавить опубликованную химиотерапию; иммунотерапия подтверждена конкретным ONCEPT. Уверенность: high. [Доказательство](https://vcahospitals.com/petcare-east/specialty/departments/oncology); 2026-10-12T22:31:00.932344+00:00. Короткая цитата: «ONCEPT is available through our hospital’s Oncology Department.».
- `verification_url`: Для местных услуг использовать отделение филиала; ACVIM сохранить как supporting source. Уверенность: high. [Доказательство](https://vcahospitals.com/petcare-east/specialty/departments/oncology); 2026-10-12T22:31:00.932344+00:00. Короткая цитата: «Our Oncology Services».
- `oncology_clinicians`: Сохранить текущих специалистов отдельно от услуг. Residency-trained не означает board-certified; диагностическая радиология не означает radiation oncology. Уверенность: high. [Доказательство](https://vcahospitals.com/petcare-east/specialty/team); 2026-10-12T22:31:00.894883+00:00. Короткая цитата: «DVM, DACVIM (Oncology)».

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 21. VCA Ragland & Riley Animal Hospital

`vca-ragland-riley-animal-hospital`

Адрес: 3207 Cookeville Highway, Livingston, TN 38570. Телефон: 931-498-3153. Официальный сайт: https://vcahospitals.com/ragland-and-riley. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/ragland-and-riley); фактическая проверка 2026-10-12T22:29:30.378258+00:00.

Принятый подтверждённый список: Local oncology care, Chemotherapy.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [John Cobb Medical Director DVM](https://vcahospitals.com/ragland-and-riley/team/john-cobb).
- [Cameron Mandel Staff Veterinarian DVM, PhD](https://vcahospitals.com/ragland-and-riley/team/cameron-mandel).
- [Halie McDonald Staff Veterinarian DVM](https://vcahospitals.com/ragland-and-riley/team/halie-mcdonald).
- [Fredrick Moody Staff Veterinarian](https://vcahospitals.com/ragland-and-riley/team/fred-moody).
- [Amanda Thomas Staff Veterinarian DVM](https://vcahospitals.com/ragland-and-riley/team/amanda-thomas).
- [Lisa Wearing Staff Veterinarian DVM](https://vcahospitals.com/ragland-and-riley/team/lisa-wearing).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-chemotherapy](https://vcahospitals.com/ragland-and-riley/services/advanced-care/chemotherapy) — 2026-10-12T22:31:28.827682+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/ragland-and-riley/everyday-care/your-visit) — 2026-10-12T22:31:28.828065+00:00; HTTP 200.
- [home](https://vcahospitals.com/ragland-and-riley/) — 2026-10-12T22:29:30.378258+00:00; HTTP 200.
- [service](https://vcahospitals.com/ragland-and-riley/services/advanced-care/oncology) — 2026-10-12T22:29:30.579713+00:00; HTTP 200.
- [services](https://vcahospitals.com/ragland-and-riley/services) — 2026-10-12T22:29:30.641005+00:00; HTTP 200.
- [team](https://vcahospitals.com/ragland-and-riley/team) — 2026-10-12T22:29:30.623801+00:00; HTTP 200.

Решения по изменениям:

- Изменений не требуется: существующая chemotherapy подтверждена отдельной локальной веткой услуги; нет новых доказательств для специализированной surgery, radiation, ECT или именованного oncology сертификата.

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 22. VCA Ridgewood Veterinary Hospital

`vca-ridgewood-veterinary-hospital`

Адрес: 320 E. Ridgewood Avenue, Ridgewood, NJ 07450. Телефон: 201-447-6000. Официальный сайт: https://vcahospitals.com/ridgewood. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/ridgewood); фактическая проверка 2026-10-12T22:29:30.729309+00:00.

Принятый подтверждённый список: Local oncology care, Chemotherapy.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Joanne Healey Medical Director DVM, CVA](https://vcahospitals.com/ridgewood/team/joanne-healey).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-chemotherapy](https://vcahospitals.com/ridgewood/services/advanced-care/chemotherapy) — 2026-10-12T22:31:54.439339+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/ridgewood/everyday-care/your-visit) — 2026-10-12T22:31:54.459824+00:00; HTTP 200.
- [home](https://vcahospitals.com/ridgewood/) — 2026-10-12T22:29:30.729309+00:00; HTTP 200.
- [service](https://vcahospitals.com/ridgewood/services/advanced-care/oncology) — 2026-10-12T22:29:31.460770+00:00; HTTP 200.
- [services](https://vcahospitals.com/ridgewood/services) — 2026-10-12T22:29:31.857520+00:00; HTTP 200.
- [team](https://vcahospitals.com/ridgewood/team) — 2026-10-12T22:29:31.657912+00:00; HTTP 200.

Решения по изменениям:

- Изменений не требуется: существующая chemotherapy подтверждена отдельной локальной веткой услуги; нет новых доказательств для специализированной surgery, radiation, ECT или именованного oncology сертификата.

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 23. VCA Roberts Animal Hospital

`vca-roberts-animal-hospital`

Адрес: 516 Washington Street, Hanover, MA 02339. Телефон: 781-826-2306. Официальный сайт: https://vcahospitals.com/roberts. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/roberts); фактическая проверка 2026-10-12T22:29:34.785998+00:00.

Принятый подтверждённый список: Chemotherapy.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Cassidy Barrett Staff Veterinarian MVB](https://vcahospitals.com/roberts/team/cassidy-barrett).
- [Marie Chartier Veterinary Specialist - Internal Medicine DVM, DACVIM](https://vcahospitals.com/roberts/team/marie-chartier).
- [Rose Guarnieri Staff Veterinarian DVM](https://vcahospitals.com/roberts/team/rose-guarnieri).
- [Nicole Morgan Staff Veterinarian DVM](https://vcahospitals.com/roberts/team/nicole-morgan).
- [Stephanie Powers Group Medical Director DVM](https://vcahospitals.com/roberts/team/stephanie-powers).
- [Mary Reynolds Callahan Staff Veterinarian DVM](https://vcahospitals.com/roberts/team/mary-reynolds-callahan).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-your-visit](https://vcahospitals.com/roberts/everyday-care/your-visit) — 2026-10-12T22:31:28.820194+00:00; HTTP 200.
- [home](https://vcahospitals.com/roberts/) — 2026-10-12T22:29:34.785998+00:00; HTTP 200.
- [service](https://vcahospitals.com/roberts/services/advanced-care/chemotherapy) — 2026-10-12T22:29:34.907838+00:00; HTTP 200.
- [services](https://vcahospitals.com/roberts/services) — 2026-10-12T22:29:35.034429+00:00; HTTP 200.
- [team](https://vcahospitals.com/roberts/team) — 2026-10-12T22:29:34.965551+00:00; HTTP 200.

Решения по изменениям:

- Изменений не требуется: существующая chemotherapy подтверждена отдельной локальной веткой услуги; нет новых доказательств для специализированной surgery, radiation, ECT или именованного oncology сертификата.

Следующий проход:

- Материального противоречия для принятых фильтров не осталось. Конкретные препараты, схема и врач на дату записи не опубликованы полностью; не расширять услугу до любых протоколов/продуктов.

### 24. VCA Roswell Animal Hospital

`vca-roswell-animal-hospital`

Адрес: 1112 Alpharetta Street, Roswell, GA 30075. Телефон: 770-993-9031. Официальный сайт: https://vcahospitals.com/roswell. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/roswell); фактическая проверка 2026-10-12T22:29:35.166633+00:00.

Принятый подтверждённый список: Local oncology care.

Филиал прямо описывает консультацию онкологов по телефону с лечащим ветеринаром; это vet-to-vet поддержка, не подтверждённая запись owner-to-oncologist и не именованный удалённый сервис.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Lori Mills Staff Veterinarian](https://vcahospitals.com/roswell/team/lori-mills).
- [Jilleen Ray Staff Veterinarian](https://vcahospitals.com/roswell/team/jilleen-ray).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены. Отдельно подтверждена телефонная vet-to-vet поддержка онколога; owner remote appointment не установлена.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-your-visit](https://vcahospitals.com/roswell/everyday-care/your-visit) — 2026-10-12T22:31:47.663839+00:00; HTTP 200.
- [home](https://vcahospitals.com/roswell/) — 2026-10-12T22:29:35.166633+00:00; HTTP 200.
- [service](https://vcahospitals.com/roswell/services/advanced-care/oncology) — 2026-10-12T22:29:35.187211+00:00; HTTP 200.
- [services](https://vcahospitals.com/roswell/services) — 2026-10-12T22:29:35.315220+00:00; HTTP 200.
- [team](https://vcahospitals.com/roswell/team) — 2026-10-12T22:29:35.281678+00:00; HTTP 200.

Решения по изменениям:

- `services`: Убрать химиотерапию из подтверждённого списка: текущие официальные Oncology/services/team/биографии не подтверждают конкретную модальность. Это не утверждение, что услугу не выполняют. Уверенность: high for evidence classification; actual absence not established. [Доказательство](https://vcahospitals.com/roswell/services/advanced-care/oncology); 2026-10-12T22:29:35.187211+00:00. Короткая цитата: «Our hospital offers Oncology services for your pet.».
- `review_flags`: Сохранить конкретные нерешённые вопросы следующему проходу; статусы not confirmed не равны service unavailable. Уверенность: high for unresolved classification. [Доказательство](https://vcahospitals.com/roswell/services/advanced-care/oncology); 2026-10-12T22:29:35.187211+00:00. Короткая цитата: «Oncology».

Следующий проход:

- Химиотерапия: не подтверждено. Найти актуальное объявление об её проведении, локальный clinical case или протокол работы филиала; не считать отсутствие онколога отрицательным доказательством.
- Pet Cancer Center прямо указывает chemotherapy, но страница без актуальной даты; общий каталог этого издателя обновлён 2019-03-06. Это историческое вторичное положительное свидетельство, недостаточное для confirmed current chemotherapy.

### 25. VCA Rutherford Animal Hospital

`vca-rutherford-animal-hospital`

Адрес: 755 Rutherford Avenue, Rutherford, NJ 07070. Телефон: 201-933-4111. Официальный сайт: https://vcahospitals.com/rutherford. Адрес/телефон сверены с опубликованным филиалом; различия Drive/Dr, Avenue/Ave и знаков телефона косметические, не переезд.

Работа: действующая официальная страница, опубликованы часы и контакты. [Источник](https://vcahospitals.com/rutherford); фактическая проверка 2026-10-12T22:29:35.333641+00:00.

Принятый подтверждённый список: Local oncology care, Cryosurgery.

Текущая опубликованная команда и квалификация (отдельно от услуг; прочитаны страницы team и доступные прямые биографии):

- [Jasmine Calle Veterinarian DVM](https://vcahospitals.com/rutherford/team/jasmine-calle).
- [Athanasia Karagiannis Veterinarian DVM](https://vcahospitals.com/rutherford/team/athanasia-karagiannis).
- [Jenny Sing Medical Director DVM](https://vcahospitals.com/rutherford/team/jenny-sing).
- [Susan Tobias Veterinarian DVM](https://vcahospitals.com/rutherford/team/susan-tobias).

Врач, обозначенный Staff Veterinarian/Associate Veterinarian, не назван здесь board-certified oncologist. DVM/BVMS — ветеринарная степень, не сертификат oncology. ABVP, DACVS и DACVIM(SAIM) не переименованы в oncology. У сотрудников без опубликованной степени её не дописывать.

Обращение: Физический приём, запись через контакты филиала/опубликованную booking-ссылку. Обязательное направление не установлено. Приглашённый врач, мобильный формат и owner oncology teleconsultation не подтверждены.

Проверенные поля без исправлений: работа филиала, адрес, город/штат/ZIP, телефон, официальный website (кроме HTTPS Northwest); именованный team roster/заявленные квалификации; услуги, referral/booking и мобильный/удалённый формат. Источники и фактические даты:

- [follow-cryosurgery](https://vcahospitals.com/rutherford/services/advanced-care/cryosurgery) — 2026-10-12T22:31:54.629167+00:00; HTTP 200.
- [follow-your-visit](https://vcahospitals.com/rutherford/everyday-care/your-visit) — 2026-10-12T22:31:54.714663+00:00; HTTP 200.
- [home](https://vcahospitals.com/rutherford/) — 2026-10-12T22:29:35.333641+00:00; HTTP 200.
- [service](https://vcahospitals.com/rutherford/services/advanced-care/oncology) — 2026-10-12T22:29:36.352933+00:00; HTTP 200.
- [services](https://vcahospitals.com/rutherford/services) — 2026-10-12T22:29:39.993278+00:00; HTTP 200.
- [team](https://vcahospitals.com/rutherford/team) — 2026-10-12T22:29:39.845002+00:00; HTTP 200.

Решения по изменениям:

- `services`: Убрать химиотерапию из подтверждённого списка: текущие официальные Oncology/services/team/биографии не подтверждают конкретную модальность. Это не утверждение, что услугу не выполняют. Добавить отдельно криохирургию ограниченных кожных опухолей, не surgical oncology. Уверенность: high for evidence classification; actual absence not established. [Доказательство](https://vcahospitals.com/rutherford/services/advanced-care/oncology); 2026-10-12T22:29:36.352933+00:00. Короткая цитата: «Oncology».
- `service_details.cryosurgery`: Официальная отдельная услуга филиала; ограниченная криохирургия, не общая онкологическая хирургия. Уверенность: medium-high. [Доказательство](https://vcahospitals.com/rutherford/services/advanced-care/cryosurgery); 2026-10-12T22:31:54.629167+00:00. Короткая цитата: «Treatment of skin tumors (depending on size)».
- `review_flags`: Сохранить конкретные нерешённые вопросы следующему проходу; статусы not confirmed не равны service unavailable. Уверенность: high for unresolved classification. [Доказательство](https://vcahospitals.com/rutherford/services/advanced-care/oncology); 2026-10-12T22:29:36.352933+00:00. Короткая цитата: «Oncology».

Следующий проход:

- Химиотерапия: не подтверждено. Найти актуальное объявление об её проведении, локальный clinical case или протокол работы филиала; не считать отсутствие онколога отрицательным доказательством.
- Cylex перечисляет Chemotherapy, но не даёт независимо проверяемого текущего clinical delivery evidence. Криохирургия подтверждается отдельно; сочетание с chemotherapy в образовательном тексте не доказывает её местное введение.

## Дополнительные и косвенные источники

- Metzger: [Penn State — clinical case, обновлено 26 June 2026](https://d1grabzpqvmyyx.cloudfront.net/news/agricultural-sciences/story/students-share-hands-experiences-vca-metzger-animal-hospital-externship). Официальный университетский репортаж, косвенный для наличия услуги клиники; не официальный перечень услуг больницы. Описывает пациента Copper в этом филиале, HSA, спленэктомию и chemotherapy в плане лечения. Проверено 2026-10-12 через Web open.
- [Pet Cancer Center — Roswell](https://www.petcancercenter.org/GA_Veterinary_Oncologist_Georgia_Atlanta_VCA_Roswell_Animal_Hospital.html): вторичный недатированный branch listing с chemotherapy. Прочитан 2026-10-12; не достаточен для current confirmed label.
- [Pet Cancer Center — общий каталог](https://www.petcancercenter.org/Veterinary_Oncologists_US_p1.html): вторичный, Last updated 3/6/2019; включает Highlands Abingdon. Прочитан 2026-10-12 только для назначенных clinic leads, без проверки trials.
- [Cylex Rutherford](https://www.cylex.us.com/company/vca-rutherford-animal-hospital-27185067.html): вторичный агрегатор, Chemotherapy в списке, независимо проверяемого свежего clinical evidence нет. Прочитан 2026-10-12.

## Препятствия и полнота

Все 25 записей обработаны. Прямые root /team и /services дали 404 у разделённых primary/specialty сайтов; реальные primary/specialty ссылки открыты, team roster восстановлен. NW/PetCare отсутствуют в supplemental, но baseline восстановлен из generated catalog; это не недоступное исходное значение.

Оставшиеся пробелы относятся к фактам: подтверждение нынешней chemotherapy Highlands/Pahle/Roswell/Rutherford; точное место RT Mountain View; назначенный medical oncologist LA/Palm Beach. Официальные branch/services/team/bios и дополнительный поиск выполнены. Отсутствие публикации нужного факта — not established, не закрытие и не внешний запрет доступа.

Общие базы/даты source inventory не обновлены по прямому запрету пользователя. Фактические checked_at находятся в отчёте/JSON; remote date persistence и production проверки не заявляются. Перед последующим применением сравнить old_value со свежим main, сохранить изменения других пакетов, интегрировать только выбранные поля в существующую схему и выполнить обычные validators/build.
