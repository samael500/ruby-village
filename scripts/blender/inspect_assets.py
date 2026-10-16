"""Inspect rendered layer alpha and produce factual image metadata, without editing assets."""
import json
import math
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/blender-chapter-1/candidates'
report={}
for path in sorted(OUT.glob('*.png')):
    with Image.open(path) as im:
        entry={'size':list(im.size),'mode':im.mode}
        if path.name.startswith('layer-'):
            assert im.size==(1672,941),(path,im.size)
            assert im.mode=='RGBA',(path,im.mode)
            alpha=im.getchannel('A')
            entry['alphaRange']=list(alpha.getextrema()); entry['alphaBounds']=alpha.getbbox()
            assert entry['alphaBounds'],path
            if path.name!='layer-background.png': assert entry['alphaRange'][0]==0,path
        report[path.name]=entry
# Compare the exported slab silhouette against the mathematical game mask.
with Image.open(OUT/'layer-stones.png') as im:
    actual=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
    expected=Image.new('L',im.size)
    center=(140+600,290+65*8.7)
    polygon=[(center[0]+70*math.cos(math.radians(30+i*60)),center[1]+45.5*math.sin(math.radians(30+i*60))) for i in range(6)]
    ImageDraw.Draw(expected).polygon(polygon,fill=255)
    # One source-pixel tolerance for rasterization and anti-alias coverage.
    outside=ImageChops.subtract(actual,expected.filter(ImageFilter.MaxFilter(3)))
    missing=ImageChops.subtract(expected.filter(ImageFilter.MinFilter(3)),actual)
    assert outside.getbbox() is None, 'Stone alpha extends outside game hex'
    assert missing.getbbox() is None, 'Stone alpha has holes inside game hex'
    report['stoneMask']={'matchesWithinPixels':1,'center':center,'radius':70,'groundScale':.65}
(OUT.parent/'image-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('Inspected',sum(name.endswith('.png') for name in report),'images; non-background layers have real transparency')
