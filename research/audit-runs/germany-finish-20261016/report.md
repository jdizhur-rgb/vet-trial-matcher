# Германия: полный отчёт о выполненном и препятствиях

**Статус: Германия НЕ завершена. Это итог разрешённой документальной сверки, а не сертификат национальной полноты.**

Работа выполнялась отдельно от других стран, в чистой копии текущего remote main `54da45666528c6e1f1007625e56d6871243ee21c`. Производственные данные, matcher и другие исполнители не изменялись. Новых клинических сетевых запросов в этой сверке — 0; удержанные действия не повторялись.

## Что проверено и доведено до результата

Разобран весь сохранённый остаток из 333 неклассифицированных URL: каждому дана маршрутная категория и основание в general-333-route-review.json. Это проверка смысла сохранённого URL/названия и назначения источника; страницы заново не открывались, находки не превращались в проверенные клиники.

Сохранены все 102 кандидата из последнего индивидуального индекса; для 87 незакрытых имён собраны сохранившиеся точные URL, исходные даты доказательств, конкретные недостающие факты и разрешительный статус. Все 87 имеют хотя бы reference URL, но только18distinctclinicalURLs сохранены: профессиональная запись не подменяет клинический источник.

## Результаты клиник

Счётчики предшествующей сверки не обновлялись искусственно: 102 assigned; 69 processed;4 NEW draft;8 DUPLICATE;3 EXCLUDED;54 UNRESOLVED;33 identity-only unprocessed. 9 полностьюпроверенных по прежней системе включают5 already-live + 4 draft, а не9 новых. Не суммировать эти единицы с1176URL/171 профессиональными ссылками/109 записями Saarland.

| Готовый проект | Подтверждённая местная услуга | Первичный источник |
|---|---|---|
| Dr. Boris Sülzle, Nortorf | Удаление опухолей | http://www.tierarztpraxis-nortorf.de/kleintierpraxis.php |
| Angelika Drensler, Elmshorn | Онкохирургия, химиотерапия | https://www.tierarzt-drensler.de/leistungen/ |
| Dr. Steffen Sager, Schönberg | Tumor-OP | https://www.tierarzt-schoenberg.de/leistungen/chirurgie |
| Nicolas Genz, Wedel | Удаление опухолей в собственных операционных | https://www.tierarztpraxis-elbe.de/chirurgie |

Точные клинические выдержки частично уцелели после прошлого сбоя; это retained selected excerpts, а не полный rawpage. Текущая регистрационная идентичность/контакты проверялись ранее отдельными официальными профессиональными источниками. Все исходные даты сохранены; эта offline сверка не является новой датой визита. Специалист-онколог, химиотерапия или лучевая терапия сверх явно подтверждённого не приписываются. Публичные цены/направление/приём новых пациентов, если не опубликованы, требуют уточнения. QA родителя дополнительно проверила отсутствие sourceID/телефон/адрес/website совпадений в свежем main. Эти четыре проекта НЕ опубликованы, потому что полный поиск страны ещё не завершён.

Дубли: Mario Erler (Kassel), Tierklinik Oberhaching, Kleintierklinik Bremen KasparFaberStraße4, AniCura Bremen StaderStraße35, Rosenhof/Claudia Hartke (Mühlhausen), Anja Zogall (Schwerin), Niendorf/Sabine Rudat, LMU Kleintierklinik. Существующие записи сохраняются, новых копий нет.

Исключённые источники и кандидаты: Pferdeklinik Eutin и Pferdeklinik Bilsen — сохранённое первичное доказательство относится к лошадям; VetMRT — диагностическая MRI/CT, не лучевая терапия. Это не утверждение о закрытии клиник.

## Национальное покрытие

