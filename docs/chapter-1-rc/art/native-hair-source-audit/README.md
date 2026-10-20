# Native hair source audit — три проверенных источника, одна условная рекомендация

Read-only audit2026-10-20. Не создавались/не импортировались модели, не запускался Blender/рендер/покупка/логин/imagegen. Чужие `_tools` только прочитаны, файлы/процессы не менялись. Исследование НЕ заменяет pending stability review текущего пилота.

**Рекомендация для ОДНОГО следующего bounded source-fit: Elvaerwyn Keylth.** На реальном upstream thumbnail длинные волны отведены в основном назад, верх идёт продольным боковым потоком, нет Daisy-подобной поперечной «крыши». Это лучший из проверенных source-shape кандидатов, **НЕ готовая подтверждённая причёска Руты**. Положение волос ЗА конкретной щекой/ухом Ellie без fit/render не доказано. Готовую замкнутую объёмную hair основу безalpha-cards этот аудит НЕ нашёл.

## Реально существующие файлы, не каталог ссылок

Все три уже находились локально в `/home/mskorokhod/life/_tools/mpfb-assets/extracted/hair/`, соответствуют byte-for-byte каждому entry имеющегося официального `hair02_ccby.zip`. OBJ, MHCLO, material, UV, текстуры и thumbnails реально прочитаны/хешированы. Полные абсолютные пути/размеры/SHA/entry proofs в inventory-and-provenance.json. Новая72MBкопия архива не скачивалась: HEAD официального зеркала200, Content-Length72283345. Официальные три PNG-thumbnails получены200 и сохранены с хешами. Малые source-license headers/materials скопированы отдельно, не сами модели.

| Источник | Реальная геометрия/лицензия | Конкретное соответствие и оставшийся разрыв |
|---|---|---|
| **Keylth — рекомендуемый**: `elvs_keylth_hair/elvs_keylth_hair_m1.obj` |3383v/2167faces,2353boundaryedges; OBJ+MHCLO: Elvaerwyn,CC-BY. NativeUV, diffuse/normal1.5, alpha-enabled/two-sided material. |Openforehead/swept side flow и длинная задняя масса ближе к канону, чем Daisy cap. Но это исходно `male`/hm08fit, не Ellie-детская голова; тонкие длинные пряди/острый передний локон, светлый photographicRGB. Ухо/eyeclearance и форма со всех сторон не проверены. Не закрытый solidvolume; карточное мерцание автоматически не решено. |
| Lady Hippy: `elvs_lady_hippy_hair/elvs_ladies_hippyhair1.obj` |4001v/2510faces,2891boundaryedges; Elvaerwyn,CC_by вOBJ/CC-BY втаблице. NativeUV/material+alpha существуют. |Длинный открытый лоб и плавные крупные изгибы; но очень длинная свисающая передняя «верёвка», остальная масса прямее/тоньше нужных свободных S-волн. Нет доказательства убранных за щёку волос. Не предлагается вторым параллельным fit. |
| Hazel: `elvs_hazel_hair/elvs_hazel_hair.obj` |3494v/4181faces,2739boundaryedges; Elvaerwyn,CC-BY. Реальные UV/diffuse/normal/thumbnail. |Длина/мягкие волны присутствуют, но несколько передних полос падают прямо на лицо, тоесть главный clearance риск заметен уже вthumbnail. Ниже приоритетом; не назначается для fit. |

`three-verified-source-thumbnails.jpg` — ровно эти три исходных thumbnails, Elvaerwyn/CC-BY, без нового рендера/AI. Отдельные `*-official.png` — настоящие официальные картинки, `*.png` — установленные.thumbбайты. Нет утверждения, что thumbnail на пустом фоне доказывает конкретную человеческую форму уха, положение пряди или closed topology. Boundary counts доказывают открытые поверхности; материал explicittransparent, а не предположительно opaque.

## Проверенные первичные URLs и право использования

[Официальная hair02 таблица](https://static.makehumancommunity.org/assets/assetpacks/hair02.html) перечисляет все три как Elvaerwyn/CC-BY и ведёт на [архив](https://files2.makehumancommunity.org/asset_packs/hair02/hair02_ccby.zip). [Keylth thumbnail](https://static.makehumancommunity.org/assets/assetpacks/elvs_keylth_hair.png), [Lady Hippy thumbnail](https://static.makehumancommunity.org/assets/assetpacks/elvs_lady_hippy_hair.png), [Hazel thumbnail](https://static.makehumancommunity.org/assets/assetpacks/elvs_hazel_hair.png) действительно доступны200.

Original asset-node links: Keylth `https://www.makehumancommunity.org/node/2173`, LadyHippy `/node/1812`, Hazel `/node/2816` — web fetch дал timeout; **не утверждается, что страницы прочитаны**. Наличие/права подтверждаются официальной package-table плюс исходными локальными OBJ/MHCLO и архивным byte-match, не недоступными nodes.

Source metadata указывает CC-BY/CC_by БЕЗ явной версии. Не переименовываем это в CC0 и не приписываем asset header строку4.0, которой там нет. [Официальная FAQ о CC-BY](https://static.makehumancommunity.org/oldsite/faq/what_do_i_need_to_do_when_i_use_a_ccby_asset.html) отсылает к [CC BY4.0](https://creativecommons.org/licenses/by/4.0/) и описывает attribution в играх; license разрешает адаптацию/коммерческое использование с сохранением условий. Для использования сохраняются Elvaerwyn, asset title, source/license links и описание изменений; реальная версия исходного notice не скрывается. Никакой покупки/дополнительной авторизации на сайте не сделано. Это source-license audit, а не утверждение blanketправ на любые внешние персонажи.

Attribution для этих review thumbnails: **Keylth Hair / Lady Hippy Hair / Hazel Hair — Elvaerwyn, MakeHuman Community hair02, CC-BY (source notice), documentation links above; thumbnail side-by-side layout only, original bitmap unchanged.**

## Минимальный следующий проверяемый шаг и предел вывода

Если root выбирает продолжать: взять ТОЛЬКО Keylth собственным immutable source-copy с лицензией; сначала проверить scalp-root/opening fit к существующей голове, сохраняя характерный боковой flow/длину, не сжимать всю причёску поheightbbox. Одни actual front/E/¾ source-fit stills должны доказать ухо/глаз/крону ДО нового48/volumetricconversion/materialpaint. Не менять тело/голову/Walk/камеру ради thumbnail.

Если обязательное требование — уже готовые closed volumetric waves с доказанным behind-earclearance, **подходящей готовой основы в этих проверенных файлах нет**. Keylth — ограниченная shape recommendation, не обещание решения; те же alpha-surface/UV/temporal риски нужно показать явно. Не предлагается массово скачать/перебрать ещё десятки моделей.
