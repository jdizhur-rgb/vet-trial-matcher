**Первый блок завершён и опубликован.** 14 октября 2026, 18:36 America/New_York.

Исправлены 9 существующих карточек: CAALM, UCD oral-margin, COTC033, FAP CAR-T, четыре протокола UTSW и TAMU feline WART. Уточнены критерии, ограничения лечения и расходы владельцев. Две существовавшие карточки UTSW вернулись в публичную выдачу; новых исследований 0.

Матчер соблюдает строгие границы возраста и веса, сохраняя возможность поиска при неизвестных значениях. Граница 15/36 кг CAALM исключительная; возраст oral-margin строго больше одного года; VROC Study 5 — вес строго больше 2,5 кг. Включительные границы других протоколов сохранены.

Каталог до → после: canonical 310 → 310; public matchable 163 → 165; treatment trials 158 → 160; other treatment access 5 → 5; sources 111 → 111.

Проверки PASS: catalog/schema, sanitation (0 новых неполных записей), semantic dedupe (0 вероятных дублей), source inventory, loading regression, 55 source-derived reviews / 247 cases, JS selection 1483 checks / 166 criteria, Python parity 19800 checks, matcher logic, build и production-sync. Старый тест числа MCT-вариантов заменён точным списком пяти подтверждённых протоколов.

Публикация: main eca20a12c3b67348db3de18935ac874a81a98e98. Локальный и удалённый tree 58be017b2a6a51d5bc62c937a115d6424547903d совпадают; все 18 файлов прочитаны обратно. Shell push не имел credentials; публикация выполнена через GitHub connector с проверкой ожидаемого main, без force push.

Deploy PASS: https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/38648415905

Production PASS: live HTML, matcher.js и trials.json побайтно совпадают со сборкой. В HTML новая версия script protocol-limits-20261014 и content-hash каталога. Живой поиск Dog / Cancer — any type, diagnosis I don't know, пустые age/weight/ZIP, все treatments, Any approach: USA 106, Japan 10, состав соответствует текущему каталогу. Это проверка отображённых результатов через форму в браузере.

Дата источников: использованы фактические утренние protocol-level evidence 14 октября; вечерняя публикация не выдана за новые посещения. source_inventory и audit_state не изменены. Общий разбор 68 источников и шесть спорных европейских карточек в этот блок не входят и остаются незавершёнными.

Подтверждения: catalog-changes.json, primary-evidence.json, validators.json, build-output.txt, remote-readback.json, production-readback.json, live-search.json, expected-live-search.json, deploy.json.
