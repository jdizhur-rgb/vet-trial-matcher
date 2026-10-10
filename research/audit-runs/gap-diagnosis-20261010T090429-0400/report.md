Разбор утреннего прохода 10 октября: 108 попыток, 36 fully reconciled, 62 partial, 10 unreachable. Исходные 72 gaps остаются INCOMPLETE.

Причины: 10 недоступных источников; 9 неустановленных полных списков; 3 ограничения свежести; 11 discovery/pipeline/secondary источников, которые ошибочно оценивались как полные recruiting rosters; 39 вопросов по отдельным протоколам, площадкам или статусам. Это классификация сохранённых причин, а не подтверждение полноты этих источников.

Корень ошибки учёта: save_receipt.py присваивает всем processing_complete=True, executor_incomplete=False и внешнюю причину для любого non-fully_reconciled результата. Во многих строках current_roster берётся из предыдущего receipt без индивидуального доказательства сегодняшней сверки. Поэтому заявление «вся работа завершена, 72 внешних блокера» не доказано. Подтверждённые каталоговые изменения этим диагнозом не отменяются.

Исправления: отдельная проверяемая gap-review для каждой причины; unknown completion не считается zero unfinished; roster coverage отдельно от individual protocol uncertainty; справочники/новости/pipeline проверяются по реальным leads; trial pages сетей остаются в scope daily. Строгий receipt gate не ослаблен, исторический receipt и даты визитов сохранены.

Сегодня дополнительно Web-open AVMA public search JSON, CSU trial portal и UC Davis StudyPages: AVMA недоступен через reader, два portal routes возвращают пустой текст. Это не полный новый обход и не доказательство исчерпания public frontend routes.
