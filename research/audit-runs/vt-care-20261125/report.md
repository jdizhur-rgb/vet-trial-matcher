# Вермонт: первый пакет клиник — 25 ноября 2026

Добавлены 8 физических клиник с подтверждённой опухолевой хирургией. Вместе с двумя существующими в каталоге 10 клиник штата. Полный поиск по штату не завершён: оставшиеся города, VCA и мобильные услуги перечислены в review.json.

| Клиника | Город |
| --- | --- |
| Veterinary Surgery of Vermont | South Burlington |
| Champlain Veterinary Clinic | St. Albans |
| Sugar Maple Veterinary Center | Williston |
| Green Mountain Veterinary Hospital | Manchester Center |
| Mount Mansfield Animal Hospital | Jericho |
| Eastwood Animal Clinic | Rutland |
| Richmond Animal Hospital | Richmond |
| Burlington Emergency and Veterinary Specialists | Williston |

Peak: действующая страница сообщает о возобновлении консультаций, но только для перечисленных семи групп диагнозов. Внесено конкретное ограничение приёма. Старый буклет BEVS не использован для подтверждения современной химиотерапии; добавлена актуальная хирургия с Josie Mallinckrodt. У новых клиник координаты не выдумывались.

## Проверки

- `python scripts/build_static_site.py`: PASS, включая каталог, фильтры, production sync и исторические проекции.
- `node scripts/test_a01_care_reconciliation.js`: PASS.
- `python scripts/test_a02_care_reconciliation.py`: PASS.
- `python scripts/test_b01_care_reconciliation.py`: PASS.
- `python scripts/test_b02_care_reconciliation.py`: PASS.
- `python scripts/test_c01_care_reconciliation.py`: PASS.
- `python scripts/check_evidence_keys.py`: PASS.
- `git diff --check`: PASS.
- Сопоставление проверенного локального дерева и origin/main: PASS.
- Побайтовое сравнение production /matcher/centers/ с собранным HTML: PASS.

## Даты проверки источников

26 сохранённых запросов URL: 25 ответов 200, один 404. 19 выполненных поисковых запросов сохранены отдельно. Для 9 изменённых записей источников текущие даты/время записаны и проверены в remote main: 9/9, PASS. Диапазон этих времён: 2026-11-25 23:31:53.828605–23:32:15.536224 UTC (18:31:53–18:32:15 EST). У 8 новых записей ранее не было даты; Peak обновлён с 2026-10-12 на 2026-11-25. Пропущенных дат среди этих 9 нет. Неизменённая Mount Anthony сохраняет прежнюю дату 2026-10-11 и не считается перепроверенной. Это не аудит всех источников каталога.

Production commit: `3a4683a8a7b395ebdc3e264ff42fc1d8d680e5cf`. Подтверждение публикации и хеш HTML — в production-readback.json.
