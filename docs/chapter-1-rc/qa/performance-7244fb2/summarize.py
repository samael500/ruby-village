import json,collections
from pathlib import Path
O=Path(__file__).resolve().parent

def category(url):
 p=url.split('/ruby-village/')[-1]
 if 'chapter-1/v6/'in p:return'legacy menu v6 PNG'
 if 'chapter-1/v9/garden/'in p:return'painted garden/prologue scene'
 if 'chapter-1/v9/gate/'in p:return'painted gate scene (also used by prologue)'
 if 'chapter-1/v9/mill/'in p:return'painted mill scene'
 if 'characters-walk-v1/'in p:return'Ruta runtime atlases/manifest'
 if 'characters-facing-v1/'in p:return'resident facing images'
 if 'characters-v1/'in p:return'character poses/portraits'
 if 'chapter-map-'in p:return'painted map'
 if 'assets/level-1/v5/'in p:return'legacy inventory tile PNGs'
 if 'assets/road-v1/'in p:return'connected road material'
 if 'assets/audio/'in p:return'audio'
 if 'assets/ui/'in p:return'UI materials/header'
 return'HTML/JS/CSS/other'
out={'samples':[],'requestPhaseSamples':[]}
for name in ['gate-1280','gate-844','mill-1280','mill-844']:
 x=json.loads((O/name/'report.json').read_text());groups=collections.defaultdict(lambda:{'requests':0,'encodedBytes':0})
 for row in x['coldRequests']:g=groups[category(row.get('url',''))];g['requests']+=1;g['encodedBytes']+=row.get('encodedBytes',0)
 row={k:x[k]for k in ['source','scene','viewport','menuGotoReturnMs','menuRequestCountAtGotoReturn','menuEncodedBytesAtGotoReturn','navToMotionReadyMs','afterFinalEntryInputToMotionReadyMs','coldReadyNetworkIdleMs','coldRequestCount','coldEncodedBytes','estimatedVisibleRgbaPixelBytes','phases','errors']};row['categoryBudgets']=dict(groups);row['top10ColdRequests']=[{'path':r.get('url','').split('/ruby-village/')[-1],'encodedBytes':r.get('encodedBytes',0),'status':r.get('status')}for r in sorted(x['coldRequests'],key=lambda r:r.get('encodedBytes',0),reverse=True)[:10]];out['samples'].append(row)
for w in ['1280','844']:
 x=json.loads((O/f'network-phases-{w}.json').read_text());groups=collections.defaultdict(lambda:{'requests':0,'encodedBytes':0});cats=collections.defaultdict(lambda:collections.defaultdict(int))
 for r in x['requests']:g=groups[r['requestPhase']];g['requests']+=1;g['encodedBytes']+=r.get('encodedBytes',0);cats[r['requestPhase']][category(r.get('url',''))]+=r.get('encodedBytes',0)
 out['requestPhaseSamples'].append({'viewport':x['viewport'],'markers':x['markers'],'budgetsByRequestPhase':dict(groups),'categoryBytesByRequestPhase':{k:dict(v)for k,v in cats.items()},'totalBytes':sum(g['encodedBytes']for g in groups.values()),'note':'Request initiation phase is exact; earlier requests can finish in later phases. See raw responsePhase/finishPhase.'})
(O/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
