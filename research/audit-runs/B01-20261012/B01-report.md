# Решения B01 приняты; перепроверка при следующем проходе

По указанию владельца выводы по спорным данным приняты без дополнительной ручной проверки. В source inventory **10 записей** получили `review_required`, `recheck_on: next_oncology_care_pass`, `recheck_after` и конкретные `review_questions` с официальными URLs. Это отметки для очередного прохода, без запуска нового обхода или фоновой работы. Даты фактических проверок сайтов сохранены; время решения указано отдельно.

- Лучевая в восьми спорных филиалах: не включать в подтверждённые местные услуги до доказательства фактического проведения по адресу. Не считать услугу отсутствующей.
- Иммунотерапия в семи спорных филиалах и Maitland: не включать до конкретного местного подтверждения.
- Maitland: сохранять опубликованные медицинскую онкологию, химиотерапию и подтверждённую лучевую; Goodson не указывать как подтверждённого нынешнего врача и не делать вывод об уходе или закрытии отдела.
- Cary: ранее принятый вывод об иммунотерапии сохранить с явной пометкой, что привязка самоотчёта Ruslander к нынешнему филиалу — inference.
- ECT в пяти филиалах и отдельная лучевая площадка Malvern 50 Three Tun Rd. сохранены.

Изменения остаются локальными. Публикация не выполнялась.

---

# Локальное применение B01 — 12 октября 2026

**Статус: изменения внесены локально; публикация и push не выполнялись.**
Ветка `audit/b01-local-20261012`, исходная ревизия `6d70a739babe40e534a295cb8c06f7bda14501ae`.
Назначены 25 source_id; создано 26 физических записей: Malvern 40 и Cancer Center 50 Three Tun Rd. разделены. Сырые ACVIM-профили и trials не изменены.

Обновлены контакты, официальные филиальные URLs, текущие врачи/сертификации и локальные услуги. Неподтверждённая лучевая исключена из фильтров Augusta, Brandon, Clearwater, Durham, Fort Myers, Nashville, Northfield и Port Washington. Неподтверждённая иммунотерапия исключена из Augusta, Brandon, Brentwood, Clearwater, Durham, Nashville, Port Washington и Maitland. Это не утверждение об отсутствии услуг.

ECT сохранена в Arden Hills, Auburn Hills, Fort Myers, Lafayette и Northfield: явное указание в локальном списке, единый порог подтверждения. Northfield RT остаётся unresolved. Для Cary указано, что отнесение сообщённого Ruslander применения иммунотерапии к нынешнему филиалу — inference. Goodson не включена в подтверждённую нынешнюю команду Maitland; медицинская онкология там остаётся опубликованной услугой.

В `B01-proposed_changes.json` раздел **applied_changes** содержит фактически внесённые значения относительно текущего checkout, URL, короткую цитату, дату проверки и branch_scope. Если поле прежде отсутствовало, old_value прямо помечает отсутствие поля; это не неизвестное исходное значение. Исторические разделы отчёта ниже сохранены для прослеживаемости; прежние указания «оставлено без изменений» для спорных фильтров заменены этим итогом.

Проверки: полная локальная сборка сайта; B01 regression; валидатор каталога и итоговый diff. Детальные результаты завершения записаны в `research/audit-runs/B01-20261012/validation.txt`.

Вопросы для следующего прохода (ручная проверка владельцем не требуется):
1. Maitland: кто сейчас принимает по медицинской онкологии, доступна ли Teresa Goodson и какая иммунотерапия? https://bluepearlvet.com/hospital/maitland-fl/our-vets/
2. Местное облучение в перечисленных выше восьми филиалах: точные официальные ссылки находятся в unresolved / B01-Q02 JSON.
3. Конкретная местная иммунотерапия в семи филиалах из B01-Q06 и Maitland из B01-Q01: ссылки и точные вопросы в unresolved JSON.

---

# B01 — аудит 25 назначенных записей BluePearl

## Косвенные источники — дополнительная проверка 11 октября 2026

**Новый результат: иммунотерапию Cary обоснованно сохранить.** В интервью ImpriMed Ruslander прямо говорит, что они применяют Oncept и gilvetmab; выпуск датирован 12 апреля 2026. Современная официальная команда относит Ruslander к Cary. Факт применения препаратов подтверждён самим врачом; привязка к его нынешнему филиалу — явно обозначенный вывод, без гарантии наличия препарата и приёма конкретного пациента. Это не только клинический интерес.

