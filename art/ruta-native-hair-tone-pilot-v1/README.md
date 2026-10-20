# Один native hair-tone material пилот — не gamma-fix/не art PASS

Frozen expression-v2 input SHA48f4b2bb9ec8cabd5c8f33ed46d3a9be1d1da499a0b099de9ed80885f4121f7c; исходные09ac/b14/sourceRGB неизменны. Только материал `Daisy alpha-aware volume candidate`: дубликат native Diffuse graph, один постоянный Multiply в LINEAR RGB между прежним fixedRGB texture и Diffuse Color: factor1, multiplier[.72,.80,.88]. Все старые изображения/UV/нормали/геометрия/глаза/выражение/аксессуары/крона/камера/анимации сохраняются. Исходный материал сохранён, не изменён. Scalp copper material не тронут.

Это ограниченный художественный выбор более сдержанного каштаново-медного тона, НЕ исправление gamut/gamma/color-space, НЕ per-frame обработка и НЕ затемнение сцены/master. Независимый предыдущий аудит6afe4ee не нашёл color-pipeline ошибки; здесь осознанно изменён native material output. Новый bitmap/faceUV/imagegen/bake не создаётся. Подробные linear параметры/хеши в contract/pixel-comparison.json.

Cold-open: все meshcoordinates/topology/UV/weights exact, включая hair shape и facialexpression;50full-key/handle action curves exact,15packedimages exact; camera/boneREST/rigmatrix exact. Sole mesh-record difference — один material slot нового hair volume. Готовый frozen derivative cache/ruta-hair-tone-trial.blend воспроизводится apply.py; heavycache не коммитится.

ОДИН actual Eevee32AA512×640 frontWalk0 yaw0, samecamera, после свободного NPC render-slot;6.50s. Baseline-front00.png — точная копия предыдущего actual expression-v2 front32AA. Canonical-before-after.jpg: канон(.45целоеизображение) / baseline1.0 / candidate1.0, механические фиксированные масштабы, без anatomyfit. Разные ракурсы canonical¾ vs nativefront явно остаются; нельзя оценивать геометрические размеры лица как angle-equivalent.

Actual same32AA comparison:26609RGBpixels changed, bbox148,121→363,367, полная alpha byte-identical (0изменений). Пример hair(240,145)223,111,56→190,98,52; другой(260,160)205,102,51→174,90,47. Проверенные face samples(250,240)255,155,114 и(245,255)241,154,121 exact; cloth(250,350)72,76,39 exact. Это показывает локальный material эффект, не fullregion identity через ручные landmark.

Наблюдение: яркая оранжевая насыщенность/светлота умеренно снижена, большие пряди/переходы/края остались читаемы. Результат ближе к chestnut/copper направлению канона, но stripe texture/crownshape по-прежнему отличаются; tone не объявляется способом скрыть геометрические/alpha проблемы. Художественная приёмка и temporal test кандидата НЕ выполнены. Аксессуары не корректировались в этом шаге.

Repro: apply.py→cold-check.py→согласованныйrender-one.py→compare.py. No48/runtime; все renderer/encoder jobs завершены.
