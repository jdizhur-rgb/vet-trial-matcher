# P00 — сверка и публикация

Завершено 12 октября 2026. 15 source_id соответствуют 14 физическим клиникам.

## Уже было опубликовано

Переезд ACCS в Littleton и исключение старого Acton-профиля; химиотерапия, иммунотерапия и targeted therapy HEAL; химиотерапия Dunes и Franklin Lakes. Повторных клиник не добавлено.

## Внесено сейчас

| Клиника | Недостающие изменения |
|---|---|
| Animal Cancer Care Specialists | Chemotherapy, Immunotherapy, Targeted therapy; website: https://accsvets.com/services/ |
| BRIDGE Animal Referral Center | Chemotherapy, Surgical oncology |
| Broward Veterinary Specialists | Chemotherapy, Immunotherapy; street: 3331 Sheridan St, phone: 954-842-4000, website: https://browardvet.com/services/pet-oncology |
| Dogwood Veterinary Specialty & Emergency | Chemotherapy, Surgical oncology; website: https://www.dogwood.vet/services/pets/pet-oncology-marietta |
| Heal Cancer Care for Pets | Услуги и контакты уже соответствовали; сохранены проверка, квалификация и доказательства. |
| Denver Animal Hospital | street: 2103 E Virginia Ave, phone: 303-871-8719, website: https://denveranimalhospital.org/ |
| Dover Veterinary Hospital | Surgery |
| Dunes Animal Hospital | Услуги и контакты уже соответствовали; сохранены проверка, квалификация и доказательства. |
| Eastern Carolina Veterinary Medical Center | Immunotherapy, Targeted therapy, Surgery; name: Eastern Carolina Veterinary Medical Center, website: https://www.easterncarolinavet.com/services/medical-oncology |
| Eclipse Specialty and Emergency Pet Care | Chemotherapy, Targeted therapy, Immunotherapy, Surgery; phone: 862-404-0991, website: https://eclipsevetcare.com/veterinary-oncology |
| Evolution Veterinary Specialists | Chemotherapy, Surgical oncology |
| Franklin Lakes Animal Hospital | Услуги и контакты уже соответствовали; сохранены проверка, квалификация и доказательства. |
| Haven Lake Animal Hospital | Surgery |
| Golden Gate Veterinary Specialists | Chemotherapy, Immunotherapy, Surgical oncology; street: 4460 Redwood Hwy Suite 11, phone: 415-726-2458, website: https://www.ggvets.com/oncology/ |

Официальные URL, короткие выдержки, исходные даты посещений и привязки к филиалам сохранены в review.json и каталоге. Не добавлена местная лучевая терапия по внешним направлениям или общим описаниям. Услуги отделены от квалификации врачей.

## Вопросы следующего прохода

- heal-cancer-care-for-pets: Separate remote-service audience, format and eligibility review; not inferred from the physical clinic.
- denver-animal-hospital: Specific local anticancer drug modalities are not established by traditional/integrative wording.
- broward-veterinary-specialists: Cancer-specific surgical access and vaccine brand remain unconfirmed.
- dogwood-veterinary-specialty-emergency: Dunwoody opening announced for October 20; do not activate before current opening and local services are confirmed.
- animal-cancer-care-specialists: Next pass: obtain direct live service/team body; archived official content is cached and direct fetch returned 403.
- haven-lake-animal-hospital: Do not map hyperthyroidism I-131 wording to confirmed malignant thyroid treatment.

## Проверки и публикация

- Data commit: `20baa6f5a32fec64cb1cb51ae00c0a67c7c42335`.
- Сборка: `python scripts/build_static_site.py` — PASS; 218 HTML-страниц, 6981 внутренних ссылок.
- Каталог: 438 записей; ACCS — ровно одна физическая клиника. Все не относящиеся к P00 записи сохранены без изменений.
- PASS: validate_trials_catalog, validate_catalog_sanitation, validate_source_inventory, semantic_dedupe_catalog; отдельная проверка уникальности care source_id и дат.
- PASS: A01/A02/B01/B02/C01 regressions, matcher catalog loading, test_evidence_keys, check_evidence_keys, diff whitespace; новые и изменённые доказательства проверены на Google/GitHub/AWS/private-key patterns.
- GitHub build, deployment, catalog integrity and evidence-key workflows — success.
- Production `/matcher/centers/`: HTTP 200; все 14 карточек и вся страница байт-в-байт совпадают со сборкой.
- SHA-256 production/build: `b2be3d068df14da7a6e96b8751191eb8b21045a90c7756e95c048cfc931bc9f7`.
- Даты проверки источников: 15 назначенных, 15 проверены по наследованным подтверждениям, 15/15 remote-verified; новых посещений сайтов не было. Исходные timestamps: 2026-10-11 15:32:27–16:12:36 America/New_York. Дата локальной сверки не выдана за новую дату посещения.
- Отдельный source-date-readback.json содержит предыдущие/опубликованные даты и результаты по каждому source_id.

Пакет завершён; вопросы оставлены в пометках следующего прохода.
