# Worker3 — остальные сети: ограниченный повторный тест

База: `7c9b55485b3f0d1cb225c9d1143126c0318ef765`. Фактический агент `/root/other_networks`. Начало первого замера02:42:42 UTC; завершение 2026-10-13T02:51:12.930382+00:00. Первые чтения инструкций и baseline произошли до первого замера. Назначено5, обработано5, полностью подтверждено по всем существенным полям1. Полнота строго отделена от обработки.

База, сайт, UI и репозиторий не изменялись; публикация не выполнялась. Это пять конкретных филиалов, не аудит сетей. Проверка Matthews не проводилась: его одноимённая строка случайно присутствует в поисковом baseline, но другой source_id исключён из назначения.

| Назначенная запись | Итог | Что осталось |
|---|---|---|
| gulf-coast-veterinary-specialists — Houston | 8042 Katy Freeway | Обработано, частично подтверждено | What days or hours does Dustin Lewis support initial Houston radiation planning/alignment? No current schedule published. Nicola Wilson is not represented as boarded; independent certification remains unestablished. |
| colorado-animal-specialty-emergency-case — Boulder | 2972 Iris Ave | Обработано, частично подтверждено | Is primary-vet referral mandatory for every first oncology appointment despite direct online scheduling?; Surgical service narrative names Prpich while current biography names Hildebrandt; confirm assigned surgeon at booking, do not infer departure.; Sponsor ECI contact303-678-8844 differs from verified branch303-545-2273; specific ECI booking availability needs confirmation. |
| medvet-new-orleans — Metairie | 2315 N. Causeway Boulevard | Обработано, частично подтверждено | Which systemic chemotherapy/ECT/immunotherapy treatments are actually delivered at Metairie today? Network menu does not establish branch delivery.; Is current ECI scheduling active at the exact MedVet New Orleans branch, and which canine patients are accepted? Sponsor provider listing alone cannot answer bookings.; Is primary-vet referral mandatory for a first oncology appointment?; What is Sarah Lyles schedule between New Orleans and Mandeville? |
| mash — Los Angeles | 6611 Santa Monica Blvd. | Обработано, частично подтверждено | Is primary-vet referral mandatory for new-owner oncology appointments, or may owners book directly? Official route describes veterinarian referral without mandate.; Does Colleen Tansey have an accessible dedicated current biography? Oncology service and current team establish board certification; service link points to general team. |
| carolina-veterinary-specialists — Greensboro | 501 Nicholas Rd. | Полностью подтверждено | Нет существенных вопросов по назначенным полям |

## Решения

- Подтверждены уже исправленные адреса, телефоны, текущие команды и осторожные локальные услуги. У MASH онкология находится на6611 Santa Monica Blvd., несмотря на адрес6565 в общем header. Greensboro не получает услуги Matthews.
- GCVS: типичное направление не является абсолютным запретом самостоятельного запроса записи. Добавлена доказательная формулировка для intake; Lewis остаётся дистанционным планирующим специалистом, Rowlands — местным hospitalist, Wilson — DVM без недоказанного board label.
- CASE: доступны отдельные online appointments для Oncology; исправляется старая основная verification-ссылка на собственный Cancer Center. Сохраняются конфликт старого текста Prpich/current Hildebrandt и несовпадение ELIAS телефона.
- MedVet New Orleans: найдено отдельное официальное свидетельство ELIAS — именно Metairie и совпадающий телефон. Предложено узкое sponsor-listed access metadata и ссылка. Это не подтверждение текущей записи на ECI и не основание добавлять все сетевые услуги. Confirmed services сохраняются как Medical oncology.
- Семь предложений заменяют/дополняют сведения об источниках, три уточняют referral/booking, одно сохраняет sponsor-listed access metadata. Точная разбивка и old_value есть ниже и в JSON; количество предложений не равно числу новых ошибок в клиниках.

## Предложения по данным

### 1. gulf-coast-veterinary-specialists — care_delivery
Файл: data/oncology_centers_supplemental.json; целевая идентичность: gulf-coast-veterinary-specialists.
Причина: Clarify current published intake route without converting typical referral to absolute rule.

Старое значение: `"Fixed Houston hospital; specialty appointments; local Halcyon radiation delivery with remote specialist planning. Not an owner teleconsultation service."`
Новое значение: `"Fixed Houston hospital; specialty appointments; local Halcyon radiation delivery with remote specialist planning. Not an owner teleconsultation service. A primary-veterinarian referral is usually required, but owners may also request an appointment; the hospital obtains records from the primary veterinarian."`
Evidence: w3-10; дополнительные: w3-02, w3-11.
Неопределённость: None for the proposed narrow factual change.

### 2. gulf-coast-veterinary-specialists — supporting_urls
Файл: data/oncology_centers_supplemental.json; целевая идентичность: gulf-coast-veterinary-specialists.
Причина: Retain current explicit tumor-excision and intake evidence.

Старое значение: `["https://www.gcvs.com/locations/houston", "https://www.gcvs.com/services/medical-oncology", "https://www.gcvs.com/services/radiation-oncology", "https://www.gcvs.com/gcvs-houston-team", "https://www.gcvs.com/referral-support", "https://www.gcvs.com/staff/jiaqi-li", "https://www.gcvs.com/staff/nicola-wilson", "https://www.gcvs.com/staff/dustin-lewis", "https://www.gcvs.com/staff/jane-rowlands"]`
Новое значение: `["https://www.gcvs.com/locations/houston", "https://www.gcvs.com/services/medical-oncology", "https://www.gcvs.com/services/radiation-oncology", "https://www.gcvs.com/gcvs-houston-team", "https://www.gcvs.com/referral-support", "https://www.gcvs.com/staff/jiaqi-li", "https://www.gcvs.com/staff/nicola-wilson", "https://www.gcvs.com/staff/dustin-lewis", "https://www.gcvs.com/staff/jane-rowlands", "https://www.gcvs.com/services/surgery-orthopedics", "https://www.gcvs.com/faq"]`
Evidence: w3-09; дополнительные: w3-10, w3-34.
Неопределённость: None for the proposed narrow factual change.

