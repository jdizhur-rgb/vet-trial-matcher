# C04 — проверка 20 филиалов VCA

Дата проверки: 12 октября 2026. Все 20 назначенных source_id найдены в актуально полученном inventory. Подготовлено 42 полевых предложений; база и публикация не изменялись.

## Исходные данные и ограничения

Прочитаны актуальные AGENTS.md и PROJECT_OPERATIONS.md целиком. Inventory использует ключ `id`, а не `source_id`. Supplemental содержит 13 из 20 карточек по точному названию, без source_id; остальные семь найдены в производном oncology_centers.json. Значения из этого файла явно обозначены как derived baseline в JSON. Для нового поля clinicians исходное значение отсутствует в этих файлах — это обозначено отдельно, а не выдумано.

Текущие официальные веб-страницы проверены прямым HTTP чтением; поисковая выдача использована только для дополнительных маршрутов. Доступный roster проверен отдельно от услуг. Статус «действует» означает действующий опубликованный филиальный сайт с текущими контактами/часами; качество лечения и лицензии независимо не проверялись. Отсутствие врача в roster не доказывает отсутствие услуги. Шаблонный рассказ о способах лечения не равен фактическому местному предложению.

## Принятые решения

- Добавить подтверждённые местные услуги Sacramento, Shoreline, South Shore, SouthPaws, Westbury, Woodland Hills и West Coast.
- Исправить смешанную запись VREC CT на Norwalk, сохранив историю ACVIM. Katonah Bedford остаётся отдельной клиникой.
- Убрать неподтверждённую местную Chemotherapy у Stirling Square, White Oak и Whitman. Клиники сохранить; отсутствие лечения не утверждать.
- Сохранить Chemotherapy у San Francis, Spring Creek, Three Notch, Tiara Rado, Valley, West Suburban, Willow Creek; physician qualification хранить отдельно.
- Madison: опубликованные услуги сохранить, текущих Shiu/Robat не переносить с Middleton. Новая oncology запись именно на Madison остаётся вопросом следующего прохода.

## Проверка по филиалам

### 1. VCA Sacramento Veterinary Referral Center

`vca-sacramento-veterinary-referral-center`

