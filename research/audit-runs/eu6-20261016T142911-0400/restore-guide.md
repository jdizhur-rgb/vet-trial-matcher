# Восстановление research-only checkpoints

Каноническая удалённая ветка: `research/europe-recovery-eu6-20261016T142911-0400`. История Git этой ветки создаётся GitHub connector сериализованно с expected SHA и без force. Локальная branch history отличается: НЕ push/reset/force-push её поверх remote. Для сайта использовать отдельный свежий main только после all-six приёмки.

1. Получить ветку конечным `git fetch` и зафиксировать фактический SHA. Прочитать `backups/ledger.json` и receipts, не полагаться на локальный ready.json.
2. Initial salvage: `backups/initial-salvage.tar.zst`, SHA256 `83482148b1daa536bccadd210c33f1f638e980c66149b7c0cbc4e5fd8c38d695`. 441 research-файл перечислен в initial-backup-manifest.json; .git/секреты/canonical snapshots туда не включены. Старые worker payloads находятся под прежним run_id; это исторические данные, не новые проверки.
3. Проверить archive SHA256 против remote control и receipt. Затем читать tar только в новый пустой recovery directory, без абсолютных путей, symlinks или `..` traversal. Initial manifest задаёт hash каждого файла.
4. Применить checkpoint-001, 002 и последующие по ledger: каждый содержит только новые immutable candidate/source/query/restriction shards и небольшой controller manifest. Проверить каждый archive SHA256 и member SHA256. Не применять research proposals к production автоматически.
5. `assignments.json` задаёт реальные agent IDs, страны, baseline SHA и пути исходных входных материалов. Полные canonical inputs воспроизводятся из baseline `2f7099307e174556883ca6eb97495bead2dc3401`; inherited inputs — из проверенного initial archive. Не считать потерю копии inputs потерей их canonical baseline.
6. Кандидатные версии/append-only amendments объединять по явному supersedes/version, а не по имени чата. DE block-02/ready.json — ошибочный непринятый draft; использовать исправленный block-02delta. Старые successful source dates не обновлять временем восстановления/неудачной попытки.
7. Восстановить exact restrictions ДО любых новых источников. Actual auth/CAPTCHA/approval denials не обходить. Не читать результаты запрещённого Procházka workflow. DE unknown scope остаётся карантином, не разрешением и не мировым запретом.

Remote `worker-N/report.md` — удобные прямые ссылки на последний замороженный отчёт, не замена архивам evidence/proposals/queries/remaining. Приёмка research_complete и публикация сайта — отдельные будущие действия, не следствие успешного backup.