### 3. colorado-animal-specialty-emergency-case — master_url
Файл: data/oncology_care_source_inventory.json; целевая идентичность: colorado-animal-specialty-emergency-case.
Причина: Replace third-party specialist-directory verification entry with branch-owned cancer-centre page.

Старое значение: `"https://www.vetspecialists.com/vet-detail/?animals=dog&specs=Onco&country=United%20States&page=46&id=299610de-6e8b-467b-814b-9602e6a67617"`
Новое значение: `"https://www.coloradoanimalspecialty.com/services/cancer-center"`
Evidence: w3-12; дополнительные: нет.
Неопределённость: None for the proposed narrow factual change.

### 4. colorado-animal-specialty-emergency-case — verification_url
Файл: data/oncology_centers_supplemental.json; целевая идентичность: colorado-animal-specialty-emergency-case.
Причина: Use current official local oncology source in clinic record.

Старое значение: `"https://www.vetspecialists.com/vet-detail/?animals=dog&specs=Onco&country=United%20States&page=46&id=299610de-6e8b-467b-814b-9602e6a67617"`
Новое значение: `"https://www.coloradoanimalspecialty.com/services/cancer-center"`
Evidence: w3-12; дополнительные: нет.
Неопределённость: None for the proposed narrow factual change.

### 5. colorado-animal-specialty-emergency-case — access_note
Файл: data/oncology_centers_supplemental.json; целевая идентичность: colorado-animal-specialty-emergency-case.
Причина: Current oncology booking is dedicated Patient Portal rather than generic request-form route.

Старое значение: `"2972 Iris Ave, Boulder CO 80301; 303-545-2273; Request a Specialty Appointment, physical care. Referral discussion published; mandatory referral requirement not established."`
Новое значение: `"2972 Iris Ave, Boulder CO 80301; 303-545-2273. Oncology has direct online scheduling through the official appointment page Patient Portal. Referral guidelines ask specialist-transfer clients to call and submit records before appointment. Physical care; an absolute initial referral-only requirement is not established."`
Evidence: w3-19; дополнительные: w3-20, w3-40.
Неопределённость: Whether every initial oncology visit requires a primary-vet referral remains unpublished; no referral-free promise.

### 6. mash — verification_url
Файл: data/oncology_centers_supplemental.json; целевая идентичность: mash.
Причина: Use branch-owned oncology page instead of third-party specialist directory.

Старое значение: `"https://www.vetspecialists.com/vet-detail/?animals=dog&specs=Onco&country=United%20States&page=46&id=6c01d834-8ec3-4152-a016-bb28daca2bb5"`
Новое значение: `"https://mash.vet/specialty-care/oncology"`
Evidence: w3-25; дополнительные: нет.
Неопределённость: None for the proposed narrow factual change.

### 7. mash — access_note
Файл: data/oncology_centers_supplemental.json; целевая идентичность: mash.
Причина: Preserve outpatient identity and publishable current oncology schedule separately from24/7 main emergency facility.

Старое значение: `null`
Новое значение: `"In-person oncology is at MASH Outpatient Facility, 6611 Santa Monica Blvd., Los Angeles CA 90038, Sunday through Friday. Call 855-350-7387; referring veterinarians can submit the specialty referral form. Mandatory initial owner referral requirement is not publicly established."`
Evidence: w3-39; дополнительные: w3-26, w3-27, w3-28.
Неопределённость: Mandatory referral requirement remains unconfirmed. Shared header6565 is not an alternate oncology site; exact clinician availability should be confirmed when booking.

### 8. mash — supporting_urls
Файл: data/oncology_centers_supplemental.json; целевая идентичность: mash.
Причина: Retain direct biography, current roster and referral evidence.

Старое значение: `["https://mash.vet/", "https://mash.vet/contact-us", "https://mash.vet/specialty-care/oncology"]`
Новое значение: `["https://mash.vet/", "https://mash.vet/contact-us", "https://mash.vet/specialty-care/oncology", "https://mash.vet/about/team/rose-dicovitsky", "https://mash.vet/about/team/", "https://mash.vet/for-vets"]`
Evidence: w3-35; дополнительные: w3-36, w3-27.
Неопределённость: None for the proposed narrow factual change.

### 9. carolina-veterinary-specialists — verification_url
Файл: data/oncology_centers_supplemental.json; целевая идентичность: carolina-veterinary-specialists.
Причина: Point to branch-specific service and required-referral source; preserve separate Matthews identity.

Старое значение: `"https://www.vetspecialists.com/vet-detail/?animals=dog&specs=Onco&country=United%20States&page=46&id=52e6752c-e861-4570-94a7-c80b212dc4e4"`
Новое значение: `"https://www.greensboro.carolinavet.com/site/specialties/oncology"`
Evidence: w3-30; дополнительные: нет.
Неопределённость: None for the proposed narrow factual change.

### 10. medvet-new-orleans — supporting_urls
Файл: data/oncology_centers_supplemental.json; целевая идентичность: medvet-new-orleans.
Причина: Store newly identified branch-specific official sponsor ECI provider evidence.

