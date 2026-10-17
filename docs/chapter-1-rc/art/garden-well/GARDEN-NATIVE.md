# Garden native pilot — #45 / #46

Base0ad8c40, dedicated worktree/branch art/45-garden-well. Read SOURCE-HANDOFF-NOT-READY before continuation. Old common art-v9-props-composite.py and runtime/common manifests untouched.

Selected source-preserving composite:
- garden-clear-v1: original clear lawn/fence/left hedges, no hidden duplicate table or orchard.
- apple-tree-prop-v1: full1374×1145 source preserved; native alpha-only2px erosion removes generated fringe, uniform588×490 placed580,100. Whole crown/roots retained; no polygon clipping or anisotropic scaling.
- garden-map-v1 group1030,375,280,155: same painted round table, two chairs, bowl/basket/apples; uniform0.6 →1215,170,168,93. Dedicated alpha segmentation removes green backdrop and disconnected edge flowers/grass, preserving complete furniture including central leg. Original dark-green contact shadow is extracted from original ground pixels/softened alpha, not an invented replacement illustration. Source crop and native cutout saved.

Initial600×500@(600,100) tree leaked816 crown pixels into free polygon interior (bbox1152,290..1191,350); ground0. Rather than clip crown, selected2% smaller whole tree with20px left translation. Full tree alpha/free interior0, ground0, table0, proposed Rabbit full sprite0. One-pixel raster tolerance explicit in checks; >8alpha threshold. Clear upper-right Rabbitfeet1295,265. Actual gameplay renderer owns resident contact shadow and can review grounding together with table's source shadow.

Map reference garden is apple-tree/table/fence only, no cottage; do not invent a different house to fill logical `house` hedge blocker. Native candidate/geometry/full-sprite comparison in art/chapter-1-v9/garden-well. Public background and dedicated manifest staged separately, no automatic activation. Root viewed initial composition and requested zero-alpha correction; actual game pilot remains pending. Painted wide continuation and well follow native review; registration templates are not final art.
