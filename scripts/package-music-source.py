"""Rebuild the optional music-source download after editing the score or instruments."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
output = root / 'public/licenses/music-source.zip'
files = [root / 'scripts/music-compose.py', root / 'THIRD_PARTY_MUSIC.md',
         root / 'art/audio/music/TimGM6mb.sf2',
         *sorted((root / 'art/audio/music').glob('*.mid')),
         *sorted((root / 'art/audio/music/licenses').glob('*.txt'))]
output.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(output, 'w', ZIP_DEFLATED, compresslevel=9) as archive:
    for source in files:
        entry = ZipInfo(source.relative_to(root).as_posix(), (2026, 10, 17, 0, 0, 0))
        entry.compress_type = ZIP_DEFLATED
        archive.writestr(entry, source.read_bytes())
print(f'{output.relative_to(root)}: {len(files)} editable source/license files')