Старое значение: `["https://www.medvet.com/location/new-orleans/", "https://www.medvet.com/doctor/sarah-lyles/", "https://www.medvet.com/doctor/amber-moses/", "https://www.medvet.com/specialty/radiation-oncology/"]`
Новое значение: `["https://www.medvet.com/location/new-orleans/", "https://www.medvet.com/doctor/sarah-lyles/", "https://www.medvet.com/doctor/amber-moses/", "https://www.medvet.com/specialty/radiation-oncology/", "https://eliasanimalhealth.com/available-locations/"]`
Evidence: w3-32; дополнительные: w3-33, w3-21.
Неопределённость: Current hospital booking, patient eligibility and active treatment-delivery schedule remain for branch confirmation.

### 11. medvet-new-orleans — sponsor_listed_treatment_access
Файл: data/oncology_centers_supplemental.json; целевая идентичность: medvet-new-orleans.
Причина: A specific current sponsor provider listing is a meaningful access lead; retain it without broadening confirmed local service filters.

Старое значение: `null`
Новое значение: `{"program": "ELIAS Cancer Immunotherapy (ECI)", "listing_status": "Official sponsor lists MedVet New Orleans as an authorized ECI provider", "identity_match": "Metairie LA; 504-835-8508 matches current branch contact", "evidence_url": "https://eliasanimalhealth.com/available-locations/", "hospital_confirmation_status": "not_established", "booking_confirmation_required": true}`
Evidence: w3-32; дополнительные: w3-33, w3-21.
Неопределённость: Proposal is audit metadata pending schema/integration review, not a confirmed-services array expansion. Hospital-confirmed active bookings not established.

## Короткие подтверждения и provenance

Дата Web-проверок2026-10-13 UTC (2026-10-12 America/New_York). Web не сообщает точные секунды посещения; они не придуманы. HTTPS attempted_at/completed_at ниже — фактические замеры Python при обращении к странице. SHA-256 рассчитан по нормализованному видимому тексту, который полностью не сохранялся.


### w3-01 — gulf-coast-veterinary-specialists
URL: https://www.gcvs.com/
Короткая цитата: «8042 Katy FWY»
Scope: Houston, 8042 Katy Freeway, TX 77024; not NASA Parkway
Подтверждение: {"street": "8042 Katy FWY", "city": "Houston", "region": "TX", "postal_code": "77024", "phone": "713-693-1111", "status": "Current Houston hospital listed with emergency and specialty care."}
Receipt: turn32view1; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:10.568174+00:00; completed_at=2026-10-13T02:46:14.787689+00:00; HTTP=200; quote_match=None.
Text fingerprint: 2bb30b5926ec14d58fe42f3f77fcd87f7d4c3fd87799413709a8bddb2d481b6e.

### w3-02 — gulf-coast-veterinary-specialists
URL: https://www.gcvs.com/locations/houston
Короткая цитата: «Specialty services are available by appointment only.»
Scope: Houston, 8042 Katy Freeway, TX 77024; not NASA Parkway
Подтверждение: {"branch_services": ["Medical oncology", "Radiation oncology", "Surgery & Orthopedics"], "specialty_access": "By appointment"}
Receipt: turn2view0; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:10.568966+00:00; completed_at=2026-10-13T02:46:14.991385+00:00; HTTP=200; quote_match=True.
Text fingerprint: 1a4f74a1c30d8d6e8dcf775b59f570e511e3791b116d3f3a1ef5352b36f74b8b.

### w3-03 — gulf-coast-veterinary-specialists
URL: https://www.gcvs.com/services/medical-oncology
Короткая цитата: «Chemotherapy and targeted therapies»
Scope: Houston, 8042 Katy Freeway, TX 77024; not NASA Parkway
Подтверждение: {"services": ["Chemotherapy", "Targeted therapy", "Immunotherapy"], "clinicians": ["Jiaqi Li DVM DACVIM", "Nicola Wilson DVM"]}
Receipt: turn5view0; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:10.569443+00:00; completed_at=2026-10-13T02:46:14.957060+00:00; HTTP=200; quote_match=True.
Text fingerprint: 6a1b6e539b5c47049a013a985a287178e87dae516f4e44f8eb9f1a8349c4e522.

### w3-04 — gulf-coast-veterinary-specialists
URL: https://www.gcvs.com/services/radiation-oncology
Короткая цитата: «Varian Halcyon Linear Accelerator with stereotactic radiation therapy (SRT) capability.»
Scope: Houston, 8042 Katy Freeway, TX 77024; not NASA Parkway
Подтверждение: {"services": ["Local radiation oncology", "SRT", "full-course radiation", "palliative radiation"]}
Receipt: turn5view1; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:10.571482+00:00; completed_at=2026-10-13T02:46:14.909777+00:00; HTTP=200; quote_match=True.
Text fingerprint: ff644a6682f4b91b732fcf727cf0735b9809e83a710a1f868e9bf048bfe41411.

### w3-05 — gulf-coast-veterinary-specialists
URL: https://www.gcvs.com/staff/jiaqi-li
Короткая цитата: «DVM, DACVIM»
Scope: Houston, 8042 Katy Freeway, TX 77024; not NASA Parkway
Подтверждение: {"clinician": "Jiaqi Li", "role": "Medical oncology", "credentials": "DVM DACVIM"}
Receipt: turn5view2; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:10.572347+00:00; completed_at=2026-10-13T02:46:14.599845+00:00; HTTP=200; quote_match=True.
Text fingerprint: 9b399e26277d785b5f835ae4e8ba9e3e945247f19344d8dececd662392113e61.

