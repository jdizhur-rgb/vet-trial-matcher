# Европа: принятые итоги шести исполнителей и подтверждённая публикация

Автор этой сводки и квитанций публикации: /root. Исходные подробные отчёты написаны отдельными исполнителями; они не заменены этой сводкой.

## Итог и доказательства

Проверка рабочего сайта: 18 октября 2026, 01:10:51–01:10:58 America/New_York. Run_id: eu6-recovery-20261018T020312Z. Baseline: 2fed31c822a626339b86d752c49949259de7b1ee.

Данные опубликованы коммитом [329bafe0ff08e2763990e721949454cf275d8b64](https://github.com/jdizhur-rgb/vet-trial-matcher/commit/329bafe0ff08e2763990e721949454cf275d8b64). [Deploy39099590156](https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/39099590156) завершился success; build-candidate, deploy и существующий notify-indexnow завершились success. Внешние формы, письма или сообщения людям не отправлялись. Новый deployment workflow не создавался и вручную не запускался.

[Каталог](https://vettrialfinder.com/matcher/centers/) и [дистанционные услуги](https://vettrialfinder.com/online-oncology-consultations/) дали HTTP200. SHA256 страниц побайтно совпал с локальной полной сборкой:
- каталог:18eb056cb9c47021a9c0cd8f6bc8e62ffec10fbdb446faa8e40b6fb65989f65f;
- дистанционные услуги:24aae291667be79148bea336c8dc42e7bd4d88dcb7fb7375bb8f3b153f9b1c43.

Опубликовано 680 новых записей услуг:645 физических провайдеров, 10 мобильных, 23 сетевых маршрута и 2 veterinarian-only remote services. Это НЕ 680 новых клиник или новых открытий. Исправлено 79 полей у 53 существующих идентичностей. Уже применённых повторно значений:0; четыре NEW Netherlands удержаны. Ранее опубликованные 61 NEW/20 updates сохранены и не посчитаны повторно.

В этом запуске заново обнаружены 50 немецких провайдеров и подтверждено одно текущее изменение существующей платформенной услуги HaustierDocs. Остальные 630 NEW для сайта — сохранённые, ранее не опубликованные предложения, прошедшие восстановление, проверку происхождения, источников и семантической идентичности; они не названы новыми открытиями текущего поиска. Полевая нормализация не считается новым клиническим открытием.

Все шесть независимо приняты research_complete=true до начала интеграции. Собственного доступного остатка у каждого 0; конкретные внешние фактические, URL-access и owner-decision gaps сохранены отдельно. Старые остановки ради интеграции не считались внешними препятствиями. Germany final-28 был возвращён на три конкретных незавершённых направления; принят только final-29 после их фактической обработки.

## Сопоставимые собственные результаты

Assigned/processed/fully_verified — отдельные счётчики исследовательских единиц данного работника, а не универсальное число клиник; aliases, URLs и individual profile hypotheses не суммируются как новые клиники.

|slot / страна|agent ID|assigned / processed / fully_verified|NEW опубликовано|UPDATE идентичности / поля|DUPLICATE|EXCLUDED|UNRESOLVED / внешний провайдерский остаток|
|---|---|---:|---:|---:|---:|---:|---:|
|1 Austria|/root/eu17_at|160 /160 /119|45|30 /51|44|19|22|
|2 Czechia|/root/eu17_cz|153 /153 /105|53|10 /10|45|12|33|
|3 Poland|/root/eu17_pl|366 /364 /240|220|2 /2|18|49|77|
|4 Germany|/root/eu17_de|341 /331 /175|100|2 /7|83|55|101|
|5 France|/root/eu17_fr|725 /662 /190|183|0 /0|8|422|112|
|6 Netherlands|/root/eu17_nl|554 /551 /95|79 из 83 draft NEW|9 /9|10|380|72|

Для всех шести строк: COMPLETE_PUBLISHED_VERIFIED; SHA329bafe0; deploy success; production exact SHA256 match. Квитанции publication-receipt-1.json…publication-receipt-6.json сохраняют отдельные собственные результаты, а publication-ledger.json — их сверенную сумму.

## 1 Austria — /root/eu17_at

[Полный собственный русский отчёт](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/bb4c0f3d79c5b07528ebd9351d62876e1e49c7cc/research/audit-runs/eu6-recovery-20261018T020312Z/worker-1/checkpoints/block-03-final/report.md).

Покрытие всех 9 федеральных земель, университетского направления, rosters Veterinaria19/AniCura6/TIERplus6/IVC2, независимых и обычных клиник, мобильных/remote маршрутов и новых сигналов проверено по сохранённому национальному пакету.45 NEW состоят из 43 физических, одного мобильного Angerer и одного сетевого Stiglhuber.51 UPDATE у 30 существующих идентичностей. Текущих новых discovery/source visits:0; унаследованное не переименовано в новую находку.

Именованные примеры: Tier&Arzt Covi/Dijkhuizen, Innsbruck — подтверждённое local oncology care, https://tierundarzt.at/medizin/; Stefan Lorenz, Mistelbach — cancer surgery, https://tierarzt-lorenz.at/chirurgie/. Surgery не расширена до chemotherapy/ECT без доказательства. Anif не получил ECT по общей хирургической странице.

Собственный доступный остаток 0. Внешние 22 провайдерских вопроса и 3 modality/reference gaps: в частности Stadtgraben/Wolfheld — building coordinates неизвестны, а не отсутствие лечения; Fürst Bregenz — held service/team scope, без обновления даты по failed read; Hutter ECT и gated ÖTK reference не превращены в доказанную услугу. Полный именованный список и допустимые следующие шаги — в отчёте и remaining.json.

## 2 Czechia — /root/eu17_cz

[Полный собственный русский отчёт](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/bb4c0f3d79c5b07528ebd9351d62876e1e49c7cc/research/audit-runs/eu6-recovery-20261018T020312Z/worker-2/checkpoints/normalized-final/report.md).

Проверены 14 краёв и 9 национальных направлений;130 сохранённых query records не названы текущими новыми запросами. В текущем восстановлении выполнены 3 официальных чтения Horky; новых клинических значений 0.53 NEW:51 физический провайдер и 2 сетевых маршрута;10 полевых UPDATE. Сетевые BUDvet и Veterina Výjezd не размножены на предполагаемые локальные филиалы.

Примеры: RPVET Plzeň — surgery, https://rpvet.cz/o-nas/sluzby/; Vetplzeň/Zahrádka — surgery, https://www.vetplzen.cz/index.php?id=50&option=com_sppagebuilder&view=page. Clinician/access aliases технически приведены к действующей схеме без клинической догадки. Неизвестные координаты и 12 неподтверждённых physical postcodes не выдуманы.

Доступный собственный остаток 0.33 внешних провайдерских вопроса плюс 2 existing-field gaps: Procházka Olomouc — точный approval-denied URL не обходился; VetPark Stará Boleslav — referral не доказательство local treatment; Vítkovice — текущая роль не опубликована; Mělník не получил чужую географию Brno. Transport timeout не переписан как 403 или successful check.

## 3 Poland — /root/eu17_pl

[Полный собственный русский отчёт](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/bb4c0f3d79c5b07528ebd9351d62876e1e49c7cc/research/audit-runs/eu6-recovery-20261018T020312Z/worker-3/checkpoints/block-6/report.md).

Все 16 воеводств, 8 университетов, 13 rosters, independent/GP cancer treatment, RT/ECT/mobile/remote и новые сигналы отражены в национальном покрытии. В этом восстановлении реально выполнены 16 региональных польских запросов, 46 просмотренных результатов и 15 чтений URL/14 провайдеров; новых клинических предложений не добавилось.220 retained NEW:211 physical, 7 network, 2 mobile. Два UPDATE — Onkovet Gliwice access note о Stelfonta и квалификация Szpunar в ZWIERZAK Rzeszów: veterinary surgery specialist, не oncology-board credential.

Примеры: Vet4Pet Warszawa — local oncology/cancer surgery, https://www.vet4pet.pl/specjalizacje/onkologia; SpecVet Mokotów, https://specvet.pl/mokotow/. Разные доказанные площадки SpecVet с общим телефоном не слиты; Therios не получил chemotherapy/radiation из Surgery/ECT.

Доступный собственный остаток 0. Внешних вопросов 77:75 обработанных неоднозначностей и 2 недоступных routing candidates, а не 77 готовых клиник. Для UPWr сохранено, что точный ранее ограниченный URL неизвестен; пути не угаданы. Отмечено guard deviation: общий query вернул held LuxVet master excerpt. Он не использован как primary clinical evidence, body не восстановлен, ограничение не объявлено снятым.

## 4 Germany — /root/eu17_de

[Полный собственный русский отчёт final-29](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/bb4c0f3d79c5b07528ebd9351d62876e1e49c7cc/research/audit-runs/eu6-recovery-20261018T020312Z/worker-4/checkpoints/final-29/report.md).

Пройдены 16 земель, 21 крупный город, университеты, независимые/GP, branch rosters, mobile/visiting/remote, RT/ECT и текущие/новые сигналы.391 фактическая попытка доступа, 441 URL/title routes — не 441 клиника.341 provider/service questions и 175 fully verified учитываются отдельно от 17 individual clinician profiles.100 NEW:89 physical, 5 network, 6 mobile;50 из них — текущие новые находки, 50 — унаследованные неопубликованные. Две UPDATE-идентичности/7 полей:2 credentials-поля LMU и 5 полей существующей HaustierDocs service.

Примеры: AVETIA Dresden — cancer surgery и chemotherapy, https://avetia-dresden.de/leistungen/onkologie/; Barleben — surgery и прямо заявленные simple chemotherapy protocols, https://www.tierarztpraxis-barleben.de/leistungen/. Vetmed visiting surgery требует записи через receiving GP; receiving units не размножены в клиники. Grünberg-Klein с mobile-словом в бренде классифицирован по фактическому месту операции, не названию.

HaustierDocs остался ОДНОЙ услугой, не 17 NEW: проверены все 17 профилей, различены Popa/Walther Premium, Reuter second-opinion routing, Lasar Standard/Premium follow-up. Квалификация Popa не повышена до oncology board. Nataliia Ignatenko/LMU credentials проверены отдельно от новых modalities.

Собственный доступный остаток 0. До приёмки дополнительно фактически разобраны Fries-Jung→Döhrener Dorftierarzt, Jensch→новый advertised host и Bolia. Owned-source502/503 и отсутствие первичного allocation mobile oncology сохранены как конкретные внешние факты, без NEW/FULL или ложного 403. Внешних provider/service gaps101 плюс 11 clinician-profile hypotheses.17 реально наблюдённых 403 имеют точный отдельный scope; утраченный scope не снят и не распространён на всю Германию.

Guard deviation Krefeld: новый домен раскрыл известную held AniCura/Saum5–8 identity. Доступ прекращён; clinical body/quote/hash, NEW/FULL и successful-date credit не использованы. Metadata-only retrospective audit не разрешал повторный доступ. Непрочитанная сессия HomeVet с collision прежнего ID не опрашивалась.

## 5 France — /root/eu17_fr

[Полный собственный русский отчёт](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/bb4c0f3d79c5b07528ebd9351d62876e1e49c7cc/research/audit-runs/eu6-recovery-20261018T020312Z/worker-5/checkpoints/normalized-final/report.md).

Покрытие 13 metropolitan regions, 5 DROM, overseas directions, 15 cities, 4 universities и 54 coverage rows восстановлено с 159 dependency/103 operational/149 safe input hashes. Rosters Sevetys247/Argos116/Fovea48/VPlus34/Synervet COM16 рассматриваются по собственным evidence; потерянные AniCura/VetPartners master payloads не названы заново полностью прочитанными.416 query records — не 416 новых запросов текущего запуска; текущих source visits/discoveries/clinical deltas0.

183 retained NEW:178 physical, 1 mobile ArriAVet, 2 network и 2 veterinarian-only tele services. UPDATE0. Пример local oncology care: Sainte-Anne, Sorgues, https://www.veterinairesainteanne-refere-urgence.com/nos-specialites/oncologie-cancerologie/. Olliolis tele-expertise, https://referentsolliolis.fr/tele-expertise.html — только ветеринары, signed specialist report; Mathilde Lajoinie не объявлена автоматически назначенным reviewer. Doliger remote case review, https://cancerologie-veterinaire.com/contact/ — veterinarian-to-veterinarian, не owner video и не выдуманная board credential.

Собственный доступный остаток 0.112 внешних/условных провайдерских вопросов:49 обработанных и 63 не прошедших доступный разрешённый маршрут. Corniche Toulon/Saint-Max held; LesVet Lesneven current role не опубликована; Calypso Aubagne branch allocation неоднозначен, а не доказанное отсутствие лечения. Salève palliative editorial decision удержано.6 genuine missing query responses не переписаны в 27; raw/cancelled/denied payloads не реконструированы.

## 6 Netherlands — /root/eu17_nl

[Полный собственный русский отчёт](https://github.com/jdizhur-rgb/vet-trial-matcher/blob/bb4c0f3d79c5b07528ebd9351d62876e1e49c7cc/research/audit-runs/eu6-recovery-20261018T020312Z/worker-6/checkpoints/block-03/report.md).

Проверены 12 провинций, 17 городов, BES, Utrecht, AniCura85, IVC220/owner-finder237 и BestCare21.596 manifest payloads/67 core dependencies и 277 retained query records не выданы за новые посещения/клиники;5 internal missing responses явно сохранены. Текущих клинических открытий/изменений 0.Из 83 proposed NEW опубликовано 79:73 physical и 6 network;9 существующих идентичностей получили 9 полевых исправлений.

Примеры: VCNN Noordwolde — cancer surgery, https://veterinaircentrumnoordnederland.nl/behandelingen/; DGC West Dronten — surgery, https://diergeneeskundigcentrumwest.nl/dierenartsenpraktijk/. Названия сетей не создали неподтверждённых адресов branches.

Четыре NEW удержаны: DC Zeeland Noordwelle — заявленный отпуск 16 октября–6 ноября; De Wagenrenk — no new oncology patients; Goudenregenstraat и De Duinen/Arnoldspoelstraat — текущая персональная роль не подтверждена. Их нельзя автоматически опубликовать после наступления даты. Неопубликованное изменение Elze Surgery также не применено: прежнее Local oncology care сохранено.

Собственный доступный остаток 0.72 внешних вопроса:69 обработанных и 3 недоступных; Vught403, SEAWF St Eustatius current visiting cancer care/clinician, De Langstraat Waalwijk/Van Kop tot Staart Hoorn — отдельные причины и scope в отчёте. Три старые dependencies отсутствовали в прежнем backup082, но реально сохранены в текущих backups002–004; история не переписана.

## Исправления причин прежней потери и контроль сохранения

Использован отдельный remote research branch research/europe-recovery-eu6-recovery-20261018T020312Z, без PR/merge в main и без deploy от research push.27 последовательных checkpoint archives; семантические блоки и URL restrictions сохранялись во время поиска. Последние данные checkpoint027:2c44d4ab540778e5223fbeb897c4842b8956a2b6, receipt:dfa2049bc2de695c9f859ff56618ed6decaf7532, exact-readback commit:c0df010561283c50ca24c79a7a403eb4a8e25e7e. Только 16 изменённых phase-two code/state/proof files добавлены в последнюю копию, а не повторные полные payload snapshots.

Actual cold restore001–025 в пустую директорию прошёл archive/member/reconstructed-file SHA checks. Последние 26/27 не добавляют новых worker payloads; их code/state/readback подтверждены отдельно. Секреты, .git и ненужные полные копии сайтов не включались. Утраченные старые девять controller receipts и старые чаты не реконструированы.

Все шесть реальных исполнителей наблюдались одновременно RUNNING17 октября 22:13:28 America/New_York. Точные индивидуальные spawn timestamps, недоступные после восстановления, не выдуманы; отчёты сохраняют известные периоды и границы.

Командный git push не получил Username; использован уже подключённый GitHub tree/commit/ref channel с expected SHA и force=false. Перед каждым страновым пакетом и перед обновлением main выполнен ограниченный по времени fetch. Remote readback37 файлов, точное множество изменённых путей и единственный parent2fed31c8 подтверждены. Посторонние main-файлы сохранены.

Офлайн полная сборка, care/schema/identity/network/filter/source-date regression, evidence-key checks, matcher loading/selection/protocol/logic и production-sync прошли. Baseline preservation regression хэшами подтверждает сохранение старых 901 public, 893 supplemental, 977 inventory rows и 64 tele rows после обратного вычитания только разрешённых изменений.78 конкретных reviewed distinct-site pairs не заменены правилом «разный ID — всегда другой провайдер». Synthetic same-branch different-ID dedupe продолжает работать.

Состояние слотов обновлено после приёмки всех шести: исторические receipts/follow_ups сохранены; current own remaining отделён от external gaps. У Poland/France cursor0→1 после завершения, у остальных уже 1 не увеличен повторно. Другие страны в этом запуске не назначались. Устаревший state pointer на RUNNING не принят за реальную активность. Новые автоматизации/дочерние субагенты не создавались; старые Europe/Weekly и утренний trial audit не изменялись.

Это завершённый фактический результат. Фонового продолжения после сообщения не заявляется.

