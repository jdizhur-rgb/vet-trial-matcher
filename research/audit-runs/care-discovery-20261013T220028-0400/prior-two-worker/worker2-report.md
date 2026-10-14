# Тест делегирования — исполнитель 2

Проверены три назначенные записи по текущим официальным страницам 12 октября 2026 года по America/New_York (13 октября UTC). Исходные значения получены из текущего снимка репозитория, а не восстановлены из названий в старом задании.

Исполнитель: `/root/scheduled_worker2`. Первый фактический замер shell: **2026-10-13T02:17:22Z**. Исследование закончено: **2026-10-13T02:19:38Z**. Время создания субагента хранится отдельно у главного исполнителя. База, исходники сайта и Git не изменялись; публикация не выполнялась.

Обработано **3/3**. Контакты, идентичность, существующие услуги и квалификации сверены у всех трёх. Строгий показатель «полностью проверено без оставшихся вопросов» — **1/3**: UTSW и VSNT сохраняют конкретные ограничения доступа/расписания. Это не неподтверждённость самих клиник.

## Принятые решения

Клинические факты в текущем supplemental исправлять не требуется. Предлагаются **три технические замены master_url** в source inventory: вместо импортированной страницы специалиста использовать проверенную официальную страницу филиала. Сохранить прежние registry URL как происхождение данных. Предложения содержатся в `proposed_changes.json`; они не внесены в базу.

## 1. UT Southwestern Veterinary Research and Oncology Clinic, Dallas

ID: `veterinary-specialists-of-north-texas`.

Старое название VSNT Dallas уже исправлено в актуальной базе. Официальный контакт подтверждает 5801 Forest Park, Dallas TX 75235, телефон **214-645-6221**. Сохранить текущую идентичность UTSW. Не переносить Sara Allstadt обратно: её текущая VSNT-биография прямо описывает возвращение из UTSW.

Текущая команда подтверждает Jonathan Maddox, DVM, clinical assistant professor, и Isabelle Vanhaezebrouck, DVM, MS. Её отдельный профиль подтверждает radiation oncology ACVR/ECVDI. Медицинскую онкологическую сертификацию Maddox не приписывать.

На месте подтверждена установка для ветеринарной лучевой терапии; существующие Radiation oncology/Radiation therapy оставить. В resources описаны лекарственные комбинации под trial protocols, поэтому общий тег доступной вне исследования химиотерапии не добавлять. Это ограничение доказательств доступа, а не отсутствие химии в учреждении.

Приём по записи; владелец может обратиться напрямую или через ветеринара. Оставить текущую availability_note.