### w3-06 — gulf-coast-veterinary-specialists
URL: https://www.gcvs.com/staff/nicola-wilson
Короткая цитата: «completed a residency in oncology»
Scope: Houston, 8042 Katy Freeway, TX 77024; not NASA Parkway
Подтверждение: {"clinician": "Nicola Wilson", "role": "Medical oncology", "credentials": "DVM; oncology residency; no board certification printed"}
Receipt: turn5view3; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:10.575724+00:00; completed_at=2026-10-13T02:46:14.568723+00:00; HTTP=200; quote_match=True.
Text fingerprint: 7c43fc1c05376e969e978c3e5ceafe7fa8610211ecbcb6c6d9a92f7a30b3c9f3.

### w3-07 — gulf-coast-veterinary-specialists
URL: https://www.gcvs.com/staff/dustin-lewis
Короткая цитата: «provides remote consultations, develops personalized radiation therapy treatment plans»
Scope: Houston, 8042 Katy Freeway, TX 77024; not NASA Parkway
Подтверждение: {"clinician": "Dustin Lewis", "credentials": "DVM MBA DACVR (RO)", "scope": "Supporting radiation oncologist based at sister hospital in Red Bank NJ; remote plans and first-day patient alignment"}
Receipt: turn5view4; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:10.577696+00:00; completed_at=2026-10-13T02:46:14.521557+00:00; HTTP=200; quote_match=True.
Text fingerprint: 3acc1a8e8f96c64e8e00a07e98bb3bf77b0e082ae08cca51411b888d2a02a079.

### w3-08 — gulf-coast-veterinary-specialists
URL: https://www.gcvs.com/staff/jane-rowlands
Короткая цитата: «dedicated hospitalist for the Radiation Oncology department»
Scope: Houston, 8042 Katy Freeway, TX 77024; not NASA Parkway
Подтверждение: {"clinician": "Jane Rowlands", "credentials": "DVM, not listed DACVR", "role": "Local radiation hospitalist"}
Receipt: turn7view3; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:10.578575+00:00; completed_at=2026-10-13T02:46:14.586564+00:00; HTTP=200; quote_match=True.
Text fingerprint: 9425f873ddecdf8e186862672918c94922c17ca10b4e4272c6df56af3bfc64c8.

### w3-09 — gulf-coast-veterinary-specialists
URL: https://www.gcvs.com/services/surgery-orthopedics
Короткая цитата: «Tumor and Integument Excision»
Scope: Houston, 8042 Katy Freeway, TX 77024; not NASA Parkway
Подтверждение: {"services": "Local tumor excision and soft-tissue oncologic procedures; not assigning fellowship credentials."}
Receipt: turn7view0; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:14.522281+00:00; completed_at=2026-10-13T02:46:18.629160+00:00; HTTP=200; quote_match=True.
Text fingerprint: 5f997d2116ae9def64aba69f1e09d7f44186f567513265c96b29fc16a524f5b7.

### w3-10 — gulf-coast-veterinary-specialists
URL: https://www.gcvs.com/faq
Короткая цитата: «However, you may also request an appointment.»
Scope: Houston, 8042 Katy Freeway, TX 77024; not NASA Parkway
Подтверждение: {"referral": "Usually primary-vet referral before specialist appointment, but owner may request appointment and clinic obtains primary-vet records."}
Receipt: turn32view0; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:14.569067+00:00; completed_at=2026-10-13T02:46:18.816835+00:00; HTTP=200; quote_match=True.
Text fingerprint: 9b9e5adfac6341b5fd7956506048e98105c8898d472390591c3733f1d19a9df6.

### w3-11 — gulf-coast-veterinary-specialists
URL: https://www.gcvs.com/referral-support
Короткая цитата: «Patient Referral Form»
Scope: Houston, 8042 Katy Freeway, TX 77024; not NASA Parkway
Подтверждение: {"referral": "Veterinary referral form plus recent records and diagnostic results requested; attending-vet call valued before transfer."}
Receipt: turn7view2; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:14.588310+00:00; completed_at=2026-10-13T02:46:18.916598+00:00; HTTP=200; quote_match=True.
Text fingerprint: 169c9b0ff03e05e2d7e169c6cc493182b7c6bd47f9da24aebab40b74acf9ef6c.

### w3-12 — colorado-animal-specialty-emergency-case
URL: https://www.coloradoanimalspecialty.com/services/cancer-center
Короткая цитата: «offers immunotherapy, chemotherapy, and electrochemotherapy options»
Scope: CASE, 2972 Iris Ave, Boulder CO 80301
Подтверждение: {"street": "2972 Iris Ave", "city": "Boulder", "region": "CO", "postal_code": "80301", "phone": "303-545-2273", "services": ["Immunotherapy", "Chemotherapy", "ECT"], "team": ["Annie Galloway DVM MS DACVIM", "Brittany Wittenberns DVM MS DACVIM", "Clarissa Freemyer DVM DACVR"]}
Receipt: turn2view1; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:14.600052+00:00; completed_at=2026-10-13T02:46:19.639638+00:00; HTTP=200; quote_match=True.
Text fingerprint: 0e539c6952b8a4ff4e13e46eab5f1c5a24168e6ce4b8637ff57757fc2a3b98d2.

### w3-13 — colorado-animal-specialty-emergency-case
URL: https://www.coloradoanimalspecialty.com/services/radiation-oncology
Короткая цитата: «Varian Halcyon linear accelerator»
Scope: CASE, 2972 Iris Ave, Boulder CO 80301
Подтверждение: {"services": ["Local IMRT", "VMAT", "SRT", "SRS", "IGRT"]}
Receipt: turn11view0; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:14.788031+00:00; completed_at=2026-10-13T02:46:19.861275+00:00; HTTP=200; quote_match=True.
Text fingerprint: 879a8f2376c893859e8670c540527f1782c9bfe56a34dd01d68c02439adf700a.

