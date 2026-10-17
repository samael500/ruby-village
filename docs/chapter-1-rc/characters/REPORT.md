# Рута: пилот #35 и независимый runtime #36

База add7670; ветка art/35-characters. AGENTS, #43/#35/#36 и ART.md из открытого PR #38 прочитаны. Общие main/style/camera не изменены.

## Конкретный результат

Новый прозрачный модельный лист `art/characters-v1/ruta-pilot-sheet.png`, отдельный полный рост, настоящий крупный бюст и вид со спины в `public/assets/characters-v1`. Это **новые** материалы built-in imagegen по доступному утверждённому `public/assets/level-1/v4/ruta-idle.png`, не восстановленные ZIP. Полный prompt сохранён в SOURCE.md. Архивы ruby-village-characters-v1.zip / ruby-village-animations-v1.zip отсутствуют в доступном дереве.

`reference-comparison.jpg`: исходник слева, новый пилот в центре, бюст справа. `alpha-light/dark/green.jpg`: реальная компоновка RGBA поверх трёх фонов. У пилота сохранены волосы, голубые глаза, платок на шее, один ремень, оливковый жилет. Лист имеет настоящую alpha (0–254). Разделение выполнено по связанным компонентам alpha воспроизводимым `art/characters-v1/extract-pilot.py` (Pillow). Ни один кадр ходьбы независимо не генерировался.

Актуальный художественный статус: **внешность Руты принята Максимом через координатора**. Новые позы и жители переданы отдельным продолжением в residents/REPORT.md. Исторический статус первого пилотного этапа ниже не означает повторного запроса внешности. Принята внешность статичного пилота; новая постановка/ходьба проходят отдельную проверку. В полном росте вид несколько более фронтальный, улыбка/форма лица чуть отличаются от исходника; сравнение намеренно оставлено явным. Задний вид — исследование дизайна, не риг и не доказательство согласованности шести направлений.

## Runtime и проверки

`src/character-animation.ts`: отдельные контролируемые часы, pause/resume без скачка, reduced motion, contact events с earth/stone/wood, гистерезис направлений в проекции, перемещение по длинам сегментов. Модуль пока не подключён к production: он не изображает несуществующую финальную ходьбу.

Node v24.15.0: 55/55 tests проходят, включая 4 новых содержательных проверки; tsc --noEmit и Vite production build проходят. Нужен PATH к `/home/mskorokhod/.ya/tools/v3/14019382748/bin`; node_modules локально связан с основным checkout, ссылка не коммитится.

## Оставшиеся блокеры

- Внешность пилота принята; нужна проверка новых поз/жителей в настоящем дворе desktop/844×390 интегратором. Точка стоп/136 px — предварительная ручная калибровка, не утверждённая в сцене.
- Продолжение: технический .blend/риг/цикл сохранён отдельно в PR #59, а painted-позы — в residents/REPORT.md. Финальная рисованная ходьба ещё не готова.
- После принятия пилота шесть жителей и настоящие бюсты произведены; см. residents/REPORT.md. Их отдельная художественная приёмка ещё не заявлена.
- Нет видео походки/пролога, нет проверки телефона или семейного теста. Эти пункты не выполнены.

## Review decision 2026-10-17

Maksim explicitly accepted the pilot appearance in chat: «Принять внешность пилотной Руты». This approves appearance for subsequent poses and walking. Frame stability, foot anchors, six directions, rig/cycle and in-game motion remain separate pending checks. No production walking is implied.

Maksim explicitly authorized all six residents/portraits and acting poses for the integration review build: «Включить комплект в игровое ревью». No main merge or publication is authorized.
