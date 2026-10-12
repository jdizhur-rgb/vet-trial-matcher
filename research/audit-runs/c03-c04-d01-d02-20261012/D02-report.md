# D02 — аудит удалённых онкологических консультаций

Проверка: **12 октября 2026, America/New_York**. Проверены все 25 назначенных идентификаторов. Это исследовательский пакет: общая база, source dates, main и production не изменялись. Trials и контакты с провайдерами не использовались.

## Исходные данные и метод

Прочитаны актуальные AGENTS.md и PROJECT_OPERATIONS.md целиком. Канонический remote directory — `seo/oncology_teleconsultations.py`, переменная ROWS; inventory — `data/oncology_care_source_inventory.json`. Все 25 source IDs найдены и сопоставлены по точному URL услуги. Исходные значения доступны для каждого изменяемого существующего поля и сохранены в JSON. GitHub blob SHA снимков: teleconsultations `23e8efbe2159fbd2793661884a16fc39e19b0b64`; inventory `335a91cfef29ca890c49a931fda8668dec7a522b`; operations `ba3240a876e02c5347aadd29de228d31225bf717`. Названия полей JSON — документированные aliases позиционных полей tuple; field_map задаёт индексы. Новые отдельные price/contact/availability поля в общий каталог не изобретались.

Официальные service pages сопоставлялись с roster/biographies, тарифами, формами, contact routes и дополнительными native-language страницами. Источник вторичного типа только для собственного заявления Škor в интервью Novinky; факт видеоконсультаций извлечён из прямого высказывания, квалификация — из RegiaVet. Публичный JS ANI.ML прочитан статически без исполнения, доступа к account, private APIs или отправки данных. Данные RVC доступны только в официальной поисковой копии, с явным ограничением свежести.

Статус «действующий» здесь означает наличие опубликованной услуги и способа обращения; свободные слоты и ответы провайдера не проверялись. Diploma/qualification — опубликованная квалификация, не независимая проверка актуального лицензионного статуса. Международная доступность признаётся только при явном service statement.

## Принятые решения

- Подготовлено **33 полевых изменений в 17 сервисах**; 8 записей остаются без изменений.
- Onkolia: owner-with-vet pathway, named reviewer/точная квалификация, письменный формат и публичные цены.
- CottOncology: Google Meets, CZK 3,000, документы и условия; Veterinary Oncology Consultants: AUD тарифы и current profiled team; Online Oncologist: literal Hong Kong тариф.
- Oncovet: сохранить совместный owner+vet video и добавить vet-only chat pathway.
- Upstate/Davies: добавить текущий опубликованный oncology roster, без гарантии назначенного remote consultant.
- West Texas: убрать неподтверждённое конкретное Eastern New Mexico coverage; teleconsult возможен вне mobile travel area, но страны/штаты не перечислены.
- OncoCats: имя practice lead и oncology/feline training; убрать необоснованное feline-only описание; не приписывать board certification.
- Никакой сервис не объявлен закрытым; физические услуги, мобильные визиты и дистанционное введение химиотерапии не добавлялись.

## Карточки проверки

### tele-26 — Royal Veterinary College

**Решение:** Сохранить без изменений. Уверенность: medium.

Официальная сохранённая страница прямо предлагает владельцам консультацию до поездки/решения о лечении. Andy Yale указан в сохранённом составе команды как DipECVIM-CA (Oncology); назначение на конкретную удалённую консультацию не установлено. Сохранить существующую запись без усиления обещаний.

**География и ограничения:** Практика UK; международный приём не установлен.

**Обращение и контакты:** Сохранённая страница команды: +44 (0)1707 666333, AYALE7@rvc.ac.uk — контакт врача, не отдельная служба записи.

**Стоимость:** Удалённый тариф не установлен.

**Нерешённое / следующий проход:** Прямые страницы услуги и Andy Yale возвращают 403; официальные поисковые копии возрастом 4–5 месяцев. Текущий состав команды и доступность расписания не подтверждены свежим чтением. Это ограничение свежести, не доказательство закрытия.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://www.rvc.ac.uk/small-animal-vet/specialist-referrals/clinical-services/veterinary-oncology — primary official; website/biography/service/tariff
- https://www.rvc.ac.uk/small-animal-vet/specialist-referrals/clinical-services/veterinary-oncology/team — primary official; website/biography/service/tariff
- https://www.rvc.ac.uk/about/our-people/andy-yale — primary official; website/biography/service/tariff

### tele-27 — Davies Veterinary Specialists

**Решение:** Изменить: clinician_label, credentials_context, clinician_url. Уверенность: high.