### w3-14 — colorado-animal-specialty-emergency-case
URL: https://www.coloradoanimalspecialty.com/services/surgical-oncology
Короткая цитата: «our surgical oncologist, radiation oncologist and medical oncologists collaborate»
Scope: CASE, 2972 Iris Ave, Boulder CO 80301
Подтверждение: {"services": "Dedicated surgical oncology at CASE", "conflict": "Service narrative still names Dr Prpich; not departure proof."}
Receipt: turn11view1; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:14.910173+00:00; completed_at=2026-10-13T02:46:19.594906+00:00; HTTP=200; quote_match=True.
Text fingerprint: 471fb90b6d38e324d216b720caf3d2e69611b3d24c622c841ae34e2dac88b953.

### w3-15 — colorado-animal-specialty-emergency-case
URL: https://www.coloradoanimalspecialty.com/staff/bella-hildebrandt
Короткая цитата: «surgical oncology fellowship at Colorado State University»
Scope: CASE, 2972 Iris Ave, Boulder CO 80301
Подтверждение: {"clinician": "Bella Hildebrandt", "credentials": "DVM DACVS-SA; surgical oncology fellowship at CSU", "role": "Current branch profile, surgical oncology"}
Receipt: turn11view2; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:14.957397+00:00; completed_at=2026-10-13T02:46:19.400632+00:00; HTTP=200; quote_match=True.
Text fingerprint: c1795315d56076915cb6e1ea6aefa56598532b809ff5cfb097fa960d3ca9d739.

### w3-16 — colorado-animal-specialty-emergency-case
URL: https://www.coloradoanimalspecialty.com/staff/annie-galloway
Короткая цитата: «DVM, MS, DACVIM»
Scope: CASE, 2972 Iris Ave, Boulder CO 80301
Подтверждение: {"clinician": "Annie Galloway", "credentials": "DVM MS DACVIM", "role": "medical oncology"}
Receipt: turn11view3; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:14.991703+00:00; completed_at=2026-10-13T02:46:19.373254+00:00; HTTP=200; quote_match=True.
Text fingerprint: 326313a4a2be0b84541a47b219c24a453e05e8962b1d8aff82c003b1c82f01d3.

### w3-17 — colorado-animal-specialty-emergency-case
URL: https://www.coloradoanimalspecialty.com/staff/brittany-wittenberns
Короткая цитата: «became a Diplomate of the American College of Veterinary Internal Medicine (Oncology) in 2021»
Scope: CASE, 2972 Iris Ave, Boulder CO 80301
Подтверждение: {"clinician": "Brittany Wittenberns", "credentials": "DVM MS DACVIM (Oncology), certified 2021"}
Receipt: turn11view4; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:18.629689+00:00; completed_at=2026-10-13T02:46:21.501149+00:00; HTTP=200; quote_match=True.
Text fingerprint: 656fc3d91fba35e27558d7b45e407ee4e245f26a14402e7692005cf7c1a21b8a.

### w3-18 — colorado-animal-specialty-emergency-case
URL: https://www.coloradoanimalspecialty.com/staff/clarissa-freemyer
Короткая цитата: «completed a three-year residency program in Radiation Oncology»
Scope: CASE, 2972 Iris Ave, Boulder CO 80301
Подтверждение: {"clinician": "Clarissa Freemyer", "credentials": "DVM DACVR; Radiation Oncology residency and current cancer-centre assignment; RO suffix not separately printed"}
Receipt: turn35view3; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:18.817199+00:00; completed_at=2026-10-13T02:46:21.521767+00:00; HTTP=200; quote_match=True.
Text fingerprint: 536a56607422dcac0b321d4a6eeec6d36bd57916bf092c8ccaf780b370f1cf99.

### w3-19 — colorado-animal-specialty-emergency-case
URL: https://www.coloradoanimalspecialty.com/appointment
Короткая цитата: «Dentistry & Oncology Appointment»
Scope: CASE, 2972 Iris Ave, Boulder CO 80301
Подтверждение: {"access": "Oncology online booking through advertised Patient Portal; general specialty request form is separate."}
Receipt: turn35view1; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:18.916872+00:00; completed_at=2026-10-13T02:46:21.600753+00:00; HTTP=200; quote_match=True.
Text fingerprint: 7619e8a10ba4223041dd01f8b15120284753904eccc8b4561e9095824d34a5ea.

### w3-20 — colorado-animal-specialty-emergency-case
URL: https://www.coloradoanimalspecialty.com/for-veterinarians
Короткая цитата: «Referral Guidelines»
Scope: CASE, 2972 Iris Ave, Boulder CO 80301
Подтверждение: {"access": "Referral route and guidelines linked; same-day transfers by phone."}
Receipt: turn35view2; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:19.373552+00:00; completed_at=2026-10-13T02:46:21.637212+00:00; HTTP=200; quote_match=True.
Text fingerprint: 3817935dea7599beee96ed306f17e9feba6c7383058ccb422abc741c785dc803.

