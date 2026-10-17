"""Registered vector masks over one unchanged painting, not procedural art.
The painted source is never recolored/resampled by this script. SVG paths only
isolate foreground depth and the gate leaf; opening is a fixed-pivot 2D transform.
"""
from pathlib import Path
import base64,json,hashlib
root=Path(__file__).resolve().parents[1];out=root/'art/chapter-1-v9/layers';out.mkdir(exist_ok=True)
source=root/'art/chapter-1-v9/candidates/gate-v2-closed.png'
data=base64.b64encode(source.read_bytes()).decode();image=f'<image width="1672" height="941" href="data:image/png;base64,{data}"/>'
# Gate leaf is inside both fixed posts, from latch at left to hinge at right.
leaf='M1321 776 L1332 759 L1347 745 L1366 733 L1387 725 L1410 720 L1435 719 L1453 724 L1453 797 L1321 847 Z'
# The fixed foreground grass band lies OUTSIDE all playable polygons.
# Source includes original leaves/flowers below fence, so no generated alpha fringe.
head='<svg xmlns="http://www.w3.org/2000/svg" width="1672" height="941" viewBox="0 0 1672 941">'
fg='M0 793 L1150 793 L1286 744 L1318 741 L1321 776 L1332 759 L1347 745 L1366 733 L1387 725 L1410 720 L1435 719 L1453 724 L1454 699 L1480 692 L1490 711 L1528 704 L1528 687 L1560 687 L1672 750 L1672 941 L0 941 Z'
def save(name,body): (out/(name+'.svg')).write_text(head+body+'</svg>')
mask=f'<defs><clipPath id="leaf"><path d="{leaf}"/></clipPath><mask id="fixed" maskUnits="userSpaceOnUse" x="0" y="0" width="1672" height="941"><path d="{fg}" fill="white"/><rect x="1319" y="717" width="136" height="224" fill="black"/></mask></defs>'
save('foreground-fixed',mask+'<g mask="url(#fixed)">'+image+'</g>')
save('gate-closed',mask+'<g clip-path="url(#leaf)">'+image+'</g>')
# Hinge is on right edge, opening outward. Project leaf to 19% width and
# shear lower points to keep hinge fixed. No independent image placement.
pivot=[1453,760];matrix=[0.19,-0.22,0,1,1453*(1-.19),1453*.22]
transform='matrix('+ ' '.join(str(x) for x in matrix)+')'
save('gate-open',mask+f'<g transform="{transform}"><g clip-path="url(#leaf)">'+image+'</g></g>')
save('foreground-closed',mask+'<g mask="url(#fixed)">'+image+'</g><g clip-path="url(#leaf)">'+image+'</g>')
manifest={'schemaVersion':1,'status':'artistic-review-pending','canvas':[1672,941],'origin':[0,0],'crop':[0,0,1672,941],'source':str(source.relative_to(root)),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'method':'unchanged source painting through registered SVG vector clip/masks; 2D affine gate animation','foregroundApertureCutout':[1319,717,136,224],'runtimeContract':'Open gate before Ruta enters goal; fixed/open clear all full playable polygons','gate':{'closedPath':leaf,'hingePivot':pivot,'openMatrix':matrix,'registration':'identical source coordinates; fixed point invariant at hinge x=1453'},'layers':{'background':'../candidates/gate-v3-base.png','foreground':'foreground-fixed.svg','gateClosed':'gate-closed.svg','gateOpen':'gate-open.svg'},'notes':['Vector clip is explicitly authorized deterministic masking, not a procedurally generated illustration','Masks do not touch playable cells; frontier outside full grid','Original v3 fringe candidates retained as rejected extraction attempts']}
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Registered source masks + gate transforms written')