Действующий oncology service прямо предлагает virtual initial discussions. Команда: Mark Goodfellow (DipECVIM-CA, RCVS oncology specialist), Sarah Benjamin (DipACVIM Oncology), Petros Odatzoglou и Luca Schiavo (DipECVIM-CA Oncology). Кто проводит удалённый разговор, не назначен заранее. Доступ владельца через referral pathway сохранён.

**География и ограничения:** UK; перечень допустимых стран/лицензий для remote service отсутствует.

**Обращение и контакты:** 01582 883950; официальный Refer Now на service page.

**Стоимость:** Не опубликован отдельный виртуальный тариф.

**Нерешённое / следующий проход:** Не переносить общие 60 минут очного приёма на виртуальный. Видео/телефон, дистанционный тариф и границы доступа не уточнены.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://www.vetspecialists.co.uk/services/oncology/ — primary official; website/biography/service/tariff

### tele-28 — Beatrice–Villa clinic

**Решение:** Изменить: consultation_details. Уверенность: high.

Laura Beatrice: ACVIM SAIM / internal medicine, не Oncology diplomate. Прямые owner video second opinions и отдельные профессиональные письменные/телефонные разборы. Отправляются результаты, изображения и видео, затем согласуется время.

**География и ограничения:** Italy; сайт прямо приглашает international owners/foreign clinics, но список разрешённых стран/право prescribing не опубликованы. Языки: Italian, English, German.

**Обращение и контакты:** +39 0522 541919; ambulatorio.beatvill@gmail.com; service request form.

**Стоимость:** Не опубликована.

**Нерешённое / следующий проход:** Не представлять SAIM как oncology board certification; конкретную страну и режим медицинской ответственности согласует сервис.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://www.ambvetbeatricevilla.eu/en/telemedicina — primary official; website/biography/service/tariff
- https://www.ambvetbeatricevilla.eu/en/copia-di-chi-siamo — primary official; website/biography/service/tariff

### tele-29 — CottOncology

**Решение:** Изменить: consultation_details. Уверенность: high.

Dagmar Kotlíková MVDr., oncology/internal medicine practice. Owner Google Meets review; 10–15 минут подготовки входят в консультацию. Анкета и до трёх файлов. Самостоятельная ECVIM/ACVIM oncology certification не заявлена. Сотрудничество со Škor датировано 2023–8/2025, не текущая гарантия supervision.

**География и ограничения:** Czechia; международное обслуживание и языки отдельно не установлены.

**Обращение и контакты:** oncology@dagmarkotlikova.cz; consultation form/calendar.

**Стоимость:** 3 000 Kč; оплатить минимум за 24 часа; отмена позднее 24 часов без возврата.

**Нерешённое / следующий проход:** Контактная страница просит сейчас записываться по email; уточнение календаря остаётся у сервиса, не подавать форму. Продолжительность всей встречи не опубликована.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://www.dagmarkotlikova.cz/ — primary official; website/biography/service/tariff
- https://www.dagmarkotlikova.cz/konzultace/ — primary official; website/biography/service/tariff
- https://www.dagmarkotlikova.cz/kontakt/ — primary official; website/biography/service/tariff

### tele-30 — Ondřej Škor / RegiaVet

**Решение:** Сохранить без изменений. Уверенность: high.

Ondřej Škor: официальный RegiaVet profile подтверждает DECVIM-CA Oncology/CertVO и руководство медицинской службой с 7/2026. Его собственное высказывание в интервью подтверждает owner video consultations. Сохранить запись; это атрибутированное высказывание врача в СМИ, а не официальная страница бронирования.

**География и ограничения:** Czechia; перечень допустимых стран/языков не установлен.

**Обращение и контакты:** info@regiavet.cz; +420 724 804 804 / +420 271 750 991.

**Стоимость:** Публичный teleconsult тариф не найден. Цена из личной переписки не использована.

**Нерешённое / следующий проход:** Расписание, форма записи, документы, тариф и cross-border limits не опубликованы в прочитанных источниках. Нет оснований удалять услугу только из-за отсутствия booking page.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://www.novinky.cz/clanek/lifestyle-osobnosti-veterinarni-onkolog-ondrej-skor-u-zvirat-chemoterapie-prodluzuje-zivot-bez-bolesti-a-potizi-40549659/ — secondary; интервью с прямым заявлением врача
- https://www.regiavet.cz/mvdr-ondrej-skor-decvim-ca-certvo — primary official; website/biography/service/tariff
- https://www.regiavet.cz/kontakt — primary official; website/biography/service/tariff

### tele-31 — Krebs beim Hund

**Решение:** Изменить: consultation_details. Уверенность: high.