### w3-21 — medvet-new-orleans
URL: https://www.medvet.com/location/new-orleans/
Короткая цитата: «2315 N. Causeway Blvd.»
Scope: MedVet New Orleans, 2315 N. Causeway Blvd, Metairie LA 70001; not Mandeville
Подтверждение: {"address": "2315 N. Causeway Blvd., Metairie LA 70001", "phone": "504-835-8508", "services": "Medical oncology in branch-specific services; no local RT claim", "team": ["Sarah Lyles DVM DACVIM (Oncology)", "Amber Moses DVM DACVIM (Oncology)"]}
Receipt: turn2view2; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:19.400848+00:00; completed_at=2026-10-13T02:46:23.596002+00:00; HTTP=200; quote_match=True.
Text fingerprint: e17e1bc633aa65b5e2c603cb60dc84b02e3a149089df0b1c26382c761a0fc2e7.

### w3-22 — medvet-new-orleans
URL: https://www.medvet.com/doctor/sarah-lyles/
Короткая цитата: «at both MedVet Mandeville and MedVet New Orleans»
Scope: MedVet New Orleans, 2315 N. Causeway Blvd, Metairie LA 70001; not Mandeville
Подтверждение: {"clinician": "Sarah Lyles", "credentials": "DVM DACVIM (Oncology)", "assignment": "Both New Orleans and Mandeville"}
Receipt: turn25view0; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:19.595514+00:00; completed_at=2026-10-13T02:46:23.466720+00:00; HTTP=200; quote_match=True.
Text fingerprint: 5e4f93d0cb990bc392377a1cb784f071249226cdb8770189c15be302de1181e1.

### w3-23 — medvet-new-orleans
URL: https://www.medvet.com/doctor/amber-moses/
Короткая цитата: «Amber Moses, DVM, DACVIM (Oncology)»
Scope: MedVet New Orleans, 2315 N. Causeway Blvd, Metairie LA 70001; not Mandeville
Подтверждение: {"clinician": "Amber Moses", "credentials": "DVM DACVIM (Oncology)", "assignment": "New Orleans"}
Receipt: turn25view1; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:19.640006+00:00; completed_at=2026-10-13T02:46:23.524577+00:00; HTTP=200; quote_match=None.
Text fingerprint: d5a40e6d8de02b2bb12b3ad38325355214f9fa5d0a869454a1a9d2af81133c26.

### w3-24 — medvet-new-orleans
URL: https://www.medvet.com/specialty/medical-oncology/
Короткая цитата: «Not all services are available in every hospital.»
Scope: Network-wide context only; NOT New Orleans local service proof
Подтверждение: {"scope": "Network treatment menu is not branch proof. New Orleans chemo, ECT and immunotherapy remain unconfirmed from this page."}
Receipt: turn32view5; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:19.861654+00:00; completed_at=2026-10-13T02:46:23.548563+00:00; HTTP=200; quote_match=True.
Text fingerprint: b7d633803020548c920487e7b6237394ef22b81c3e761dd228e0de46e969ce13.

### w3-25 — mash
URL: https://mash.vet/specialty-care/oncology
Короткая цитата: «Injectable and Oral Chemotherapy»
Scope: MASH Outpatient, 6611 Santa Monica Blvd, Los Angeles CA 90038; not main ER at 6565
Подтверждение: {"services": ["Chemotherapy", "ECT", "Immunotherapy"], "team": ["Rose Dicovitsky VMD DACVIM", "Colleen Tansey DVM DACVIM"], "access": "Oncology Sunday through Friday at Outpatient Facility"}
Receipt: turn2view3; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:21.501468+00:00; completed_at=2026-10-13T02:46:24.209057+00:00; HTTP=200; quote_match=True.
Text fingerprint: 5e92813b8e4011a5192a699f3b1681a2873644b7f65420490b8afd4549293274.

### w3-26 — mash
URL: https://mash.vet/contact-us
Короткая цитата: «6611 Santa Monica Blvd.»
Scope: MASH Outpatient, 6611 Santa Monica Blvd, Los Angeles CA 90038; not main ER at 6565
Подтверждение: {"address": "Outpatient Facility, 6611 Santa Monica Blvd., Los Angeles CA 90038", "phone": "855-350-7387", "scope": "Main ER address in shared header is not oncology treatment address"}
Receipt: turn18view0; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:21.522021+00:00; completed_at=2026-10-13T02:46:24.324261+00:00; HTTP=200; quote_match=True.
Text fingerprint: e7146fec752aa3b58d98e4846715b33226a613e0651acff5369b385d4ec3cc33.

### w3-27 — mash
URL: https://mash.vet/for-vets
Короткая цитата: «please complete the referral form»
Scope: MASH Outpatient, 6611 Santa Monica Blvd, Los Angeles CA 90038; not main ER at 6565
Подтверждение: {"referral": "Veterinarian referral form for specialty cases. No published statement this is mandatory for owners."}
Receipt: turn18view1; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:21.601175+00:00; completed_at=2026-10-13T02:46:24.360262+00:00; HTTP=200; quote_match=True.
Text fingerprint: 53a1b5fb6bc920757b279ea76b1d311deade7eaf57f82a05fb5fcf5838b469ba.

### w3-28 — mash
URL: https://mash.vet/patient-center
Короткая цитата: «new client forms»
Scope: MASH Outpatient, 6611 Santa Monica Blvd, Los Angeles CA 90038; not main ER at 6565
Подтверждение: {"access": "Owner patient centre includes forms and general contact. Mandatory referral unresolved."}
Receipt: turn18view2; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:21.637586+00:00; completed_at=2026-10-13T02:46:24.418317+00:00; HTTP=200; quote_match=True.
Text fingerprint: e4b95515742cb88bb40b22cd3033477fc6b9de9cab2b4e113172f1ccc7432a43.