| Обязательное направление | Реально достигнуто | Чего не хватает |
|---|---|---|
| Все16 земель и21 крупныйгород | Ранее сохранены current/undated иnewsignalпоиски115queries/30searchcalls | Постатейная проверка клинических кандидатов не завершена |
| FU Berlin, TiHo Hannover, JLU Giessen, Leipzig, LMU | Все 5 в поисковом плане; LMUcredentialcorroborated | Полная свежая клиническая сверка5 университетов не доказана |
| AniCura, Evidensia, TAPP, VUK | Сохранены сетевые discovery/rosterleads | Исходные heldclinicalqueues частично утрачены; нет подтверждения branchclinicalполноты |
| filu | Ранее перечислены12 веток | 0 веток подтверждены по онкоуслугам; все12 остаются в87namedlist |
| НезависимыеGP/химиотерапия/хирургия | 4 достаточных проекта, остальные имена сохранены | 61 утраченныйclinicalpayload не восстановлен; частичныеprofessionalreferences не подтверждают лечение |
| RT/ECT/mobile/visiting/remote | Сигналы и конкретные имена сохранены | Местное выполнение, врач и доступ не подтверждены во всём остатке |

Названия16 земель: Baden-Württemberg;Bayern;Berlin;Brandenburg;Bremen;Hamburg;Hessen;Mecklenburg-Vorpommern;Niedersachsen;Nordrhein-Westfalen;Rheinland-Pfalz;Saarland;Sachsen;Sachsen-Anhalt;Schleswig-Holstein;Thüringen. Поисковое покрытие не означает клиническое закрытие ни одной земли.

## Что именно блокирует завершение

Ранее automatic approval review отклонил workflow Evidensiaservices(session1729,837targets) и Clinicalreread(session2322,854targets). BWclinical10(session99412) был отменён. Сохранились ретроспективные receipts этих событий, но не оригинальный полный текст statedreason и не exact1701queue. Поэтому причина отказа неизвестна; не выдумывается ни риск, ни автоматическое разрешение. Блок — на повторение ранее удержанного клинического действия, а не на всю Германию и не на любые новые независимые источники.

Конкретный reviewableостаток — named-87-clinical-recovery.json и18 сохранившихсяclinicalroutesв clinical-URL-review-list.json. Не предлагается одобрить неизвестные1701URL. Для61 утраченного проекта понадобится восстановить точные clinicalsources до повторного запроса. Прямые denialhosts и consentgates сохраняются отдельно и не обходятся.

Отдельные доступные профессиональные/университетские неклинические ссылки могут дополнить имя и квалификацию, но не заменяют обязательные clinicalfacts. Их дальнейшее массовое чтение не закроет национальную онкологию. Нельзя утверждать, что все независимые допустимые источники Германии исчерпаны: завершена конечная offlineсверка сохранённого списка, а не неограниченный новый вебпоиск.

## Точный индивидуальный остаток