Dr Diana Schulenburg: Fachtierärztin Innere Medizin + GP Certificate Oncology; не ECVIM Oncology. Действующий veterinary oncology second opinion через Teams или телефон, Deutsch/English. Документы необходимо прислать заранее. Отдельные услуги Tierheilpraktiker не приписаны ветеринарному врачу.

**География и ограничения:** Germany; нет установленного списка других стран.

**Обращение и контакты:** krebsbeimhund@gmx.de; booking link; бесплатная регистрация на платформе нужна для использования услуг.

**Стоимость:** €119; основной экран 45 минут, описание 30–60 минут, альтернативная карточка 40 минут.

**Нерешённое / следующий проход:** Противоречие длительности сохраняется; не выбирать одну цифру как окончательную. Ограничения по странам не опубликованы.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://www.krebsbeimhund.com/service-page/tier%C3%A4rztliche-beratung-krebs — primary official; website/biography/service/tariff
- https://www.krebsbeimhund.com/service-page/tiermedizinische-onkologische-beratung — primary official; website/biography/service/tariff
- https://www.krebsbeimhund.com/experten-krebs-beim-hund — primary official; website/biography/service/tariff
- https://www.krebsbeimhund.com/ — primary official; website/biography/service/tariff

### tele-32 — Oncovet Online

**Решение:** Изменить: access, consultation_details. Уверенность: high.

Онкологический, не общий telemedicine portal. Laura Arconada/Inés Álvarez в официальном roster, без подтверждения board oncology. Два пути: joint owner+vet video appointment через зарегистрированного ветеринара и отдельный vet-only chat advice (разовый/подписка).

**География и ограничения:** Spain; международный приём не установлен.

**Обращение и контакты:** online@oncovet.es; +34 695 32 56 31; бесплатная регистрация ветеринара.

**Стоимость:** Публичная сумма не обнаружена на открытой странице. Регистрация free не означает free consultation.

**Нерешённое / следующий проход:** Нет публичных точных board credentials/назначения врача на конкретный случай; тарифы и страны могут быть доступны только после входа.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://www.online.oncovet.es/es — primary official; website/biography/service/tariff
- https://www.oncovet.es/quienes-somos — primary official; website/biography/service/tariff

### tele-33 — SOIVET

**Решение:** Сохранить без изменений. Уверенность: medium.

Официальная страница подтверждает owner video second opinion и professional teleoncology/cytology support. SOIVET также выездная очная практика, но это отдельный раздел услуг. Консультант teleoncology и сертификаты на прочитанной service page не названы. Сохранить нынешние access/specialty с неопределёнными credentials.

**География и ограничения:** Spain; удалённые страны/региональное покрытие не опубликованы.

**Обращение и контакты:** Официальный сайт и service page работают; отдельный contact route выдаёт interstitial, извлекаемый проверенный телефон/email не установлен.

**Стоимость:** Не опубликована.

**Нерешённое / следующий проход:** Home/contact/team пути нестабильны (502/interstitial); имя консультанта, квалификация и прямые контакты не подтверждены. Это пробел данных, не закрытие.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://www.soivet.es/servicios/ — primary official; website/biography/service/tariff
- https://www.soivet.es/ — primary official; website/biography/service/tariff
- https://www.soivet.es/contactar/ — primary official; website/biography/service/tariff

### tele-34 — The Cancer Vet

**Решение:** Изменить: consultation_details. Уверенность: high.

Teleconsults для owners прямо заявлены across India throughout the week; форма разрешает прикрепить файл. Founder Noopur Desai: BVSc, MVSc Surgery, DACVR Radiation Oncology. Advisors Vail/Turek/Selmic не автоматически проводят remote appointments.

**География и ограничения:** Подтверждена India; другие страны не подтверждены.

**Обращение и контакты:** Официальная teleconsult request form; Mumbai +91 87999 49294 / mumbai@thecancer.vet, Pune +91 87999 49295 / pune@thecancer.vet на contact page (поисковая копия 5 месяцев). Это филиальные контакты, не отдельная международная hotline.

**Стоимость:** Не опубликована.

**Нерешённое / следующий проход:** Конкретный doctor, видео/телефон, длительность и cross-border service не названы. Medical/radiation oncology — scope практики, не гарантия двух сертификатов назначенного консультанта.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://thecancer.vet/tele-consults/ — primary official; website/biography/service/tariff
- https://thecancer.vet/team/ — primary official; website/biography/service/tariff
- https://thecancer.vet/contact-us/ — primary official; website/biography/service/tariff

### tele-41 — Harvest Veterinary Oncology Centre

**Решение:** Сохранить без изменений. Уверенность: high.