| Поле | Официальный источник | Короткая опора |
|---|---|---|
| Контакты и master_url | [Contact](https://www.utsouthwestern.edu/departments/radiation-oncology/veterinary-research-oncology-clinic/contact-us.html) | “The Veterinary Research and Oncology Clinic is located at:” |
| Команда | [Meet the team](https://www.utsouthwestern.edu/departments/radiation-oncology/veterinary-research-oncology-clinic/meet-the-team.html) | “Jonathan Maddox, D.V.M.” |
| Квалификация | [Vanhaezebrouck profile](https://profiles.utsouthwestern.edu/profile/236540/isabelle-vanhaezebrouck.html) | “board certified in radiation oncology” |
| Местная лучевая | [Infrastructure](https://www.utsouthwestern.edu/departments/radiation-oncology/veterinary-research-oncology-clinic/clinical-infrastructure.html) | “radiation therapy unit designed specifically for veterinary use” |
| Запись | [Resources](https://www.utsouthwestern.edu/departments/radiation-oncology/veterinary-research-oncology-clinic/resources.html) | “Visits are available by appointment only.” |

Нерешённое: обычная химиотерапия вне исследования и обычный доступ к focused ultrasound отдельно не установлены. Профиль Maddox дважды оказался недоступен инструменту; официальная страница команды доступна. Не нужно заново ставить под вопрос UTSW-адрес или сертификацию Vanhaezebrouck.

## 2. Veterinary Specialists of North Texas, Fort Worth

ID: `veterinary-specialists-of-north-texas-3cbba709`.

Подтверждены **4631 Citylake Blvd. West, Fort Worth TX 76132**, **817-263-4300**, контакт внутри Fort Worth Veterinary Specialty & Emergency Hospital.

Официальная Medical Oncology прямо перечисляет oral/injectable chemotherapy, electrochemotherapy и immunotherapy. Radiation Oncology описывает собственный LINAC/Elekta Versa HD, SRT/SBRT и GRID. Все существующие теги услуг сохранить независимо от списка сертифицированных врачей.

Подтверждены Sara Allstadt (DACVIM Oncology), Stephanie Cook (DACVR Radiation Oncology), Nicholas Rancilio (DACVR Radiation Oncology), Carlos Rodriguez Jr (DACVIM Oncology). У Rodriguez официальная биография описывает работу на подмене в разных учреждениях США — сохранить caveat о необходимости уточнить расписание, не считать его гарантированно ежедневно принимающим здесь.

VSNT требует направление, запись и заполнение new-patient form. Хирургия предоставляется co-located Dallas Veterinary Surgical Center, не приписывать её самостоятельной хирургической службе VSNT.

| Поле | Официальный источник | Короткая опора |
|---|---|---|
| Контакт и master_url | [Contact](https://vsnt.com/contact/) | “4631 Citylake Blvd. West” |
| Химия/ECT/иммунотерапия | [Medical oncology](https://vsnt.com/services/medical-oncology/) | “Our medical oncology treatments include both traditional and innovative options:” |
| Местная RT/GRID | [Radiation oncology](https://vsnt.com/services/radiation-oncology/) | “GRID is available using our equipment.” |
| Направление | [FAQ](https://vsnt.com/pet-owners/faqs/) | “VSNT is a by referral only specialty hospital.” |

Квалификации сверены по [Allstadt](https://vsnt.com/specialists/sara-allstadt/), [Cook](https://vsnt.com/specialists/stephanie-cook/), [Rancilio](https://vsnt.com/specialists/nicholas-rancilio/) и [Rodriguez](https://vsnt.com/specialists/carlos-rodriguez-jr/).

Нерешённое: конкретное расписание Fort Worth у relief-provider Rodriguez. Ошибки первоначального получения контактной страницы и его профиля были временными: повторные официальные открытия завершились успешно.

## 3. Veterinary Specialty Center, Bannockburn

ID: `veterinary-specialty-center`.

Подтверждены **2051 Waukegan Road, Bannockburn IL 60015**, **847-459-7535**, местное отделение medical/radiation oncology, химиотерапия и лучевая терапия. Приём по записи понедельник–пятница; перед приёмом запрашивают записи лечащего ветеринара. Существующие факты сохранить.

Текущая команда перечисляет Blake Marcum и Richard Sheng (DACVIM Oncology), Hayley Ashworth и Carolynne Kruckman-Gatesy (DACVR-RO), Rhonda Feinmehl — residency-trained in oncology. Не превращать residency-trained в board-certified. Список пяти врачей и число четырёх подтверждённых сертифицированных специалистов не являются новым расхождением.

| Поле | Официальный источник | Короткая опора |
|---|---|---|
| Филиал, услуги, master_url | [Medical & radiation oncology](https://www.vetspecialty.com/specialties/medical-and-radiation-oncology/) | “Veterinary Medical & Radiation Oncology in Bannockburn, IL” |
| Команда | [Our team](https://www.vetspecialty.com/our-team/page/3/) | “Rhonda Feinmehl DVM, Residency-Trained in Oncology” |
| Документы | [Preparing for your visit](https://www.vetspecialty.com/pet-owners/preparing-for-your-visit/) | “your pet’s regular veterinarian will be asked to send us all records” |
| Местный аппарат | [Radiation therapy](https://www.vetspecialty.com/specialties/medical-and-radiation-oncology/radiation-therapy/) | “linear accelerator (LINAC)” |

Нерешённых вопросов по назначенным полям не осталось.

## Проверяемые файлы

- `input.json`: фактический исходный снимок трёх inventory и трёх supplemental записей.
- `proposed_changes.json`: три предложения по master_url, без изменений clinical data.
- `result.json`: времена, счётчики, проверенные поля, решения и вопросы.
- `evidence.json`: реальные ответы веб-инструмента с retrieval refs, включая неудачные попытки. Точная метка получения каждой страницы веб-инструментом не предоставляется; checked_at означает фактическую дату проверки, а не выдуманное время визита. Время публикации/доступность записи в Git не тестировались.

