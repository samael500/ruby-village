# Актуальный checkpoint — 18.10

Эта таблица заменяет противоречащие ранние статусы ниже. Интеграция2fe65f4/151efd4, production layout1 остаётся, main add76709 не менялся.

| Замечание | Статус | PR / проверенный commit | Доказательство |
|---|---|---|---|
| #61 invalid release→rotate valid→auto-place | Исправлено, независимые mouse/touch и cancel/undo/save PASS | #55/#64 f2a3600,c385b22,38706d6 | evidence/rotate-place; qa/map-rotation-f2a3600 |
| #62.1 Rabbit/table | Native candidate: целая яблоня, один соразмерный стол, full-alpha FREE0; wide/game pending | #68 f1e8ea2 | art/garden-well/GARDEN-NATIVE.md; source proof, не игра |
| #62.2 story stones | Увеличены18→32, текущие игровые кадры проверены; финальный арт повторить | #55 | evidence/prologue-stones |
| #62.3 story field | Полностью скрывается; сюжетные камни сохраняются | #55 5dc2036 и независимый467eab2 | qa/residents-bridge-audio-467 |
| #62.4 walk | Пользователь требует MPFB. Genuine model/rig/IK технически работают; лицо/волосы не похожи на принятую Руту, отклонены;24-позный motion-study не финальная ходьба | #69 source25690fa, #71 source24315ea | MPFB head comparisons и motion strips/actual loop в этих ветках; production не активирован |
| #62.6 stream/mill bridge | Exactmask/source guards, actualstream pilot functionalPASS; ARTNOTREADY P1 steppedbank, P2 flatroadedge | #70/#55 8a584f2,2fe65f4,151efd4 | qa/stream-road-c64b249 clean/overlay/crops/actualinputAV; separate reviewed-only branchc64b249 |
| #62.7 map | Native painted paving, registeredwide, independent navigation/reload PASS; финальная глава повторить | #55 f2a3600,c385b22 | evidence/painted-map-runtime; qa/map-rotation-f2a3600 |
| #62.8 results | Текущее место/реальная дорога/жители, старые8 independentlychecked; финальные сцены повторить | #55 | qa/residents-bridge-audio-467, qa/f1-recheck-ff60cb1 |
| #62.9 residents + facing | Шесть жителей в сценах, восемь authored views, event-driven facing; найденное millF1перекрытие исправлено и независимо перепроверено | #67/#55 0ad8c40,ff60cb1,27d8ecc | qa/facing-header-0ad8c40 и qa/f1-recheck-ff60cb1:2 normalroutes/allarrivalpages/replay/reload, overlap0 |
| Header emblem | Уточнён пользователем top icon/title; painted ruby plaque+live title,24 realconfigs independentlyPASS | #55 b2ac3c8,25fcc96 | ui-header/before-after-phone.png; qa/facing-header-0ad8c40/headers |
| Clean sound | Шумовой слой удалён без сниженияmaster, Максим «Шипение исчезло» | #55 51e15d5 | audio-noise matchedRMS+actualWebAudio gameAV+userlistening |

Source masks/Blender renders не заменяют игру. Scope stream pilot явно НЕRC: только отдельная веткаreview/46-stream-road включаетlayout2streamдлялокальногоревью; production gate интеграции остаётся целиком закрыт. IndependentQA подтвердил clip/ownership/edge topology/input/save, но указал P1/P2 — художественно готовым не объявляем. Реальные audio/video сохранены с явными ограничениями A/V alignment, без вымышленного humanlistening. Physical phone/family и финальная #37/#49 NOT RUN.

---

# Приёмка замечаний #61 и #62

Прочитаны координатором 17.10.2026 на интеграционном commit `16f6e54`.
Источники: https://github.com/samael500/ruby-village/issues/61 и https://github.com/samael500/ruby-village/issues/62.
Обновление: интеграция063bb19 и неактивный art handoffbe6831f. Доказательства ниже различают проверенный legacy runtime и ещё не включённое финальное оформление.

