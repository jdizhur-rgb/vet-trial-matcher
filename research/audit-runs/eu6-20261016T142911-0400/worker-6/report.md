# Нидерланды — исследование в работе

Агент /root/recovery_nl, фактический старт 2026-10-16 18:43:10 UTC; eu6-20261016T142911-0400; baseline 2f7099307e174556883ca6eb97495bead2dc3401. Исследование НЕ завершено, publication_permitted=false.

## Что унаследовано

Checkpoint-14: 177 промежуточных adjudication-групп, 45 fully, 51 старых NEW и 3 UPDATE. Это НЕ результаты нового исполнения. Spijkenisse подтверждён в текущем полном baseline и не является NEW. Сохранены 49 неопубликованных физических кандидатов, частичный VSC и 3 field-scoped UPDATE. 10 lump-only withdrawals и Max & Bella остаются held. Исходные даты не обновляются offline-сверкой.

## Новая фактическая работа

{"assigned":4,"processed":4,"fully_verified":0,"NEW":0,"UPDATE":0,"DUPLICATE":0,"EXCLUDED":1,"UNRESOLVED":3}; 19 новых query executions, не клиник. Первые четыре кандидатных review см. records/review-001.json; source/evidence append-only shards в shards/.

Восстановлен текущий публичный BestCare master: https://bestcaredierenartsen.nl/praktijken/ (старый /deelnemende-praktijken/ возвращает 404). Он показывает 12 записей: 10 клинических групп плюс administrative Best Care Organisatie и Voorbeeldkliniek; это не 12 новых клиник. Публично открыты 9 групповых branch-roster страниц; работа по реальным локальным филиалам продолжается.

De Verwijskliniek (Bergen op Zoom, Laan van Hildernisse Noord 8, +31 164 657675): текущие процедуры/команда/контакт подтверждены; только общая soft-tissue/orthopedic/neurosurgery, явное лечение опухоли не установлено — не продвигается как cancer surgery. Veterinaire Specialisten Vught: точный root403 сохранён без повторов.

BES больше не «не искали»: просмотрены первичные Bonaire Veterinary Center, SEAWF Statia, Saba government veterinary/clinic notices, Bonaire government and shelter current contacts. BVC: Dr. Jochem/Eva/Yara, адрес/телефон/приём, Oncology+mass removal опубликованы, но конкретный cancer-treatment scope требует осторожной проверки из-за незаполненных template-блоков. Statia: Dr. Veira и visiting Dr. Swanston, регулярный pet clinic/стерилизация, не доказательство онколечения. Saba SFPCA: Eva de Vries DVM, English Quarter agriculture building, +599 4167947; онкология ещё не установлена. Общенационального absence-вывода нет.

## Покрытие и доступный остаток

Все 12 провинций имеют сохранённые прежние current/new search layers, но доступный национальный frontier остаётся. Utrecht university прежняя первичная проверка сохранена; свежего визита университету этим исполнением пока нет. AniCura85/IVC219-label и othernetwork rosters — наследие, не новые выполненные visits. Текущая очередь: BestCare actualbranches, Ossehoofd2/ZOD3 allocation, другие текущие сети/aliases, independent/opening leads, original18 same-standard fields и окончательные distinct-provider counts. Все10 workgroups в remaining.json остаются явным own unfinished, не внешними блокерами.

## Ограничения и сохранность

22 inherited NL holds плюс новый https://veterinairespecialisten.nl/ Web403 (turn2837view1), scope exact root/equivalent. Общие copied holds проверяются guard перед запросами. Noaber roster из случайного поискового результата не открывался/не восстанавливался. Общая старая offline-pause отменена новым run; реальные access-ограничения не отменены.

Даты проверки: новые Web источники 2026-10-16, date-only; failed attempts не обновляют successful source date. Baseline triage records/baseline-dedupe-001.json использует полный copied physical/supplemental/inventory/ACVIM и tele; exact/name/address hits: Spijkenisse already-applied плюс три existing UPDATE identity. Нулевой exact hit не заменяет ручную semantic review.

Remote backup VERIFIED только block01+restriction001: branch research/europe-recovery-eu6-20261016T142911-0400; data SHA626eea1561eec9404e09cdc438b166c3052500a5; receipt17933a8a3766a8c8141872b0739a72f7c14a3ffc. Остальные текущие файлы ещё не имеют remote-подтверждения. Production/canonical/commit/push/deploy worker не выполняет.
