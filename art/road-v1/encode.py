"""Encode immutable generated material and expose its repeat for review."""
from pathlib import Path
from PIL import Image, ImageChops, ImageStat, ImageDraw, ImageFilter
import hashlib, json

root = Path(__file__).resolve().parents[2]
folder = Path(__file__).resolve().parent
dest = root / 'public/assets/road-v1'
dest.mkdir(parents=True, exist_ok=True)
original = folder/'charoite-generated-v1.png'
repair = folder/'charoite-offset-repaired-v2.png'
if repair.exists():
    offset=ImageChops.offset(Image.open(original).convert('RGB'),627,627)
    edited=Image.open(repair).convert('RGB')
    assert edited.size == offset.size == (1254,1254)
    # Only the explicitly requested central cross is imported from the edit.
    # The immutable outer region restores adjacent original pixels on tile edges.
    cross=Image.new('L',offset.size)
    draw=ImageDraw.Draw(cross)
    draw.rectangle((527,0,727,1253),fill=255)
    draw.rectangle((0,527,1253,727),fill=255)
    cross=cross.filter(ImageFilter.GaussianBlur(12))
    # At outer edges, the crossing repair would destroy tiling. Taper the cross
    # to zero in the final64px before the original offset edges.
    pixels=cross.load()
    for y in range(1254):
        for x in range(1254):
            edge=min(x,y,1253-x,1253-y)
            pixels[x,y]=round(pixels[x,y]*min(1,edge/64))
    combined=Image.composite(edited,offset,cross)
    ImageChops.offset(combined,-627,-627).save(folder/'charoite-seam-repaired-v2.png')
source = folder / 'charoite-seam-repaired-v2.png' if repair.exists() else original
image = Image.open(source).convert('RGB').resize((1024, 1024), Image.Resampling.LANCZOS)
image.save(dest / 'charoite.webp', lossless=True, method=6)
repeat = Image.new('RGB', (2048, 2048))
for x in (0, 1024):
    for y in (0, 1024):
        repeat.paste(image, (x, y))
repeat.save(folder / 'charoite-repeat-2x2.webp', lossless=True, method=6)
def jump(a, b):
    return sum(ImageStat.Stat(ImageChops.difference(image.crop(a), image.crop(b))).mean) / 3
manifest = {
    'schemaVersion': 1, 'file': 'assets/road-v1/charoite.webp', 'size': [1024,1024],
    'source': str(source.relative_to(root)), 'sourceSha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'sha256': hashlib.sha256((dest/'charoite.webp').read_bytes()).hexdigest(),
    'encoding': 'builtin central-cross seam repair composited only over offset source cross; 64px original-edge guard; inverse offset; uniform Lanczos resize; lossless WebP; no mirroring',
    'repeatWorldHexRadii': 3.2, 'registration': 'fixed world origin; runtime ground camera',
    'checks': {'repeatPreview': 'art/road-v1/charoite-repeat-2x2.webp',
        'edgeMeanAbsoluteRgbJump': {'x': jump((0,0,1,1024),(1023,0,1024,1024)), 'y': jump((0,0,1024,1),(0,1023,1024,1024))},
        'seamVisualAudit': 'pending', 'actualGameplay': 'not-run'},
    'status': 'encoded-candidate-seam-and-game-review-pending',
    'rights': json.loads((folder/'source.json').read_text())['rights'],
}
(dest/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
(folder/'encoding-checks.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(json.dumps(manifest, indent=2))