| Пункт | Владелец | Состояние / необходимое доказательство |
| --- | --- | --- |
| #61 invalid drop | #61 автор + координатор; независимая qa_runtime | Интегрирован f7aac88; независимый runtime проверил mouse/touch, single/composite/bridge, cancel/undo/reload. Дополнительный touch-adapter063bb19 исправляет пропуск первого быстрого нажатия послеdrag:6/6 повторов,48/48 быстрых касаний, Enter/Space/mouse PASS; независимый повтор адаптера выполняется. evidence/TOUCH-RELEASE.md, qa/GROUNDED-RUNTIME-REPORT.md. |
| #62.1 Кролик и стол | art_scenes + интеграция | Поза с baked-столом убрана из пролога, но масштаб единственного стола на финальном фоне ещё исправляется. Открыто. |
| #62.2 камни | интеграция #47 | Сюжетные камни увеличены18→32 без изменения логики; actual desktop/landscape evidence/prologue-stones. Повтор на финальных сценах обязателен. |
| #62.3 скрытие поля | интеграция #47 | Runtime и независимая проверка: техническое поле/controls display:none; сюжетные камни остаются. После победы технические слои также убраны5dc2036, все8 результатов проверены. |
| #62.4 ходьба | motion автор + интеграция | Подключена настоящая phased gait со стартом/остановкой, semantic footsteps и паузой при portrait. Независимые8 маршрутов19.2–24s,4 игровых направления;6 исходных направлений отдельно. Реальные AV в evidence/grounded-game и независимой qa. Финальные фоны требуют повторного прохода. |
| #62.5 invalid drop | #61 | См. #61; финальная независимая проверка быстрого touch выполняется. |
| #62.6 мосты | art_scenes + интеграция #46 | Рисованный деревянный мост и реальные hit-cells подключены, desktop/landscape evidence/painted-bridge. Точные берега новых stream/mill ещё не прошли; финальная совмещённая проверка открыта. |
| #62.7 карта | интеграция #48 + art owners | Рисованные тропинки и чароитовый прогресс подключены; реальные map captures имеются. Gate/bakery/post/forest map-match cores сохранены неактивно; оставшиеся объекты/стыки требуют художественной проверки. |
| #62.8 результаты | интеграция #48 | Общая completion-gate картинка заменена snapshot текущей сцены и фактической дороги. Независимая проверка всех8 PASS, включая скрытие технического фона5dc2036. Жители появятся одновременно с финальными сценами. |
| #62.9 жители | art owner anchors + интеграция | Спрайты/портреты готовы и приняты для игрового ревью; native-anchors runtime готов, но полные жители в сценах ещё не активны. Состав: rabbit/teacher/baker/squirrel/miller+squirrel/hedgehog. Финальная геометрия/grounding открыты. |

Для каждого пункта сохранить конкретный commit, screenshots desktop/landscape и для движения/drop видео реального ввода. После общей интеграции независимая #37 повторяет весь список на production build; #49 не считает эти пункты завершёнными до доказательств. Исходные пользовательские вложения из issue локально недоступны: не выдавать чтение текста за просмотр этих изображений. Телефонная эмуляция не заменяет настоящий телефон; семейный тест остаётся NOT RUN.


## Последнее уточнение и новые runtime-исправления

Последние требования в LATEST-REQUIREMENTS.md заменяют противоречащие ранние формулировки.

| Пункт | PR | Commit | Фактический статус и доказательство |
| --- | --- | --- | --- |
| #61/#62.5 | #64, #55 |063bb19, независимыйb0a65af|8/8 rapid-touch,10/10 full regression,48taps PASS; qa/touch-release-063. |
| #62.4 | #60, #55 | текущие mesh кадры отклонены | Технические проходы остаются доказательством контроллера, не художественной готовности. Новый целостный pilot и немного более быстрый согласованный шаг в работе. |
| #62.7 | #53, #55 | новая иллюстрация в работе | SVG-бусы/пунктир не отвечают уточнению. Нужен плотный рисованный плитняк внутри изображения, сохраняющий объекты карты. |
| #62.9 | #55 |498d069 +3d24558|Жители активны в текущих сценах; Кролик заземлён рядом со столом.12 desktop/landscape scene runs: dialog/puzzle/replay/reload/result PASS;7 full alpha/polygon clearances0. evidence/residents-runtime. Независимый итоговый повтор ещё нужен. |
| #62.6 | #55 |f121bc7 + неактивный36f94a6|Трёхгексный игровой мост, пары stream/mill с водной маской/без, actual placement/results PASS наlegacy. Принятые новые водные маски переданы, художественные берега ещё не финальны. |
| Чистый звук | #55 |51e15d5|Удалён непрерывный шумовой слой из атмосфер; music/SFX/master не менялись.29-file audit, matched-RMS stems и43.677s actual browser AV. audio-noise. Субъективное прослушивание и итоговая независимая проверка открыты. |

Финальный RC не подтверждён. Неактивные новые сцены должны пройти совместную художественную/геометрическую проверку и включаться сlayout2 атомарно. Реальный телефон/семейный тест/прослушивание не подменяются Chromium и измерениями.

User audio review: Maksim explicitly confirmed «Шипение исчезло» in the recommended comparison (51e15d5). Steady-hiss complaint resolved by user listening; final integrated loop/transitions and physical device remain separate checks.
