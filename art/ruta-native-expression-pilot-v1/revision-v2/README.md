# Revision v2: только native brow controls + исходно открытые глаза

ОДИН новый static trial после отклонённого sleepy v1. Frozen parent09ac неизменён. Рецепт native face_default→eyemask_content→mouth_smileclosed2; затем65%eyemask_relaxed ТОЛЬКО для allowlist108channels `pose.bones["…Eyebrow…"].location/rotation_euler/scale`; затем прежние35%mouth_smileopen. Все eyelid/eye/прочие channels relaxed пропущены. Фактический allowlist и native дельты — derivation.json; никаких произвольных vertex cap/масок для сокрытия результата, новой faceUV/AI/перемасштабирования головы нет.

## Проверка разделимости и честное ограничение

Строгая первая проверка «ноль ВСЕХ eyelid-weight vertices» НЕ прошла: region16nativeDEF-Eyelidgroups с totalweight>.05 содержит1831вершину,994изменены, max0.822130mm в оригинальном Ellie (~1.109mm в Руте). Это overlap весов в переходной коже бровь/веко. Root явно разрешила такой малый естественный overlap для отдельного trial, не требуя искусственного обрезания координат; НЕ заявляем exactpreservation всей кожи век.

Допроверка original evaluated native topology/weights:128boundaryvertices с eyelidweights — deltaEXACT0; highweight>.95region378vertices EXACT0; >.8region826vertices max1.460µm native. Это сохраняет проверяемую eye-opening boundary, а не вывод из bbox лица. Абсолютная ширина/высота зрачка не подгонялась. Eye globes L/R, highlights, eyelashes, face_lines также EXACT0. Реальная вертикальная граница отверстия глаза не изменена; изменение выражения бровей не выдается за новое движение глаз.

Head-face max30.872mm (в основном mouth), eyebrows14.708mm, верхние зубы8.138mm, нижние25.870mm, язык33.133mm. Эти крупные mouth pose дельты по-прежнему UNCERTIFIED; одно фото не заменяет collision/всеракурсную проверку. Ничего не клиппировано по величине.

## Cold и один actual render

Сначала cold-check:50fullkey+handle actionhashes, boneREST/rigmatrix/camera,15packedimages, topologyUVweightsmaterialslotsrenderVisibility exact; все nonfacialcoords, crown и protectedneck ниже1.18 exact. Явный исторический headfit+up20 baseline mappingmax0.235µm; новый fit/масштаб не вычислялся. Исходные09ac/b14/sourceEllie неизменны; готовая модель в ignoredcache воспроизводима derive.py.

После согласованного свободного render-slot npc_facing, выполнен РОВНО ОДИН frontWalk0 yaw0 Eevee32AA512×640,5.92s. baseline-front00.png — byte-exact исходный128AA00; разноеAA не позволяет выдавать полный pixel-diff за чистую дельту выражения. front-before-after.jpg и общий3×nearest face crop — только review, no anatomy registration. Renderer jobs завершены; no48/runtime.

Наблюдение: глаза снова открыты как baseline, сонный верхний край v1 отсутствует; улыбка с зубами и более спокойные брови остались. Это конкретный кандидат, НЕ художественная приёмка, не доказанное каноническое сходство и не готовая разговорная лицевая анимация. Весь цикл/направления/intersections ещё не проверялись.
