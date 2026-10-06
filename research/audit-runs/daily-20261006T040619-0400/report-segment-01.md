6 октября 2026, 05:06 America/New_York
Режим: DAILY GLOBAL WORK AUDIT

Проверка среды: PASS — фактически исполнены pwd (/workspace/scratch/0856bb16a45a), python --version (Python 3.12.14), git --version (git version 2.51.1).

Промежуточный статус: INCOMPLETE. Run ID: daily-20261006T040619-0400; начало 04:06:19 −04:00. Часовая контрольная точка: работа продолжается с оставшейся очереди.

Known-source coverage: исходные 82 источника посещены; все обязательные inventory fallback_urls при недостаточном master были попытаны. Вместе с 9 новыми источниками: 91/91 попыток, 38 достаточных сверок, 45 partial, 8 unreachable. Открытие страницы и свежая дата не считаются полным покрытием. Для CSU восстановлен официальный текущий Flint roster и прочитаны перенаправленные протоколы; для Wisconsin прочитаны актуальные DOCX-согласия; для SAGE сверены ссылки PetCure и ImpriMed. Остаток: 53 источника. Точная очередь с ID, URL и причинами сохранена в pending-queue-segment-02.json; текущий immutable receipt — receipt-segment-01.json.

Главные пробелы: AVMA перечислен полностью (850 записей, 62 recruiting oncology), но остаются противоречия дат/статусов и multicenter-сверка; у CSU/Tufts/UC Davis не установлено точное отношение FAP CAR-T когорт; NCI/RVC/MSU/WSU и отдельные официальные маршруты блокируются; часть японских и спонсорских программ не публикует полный текущий набор протоколов или enrollment. Их нельзя объявить проверенными.

Global discovery: выполнены поиски США, Канады, Великобритании, континентальной Европы, Мексики/Центральной Америки/Карибов, Южной Америки, Австралии/Новой Зеландии, Восточной/Южной/Юго-Восточной Азии, Ближнего Востока и Африки. Использованы английский, французский, немецкий, испанский, португальский, японский, китайский, корейский, хинди, тайский, иврит, арабский и африкаанс. Точные дополнительные запросы и найденные ссылки сохранены в global-discovery.json. Это не утверждение об исчерпывающем поиске всего мира.

NEW — 2: Gifu, кошки с oral SCC, лучевая терапия + Lavurchin/SQAP; Hokkaido, собаки с oral melanoma и лёгочными метастазами, anti-PD-L1. Первичные протоколы: https://www.animalhospital.gifu-u.ac.jp/cancer/clinical_trial/202508.html и https://www.vetmed.hokudai.ac.jp/VMTH/aboutus/research/.

UPDATE — 3: CSU engineered T cells теперь только soft tissue sarcoma, уточнены минимум 11 кг, ограничения и лимиты финансирования; Wisconsin half-body RT + CHOP — четыре фракции, включение после двух циклов CHOP при partial/complete remission и точные оплачиваемые расходы; Wisconsin FLASH — оплата radiation/amputation, лекарства от побочных эффектов не покрыты, matching консервативно учитывает требование ампутации в согласии.

CLOSE/HIDE — 0. NEW SOURCES — 9: EVVIVAX, CureLab, The Cancer Vet India, Dog Cancer Foundation directory, Gifu, Hokkaido, Benno Therapeutics, Seoul VMTH, ACI Biosciences. Новые trial sources не означают 9 новых trials.

UNRESOLVED: текущий набор Enzistat/UQ; Elenagen/CureLab; BTX001/Benno; старые окна SNU; точная multicenter-идентичность FAP CAR-T; конфликт optional amputation в кратком Wisconsin listing и обязательной ампутации в текущем consent.

REJECTED/DUPLICATES: закрытый набор ACI oral melanoma и Purdue PD-L1 vaccine; PetCure прямо сообщает об отсутствии активного набора; ImpriMed MCT на паузе и diagnostic/sample-only, feline страница теперь диагностика; UK sample/AI-generated cards; diagnostics, prevention, биобанки, supportive diarrhea и safety/PK-only; уже имеющиеся Penn FLASH glioma, UC Davis CARE/PRISM, REACH-GLIO и исторические EVVIVAX. Новых автоматических semantic-дублей: 0. Ручных действий Юли сейчас не требуется.

Exact counts: canonical 299 → 301; публичный matcher 161 → 163; лечебные trials 156 → 158; другие treatment-access записи 5 → 5; trial source inventory 82 → 91.

Изменённые и опубликованные файлы: data/trials_base.json, data/source_inventory.json, data/audit_source_coverage.json, data/audit_state.json, seo/static/matcher/trials.json, seo/static/matcher/matcher.js, scripts/test_matcher_logic.js; per-run receipt, global-discovery, local-readback, confirmed-changes и immutable архив evidence. Проверки клиник/онкологов и care inventories не выполнялись; их сгенерированные сборкой побочные изменения восстановлены.

Даты проверки источников: local readback PASS 91/91; remote-main readback PASS 91/91. Предыдущие и новые значения сохранены по каждому источнику. last_checked_at: 2026-10-06T04:06:19.573517−04:00 … 2026-10-06T04:52:47.933375−04:00. Несовпадений дат: 0. Partial/unreachable сохраняют дату попытки, но не считаются успешно сверенными. Remote SHA: 39c783e5fc9c8b58406f54ddd7f1c9ff0b32c0ed.

Проверки: canonical/schema, sanitation (0 новых partial records), source inventory, semantic dedupe, matcher regressions, build и production sync — PASS. validate_audit_receipt.py — INCOMPLETE: 0 ошибок целостности, 53 coverage gaps. Общий аудит не завершён.

Commit/main: 39c783e5fc9c8b58406f54ddd7f1c9ff0b32c0ed — опубликован. GitHub deploy 37440294486 — success. Production — PASS: live trials.json (163 записи), matcher.js и matcher/ побайтово совпали со сборкой; новые японские trials и исправленная CSU disease scope присутствуют. Проверено 05:05:36 America/New_York. Результаты продолжающейся сверки будут сохранены следующим immutable сегментом этого же run_id.
