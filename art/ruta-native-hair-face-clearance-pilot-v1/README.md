# Один bounded cheek-lock clearance пилот — НЕ выбран, риск контактов открыт

Frozen tone+expression input SHA159298a6225fa24c174af5562c7a14113e93bbbc5e463ac3e0968b0f15bb81f9. Только новый derivative, исходники09ac/b14/tone не изменены. Body/face/eyes/crown не перестраивались; нет новых UV/texture/imagegen/bitmap processing.

## Область и одна 3D-деформация

На native alpha-derived hair volume задано одно плавное постоянное REST поле: dy=40mm*w назад по+Y к уху, dx=sign(x)*12mm*w наружу. w — произведение кубическихsmoothstep: absXfade-in.09→.135, fade-out.23→.29; frontYfade-out−.025→.09; Zfade-in1.24→1.31, fade-out1.41→1.48.107726из527846вершин изменены, max41.761mm. Все crownverticesZ≥1.48 и lower-waveverticesZ≤1.24 EXACT0; границы/количества в derivation.json. Это локальная проба, не новое прижатие crown к голове и не per-frame fit. Не было подбора нескольких форм после результата.

Cold-open: все прочие mesh coordinates exact; topologyUVweightsmaterials exact,50full-key/handle actionhashes exact,15images exact, boneREST/rigmatrix/camera exact. Eyeexpression/size и исходный tone материал не изменены. Единственная meshrecord дельта — hairvolume coordinates. Heavy trial в ignoredcache, derive.py полностью воспроизводит.

## Выявленный геометрический blocker ДО рендера

REST BVH пересечения изменяемых hairfaces с actualhead:
- trianglepairs2818→3214;
- затронутые headpolygons1007→1210;
- ear-side spatialproxy(absX>.145,1.24<Z<1.48)910→1114.

Это растущий риск/неподтверждённая clearance, НЕ точная penetrationdepth и НЕ анатомическая маска уха. Исходные контакты уже существовали. Нельзя объявлять отсутствие коллизий, безопасность уха или исправление по одной сумме. До известного результата root явно разрешила только TWO plannedE32AA диагностических stills, несмотря на открытый риск; никаких молчаливых дополнительных geometric tweaks.

## Два actual production-E вида

`render-two.py`: same actual tone/expression, Walk0, production yawπ/2, originalRootRest/camera512×640,32AA у обоих. E-baseline32.png иE-candidate32.png (фактические имена строчными e-…). Один before/after fullcanvas scale1, без registration/cropfit. e-face-common-crop.jpg — один общий прямоугольник для просмотра. Actual original bounds обеих alpha128масок[142,127,374,531] одинаковы. Никакая reference09 с другим выражением/palette не используется как causalA/B.

Наблюдение: слегка больше видны щека и белый край глаза, но полноценный читаемый синий глаз не открыт. Чисто диагностический threshold B>R+25,B>G+10,B>70,alpha>128 в projected обеих неизменённых eyeballmeshROI[258,174,288,240] даёт **0→0pixels**. Это не точная segmentation радужки, не физическое доказательство отсутствия всех глазных деталей и не allfacePASS. Нельзя считать любой белый треугольник исправленным лицом. Из этого также не следует, что вся проблема доказанно только в волосах: ракурс/форма/направление реальной радужки остаются отдельными ограничениями.

**Verdict: candidate НЕ выбран.** Недостаточный выигрыш читаемости при увеличившемся контакте возле уха. По rootgate front/¾ не рендерились,48/runtime не запускались. Эта одна проба не доказывает невозможность другой правильной авторской укладки; она документирует конкретный неудачный локальный сдвиг, не маскируя его успешной сборкой/закрытым mesh.

Renderproof содержит source hashes/камеры/eyeprojectedbounds; cold/derivation/proxy JSON и processlogs сохранены. Все renderer/encoderjobs закончены. Новых вариантов после failedprobe нет.
