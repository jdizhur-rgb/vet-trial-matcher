# Вермонт: расширенный поиск клиник, 25 ноября 2026

После продолжения поиска в каталоге **45 физических клиник и одна выездная хирургическая служба**. Добавлены 35 физических мест и Ascend Veterinary Surgery. У Mount Anthony отдельно подтверждена хирургия опухолей.

Первоначальные 10 записей были результатом произвольного ограничения прохода, а не полного поиска штата. Это ограничение снято.

## Что важно

- West Mountain Animal Hospital в Беннингтоне прямо подтверждает введение химиотерапии в клинике. Всего подтверждены две физические локации с химиотерапией: West Mountain и Peak.
- Mount Anthony и West Mountain — разные больницы. Исправлено ложное слияние по похожему имени и ZIP 05201; их услуги не смешиваются.
- Ascend — выездная хирургия по направлению лечащего ветеринара; почтовый ящик в Shelburne не является кабинетом лечения.
- Enosburg не принимает новых клиентов. Westminster на нынешнем сайте сообщает о приёме новых клиентов; более старое ограничение из программы VSNIP не перенесено как актуальное.
- Riverside добавлен для Ратленда. Опухолевая хирургия в его филиале Ludlow и в филиале Veremedy Woodstock отдельно не подтверждена.
- Четыре записи опираются на развёрнутые тексты официальных страниц из поискового индекса. Прямые ограничения доступа и необходимость уточнить запись сохранены. Координаты новых больниц не выдумывались; ZIP Essex Veterinary Center оставлен неизвестным.

## Добавленные физические клиники

| Клиника | Город | Подтверждённая услуга |
| --- | --- | --- |
| Arlington Animal Hospital | Arlington | Удаление опухолей/масс |
| West Mountain Animal Hospital | Bennington | Химиотерапия |
| Onion River Animal Hospital | Berlin | Удаление опухолей/масс |
| Country Animal Hospital | Bethel | Удаление опухолей/масс |
| Bradford Veterinary Clinic | Bradford | Удаление опухолей/масс |
| Brattleboro Veterinary Clinic | Brattleboro | Удаление опухолей/масс |
| VCA Windham Animal Hospital | Brattleboro | Удаление опухолей/масс |
| VCA Fitzgerald Animal Hospital | Colchester | Удаление опухолей/масс |
| East Haven Veterinary Service | East Haven | Удаление опухолей/масс |
| Ryegate Small Animal Hospital | East Ryegate | Удаление опухолей/масс |
| Enosburg Veterinary Care | Enosburg Falls | Удаление опухолей/масс |
| Essex Veterinary Center | Essex Junction | Удаление опухолей/масс |
| Mountain View Animal Hospital | Essex Junction | Удаление опухолей/масс |
| Northeast Kingdom Community Animal Hospital | Lyndonville | Удаление опухолей/масс |
| Milton Veterinary Hospital | Milton | Удаление опухолей/масс |
| Montpelier Veterinary Hospital | Montpelier | Удаление опухолей/масс |
| West River Veterinary Service | Newfane | Удаление опухолей/масс |
| Newport Veterinary Hospital | Newport | Удаление опухолей/масс |
| River Road Veterinary Clinic | Norwich | Удаление опухолей/масс |
| Riverside Veterinary Care and Dental Services | Rutland | Удаление опухолей/масс |
| Rutland Veterinary Clinic and Surgical Center | Rutland | Удаление опухолей/масс |
| Ark Veterinary Hospital | Shelburne | Удаление опухолей/масс |
| Shelburne Veterinary Hospital | Shelburne | Удаление опухолей/масс |
| Dorset Street Animal Hospital | South Burlington | Удаление опухолей/масс |
| Orchard Veterinary Hospital | South Burlington | Удаление опухолей/масс |
| VCA Brown Animal Hospital | South Burlington | Удаление опухолей/масс |
| Springfield Animal Hospital | Springfield | Удаление опухолей/масс |
| Tanneberger Veterinary Hospital | St. Albans | Удаление опухолей/масс |
| Stowe Veterinary Clinic | Stowe | Удаление опухолей/масс |
| Vergennes Animal Hospital | Vergennes | Местная онкопомощь; метод уточнить |
| Waterbury Veterinary Hospital | Waterbury Center | Удаление опухолей/масс |
| Westminster Animal Hospital | Westminster Station | Удаление опухолей/масс |
| Veremedy Pet Hospital | White River Junction | Удаление опухолей/масс |
| Long Trail Veterinary Center | Williston | Удаление опухолей/масс |
| Kedron Valley Veterinary Clinic | Woodstock | Удаление опухолей/масс |

## Охват и ограничения

Использованы независимые городские каталоги, государственный список VSNIP и список Humane Society of Chittenden County, затем текущие страницы услуг, врачей и контактов клиник. У VCA пройден национальный индекс → карта Вермонта (236 URL) → шесть страниц хирургических услуг трёх местных филиалов. Каталожные строки включают старые названия, повторы, лошадей и соседние штаты; это не число независимо проверенных больниц.

Сохранено 1181 URL-запросов. По каждому домену ведётся отдельное решение в clinic-review-ledger.json. Неподтверждённые процедуры, недоступные источники, исторические названия и филиальные вопросы сохранены в remaining.json. Это не перепись всех лицензированных ветеринаров и не доказательство отсутствия других услуг. Клиникам не писали.

## Проверки

- `python scripts/build_static_site.py` — PASS (каталог, фильтры, matcher, production sync и исторические регрессии).
- `node scripts/test_a01_care_reconciliation.js` — PASS.
- `python scripts/test_a02_care_reconciliation.py` — PASS.
- `python scripts/test_b01_care_reconciliation.py` — PASS.
- `python scripts/test_b02_care_reconciliation.py` — PASS.
- `python scripts/test_c01_care_reconciliation.py` — PASS.
- `python scripts/check_evidence_keys.py` и `git diff --check` — PASS.
- Проверены все 36 новых идентичностей, отдельные адреса/телефоны, неизвестные координаты, запрет новых клиентов Enosburg и обе клиники Беннингтона.

## Даты проверки источников

Всего в реестре источников: 2036. Изменено и проверено локально: 42 записей. Диапазон сохранённых фактических запросов: 2026-11-26T02:50:59.477839+00:00 — 2026-11-26T03:04:57.725802+00:00. Дата клинического просмотра — 25 ноября по America/New_York; точные UTC-времена сохранены отдельно. У четырёх индексных клинических просмотров — точность до даты, без выдуманного успешного live-времени. Их результаты остаются partial, фактические 403/406 не превращены в 200. Для новых записей прежней даты не было; Mount Anthony обновлён с 11 октября на 25 ноября. Исходные клинические даты остальных записей не освежались от одного запроса.

Удалённая проверка SHA, дат и публикации будет зафиксирована в production-readback.json.