| Кандидат | Сохранившийся клинический URL (если есть) |
|---|---|
| Brockhaus Eckernförde | https://kleintierpraxis-brockhaus.de/leistungen/ |
| Nestler Dohna | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Backhaus Thalfang | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| AniCura Krefeld Saumstraße | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Stockelsdorf | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Beck Rossach | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Obermain | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Bencec Linkenheim-Hochstetten | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Callavet mobile service | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Nord-Ostsee Tarp | https://nordostsee-tieraerzte.de/kleintiere/onkologie; https://nordostsee-tieraerzte.de/kleintiere/op_bereich; https://nordostsee-tieraerzte.de/kontakt; https://nordostsee-tieraerzte.de/ueber-uns/praxis |
| Düsseldorf Münsterstraße359 | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Bad Birnbach | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Sewastianiuk Stockach | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Falk Strutz Schwentinental | https://www.kleintierpraxis-strutz.de/leistungen/ |
| Stauferland Rechberghausen | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Wasbek | https://www.kleintierklinik-wasbek.de/willkommen/unsere-leistungen/ |
| Uetersen KleinerSand99–101 | https://www.kleintierzentrum-uetersen.de/leistungen/chirugie; https://www.kleintierzentrum-uetersen.de/leistungen/innere-medizin |
| Schumacher Lammersdorf | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Haag Almenhof Mannheim | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Böttner Blankenese | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Rahnsdorf Gürtler | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Müllheim | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Stahl Menden | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Beyen Hirschberg | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Seffner Bremervörde | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Biet Wanschura Nagold | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Janssen Halle Westfalen | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Olma Zeise Weimar | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Bockenheim Frankfurt | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Britta Richter / Ellund West / im Sonnenschein | https://tierarztpraxisimsonnenschein.de/Leistungen/ |
| Wissenbach | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Pommerening Wolfenbüttel | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Dr Stief Mühlhausen | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Neufahrn | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Westerhorn | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Asterlagen Duisburg | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| AniCura Neu-Ulm | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| KlickVet Quickborn / van Haaren | https://klick-vet.de/leistungen/ |
| Saur Garmisch | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Kruse Bremen | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Valentin Grünheide | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Hoech Saalfeld | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Rondorf Köln | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Arsten Vennefrohne | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| www.kleintierpraxis-preetz-schellhorn.de | http://www.kleintierpraxis-preetz-schellhorn.de/ |
| Altona | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Hänel Hartmannsdorf | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Waschbüsch Saarwellingen | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Weichert Sandhausen | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| praxis-fuer-kleine-haustiere.jimdo.com | https://praxis-fuer-kleine-haustiere.jimdo.com/ |
| ZweitmeinungTierarzt / VetOnkologie one remote intake group | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Bramfeld Hamburg / Gregor Zschoch | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| ClaudiaKellermeier SchwachhauserHeer44/28209Bremen | https://tierarztpraxis-schwachhausen.de/ |
| Ganal Ewert Weingarten | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Fritzenschaf Eggenstein | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Arui Donaueschingen | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Bürgener Wermelskirchen | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Pfeiffer Murrhardt | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Schmidl Bremen | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Wendel Mannheim | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Wiblingen Ulm | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Hoppe & Stech Schenefeld | https://kleintierpraxis-hoppe-stech.de/leistungen/ |
| Büttner Oberhausen | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Anke Wendel visiting service | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Rotenbühl Saarbrücken | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Bungartz Reuth | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Liane Kruse Oesterdeichstrich | https://www.tierarzt-kruse.de/Leistungen/ |
| Rudloff Elzach | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| KielVET Zentrale Elmschenhagen PreetzerChaussee122 | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Grommelt Kehl-Kork | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Itterburg Eberbach | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Ingelheim | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Nord-Ostsee Schafflund | https://nordostsee-tieraerzte.de/kleintiere/onkologie; https://nordostsee-tieraerzte.de/kleintiere/op_bereich; https://nordostsee-tieraerzte.de/kontakt; https://nordostsee-tieraerzte.de/ueber-uns/praxis |
| Sliwon Dormagen | Клинический URL не уцелел; точные reference URL и недостающие факты — в JSON |
| Karin Rieckhoff Rendsburg | https://www.fachtierarzt-rendsburg.de/seite/697815/leistungen.html |
| filu Tierarzt Waiblingen | https://www.filu.vet/standorte |
| filu Tierarzt Berlin Prenzlauer Berg | https://www.filu.vet/standorte |
| filu Tierarzt München Wiener Platz | https://www.filu.vet/standorte |
| filu Tierarzt Hannover List | https://www.filu.vet/standorte |
| filu Tierarzt Hamburg Hoheluft | https://www.filu.vet/standorte |
| filu Tierarzt Berlin Charlottenburg | https://www.filu.vet/standorte |
| filu Tierarzt Frankfurt Nordend | https://www.filu.vet/standorte |
| filu Tierarzt Köln Rudolfplatz | https://www.filu.vet/standorte |
| filu Tierarzt Hamburg Winterhuder Weg | https://www.filu.vet/standorte |
| filu Tierarzt Düsseldorf Pempelfort | https://www.filu.vet/standorte |
| filu Tierarzt München Schwabing | https://www.filu.vet/standorte |
| filu Tierarzt München Theresienwiese | https://www.filu.vet/standorte |

## Даты проверки источников и публикация

Новые sourceattempts этой сверки0; новые successfuldates0; дата интеграции не использована как дата первичной проверки. Диапазоны прежних datesсохранены в per-candidateJSON. Production0 изменений;main0 публикаций;deployне запускался. Researchcheckpoint должен быть сохранён в отдельную remotebranch с обратным чтением до передачи отчёта.

Полнота отчёта не означает полноту страны. До восстановления разрешения для конкретных удержанных clinicalroutes и завершения остатка страна остаётся INCOMPLETE.
