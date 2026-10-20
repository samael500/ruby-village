"""Whole-frame native guide sheets, fixed0.5 only. No fit, crop or image edits."""
from pathlib import Path
from PIL import Image
import json,hashlib
O=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();records=[]
for direction in ['se','sw','w','nw','ne']:
 D=O/direction;contract=json.loads((D/'source-contract.json').read_text());variant=contract['cameraVariants']['base'];frames=variant['directions'][direction]['clips']['walk']['frames'];assert len(frames)==48
 sheet=Image.new('RGBA',(2048,1920));frameRecords=[]
 for i,f in enumerate(frames):
  src=D/f['file'];assert sha(src)==f['sha256'];im=Image.open(src).convert('RGBA');assert im.size==(512,640);whole=im.resize((256,320),Image.Resampling.LANCZOS);sheet.paste(whole,((i%8)*256,(i//8)*320));frameRecords.append({'phase':i,'sourcePng':str(src.relative_to(O)),'sourcePngSha256':sha(src),'rect':[(i%8)*256,(i//8)*320,256,320],'sourceFrame':f['sourceFrame']})
 out=D/'pose-guide48.png';sheet.save(out);assert Image.open(out).convert('RGBA').tobytes()==sheet.tobytes();records.append({'direction':direction,'path':str(out.relative_to(O)),'sha256':sha(out),'size':[2048,1920],'sourceContractSha256':sha(D/'source-contract.json'),'uniformScale':.5,'frames':frameRecords})
(O/'pose-guide-sheets.json').write_text(json.dumps({'scope':'technical native poses only, not painted art or runtime; same fullcanvas global0.5,8x6 rearrangement','existingE':'art/ruta-native-layered-walk48-v2/','sheets':records},indent=2)+'\n')