- [Первичная стенограмма](https://www.imprimedicine.com/veterinary/content/dr-david-ruslander): «Melanoma vaccine and the Oncept. And also the gilvetmab». Проверено 2026-10-12T01:21:21.829124+00:00.
- [Дата выпуска у издателя](https://sites.libsyn.com/482088/david-ruslander-lifelong-learning-in-veterinary-oncology): Apr 12, 2026. Search result supplied date; direct Web-open returns 403, so that route is not claimed as full page read.
- [Текущая филиальная команда](https://bluepearlvet.com/hospital/cary-nc/our-vets/).

**Лучевая: косвенные результаты не подтвердили шесть местных аппаратов.** Практическое предложение для будущей интеграции — не показывать on-site RT как подтверждённую в Augusta, Brandon, Clearwater, Durham, Nashville и Port Washington. Это не «услуги нет» и не закрытие; это неподтверждённая физическая площадка.

- Port Washington: [PetCure/Lakeshore release от 20 января 2016](https://petcureoncology.com/wp-content/uploads/PetCure-Oncology-Partners-with-Lakeshore-Veterinary-Specialists.pdf) прямо размещает SRS в Glendale. Oak Creek и Port Washington названы как другие филиалы сети. Поэтому перенос RT на Port Washington логически не обоснован; сегодняшний referral маршрут из старого релиза не устанавливается.
- Brandon: [полный BringFido список](https://www.bringfido.com/resource/veterinarians/city/apollo-beach-fl-us/) относит описание radiation therapy к Fetch Brandon, не BluePearl. Поисковый фрагмент склеивал соседние карточки.
- Clearwater/Durham: вакансии при поиске города содержат соседние Tampa/Cary jobs. География поиска не является адресом работы. Из описания трёх клиник NC не следует наличие аппарата во всех трёх.
- Nashville: [oncology technician vacancy](https://www.simplyhired.com/job/RXIDv_B7uSO8TzlCwTfERTP0EZd0J1V4qIzWuSzl3SGozf6-oAOBIw) описывает обучение владельцев побочным эффектам radiation, но не работу с аппаратом. Это может сопровождать межфилиальное лечение и не устанавливает on-site RT.
- Augusta: общие сторонние списки добавляют множество специальностей без оборудования/назначенного врача; положительной конкретной зацепки не найдено. Отсутствие зацепки не доказательство отсутствия услуги.

**Maitland/Goodson:** новых надёжных сведений о текущем месте работы не найдено. Старые научные упоминания и устаревшие каталоги не дают текущую запись. Сохранять опубликованную медицинскую службу, но не представлять Goodson как подтверждённого текущего врача. Однофамильцы другой профессии исключены.

**Остальная иммунотерапия:** семь филиалов, кроме Cary, остаются без достаточного текущего branch-level подтверждения. Благодарность врачу в старой многоцентровой статье не доказывает, что именно его филиал проводил указанную иммунотерапию. Dermatology allergy immunotherapy и возможная будущая неназванная oral therapy не приняты как текущая anticancer услуга.

JSON: 54 предложения, из них последнее имеет статус supported_inference_proposal; 3 группы вопросов остаются, immunotherapy группа теперь содержит семь филиалов. Ничего не внесено в общую базу и не опубликовано.


## Углублённая проверка — дополнение от 11 октября 2026 (America/New_York)

Первый проход содержал ошибку чтения: ECT явно была опубликована в местных Treatment plans Arden Hills и BluePearl Fort Myers, но её ошибочно оставили unresolved. Ошибка исправлена; оригинальные timestamps не переписаны.

Сняты вопросы по ECT в обоих филиалах и местному оборудованию RT в Brentwood/Cary/Maitland. Для Malvern установлена точная площадка RT: Cancer Center, 50 Three Tun Rd.; нет основания автоматически показывать её по адресу Hospital 40. Три группы остаются: текущий назначенный medical-oncology врач Maitland; местное облучение в шести филиалах; anticancer immunotherapy в семи филиалах, кроме дополнительно подтверждённого Cary.

- **bluepearl-pet-hospital-arden-hills / local_service_verification.Electrochemotherapy**: "confirmed: ECT explicitly listed in branch Treatment plans"; [официальный источник](https://bluepearlvet.com/hospital/arden-hills-mn/specialties-services/oncology/); «Chemotherapy
Electrochemotherapy»; 2026-10-12T01:12:42.399041+00:00; scope BluePearl Pet Hospital – Arden Hills — 1285 Grey Fox Rd. Ste. 100; только arden-hills-mn. Метод: direct public-page text.
- **bluepearl-pet-hospital-fort-myers / local_service_verification.Electrochemotherapy**: "confirmed: ECT explicitly listed in branch Treatment plans"; [официальный источник](https://bluepearlvet.com/hospital/fort-myers-fl/specialties-services/oncology/); «Chemotherapy
Electrochemotherapy»; 2026-10-12T01:12:42.400715+00:00; scope BluePearl Pet Hospital – Fort Myers — 9500 Marketplace Rd.; только fort-myers-fl. Метод: direct public-page text.
- **bluepearl-pet-hospital-brentwood / local_service_verification.Radiation oncology**: "confirmed: current Brentwood team plus new hospital tour identifies on-site linear accelerator"; [официальный источник](https://www.linkedin.com/posts/bluepearl-vet_tour-our-bluepearl-brentwood-hospital-activity-7374534271455092738-LwJ5); «Our new linear accelerator for radiation oncology»; 2026-10-12T01:15:39.459233+00:00; scope BluePearl Pet Hospital – Brentwood — 1569 Mallory Ln. Bldg 200; только brentwood-tn. Метод: direct public-page text.
- **bluepearl-pet-hospital-orlando-maitland / local_service_verification.Radiation oncology**: "confirmed: on-site Linear Accelerator explicitly published by employer; Zulema Villa DACVR-RO on branch roster"; [официальный источник](https://careers.bluepearlvet.com/us/en/job/BVOBLUUSR247838EXTERNALENUS/Veterinarian-Critical-Care); «Linear Accelerator and a chemotherapy hood.»; 2026-10-12T01:13:51.286308+00:00; scope BluePearl Pet Hospital Orlando – Maitland — 9905 S U.S. Hwy. 17-92; только maitland-fl. Метод: public embedded phApp.ddo job description, not rendered shell.
- **bluepearl-pet-hospital-orlando-maitland / availability_note**: "Medical Oncology service and chemotherapy infrastructure remain advertised by BluePearl; named current medical-oncology clinician and Goodson availability unresolved."; [официальный источник](https://careers.bluepearlvet.com/us/en/job/BVOBLUUSR241138EXTERNALENUS/Veterinary-Internist); «Medical Oncology Radiation Oncology»; 2026-10-12T01:13:51.191168+00:00; scope BluePearl Pet Hospital Orlando – Maitland — 9905 S U.S. Hwy. 17-92; только maitland-fl. Метод: public embedded phApp.ddo job description, not rendered shell.
- **bluepearl-pet-hospital-cary / local_service_verification.Radiation oncology**: "confirmed: current official Radiation Oncology job in Cary + local Ruslander roster/treatment page; VCS equipment directory specifically identifies Cary Halcyon, not Durham."; [официальный источник](https://careers.bluepearlvet.com/us/en/job/BVOBLUUSR247572EXTERNALENUS/Veterinary-Technician-Radiation-Oncology); «Veterinary Technician - Radiation Oncology»; 2026-10-12T01:13:51.304610+00:00; scope BluePearl Pet Hospital – Cary — 6405-100 Tryon Rd.; только cary-nc. Метод: public embedded phApp.ddo job description, not rendered shell.
- **bluepearl-pet-hospital-malvern / radiation_treatment_location**: {"name": "BluePearl Veterinary CyberKnife Cancer Center", "street": "50 Three Tun Rd.", "city": "Malvern", "region": "PA", "postal_code": "19355", "phone": "610-296-2099", "website": "https://bluepearlvet.com/hospital/bluepearl-veterinary-cyberknife-cancer-center/", "equipment": ["CyberKnife", "Linear accelerator"], "note": "Do not attribute this equipment to Hospital at 40 Three Tun Rd.; no conclusion of absence at 40."}; [официальный источник](https://bluepearlvet.com/hospital/bluepearl-veterinary-cyberknife-cancer-center/); «we also use a linear accelerator for precision radiation on tumors»; 2026-10-12T00:56:04.226095+00:00; scope BluePearl Pet Hospital – Malvern — 40 Three Tun Rd.; только malvern-pa. Метод: direct public-page text.

Дополнительное подтверждение Cary: [VCS Radiation Facilities List](https://vetcancersociety.org/wp-content/uploads/2024/08/Radiation-Facilities-List.pdf), точная строка Cary/919-233-4911/David Ruslander/Halcyon. Это corroboration официальной врачебной организации, не самостоятельное доказательство сегодняшней комплектации. Вместе с нынешней местной командой и публичным employer Radiation Oncology record оно достаточно для сохранения услуги RT.

Maitland: [official current internist description](https://careers.bluepearlvet.com/us/en/job/BVOBLUUSR241138EXTERNALENUS/Veterinary-Internist) прямо перечисляет Medical Oncology/Radiation Oncology и local linear accelerator; [critical care description](https://careers.bluepearlvet.com/us/en/job/BVOBLUUSR247838EXTERNALENUS/Veterinarian-Critical-Care) — accelerator/chemotherapy hood. Описания получены из публичного встроенного phApp.ddo, поскольку reader отдаёт shell с job filled; извлечение публичных данных не выдано за браузерный просмотр. Имя врача этим не установлено.

Brentwood: старое employer description criticalist сохраняет прежние Franklin/2015/11,500 sqft. Оно не доказывает нынешнюю комплектацию. Использована собственная BluePearl видеоэкскурсия нового Brentwood с явным упоминанием линейного ускорителя, плюс действующая местная team page.

Иммунотерапия: проверены branch/drug-specific запросы для всех восьми филиалов. Allergy immunotherapy на dermatology не является противоопухолевой. [Официальная история Brentwood/Cosmo](https://www.linkedin.com/posts/bluepearl-vet_bluepearlbrentwood-collaborativecare-elevatingvetmed-activity-7482839347143110657-3BUN) говорит лишь о возможной будущей неназванной oral immunotherapy, поэтому не устанавливает конкретное текущее лечение.

По шести спорным RT филиалам дополнительный поиск по оборудованию, employer local descriptions и VCS не дал достаточного положительного местного подтверждения. Неполный перечень оборудования или отсутствие в VCS не доказывает отсутствия RT. Старые network/aggregator тексты не использованы для усиления услуги.

База и production не изменены. JSON содержит 54 предложения; 3 оставшиеся группы unresolved. Все добавленные изменения имеют исходное значение/явную пометку отсутствия, официальный источник, короткую точную цитату, время и branch_scope.


Дата посещений: 2026-10-12T00:53:10.602830+00:00 — 2026-10-12T00:56:04.225133+00:00 (UTC; в America/New_York 11 октября 2026).

Прочитаны актуальные AGENTS.md и PROJECT_OPERATIONS.md. Inventory и supplemental получены из remote main; исходные значения сохранены в этом отчёте/JSON. ACVIM-снимок дополнительно прочитан только для назначенных идентичностей. Общие файлы не изменены, коммитов и публикации нет. Trials и обращения в клиники не выполнялись.

Обработано 25/25 записей. 54 предложения (53 прежних и одно с явно обозначенным выводом) (в основном местные source URLs и заполнение пустых телефонов), 3 группы unresolved после углублённой проверки. Это завершённый просмотр доступных местных разделов, а не утверждение, что все услуги подтверждены. Закрытие ни одного филиала не установлено. Внешнего запрета доступа к требуемым действующим местным страницам не встретилось.

## Как читать результат

Контакты и рабочий официальный маршрут подтверждены по местному overview. Услуги сверены с branch services, team, oncology и surgery. Лучевая в шаблонном Treatment plans/FAQ не принята автоматически; diagnostic radiology, I-131 при гипертиреозе и прошлый опыт не превращены в противоопухолевую лучевую. Общий Surgery не превращён в Surgical oncology. Сертификации — утверждения официальных страниц, без независимой проверки лицензий. Неуказанная board certification не означает доказанное отсутствие сертификата.

Все филиалы представлены как физический приём по предварительной specialty appointment: телефон/местная форма доступны. Oncology страницы предлагают прямой звонок либо направление primary vet; это не обязательное направление. Формы просят сведения о primary veterinarian, но не доказывают юридическое требование направления. Мобильная онкология и дистанционный owner oncology приём для этих 25 не подтверждены; hospice/home services не приравнены к мобильному противоопухолевому лечению.

Предложения JSON не являются патчем: перед интеграцией сверить свежий main, найти supplemental строки по идентичности/URL, сохранить raw ACVIM профили. Поля source_id не всегда присутствуют в supplemental; отчёт не создаёт фиктивную исходную строку. Спорные services не удалены из предлагаемого списка без доказательства/решения владельца.

## Оставшиеся проблемные вопросы после углублённой проверки

### B01-Q01. Кто сейчас назначен на медицинскую онкологию в Maitland, принимает ли Teresa Goodson, какая противоопухолевая иммунотерапия фактически доступна?

Medical Oncology и chemotherapy hood опубликованы в нынешних official job descriptions. Goodson отсутствует в прямых team/oncology/internal-medicine, но сохранилась в поисковых копиях. Нельзя вывести уход/пенсию/закрытие; текущая назначенная медицинская команда не установлена.

- [BluePearl Pet Hospital Orlando – Maitland — 9905 S U.S. Hwy. 17-92; только maitland-fl](https://bluepearlvet.com/hospital/maitland-fl/specialties-services/oncology/)

### B01-Q02. Есть ли облучение непосредственно в каждом из этих шести филиалов, и где оно проводится?

Radiation есть в повторяющемся Treatment plans; локальное оборудование/радиационная команда не установлены после чтения overview, services, team, oncology, surgery, booking, referring-vets. Existing Radiation oncology сохраняется как спорное, не удалено.

- [BluePearl Pet Hospital – Augusta — 410 Topgolf Way; только augusta-ga](https://bluepearlvet.com/hospital/augusta-ga/specialties-services/oncology/)
- [BluePearl Pet Hospital – Brandon — 607 Lumsden Professional Ct.; только brandon-fl](https://bluepearlvet.com/hospital/brandon-fl/specialties-services/oncology/)
- [BluePearl Pet Hospital – Clearwater — 4701 Ulmerton Rd. Ste. 500; только clearwater-fl](https://bluepearlvet.com/hospital/clearwater-fl/specialties-services/oncology/)
- [BluePearl Pet Hospital – Durham — 7015 NC Hwy. 751; только durham-nc](https://bluepearlvet.com/hospital/durham-nc/specialties-services/oncology/)
- [BluePearl Pet Hospital – Nashville — 2409 21st Ave S; только nashville-tn](https://bluepearlvet.com/hospital/nashville-tn/specialties-services/oncology/)
- [BluePearl Pet Hospital – Port Washington — 207 W Seven Hills Rd; только port-washington-wi](https://bluepearlvet.com/hospital/port-washington-wi/specialties-services/oncology/)

### B01-Q06. Какая конкретная иммунотерапия доступна в каждом из этих филиалов на месте?

Existing Immunotherapy есть в supplemental, но FAQ сети/интерес врача/мультимодальное планирование не подтверждают конкретный филиальный доступ. Не удалять молча. Lafayette подтверждает её напрямую; Malvern и Christiana описывают применение у обслуживающих врачей, отдельно от общего FAQ.

- [BluePearl Pet Hospital – Augusta — 410 Topgolf Way; только augusta-ga](https://bluepearlvet.com/hospital/augusta-ga/specialties-services/oncology/)
- [BluePearl Pet Hospital – Brandon — 607 Lumsden Professional Ct.; только brandon-fl](https://bluepearlvet.com/hospital/brandon-fl/specialties-services/oncology/)
- [BluePearl Pet Hospital – Brentwood — 1569 Mallory Ln. Bldg 200; только brentwood-tn](https://bluepearlvet.com/hospital/brentwood-tn/specialties-services/oncology/)
- [BluePearl Pet Hospital – Clearwater — 4701 Ulmerton Rd. Ste. 500; только clearwater-fl](https://bluepearlvet.com/hospital/clearwater-fl/specialties-services/oncology/)
- [BluePearl Pet Hospital – Durham — 7015 NC Hwy. 751; только durham-nc](https://bluepearlvet.com/hospital/durham-nc/specialties-services/oncology/)
- [BluePearl Pet Hospital – Nashville — 2409 21st Ave S; только nashville-tn](https://bluepearlvet.com/hospital/nashville-tn/specialties-services/oncology/)
- [BluePearl Pet Hospital – Port Washington — 207 W Seven Hills Rd; только port-washington-wi](https://bluepearlvet.com/hospital/port-washington-wi/specialties-services/oncology/)

## Все 25 результатов

### 1. Blue Pearl- Summerville — `blue-pearl-summerville`

**branch_scope:** Blue Pearl- Summerville — 319 E 3rd N St; только summerville-sc
**Контакт:** 843.216.1331 | 319 E 3rd N St | Summerville, | SC                                    29483 · 843-216-1331.
**Проверка:** 2026-10-12T00:53:10.602830+00:00; действующий официальный overview с текущими контактами/записью.

Kathryn Taylor — medical oncology. Химиотерапия указана в местном Treatment plans; общая Surgery подтверждена, специализированная онкологическая хирургия отдельно не установлена.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Henri Bianucci — DVM, DACVS; Surgery.
- Hannah Ghindea — DVM; Surgery.
- Kelsey Goode — DVM, DACVS (SA); Surgery.
- Sean Schubmehl — DVM, DACVS (SA); Surgery.
- Kathryn Taylor — DVM, MS, DACVIM (Oncology); Oncology.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

Назначенная запись не найдена в supplemental по source_id/названию/совпадающему master URL; старые supplemental поля недоступны. Это не означает отсутствия записи в итоговом построенном каталоге.

Исторический ACVIM-снимок: Kathryn Holley Taylor, DVM, DACVIM (Oncology); адрес 319 East 3rd North St / Summerville, SC 29483; телефон ``. Это baseline, не доказательство текущего приёма.

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/summerville-sc/) — «BluePearl Pet Hospital | Summerville, SC»; 2026-10-12T00:53:10.602830+00:00; HTTP 200; scope `summerville-sc`.
- [Local services](https://bluepearlvet.com/hospital/summerville-sc/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Summerville SC»; 2026-10-12T00:53:10.605345+00:00; HTTP 200; scope `summerville-sc`.
- [Local team](https://bluepearlvet.com/hospital/summerville-sc/our-vets/) — «BluePearl Pet Hospital | Summerville, SC | Our Vets»; 2026-10-12T00:53:10.603525+00:00; HTTP 200; scope `summerville-sc`.
- [Oncology](https://bluepearlvet.com/hospital/summerville-sc/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Summerville SC»; 2026-10-12T00:53:10.607150+00:00; HTTP 200; scope `summerville-sc`.
- [Surgery](https://bluepearlvet.com/hospital/summerville-sc/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Summerville SC»; 2026-10-12T00:53:55.590346+00:00; HTTP 200; scope `summerville-sc`.
- [Appointment](https://bluepearlvet.com/hospital/summerville-sc/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:53:55.591573+00:00; HTTP 200; scope `summerville-sc`.
- [Referring vets](https://bluepearlvet.com/hospital/summerville-sc/referring-vets/) — «BluePearl Pet Hospital | Summerville, SC | Referring Vets»; 2026-10-12T00:55:57.569470+00:00; HTTP 200; scope `summerville-sc`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** master_url, supporting_urls, phone.
**Unresolved:** отдельных вопросов по исходным утверждениям не осталось; непубликуемые дополнительные услуги не добавлены.

### 2. Blue Pearl Veterinary Partners — `blue-pearl-veterinary-partners`

**branch_scope:** Blue Pearl Veterinary Partners — 410 W 55th St.; только midtown-nyc
**Контакт:** 212.767.0099 | 212.767.0098 | 410 W 55th St. | New York, | NY                                    10019 · 212-767-0099.
**Проверка:** 2026-10-12T00:54:19.153872+00:00; действующий официальный overview с текущими контактами/записью.

John Farrelly — DACVIM (Oncology), DACVR-RO; Timothy Rocha — DACVIM (Oncology). Лучевая подтверждена местным описанием линейного ускорителя, не только сертификацией врача. Исходный адрес 410 West 55th Street однозначно соответствует Midtown, а не всей сети New York.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- John Farrelly — DVM, MS, DACVIM (Oncology), DACVR-RO; Oncology, Radiation Oncology.
- Canny Fung — DVM, DACVS (SA); Surgery.
- Timothy Rocha — DVM, DACVIM (Oncology); Oncology.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

Назначенная запись не найдена в supplemental по source_id/названию/совпадающему master URL; старые supplemental поля недоступны. Это не означает отсутствия записи в итоговом построенном каталоге.

Исторический ACVIM-снимок: John Farrelly, DVM, MS, MBA, DACVIM (Oncology), DACVR (Radiation Oncology); адрес 410 West 55th Street / New York, NY 10019; телефон `212.767.0099`. Это baseline, не доказательство текущего приёма.

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/midtown-nyc/) — «BluePearl Pet Hospital Midtown | New York, NY»; 2026-10-12T00:54:19.153872+00:00; HTTP 200; scope `midtown-nyc`.
- [Local services](https://bluepearlvet.com/hospital/midtown-nyc/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists New York NY»; 2026-10-12T00:54:19.389015+00:00; HTTP 200; scope `midtown-nyc`.
- [Local team](https://bluepearlvet.com/hospital/midtown-nyc/our-vets/) — «BluePearl Pet Hospital | Midtown NYC, NY | Our Vets»; 2026-10-12T00:54:19.249686+00:00; HTTP 200; scope `midtown-nyc`.
- [Oncology](https://bluepearlvet.com/hospital/midtown-nyc/specialties-services/oncology/) — «Veterinary Oncology by BluePearl New York NY»; 2026-10-12T00:54:19.399993+00:00; HTTP 200; scope `midtown-nyc`.
- [Surgery](https://bluepearlvet.com/hospital/midtown-nyc/specialties-services/surgery/) — «Veterinary Surgery by BluePearl New York NY»; 2026-10-12T00:54:21.912212+00:00; HTTP 200; scope `midtown-nyc`.
- [Appointment](https://bluepearlvet.com/hospital/midtown-nyc/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:21.961588+00:00; HTTP 200; scope `midtown-nyc`.
- [Referring vets](https://bluepearlvet.com/hospital/midtown-nyc/referring-vets/) — «BluePearl Pet Hospital | Midtown NYC, NY | Referring Vets»; 2026-10-12T00:56:04.158136+00:00; HTTP 200; scope `midtown-nyc`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** master_url, supporting_urls.
**Unresolved:** отдельных вопросов по исходным утверждениям не осталось; непубликуемые дополнительные услуги не добавлены.

### 3. BluePearl Kirkland — `bluepearl-kirkland`

**branch_scope:** BluePearl Kirkland — 11814 115th Ave. NE Bldg. J; только kirkland-wa
**Контакт:** 425.823.9111 | 425.823.4008 | 11814 115th Ave. NE                                    Bldg. J | Kirkland, | WA                                    98034 · 425-823-9111.
**Проверка:** 2026-10-12T00:53:10.612442+00:00; действующий официальный overview с текущими контактами/записью.

Kevin Choy — DACVIM (Oncology). Aidan Chambers — DACVS (SA), текущий интерес к surgical oncology; Peter Laminette — хирургический резидент без опубликованной board certification. Не приписывать хирургам DACVIM Oncology.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Aidan Chambers — VMD, DACVS (SA); Surgery.
- Kevin Choy — BVSc, MS, DACVIM (Oncology); Oncology.
- Mark Engen — DVM, DACVS; Surgery.
- Peter Laminette — MS, DVM; Surgery.
- Kent Vince — DVM, MSpVM, DACVS (SA); Surgery.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

Назначенная запись не найдена в supplemental по source_id/названию/совпадающему master URL; старые supplemental поля недоступны. Это не означает отсутствия записи в итоговом построенном каталоге.

Исторический ACVIM-снимок: Kevin Choy, BVSc (Hons), MS, DACVIM (Oncology); адрес BluePearl Kirkland / 11814 115th Ave NE Bldg J / Kirkland, WA 98034; телефон `425.823.9111`. Это baseline, не доказательство текущего приёма.

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/kirkland-wa/) — «BluePearl Pet Hospital | Kirkland, WA»; 2026-10-12T00:53:10.612442+00:00; HTTP 200; scope `kirkland-wa`.
- [Local services](https://bluepearlvet.com/hospital/kirkland-wa/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Kirkland WA»; 2026-10-12T00:53:14.009357+00:00; HTTP 200; scope `kirkland-wa`.
- [Local team](https://bluepearlvet.com/hospital/kirkland-wa/our-vets/) — «BluePearl Pet Hospital | Kirkland, WA | Our Vets»; 2026-10-12T00:53:10.614195+00:00; HTTP 200; scope `kirkland-wa`.
- [Oncology](https://bluepearlvet.com/hospital/kirkland-wa/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Kirkland WA»; 2026-10-12T00:53:14.042837+00:00; HTTP 200; scope `kirkland-wa`.
- [Surgery](https://bluepearlvet.com/hospital/kirkland-wa/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Kirkland WA»; 2026-10-12T00:53:55.596808+00:00; HTTP 200; scope `kirkland-wa`.
- [Appointment](https://bluepearlvet.com/hospital/kirkland-wa/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:53:55.597726+00:00; HTTP 200; scope `kirkland-wa`.
- [Referring vets](https://bluepearlvet.com/hospital/kirkland-wa/referring-vets/) — «BluePearl Pet Hospital | Kirkland, WA | Referring Vets»; 2026-10-12T00:55:57.569818+00:00; HTTP 200; scope `kirkland-wa`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** master_url, supporting_urls.
**Unresolved:** отдельных вопросов по исходным утверждениям не осталось; непубликуемые дополнительные услуги не добавлены.

### 4. Bluepearl Pet Hospital — `bluepearl-pet-hospital`

**branch_scope:** Bluepearl Pet Hospital — 2100 W Silver Spring Dr; только glendale-wi
**Контакт:** 414.540.6710 | 2100 W Silver Spring Dr | Glendale, | WI                                    53209 · 414-540-6710.
**Проверка:** 2026-10-12T00:53:14.117318+00:00; действующий официальный overview с текущими контактами/записью.

Rachel Reiman — DACVIM (Oncology), обслуживает также Port Washington. Matt Stepnik — DACVS (SA), местная биография описывает онкологические операции. Elke Rudloff — DACVECC, hospice, не сертифицированный медицинский онколог.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Rachel Reiman — DVM, DACVIM (Oncology); Oncology.
- Matt Stepnik — DVM, DACVS (SA); Surgery.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

Назначенная запись не найдена в supplemental по source_id/названию/совпадающему master URL; старые supplemental поля недоступны. Это не означает отсутствия записи в итоговом построенном каталоге.

Исторический ACVIM-снимок: Rachel A. Reiman, DVM, DACVIM (Oncology); адрес 2100 W. Silver Spring Dr. / Glendale, WI 53209; телефон `414.540.6710`. Это baseline, не доказательство текущего приёма.

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/glendale-wi/) — «BluePearl Pet Hospital | Glendale, WI»; 2026-10-12T00:53:14.117318+00:00; HTTP 200; scope `glendale-wi`.
- [Local services](https://bluepearlvet.com/hospital/glendale-wi/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Glendale WI»; 2026-10-12T00:53:14.120413+00:00; HTTP 200; scope `glendale-wi`.
- [Local team](https://bluepearlvet.com/hospital/glendale-wi/our-vets/) — «BluePearl Pet Hospital | Glendale, WI | Our Vets»; 2026-10-12T00:53:14.119051+00:00; HTTP 200; scope `glendale-wi`.
- [Oncology](https://bluepearlvet.com/hospital/glendale-wi/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Glendale WI»; 2026-10-12T00:53:14.148660+00:00; HTTP 200; scope `glendale-wi`.
- [Surgery](https://bluepearlvet.com/hospital/glendale-wi/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Glendale WI»; 2026-10-12T00:53:58.707953+00:00; HTTP 200; scope `glendale-wi`.
- [Appointment](https://bluepearlvet.com/hospital/glendale-wi/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:53:58.817114+00:00; HTTP 200; scope `glendale-wi`.
- [Referring vets](https://bluepearlvet.com/hospital/glendale-wi/referring-vets/) — «BluePearl Pet Hospital | Glendale, WI | Referring Vets»; 2026-10-12T00:55:57.571410+00:00; HTTP 200; scope `glendale-wi`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** master_url, supporting_urls.
**Unresolved:** отдельных вопросов по исходным утверждениям не осталось; непубликуемые дополнительные услуги не добавлены.

### 5. BluePearl Pet Hospital – Arden Hills — `bluepearl-pet-hospital-arden-hills`

**branch_scope:** BluePearl Pet Hospital – Arden Hills — 1285 Grey Fox Rd. Ste. 100; только arden-hills-mn
**Контакт:** 763.754.5000 | 763.754.6002 | 1285 Grey Fox Rd.                                    Ste. 100 | Arden Hills, | MN                                    55112 · 763-754-5000.
**Проверка:** 2026-10-12T00:53:14.335285+00:00; действующий официальный overview с текущими контактами/записью.

ECT подтверждена прямым местным Treatment plans, не только интересом Megan Duffy. Первое заключение B01 об insufficient ECT было ошибкой чтения; подтверждающая строка уже была в первоначальных сохранённых данных.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Antonella Borgatti — DVM, MS, DACVIM (Oncology), DECVIM-CA; Oncology.
- Carly Campbell — DVM; Surgery.
- Haley Carlson — DVM; Dentistry & Oral Surgery.
- Megan Duffy — DVM, MS, DACVIM (Oncology); Oncology.
- Emily Edstrom — DVM, DAVDC; Dentistry & Oral Surgery.
- Bishoy Eskander — DVM, DACVS (SA); Surgery.
- Donnell Hansen — DVM, DAVDC; Dentistry & Oral Surgery.
- Andrew Jackson — DVM, DACVS; Surgery.
- Alexandra Kalamaras — DVM, MS, DACVS (SA); Surgery.
- Adriana Kalaska — DVM; Surgery.
- Kathryn Kaufman — DVM, DACVS (SA); Surgery.
- Maddie McDermott — DVM; Surgery.
- Joseph Rogers — DVM; Surgery.
- Melissa Tye — DVM; Surgery.
- Jeff Yu — DVM, DACVS (SA); Surgery.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

Назначенная запись не найдена в supplemental по source_id/названию/совпадающему master URL; старые supplemental поля недоступны. Это не означает отсутствия записи в итоговом построенном каталоге.

Исторический ACVIM-снимок: Megan Duffy, DVM, MS, DACVIM (Oncology); адрес 1285 Grey Fox Road / Arden Hills, MN 55112; телефон ``. Это baseline, не доказательство текущего приёма.

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/arden-hills-mn/) — «BluePearl Pet Hospital | Arden Hills, MN»; 2026-10-12T00:53:14.335285+00:00; HTTP 200; scope `arden-hills-mn`.
- [Local services](https://bluepearlvet.com/hospital/arden-hills-mn/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Arden Hills MN»; 2026-10-12T00:53:14.387051+00:00; HTTP 200; scope `arden-hills-mn`.
- [Local team](https://bluepearlvet.com/hospital/arden-hills-mn/our-vets/) — «BluePearl Pet Hospital | Arden Hills, MN | Our Vets»; 2026-10-12T00:53:14.372120+00:00; HTTP 200; scope `arden-hills-mn`.
- [Oncology](https://bluepearlvet.com/hospital/arden-hills-mn/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Arden Hills MN»; 2026-10-12T00:53:14.879163+00:00; HTTP 200; scope `arden-hills-mn`.
- [Surgery](https://bluepearlvet.com/hospital/arden-hills-mn/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Arden Hills MN»; 2026-10-12T00:53:58.843509+00:00; HTTP 200; scope `arden-hills-mn`.
- [Appointment](https://bluepearlvet.com/hospital/arden-hills-mn/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:53:59.004341+00:00; HTTP 200; scope `arden-hills-mn`.
- [Referring vets](https://bluepearlvet.com/hospital/arden-hills-mn/referring-vets/) — «BluePearl Pet Hospital | Arden Hills, MN | Referring Vets»; 2026-10-12T00:55:57.573208+00:00; HTTP 200; scope `arden-hills-mn`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** master_url, supporting_urls, phone.
**Unresolved:** вопросы первого прохода сняты; см. углублённую проверку.

### 6. BluePearl Pet Hospital – Auburn Hills — `bluepearl-pet-hospital-auburn-hills`

**branch_scope:** BluePearl Pet Hospital – Auburn Hills — 3412 E Walton Blvd.; только auburn-hills-mi
**Контакт:** 248.371.3713 | 248.371.3714 | 3412 E Walton Blvd. | Auburn Hills, | MI                                    48326 · 248-371-3713.
**Проверка:** 2026-10-12T00:53:16.792851+00:00; действующий официальный overview с текущими контактами/записью.

Eric Bulakowski — DACVIM (Oncology). Местный список услуг: emergency и oncology; не переносить хирургию или лучевую из общего блока oncology Treatment plans в подтверждённые фильтры.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Eric Bulakowski — DVM, DACVIM (Oncology); Oncology.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

Назначенная запись не найдена в supplemental по source_id/названию/совпадающему master URL; старые supplemental поля недоступны. Это не означает отсутствия записи в итоговом построенном каталоге.

Исторический ACVIM-снимок: Eric J. Bulakowski, DVM, DACVIM (Oncology); адрес 3412 East Walton Blvd / Auburn Hills, MI 48326; телефон ``. Это baseline, не доказательство текущего приёма.

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/auburn-hills-mi/) — «24 Hour Emergency Vet in Auburn Hills, MI | BluePearl Pet Hospital»; 2026-10-12T00:53:16.792851+00:00; HTTP 200; scope `auburn-hills-mi`.
- [Local services](https://bluepearlvet.com/hospital/auburn-hills-mi/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Auburn Hills MI»; 2026-10-12T00:53:16.874416+00:00; HTTP 200; scope `auburn-hills-mi`.
- [Local team](https://bluepearlvet.com/hospital/auburn-hills-mi/our-vets/) — «BluePearl Pet Hospital | Auburn Hills, MI | Our Vets»; 2026-10-12T00:53:16.865786+00:00; HTTP 200; scope `auburn-hills-mi`.
- [Oncology](https://bluepearlvet.com/hospital/auburn-hills-mi/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Auburn Hills MI»; 2026-10-12T00:53:16.941498+00:00; HTTP 200; scope `auburn-hills-mi`.
- [Surgery](https://bluepearlvet.com/hospital/auburn-hills-mi/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Auburn Hills MI»; 2026-10-12T00:53:59.037333+00:00; HTTP 200; scope `auburn-hills-mi`.
- [Appointment](https://bluepearlvet.com/hospital/auburn-hills-mi/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:53:59.067705+00:00; HTTP 200; scope `auburn-hills-mi`.
- [Referring vets](https://bluepearlvet.com/hospital/auburn-hills-mi/referring-vets/) — «BluePearl Pet Hospital | Auburn Hills, MI | Referring Vets»; 2026-10-12T00:55:57.573909+00:00; HTTP 200; scope `auburn-hills-mi`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** master_url, supporting_urls, phone.
**Unresolved:** отдельных вопросов по исходным утверждениям не осталось; непубликуемые дополнительные услуги не добавлены.

### 7. BluePearl Pet Hospital – Augusta — `bluepearl-pet-hospital-augusta`

**branch_scope:** BluePearl Pet Hospital – Augusta — 410 Topgolf Way; только augusta-ga
**Контакт:** 706.733.7458 | 706.737.4399 | 410 Topgolf Way | Augusta, | GA                                    30909 · 706-733-7458.
**Проверка:** 2026-10-12T00:53:16.954400+00:00; действующий официальный overview с текущими контактами/записью.

Paul Rossman — DVM, MS, DACVIM (Oncology); статус подтверждён строкой Diplomate в Education, даже без отдельного Board Certified заголовка. Kevin Kunkel — DACVS (SA), хирург; его профиль не подтверждает отдельную онкохирургическую специализацию.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Kevin Kunkel — DVM, DACVS (SA); Surgery.
- Paul Rossman — DVM, MS, DACVIM (Oncology); Oncology.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

```json
{
  "name": "BluePearl Pet Hospital – Augusta",
  "street": "410 Topgolf Way",
  "city": "Augusta",
  "region": "GA",
  "postal_code": "30909",
  "phone": "706-733-7458",
  "website": "https://bluepearlvet.com/hospital/augusta-ga/specialties-services/oncology/",
  "services": [
    "Medical oncology",
    "Chemotherapy",
    "Radiation oncology",
    "Immunotherapy",
    "Surgery"
  ]
}
```

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/augusta-ga/) — «BluePearl Pet Hospital | Augusta, GA»; 2026-10-12T00:53:16.954400+00:00; HTTP 200; scope `augusta-ga`.
- [Local services](https://bluepearlvet.com/hospital/augusta-ga/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Augusta GA»; 2026-10-12T00:53:16.983083+00:00; HTTP 200; scope `augusta-ga`.
- [Local team](https://bluepearlvet.com/hospital/augusta-ga/our-vets/) — «BluePearl Pet Hospital | Augusta, GA | Our Vets»; 2026-10-12T00:53:16.960959+00:00; HTTP 200; scope `augusta-ga`.
- [Oncology](https://bluepearlvet.com/hospital/augusta-ga/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Augusta GA»; 2026-10-12T00:53:16.984156+00:00; HTTP 200; scope `augusta-ga`.
- [Surgery](https://bluepearlvet.com/hospital/augusta-ga/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Augusta GA»; 2026-10-12T00:53:59.505415+00:00; HTTP 200; scope `augusta-ga`.
- [Appointment](https://bluepearlvet.com/hospital/augusta-ga/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:01.690751+00:00; HTTP 200; scope `augusta-ga`.
- [Referring vets](https://bluepearlvet.com/hospital/augusta-ga/referring-vets/) — «BluePearl Pet Hospital | Augusta, GA | Referring Vets»; 2026-10-12T00:55:57.574765+00:00; HTTP 200; scope `augusta-ga`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** supporting_urls.
**Unresolved:** B01-Q02, B01-Q06.

### 8. BluePearl Pet Hospital – Brandon — `bluepearl-pet-hospital-brandon`

**branch_scope:** BluePearl Pet Hospital – Brandon — 607 Lumsden Professional Ct.; только brandon-fl
**Контакт:** 813.571.3303 | 813.571.3373 | 607 Lumsden Professional Ct. | Brandon, | FL                                    33511 · 813-571-3303.
**Проверка:** 2026-10-12T00:53:16.985338+00:00; действующий официальный overview с текущими контактами/записью.

Jen Coyle — DACVIM (Oncology), обслуживает Brandon и Tampa. Местная химия и хирургическая служба опубликованы; лучевая и иммунотерапия требуют более конкретного филиального подтверждения.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Jen Coyle — DVM, DACVIM (Oncology); Oncology.
- Elena Pfisterer — DVM, DACVS (SA); Surgery.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

```json
{
  "name": "BluePearl Pet Hospital – Brandon",
  "street": "607 Lumsden Professional Court",
  "city": "Brandon",
  "region": "FL",
  "postal_code": "33511",
  "phone": "813-571-3303",
  "website": "https://bluepearlvet.com/hospital/brandon-fl/specialties-services/oncology/",
  "services": [
    "Medical oncology",
    "Chemotherapy",
    "Radiation oncology",
    "Immunotherapy",
    "Surgery"
  ]
}
```

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/brandon-fl/) — «BluePearl Pet Hospital | Brandon, FL»; 2026-10-12T00:53:16.985338+00:00; HTTP 200; scope `brandon-fl`.
- [Local services](https://bluepearlvet.com/hospital/brandon-fl/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Brandon FL»; 2026-10-12T00:53:19.472088+00:00; HTTP 200; scope `brandon-fl`.
- [Local team](https://bluepearlvet.com/hospital/brandon-fl/our-vets/) — «BluePearl Pet Hospital | Brandon, FL | Our Vets»; 2026-10-12T00:53:17.038378+00:00; HTTP 200; scope `brandon-fl`.
- [Oncology](https://bluepearlvet.com/hospital/brandon-fl/specialties-services/oncology/) — «Veterinary Oncology in Brandon, FL | BluePearl Pet Hospital Brandon FL»; 2026-10-12T00:53:19.474678+00:00; HTTP 200; scope `brandon-fl`.
- [Surgery](https://bluepearlvet.com/hospital/brandon-fl/specialties-services/surgery/) — «Veterinary Surgery in Brandon, FL | BluePearl Pet Hospital Brandon FL»; 2026-10-12T00:54:01.725110+00:00; HTTP 200; scope `brandon-fl`.
- [Appointment](https://bluepearlvet.com/hospital/brandon-fl/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:01.726609+00:00; HTTP 200; scope `brandon-fl`.
- [Referring vets](https://bluepearlvet.com/hospital/brandon-fl/referring-vets/) — «BluePearl Pet Hospital | Brandon, FL | Referring Vets»; 2026-10-12T00:55:57.575482+00:00; HTTP 200; scope `brandon-fl`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** supporting_urls.
**Unresolved:** B01-Q02, B01-Q06.

### 9. BluePearl Pet Hospital – Brentwood — `bluepearl-pet-hospital-brentwood`

**branch_scope:** BluePearl Pet Hospital – Brentwood — 1569 Mallory Ln. Bldg 200; только brentwood-tn
**Контакт:** 615.333.1212 | 615.661.9883 | 1569 Mallory Ln.                                    Bldg 200 | Brentwood, | TN                                    37027 · 615-333-1212.
**Проверка:** 2026-10-12T00:53:19.591514+00:00; действующий официальный overview с текущими контактами/записью.

Местная лучевая подтверждена официальной видеоэкскурсией BluePearl: new linear accelerator for radiation oncology; текущая Jean Rogers DACVR-RO относится к этому филиалу. Старое объявление criticalist всё ещё описывает прежний Franklin и не использовано как подтверждение нынешнего оборудования.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Kevin Au — BVMS, MS, DACVS (SA); Surgery.
- Sarah Daniel — DVM, DACVS (SA); Surgery.
- Brianna Jacobs — DVM; Oncology.
- Rebecca Laube — DVM, DACVS (SA); Surgery.
- Francesca Lerner — DVM, MS; Oncology.
- Pamela Lucas — DVM, MS, DACVIM (Oncology); Oncology.
- Jean Rogers — DVM, DACVR-RO; Radiation Oncology.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

```json
{
  "name": "BluePearl Pet Hospital – Brentwood",
  "street": "1569 Mallory Lane, Building 200",
  "city": "Brentwood",
  "region": "TN",
  "postal_code": "37027",
  "phone": "615-333-1212",
  "website": "https://bluepearlvet.com/hospital/brentwood-tn/specialties-services/oncology/",
  "services": [
    "Medical oncology",
    "Chemotherapy",
    "Radiation oncology",
    "Immunotherapy",
    "Surgery"
  ]
}
```

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/brentwood-tn/) — «BluePearl Pet Hospital | Brentwood, TN»; 2026-10-12T00:53:19.591514+00:00; HTTP 200; scope `brentwood-tn`.
- [Local services](https://bluepearlvet.com/hospital/brentwood-tn/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Brentwood TN»; 2026-10-12T00:53:19.638412+00:00; HTTP 200; scope `brentwood-tn`.
- [Local team](https://bluepearlvet.com/hospital/brentwood-tn/our-vets/) — «BluePearl Pet Hospital | Brentwood, TN | Our Vets»; 2026-10-12T00:53:19.636664+00:00; HTTP 200; scope `brentwood-tn`.
- [Oncology](https://bluepearlvet.com/hospital/brentwood-tn/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Brentwood TN»; 2026-10-12T00:53:19.644844+00:00; HTTP 200; scope `brentwood-tn`.
- [Surgery](https://bluepearlvet.com/hospital/brentwood-tn/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Brentwood TN»; 2026-10-12T00:54:01.730112+00:00; HTTP 200; scope `brentwood-tn`.
- [Appointment](https://bluepearlvet.com/hospital/brentwood-tn/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:01.819801+00:00; HTTP 200; scope `brentwood-tn`.
- [Referring vets](https://bluepearlvet.com/hospital/brentwood-tn/referring-vets/) — «BluePearl Pet Hospital | Brentwood, TN | Referring Vets»; 2026-10-12T00:55:57.576585+00:00; HTTP 200; scope `brentwood-tn`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** supporting_urls.
**Unresolved:** B01-Q06

### 10. BluePearl Pet Hospital – Cary — `bluepearl-pet-hospital-cary`

**branch_scope:** BluePearl Pet Hospital – Cary — 6405-100 Tryon Rd.; только cary-nc
**Контакт:** 919.233.4911 | 919.854.1155 | 6405-100 Tryon Rd. | Cary, | NC                                    27518 · 919-233-4911.
**Проверка:** 2026-10-12T00:53:19.645650+00:00; действующий официальный overview с текущими контактами/записью.

Местная лучевая подтверждена совокупностью текущего официального employer Radiation Oncology job, местного врача Ruslander/oncology page и точной записи VCS о Cary Halcyon. Название/модель не переносится в Durham; VCS directory corroboration не является самопроверкой сертификации.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Courtney Bounds — DVM, MS; Surgery.
- Sarah Christie — DVM; Surgery.
- Meghan Kruse — DVM, DACVS (SA); Surgery.
- David Lee — DVM, DACVS; Surgery.
- Emily Lemoine — DVM; Oncology.
- David Ruslander — DVM, DACVIM (Oncology), DACVR-RO; Oncology, Radiation Oncology.
- Susan Shapiro — PhD, DVM, DACVIM (Oncology); Oncology.
- KP Spivey — DVM, DACVS (SA); Surgery.
- Carly Stevens — DVM, DACVIM (Oncology); Oncology.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

```json
{
  "name": "BluePearl Pet Hospital – Cary",
  "street": "6405-100 Tryon Road",
  "city": "Cary",
  "region": "NC",
  "postal_code": "27518",
  "phone": "919-233-4911",
  "website": "https://bluepearlvet.com/hospital/cary-nc/specialties-services/oncology/",
  "services": [
    "Medical oncology",
    "Chemotherapy",
    "Radiation oncology",
    "Immunotherapy",
    "Surgery"
  ]
}
```

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/cary-nc/) — «BluePearl Pet Hospital | Cary, NC»; 2026-10-12T00:53:19.645650+00:00; HTTP 200; scope `cary-nc`.
- [Local services](https://bluepearlvet.com/hospital/cary-nc/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Cary NC»; 2026-10-12T00:53:19.683133+00:00; HTTP 200; scope `cary-nc`.
- [Local team](https://bluepearlvet.com/hospital/cary-nc/our-vets/) — «BluePearl Pet Hospital | Cary, NC | Our Vets»; 2026-10-12T00:53:19.666403+00:00; HTTP 200; scope `cary-nc`.
- [Oncology](https://bluepearlvet.com/hospital/cary-nc/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Cary NC»; 2026-10-12T00:53:19.690177+00:00; HTTP 200; scope `cary-nc`.
- [Surgery](https://bluepearlvet.com/hospital/cary-nc/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Cary NC»; 2026-10-12T00:54:01.826090+00:00; HTTP 200; scope `cary-nc`.
- [Appointment](https://bluepearlvet.com/hospital/cary-nc/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:01.898130+00:00; HTTP 200; scope `cary-nc`.
- [Referring vets](https://bluepearlvet.com/hospital/cary-nc/referring-vets/) — «BluePearl Pet Hospital | Cary, NC | Referring Vets»; 2026-10-12T00:55:57.577412+00:00; HTTP 200; scope `cary-nc`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** supporting_urls.
**Unresolved:** B01-Q06

### 11. BluePearl Pet Hospital – Christiana — `bluepearl-pet-hospital-christiana`

**branch_scope:** BluePearl Pet Hospital – Christiana — 106 Geoffrey Dr.; только christiana-de
**Контакт:** 302.322.6933 | 302.297.4052 | 106 Geoffrey Dr. | Newark , | DE                                    19713 · 302-322-6933.
**Проверка:** 2026-10-12T00:54:21.972400+00:00; действующий официальный overview с текущими контактами/записью.

Rachael Gaeta и Kristin Kicenuik — DACVIM (Oncology). Kicenuik обслуживает также Malvern и CyberKnife Center; её биография прямо описывает chemotherapy, targeted therapy, immunotherapy. Alyson Frederick — DACVS (SA), surgical oncology среди текущих интересов. I-131 для гипертиреоза и CT не являются доказательством противоопухолевой лучевой.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Alyson Frederick — DVM, DACVS (SA); Surgery.
- Rachael Gaeta — DVM, DACVIM (Oncology); Oncology.
- Dana Gale — DVM; Surgery.
- Kristin Kicenuik — DVM, DACVIM (Oncology); Oncology.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

Назначенная запись не найдена в supplemental по source_id/названию/совпадающему master URL; старые supplemental поля недоступны. Это не означает отсутствия записи в итоговом построенном каталоге.

Исторический ACVIM-снимок: Rachael Ann Gaeta, DVM, DACVIM (Oncology); адрес 106 Geoffrey Drive / Newark, DE 19713; телефон `302.322.6933`. Это baseline, не доказательство текущего приёма.

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/christiana-de/) — «BluePearl Pet Hospital | Christiana, DE»; 2026-10-12T00:54:21.972400+00:00; HTTP 200; scope `christiana-de`.
- [Local services](https://bluepearlvet.com/hospital/christiana-de/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Newark DE»; 2026-10-12T00:54:22.055700+00:00; HTTP 200; scope `christiana-de`.
- [Local team](https://bluepearlvet.com/hospital/christiana-de/our-vets/) — «BluePearl Pet Hospital | Christiana, DE | Our Vets»; 2026-10-12T00:54:21.978979+00:00; HTTP 200; scope `christiana-de`.
- [Oncology](https://bluepearlvet.com/hospital/christiana-de/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Newark DE»; 2026-10-12T00:54:22.060988+00:00; HTTP 200; scope `christiana-de`.
- [Surgery](https://bluepearlvet.com/hospital/christiana-de/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Newark DE»; 2026-10-12T00:54:22.104491+00:00; HTTP 200; scope `christiana-de`.
- [Appointment](https://bluepearlvet.com/hospital/christiana-de/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:22.150120+00:00; HTTP 200; scope `christiana-de`.
- [Referring vets](https://bluepearlvet.com/hospital/christiana-de/referring-vets/) — «BluePearl Pet Hospital | Christiana, DE | Referring Vets»; 2026-10-12T00:56:04.159122+00:00; HTTP 200; scope `christiana-de`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** master_url, supporting_urls.
**Unresolved:** отдельных вопросов по исходным утверждениям не осталось; непубликуемые дополнительные услуги не добавлены.

### 12. BluePearl Pet Hospital – Clearwater — `bluepearl-pet-hospital-clearwater`

**branch_scope:** BluePearl Pet Hospital – Clearwater — 4701 Ulmerton Rd. Ste. 500; только clearwater-fl
**Контакт:** 727.572.0132 | 813.682.0478 | 4701 Ulmerton Rd.                                    Ste. 500 | Clearwater, | FL                                    33762 · 727-572-0132.
**Проверка:** 2026-10-12T00:53:22.656356+00:00; действующий официальный overview с текущими контактами/записью.

Kelly Kezer — BVSc, DACVIM (Oncology), обслуживает Clearwater и Tampa; Curtis Kane — DVM в oncology, без опубликованного DACVIM. Интерес Kezer к immunotherapy не подтверждает конкретную доступную услугу в Clearwater.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Natali Almodovar Garcia — DVM; Surgery.
- Helga Bleyaert — VMD, DACVS; Surgery.
- Kaitlyn Cassel — VMD; Surgery.
- Kelsey Human — DVM, DACVS (SA); Surgery.
- Curtis Kane — DVM; Oncology.
- Kelly Kezer — BVSc, DACVIM (Oncology); Oncology.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

```json
{
  "name": "BluePearl Pet Hospital – Clearwater",
  "street": "4701 Ulmerton Road, Suite 500",
  "city": "Clearwater",
  "region": "FL",
  "postal_code": "33762",
  "phone": "727-572-0132",
  "website": "https://bluepearlvet.com/hospital/clearwater-fl/specialties-services/oncology/",
  "services": [
    "Medical oncology",
    "Chemotherapy",
    "Radiation oncology",
    "Immunotherapy",
    "Surgery"
  ]
}
```

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/clearwater-fl/) — «BluePearl Pet Hospital | Clearwater, FL»; 2026-10-12T00:53:22.656356+00:00; HTTP 200; scope `clearwater-fl`.
- [Local services](https://bluepearlvet.com/hospital/clearwater-fl/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Clearwater FL»; 2026-10-12T00:53:22.689419+00:00; HTTP 200; scope `clearwater-fl`.
- [Local team](https://bluepearlvet.com/hospital/clearwater-fl/our-vets/) — «BluePearl Pet Hospital | Clearwater, FL | Our Vets»; 2026-10-12T00:53:22.662077+00:00; HTTP 200; scope `clearwater-fl`.
- [Oncology](https://bluepearlvet.com/hospital/clearwater-fl/specialties-services/oncology/) — «Veterinary Oncology in Clearwater | BluePearl Pet Hospital Clearwater FL»; 2026-10-12T00:53:22.690806+00:00; HTTP 200; scope `clearwater-fl`.
- [Surgery](https://bluepearlvet.com/hospital/clearwater-fl/specialties-services/surgery/) — «Veterinary Surgery in Clearwater | BluePearl Pet Hospital Clearwater FL»; 2026-10-12T00:54:04.877252+00:00; HTTP 200; scope `clearwater-fl`.
- [Appointment](https://bluepearlvet.com/hospital/clearwater-fl/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:04.936812+00:00; HTTP 200; scope `clearwater-fl`.
- [Referring vets](https://bluepearlvet.com/hospital/clearwater-fl/referring-vets/) — «BluePearl Pet Hospital | Clearwater, FL | Referring Vets»; 2026-10-12T00:55:57.578678+00:00; HTTP 200; scope `clearwater-fl`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** supporting_urls.
**Unresolved:** B01-Q02, B01-Q06.

### 13. BluePearl Pet Hospital - Conshohocken — `bluepearl-pet-hospital-conshohocken`

**branch_scope:** BluePearl Pet Hospital - Conshohocken — 625 Ridge Pike Bldg. B; только conshohocken-pa
**Контакт:** 484.567.7999 | 484.567.7998 | 625 Ridge Pike                                    Bldg. B | Conshohocken, | PA                                    19428 · 484-567-7999.
**Проверка:** 2026-10-12T00:53:22.788072+00:00; действующий официальный overview с текущими контактами/записью.

Jennifer Kim — DACVIM (Oncology). Местная медицинская онкология, химиотерапия и хирургическая служба опубликованы. CyberKnife в соседнем Malvern не приписан Conshohocken.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Jennifer Kim — DVM, DACVIM (Oncology); Oncology.
- Sarah Round — DVM, DACVS (SA); Surgery.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

Назначенная запись не найдена в supplemental по source_id/названию/совпадающему master URL; старые supplemental поля недоступны. Это не означает отсутствия записи в итоговом построенном каталоге.

Исторический ACVIM-снимок: Jennifer Kim, DVM, DACVIM (Oncology); адрес 625 Ridge Pike / Building B / Conshohocken, PA 19428; телефон `484.567.7999`. Это baseline, не доказательство текущего приёма.

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/conshohocken-pa/) — «BluePearl Pet Hospital | Conshohocken, PA»; 2026-10-12T00:53:22.788072+00:00; HTTP 200; scope `conshohocken-pa`.
- [Local services](https://bluepearlvet.com/hospital/conshohocken-pa/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Conshohocken PA»; 2026-10-12T00:53:25.186145+00:00; HTTP 200; scope `conshohocken-pa`.
- [Local team](https://bluepearlvet.com/hospital/conshohocken-pa/our-vets/) — «BluePearl Pet Hospital | Conshohocken, PA | Our Vets»; 2026-10-12T00:53:22.790263+00:00; HTTP 200; scope `conshohocken-pa`.
- [Oncology](https://bluepearlvet.com/hospital/conshohocken-pa/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Conshohocken PA»; 2026-10-12T00:53:25.205776+00:00; HTTP 200; scope `conshohocken-pa`.
- [Surgery](https://bluepearlvet.com/hospital/conshohocken-pa/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Conshohocken PA»; 2026-10-12T00:54:04.967019+00:00; HTTP 200; scope `conshohocken-pa`.
- [Appointment](https://bluepearlvet.com/hospital/conshohocken-pa/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:05.022251+00:00; HTTP 200; scope `conshohocken-pa`.
- [Referring vets](https://bluepearlvet.com/hospital/conshohocken-pa/referring-vets/) — «BluePearl Pet Hospital | Conshohocken, PA | Referring Vets»; 2026-10-12T00:56:01.280803+00:00; HTTP 200; scope `conshohocken-pa`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** master_url, supporting_urls.
**Unresolved:** отдельных вопросов по исходным утверждениям не осталось; непубликуемые дополнительные услуги не добавлены.

### 14. BluePearl Pet Hospital – Durham — `bluepearl-pet-hospital-durham`

**branch_scope:** BluePearl Pet Hospital – Durham — 7015 NC Hwy. 751; только durham-nc
**Контакт:** 919.600.6600 | 919.294.6787 | 7015 NC Hwy. 751 | Durham, | NC                                    27707 · 919-600-6600.
**Проверка:** 2026-10-12T00:53:25.323865+00:00; действующий официальный overview с текущими контактами/записью.

Susan Shapiro и Carly Stevens — DACVIM (Oncology), обе перечислены для Durham. На актуальной напрямую загруженной команде David Ruslander указан в Cary, не Durham; поисковая копия сохраняет более широкий список. Не переносить его радиационную сертификацию/лучевую службу на Durham.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Courtney Bounds — DVM, MS; Surgery.
- Sarah Christie — DVM; Surgery.
- Meghan Kruse — DVM, DACVS (SA); Surgery.
- David Lee — DVM, DACVS; Surgery.
- Susan Shapiro — PhD, DVM, DACVIM (Oncology); Oncology.
- Carly Stevens — DVM, DACVIM (Oncology); Oncology.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

```json
{
  "name": "BluePearl Pet Hospital – Durham",
  "street": "7015 NC Highway 751",
  "city": "Durham",
  "region": "NC",
  "postal_code": "27707",
  "phone": "919-600-6600",
  "website": "https://bluepearlvet.com/hospital/durham-nc/specialties-services/oncology/",
  "services": [
    "Medical oncology",
    "Chemotherapy",
    "Radiation oncology",
    "Immunotherapy",
    "Surgery"
  ]
}
```

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/durham-nc/) — «24 Hour Emergency Vet | BluePearl Pet Hospital | Durham, NC»; 2026-10-12T00:53:25.323865+00:00; HTTP 200; scope `durham-nc`.
- [Local services](https://bluepearlvet.com/hospital/durham-nc/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Durham NC»; 2026-10-12T00:53:25.354277+00:00; HTTP 200; scope `durham-nc`.
- [Local team](https://bluepearlvet.com/hospital/durham-nc/our-vets/) — «BluePearl Pet Hospital | Durham, NC | Our Vets»; 2026-10-12T00:53:25.344636+00:00; HTTP 200; scope `durham-nc`.
- [Oncology](https://bluepearlvet.com/hospital/durham-nc/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Durham NC»; 2026-10-12T00:53:25.377752+00:00; HTTP 200; scope `durham-nc`.
- [Surgery](https://bluepearlvet.com/hospital/durham-nc/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Durham NC»; 2026-10-12T00:54:08.075292+00:00; HTTP 200; scope `durham-nc`.
- [Appointment](https://bluepearlvet.com/hospital/durham-nc/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:08.098099+00:00; HTTP 200; scope `durham-nc`.
- [Referring vets](https://bluepearlvet.com/hospital/durham-nc/referring-vets/) — «BluePearl Pet Hospital | Durham, NC | Referring Vets»; 2026-10-12T00:56:01.305143+00:00; HTTP 200; scope `durham-nc`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** supporting_urls.
**Unresolved:** B01-Q02, B01-Q06.

### 15. BluePearl Pet Hospital – Fort Myers — `bluepearl-pet-hospital-fort-myers`

**branch_scope:** BluePearl Pet Hospital – Fort Myers — 9500 Marketplace Rd.; только fort-myers-fl
**Контакт:** 239.947.0588 | 239.947.0598 | 9500 Marketplace Rd. | Fort Myers, | FL                                    33912 · 239-947-0588.
**Проверка:** 2026-10-12T00:53:25.584087+00:00; действующий официальный overview с текущими контактами/записью.

ECT подтверждена прямым местным Treatment plans, не только интересом Luis Lembcke. Первое заключение B01 было ошибкой чтения; подтверждающая строка уже была в первоначальных данных. Иммунотерапия из интересов врача отдельно не активирована.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Oscar Carballo — DVM, DACVS (SA); Surgery.
- Luis Lembcke — MV, MS, PhD, DACVIM (Oncology); Oncology.
- Beatrix Nanai — DVM, DECVN, DACVS (SA); Neurology, Neurosurgery, Surgery.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

Назначенная запись не найдена в supplemental по source_id/названию/совпадающему master URL; старые supplemental поля недоступны. Это не означает отсутствия записи в итоговом построенном каталоге.

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/fort-myers-fl/) — «24-Hour Emergency Vet | BluePearl Pet Hospital | Fort Myers, FL»; 2026-10-12T00:53:25.584087+00:00; HTTP 200; scope `fort-myers-fl`.
- [Local services](https://bluepearlvet.com/hospital/fort-myers-fl/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Fort Myers FL»; 2026-10-12T00:53:25.603072+00:00; HTTP 200; scope `fort-myers-fl`.
- [Local team](https://bluepearlvet.com/hospital/fort-myers-fl/our-vets/) — «BluePearl Pet Hospital | Fort Myers, FL | Our Vets»; 2026-10-12T00:53:25.585098+00:00; HTTP 200; scope `fort-myers-fl`.
- [Oncology](https://bluepearlvet.com/hospital/fort-myers-fl/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Fort Myers FL»; 2026-10-12T00:53:25.897958+00:00; HTTP 200; scope `fort-myers-fl`.
- [Surgery](https://bluepearlvet.com/hospital/fort-myers-fl/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Fort Myers FL»; 2026-10-12T00:54:08.140549+00:00; HTTP 200; scope `fort-myers-fl`.
- [Appointment](https://bluepearlvet.com/hospital/fort-myers-fl/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:08.193132+00:00; HTTP 200; scope `fort-myers-fl`.
- [Referring vets](https://bluepearlvet.com/hospital/fort-myers-fl/referring-vets/) — «BluePearl Pet Hospital | Fort Myers, FL | Referring Vets»; 2026-10-12T00:56:01.309433+00:00; HTTP 200; scope `fort-myers-fl`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** supporting_urls.
**Unresolved:** вопросы первого прохода сняты; см. углублённую проверку.

### 16. BluePearl Pet Hospital – Framingham — `bluepearl-pet-hospital-framingham`

**branch_scope:** BluePearl Pet Hospital – Framingham — 659 Worcester Road #9; только framingham-ma
**Контакт:** 781.684.8387 | 781.890.2871 | 659 Worcester Road #9 | Framingham, | MA                                    01701 · 781-684-8387.
**Проверка:** 2026-10-12T00:53:28.803257+00:00; действующий официальный overview с текущими контактами/записью.

Rachel Wong — DACVIM (Oncology); Janis Lapsley — DACVS (SA), опубликован fellowship Surgical Oncology. Её текущая практика прямо ориентирована на хирургическое лечение рака, с перечислением резекций и реконструкций. Подтверждена именно текущая местная работа, а не только прошлый опыт в Ohio State.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Robert Deegan — DVM; Surgery.
- Janis Lapsley — DVM, DACVS (SA); Surgery.
- Rachel Wong — DVM, DACVIM (Oncology); Oncology.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

```json
{
  "name": "BluePearl Pet Hospital – Framingham",
  "street": "659 Worcester Road, Suite 9",
  "city": "Framingham",
  "region": "MA",
  "postal_code": "01701",
  "phone": "781-684-8387",
  "website": "https://bluepearlvet.com/hospital/framingham-ma/",
  "services": [
    "Medical oncology"
  ]
}
```

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/framingham-ma/) — «BluePearl Pet Hospital | Framingham, MA»; 2026-10-12T00:53:28.803257+00:00; HTTP 200; scope `framingham-ma`.
- [Local services](https://bluepearlvet.com/hospital/framingham-ma/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Framingham MA»; 2026-10-12T00:53:28.891950+00:00; HTTP 200; scope `framingham-ma`.
- [Local team](https://bluepearlvet.com/hospital/framingham-ma/our-vets/) — «BluePearl Pet Hospital | Framingham, MA | Our Vets»; 2026-10-12T00:53:28.887742+00:00; HTTP 200; scope `framingham-ma`.
- [Oncology](https://bluepearlvet.com/hospital/framingham-ma/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Framingham MA»; 2026-10-12T00:53:28.893815+00:00; HTTP 200; scope `framingham-ma`.
- [Surgery](https://bluepearlvet.com/hospital/framingham-ma/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Framingham MA»; 2026-10-12T00:54:08.285677+00:00; HTTP 200; scope `framingham-ma`.
- [Appointment](https://bluepearlvet.com/hospital/framingham-ma/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:08.346817+00:00; HTTP 200; scope `framingham-ma`.
- [Referring vets](https://bluepearlvet.com/hospital/framingham-ma/referring-vets/) — «BluePearl Pet Hospital | Framingham, MA | Referring Vets»; 2026-10-12T00:56:01.322592+00:00; HTTP 200; scope `framingham-ma`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** master_url, supporting_urls, services, clinician_review.
**Unresolved:** отдельных вопросов по исходным утверждениям не осталось; непубликуемые дополнительные услуги не добавлены.

### 17. BluePearl Pet Hospital – Lafayette — `bluepearl-pet-hospital-lafayette`

**branch_scope:** BluePearl Pet Hospital – Lafayette — 2000 W South Boulder Rd.; только lafayette-co
**Контакт:** 720.699.7766 | 720.699.7767 | 2000 W South Boulder Rd. | Lafayette, | CO                                    80026 · 720-699-7766.
**Проверка:** 2026-10-12T00:53:28.901960+00:00; действующий официальный overview с текущими контактами/записью.

Caitlin Cowan — DACVIM (Oncology). Местный подробный список прямо подтверждает IV/oral chemotherapy, surgery, ECT, immunotherapy; external beam radiation только referrals. Kaleigh Peters — DACVS (SA), онкологические операции в текущих интересах; Jacqueline Hansen — DACVR диагностической радиологии, не radiation oncology.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Caitlin Cowan — DVM, MS, DACVIM (Oncology); Oncology.
- Kaleigh Peters — DVM, MS, DACVS (SA); Surgery.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

Назначенная запись не найдена в supplemental по source_id/названию/совпадающему master URL; старые supplemental поля недоступны. Это не означает отсутствия записи в итоговом построенном каталоге.

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/lafayette-co/) — «BluePearl Pet Hospital | Lafayette, CO»; 2026-10-12T00:53:28.901960+00:00; HTTP 200; scope `lafayette-co`.
- [Local services](https://bluepearlvet.com/hospital/lafayette-co/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Lafayette CO»; 2026-10-12T00:53:28.912248+00:00; HTTP 200; scope `lafayette-co`.
- [Local team](https://bluepearlvet.com/hospital/lafayette-co/our-vets/) — «BluePearl Pet Hospital | Lafayette, CO | Our Vets»; 2026-10-12T00:53:28.910333+00:00; HTTP 200; scope `lafayette-co`.
- [Oncology](https://bluepearlvet.com/hospital/lafayette-co/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Lafayette CO»; 2026-10-12T00:53:28.944416+00:00; HTTP 200; scope `lafayette-co`.
- [Surgery](https://bluepearlvet.com/hospital/lafayette-co/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Lafayette CO»; 2026-10-12T00:54:08.718581+00:00; HTTP 200; scope `lafayette-co`.
- [Appointment](https://bluepearlvet.com/hospital/lafayette-co/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:12.120706+00:00; HTTP 200; scope `lafayette-co`.
- [Referring vets](https://bluepearlvet.com/hospital/lafayette-co/referring-vets/) — «BluePearl Pet Hospital | Lafayette, CO | Referring Vets»; 2026-10-12T00:56:01.375804+00:00; HTTP 200; scope `lafayette-co`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** supporting_urls, services, availability_note.
**Unresolved:** отдельных вопросов по исходным утверждениям не осталось; непубликуемые дополнительные услуги не добавлены.

### 18. Bluepearl Pet Hospital, Levittown, PA — `bluepearl-pet-hospital-levittown-pa`

**branch_scope:** Bluepearl Pet Hospital, Levittown, PA — 301 Veterans Hwy.; только vsec-levittown-pa
**Контакт:** 215.750.7884 | 215.752.3156 | 301 Veterans Hwy. | Levittown, | PA                                    19056 · 215-750-7884.
**Проверка:** 2026-10-12T00:54:22.158936+00:00; действующий официальный overview с текущими контактами/записью.

Olivier Campbell — DVM, MVSc, DACVIM (Oncology). Robert Matus из старого ACVIM-снимка не перечислен в актуальной местной команде: это не доказательство пенсии/увольнения. Jennifer MacLeod — DACVS (SA), интерес к oncologic surgery. Линейный ускоритель прямо указан на местной странице; не объявлять закрытой лучевую из-за отсутствия именованного radiation oncologist.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Olivier Campbell — DVM, MVSc, DACVIM (Oncology); Oncology.
- Lauren Deahl — DVM, DACVS (SA); Surgery.
- Cody Dickens — VMD; Surgery.
- Michael Jennings — VMD, DAVDC; Dentistry & Oral Surgery.
- Jennifer MacLeod — VMD, DACVS (SA); Surgery.
- Catherine Popovitch — DVM, DACVS, DECVS; Surgery.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

Назначенная запись не найдена в supplemental по source_id/названию/совпадающему master URL; старые supplemental поля недоступны. Это не означает отсутствия записи в итоговом построенном каталоге.

Исторический ACVIM-снимок: Robert Edward Matus, DVM, MS, MRCVS, DACVIM (SAIM & Oncology); адрес Veterinary Specialty & Emergency Center / 301 Veteran Highway / Middleton on Sea / Levittown, PA 19056; телефон `215.750.7884`. Это baseline, не доказательство текущего приёма.

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/vsec-levittown-pa/) — «BluePearl Pet Hospital | Levittown, PA»; 2026-10-12T00:54:22.158936+00:00; HTTP 200; scope `vsec-levittown-pa`.
- [Local services](https://bluepearlvet.com/hospital/vsec-levittown-pa/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Levittown PA»; 2026-10-12T00:54:24.764188+00:00; HTTP 200; scope `vsec-levittown-pa`.
- [Local team](https://bluepearlvet.com/hospital/vsec-levittown-pa/our-vets/) — «BluePearl Pet Hospital | Levittown, PA | Our Vets»; 2026-10-12T00:54:24.742348+00:00; HTTP 200; scope `vsec-levittown-pa`.
- [Oncology](https://bluepearlvet.com/hospital/vsec-levittown-pa/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Levittown PA»; 2026-10-12T00:54:24.786597+00:00; HTTP 200; scope `vsec-levittown-pa`.
- [Surgery](https://bluepearlvet.com/hospital/vsec-levittown-pa/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Levittown PA»; 2026-10-12T00:54:24.880329+00:00; HTTP 200; scope `vsec-levittown-pa`.
- [Appointment](https://bluepearlvet.com/hospital/vsec-levittown-pa/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:24.889326+00:00; HTTP 200; scope `vsec-levittown-pa`.
- [Referring vets](https://bluepearlvet.com/hospital/vsec-levittown-pa/referring-vets/) — «BluePearl Pet Hospital | Levittown, PA | Referring Vets»; 2026-10-12T00:56:04.225133+00:00; HTTP 200; scope `vsec-levittown-pa`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** master_url, supporting_urls.
**Unresolved:** отдельных вопросов по исходным утверждениям не осталось; непубликуемые дополнительные услуги не добавлены.

### 19. BluePearl Pet Hospital – Malvern — `bluepearl-pet-hospital-malvern`

**branch_scope:** BluePearl Pet Hospital – Malvern — 40 Three Tun Rd.; только malvern-pa
**Контакт:** 610.296.2099 | 40 Three Tun Rd. | Malvern, | PA                                    19355 · 610-296-2099.
**Проверка:** 2026-10-12T00:53:31.637243+00:00; действующий официальный overview с текущими контактами/записью.

Физическое место опубликованного CyberKnife и conventional LINAC установлено: Cancer Center 50 Three Tun Rd. Hospital 40 Three Tun Rd. остаётся своим самостоятельным адресом. Оборудование по 50 не переносится в 40. Отдельная пользовательская догадка не требуется для точной привязки известной услуги.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Craig Clifford — MS, DVM, DACVIM (Oncology); Oncology.
- Evan Ducker — DVM, DACVR-RO; Radiation Oncology.
- Siobhan Haney — MS, VMD, DACVR-RO, MBA; Radiation Oncology.
- Kristin Kicenuik — DVM, DACVIM (Oncology); Oncology.
- Christine Mullin — VMD, DACVIM (Oncology); Oncology.
- Paul G. Orsini — DVM, DACVS, DAVDC; Dentistry & Oral Surgery.
- Jennifer Reagan — DVM, DACVS (SA), MS; Surgery.
- Rebecca Risbon — VMD, DACVIM (Oncology); Oncology.
- Scott Roberts — VMD, DACVS (SA); Surgery.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

Назначенная запись не найдена в supplemental по source_id/названию/совпадающему master URL; старые supplemental поля недоступны. Это не означает отсутствия записи в итоговом построенном каталоге.

Исторический ACVIM-снимок: Christine Mullin, VMD, DACVIM (Oncology); адрес 40 Three Tun Rd / Malvern, PA 19355; телефон `610.296.2099`. Это baseline, не доказательство текущего приёма.

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/malvern-pa/) — «BluePearl Pet Hospital | Malvern, PA»; 2026-10-12T00:53:31.637243+00:00; HTTP 200; scope `malvern-pa`.
- [Local services](https://bluepearlvet.com/hospital/malvern-pa/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Malvern PA»; 2026-10-12T00:53:31.780725+00:00; HTTP 200; scope `malvern-pa`.
- [Local team](https://bluepearlvet.com/hospital/malvern-pa/our-vets/) — «BluePearl Pet Hospital | Malvern, PA | Our Vets»; 2026-10-12T00:53:31.753553+00:00; HTTP 200; scope `malvern-pa`.
- [Oncology](https://bluepearlvet.com/hospital/malvern-pa/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Malvern PA»; 2026-10-12T00:53:31.784719+00:00; HTTP 200; scope `malvern-pa`.
- [Surgery](https://bluepearlvet.com/hospital/malvern-pa/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Malvern PA»; 2026-10-12T00:54:12.246679+00:00; HTTP 200; scope `malvern-pa`.
- [Appointment](https://bluepearlvet.com/hospital/malvern-pa/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:12.248530+00:00; HTTP 200; scope `malvern-pa`.
- [Referring vets](https://bluepearlvet.com/hospital/malvern-pa/referring-vets/) — «BluePearl Pet Hospital | Malvern, PA | Referring Vets»; 2026-10-12T00:56:01.386791+00:00; HTTP 200; scope `malvern-pa`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** master_url, supporting_urls.
**Unresolved:** вопросы первого прохода сняты; см. углублённую проверку.

### 20. BluePearl Pet Hospital – Nashville — `bluepearl-pet-hospital-nashville`

**branch_scope:** BluePearl Pet Hospital – Nashville — 2409 21st Ave S; только nashville-tn
**Контакт:** 615.383.2600 | 615.383.5666 | 2409 21st Ave S | Nashville, | TN                                    37212 · 615-383-2600.
**Проверка:** 2026-10-12T00:53:31.785444+00:00; действующий официальный overview с текущими контактами/записью.

Zoe Williams — DACVIM (Oncology). Местная хирургия опубликована; опыт хирурга в surgical oncology internship не превращается в отдельную сертификацию. Лучевую не переносить из шаблонного блока.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Michael Blumenthal — DVM; Surgery.
- Michael Pawenski — DVM, DACVS (SA); Surgery.
- Zoe Williams — DVM, DACVIM (Oncology); Oncology.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

```json
{
  "name": "BluePearl Pet Hospital – Nashville",
  "street": "2409 21st Avenue S",
  "city": "Nashville",
  "region": "TN",
  "postal_code": "37212",
  "phone": "615-383-2600",
  "website": "https://bluepearlvet.com/hospital/nashville-tn/specialties-services/oncology/",
  "services": [
    "Medical oncology",
    "Chemotherapy",
    "Radiation oncology",
    "Immunotherapy",
    "Surgery"
  ]
}
```

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/nashville-tn/) — «BluePearl Pet Hospital | Nashville, TN»; 2026-10-12T00:53:31.785444+00:00; HTTP 200; scope `nashville-tn`.
- [Local services](https://bluepearlvet.com/hospital/nashville-tn/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Nashville TN»; 2026-10-12T00:53:32.067222+00:00; HTTP 200; scope `nashville-tn`.
- [Local team](https://bluepearlvet.com/hospital/nashville-tn/our-vets/) — «BluePearl Pet Hospital | Nashville, TN | Our Vets»; 2026-10-12T00:53:31.787242+00:00; HTTP 200; scope `nashville-tn`.
- [Oncology](https://bluepearlvet.com/hospital/nashville-tn/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Nashville TN»; 2026-10-12T00:53:32.083837+00:00; HTTP 200; scope `nashville-tn`.
- [Surgery](https://bluepearlvet.com/hospital/nashville-tn/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Nashville TN»; 2026-10-12T00:54:12.402721+00:00; HTTP 200; scope `nashville-tn`.
- [Appointment](https://bluepearlvet.com/hospital/nashville-tn/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:12.405041+00:00; HTTP 200; scope `nashville-tn`.
- [Referring vets](https://bluepearlvet.com/hospital/nashville-tn/referring-vets/) — «BluePearl Pet Hospital | Nashville, TN | Referring Vets»; 2026-10-12T00:56:01.387267+00:00; HTTP 200; scope `nashville-tn`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** supporting_urls.
**Unresolved:** B01-Q02, B01-Q06.

### 21. BluePearl Pet Hospital – Northfield — `bluepearl-pet-hospital-northfield`

**branch_scope:** BluePearl Pet Hospital – Northfield — 820 W Frontage Rd; только northfield-il
**Контакт:** 847.564.5775 | 847.564.5899 | 820 W Frontage Rd | Northfield, | IL                                    60093 · 847-564-5775.
**Проверка:** 2026-10-12T00:53:34.220534+00:00; действующий официальный overview с текущими контактами/записью.

Pedro Boria — DACVIM (Oncology); две residency (internal medicine/oncology) не означают две подтверждённые board certifications. Bob Wilson — DACVS (SA), surgical oncology среди текущих интересов. Общая хирургическая служба подтверждена.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Pedro Boria — DVM, MS, DACVIM (Oncology); Oncology.
- David Wilson — DVM, DACVS (SA); Surgery.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

Назначенная запись не найдена в supplemental по source_id/названию/совпадающему master URL; старые supplemental поля недоступны. Это не означает отсутствия записи в итоговом построенном каталоге.

Исторический ACVIM-снимок: Pedro A. Boria, DVM, MS, DACVIM (Oncology); адрес 820 W Frontage Rd / Northfield, IL 60093; телефон ``. Это baseline, не доказательство текущего приёма.

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/northfield-il/) — «BluePearl Pet Hospital | Northfield, IL»; 2026-10-12T00:53:34.220534+00:00; HTTP 200; scope `northfield-il`.
- [Local services](https://bluepearlvet.com/hospital/northfield-il/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Northfield IL»; 2026-10-12T00:53:34.330707+00:00; HTTP 200; scope `northfield-il`.
- [Local team](https://bluepearlvet.com/hospital/northfield-il/our-vets/) — «BluePearl Pet Hospital | Northfield, IL | Our Vets»; 2026-10-12T00:53:34.287133+00:00; HTTP 200; scope `northfield-il`.
- [Oncology](https://bluepearlvet.com/hospital/northfield-il/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Northfield IL»; 2026-10-12T00:53:34.381164+00:00; HTTP 200; scope `northfield-il`.
- [Surgery](https://bluepearlvet.com/hospital/northfield-il/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Northfield IL»; 2026-10-12T00:54:14.969193+00:00; HTTP 200; scope `northfield-il`.
- [Appointment](https://bluepearlvet.com/hospital/northfield-il/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:15.054547+00:00; HTTP 200; scope `northfield-il`.
- [Referring vets](https://bluepearlvet.com/hospital/northfield-il/referring-vets/) — «BluePearl Pet Hospital | Northfield, IL | Referring Vets»; 2026-10-12T00:56:01.388745+00:00; HTTP 200; scope `northfield-il`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** master_url, supporting_urls, phone.
**Unresolved:** отдельных вопросов по исходным утверждениям не осталось; непубликуемые дополнительные услуги не добавлены.

### 22. BluePearl Pet Hospital Oak Creek — `bluepearl-pet-hospital-oak-creek`

**branch_scope:** BluePearl Pet Hospital Oak Creek — 9472 S 27th St; только oak-creek-wi
**Контакт:** 414.761.6333 | 9472 S 27th St | Oak Creek, | WI                                    53154 · 414-761-6333.
**Проверка:** 2026-10-12T00:53:34.381774+00:00; действующий официальный overview с текущими контактами/записью.

Rachel Sternberg — DACVIM (Oncology). Сотрудничество с radiation oncology teams не устанавливает местное облучение. Опубликованы физический приём и общая хирургическая служба; специализированная онкохирургия отдельно не установлена.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Elizabeth Hiebert — DVM, MS, DACVS (SA); Surgery.
- Rachel Sternberg — DVM, DACVIM (Oncology); Oncology.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

Назначенная запись не найдена в supplemental по source_id/названию/совпадающему master URL; старые supplemental поля недоступны. Это не означает отсутствия записи в итоговом построенном каталоге.

Исторический ACVIM-снимок: Rachel A. Sternberg, DVM, DACVIM (Oncology); адрес 9472 S 27th St / Oak Creek, WI 53154; телефон `414.761.6333`. Это baseline, не доказательство текущего приёма.

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/oak-creek-wi/) — «BluePearl Pet Hospital | Oak Creek, WI»; 2026-10-12T00:53:34.381774+00:00; HTTP 200; scope `oak-creek-wi`.
- [Local services](https://bluepearlvet.com/hospital/oak-creek-wi/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Oak Creek WI»; 2026-10-12T00:53:34.405473+00:00; HTTP 200; scope `oak-creek-wi`.
- [Local team](https://bluepearlvet.com/hospital/oak-creek-wi/our-vets/) — «BluePearl Pet Hospital | Oak Creek, WI | Our Vets»; 2026-10-12T00:53:34.383342+00:00; HTTP 200; scope `oak-creek-wi`.
- [Oncology](https://bluepearlvet.com/hospital/oak-creek-wi/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Oak Creek WI»; 2026-10-12T00:53:34.437741+00:00; HTTP 200; scope `oak-creek-wi`.
- [Surgery](https://bluepearlvet.com/hospital/oak-creek-wi/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Oak Creek WI»; 2026-10-12T00:54:15.078698+00:00; HTTP 200; scope `oak-creek-wi`.
- [Appointment](https://bluepearlvet.com/hospital/oak-creek-wi/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:15.169786+00:00; HTTP 200; scope `oak-creek-wi`.
- [Referring vets](https://bluepearlvet.com/hospital/oak-creek-wi/referring-vets/) — «BluePearl Pet Hospital | Oak Creek, WI | Referring Vets»; 2026-10-12T00:56:01.414085+00:00; HTTP 200; scope `oak-creek-wi`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** master_url, supporting_urls.
**Unresolved:** отдельных вопросов по исходным утверждениям не осталось; непубликуемые дополнительные услуги не добавлены.

### 23. BluePearl Pet Hospital Orlando – Maitland — `bluepearl-pet-hospital-orlando-maitland`

**branch_scope:** BluePearl Pet Hospital Orlando – Maitland — 9905 S U.S. Hwy. 17-92; только maitland-fl
**Контакт:** 407.644.1287 | 407.644.9075 | 9905 S U.S. Hwy. 17-92 | Maitland, | FL                                    32751 · 407-644-1287.
**Проверка:** 2026-10-12T00:53:34.640018+00:00; действующий официальный overview с текущими контактами/записью.

Местная лучевая подтверждена официальными актуальными employer descriptions с Linear Accelerator и текущей Villa DACVR-RO. Medical Oncology и chemotherapy hood также опубликованы; Goodson и конкретный назначенный медицинский врач остаются неустановленными, anticancer immunotherapy не подтверждена.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Jean Frazho — DVM, DACVS (SA); Surgery.
- Mackenzie Grace — DVM; Surgery.
- Micheala Polly — DVM; Surgery.
- Mariana Quina — DVM, DACVS (SA); Surgery.
- Dillon Scott — DVM; Surgery.
- Zulema Villa — DVM, MS, DACVR-RO; Radiation Oncology.
- Katelyn Walraven — VMD, DACVS (SA); Surgery.
- Nathan Zab — DVM; Surgery.

Goodson не включена в текущую команду: прямые страницы и поисковая копия расходятся.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

```json
{
  "name": "BluePearl Pet Hospital Orlando – Maitland",
  "street": "9905 S U.S. Highway 17-92",
  "city": "Maitland",
  "region": "FL",
  "postal_code": "32751",
  "phone": "407-644-1287",
  "website": "https://bluepearlvet.com/hospital/maitland-fl/specialties-services/oncology/",
  "services": [
    "Medical oncology",
    "Chemotherapy",
    "Radiation oncology",
    "Immunotherapy",
    "Surgery"
  ]
}
```

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/maitland-fl/) — «BluePearl Pet Hospital Orlando | Maitland, FL»; 2026-10-12T00:53:34.640018+00:00; HTTP 200; scope `maitland-fl`.
- [Local services](https://bluepearlvet.com/hospital/maitland-fl/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Maitland FL»; 2026-10-12T00:53:36.838547+00:00; HTTP 200; scope `maitland-fl`.
- [Local team](https://bluepearlvet.com/hospital/maitland-fl/our-vets/) — «BluePearl Pet Hospital | Maitland, FL | Our Vets»; 2026-10-12T00:53:35.023784+00:00; HTTP 200; scope `maitland-fl`.
- [Oncology](https://bluepearlvet.com/hospital/maitland-fl/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Maitland FL»; 2026-10-12T00:53:36.846694+00:00; HTTP 200; scope `maitland-fl`.
- [Surgery](https://bluepearlvet.com/hospital/maitland-fl/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Maitland FL»; 2026-10-12T00:54:15.210728+00:00; HTTP 200; scope `maitland-fl`.
- [Appointment](https://bluepearlvet.com/hospital/maitland-fl/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:15.264053+00:00; HTTP 200; scope `maitland-fl`.
- [Referring vets](https://bluepearlvet.com/hospital/maitland-fl/referring-vets/) — «BluePearl Pet Hospital | Maitland, FL | Referring Vets»; 2026-10-12T00:56:01.422148+00:00; HTTP 200; scope `maitland-fl`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** supporting_urls.
**Unresolved:** B01-Q01

### 24. BluePearl Pet Hospital – Overland Park — `bluepearl-pet-hospital-overland-park`

**branch_scope:** BluePearl Pet Hospital – Overland Park — 11950 W 110th St.; только overland-park-ks
**Контакт:** 913.642.9563 | 913.381.0421 | 11950 W 110th St. | Overland Park, | KS                                    66210 · 913-642-9563.
**Проверка:** 2026-10-12T00:53:36.859002+00:00; действующий официальный overview с текущими контактами/записью.

Heather Heeb — DACVIM (Oncology). Brenna Williams — DACVS (SA), текущая биография прямо описывает совместную работу с medical oncologist и операции при раке кости/кожных опухолях. Это подтверждает местные онкологические операции, без выдуманной oncology board certification хирурга.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Heather Heeb — DVM, DACVIM (Oncology); Oncology.
- Dana White — DVM, MS, DACVS (SA); Surgery.
- Brenna Williams — DVM, MS, DACVS (SA); Surgery.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

```json
{
  "name": "BluePearl Pet Hospital – Overland Park",
  "street": "11950 W 110th Street",
  "city": "Overland Park",
  "region": "KS",
  "postal_code": "66210",
  "phone": "913-642-9563",
  "website": "https://bluepearlvet.com/hospital/overland-park-ks/specialties-services/oncology/",
  "services": [
    "Medical oncology",
    "Chemotherapy",
    "Surgery"
  ]
}
```

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/overland-park-ks/) — «BluePearl Pet Hospital | Overland Park, KS»; 2026-10-12T00:53:36.859002+00:00; HTTP 200; scope `overland-park-ks`.
- [Local services](https://bluepearlvet.com/hospital/overland-park-ks/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Overland Park KS»; 2026-10-12T00:53:36.974471+00:00; HTTP 200; scope `overland-park-ks`.
- [Local team](https://bluepearlvet.com/hospital/overland-park-ks/our-vets/) — «BluePearl Pet Hospital | Overland Park, KS | Our Vets»; 2026-10-12T00:53:36.877878+00:00; HTTP 200; scope `overland-park-ks`.
- [Oncology](https://bluepearlvet.com/hospital/overland-park-ks/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Overland Park KS»; 2026-10-12T00:53:36.975373+00:00; HTTP 200; scope `overland-park-ks`.
- [Surgery](https://bluepearlvet.com/hospital/overland-park-ks/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Overland Park KS»; 2026-10-12T00:54:19.050413+00:00; HTTP 200; scope `overland-park-ks`.
- [Appointment](https://bluepearlvet.com/hospital/overland-park-ks/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:19.075173+00:00; HTTP 200; scope `overland-park-ks`.
- [Referring vets](https://bluepearlvet.com/hospital/overland-park-ks/referring-vets/) — «BluePearl Pet Hospital | Overland Park, KS | Referring Vets»; 2026-10-12T00:56:04.103446+00:00; HTTP 200; scope `overland-park-ks`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** supporting_urls.
**Unresolved:** отдельных вопросов по исходным утверждениям не осталось; непубликуемые дополнительные услуги не добавлены.

### 25. BluePearl Pet Hospital – Port Washington — `bluepearl-pet-hospital-port-washington`

**branch_scope:** BluePearl Pet Hospital – Port Washington — 207 W Seven Hills Rd; только port-washington-wi
**Контакт:** 262.268.7800 | 207 W Seven Hills Rd | Port Washington, | WI                                    53074 · 262-268-7800.
**Проверка:** 2026-10-12T00:53:36.981069+00:00; действующий официальный overview с текущими контактами/записью.

Rachel Reiman — DACVIM (Oncology), обслуживает также Glendale. Janice Buback — DACVS, местные ортопедические/soft tissue операции; отдельная oncology certification не опубликована. Ограниченные emergency часы не означают закрытие филиала.

**Опубликованная текущая команда (относящиеся к oncology/surgery):**

- Janice Buback — DVM, MS, DACVS; Surgery.
- Rachel Reiman — DVM, DACVIM (Oncology); Oncology.

**Проверенные поля без контактного изменения:** адрес, город/штат/ZIP, телефон (кроме заполнения пустых исходных телефонов), филиальная идентичность, официальный сайт/booking route. Пунктуация адресов нормализована только для сравнения; отсутствие supplemental явно указано ниже. Проверены врачебная специальность/сертификация, local service list, формат записи/направления.

**Исходный supplemental:**

```json
{
  "name": "BluePearl Pet Hospital – Port Washington",
  "street": "207 W Seven Hills Road",
  "city": "Port Washington",
  "region": "WI",
  "postal_code": "53074",
  "phone": "262-268-7800",
  "website": "https://bluepearlvet.com/hospital/port-washington-wi/specialties-services/oncology/",
  "services": [
    "Medical oncology",
    "Chemotherapy",
    "Radiation oncology",
    "Immunotherapy",
    "Surgery"
  ]
}
```

**Источники и короткие опорные цитаты:**

- [Overview/contact](https://bluepearlvet.com/hospital/port-washington-wi/) — «BluePearl Pet Hospital | Port Washington, WI»; 2026-10-12T00:53:36.981069+00:00; HTTP 200; scope `port-washington-wi`.
- [Local services](https://bluepearlvet.com/hospital/port-washington-wi/specialties-services/) — «BluePearl Pet Hospital – Veterinary Specialists Port Washington WI»; 2026-10-12T00:53:36.986396+00:00; HTTP 200; scope `port-washington-wi`.
- [Local team](https://bluepearlvet.com/hospital/port-washington-wi/our-vets/) — «BluePearl Pet Hospital | Port Washington, WI | Our Vets»; 2026-10-12T00:53:36.985023+00:00; HTTP 200; scope `port-washington-wi`.
- [Oncology](https://bluepearlvet.com/hospital/port-washington-wi/specialties-services/oncology/) — «Veterinary Oncology by BluePearl Port Washington WI»; 2026-10-12T00:53:36.989972+00:00; HTTP 200; scope `port-washington-wi`.
- [Surgery](https://bluepearlvet.com/hospital/port-washington-wi/specialties-services/surgery/) — «Veterinary Surgery by BluePearl Port Washington WI»; 2026-10-12T00:54:19.121877+00:00; HTTP 200; scope `port-washington-wi`.
- [Appointment](https://bluepearlvet.com/hospital/port-washington-wi/request-appointment/) — «Request Appointment - BluePearl Pet Hospital»; 2026-10-12T00:54:19.152668+00:00; HTTP 200; scope `port-washington-wi`.
- [Referring vets](https://bluepearlvet.com/hospital/port-washington-wi/referring-vets/) — «BluePearl Pet Hospital | Port Washington, WI | Referring Vets»; 2026-10-12T00:56:04.125794+00:00; HTTP 200; scope `port-washington-wi`.

Запись: прямой звонок или направление primary vet; обе возможности опубликованы на oncology странице.

**Предложения:** supporting_urls.
**Unresolved:** B01-Q02, B01-Q06.

## Конкретные подтверждённые дополнения

- Framingham: химиотерапия на местной oncology странице; текущая хирургическая практика Janis Lapsley прямо занимается лечением рака. Supplemental сейчас содержит только Medical oncology.
- Lafayette: локальные IV/oral chemotherapy, Surgery, ECT, Immunotherapy; external beam RT referrals. Supplemental для назначенного source_id отсутствует — новое дополнение требует полного контактного ряда, не метаданных вместо клиники.
- Пустые исторические телефоны заполняются только текущими местными номерами. Nashville: исходный 615-383-2600 совпадает, телефон не меняется.
- Inventory: старые ACVIM master заменяются/дополняются филиальными BluePearl страницами; известные местные master сохраняются. Не переносить иной филиал из автоматического redirect.

## Ограничения и проверка файлов

Неуспешные guessed URL не являются блокером: NYC, Christiana и Levittown проверены по фактическим midtown-nyc/christiana-de/vsec-levittown-pa маршрутам. Some invalid paths redirected to Skokie/other branches with HTTP 200; they were rejected as wrong-identity evidence. radiation-oncology URLs returned 404; реальные oncology/team/overview/services/booking/referring-vets страницы просмотрены вместо них. Ни один 404 не принят как доказательство закрытия услуги.

Maitland: поисковая копия с Goodson расходится с прямым HTTP и Web-open команды; сохранён вопрос о текущей доступности. Для ECT есть прямые филиальные строки Treatment plans; прежняя неопределённость Arden Hills/Fort Myers исправлена. Спорные local modalities остаются unresolved, а не «услуги нет».

JSON разобран; обязательные поля изменений, official domain, quotes-as-substrings, scope 25/25 и отсутствие чужих source_id проверены. Сборка/production tests не выполнялись: production файлы не менялись. Исходные файлы сверены с полученными remote main версиями по содержимому; локальных изменений в них нет.
