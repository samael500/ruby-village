"""Build all eight technical Blender layouts; deliberately no final artwork.
blender --background --factory-startup --threads 8 --python-exit-code 1 --python scripts/blender/chapter_layouts.py -- --scene all
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from layout_math import Geometry,area,hull,box_vertices,terminal,exterior
OUT=ROOT/'docs/blender-chapter-1/layouts'
SOURCES=ROOT/'art/blender/chapter-layouts'
IDS=['gate','garden','well','bakery','stream','mill','post','forest']
p=argparse.ArgumentParser();p.add_argument('--scene',choices=IDS+['all'],default='all');p.add_argument('--build-only',action='store_true')
args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
SOURCES.mkdir(exist_ok=True);(OUT/'renders').mkdir(exist_ok=True)
COLORS={'earth':(.72,.76,.57,1),'house':(.57,.43,.31,1),'tree':(.29,.47,.29,1),'flower':(.65,.43,.53,1),'water':(.24,.55,.66,1),
        'wall':(.85,.73,.53,1),'roof':(.59,.31,.23,1),'wood':(.39,.27,.17,1),'court':(.77,.66,.45,1),'stone':(.52,.53,.49,1),
        'start':(.29,.65,.51,1),'goal':(.91,.58,.24,1),'solution':(.53,.35,.71,1),'bridge':(.69,.49,.29,1),'ink':(.18,.23,.21,1)}


def build(id):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    engine=json.loads((OUT/'engine'/f'{id}.json').read_text());g=Geometry(engine)
    scene=bpy.context.scene; scene['sceneId']=id;scene['layoutPurpose']='technical geometry for later 2D redraw; not final art'
    if engine.get('layoutChanges'):
        scene['layoutChanges']=json.dumps(engine['layoutChanges'])
        scene['requiresGameIntegration']=True
    cols={}
    for name in ['ground','terrain','playable_contract','scenery','gate_closed','gate_open','verification','solution','bridge']:
        c=bpy.data.collections.new(name);scene.collection.children.link(c);cols[name]=c
    objects=[];approaches=[];landmarks=[]

    def mesh(name,verts,faces,color,col='scenery',solid=False):
        m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.update()
        o=bpy.data.objects.new(name,m);cols[col].objects.link(o);o.color=COLORS.get(color,color)
        o['clearanceRole']='solid' if solid else 'surface';objects.append(o)
        return o

    def box(name,center,size,color='wood',col='scenery',solid=True):
        verts=[(center[0]+sx*size[0]/2,center[1]+sy*size[1]/2,center[2]+sz*size[2]/2) for sx in [-1,1] for sy in [-1,1] for sz in [-1,1]]
        faces=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]
        return mesh(name,verts,faces,color,col,solid)

    def prism(name,polygon,top=0,depth=.08,color='earth',col='terrain',solid=False):
        if depth==0:return mesh(name,[(x,y,top) for x,y in polygon],[tuple(range(len(polygon)))],color,col,solid)
        n=len(polygon);cx=sum(x for x,y in polygon)/n;cy=sum(y for x,y in polygon)/n
        taper=.82 if col in ['solution','bridge'] else 1
        verts=[(x,y,top) for x,y in polygon]+[(cx+(x-cx)*taper,cy+(y-cy)*taper,top-depth) for x,y in polygon]
        faces=[tuple(range(n)),tuple(reversed(range(n,2*n)))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
        return mesh(name,verts,faces,color,col,solid)

    def beam(name,a,b,r,color='wood',col='scenery',solid=True):
        a,b=Vector(a),Vector(b);center=(a+b)/2;v=b-a
        o=box(name,(0,0,0),(r,r,v.length),color,col,solid);o.location=center;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();return o

    def ring(name,center,radius,height,color='stone',col='scenery',solid=True):
        vs=[];n=16
        for z in [center[2],center[2]+height]:
            for r in [radius,radius*.70]:
                vs.extend((center[0]+r*math.cos(i*math.tau/n),center[1]+r*math.sin(i*math.tau/n),z) for i in range(n))
        faces=[]
        for i in range(n):
            j=(i+1)%n
            faces.extend([(i,j,2*n+j,2*n+i),(n+i,3*n+i,3*n+j,n+j),(2*n+i,2*n+j,3*n+j,3*n+i)])
        return mesh(name,vs,faces,color,col,solid)

    def court(role,anchor,layout):
        poly=layout['court']; c=g.world(anchor['pixel']);verts=[c]+[(x,y,-.004) for x,y in poly]
        o=mesh(role+' approach',verts,[(0,i+1,(i+1)%len(poly)+1) for i in range(len(poly))],'court','ground')
        o['approachRole']=role;o['anchorVertex']=0;o['endpoint']=list(layout['point'])+[0]
        approaches.append({'role':role,'object':o.name,'landmark':layout,'anchor':anchor})

    def transformed(mid,u,n,t,d,z):return (mid[0]+t*u[0]-d*n[0],mid[1]+t*u[1]-d*n[1],z)

    def oriented_box(name,layout,width,depth,height,color,front=0,z0=0):
        mid,u,n=layout['point'],layout['across'],layout['outward']
        verts=[transformed(mid,u,n,t,d,z) for t in [-width/2,width/2] for d in [front,front+depth] for z in [z0,z0+height]]
        return mesh(name,verts,[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)],color,solid=True)

    def landmark(role,anchor,kind):
        layout=terminal(g,anchor,kind);mid,u,n=layout['point'],layout['across'],layout['outward'];w,d,h=layout['width'],layout['depth'],layout['height']
        if kind=='house':
            oriented_box(role+' entrance bay',layout,w,d,h*.82,'wall',.002)
            # A larger connected main volume sits behind the entrance bay, where it fits.
            mass=None
            for mw,md,mh in [(2.4,1.4,1.7),(2.0,1.2,1.5),(1.6,1.0,1.25),(1.2,.8,1.1)]:
                for front in [.6,.8,1.0,1.2]:
                    shifted=(mid[0]-front*n[0],mid[1]-front*n[1])
                    if not g.clear(box_vertices(shifted,u,n,mw,md,mh)):continue
                    # Keep entrance and main volume connected by a narrow solid vestibule.
                    if not g.clear(box_vertices(mid,u,n,w*.6,front+.04,h*.70)):continue
                    mass=(mw,md,mh,front);break
                if mass:break
            if mass:
                mw,md,mh,front=mass
                oriented_box(role+' vestibule',layout,w*.6,front+.04,h*.70,'wall',.002)
                oriented_box(role+' main building',layout,mw,md,mh*.70,'wall',front)
                verts=[transformed(mid,u,n,t,dd,z) for dd in [front,front+md] for t,z in [(-mw/2,mh*.70),(mw/2,mh*.70),(0,mh)]]
                mesh(role+' pitched roof',verts,[(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2),(2,5,3,0)],'roof',solid=True)
                layout['mainVolume']={'width':mw,'depth':md,'height':mh,'front':front}
            oriented_box(role+' porch roof',layout,w,d,.04,'roof',.002,z0=h*.82)
            door=oriented_box(role+' doorway',layout,w*.66,.008,h*.68,'wood',.0002)
            door['entrancePoint']=list(mid)+[0]
            if id in ['bakery','post']:
                # Clear icon silhouettes on the actual facade, not new obstacles.
                oriented_box('bread shelf' if id=='bakery' else 'letter panel',layout,w*.55,.012,h*.18,'bridge' if id=='bakery' else 'goal',.0001,z0=h*.60)
        elif kind=='well':
            center=transformed(mid,u,n,0,d*.53,0);r=min(w/2,d*.46)
            ring('well masonry',center,r,h*.42)
            for side in [-1,1]:
                a=transformed(mid,u,n,side*w*.35,d*.5,.05);b=(*a[:2],h*.85)
                beam('well upright',a,b,.045)
            beam('well crossbar',transformed(mid,u,n,-w*.36,d*.5,h*.82),transformed(mid,u,n,w*.36,d*.5,h*.82),.05)
            ring('well bucket',transformed(mid,u,n,0,d*.5,h*.20),r*.3,h*.15,'wood')
        elif kind=='table':
            oriented_box('garden table top',layout,w,d,.04,'bridge',.002,z0=h*.82)
            for t in [-w*.38,w*.38]:
                for dd in [d*.18,d*.82]:
                    a=transformed(mid,u,n,t,dd,.02);beam('table leg',a,(*a[:2],h*.82),.05)
            oriented_box('apple basket',layout,w*.30,d*.35,h*.15,'wood',d*.35,z0=h*.86)
        else:
            a=transformed(mid,u,n,0,d*.5,0);beam('forest signpost',a,(*a[:2],h*.88),.055)
            oriented_box('forest sign board',layout,w,.035,h*.22,'bridge',d*.5,z0=h*.65)
        court(role,anchor,layout);landmarks.append({'role':role,'kind':kind,**layout})
        return layout

    def portal(role,anchor):
        layout=exterior(g,anchor,role);p,u=layout['point'],layout['across'];width=layout['width']
        for side in [-1,1]:
            x,y=p[0]+side*width/2*u[0],p[1]+side*width/2*u[1]
            box(role+' entrance post',(x,y,.425),(.15,.15,.85))
        court(role,anchor,layout);landmarks.append({'role':role,**layout})

    # Every exact cap is a real mesh. Ground masks, never a picture on a plane.
    for c in engine['cells']:
        poly=[g.world(v)[:2] for v in c['polygon']];terrain=c['terrain']
        color=terrain or 'earth'
        if terrain=='house' and (id=='forest' or c['r']>1 and c['q']<1):color='tree'
        o=prism('terrain '+c['id'] if terrain else 'ground '+c['id'],poly,depth=0 if terrain=='water' else .08,color=color,col='terrain' if terrain else 'playable_contract')
        o['cellId']=c['id'];o['engineTerrain']=terrain or '';o['capFace']=0
        o['semanticRole']=('forest boundary' if id=='forest' else 'perimeter planting') if terrain=='house' and color=='tree' else terrain or 'walkable'
        # Independent diagnostic lines; not part of clean exports.
        for i,(a,b) in enumerate(zip(poly,poly[1:]+poly[:1])):
            beam('grid '+c['id']+' '+str(i),(*a,.004),(*b,.004),.009,'ink','verification',False)
        if terrain=='water':
            # The shoreline is the actual polygon edge. No extra dry strips over water.
            for i,(a,b) in enumerate(zip(poly,poly[1:]+poly[:1])):
                edge=tuple(sorted((tuple(round(v,5) for v in a),tuple(round(v,5) for v in b))))
                # Stored for independent shore extraction by the audit.
                o['waterCell']=True
    # Wide real ground extends past the fixed export crop, never a mirrored image.
    prism('outside ground',[(-10,-15),(25,-15),(25,12),(-10,12)],top=-.012,depth=.05,color='earth',col='ground')

    for role in ['start','goal']:
        anchor=engine[role];c=g.world(anchor['pixel'])
        empty=bpy.data.objects.new(role+' ground anchor',None);cols['verification'].objects.link(empty);empty.location=c
        empty['cellId']=f"{anchor['q']},{anchor['r']}"
        poly=[g.world(v)[:2] for v in engine['cells'][next(i for i,c in enumerate(engine['cells']) if c['id']==empty['cellId'])]['polygon']]
        prism(role+' highlight',poly,top=.007,depth=.002,color=role,col='verification')
        if id=='gate' and role=='goal':
            # Copy only accepted moving gate and continuous fence. All transforms preserved.
            old=ROOT/'art/blender/gate-pilot.blend'
            with bpy.data.libraries.load(str(old),link=False) as (available,loaded):
                loaded.objects=[name for name in available.objects if name.startswith(('fence post','fence rail','post cap','gate vertical','gate cross','gate diagonal','gate brass','hinge gate'))]
            for o in loaded.objects:
                if o is None:continue
                state='gate_open' if (o.parent and o.parent.name=='hinge gate_open') or o.name=='hinge gate_open' else 'gate_closed' if (o.parent and o.parent.name=='hinge gate_closed') or o.name=='hinge gate_closed' else 'scenery'
                cols[state].objects.link(o);o.color=COLORS['wood'];o['clearanceRole']='solid';o['acceptedGateTransform']=True
            old_layout=json.loads((ROOT/'docs/blender-chapter-1/manifest.json').read_text())['gateLayout']
            layout={**old_layout,'point':old_layout['openingCenter'],'kind':'accepted gate'}
            scene['gate_layout_json']=json.dumps(old_layout);court(role,anchor,layout);landmarks.append({'role':role,**layout})
        elif (id=='gate' and role=='start') or (role=='goal' and id in ['bakery','post','mill']):landmark(role,anchor,'house')
        elif role=='goal' and id in ['garden','well','forest']:landmark(role,anchor,{'garden':'table','well':'well','forest':'sign'}[id])
        elif id=='stream' or id=='mill':
            layout={'point':c[:2],'court':poly,'kind':'bank landing','distance':0}
            court(role,anchor,layout);landmarks.append({'role':role,**layout})
        else:portal(role,anchor)

    # Fit semantic tree/flower proxies inside their exact reserved ground AND silhouette.
    for c in engine['cells']:
        t=c['terrain'];x,y,_=g.world(c['center'])
        if t not in ['tree','flower'] and not (t=='house' and (id=='forest' or c['r']>1 and c['q']<1)):continue
        if t=='flower':
            height=.15;radius=.21
        else:
            height=.85;radius=.30
        verts=[(x+dx,y+dy,z) for dx in [-radius,radius] for dy in [-radius,radius] for z in [0,height]]
        if not g.clear(verts):continue
        if t=='flower':
            box('raised flower bed '+c['id'],(x,y,.04),(.42,.42,.08),'flower')
            for dx in [-.10,.10]:box('flower marker '+c['id'],(x+dx,y,.12),(.09,.09,.06),'goal')
        else:
            box('tree trunk '+c['id'],(x,y,.28),(.10,.10,.56),'wood')
            # Octagonal low-poly canopy remains within the checked box.
            poly=[(x+radius*math.cos(i*math.tau/8),y+radius*math.sin(i*math.tau/8)) for i in range(8)]
            prism('tree canopy '+c['id'],poly,top=height,depth=.42,color='tree',col='scenery',solid=True)

    # Mill wheel remains its own physical object, contained in the mill's reserved area.
    if id=='mill':
        l=next(v for v in landmarks if v['role']=='goal')
        top_water=min((c for c in engine['cells'] if c['terrain']=='water'),key=lambda c:c['r'])
        wx,wy,_=g.world(top_water['center']);x=l['point'][0]-1.3
        y=1.15;center=(x,y,.58);r=.56
        extension=hull([g.world(v)[:2] for v in top_water['polygon']]+[(wx-.18,y+.12),(wx+.18,y+.12)])
        assert g.clear([(*p,0) for p in extension],water=False)
        o=prism('mill stream extension',extension,depth=0,color='water',col='terrain');o['waterExtension']=True
        race=[(wx,y-.12),(x+.2,y-.12),(x+.2,y+.12),(wx,y+.12)]
        assert g.clear([(*p,0) for p in race],water=False)
        o=prism('mill race outside board',race,depth=0,color='water',col='terrain');o['waterExtension']=True
        wheel=ring('mill wheel',(0,0,0),r,.08,'wood');wheel.location=center;wheel.rotation_euler[0]=math.pi/2
        wheel['interactiveRole']='mill wheel';wheel['rotationAxis']='Y'
        for a in range(8):
            angle=a*math.tau/8;beam('wheel spoke',center,(center[0]+r*math.cos(angle),center[1],center[2]+r*math.sin(angle)),.025)

    for piece in engine['pieces']:
        for ident in piece['cells']:
            poly=[g.world({'x':x,'y':y})[:2] for x,y in g.polygons[ident]]
            col='bridge' if piece['kind']=='bridge' else 'solution'
            o=prism('bridge deck '+ident if col=='bridge' else 'solution '+ident,poly,top=0,depth=.045,color=col,col=col)
            o['cellId']=ident;o['pieceId']=piece['id'];o['pieceKind']=piece['kind'];o['capFace']=0
            if col=='bridge':
                # Separate wood seams; all inside the exact three-cell bridge mask.
                cx,cy,_=g.world(next(c['center'] for c in engine['cells'] if c['id']==ident))
                for shift in [-.3,0,.3]:beam('bridge plank seam',(cx-.37,cy+shift,.006),(cx+.37,cy+shift,.006),.008,'wood','bridge',False)

    # Camera: source mesh ground is already rotated by the engine's per-scene angle.
    # Fixed 100px/world-unit camera exactly reproduces those exported polygons.
    w,h=engine['resolution'];s=g.scale
    target=Vector(((w/2-g.origin['x'])/100,(g.origin['y']-h/2)/(100*s),0))
    camera_data=bpy.data.cameras.new('calibrated camera');camera=bpy.data.objects.new('calibrated camera',camera_data);scene.collection.objects.link(camera)
    camera.location=target+Vector((0,-math.sqrt(1-s*s)*30,s*30));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.type='ORTHO';camera.data.ortho_scale=w/100;scene.camera=camera
    scene.render.resolution_x=w;scene.render.resolution_y=h;scene.render.resolution_percentage=100
    scene.render.engine='BLENDER_WORKBENCH';scene.display.shading.light='STUDIO';scene.display.shading.color_type='OBJECT'
    scene.display.shading.show_shadows=False;scene.display.shading.show_cavity=True;scene.display.shading.cavity_type='BOTH'
    scene.display.shading.background_type='WORLD';scene.world=bpy.data.worlds.new('technical backdrop');scene.world.color=(.72,.76,.57)
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.display.render_aa='16';scene.view_settings.view_transform='Standard'
    scene['approaches']=json.dumps(approaches);scene['landmarks']=json.dumps(landmarks)
    scene['engineSha256']=hashlib.sha256((OUT/'engine'/f'{id}.json').read_bytes()).hexdigest()
    scene['worldToPixel']=json.dumps([[100,0,0,g.origin['x']],[0,-100*s,-100*math.sqrt(1-s*s),g.origin['y']]])
    for name in ['verification','solution','bridge','gate_open','playable_contract']:cols[name].hide_render=True
    cols['playable_contract'].hide_viewport=True
    # Save useful startup view with the exact camera, clean state and separate collections.
    for screen in bpy.data.screens:
        for a in screen.areas:
            if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA'
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCES/f'{id}.blend'),compress=True)
    if not args.build_only:
        for state in ['clean','check','solved']:
            cols['verification'].hide_render=state=='clean'
            cols['solution'].hide_render=state!='solved';cols['bridge'].hide_render=state!='solved'
            cols['gate_closed'].hide_render=state=='solved';cols['gate_open'].hide_render=state!='solved'
            for o in cols['terrain'].objects:
                o.hide_render=state=='solved' and o.get('waterCell',False) and any(o.get('cellId') in piece['cells'] for piece in engine['pieces'] if piece['kind']=='bridge')
            scene.render.filepath=str(OUT/'renders'/f'{id}-{state}.png');bpy.ops.render.render(write_still=True)
        # Transparent exports keep diagnostics and the unbuilt bridge out of backgrounds.
        scene.render.film_transparent=True
        for o in cols['terrain'].objects:o.hide_render=False
        for layer,visible in [('background',{'ground','terrain','scenery'}),('solution',{'solution'}),('bridge',{'bridge'}),('gate_closed',{'gate_closed'}),('gate_open',{'gate_open'})]:
            if layer=='bridge' and id not in ['stream','mill']:continue
            if layer.startswith('gate_') and id!='gate':continue
            for name,c in cols.items():c.hide_render=name not in visible
            scene.render.filepath=str(OUT/'renders'/f'{id}-{layer}.png');bpy.ops.render.render(write_still=True)
    summary={'sceneId':id,'name':engine['name'],'resolution':[w,h],'source':f'art/blender/chapter-layouts/{id}.blend','engine':f'engine/{id}.json','engineSha256':scene['engineSha256'],
             'camera':{'engine':engine['camera'],'worldToPixel':json.loads(scene['worldToPixel']),'pixelToGround':[[.01,0,-g.origin['x']/100],[0,-1/(100*s),g.origin['y']/(100*s)]],
                       'note':'Mesh ground already includes engine angle; camera elevation asin(groundScale).'},
             'anchors':{role:engine[role] for role in ['start','goal']},'landmarks':landmarks,'collections':list(cols),'states':{'clean':'no grid, path or bridge','check':'grid/start/goal; no placed pieces','solved':'exact engine solution and built bridge; accepted gate open'},
             'exportRect':[0,0,w,h],'technicalLayout':True,'productionChanged':False}
    (OUT/f'{id}-layout.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
    print('BUILT',id,json.dumps(landmarks,ensure_ascii=False),flush=True)


for id in IDS if args.scene=='all' else [args.scene]:build(id)