### w3-29 — carolina-veterinary-specialists
URL: https://www.greensboro.carolinavet.com/site/home
Короткая цитата: «501 Nicholas Rd Greensboro NC 27409 US»
Scope: Carolina Veterinary Specialists Greensboro, 501 Nicholas Rd, NC 27409; not Matthews
Подтверждение: {"address": "501 Nicholas Rd, Greensboro NC 27409", "phone": "336-632-0605", "access": "Specialty appointments Monday-Friday, 8am-5pm; emergency 24/7 distinct"}
Receipt: turn18view3; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:23.466951+00:00; completed_at=2026-10-13T02:46:26.585391+00:00; HTTP=200; quote_match=True.
Text fingerprint: 20b3c8d297de043bb887d1e710f40bc661d2a14c11096950a66617b8ceb2f17d.

### w3-30 — carolina-veterinary-specialists
URL: https://www.greensboro.carolinavet.com/site/specialties/oncology
Короткая цитата: «referral from your primary care veterinarian is required»
Scope: Carolina Veterinary Specialists Greensboro, 501 Nicholas Rd, NC 27409; not Matthews
Подтверждение: {"services": ["Medical oncology", "Chemotherapy", "Immunotherapy", "Targeted therapy"], "referral": "Primary-vet referral required before oncology appointment"}
Receipt: turn35view0; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:23.524824+00:00; completed_at=2026-10-13T02:46:26.680715+00:00; HTTP=200; quote_match=True.
Text fingerprint: 0e2b1e8674f1957874b6795e6f24a9efdbeaa225fc1d7550297d9982f951b8af.

### w3-31 — carolina-veterinary-specialists
URL: https://www.greensboro.carolinavet.com/site/specialty-veterinarians/dr-diana-burr-oncology
Короткая цитата: «Diana Burr, DVM, MS, Diplomate ACVIM»
Scope: Carolina Veterinary Specialists Greensboro, 501 Nicholas Rd, NC 27409; not Matthews
Подтверждение: {"clinician": "Diana Burr", "credentials": "DVM MS Diplomate ACVIM Oncology; current Greensboro board-certified oncologist"}
Receipt: turn18view4; public HTTPS GET with finite timeout, HTML visible text extraction; no raw source retained; checked_at=2026-10-13; attempted_at=2026-10-13T02:46:23.548976+00:00; completed_at=2026-10-13T02:46:26.649059+00:00; HTTP=200; quote_match=True.
Text fingerprint: 891490a5cf3d2d4769f3c14bc68142c7a912c256f2ad6d19ea464f3a0a8320cb.

### w3-32 — medvet-new-orleans
URL: https://eliasanimalhealth.com/available-locations/
Короткая цитата: «MedVet New Orleans»
Scope: Sponsor-listed ECI provider: MedVet New Orleans in Metairie; exact matching name, city, phone. Not network menu.
Подтверждение: {"sponsor_provider_listing": "ELIAS current ECI provider list identifies MedVet New Orleans in Metairie LA, phone 504-835-8508 matching branch. Sponsor page updated September 21 2026. Hospital direct confirmation of current bookings remains missing.", "case_existing_eci": "Same provider roster lists Colorado Animal Specialty and Emergency in Boulder, phone303-678-8844; do not overwrite CASE branch confirmed phone303-545-2273."}
Receipt: turn52view1; public HTTPS GET with finite timeout, normalized visible text; short quotes only; checked_at=2026-10-13; attempted_at=2026-10-13T02:48:26.852540+00:00; completed_at=2026-10-13T02:48:30.089639+00:00; HTTP=200; quote_match=True.
Text fingerprint: 135e070ddfea07a7f8b6c050fcd759955f5c5b9bbda83ed80bc1d854288f271c.

### w3-33 — medvet-new-orleans
URL: https://eliasanimalhealth.com/available-locations/
Короткая цитата: «Find an ECI® Provider Near You»
Scope: Specific ECI program context only; no broad chemotherapy or ECT inference
Подтверждение: {"program_scope": "Roster is specifically ELIAS Cancer Immunotherapy ECI authorized treatment centres for canine patients."}
Receipt: turn52view1; public HTTPS GET with finite timeout, normalized visible text; short quotes only; checked_at=2026-10-13; attempted_at=2026-10-13T02:48:30.089926+00:00; completed_at=2026-10-13T02:48:32.890579+00:00; HTTP=200; quote_match=True.
Text fingerprint: 135e070ddfea07a7f8b6c050fcd759955f5c5b9bbda83ed80bc1d854288f271c.

### w3-34 — gulf-coast-veterinary-specialists
URL: https://www.gcvs.com/gcvs-houston-team
Короткая цитата: «Jiaqi Li»
Scope: Houston exact branch
Подтверждение: {"branch_team": "Houston roster confirms Jiaqi Li and Nicola Wilson medical oncology; Dustin Lewis/Jane Rowlands radiation; seven surgeons listed without new fellowship labels."}
Receipt: turn58view5; public HTTPS GET with finite timeout, normalized visible text; short quotes only; checked_at=2026-10-13; attempted_at=2026-10-13T02:48:32.890833+00:00; completed_at=2026-10-13T02:48:35.962271+00:00; HTTP=200; quote_match=True.
Text fingerprint: 3b37bae82dd3b2a19e605a1cac15761d5516b2a033a5f7897f630d5192a35cc4.

