# DAILY GLOBAL WORK AUDIT — 27 ноября 2026

**Статус: INCOMPLETE.** Учёт исполнения прошёл (`PASS`), но клиническая полнота не достигнута: 165 источников имеют текущие документированные внешние пробелы, а независимый same-day protocol gate не получил свежего полного разбора для 155 публичных записей.

- Run ID: `daily-20261127T030136-0500`
- Фактическое начало: `2026-11-27T03:02:11.067858-05:00`
- Актуальная база remote-main: `a57183ff6dc9c5ba8970a04556593453f7054be9`
- Опубликованный audit commit: `497c08c3f2e6acc5e8a72dc8d5e99814e42b7821`
- Причина окончания: `completed_available_work` — вся доступная в этом запуске работа выполнена; оставшиеся пробелы требуют внешнего evidence или будущей повторной проверки.

## Основной обход и клиническая проверка

- Источники: 169/169 попыток и индивидуальных решений. До запуска было 168; добавлен один официальный исторический источник NUS.
- Полноценный текущий roster evidence: 4 источника. Внешние пробелы: 165.
- Публичные протоколы: 155/155 попыток; 172 protocol jobs; 138 HTTP-ответов и 34 точных access restrictions.
- Нативный обход источников: 303 маршрута; 249 HTTP-ответов, 52 точных ограничения доступа, 2 transport errors.
- Web fallback: отдельно рассмотрены 35 source URLs и 52 protocol URLs.
- Exact access restrictions: 86/86 решений соблюдены, обходов и необоснованного расширения запретов нет.
- Durable issues: 63/63 разобраны индивидуально; все оставлены `BLOCKED` с текущей конкретной причиной и следующим допустимым шагом.
- Same-day independent gate: 0/155 свежих независимых полных разборов; 155 pending. Это отдельная причина честного `INCOMPLETE`.

## Global discovery

Выполнено 124 отдельных country/language-specific запроса: 48 текущих/без даты, 48 за последние 7 дней и 28 углубляющих запросов для слабых регионов. Широкие запросы не использованы как доказательство полноты.

Новых текущих лечебных протоколов с достаточным protocol-level evidence не найдено. В каталог trials ничего не добавлено.

- Добавлен официальный исторический источник `singapore-nus-msc-5fc-chemoimmunotherapy`: отчёт NUS от 19 января 2023 года об engineered MSC/cytosine-deaminase + oral 5-flucytosine у 65 собак и 2 кошек, начатом в 2018 году. Текущего ветеринарного набора источник не подтверждает, поэтому lead оставлен unresolved/nonmatchable.
- Ghent nanobody fluorescence-guided surgery сохранён как отдельный `PENDING_EVIDENCE`: точный текущий протокол и canonical ID не подтверждены. Он не объединён с закрытым Ghent fluorescence-lifetime исследованием.
- USP perianal page относится к исторической perioperative support работе, а не к новому лечебному trial.
- NTU lead не онкологический.
- Midwestern Glendale совпал с точным существующим canonical ID `midwestern-glendale-canine-cancer-chemotherapy`.
- UF leads сопоставлены с существующими canonical IDs; UNAM — с существующей nonmatchable записью. SNU index не дал нового именованного протокола.

## Сроки набора

Проверены 325/325 canonical записей независимо от прежних deep-review сроков. Исходные даты evidence сохранены. В 43 записях есть опубликованные даты; 3 даты уже пересечены, и все три записи ранее были nonmatchable. Активных записей с пересечённым сроком нет, новых продлений не подтверждено.

## Проверки и публикация

- Canonical catalog: 325 уникальных записей; публичных 155.
- Matcher: 155 записей, из них 152 treatment и 3 treatment-access.
- JS/Python selection, parity (18 600 случаев), catalog loading, build_static_site, matcher logic и production sync: PASS.
- Audit execution gate: PASS; strict receipt: INCOMPLETE с 165 gaps; gap validator: PASS / EXTERNAL_GAPS_ONLY.
- 22 unit tests audit gate: PASS.
- Secret/evidence-key validator: PASS после точечной redaction 64 публично скопированных Google browser keys и пересчёта 128 SHA-256 evidence rows. Evidence не удалялось.
- Preflight: `PASS_WITH_INCONCLUSIVE`; единственная inconclusive проверка — локально отсутствует модуль Streamlit. `safe_to_continue=true`.
- Source inventory validator: PASS, 169 источников.
- Audit commit опубликован в `main`; production matcher прочитан после публикации: USA — 97, Japan — 14 для Dog + “Cancer — any type”.
- GitHub Actions: Full catalog integrity audit — PASS; Check copied evidence keys — PASS; Build and deploy static site — PASS.

Изменений пользовательского текста, UI/CSS/navigation и неоднозначных медицинских решений не вносилось. Онкологические care/services directories не обходились. BluePearl/VCA/Ethos trial pages входили в клинический scope. Outreach не выполнялся.