Действующий cancer centre. Telemedicine section предлагает владельцу digital meeting с overseas expert. Личность и board qualification именно overseas remote expert не названы; нынешние местные специалисты не автоматически remote consultant. Сохранить запись с неизвестным назначением.

**География и ограничения:** Организатор Hong Kong; overseas expert означает местонахождение врача, не глобальную доступность пациентам.

**Обращение и контакты:** 24-hour hospital hotline 3102 8528; oncology WhatsApp и referral form доступны на странице.

**Стоимость:** Не опубликована.

**Нерешённое / следующий проход:** Видео vs иной digital channel, имя зарубежного консультанта, fee и eligibility не установлены. Заявление сайта о diagnosis/prescription не расширено до международного prescribing.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://hvoc.com.hk/en/oncology-services/ — primary official; website/biography/service/tariff

### tele-42 — MARS / Melbourne Animal Referral Services

**Решение:** Изменить: consultation_details. Уверенность: high.

Owner и referring vet secure video conferencing + индивидуальный письменный план обоим. В истории current team есть Paul Crocker как Lead Oncology Veterinarian (в изображении/alt); собственная Oncology board qualification и personal telehealth assignment не подтверждены. Thursday/Friday опубликованы.

**География и ограничения:** Australia; фраза no matter where you are не устанавливает все страны. Не переносить географию mobile surgery на telehealth.

**Обращение и контакты:** enquiries@marsvets.com.au; 03 9050 0671. Медицинская история и результаты email перед записью.

**Стоимость:** Официальный PDF 2025–26, oncology page 9: A$300, hospital prices incl. GST; текущую цену при записи подтвердить.

**Нерешённое / следующий проход:** PDF содержит прежний физический адрес; использовать только tariff scope, не адрес лечения. Cross-border eligibility и exact oncologist credential неизвестны.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://marsvets.com.au/services/vet-cancer-care-telehealth/ — primary official; website/biography/service/tariff
- https://marsvets.com.au/about-us/meet-the-team/ — primary official; website/biography/service/tariff
- https://marsvets.com.au/wp-content/uploads/2025/09/MARS-2025-26-Price-List.pdf — primary official; website/biography/service/tariff

### tele-43 — Animal Cancer Centre WA

**Решение:** Изменить: consultation_details. Уверенность: high.

Jessica Finlay BVSc MVS FANZCVS, Registered Specialist Veterinary Oncology. Referral-only specialist practice: Zoom most cases, initial consultations 45 минут; по согласию запись доступна в patient portal. Запись можно запросить до получения referral papers.

**География и ограничения:** Australia/Western Australia — опубликован региональный pathway; международный доступ не установлен.

**Обращение и контакты:** (08) 6556 9901; letstalk@animalcancercentrewa.com.au; bookings.

**Стоимость:** Не опубликована.

**Нерешённое / следующий проход:** Не гарантировать, что Finlay лично ведёт каждый Zoom; имя team lead не заменяет booking assignment. География Zoom/тариф не перечислены.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://animalcancercentrewa.com.au/the-journey/ — primary official; website/biography/service/tariff
- https://animalcancercentrewa.com.au/the-family/ — primary official; website/biography/service/tariff

### tele-44 — Upstate Veterinary Specialties

**Решение:** Изменить: clinician_label, credentials_context, clinician_url, consultation_details. Уверенность: high.

Vet-to-vet consults с любым специалистом прямо предлагаются на referral page. Current oncology service names Ashleigh Cappello (Cournoyer), DVM DACVIM Oncology (2023), Ariana Verrilli DVM DACVIM Oncology (2021). Team member ≠ заранее назначенный remote clinician.

**География и ограничения:** US/New York practice; teleconsult accepted states/countries not listed.

**Обращение и контакты:** 518-783-3198: request oncology department.

**Стоимость:** Не опубликована.

**Нерешённое / следующий проход:** Live/written format, fee, required document set for teleconsult не перечислены; 12 months records относится к очному specialty referral, не автоматически teleconsult.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://www.uvsonline.com/referring-veterinarians/ — primary official; website/biography/service/tariff
- https://www.uvsonline.com/specialty/oncology/ — primary official; website/biography/service/tariff
- https://www.uvsonline.com/doctors/ashleigh-cappello-cournoyer/ — primary official; website/biography/service/tariff
- https://www.uvsonline.com/doctors/ariana-verrilli/ — primary official; website/biography/service/tariff

### tele-45 — DVM STAT

**Решение:** Изменить: consultation_details. Уверенность: high.

Действующий vet-only oncology case review. Michelle Silver DVM DACVIM Oncology / Ester Yang VMD MS DACVIM Oncology. Written tailored report: staging/diagnosis/treatment options; follow-up specialist support. Инъекционные препараты рекомендуются local practice, не вводятся онлайн провайдером.

