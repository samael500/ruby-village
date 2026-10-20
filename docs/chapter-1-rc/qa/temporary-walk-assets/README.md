# Временная ходьба: оставить существующий animated-v3

Read-only snapshot интеграции **e32cad43a8b4061dec2f95a09e3669ac4537f405**. Manifest и все12фактически прочитанных atlasfiles совпадают byte-for-byte с commit. Никакие runtime/asset/controller файлы не изменены, Blender/генерация/рендер не запускались.

**Один минимальный вариант: оставить `public/assets/characters-walk-v1/animated-v3/` как TEMPORARY.** Контактный лист `animated-v3-two-directions-four-poses.jpg` показывает actual E/SE, phases0/4/8/12, без framefit (один2×nearest viewing scale). Ноги действительно переходят из вынесенной в согнутую/противоположную позу — это не статичный спрайт, просто движущийся по полю.

Все6dirs в base+calibrated-1 имеют16уникальных walkframes,50ms/кадр,800ms/цикл. JSON содержит исходные rects/хеши/изменения visiblepixels; rawRGBAразличия сами по себе НЕ считаются доказательством хорошей походки (в transparentRGB есть шум). Визуальный вывод основан на фактических позах листа. Общийrenderer e32cad4 уже запрашивает этотmanifest в src/ruta-motion-view.ts; art replacement не нужен для начала временной работы.

`animated-v2` содержит тот же6-направленный16-фазный source-v2комплект; v3 — его optimizeddelivery. Возврат кv2 не добавит фаз/новой походки. Верхний characters-walk manifest — rejectedreviewset, east-mesh-pilot — эксперимент толькоEast, полного6dir drop-in не дают.

Ограничения видны честно: старые разрывы/стыки коленей и вырезанные части фигуры остаются; это НЕфинальная графика/принятаяанимация. Новые nativehair/model исследования остановлены. Реальное переключение кадров при движении и mouse/touch/reduced-motion в приложении здесь НЕ проверялись; это следующий root runtime check, не основание генерировать новые атласы. Код/контроллер общие файлы принадлежат root.
