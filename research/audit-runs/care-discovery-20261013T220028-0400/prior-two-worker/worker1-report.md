# Результат исполнителя 1 — три клиники

Исполнитель `/root/scheduled_worker1`. Первая измеренная рабочая отметка 2026-10-13T02:17:04Z; завершение 2026-10-13T02:21:46.968893+00:00. Назначено 3, обработано 3, полностью подтверждено по выбранным полям 2. База не редактировалась, публикация не выполнялась.

13 официальных страниц получены прямыми GET с конечным timeout 15 секунд; все HTTP200. Реальные время/URL/тексты в shell-evidence.json. Web refs и давность crawl сохраняются отдельно, не выдаются за время сегодняшней прямой загрузки.

## River Ridge Animal Hospital — Dixon

Адрес 273 Illinois Route 2, Dixon IL 61021; телефон 815-288-3394 — [контакты](https://riverridgevets.com/contact/). Запись владельцем через запрос приёма. [Команда](https://riverridgevets.com/veterinarian-dixon-il/): Nathan McClain, Chris Gunnon, Phil Fassler, Erin Graves, Trisha Cooper, Lauren Robinson, Justin Hohlen, Melissa Corson — ветеринары общей практики без приписанной онкологической сертификации. [Местная химиотерапия](https://riverridgevets.com/pet-chemotherapy-dixon-il/) и хирургическое лечение рака в биографии Fassler подтверждены. Решение: сохранить baseline без исправлений; отсутствие сертифицированного онколога не отменяет химиотерапию.

## San Francisco Animal Medical Center — San Francisco

2343 Fillmore St, San Francisco CA 94115; 415-465-6291 — [контакты](https://www.sfamc.com/contact). [Отделение](https://www.sfamc.com/specialty-care/oncology) подтверждает Chemotherapy, ECT, вакцинную Immunotherapy и удаление опухолей собственным хирургическим отделением. Биографии подтверждают Aarti Sabhlok DVM DACVIM и Dillon Didehvar VMD DACVIM как местных онкологов. Решение: сохранить baseline. Прошлая подготовка Sabhlok по radiation oncology не доказывает местную лучевую терапию.

Остаётся вопрос: [форма](https://www.sfamc.com/referrals/refer) подтверждает направление ветеринаром, но не его обязательность. Дни онкологического приёма не опубликованы на проверенных страницах. 24/7 относится к экстренной помощи. Эти поля оставлены неизвестными; запись считается partial.

## SERV — Stratham

137 Portsmouth Ave, Stratham NH 03885; 603-379-8383; specialty Mon–Thurs 9am–5pm, emergency 24/7 — [контакты](https://servnh.com/contact-veterinary-hospital-stratham-nh/). Есть прямой запрос онкологической записи владельцем и отдельный путь направления. Kelvin Kow — местный board-certified ACVIM Oncology по биографии; DAVCD в заголовке — внутренняя опечатка, которую не переносим в данные. Существующие услуги подтверждены [онкологической страницей](https://servnh.com/veterinary-cancer-care/).

Найдено дополнение на [странице хирургии](https://servnh.com/veterinary-surgery/): «Mass and tumor removal». Предложить добавить Surgery и местные surgery/contact URLs. Это доказанное удаление опухолей; отдельная сертификация surgical oncology не заявляется. Robin Zuckerman указан DVM/хирургом.

## Результат

Два предложения только для SERV: services и supporting_urls. Старые значения взяты из переданного актуального supplemental baseline. proposed_changes.json содержит цитаты, время, URL и scope. evidence.json содержит field-level подтверждения; result.json — счётчики, состав проверки и остаток. SFAMC частично подтверждён по условиям доступа. Внешних препятствий для базовых фактов нет. Долговечное сохранение выполняет главный исполнитель; scratch не считается сохранением.