**География и ограничения:** US practice; всемирная/всештатная доступность публично не установлена.

**Обращение и контакты:** 833-386-7828; info@dvmstat.com; clinic registration/platform.

**Стоимость:** Не установлена публичная сумма.

**Нерешённое / следующий проход:** Не переносить общие 24/7 или STAT line гарантии на немедленный oncology ответ. Конкретный assigned oncologist и доступные юрисдикции не перечислены.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://www.dvmstat.com/oncology — primary official; website/biography/service/tariff
- https://www.dvmstat.com/specialists — primary official; website/biography/service/tariff

### tele-46 — University of Florida Small Animal Hospital

**Решение:** Изменить: consultation_details. Уверенность: high.

Форма прямо предлагает vet-to-vet consultation via phone/email. Paulo Vilar Saavedra — chief, DVM MSc PhD DACVIM Oncology; responding doctor not guaranteed.

**География и ограничения:** US/Florida; географические границы remote support не перечислены.

**Обращение и контакты:** (352) 392-2235; official referral/consult form; chief biography pvilarsaavedra@ufl.edu.

**Стоимость:** Не опубликована.

**Нерешённое / следующий проход:** Нужно ZIP all relevant records (max 125 MB); ultrasound/CT DICOM отправлять reply к confirmation email. Owner participation отдельно не подтверждено.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://smallanimal.vethospital.ufl.edu/contact-us/referring-veterinarians/for-referring-veterinarians-medical-oncology-referral-form/ — primary official; website/biography/service/tariff
- https://www.vetmed.ufl.edu/profile/vilar-saavedra-paulo/ — primary official; website/biography/service/tariff

### tele-47 — Veterinary Oncology Partners

**Решение:** Сохранить без изменений. Уверенность: high.

Vet-only written case reports; direct owner consultation expressly not offered. M.J. Hamilton DVM DACVIM Oncology; founders Rizzo/Clark SAIM, не oncology boards. Consulting all US states, chemotherapy fulfilment subset states. Никакого дистанционного введения препаратов. Сохранить существующую запись.

**География и ограничения:** Все US states — прямо опубликовано для consulting; не переносить на shipping/other countries.

**Обращение и контакты:** Online Submit a Consult; owner form только передаёт контакт своего veterinarian.

**Стоимость:** Fee on request; публичная сумма на прочитанных страницах не найдена.

**Нерешённое / следующий проход:** Нынешний subset states для fulfilment не является scope этой audit задачи и не добавлен в remote availability.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://www.veterinaryoncologypartners.com/pet-owners.html — primary official; website/biography/service/tariff
- https://www.veterinaryoncologypartners.com/our-story.html — primary official; website/biography/service/tariff

### tele-48 — West Texas Veterinary Specialists

**Решение:** Изменить: consultation_details. Уверенность: high.

Vet-only oncology written review; Avenelle Turner DVM DACVIM Oncology официально listed collaborator. История, examination findings, diagnostics/images; рекомендации local vet. Mobile medicine/surgery отделены от oncology teleconsult.

**География и ограничения:** Опубликована West Texas practice; about page прямо допускает teleconsults вне travel area. Eastern New Mexico как гарантированный teleconsult регион не подтверждён.

**Обращение и контакты:** info@txvetspecialty.com; Consultation Request official portal.

**Стоимость:** Не опубликована.

**Нерешённое / следующий проход:** Доступ за пределами travel area подтверждён в принципе, но конкретные states/countries не перечислены; не заменять это всемирной доступностью.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://txvetspecialty.com/services/oncology/ — primary official; website/biography/service/tariff
- https://txvetspecialty.com/dr-turner/ — primary official; website/biography/service/tariff
- https://txvetspecialty.com/about-our-practice/ — primary official; website/biography/service/tariff
- https://txvetspecialty.com/contact/ — primary official; website/biography/service/tariff

### tele-49 — Balto / ANI.ML Health

**Решение:** Сохранить без изменений. Уверенность: high.

HTML reader видит JS shell. Статическое чтение реально опубликованного /assets/index-D63pDWWF.js, без исполнения/входа/API, подтверждает vet-to-vet written opinion within 24 hours и Oncology в service menu. Pinard DVM DVSc DACVIM Oncology/cofounder подтверждён Guelph; headshot asset сам по себе не доказательство assigned reviewer. Существующие cautious clinician/assignment fields сохранить.

**География и ограничения:** Canada в официальных meta; UI country options CA/US не доказательство доступности во всех states или cross-border лицензий.

**Обращение и контакты:** we.care@animl.health — публичная support ссылка в модуле; case platform.

