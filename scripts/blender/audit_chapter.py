"""Audit saved Blender meshes against independent exports from the actual game.
Full polygon intersections, not screenshots, centers or a sampling lattice.
"""
import hashlib
import html
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/blender-chapter-1/layouts'
sys.path.insert(0,str(Path(__file__).resolve().parent))
from layout_math import area,intersection,bounds,touching
IDS=['gate','garden','well','bakery','stream','mill','post','forest']
(OUT/'plans').mkdir(exist_ok=True)


def check(id):
    source=ROOT/'art/blender/chapter-layouts'/f'{id}.blend'
    bpy.ops.wm.open_mainfile(filepath=str(source))
    engine_path=OUT/'engine'/f'{id}.json';engine=json.loads(engine_path.read_text());scene=bpy.context.scene;camera=scene.camera
    assert scene['engineSha256']==hashlib.sha256(engine_path.read_bytes()).hexdigest(),'Stale source'
    if engine.get('layoutChanges'):assert json.loads(scene['layoutChanges'])==engine['layoutChanges'] and scene['requiresGameIntegration']
    for path,digest in engine['inputs'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,('Stale engine export',path)
    w,h=engine['resolution'];assert [scene.render.resolution_x,scene.render.resolution_y]==[w,h]
    assert camera.data.type=='ORTHO'
    def pixel(p):
        projected=world_to_camera_view(scene,camera,Vector(p));return (projected.x*w,(1-projected.y)*h)
    def cap(obj):
        return [pixel(obj.matrix_world @ obj.data.vertices[i].co) for i in obj.data.polygons[obj['capFace']].vertices]
    actual={o['cellId']:o for o in scene.objects if 'engineTerrain' in o}
    expected={c['id']:[(p['x'],p['y']) for p in c['polygon']] for c in engine['cells']}
    assert set(actual)==set(expected) and len(actual)==77
    polygons={ident:cap(obj) for ident,obj in actual.items()}
    blockers={ident:polygons[ident] for ident,obj in actual.items() if obj['engineTerrain']}
    free={c['id']:expected[c['id']] for c in engine['cells'] if not c['terrain']}
    maximum_corner=max(max(min(math.dist(p,q) for q in polygons[ident]) for p in poly) for ident,poly in expected.items())
    coverage=[]
    for c in engine['cells']:
        poly=expected[c['id']];covered=sum(area(intersection(poly,p)) for p in blockers.values() if touching(poly,p))
        error=abs(covered-(area(poly) if c['terrain'] else 0))
        coverage.append({'id':c['id'],'terrain':c['terrain'],'errorPx2':error})
        assert actual[c['id']]['engineTerrain']==(c['terrain'] or '')
    maximum_area=max(c['errorPx2'] for c in coverage)
    assert maximum_corner<.001,(id,maximum_corner)
    assert maximum_area<.25,(id,maximum_area)
    # Mutation checks prove that missing and displaced blockers cannot pass.
    missing=next(iter(blockers));negative_missing=area(expected[missing])-sum(area(intersection(expected[missing],p)) for ident,p in blockers.items() if ident!=missing)
    c0=next(c for c in engine['cells'] if c['id']==missing);c1=next(c for c in engine['cells'] if not c['terrain'])
    dx,dy=c1['center']['x']-c0['center']['x'],c1['center']['y']-c0['center']['y']
    moved=[(x+dx,y+dy) for x,y in blockers[missing]];negative_spill=area(intersection(moved,expected[c1['id']]))
    assert negative_missing>7000 and negative_spill>7000
    # Evaluate real mesh triangles for props, including the accepted fence/door.
    bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
    solids=[o for o in scene.objects if o.type=='MESH' and o.get('clearanceRole')=='solid']
    def triangles(obj):
        evaluated=obj.evaluated_get(deps);m=evaluated.to_mesh();m.calc_loop_triangles()
        result=[[obj.matrix_world @ m.vertices[i].co for i in face.vertices] for face in m.loop_triangles]
        evaluated.to_mesh_clear();return result
    def interference(obj,ground=False):
        hits=[]
        for tri in triangles(obj):
            poly=[pixel((p.x,p.y,0) if ground else p) for p in tri]
            if area(poly)<.00001:continue
            for ident,cell in free.items():
                if not touching(poly,cell):continue
                overlap=area(intersection(poly,cell))
                if overlap>.12:hits.append({'object':obj.name,'cell':ident,'areaPx2':overlap,'mode':'ground' if ground else 'visible'})
        return hits
    hits=[]
    for obj in solids:hits.extend(interference(obj)+interference(obj,True))
    assert not hits,(id,'Props obscure free cells',hits[:10])
    # Check true water surfaces too: only these two levels may contain any water.
    water=[o for o in scene.objects if o.get('waterExtension') or o.get('engineTerrain')=='water']
    assert bool(water)==(id in ['stream','mill'])
    for o in water:assert not interference(o),(id,'Water spill',o.name)
    # Each approach is an actual connected triangle fan containing the full anchor hex.
    approaches=json.loads(scene['approaches']);approach_reports=[]
    for approach in approaches:
        o=scene.objects[approach['object']];role=approach['role'];anchor=engine[role];ref=(anchor['pixel']['x'],anchor['pixel']['y'])
        vertex=o.matrix_world @ o.data.vertices[o['anchorVertex']].co
        error=math.dist(pixel(vertex),ref);assert error<.001,(id,role,error)
        triangles_ground=[[(p.x,p.y,0) for p in tri] for tri in triangles(o)]
        anchor_poly=expected[f"{anchor['q']},{anchor['r']}"]
        covered=sum(area(intersection(anchor_poly,[pixel(p) for p in tri])) for tri in triangles_ground)
        assert abs(covered-area(anchor_poly))<.25,(id,role,'Incomplete landing',covered)
        blocked_overlap=sum(area(intersection([pixel(p) for p in tri],poly)) for tri in triangles_ground for poly in blockers.values() if touching([pixel(p) for p in tri],poly))
        assert blocked_overlap<.25,(id,role,'Approach crosses blocker',blocked_overlap)
        endpoint=o['endpoint'];endpoint_px=pixel(endpoint)
        approach_reports.append({'role':role,'anchorErrorPx':error,'blockedAreaPx2':blocked_overlap,'landmarkDistancePx':math.dist(endpoint_px,ref),'coversFullAnchor':True})
    # The actual exported three bridge caps must cover the two dry ends and one water cell.
    bridge=[o for o in scene.objects if o.get('pieceKind')=='bridge']
    bridge_reports=[]
    for piece in engine['pieces']:
        if not piece['placement']:continue
        meshes=[o for o in scene.objects if o.get('pieceId')==piece['id']]
        assert {o['cellId'] for o in meshes}==set(piece['cells'])
        for o in meshes:
            poly=cap(o);expected_poly=expected[o['cellId']]
            assert max(min(math.dist(p,q) for q in poly) for p in expected_poly)<.001
        if piece['kind']=='bridge':
            assert len(meshes)==3 and sum(actual[o['cellId']]['engineTerrain']=='water' for o in meshes)==1
            assert bpy.data.collections['bridge'].hide_render
            anchor=piece['placement']['anchor'];middle=f"{anchor['q']},{anchor['r']}"
            directions={(1,0),(1,-1),(0,-1),(-1,0),(-1,1),(0,1)}
            adjoining=[c for c in engine['cells'] if c['terrain']=='water' and (c['q']-anchor['q'],c['r']-anchor['r']) in directions]
            assert len(adjoining)==2
            def centroid(poly):return tuple(sum(p[i] for p in poly)/len(poly) for i in [0,1])
            entry,exit=[centroid(polygons[c['id']]) for c in adjoining];center=centroid(polygons[middle])
            center_error=math.dist(((entry[0]+exit[0])/2,(entry[1]+exit[1])/2),center)
            assert center_error<.001,(id,'Water bypasses bridge center',center_error)
            # Regression: reversing the approved move recreates the old off-center bend.
            old=json.loads((ROOT/'src/chapter-1.logical.json').read_text())[id]['terrain']
            old_adjoining=[c for c in engine['cells'] if old.get(c['id'])=='water' and (c['q']-anchor['q'],c['r']-anchor['r']) in directions]
            old_points=[centroid(polygons[c['id']]) for c in old_adjoining]
            old_error=math.dist(tuple(sum(p[i] for p in old_points)/len(old_points) for i in [0,1]),center)
            assert old_error>50,(id,'Negative crossing check is ineffective')
            bridge_reports.append({'pieceId':piece['id'],'cells':piece['cells'],'waterCenter':middle,'dryEnds':2,'hiddenBeforeBuild':True,'exactCaps':True,
                                   'adjoiningWaterCells':[c['id'] for c in adjoining],'riverCenterErrorPx':center_error,'negativeOriginalBendErrorPx':old_error})
    assert bool(bridge)==(id in ['stream','mill'])
    assert all(bpy.data.collections[n].hide_render for n in ['verification','solution','bridge','gate_open','playable_contract'])
    # The gate uses the accepted transforms and remains clear over its entire sampled swing.
    gate_report=None
    if id=='gate':
        old=ROOT/'art/blender/gate-pilot.blend'
        # Load comparison objects without inserting them into the scene.
        with bpy.data.libraries.load(str(old),link=False) as (available,loaded):
            wanted=[name for name in available.objects if name.startswith(('gate vertical','gate cross','gate diagonal','gate brass','hinge gate'))]
            loaded.objects=list(wanted)
        for name,original in zip(wanted,loaded.objects):
            local=scene.objects[name]
            assert max(abs(local.matrix_basis[i][j]-original.matrix_basis[i][j]) for i in range(4) for j in range(4))<1e-6
            if local.type=='MESH':
                assert len(local.data.vertices)==len(original.data.vertices)
                assert max((a.co-b.co).length for a,b in zip(local.data.vertices,original.data.vertices))<1e-6
        hinge=scene.objects['hinge gate_closed'];layout=json.loads(scene['gate_layout_json']);sweep=[]
        for i in range(20):
            hinge.rotation_euler[2]=layout['closedAngle']+(layout['openAngle']-layout['closedAngle'])*i/19
            bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
            posed_hits=[]
            for o in bpy.data.collections['gate_closed'].objects:
                if o.type=='MESH':posed_hits.extend(interference(o)+interference(o,True))
            assert not posed_hits,(id,'Gate sweep',i,posed_hits[:3]);sweep.append(i)
        hinge.rotation_euler[2]=layout['closedAngle'];bpy.context.view_layer.update()
        gate_report={'acceptedTransformsPreserved':True,'sweepPoses':len(sweep),'freeCellIntersections':0,'openingWidthWorld':layout['width']}
    # Draw a labelled handoff using actual projected saved .blend caps; engine contours are independent.
    colors={None:'#dce3c7','house':'#b99574','tree':'#8fb786','flower':'#d69bac','water':'#7ebacb'}
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">','<rect width="100%" height="100%" fill="#f7f3e8"/>',
           '<g font-family="DejaVu Sans,sans-serif" fill="#302f27">',f'<text x="55" y="65" font-size="32">{IDS.index(id)+1}. {html.escape(engine["name"])}</text>',
           '<text x="55" y="106" font-size="20">Грани Blender · пунктир: расчёт движка для макета · фиолетовый: эталон</text>']
    path=set(engine['path']);start=f"{engine['start']['q']},{engine['start']['r']}";goal=f"{engine['goal']['q']},{engine['goal']['r']}"
    for c in engine['cells']:
        ident=c['id'];color=colors[c['terrain']]
        if actual[ident]['semanticRole'] in ['forest boundary','perimeter planting']:color=colors['tree']
        if ident in path:color='#bea2d4'
        if ident==start:color='#75b99d'
        if ident==goal:color='#e6ac69'
        pts=' '.join(f'{x:.5f},{y:.5f}' for x,y in polygons[ident]);ep=' '.join(f'{x:.5f},{y:.5f}' for x,y in expected[ident])
        parts.extend([f'<polygon points="{pts}" fill="{color}" stroke="#655b49" stroke-width="1.3"/>',f'<polygon points="{ep}" fill="none" stroke="#326a93" stroke-width=".7" stroke-dasharray="5 3"/>'])
        x,y=c['center']['x'],c['center']['y'];label='СТАРТ' if ident==start else 'ЦЕЛЬ' if ident==goal else ident
        parts.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" font-size="15">{label}</text>')
    parts.extend([f'<text x="55" y="835" font-size="23">77 клеток · {len(blockers)} препятствий · {len(free)} доступных · {len(engine["path"])} клеток пути</text>',
                  '<text x="55" y="875" font-size="19">Дом / граница — коричневый; деревья — зелёный; клумба — розовый; вода — голубой.</text>',
                  '<text x="55" y="910" font-size="18">'+('Макет исправлен по рисунку Максима; изменения указаны в manifest.' if engine.get('layoutChanges') else 'Техническая схема для перерисовки в 2D. Игровые данные неизменны.')+'</text></g></svg>'])
    (OUT/'plans'/f'{id}.svg').write_text('\n'.join(parts)+'\n')
    exports={mode:{'file':f'renders/{id}-{mode}.png','resolution':[w,h],'origin':[0,0],'sourceRect':[0,0,w,h],'diagnostics':mode!='clean','bridgeBuilt':mode=='solved' and bool(bridge)} for mode in ['clean','check','solved']}
    layers={name:{'file':f'renders/{id}-{name}.png','resolution':[w,h],'origin':[0,0],'sourceRect':[0,0,w,h],'alpha':'straight'} for name in ['background','solution']+(['bridge'] if bridge else [])+(['gate_closed','gate_open'] if id=='gate' else [])}
    result={'sceneId':id,'status':'pass','source':str(source.relative_to(ROOT)),'layoutFile':f'{id}-layout.json','exports':exports,'layers':layers,'cells':77,'blocked':len(blockers),'free':len(free),'maxCornerErrorPx':maximum_corner,'maxAreaErrorPx2':maximum_area,
            'solidObjectsChecked':len(solids),'solidFreeIntersections':0,'groundFootprintsChecked':True,'approaches':approach_reports,'bridge':bridge_reports,'gate':gate_report,
            'mutationChecks':{'removedBlockerMissingAreaPx2':negative_missing,'movedBlockerSpillAreaPx2':negative_spill},'waterObjects':len(water),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'layoutChanges':engine.get('layoutChanges',[]),'requiresGameIntegration':engine.get('requiresGameIntegration',False)}
    print('AUDIT',json.dumps(result),flush=True)
    (OUT/f'{id}-report.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


reports=[check(id) for id in IDS]
manifest={'purpose':'all eight chapter-1 technical layouts for later 2D artwork','blender':bpy.app.version_string,'sourceCommand':'blender --background --factory-startup --threads 8 --python-exit-code 1 --python scripts/blender/chapter_layouts.py',
          'auditCommand':'blender --background --threads 8 --python-exit-code 1 --python scripts/blender/audit_chapter.py','scenes':reports,'productionChanged':False,
          'inputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__).resolve(),ROOT/'scripts/blender/chapter_layouts.py',ROOT/'scripts/blender/layout_math.py',ROOT/'scripts/blender/export-chapter.ts',ROOT/'art/blender/gate-pilot.blend',ROOT/'docs/blender-chapter-1/manifest.json']}}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('PASS: 8 saved scenes, 616 full cells, props, endpoints, bridges and gate sweep',flush=True)