**Контакты и работа.** 9801 Old Winery Place, Sacramento, CA, 95827; телефон 916-362-3111. [Официальный филиал](https://vcahospitals.com/sacramento-veterinary-referral-center). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Исправить официальный URL и заполнить телефон; добавить местную химиотерапию, опубликованную иммунотерапию и RT Halcyon. Сохранить медицинскую онкологию. Не выводить surgical oncology из обычного отделения Surgery.

**Подтверждённый список услуг после решения:** Medical oncology, Chemotherapy, Immunotherapy, Radiation oncology.

**Текущие профильные врачи.** Danielle O'Brien — Medical oncology, DVM, DACVIM/Oncology, cVMA; Jenny Schutte — Radiation oncology, DVM, DACVR-RO.

**Обращение/формат.** Физический филиал. Плановая specialty consultation по записи; на сайте есть referral form и передача records. Круглосуточная emergency работа не означает круглосуточный приём онколога. Обязательность направления для всех owner appointments не установлена. Oncology liaison: 916-361-5222; hospital main: 916-362-3111.

**Уверенность:** high.

**Следующий проход:**

- Конкретный продукт иммунотерапии не установлен; общий раздел ONCEPT в шаблонном тексте не является подтверждением его применения здесь.
- Специализированная хирургия опухолей отдельно не подтверждена; обычные DACVS-SA хирурги не равны surgical oncology fellow.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:29:49.093892+00:00 — 2026-10-12T22:33:35.799063+00:00.

- https://vcahospitals.com/sacramento-veterinary-referral-center
- https://vcahospitals.com/sacramento-veterinary-referral-center/team
- https://vcahospitals.com/sacramento-veterinary-referral-center/contact-us
- https://vcahospitals.com/sacramento-veterinary-referral-center/departments/medical-oncology
- https://vcahospitals.com/sacramento-veterinary-referral-center/departments/medical-oncology/chemotherapy
- https://vcahospitals.com/sacramento-veterinary-referral-center/departments/medical-oncology/immunotherapy
- https://vcahospitals.com/sacramento-veterinary-referral-center/departments/radiation-oncology
- https://vcahospitals.com/sacramento-veterinary-referral-center/for-vets/referral-forms
- https://vcahospitals.com/sacramento-veterinary-referral-center/team/danielle-obrien
- https://vcahospitals.com/sacramento-veterinary-referral-center/team/jenny-schutte

### 2. VCA San Francis Animal Hospital

`vca-san-francis-animal-hospital`

**Контакты и работа.** 16901 Shady Hills Road, Spring Hill, FL, 34610; телефон 352-848-0940. [Официальный филиал](https://vcahospitals.com/san-francis/). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Без изменения карточки: сохранить Chemotherapy по местному списку услуг и отдельной странице. Сертифицированный онколог не подтверждён; химиотерапию из-за этого не убирать.

**Подтверждённый список услуг после решения:** Chemotherapy.

**Проверенный roster.** Carlos Campos — DVM, medical director; Marybeth Lowe — DVM; Katieri Smith — veterinarian, степень на roster не опубликована; Kinga Szakacs — DVM.

**Обращение/формат.** Физический general-practice филиал, обращение через местную запись/телефон. Сайт не подтверждает мобильный формат или приезжающего oncology specialist. Live chat/myVCA не является подтверждённой oncology teleconsultation.

**Уверенность:** high.

**Следующий проход:**

- Какие препараты/диагнозы принимают и кто выполняет лечение, сайт не уточняет; наличие постоянного или приглашённого oncology specialist не установлено.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:29:49.094228+00:00 — 2026-10-12T22:29:56.882435+00:00.

- https://vcahospitals.com/san-francis
- https://vcahospitals.com/san-francis/team
- https://vcahospitals.com/san-francis/services
- https://vcahospitals.com/san-francis/contact-us
- https://vcahospitals.com/san-francis/services/advanced-care/chemotherapy

### 3. VCA Shoreline Veterinary Referral and Emergency Center

`vca-shoreline-veterinary-referral-and-emergency-center`

**Контакты и работа.** 895 Bridgeport Ave, Shelton, CT, 06484; телефон 203-929-8600. [Официальный филиал](https://vcahospitals.com/shoreline). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Добавить Chemotherapy: она прямо включена в Our Oncology Services. Сохранить текущего сертифицированного онколога Kate Taikowski. Не добавлять RT, immunotherapy или ONCEPT из общей образовательной части страницы.

**Подтверждённый список услуг после решения:** Medical oncology, Chemotherapy.

**Текущие профильные врачи.** Kate Taikowski — Medical oncology, DVM, MS, DACVIM/Oncology.

**Обращение/формат.** Физический филиал. Плановая specialty consultation по записи; на сайте есть referral form и передача records. Круглосуточная emergency работа не означает круглосуточный приём онколога. Обязательность направления для всех owner appointments не установлена.

**Уверенность:** high.

**Следующий проход:**

- Местные RT, ONCEPT, ECT и специализированная surgical oncology не подтверждены. Интерес врача к сотрудничеству с radiation oncologists не доказывает местный аппарат.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:29:49.096554+00:00 — 2026-10-12T22:33:35.802698+00:00.

- https://vcahospitals.com/shoreline
- https://vcahospitals.com/shoreline/team
- https://vcahospitals.com/shoreline/contact-us
- https://vcahospitals.com/shoreline/departments/oncology
- https://vcahospitals.com/shoreline/departments/oncology/chemotherapy
- https://vcahospitals.com/shoreline/for-vets/referral-forms
- https://vcahospitals.com/shoreline/team/kate-taikowski

### 4. VCA South Shore (Weymouth) Animal Hospital

`vca-south-shore-weymouth-animal-hospital`

**Контакты и работа.** 595 Columbian St, South Weymouth, MA, 02190; телефон 781-337-6622. [Официальный филиал](https://vcahospitals.com/south-shore-weymouth/specialty/departments/medical-oncology). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Сохранить исходные пять услуг и добавить Surgical oncology: филиал прямо заявляет surgical management опухолей; William Snell имеет ACVS fellowship. Specialty phone 781-337-6622 оставить; 781-534-7455 относится к Primary Care. Kelly Hicks не включать в текущий roster: персональная ссылка перенаправляет на team, а в текущем списке её нет.

**Подтверждённый список услуг после решения:** Medical oncology, Chemotherapy, ECT, Immunotherapy, ONCEPT, Surgical oncology.

**Текущие профильные врачи.** Torri Cicchirillo — Medical oncology, DVM, DACVIM (Oncology); Meredith Gumash — Medical oncology, DVM, DACVIM (Oncology); William Snell — Surgical oncology, DVM, DACVS-SA, ACVS Fellow (Surgical Oncology).

**Обращение/формат.** Физический филиал. Плановая specialty consultation по записи; на сайте есть referral form и передача records. Круглосуточная emergency работа не означает круглосуточный приём онколога. Обязательность направления для всех owner appointments не установлена.

**Уверенность:** high.

**Следующий проход:**

- Причина отсутствия Kelly Hicks не установлена: не утверждать уход, пенсию или закрытие услуги.
- DACVR диагностических радиологов не подтверждает местную RT.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:29:49.097510+00:00 — 2026-10-12T22:33:35.803667+00:00.

- https://vcahospitals.com/south-shore-weymouth/specialty
- https://vcahospitals.com/south-shore-weymouth/specialty/team
- https://vcahospitals.com/south-shore-weymouth/specialty/contact-us
- https://vcahospitals.com/south-shore-weymouth/specialty/departments/medical-oncology
- https://vcahospitals.com/south-shore-weymouth/specialty/departments/medical-oncology/chemotherapy
- https://vcahospitals.com/south-shore-weymouth/specialty/departments/medical-oncology/electrochemotherapy
- https://vcahospitals.com/south-shore-weymouth/specialty/departments/medical-oncology/immunotherapy
- https://vcahospitals.com/south-shore-weymouth/specialty/departments/surgical-oncology
- https://vcahospitals.com/south-shore-weymouth/specialty/for-vets/referral-forms
- https://vcahospitals.com/south-shore-weymouth/specialty/team/torri-cicchirillo
- https://vcahospitals.com/south-shore-weymouth/specialty/team/meredith-gumash
- https://vcahospitals.com/south-shore-weymouth/specialty/team/william-snell

### 5. VCA SouthPaws Veterinary Specialists and Emergency

`vca-southpaws-veterinary-specialists-and-emergency`

**Контакты и работа.** 8500 Arlington Blvd, Fairfax, VA, 22031; телефон 703.752.9100. [Официальный филиал](https://vcahospitals.com/southpaws). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Добавить Chemotherapy, Immunotherapy и местную RT: отдельный местный аппарат Varian 2100 EX/IMRT и текущая Lily Thorsen. Metronomic Therapy отражена как режим химиотерапии, без нового отдельного filter tag. ECT в specialties Alyssa Przydrozny — обоснованное указание её местной компетенции, но фактическая доступность аппарата/сеансов здесь не подтверждена; пока вне confirmed services.

**Подтверждённый список услуг после решения:** Medical oncology, Chemotherapy, Immunotherapy, Radiation oncology.

**Текущие профильные врачи.** Daniela Korec — Medical oncology, DVM, DACVIM (Oncology); Jack O'Day — Medical oncology, DVM, DACVIM (Oncology); Alyssa Przydrozny — Medical oncology, DVM, DACVIM (Oncology); Sarah Sheafor — Medical oncology, DVM, DACVIM (Oncology); Lily Thorsen — Radiation oncology, DVM, DACVR (RO).

**Обращение/формат.** Физический филиал. Плановая specialty consultation по записи; на сайте есть referral form и передача records. Круглосуточная emergency работа не означает круглосуточный приём онколога. Обязательность направления для всех owner appointments не установлена.

**Уверенность:** high.

**Следующий проход:**

- ECT: текущая биография перечисляет компетенцию врача, но нет отдельного доказательства выполняемых в Fairfax сеансов. Уровень вывода moderate; услугу пока не добавлять.
- Текст отдела говорит о пяти medical oncologists, roster содержит четыре плюс radiation oncologist. Для текущего медицинского состава использовать roster, а не старую цифру в тексте.
- Конкретный продукт иммунотерапии и актуальный перечень targeted drugs не установлены.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:29:49.099211+00:00 — 2026-10-12T22:33:35.804502+00:00.

- https://vcahospitals.com/southpaws
- https://vcahospitals.com/southpaws/team
- https://vcahospitals.com/southpaws/contact-us
- https://vcahospitals.com/southpaws/departments/oncology
- https://vcahospitals.com/southpaws/departments/oncology/chemotherapy
- https://vcahospitals.com/southpaws/departments/oncology/immunotherapy
- https://vcahospitals.com/southpaws/departments/radiation-oncology
- https://vcahospitals.com/southpaws/for-vets/referral-forms
- https://vcahospitals.com/southpaws/team/daniela-korec
- https://vcahospitals.com/southpaws/team/jack-oday
- https://vcahospitals.com/southpaws/team/alyssa-przydrozny
- https://vcahospitals.com/southpaws/team/sarah-sheafor
- https://vcahospitals.com/southpaws/team/lily-thorsen

### 6. VCA Spring Creek Animal Care Hospital

`vca-spring-creek-animal-care-hospital`

**Контакты и работа.** 1035 W. Broadway, Jackson Hole, WY, 83001; телефон 307-733-1606. [Официальный филиал](https://vcahospitals.com/spring-creek/). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Без изменения карточки: сохранить Chemotherapy независимо от отсутствия подтверждённого oncology specialist. Robert Dyke имеет DABVP, это не DACVIM Oncology.

**Подтверждённый список услуг после решения:** Chemotherapy.

**Проверенный roster.** Owen Black — DVM; Robert Dyke — DVM, DABVP; Leigh Farrell — DVM; Salene Freeman — DVM; Stephanie Ninnemann — DVM, MS; Kaley Parent — DVM, rehabilitation/acupuncture; Ernie Patterson — DVM.

**Обращение/формат.** Физический general-practice филиал, обращение через местную запись/телефон. Сайт не подтверждает мобильный формат или приезжающего oncology specialist. Live chat/myVCA не является подтверждённой oncology teleconsultation.

**Уверенность:** high.

**Следующий проход:**

- Назначенный врач, конкретные препараты и участие внешнего онколога не опубликованы.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:29:49.099876+00:00 — 2026-10-12T22:29:56.697502+00:00.

- https://vcahospitals.com/spring-creek
- https://vcahospitals.com/spring-creek/team
- https://vcahospitals.com/spring-creek/services
- https://vcahospitals.com/spring-creek/contact-us
- https://vcahospitals.com/spring-creek/services/advanced-care/chemotherapy

### 7. VCA Stirling Square Animal Hospital

`vca-stirling-square-animal-hospital`

**Контакты и работа.** 3000 Stirling Road, Suite 132, Hollywood, FL, 33021; телефон 954-963-5300. [Официальный филиал](https://vcahospitals.com/stirling-square/). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Убрать Chemotherapy только из подтверждённых услуг. Oncology есть в филиальном списке, но текст не описывает местную химиотерапию. Сохранить клинику, адрес, контакты и Local oncology care.

**Подтверждённый список услуг после решения:** Local oncology care.

**Проверенный roster.** Jaime Amaya — DVM, medical director; Rene Ley — DVM, associate veterinarian. Подтверждения oncology board certification нет.

**Обращение/формат.** Физический general-practice филиал, обращение через местную запись/телефон. Сайт не подтверждает мобильный формат или приезжающего oncology specialist. Live chat/myVCA не является подтверждённой oncology teleconsultation.

**Уверенность:** high for catalog correction; actual chemotherapy availability unknown.

**Следующий проход:**

- Химиотерапия не подтверждена после чтения services, advanced care, oncology, team, биографий Amaya/Ley и дополнительного поиска. Это не утверждение, что её не выполняют.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:30:00.665754+00:00 — 2026-10-12T22:32:35.849070+00:00.

- https://vcahospitals.com/stirling-square
- https://vcahospitals.com/stirling-square/team
- https://vcahospitals.com/stirling-square/services
- https://vcahospitals.com/stirling-square/contact-us
- https://vcahospitals.com/stirling-square/services/advanced-care/oncology
- https://vcahospitals.com/stirling-square/services/advanced-care

### 8. VCA Three Notch Animal Hospital

`vca-three-notch-animal-hospital`

**Контакты и работа.** 44215 Airport View Drive, Hollywood, MD, 20636; телефон 301-373-8633. [Официальный филиал](https://vcahospitals.com/three-notch/). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Без изменения карточки: сохранить Chemotherapy по местному Available Services и отдельной странице. Не добавлять RT или specialized surgical oncology из диагностической радиологии/soft-tissue surgery.

**Подтверждённый список услуг после решения:** Chemotherapy.

**Проверенный roster.** Kara Blankenship; Emily Hurley; Alina McClain — veterinarians, степени в roster не указаны; Jennifer O'Connor-Porter — DVM, co-medical director; Sara Pilkerton — DVM, medical director; Melissa Webb — DVM.

**Обращение/формат.** Физический general-practice филиал, обращение через местную запись/телефон. Сайт не подтверждает мобильный формат или приезжающего oncology specialist. Live chat/myVCA не является подтверждённой oncology teleconsultation.

**Уверенность:** high.

**Следующий проход:**

- Назначенный врач, протоколы химиотерапии и specialist consultation arrangement не указаны.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:30:01.526825+00:00 — 2026-10-12T22:30:09.529906+00:00.

- https://vcahospitals.com/three-notch
- https://vcahospitals.com/three-notch/team
- https://vcahospitals.com/three-notch/services
- https://vcahospitals.com/three-notch/contact-us
- https://vcahospitals.com/three-notch/services/advanced-care/chemotherapy

### 9. VCA Tiara Rado Animal Hospital

`vca-tiara-rado-animal-hospital`

**Контакты и работа.** 2245 3/4 Broadway, Grand Junction, CO, 81507; телефон 970-243-4007. [Официальный филиал](https://vcahospitals.com/tiara-rado/). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Без изменения карточки: сохранить Chemotherapy. Troy Everson — canine/feline ABVP, не oncology board certification. Robert D. Marquis помечен In Memoriam, не действующий врач.

**Подтверждённый список услуг после решения:** Chemotherapy.

**Проверенный roster.** Troy Everson — DVM, ABVP (canine/feline), CCRT, CVA, CVMST; Katie Ferris — DVM; Wendy Harley — CCRT, CVMA (DVM на roster не показан); Tara Suplizio — DVM. Robert D. Marquis исключён из текущего состава по In Memoriam.

**Обращение/формат.** Физический general-practice филиал, обращение через местную запись/телефон. Сайт не подтверждает мобильный формат или приезжающего oncology specialist. Live chat/myVCA не является подтверждённой oncology teleconsultation.

**Уверенность:** high.

**Следующий проход:**

- Текущий ответственный за химиотерапию и допустимые протоколы не опубликованы.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:30:13.109645+00:00 — 2026-10-12T22:30:20.163737+00:00.

- https://vcahospitals.com/tiara-rado
- https://vcahospitals.com/tiara-rado/team
- https://vcahospitals.com/tiara-rado/services
- https://vcahospitals.com/tiara-rado/contact-us
- https://vcahospitals.com/tiara-rado/services/advanced-care/chemotherapy

### 10. VCA Valley Animal Hospital

`vca-valley-animal-hospital`

**Контакты и работа.** 5146 Hildebrand Road, Roanoke, VA, 24012; телефон 540-366-3433. [Официальный филиал](https://vcahospitals.com/valley-va/). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Без изменения карточки: сохранить Local oncology care и Chemotherapy. Дополнительно найдена отдельная филиальная Chemotherapy, поэтому положительная отметка не зависит от общей страницы Oncology.

**Подтверждённый список услуг после решения:** Local oncology care, Chemotherapy.

**Проверенный roster.** Jaime Jonen — DVM; Michael Mannebach — DVM; Corwin Martin — DVM, MPH; Hillary Rader — DVM; Jessica Staley — DVM, medical director.

**Обращение/формат.** Физический general-practice филиал, обращение через местную запись/телефон. Сайт не подтверждает мобильный формат или приезжающего oncology specialist. Live chat/myVCA не является подтверждённой oncology teleconsultation.

**Уверенность:** high.

**Следующий проход:**

- Сертифицированный/приглашённый онколог и конкретные препараты не установлены.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:30:13.128912+00:00 — 2026-10-12T22:30:20.256388+00:00.

- https://vcahospitals.com/valley-va
- https://vcahospitals.com/valley-va/team
- https://vcahospitals.com/valley-va/services
- https://vcahospitals.com/valley-va/contact-us
- https://vcahospitals.com/valley-va/services/advanced-care/chemotherapy
- https://vcahospitals.com/valley-va/services/advanced-care/oncology

### 11. VCA Veterinary Emergency and Referral Center CT

`vca-veterinary-emergency-and-referral-center-ct`

**Контакты и работа.** 123 W. Cedar Street, Norwalk, CT, 06854; телефон 203-854-9960. [Официальный филиал](https://vcahospitals.com/veterinary-referral-and-emergency-center). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Исправить смешанную запись на VCA Veterinary Referral and Emergency Center, Norwalk CT, 123 W. Cedar Street / 06854 / 203-854-9960. Исторический ACVIM профиль Jessica Chin сохранить, но не регенерировать из него адрес Bedford Hills. Не объединять с Katonah Bedford. FidoCure и Stelfonta прямо предложены в нынешней биографии Chin; Chemotherapy — вывод moderate из текущего oncology department, двух врачей и описанной Chin сочетанной терапии. Старые координаты NY обнулить до проверенного geocode.

**Подтверждённый список услуг после решения:** Medical oncology, Chemotherapy, Targeted therapy, Intratumoral therapy, Stelfonta.

**Текущие профильные врачи.** Jessica Chin — Medical oncology, DVM, DACVIM; oncology certification отдельно подтверждается историческим ACVIM snapshot (Текущая VCA страница публикует DACVIM без specialty в скобках; historical ACVIM называет Oncology.); Kayla Neiderfer — Medical oncology, DVM, DACVIM (Текущая страница публикует DACVIM и oncology role; residency 2025. Не расширять подпись до DACVIM (Oncology) без отдельной явной сертификации.).

**Обращение/формат.** Физический филиал. Плановая specialty consultation по записи; на сайте есть referral form и передача records. Круглосуточная emergency работа не означает круглосуточный приём онколога. Обязательность направления для всех owner appointments не установлена.

**Уверенность:** high for identity/address/phone and FidoCure/Stelfonta; moderate for chemotherapy.

**Следующий проход:**

- Прямая oncology URL перенаправляет на departments; это не закрытие отдела: текущие departments и roster всё ещё указывают Oncology.
- Химиотерапия подтверждается совокупностью сведений, не отдельным актуальным перечнем препаратов; типы injectable/oral не установлены.
- Новый точный geocode Norwalk необходимо получить при интеграции; старые NY координаты не использовать.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:30:13.429447+00:00 — 2026-10-12T22:33:35.808094+00:00.

- https://vcahospitals.com/veterinary-referral-and-emergency-center
- https://vcahospitals.com/veterinary-referral-and-emergency-center/team
- https://vcahospitals.com/veterinary-referral-and-emergency-center/contact-us
- https://vcahospitals.com/veterinary-referral-and-emergency-center/departments
- https://vcahospitals.com/veterinary-referral-and-emergency-center/departments/oncology/immunotherapy
- https://vcahospitals.com/veterinary-referral-and-emergency-center/for-vets/referral-forms
- https://vcahospitals.com/veterinary-referral-and-emergency-center/team/kayla-neiderfer
- https://vcahospitals.com/veterinary-referral-and-emergency-center/team/jessica-chin
- https://vcahospitals.com/katonah-bedford/specialty/team
- https://vcahospitals.com/katonah-bedford/specialty/departments/oncology
- https://vcahospitals.com/katonah-bedford/specialty/for-vets/referral-forms

### 12. VCA Veterinary Emergency Referral Center of Westbury

`vca-veterinary-emergency-referral-center-of-westbury`

**Контакты и работа.** 609-5 cantiague rock rd., Westbury, NY, 11590; телефон 516.420.0000. [Официальный филиал](https://vcahospitals.com/westbury). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Заменить общесетевой/старый website на vcahospitals.com/westbury; добавить hospital-listed Chemotherapy и Immunotherapy. Текущий Michael Linderman — DACVIM/Oncology. Не переносить RT или specialized surgical oncology из общесетевой информации.

**Подтверждённый список услуг после решения:** Medical oncology, Chemotherapy, Immunotherapy.

**Текущие профильные врачи.** Michael Linderman — Medical oncology, DVM, DACVIM/Oncology.

**Обращение/формат.** Физический филиал. Плановая specialty consultation по записи; на сайте есть referral form и передача records. Круглосуточная emergency работа не означает круглосуточный приём онколога. Обязательность направления для всех owner appointments не установлена.

**Уверенность:** high.

**Следующий проход:**

- Продукт иммунотерапии, местные RT и ECT не подтверждены. Вакансия онколога не означает отсутствие действующего Linderman.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:30:15.404788+00:00 — 2026-10-12T22:33:35.808997+00:00.

- https://vcahospitals.com/westbury
- https://vcahospitals.com/westbury/team
- https://vcahospitals.com/westbury/contact-us
- https://vcahospitals.com/westbury/departments/oncology
- https://vcahospitals.com/westbury/departments/oncology/chemotherapy
- https://vcahospitals.com/westbury/departments/oncology/immunotherapy
- https://vcahospitals.com/westbury/for-vets/referral-forms
- https://vcahospitals.com/westbury/team/michael-linderman

### 13. VCA Veterinary Emergency Service & Veterinary Specialty Center

`vca-veterinary-emergency-service-veterinary-specialty-center`

**Контакты и работа.** 4902 East Broadway, Madison, WI, 53716; телефон 608-222-2455. [Официальный филиал](https://vcahospitals.com/veterinary-specialty-center-madison/). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Сохранить Madison 4902 East Broadway, Medical oncology и Chemotherapy как опубликованные филиалом услуги; не утверждать, что их не выполняют из-за пустого specialty roster. Не приписывать Madison врачей Kai Shiu и Cecilia Robat: их текущие страницы относятся к Middleton. Пока не расширять услуги Madison на immunotherapy/RT по общей сети. Отметить расхождение roster/services и неопределённость нового specialty appointment.

**Подтверждённый список услуг после решения:** Medical oncology, Chemotherapy.

**Проверенный roster.** На Madison roster опубликован Dana King — DVM, DACVS (surgery), а также ER/general staff: Rachel Bradshaw, Lydia Colopy, Emily Duane (DVM), Carli Fawcett, Lisa Flood (DVM), Allison Gunn, Heidi Haw (DVM), Rachel Hawley (DVM), Megan Jordan (DVM), Ashley Kelly, Mykayla Muench, Kate Palmer, Emily Paulson (DVM), Abby Rothering, Melissa Shear (DVM), Samantha Trollope. Kai Shiu — BVMS, MRCVS, DACVIM (Oncology) и Cecilia Robat — DVM, DACVIM (Oncology) подтверждены в Middleton, не Madison.

**Обращение/формат.** Физический филиал. Плановая specialty consultation по записи; на сайте есть referral form и передача records. Круглосуточная emergency работа не означает круглосуточный приём онколога. Обязательность направления для всех owner appointments не установлена. Неопределённость текущей specialty записи именно на Madison сохранена отдельно.

**Уверенность:** moderate for current local treatment access; high for Middleton clinician attribution.

**Следующий проход:**

- Установить в следующем проходе, принимают ли новые oncology/chemo cases на Madison East, кто назначен и является ли местная страница сохранённой старой страницей. Доступное доказательство не позволяет объявить лечение отсутствующим.
- Нельзя переносить Middleton специалистов и услуги на Madison по общему названию VES/VSC. Middleton проверен только для разрешения адресной привязки C04, его отдельную карточку не менять.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:30:20.267908+00:00 — 2026-10-12T22:33:40.237664+00:00.

- https://vcahospitals.com/veterinary-specialty-center-madison
- https://vcahospitals.com/veterinary-specialty-center-madison/team
- https://vcahospitals.com/veterinary-specialty-center-madison/contact-us
- https://vcahospitals.com/veterinary-specialty-center-madison/departments/oncology
- https://vcahospitals.com/veterinary-specialty-center-madison/departments/oncology/chemotherapy
- https://vcahospitals.com/veterinary-specialty-center-madison/departments/oncology/immunotherapy
- https://vcahospitals.com/veterinary-specialty-center-madison/for-vets/referral-forms
- https://vcahospitals.com/veterinary-specialty-center-middleton/team
- https://vcahospitals.com/veterinary-specialty-center-middleton/departments/oncology

### 14. VCA Veterinary Specialists of the Valley

`vca-veterinary-specialists-of-the-valley`

**Контакты и работа.** 22123 Ventura Blvd, Woodland Hills, CA, 91364; телефон 818.883.8387. [Официальный филиал](https://vcahospitals.com/veterinary-specialists-valley). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Добавить Chemotherapy и Immunotherapy из Our Oncology Services. John Chretin и Mark Jeon — нынешние medical oncologists. Историческое создание Chretin bone-marrow transplant программы в West Los Angeles не подтверждает transplant в Woodland Hills.

**Подтверждённый список услуг после решения:** Medical oncology, Chemotherapy, Immunotherapy.

**Текущие профильные врачи.** John Chretin — Medical oncology, DVM, DACVIM (Oncology); Mark Jeon — Medical oncology, DVM, DACVIM (Oncology).

**Обращение/формат.** Физический филиал. Плановая specialty consultation по записи; на сайте есть referral form и передача records. Круглосуточная emergency работа не означает круглосуточный приём онколога. Обязательность направления для всех owner appointments не установлена. John Chretin прямо предлагает phone consultations местным ветеринарам; owner remote consultation не установлена.

**Уверенность:** high.

**Следующий проход:**

- RT, ECT, transplant и specialized surgical oncology здесь не подтверждены; конкретный продукт иммунотерапии неизвестен.
- John Chretin предлагает phone consultation местным ветеринарам. Отдельного owner teleoncology appointment не установлено.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:30:23.491655+00:00 — 2026-10-12T22:33:39.834539+00:00.

- https://vcahospitals.com/veterinary-specialists-valley
- https://vcahospitals.com/veterinary-specialists-valley/team
- https://vcahospitals.com/veterinary-specialists-valley/contact-us
- https://vcahospitals.com/veterinary-specialists-valley/departments/oncology
- https://vcahospitals.com/veterinary-specialists-valley/departments/oncology/chemotherapy
- https://vcahospitals.com/veterinary-specialists-valley/departments/oncology/immunotherapy
- https://vcahospitals.com/veterinary-specialists-valley/for-vets/referral-forms
- https://vcahospitals.com/veterinary-specialists-valley/team/john-chretin
- https://vcahospitals.com/veterinary-specialists-valley/team/mark-jeon

### 15. VCA Veterinary Specialty & Emergency Center of Kalamazoo

`vca-veterinary-specialty-emergency-center-of-kalamazoo`

**Контакты и работа.** 5348 S. Westnedge Avenue, Portage, MI, 49002; телефон 269-381-5228. [Официальный филиал](https://vcahospitals.com/kalamazoo/). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Сохранить местную Radiation oncology: Varian TrueBeam и нынешняя Brittney Stanton, DACVR (RO), board certification 2025. Не добавлять chemotherapy/medical oncology из вакансии или наличия radiation oncologist. Steven Baker — DACVS-SA, обычная хирургия, не доказательство specialized surgical oncology.

**Подтверждённый список услуг после решения:** Radiation oncology.

**Текущие профильные врачи.** Brittney Stanton — Radiation oncology, DVM, DACVR (RO).

**Обращение/формат.** Физический филиал. Плановая specialty consultation по записи; на сайте есть referral form и передача records. Круглосуточная emergency работа не означает круглосуточный приём онколога. Обязательность направления для всех owner appointments не установлена.

**Уверенность:** high.

**Следующий проход:**

- Нынешний medical oncologist не найден; вакансия не доказывает отсутствие химиотерапии. Конкретные RT протоколы/доступность SRT должны определяться при oncology appointment.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:30:24.333316+00:00 — 2026-10-12T22:33:40.001056+00:00.

- https://vcahospitals.com/kalamazoo
- https://vcahospitals.com/kalamazoo/team
- https://vcahospitals.com/kalamazoo/contact-us
- https://vcahospitals.com/kalamazoo/departments/radiation-oncology
- https://vcahospitals.com/kalamazoo/for-vets/referral-forms
- https://vcahospitals.com/kalamazoo/team/brittney-stanton

### 16. VCA West Coast Specialty and Emergency Hospital

`vca-west-coast-specialty-and-emergency-hospital`

**Контакты и работа.** 18300 Euclid Street, Fountain Valley, CA, 92708; телефон 714.241.9001. [Официальный филиал](https://vcahospitals.com/west-coast). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Добавить Chemotherapy, Immunotherapy, местную RT (Varian 2100 EX/IMRT) и Surgical oncology. Arathi Vinayak имеет ACVS Fellow Surgical Oncology; Abbey Sadowski — practice limited medical oncology, без неподтверждённой board certification. Bone Marrow Transplant и CERT опубликованы в списке, но для этих редких услуг требуется свежая явная доступность; пока вне подтверждённого списка.

**Подтверждённый список услуг после решения:** Medical oncology, Chemotherapy, Immunotherapy, Radiation oncology, Surgical oncology.

**Текущие профильные врачи.** Samantha Bajorek — Medical oncology, DVM, DACVIM (Medical Oncology); Abbey Sadowski — Medical oncology, DVM (Practice Limited - Medical Oncology) (Board certification не подтверждена.); Cory Wakamatsu — Radiation oncology, DVM, MS, DACVR (RO); Arathi Vinayak — Surgical oncology, DVM, DACVS-SA, ACVS Fellow (Surgical Oncology).

**Обращение/формат.** Физический филиал. Плановая specialty consultation по записи; на сайте есть referral form и передача records. Круглосуточная emergency работа не означает круглосуточный приём онколога. Обязательность направления для всех owner appointments не установлена.

**Уверенность:** high for core modalities and roster; low for current transplant/CERT access.

**Следующий проход:**

- Bone Marrow Transplant/CERT: ссылка и меню сами по себе не разрешают текущую фактическую доступность редкой программы; оставить для отдельного прохода.
- У Bajorek и Wakamatsu отдельные bio страницы дают оболочку без развёрнутого профиля; квалификация опубликована на текущем roster, её источник обозначен именно так.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:30:37.232854+00:00 — 2026-10-12T22:33:40.131128+00:00.

- https://vcahospitals.com/west-coast
- https://vcahospitals.com/west-coast/team
- https://vcahospitals.com/west-coast/contact-us
- https://vcahospitals.com/west-coast/departments/medical-oncology
- https://vcahospitals.com/west-coast/departments/medical-oncology/chemotherapy
- https://vcahospitals.com/west-coast/departments/medical-oncology/immunotherapy
- https://vcahospitals.com/west-coast/departments/radiation-oncology
- https://vcahospitals.com/west-coast/departments/surgical-oncology
- https://vcahospitals.com/west-coast/for-vets/referral-forms
- https://vcahospitals.com/west-coast/team/samantha-bajorek
- https://vcahospitals.com/west-coast/team/abbey-sadowski
- https://vcahospitals.com/west-coast/team/arathi-vinayak
- https://vcahospitals.com/west-coast/team/cory-wakamatsu

### 17. VCA West Suburban Veterinary Hospital

`vca-west-suburban-veterinary-hospital`

**Контакты и работа.** 518 N. Warwick Avenue, Westmont, IL, 60559; телефон 630-968-4212. [Официальный филиал](https://vcahospitals.com/west-suburban/). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Без изменения карточки: сохранить Local oncology care и Chemotherapy. Отдельная страница прямо описывает лечение cancer patients врачами WSVA; отсутствие oncology diplomate не повод удалить химиотерапию.

**Подтверждённый список услуг после решения:** Local oncology care, Chemotherapy.

**Проверенный roster.** Daniella Cantu — DVM; Brittany Childs — DVM; Kyle Kayson — DVM; Emily Nelson — DVM; Steven Zary — DVM, medical director.

**Обращение/формат.** Физический general-practice филиал, обращение через местную запись/телефон. Сайт не подтверждает мобильный формат или приезжающего oncology specialist. Live chat/myVCA не является подтверждённой oncology teleconsultation.

**Уверенность:** high.

**Следующий проход:**

- Протоколы/назначенный врач не указаны; фразу о targeted treatment не превращать в отдельный Targeted therapy filter без конкретной услуги.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:30:37.384572+00:00 — 2026-10-12T22:30:47.261024+00:00.

- https://vcahospitals.com/west-suburban
- https://vcahospitals.com/west-suburban/team
- https://vcahospitals.com/west-suburban/services
- https://vcahospitals.com/west-suburban/contact-us
- https://vcahospitals.com/west-suburban/services/advanced-care/chemotherapy
- https://vcahospitals.com/west-suburban/services/advanced-care/oncology

### 18. VCA White Oak Animal Hospital

`vca-white-oak-animal-hospital`

**Контакты и работа.** 10 Walsh Lane, Fredericksburg, VA, 22405; телефон 540-374-0462. [Официальный филиал](https://vcahospitals.com/white-oak/). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Убрать Chemotherapy только из confirmed services: Oncology страница содержит общий текст, а services/advanced care, roster и доступная biography не подтверждают проведение химиотерапии. Сохранить клинику и Local oncology care.

**Подтверждённый список услуг после решения:** Local oncology care.

**Проверенный roster.** Melanie Bell — DVM; Elysia-Marie Branson — DVM; Sandi Pepper — DVM; Jennifer V. Skarbek — DVM, medical director. Сертифицированный oncology specialist не подтверждён.

**Обращение/формат.** Физический general-practice филиал, обращение через местную запись/телефон. Сайт не подтверждает мобильный формат или приезжающего oncology specialist. Live chat/myVCA не является подтверждённой oncology teleconsultation.

**Уверенность:** high for catalog correction; actual chemotherapy availability unknown.

**Следующий проход:**

- Местная химиотерапия не подтверждена, не отрицать её существование. В следующем проходе искать новые конкретные branch-treatment сведения, а не повторно переносить общую Oncology страницу.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:30:37.434934+00:00 — 2026-10-12T22:32:35.842240+00:00.

- https://vcahospitals.com/white-oak
- https://vcahospitals.com/white-oak/team
- https://vcahospitals.com/white-oak/services
- https://vcahospitals.com/white-oak/contact-us
- https://vcahospitals.com/white-oak/services/advanced-care/oncology
- https://vcahospitals.com/white-oak/services/advanced-care

### 19. VCA Whitman Animal Hospital

`vca-whitman-animal-hospital`

**Контакты и работа.** 795 Bedford Street, Whitman, MA, 02382; телефон 781-447-0011. [Официальный филиал](https://vcahospitals.com/whitman/). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Убрать местную Chemotherapy из confirmed services, сохранить local cancer assessment и добавить Oncology referral. Сайт направляет в South Shore и описывает chemotherapy Dr. Finney at Hanson; это другой филиал. Телефонные консультации описаны для treating veterinarian, не owner teleoncology и не доказательство приезда онколога в Whitman.

**Подтверждённый список услуг после решения:** Local oncology care, Oncology referral.

**Проверенный roster.** Nichole Correia — DVM; Katerina Hatzidis — DVM; Laura Serbin — DVM. Постоянный либо приглашённый board-certified онколог в Whitman не подтверждён.

**Обращение/формат.** Физический general-practice филиал, обращение через местную запись/телефон. Сайт не подтверждает мобильный формат или приезжающего oncology specialist. Live chat/myVCA не является подтверждённой oncology teleconsultation. Указана телефонная помощь oncology specialists лечащему ветеринару, а сложные случаи направляются в South Shore; chemotherapy Hanson отделена от Whitman.

**Уверенность:** high for separating branches; actual Whitman chemotherapy unknown.

**Следующий проход:**

- Есть ли собственная местная химиотерапия Whitman, помимо внешнего Hanson/South Shore, остаётся неизвестным. Не писать 'не выполняют'.
- Свежесть упоминания Dr. Finney at Hanson не установлена; использовать как опубликованный referral lead с предупреждением проверить доступность, не как подтверждённую текущую услугу Hanson.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:30:48.221836+00:00 — 2026-10-12T22:30:55.611818+00:00.

- https://vcahospitals.com/whitman
- https://vcahospitals.com/whitman/team
- https://vcahospitals.com/whitman/services
- https://vcahospitals.com/whitman/contact-us
- https://vcahospitals.com/whitman/services/advanced-care/oncology

### 20. VCA Willow Creek Pet Center

`vca-willow-creek-pet-center`

**Контакты и работа.** 2055 East Creek Road, Cottonwood Heights, UT, 84093; телефон 801-942-0777. [Официальный филиал](https://vcahospitals.com/willow-creek/). Публичный филиал с часами работы сохранён; доказательств закрытия нет.

**Решение.** Без изменения карточки: сохранить Local oncology care и Chemotherapy — есть отдельная местная Chemotherapy и запись в advanced-care списке, независимо от отсутствия oncologist в roster.

**Подтверждённый список услуг после решения:** Local oncology care, Chemotherapy.

**Проверенный roster.** Angela Ahlstrom — DVM, CVA; Aaron Barney — DVM, medical director; Jeonghwa Kim — DVM, MSc; Deanna Mitchell — DVM; Veronica Quintana — DVM; Kate Walters — DVM.

**Обращение/формат.** Физический general-practice филиал, обращение через местную запись/телефон. Сайт не подтверждает мобильный формат или приезжающего oncology specialist. Live chat/myVCA не является подтверждённой oncology teleconsultation.

**Уверенность:** high.

**Следующий проход:**

- Назначенный химиотерапевт и доступные препараты/диагнозы не опубликованы. Ветеринарная acupuncture credential не oncology board certification.

**Проверенные поля и источники.** Контакты/адрес/работа, roster/квалификация, услуги, направление/запись и mobile/remote признаки проверены по следующим URL. Дата/время конкретного источника сохранены в предложениях JSON; общий диапазон попыток 2026-10-12T22:30:49.060441+00:00 — 2026-10-12T22:30:56.254672+00:00.

- https://vcahospitals.com/willow-creek
- https://vcahospitals.com/willow-creek/team
- https://vcahospitals.com/willow-creek/services
- https://vcahospitals.com/willow-creek/contact-us
- https://vcahospitals.com/willow-creek/services/advanced-care/chemotherapy
- https://vcahospitals.com/willow-creek/services/advanced-care/oncology

## Доказательства изменений и применение

Каждое поле в C04-proposed_changes.json содержит source_id, field, old_value, new_value, evidence_url, короткую точную supporting_quote, фактический checked_at и branch_scope. Дополнительные источники RT/врачей представлены отдельно. Выводы moderate явно отделены от прямых утверждений сайта. Списки услуг — предложение целиком, а не удаление клиник.

Исходные файлы сняты отдельными чтениями remote main; другие чаты могут изменять main параллельно. Перед применением сверить old_value с новым main. Для семь ACVIM-derived карточек использовать устойчивый same-location supplemental override. Для Norwalk не оставлять старую геоточку NY и не возвращать смешанный raw профиль при сборке.

Никаких писем клиникам, trial audit, изменений общих файлов или публикации этим пакетом не выполнено. Нерешённые вопросы перечислены по каждому филиалу и сохранены в JSON records.unresolved. Это полный проход по назначенному пакету с отмеченными ограничениями публичных источников, не полный аудит сети VCA.

## Даты проверки источников

20/20 назначенных филиалов проверены. Новые даты inventory в main: 0/20, намеренно не записаны по запрету пользователя. Remote publication/production readback не выполнялись. Точные timestamp попыток, old_value provenance и SHA256 исходных локальных снимков сохранены в JSON.