**Стоимость:** Публичный фиксированный oncology tariff не установлен.

**Нерешённое / следующий проход:** Live roster/оплата требуют account. Не извлекать из приложения административные/пользовательские данные, не подавать case. 24h — рекламируемый срок, не независимая гарантия.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://consult.animl.health/ — primary official; website/biography/service/tariff
- https://consult.animl.health/assets/index-D63pDWWF.js — primary official; static public client module
- https://www.uoguelph.ca/ovc/clinical-studies/faculty/christopher-pinard — primary official; website/biography/service/tariff

### tele-50 — Veterinary Oncology Consultants

**Решение:** Изменить: clinician_label, consultation_details. Уверенность: high.

Current consulting team page подробно представляет Penny Thomas и Amy Lane, FANZCVS Veterinary Oncology. Moore/Frimberger указаны как основатели, без доказательства нынешнего назначения на случаи. Written report, optional phone to veterinarian only, not owner.

**География и ограничения:** Worldwide прямо опубликовано, any species/any cancer; Australia, NZ, Singapore, Hong Kong, Malaysia, USA, Canada, UAE, Vanuatu приведены как примеры.

**Обращение и контакты:** +61 0459 952 124; request form. Новые clinic clients сначала связываются с сервисом. Мedical/test reports прикрепляются/отправляются email.

**Стоимость:** AUD 300 written/email; AUD 350 report+phone; AUD 35 follow-up contact; protocol AUD 50. Australia fees include 10% GST.

**Нерешённое / следующий проход:** Не считать исторических основателей текущими assigned consultants. Рабочее время 8–15 NSW Mon–Fri; response до конца следующего consulting day — не круглосуточно.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://www.vetoncologyconsults.com/oncology-consulting/ — primary official; website/biography/service/tariff
- https://www.vetoncologyconsults.com/about/ — primary official; website/biography/service/tariff

### tele-51 — Online Oncologist

**Решение:** Изменить: consultation_details. Уверенность: high.

Sonya Yu BVSc MANZCVS FANZCVS Veterinary Oncology, registered specialist. Veterinary primary care consulting; Hong Kong single case и подписки, Teams messaging support—not automatically video visit.

**География и ограничения:** Practice Australia; конкретно Hong Kong опубликован service tariff. Main site ведёт также на Australia; не заявлять весь мир.

**Обращение и контакты:** sonya@onlineoncologist.vet; HK-specific joseph@onlineoncologist.vet, WhatsApp +852 5741 9350.

**Стоимость:** HKD 1,800 single case; standard 7,000/3 cases monthly; premium 10,000/5. Single-case add-ons: protocol 250, handout 150, drug sheet 150, follow-up 500.

**Нерешённое / следующий проход:** Teams scope Mon–Fri 9–17 AEST stated by provider; не обещать видеоприём, скорость ответа сверх terms или перевод timestamps на своё расписание.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://www.onlineoncologist.vet/hong-kong — primary official; website/biography/service/tariff
- https://www.onlineoncologist.vet/about — primary official; website/biography/service/tariff
- https://www.onlineoncologist.vet/ — primary official; website/biography/service/tariff

### tele-52 — Onco Cats

**Решение:** Изменить: clinician_label, credentials_context, consultation_details, clinician_url. Уверенность: high.

OncoCats основан/ведётся Gabriela Clezar, ветеринар с oncology/feline postgraduate specializations (без подтверждённого ACVIM/ECVIM board). Онлайн teleinterconsulta для ветеринаров. Local oncology treats dogs and cats, поэтому не ограничивать remote description только кошками без основания.

**География и ограничения:** Practice South Santa Catarina/North coast Rio Grande do Sul; online отдельно, международная география не названа.

**Обращение и контакты:** WhatsApp +55 (48) 99800-4811; Mon–Fri 9–18.

**Стоимость:** Не опубликована.

**Нерешённое / следующий проход:** Не гарантировано личное назначение Gabriela; exact remote format и country limits не опубликованы. Local chemo/surgery/ECT не добавлены как выполняемые remotely.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://www.oncocats.com/ — primary official; website/biography/service/tariff
- https://www.oncocats.com/conhe%C3%A7a-mais — primary official; website/biography/service/tariff

### tele-53 — Vetonc

**Решение:** Изменить: consultation_details. Уверенность: high.

Franziska Hergt DipECVIM-CA Oncology, EBVS European specialist прямо опубликованы. Vet-only email/phone oncology case review and staging/prognosis. Не owner consultation.

**География и ограничения:** Germany; перечень стран не опубликован.

**Обращение и контакты:** info@vetonc.de; official contact form.

**Стоимость:** Не опубликована.

