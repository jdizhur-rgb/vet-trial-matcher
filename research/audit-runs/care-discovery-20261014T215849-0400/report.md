Пакет Канада/Европа, начат 14 октября 2026.

| Территория | Обработано | Полностью по полям | Новые очные | Новые remote |
|---|---:|---:|---:|---:|
| Ontario | 10 | 5 | 7 | 0 |
| United Kingdom | 10 | 8 | 8 | 1 |
| Quebec | 10 | 4 | 7 | 0 |
| Germany | 10 | 7 | 8 | 0 |
| France | 10 | 7 | 10 | 0 |
| Netherlands | 10 | 4 | 6 | 0 |

Итого: 60 обработано, 35 полностью проверены по предусмотренным опубликованным полям; 46 новых очных + VOS удалённо. У 12 опубликованных карточек остались конкретные вопросы: в них только подтверждённые услуги/поля. 13 кандидатов не опубликованы: адрес/актуальный врач/локальное лечение/источник не подтверждены в достаточной степени. Это не вывод о закрытии или отсутствии услуги. Все 25 неполных записей имеют конкретные вопросы и URLs, recheck_after 2026-10-21; причины и разрешённые дальнейшие шаги см. results.

39 новых непроверенных находок сохранены. Обработанные первоначальные UK/Ontario leads сняты с unprocessed, включая альтернативные названия и старые news/form URLs; нерешённые перенесены в pending. Каждая страна/территория остаётся частично исследованной, полного покрытия нет. Следующий пакет: существующие очные записи, мобильные/приглашённые службы и телеконсультации, до пяти записей на исполнителя; приоритет давним проверкам и подошедшим конкретным вопросам.

Проверки PASS: care schema, IDs/semantic dedupe, сохранение всех 527 прежних inventory и 447 supplemental записей, A01/A02/B01/B02/C01/E/six regressions, static build, production sync, evidence-key scan. Main изменился параллельно: сохранён отдельный morning source audit 936416e8, после rebase сборка повторена. Clinical-trial research в этом care-пакете не проводился.

Публикация: первоначальный пакет 638ed421; финальная точность тега Oncovet a20006ecc9ce74ec96a1a06c691c5ed2454832fa. Услуга medical oncology подтверждается отдельно от квалификации врачей. Build/deploy/IndexNow PASS: https://github.com/jdizhur-rgb/vet-trial-matcher/actions/runs/38706613432. Обе production-страницы https://vettrialfinder.com/matcher/centers/ и https://vettrialfinder.com/online-oncology-consultations/ имеют точное SHA-256 совпадение с проверенной сборкой; hashes и фактические readback timestamps в production-readback.json.

Даты проверки источников: total inventory 574; attempted published sources 47; remote-verified 47 — PASS. 22 фактических exact successful timestamps и 25 date-only reviews, даты 2026-10-14—2026-10-15 (UTC/date precision явно указаны в evidence). Для новых source rows before_last_checked=null; прежние source dates не обновлялись. Дополнительно сохранены все 60 candidate reviews; unprocessed leads не получают successful review date. Родитель открыл 46 primary service URLs: 44 успешных, два последующих 502; исходные успешные worker evidence Cambridge/Laval сохранены, не заменены временем неудачной попытки.
