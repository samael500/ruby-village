# UI / пролог: пакет интеграции #48, #47

База `add7670` плюс #44 (`3578e89`, `d5378e9`). Владение: `src/chapter-ui.ts`, `src/prologue-staging.ts`, `tests/chapter-ui.test.ts`, этот каталог. Общие main/style/camera не изменены. Источник реплик — существующий `prologue.ts` и HANDOFF; сюжет не переписан.

## Контракт координатору #46

- `chapterMap(completed)` возвращает восемь мест: state, disabled, label и connectionRestored. Последнее означает восстановленную связь между двумя пройденными местами, а не просто доступность следующего. Использовать label как aria-label, disabled как настоящее button.disabled. Старая отдельно сохранённая победа mill остаётся replayable, но не открывает разрыв прогрессии.
- `continueTarget(completed, savedSession?.levelId)` выбирает валидную доступную сессию, затем первое непройденное место. Завершённая глава возвращает двор для replay; sandbox поддерживается. Этот модуль не запускает пролог: сначала применять существующий shouldStartPrologue.
- `learningHint({levelId,mode,selected,placed,rotated,hasBridge,bridgePlaced})` возвращает одну актуальную подсказку либо null. Вызывать после выбора/размещения/поворота и смены режима. Вывести text через textContent в status. bridgePlaced считать по реальной фигуре bridge на поле; rotated означает действие пользователя в текущей сессии. Подсказки не требуют израсходовать лишние плиты.
- `chapterCompletion`: DOM-текст финала и три допустимых действия map/replay/letter. Кнопку главы 2 не создавать; invitation доступно для повторного чтения.
- `stagedPrologueFrame(index)` объединяет точную реплику с постановкой. Только DOM-текст; backDisabled у первого кадра, next у последнего «К калитке». UI пазла скрыт на всех шести кадрах.

## Контракт ресурсов

`staging.scene` gate/garden использует ту же production-сцену и camera manifest, что пазл. anchors `start`/`goal` берутся из scene manifest; `loose-stone` должен быть предоставлен окружением. В кадре 6 camera=gameplay и ruta anchor=start — никаких собственных координат или изменения масштаба вместо позы. `wide` — согласованный широкий вариант камеры той же сцены. Actors/poses: ruta basket-hold/surprised/crouch/idle; rabbit baking. Props: basket-apples, basket-ground, loose-stones, table, bowl, spoon. Road intact только до обнаружения пропажи, missing в кадрах 4–6; скрыта в саду. Не рисовать гексы в прологе. Reduced motion: статическая конечная поза, без обязательной анимации.

Ни один идентификатор не означает, что финальный asset уже готов. Отсутствие художественно принятого двора/Руты/поз блокирует финальную интеграцию. Существующие SVG не названы финальным контентом. Рассказчик остаётся без портрета через speakerPortrait.

## Проверки и ограничения

Добавлены поведенческие тесты: sparse legacy completed, недоступная saved session, replay завершённой главы, подсказки select/drag/rotate/bridge, шесть кадров и точный handoff. Browser evidence будет достоверно только после подключения модулей координатором к production runtime; этот пакет не выдаёт тест pure functions за UI-приёмку.

Not-run: художественная приёмка, шесть целевых viewport, реальный touch/portrait, телефон, семейный тест, полное production-прохождение. Требуются реальные снимки new/saved меню, new/partial/complete карты, обучения/лотка, паузы/письма/финала и шести кадров; видео перехода к пазлу после ресурсов #35/#45.

Проверено 2026-10-17: Node v24.15.0; 62/62 tests pass; `tsc --noEmit` pass; Vite production build pass (JS 81.36 kB / gzip 27.04 kB, CSS 16.01 kB / gzip 4.42 kB); `git diff --check` pass. Эти размеры включают staged #44 и не являются окончательным бюджетом RC.