**Нерешённое / следующий проход:** Отдельное board-registry подтверждение current registration не получено; на сайте credential stated, employment timeline может быть старым. Не трактовать дату ©2019 как закрытие.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://vetonc.de/ — primary official; website/biography/service/tariff

### tele-54 — Onkolia

**Решение:** Изменить: access, clinician_label, credentials_context, specialty, consultation_details, clinician_url, assignment. Уверенность: high.

Paul GHISLAIN назван автором всех avis; CEAV Internal Medicine и école cancer/chemotherapy capacity, не ECVIM/ACVIM Oncology board. Владельцы по направлению своего врача могут создать account/submit documents; заключение адресуется treating vet. Это не owner video consult, remote diagnosis или prescription.

**География и ограничения:** France; international eligibility not enumerated.

**Обращение и контакты:** contact@onkolia.fr; account/clinical dossier portal.

**Стоимость:** €129 incl VAT single avis (до 5 рабочих дней + один Q&A); €389 three-month / €649 annual packages.

**Нерешённое / следующий проход:** Страницы по-разному формулируют медицинскую степень учреждения, поэтому точные опубликованные credential названия без дополнительного university attribution. Не воспроизводить правовые выводы из маркетинговой статьи как независимо проверенное право.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://www.onkolia.fr/articles/avis-cancerologique-veterinaire-distance-confrere — primary official; website/biography/service/tariff
- https://www.onkolia.fr/ — primary official; website/biography/service/tariff
- https://www.onkolia.fr/a-propos — primary official; website/biography/service/tariff
- https://www.onkolia.fr/tarifs — primary official; website/biography/service/tariff

### tele-55 — ARC Vets

**Решение:** Сохранить без изменений. Уверенность: high.

Patrick Smith BSc BVMS MRCVS DECVIM Oncology, Registered Specialist. Initial remote consultation through referring veterinarian explicitly offered; after-discharge remote follow-up conditional. Эти два пути и нынешнее access уже верны.

**География и ограничения:** New Zealand national referrals published; международный remote доступ не подтверждён.

**Обращение и контакты:** Official Talk to our team/contact Central/North links; initial teleconsult via referring vet.

**Стоимость:** Не опубликована.

**Нерешённое / следующий проход:** Конкретный remote format, fee и exact document set не перечислены; не переносить local ECT/chemo/partner radiation в услуги remote administration.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://arcvets.co.nz/services/oncology-cancer-care/ — primary official; website/biography/service/tariff

### tele-56 — HEAL Cancer Care for Pets

**Решение:** Сохранить без изменений. Уверенность: high.

Nick Szigetvari DVM DACVIM Oncology в действующем team HTML; teleconsultation New Patient Form прямо на approach/cancer-care/team pages. Мedical records coordination with primary veterinarian. Существующий осторожный текст правильный.

**География и ограничения:** Practice Seattle/WA; geographic eligible states/countries not published.

**Обращение и контакты:** 206-888-4325; info@healpetcancer.com; New Patient Form.

**Стоимость:** Не опубликована.

**Нерешённое / следующий проход:** Каналы video/phone/written, длительность, referral requirements и eligibility не определены публично. Не превращать физический Seattle address в teleconsult service limit.

**Проверенные поля:** наличие oncology remote service; сайт/обращение; current published clinician/qualification; аудитория; формат; география; направление/документы; цена. Отсутствующие сведения прямо отмечены выше, не считаются подтверждёнными.

**Источники (проверены 2026-10-12):**
- https://healpetcancer.com/our-approach/ — primary official; website/biography/service/tariff
- https://healpetcancer.com/cancer-care/ — primary official; website/biography/service/tariff
- https://healpetcancer.com/meet-the-veterinary-team/ — primary official; website/biography/service/tariff
- https://healpetcancer.com/veterinary-colleagues/ — primary official; website/biography/service/tariff

## Таблица изменений

