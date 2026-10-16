"""Rebuild static residents/acting-pose resource contracts from exported PNGs."""
from pathlib import Path
from PIL import Image
import json
R=Path(__file__).resolve().parents[2];A=R/'public/assets/characters-v1'
def frame(rel,foot=None):
 im=Image.open(A/rel);w,h=im.size
 return {'image':rel,'sourceRect':[0,0,w,h],'frameSize':[w,h],'footAnchor':foot}
res={'schemaVersion':1,'version':'residents-painted-v1-2026-10-17','status':'new-painted-assets-ready-for-review','sceneSize':[1672,941],'origin':'new built-in imagegen sheets, not recovered archives','characters':{}}
config={'rabbit':('Кролик',108,[302,977]),'squirrel':('Бельчонок',92,[438,900]),'hedgehog':('Ёж',74,[319,840]),'teacher':('Учительница',174,[239,1004]),'baker':('Пекарь',165,[258,995]),'miller':('Мельник',181,[231,996])}
for id,(speaker,height,foot) in config.items():
 f=frame(f'residents/{id}-idle.png',foot);h=f['frameSize'][1]
 res['characters'][id]={'speaker':speaker,'source':f'art/characters-v1/{id}-source-v1.png','nativeHeightPx':h,'sceneHeightPx':height,'scale':height/h,'frames':{'idle':f,'portrait':frame(f'residents/{id}-portrait.png')},'clips':{'idle':{'loop':True,'frames':[{'frame':'idle','durationMs':1000}]}},'anatomyChecked':True,'appearanceApproval':'new-design-review-pending'}
(A/'residents-manifest.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
poses={'schemaVersion':1,'version':'prologue-painted-poses-v1-2026-10-17','status':'ruta-identity-approved-pose-review-pending','sceneSize':[1672,941],'origin':'new coherent static source sheet; not animation frames','frames':{}}
commonScale=136/768
config={'ruta-basket':([199,764],{'basket':'baked-in-held-both-hands'}),'ruta-adjust-satchel':([241,772],{'basket':'baked-in-held','satchel':'baked-in-adjusted-one-strap'}),'ruta-surprised':([276,713],{'basket':'baked-in-held'}),'ruta-crouch-basket':([155,516],{'basket':'baked-in-on-ground','basketGroundAnchor':[420,461],'reachingHandAnchor':[355,485]})}
for id,(anchor,props) in config.items():
 f=frame(f'poses/{id}.png',anchor);f.update({'character':'ruta','scale':commonScale,'nativeHeightPx':f['frameSize'][1],'nativeStandingHeightPx':768,'sceneStandingHeightPx':136,'sceneHeightPx':f['frameSize'][1]*commonScale,'props':props,'direction':'three-quarter-right','asymmetricMirroring':False});poses['frames'][id]=f
for id,height,anchor,character,props in [('basket-ground',27,[564,1072],None,{'basket':'standalone-ground-prop'}),('rabbit-baking',133,[464,1279],'rabbit',{'table':'baked-in','bowl':'baked-in','spoon':'baked-in-held'})]:
 f=frame(f'poses/{id}.png',anchor);f.update({'character':character,'nativeHeightPx':f['frameSize'][1],'sceneHeightPx':height,'scale':height/f['frameSize'][1],'props':props,'asymmetricMirroring':False});poses['frames'][id]=f
poses['staging']=[{'frameIndex':0,'scene':'courtyard','pose':'ruta-basket','foot':[560,480],'cameraReviewCrop':None},{'frameIndex':1,'scene':'courtyard','pose':'ruta-adjust-satchel','foot':[560,480],'cameraReviewCrop':[250,230,836,470]},{'frameIndex':2,'scene':'orchard','pose':'rabbit-baking','foot':[850,570],'cameraReviewCrop':None},{'frameIndex':3,'scene':'courtyard','pose':'ruta-surprised','foot':[670,520],'stones':[[705,518],[725,524],[695,537]],'cameraReviewCrop':[350,250,836,470]},{'frameIndex':4,'scene':'courtyard','pose':'ruta-crouch-basket','foot':[670,520],'stones':[[706,514]],'cameraReviewCrop':[350,250,836,470]},{'frameIndex':5,'scene':'courtyard','pose':'idle-pilot','foot':[560,480],'cameraReviewCrop':None}]
(A/'poses-manifest.json').write_text(json.dumps(poses,ensure_ascii=False,indent=2)+'\n')
print('6 residents / 6 acting or prop frames / 6 semantic stage entries')