### w3-35 — mash
URL: https://mash.vet/about/team/rose-dicovitsky
Короткая цитата: «VMD, DACVIM (Oncology)»
Scope: MASH; current outpatient assignment established on branch oncology page
Подтверждение: {"clinician": "Rose Dicovitsky board-certified medical oncology; direct official biography"}
Receipt: turn61view0; public HTTPS GET with finite timeout, normalized visible text; short quotes only; checked_at=2026-10-13; attempted_at=2026-10-13T02:48:35.962739+00:00; completed_at=2026-10-13T02:48:38.879253+00:00; HTTP=200; quote_match=True.
Text fingerprint: c04d18c3f5b4de37e173c9e426e2eb9edb647be5d67fcb55d3514743585d8a32.

### w3-36 — mash
URL: https://mash.vet/about/team/
Короткая цитата: «Colleen Tansey»
Scope: MASH; outpatient assignment established by dedicated oncology page
Подтверждение: {"clinician": "Colleen Tansey DVM DACVIM Oncology; current roster; page card points to team rather than dedicated biography"}
Receipt: turn61view1; public HTTPS GET with finite timeout, normalized visible text; short quotes only; checked_at=2026-10-13; attempted_at=2026-10-13T02:48:38.879521+00:00; completed_at=2026-10-13T02:48:41.742251+00:00; HTTP=200; quote_match=True.
Text fingerprint: ec6bf3e4fafa93f17d30630f08923cc06b37c8c9101dd79d2a990cb7f848f905.

### w3-37 — medvet-new-orleans
URL: https://www.medvet.com/faqs/?nav_context=for-pet-parents
Короткая цитата: «our specialty patients are seen by appointment»
Scope: MedVet general intake policy applied as intake context only
Подтверждение: {"access": "Published MedVet specialty process uses appointments; this supports booking process only, not local treatment modalities. Mandatory initial oncology referral unanswered."}
Receipt: turn61view4; public HTTPS GET with finite timeout, normalized visible text; short quotes only; checked_at=2026-10-13; attempted_at=2026-10-13T02:48:41.742475+00:00; completed_at=2026-10-13T02:48:45.158009+00:00; HTTP=200; quote_match=True.
Text fingerprint: ecd9e0030886f226423dd8442d2cd34e330c3f1a5bcd2b0257a38af5a0be9318.

### w3-38 — carolina-veterinary-specialists
URL: https://www.greensboro.carolinavet.com/site/specialties/oncology
Короткая цитата: «immunotherapy, chemotherapy, targeted therapies»
Scope: Greensboro only; not Matthews
Подтверждение: {"services": "Greensboro oncology page directly discusses these three systemic treatment options in branch team treatment planning. Surgery planning text does not establish specialized surgical oncology."}
Receipt: turn52view0; public HTTPS GET with finite timeout, normalized visible text; short quotes only; checked_at=2026-10-13; attempted_at=2026-10-13T02:48:45.158223+00:00; completed_at=2026-10-13T02:48:48.030100+00:00; HTTP=200; quote_match=True.
Text fingerprint: 4adc582e378e82275b33e045bb8d9fde83250fdedc0479bbcbb68f19673b9135.

### w3-39 — mash
URL: https://mash.vet/specialty-care/oncology
Короткая цитата: «Sunday through Friday»
Scope: MASH Outpatient at6611 Santa Monica Blvd
Подтверждение: {"access": "Published oncology availability Sunday-Friday; in person outpatient facility."}
Receipt: turn2view3; public HTTPS GET with finite timeout, normalized visible text; short quotes only; checked_at=2026-10-13; attempted_at=2026-10-13T02:48:48.030321+00:00; completed_at=2026-10-13T02:48:51.465606+00:00; HTTP=200; quote_match=True.
Text fingerprint: 5e92813b8e4011a5192a699f3b1681a2873644b7f65420490b8afd4549293274.

### w3-40 — colorado-animal-specialty-emergency-case
URL: https://assets.ctfassets.net/rt5zmd3ipxai/2mch0tnC49P1ZmSv0lMwdh/3071cea4fd473e9a33c22e5548027c28/62c908d8-64eb-46f5-8a97-234ce72e8d6a.pdf
Короткая цитата: «Please have client call and schedule»
Scope: CASE 2972 Iris Ave Boulder CO80301
Подтверждение: {"referral": "Referral guidelines ask specialist-transfer clients to phone for appointments and submit records before appointment; do not establish an absolute referral-only initial-booking requirement."}
Receipt: turn61view2; Web PDF text open, pages0-1, lines9-10 and23-40; checked_at=2026-10-13; attempted_at=не измерено Web; completed_at=не измерено Web; HTTP=Web PDF; quote_match=Web exact excerpt.
Text fingerprint: не рассчитан для Web PDF.

## Ошибки и остаток

- https://www.medvet.com/for-pets/ — Branch-linked For Pet Parents route and FAQs used instead.
- https://www.medvet.com/for-pet-owners/ — Branch-linked For Pet Parents route used.
- https://www.medvet.com/faq/ — Actual branch-linked /faqs/ used.
- https://mash.vet/team/rose-dicovitsky — Clicked actual oncology link to /about/team/rose-dicovitsky.
- https://mash.vet/team/colleen-tansey — Actual oncology link points to current general team.

Сетевые строки меню не были приняты за proof local treatment. Все5 назначенных идентичностей имеют доступные официальные branch/service/team/contact evidence. Остаток — конкретные вопросы в таблице, без выводов об отсутствии услуги или закрытии. Координатный вопрос MASH не решён точным geocode; существующий ZIP centroid не выдаётся за геокод здания.

Для следующего технического пакета сохранять5 подобных глубоких филиальных записей на исполнителя. Увеличение до10–15 пока не обосновано: число открытых вопросов определяется публикациями клиник, а не скоростью обработки. Из этого теста нельзя сделать вывод о готовой недельной системе.
