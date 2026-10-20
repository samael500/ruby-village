# Один native facial-expression пилот — не художественная приёмка

Parent frozen09acadc1f01d1abb940723c80b8fdbd357553aa9cf8be09f7e7d225ea4b1715d, original combined b14 не изменён. Оригинальный официальный Ellie rig сохранён в существующем source/ellie-original.blend SHA3dd23521…; общие scripts/ruta-ellie-head.py и source не редактировались. Новых faceUV/AI-изображений, изменений кроны/размеров головы/глаз, скелета тела и походки нет.

## Проверенные родные controls и один рецепт

Текущая Рута УЖЕ заморожена из Ellie `face_default → eyemask_content → mouth_smileclosed2`; поэтому повторное применение тех же pose-assets не будет новым исправлением. `inventory.py` читает реальные action curves/контролы исходного RIG-Ellie; native-controls.json содержит имена/количества и отличающиеся channels. Полный7MB inventory воспроизводим в ignoredcache, не дублирует весь риг в PR. Scripts autoexec отключены; использован тот же evaluated subdivision1..2, что при исходном извлечении.

ОДИН trial: поверх ровно этого baseline интерполированы65%родного eyemask_relaxed и35%mouth_smileopen. Включены связанные веки/брови/губы/челюсть/зубы/язык, а не только внешняя линия улыбки. Это постоянная native3D REST-expression, не отдельная лицевой анимационный риг в runtime.

Нативные evaluated baseline/candidate проходят ЯВНЫЙ исторический uniformHeadFit и существующее up20 поле шеи. Проверка против frozen текущих mesh до изменения: максимальная ошибка0.235µm. Не делался новый bbox-fit/размер/камера. Дельта выражения переносится в уже существующие mesh; координаты нижеRESTZ1.18 защищены с нулевым изменением. Перечень дельт/контролов в derivation.json.

## Реальные дельты и ограничение больших движений

Глазные яблоки L/R, eye_highlights и обе face_line meshes: дельта **EXACT0**, размеры/положение не менялись. Head facial surface max30.872mm, brows14.708mm, lashes22.747mm, upperteeth8.138mm, lowerteeth25.870mm, tongue33.133mm. Это существенные исходные facial-pose деформации, НЕ автоматически принятые значения. Они не скрыты нормализацией/перекадровым масштабом и не обрезаны по вершинам искусственным cap: такая обрезка разрушила бы связное native выражение. Коллизии mouth/eyelid/crown и весь диапазон походки/ракурсов НЕ сертифицированы одним статическим кадром. Материал/крона untouched.

Cold-open до рендера:50action full-key/handle hashes exact, boneREST/rigmatrix/camera exact,15packedimages exact, topologyUVweightsmaterialslotsrenderVisibility всех старых mesh exact; все nonfacial координаты, включая crown и eye-globes exact. Защищённая нижняя шея delta0. Trial self-contained blend и native deltas остаются в ignoredcache, полностью воспроизводимы derive.py. Source hashes unchanged.

## Один actual front trial

После прямого подтверждения npc_facing, что80+wrap renders закончены, запущен РОВНО ОДИН Eevee32AA512×640 frontWalk0, yaw0, та же исходная камера/Rootrest. Наблюдаемое время6.05s. Файл front-trial32.png. baseline-front00.png — byte-exact копия исходного frozen09ac48proof кадра00,128AA; он не перерисован/не подменён. Из-за разного AA это НЕ exactpixel-diff проверка. Обе картинки целиком, одинscale1, никакой registration. Крупный face crop — один и тот же прямоугольник и3×nearest только для review.

Наблюдение: появилась читаемая приоткрытая улыбка с зубами, внутренний тревожный подъём бровей смягчился; верхние веки теперь тяжелее/глаза полуприкрыты. Это может читатьcя спокойнее, но также соннее, чем уверенный ясный взгляд канона. Не считать recipe доказанным сходством/принятой внешностью. Грубого отрыва глаз/зубов в этом единственном фронтальном кадре не видно; это не полный intersection audit. Ракурс исходной камеры всё ещё сверху, взгляд/голова не развёрнуты отдельным трюком.

Репродукция: inventory.py → derive.py → cold-check.py; ТОЛЬКО после проверки/свободного render-slot render-one.py; compare.py. Renderer/encoder jobs завершены. No48, no runtime integration, no new art acceptance.
