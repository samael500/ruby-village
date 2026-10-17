"""Read-only integrity inventory of completed shared downloads; never extract/change shared tools."""
from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parents[1];shared=Path('/home/mskorokhod/life/_tools/mpfb-assets');source=Path('/home/mskorokhod/life/_tools/mpfb2-v2.0.18');report={'toolSource':'https://github.com/makehumancommunity/mpfb2/tree/v2.0.18','guide':'https://static.makehumancommunity.org/mpfb/docs/getting_started.html','readOnlySharedSources':True,'packs':[],'sourceFiles':{}}
for p in sorted(shared.glob('*.zip')):
 with zipfile.ZipFile(p)as z:
  bad=z.testzip();assert bad is None,bad
  report['packs'].append({'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'zipCRC':'PASS','entries':len(z.namelist())})
for name in ['src/mpfb/__init__.py','src/mpfb/data/rigs/standard/rig.default.json','src/mpfb/data/rigs/standard/weights.default.json','LICENSE.md','LICENSE.ASSETS.md','LICENSE.CODE.md']:
 report['sourceFiles'][name]=hashlib.sha256((source/name).read_bytes()).hexdigest()
report['availableAssets']={p.name:json.loads(p.read_text()) for p in sorted((shared/'extracted/packs').glob('*.json'))}
(root/'art/characters-mpfb-v1/inventory.json').write_text(json.dumps(report,indent=2)+'\n');print('CRC PASS',len(report['packs']),'packs; source files hashed; inventory saved')
