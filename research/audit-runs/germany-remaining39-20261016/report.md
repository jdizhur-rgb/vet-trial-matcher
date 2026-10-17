# Германия: завершение повторной проверки 39 кандидатов

Обновление 17 октября: новое правило владельца разрешает одну карточку сети при подтверждённой сетевой услуге. Десять filu теперь представлены сетевым контактом; обязательных внешних подтверждений осталось семь, плюс два будущих открытия. Подробности: [новый отчёт](../filu-network-20261017/report.md). Ниже сохранён исходный отчёт прохода 16 октября; его прежний счётчик17 не является текущим остатком.

Доступный конечный проход завершён. Подготовлено 18 новых записей: 17 физических клиник и один выездной сервис. Ранее опубликованные 882 записи сохранены без изменения всех полей; итоговый каталог содержит 900 мест оказания помощи, из них 238 в Германии. Удалённых консультаций по-прежнему 64.

## Подтверждённые дополнения

| Провайдер | Город / территория | Подтверждённая помощь | Официальный источник |
|---|---|---|---|
| Kleintierzentrum Beyen Hirschberg | Hirschberg an der Bergstraße | Surgery | https://www.kleintierzentrum-hirschberg.de/home/ |
| Tierarztpraxis Schwachhausen – Dr. Claudia Kellermeier | Bremen | Local oncology care | https://tierarztpraxis-schwachhausen.de/ |
| Kleintierzentrum Kiel – kielVET Elmschenhagen | Kiel | Surgery | https://kielvet.de/leistungen/ |
| Internistische Kleintierpraxis Hoppe & Stech | Schenefeld | Local oncology care | https://kleintierpraxis-hoppe-stech.de/leistungen/ |
| Tierärzte Wiblingen | Ulm | Local oncology care | https://www.tieraerzte-wiblingen.de/fachgebiete |
| Tierarztpraxis Daniela Pommerening | Wolfenbüttel | Surgery | https://tierarztpraxis-pommerening.de/leistungen/operation.html |
| Kleintierpraxis Wendel | Mannheim | Surgery | https://kleintierpraxis-wendel.de/leistungen/ |
| Tierklinik Ganal & Ewert | Weingarten | Surgery | https://www.tierklinik-ganal-ewert.de/ueber-uns/leistungen/operative-eingriffe-chirurgie |
| Tierarztpraxis Dr. Jörg Waschbüsch | Saarwellingen | Chemotherapy, Surgery | https://tierarzt-waschbuesch.de/behandlungsspektrum/ |
| Kleintierpraxis Oberhausen – K. Büttner | Oberhausen | Surgery | https://www.kleintierpraxis-oberhausen.de/leistungen/ |
| Tierklinik auf dem Lichtenberge | Steyerberg | Surgery | https://tierklinik-lichtenberge.de/leistungen/chirurgie-bei-kleintieren/ |
| Kleintierpraxis Eckhard Bürgener | Wermelskirchen | Surgery | https://www.tierarzt-buergener.de/seite/492776/operationen.html |
| Zentrum für Tiergesundheit Linkenheim-Hochstetten | Linkenheim-Hochstetten | Surgery | https://www.tierarzt-liho.de/leistungen/chirurgie/ |
| Kleintierpraxis Stockelsdorf | Stockelsdorf | Chemotherapy, Surgery | https://www.tierarzt-stockelsdorf.de/onkologie.html |
| callavet – mobile veterinary service | Wiesbaden / Frankfurt / Mainz area | Chemotherapy | https://callavet.de/leistungen/tieraerztliche-leistungen/ |
| AniCura Tierärztliche Praxis Ingelheim | Ingelheim | Surgery | https://ingelheimer-tieraerzte.de/leistungen/ |
| Kleintierpraxis Dr. Tanja Kruse | Bremen-Oberneuland | Surgery | https://www.kleintierpraxis-kruse.de/unsere-leistungen/innere-medizin-orthopaedie-und-chirurgie |
| KleinTierzentrum Asterlagen | Duisburg-Asterlagen | Chemotherapy, Surgery | https://www.tierklinik-duisburg-asterlagen.de/index.php/auf-einen-blick/alle-fachbereiche/onkologie?view=article&id=9 |

## Итог всех 39

18 новых записей готовы к публикации. Из 21 остальных: десять действующих филиалов filu требуют подтверждения, в каком именно филиале выполняют лечение опухолей; два филиала ещё не открылись (Prenzlauer Berg — 19 октября 2026, Waiblingen — ноябрь); Tarp сопоставлен с опубликованной основной клиникой Schafflund для сложной помощи; у KlickVet на доступных собственных страницах не найдено достаточного онкологического сигнала. Это не утверждение, что клиника не лечит рак.

Оставшиеся семь внешних пробелов: три точных маршрута AniCura сохраняют ограничение действия, страница Stahl сохраняет реальный HTTP403, а официальные сайты Neufahrn, Sandhausen и Jimdo не дали доступного текущего первичного подтверждения. Таким образом, прямое подтверждение нужно для 17 провайдеров (10 filu и 7 отдельных); ещё два ожидают открытия. Подробные факты, вопросы и ссылки находятся в final-39-dispositions.json и unsent-confirmation-requests-de.md. Письма и формы не отправлялись.

## Почему прежние проверки зависали

Автоматический отказ смешанного запроса ошибочно был распространён на независимые сайты всего пакета. Фактический риск относился к маршрутам национального списка AniCura. Новые отдельные обычные запросы к шести независимым провайдерам, исключавшие ограниченные маршруты национального списка AniCura и запрещённые перенаправления, оказались доступны. Результаты старых отклонённых пакетов не использовались. Настоящие ограничения конкретных URL сохраняются.

Остальные клинические пробелы разрешены чтением собственных страниц операций, команды и контактов, а также единым порогом limited Local oncology care: явное текущее лечение или консультация по раку с квалифицированным врачом и доступным приёмом допускаются без выдуманной химиотерапии или хирургии. Только диагностика и направление к другим провайдерам недостаточны.

## Проверки и сохранение прежних данных

Полная сборка успешна; A01/A02/B01/B02/C01, sanitation, европейские и немецкие identity-регрессии пройдены. Семантическая проверка 18 новых записей не нашла совпадений идентификатора, телефона или адреса с прежними 882 и внутри дополнения.

Найдена и исправлена конкретная ошибка автоматического объединения двух разных практик Saarwellingen: Am Steinhübel и Waschbüsch. Добавлено исключение ровно для этой пары и регрессионный тест. Старые адрес, телефон, врач, Chemo/Surgery и ограничение «не принимает новых клиентов» Am Steinhübel полностью сохранены. Новый провайдер имеет другой адрес, телефон и врача.

## Продолжение

Не повторять поиск 87/39 с нуля. Использовать germany-continuation.json, финальный ledger и восемь подготовленных, но не отправленных немецких запросов. Поиск новых регионов и автоматизации не запускались. Полное подтверждение всех провайдеров Германии не заявляется.

Опубликовано: PR22, main `f8e19c7c8d2216ceade92ef802b33cb1fec43c5a`. Все три workflow успешны. Production HTTP200 побайтово совпадает с полной сборкой: centers852369bytes, SHA256 `fbf0e4941569cfc903cd30eeba4fe30e7d709e83de85ce22edc89c87c19138ad`; tele172029bytes, SHA256 `449d48ff730f125baca3dc6e5c0450ae07a0dbc75253d4bcd404d9ac776c3d5c`. Все18 новых имён присутствуют на опубликованной странице. Полная квитанция: publication-receipt.json.