| ID | Поле | Решение |
|---|---|---|
| tele-27 | clinician_label | Заменить неопределённую команду текущим опубликованным составом; назначение на teleconsult остаётся неизвестным. |
| tele-27 | credentials_context | Точная квалификация отделена от назначения. |
| tele-27 | clinician_url | Добавить существующий официальный roster URL. |
| tele-28 | consultation_details | Добавить реальный профессиональный формат и процедуру, сохранив ограничения географии. |
| tele-29 | consultation_details | Опубликованные формат, цена и условия оплаты; email подтверждён отдельной контактной страницей. |
| tele-31 | consultation_details | Сохранить подтверждённую цену/языки и явно зафиксировать все несовместимые длительности. |
| tele-32 | access | Добавить отдельный vet-only путь, не открывая прямую самостоятельную owner booking. |
| tele-32 | consultation_details | Добавить реально опубликованный второй формат; не обещать бесплатное лечение. |
| tele-34 | consultation_details | Добавить явно установленную географию и не обещать международный доступ. |
| tele-42 | consultation_details | Уточнить документы/контакт, scope совместного приёма и отсутствие доказанной глобальной доступности; цену подтверждает отдельный PDF. |
| tele-43 | consultation_details | Уточнить обязательную модель направления, опубликованную длительность и роль записи. |
| tele-44 | clinician_label | Заменить неназванную команду текущим официальным oncology roster. |
| tele-44 | credentials_context | Квалификация Cournoyer подтверждена биографией; Verrilli отдельной linked biography в report. |
| tele-44 | clinician_url | Добавить официальный roster URL. |
| tele-44 | consultation_details | Добавить точный путь обращения, не приписывать очные referral требования remote услуге. |
| tele-45 | consultation_details | Письменный формат теперь явно подтверждён; не оставлять его как полностью неизвестный. |
| tele-46 | consultation_details | Добавить точные опубликованные требования документов вместо общей рекомендации. |
| tele-48 | consultation_details | Удалить неподтверждённый конкретный Eastern New Mexico promise; не ограничивать teleconsult мобильным радиусом. |
| tele-50 | clinician_label | Убрать впечатление, что все четыре имени одинаково подтверждены как текущие консультанты; не утверждать уход основателей. |
| tele-50 | consultation_details | Добавить опубликованные цены/валюту/налог/формат вместо неподтверждённой цены. |
| tele-51 | consultation_details | Добавить literal HK-specific тариф и отделить messaging от видео. |
| tele-52 | clinician_label | Указать подтверждённого руководителя, сохранив неизвестное назначение. |
| tele-52 | credentials_context | Не приписывать board qualification из местного слова especialização. |
| tele-52 | consultation_details | Убрать неподтверждённое feline-only ограничение онкологического case review. |
| tele-52 | clinician_url | Добавить official biography URL. |
| tele-53 | consultation_details | Добавить подтверждённые formats/contact. |
| tele-54 | access | Owner dossier submission подтвержден; сохранили обязательную связь с treating vet. |
| tele-54 | clinician_label | Reviewer named explicitly, not unnamed oncology team. |
| tele-54 | credentials_context | Указать literal qualifications, отделить их от oncology boards. |
| tele-54 | specialty | Убрать впечатление verified oncology diplomate. |
| tele-54 | consultation_details | Добавить published tariffs; owner pathway documented on home, PDF/no diagnosis/no prescription on linked service article. |
| tele-54 | clinician_url | Добавить named reviewer biography. |
| tele-54 | assignment | Заменить неназванное assignment подтверждённым автором. |

Каждый new_value, точный old_value, supporting_quote, evidence_url, дата и service scope находятся в D02-proposed_changes.json. При составном изменении дополнительные официальные sources перечислены в карточке; единственный evidence_url обозначает главный источник, а не единственный источник всего нового текста.

## Конкретные препятствия и ограничения

- RVC: 403 на direct service/team routes; доступен официальный cached текст 4–5 месяцев. Сохранить осторожную существующую запись; свежая roster/booking availability требует доступного официального чтения при следующем проходе.
- SOIVET: service body доступен, но home/contact/team routes дают нестабильный 502/interstitial; текущий remote consultant и проверенные прямые contacts не установлены. Не обходить защитную страницу.
- ANI.ML: public module подтверждает oncology menu и vet-to-vet written service; персональное назначение, live roster, price и licence coverage не устанавливаются headshot assets или country selector. Не входить/не подавать case.
- Krebs beim Hund: противоречие 40/45/30–60 минут не устранено официальными карточками. Все варианты сохранены как конфликт.
- Для остальных конкретные нераскрытые booking/fee/format/geographic/assignment поля перечислены в карточках. Непубликация информации не является доказательством отсутствия услуги.

## Даты и проверка файлов

Source attempt coverage: 25/25, полевая reconciliation: 25/25 с перечисленными ограничениями доказательств. Remote source-date updates: **0/25 — intentionally not written** по запрету менять общие файлы. Это не weekly global audit и не подтверждение полноты 487 источников.

Проверено: JSON parse; все 25 ожидаемых IDs ровно по одному в reviews; каждое изменение только назначенного source ID; уникальность (source_id, field); точное совпадение old_value со снимком ROWS; required keys/URL/quote/date/scope; отсутствие raw Google browser keys. Build/matcher/deploy tests не запускались: production files не изменены. Перед интеграцией нужен fresh baseline conflict check и обычные repo validation/build gates.
