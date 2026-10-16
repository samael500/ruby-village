"""Deterministic gate placement constrained by full projected game-cell polygons."""
import json
import math


def hull(points):
    pts=sorted(set(points))
    def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    lower=[]; upper=[]
    for p in pts:
        while len(lower)>1 and cross(lower[-2],lower[-1],p)<=0:lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper)>1 and cross(upper[-2],upper[-1],p)<=0:upper.pop()
        upper.append(p)
    return lower[:-1]+upper[:-1]


def area(poly):
    return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1])))/2 if poly else 0


def overlap(subject,clip):
    result=list(subject)
    for a,b in zip(clip,clip[1:]+clip[:1]):
        def side(p):return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
        previous=result[-1] if result else None
        new=[]
        for p in result:
            before=side(previous); after=side(p)
            if (before>=0)!=(after>=0):
                t=before/(before-after)
                new.append((previous[0]+t*(p[0]-previous[0]),previous[1]+t*(p[1]-previous[1])))
            if after>=0:new.append(p)
            previous=p
        result=new
        if not result:break
    return area(result)


def bounds(poly):return min(p[0] for p in poly),min(p[1] for p in poly),max(p[0] for p in poly),max(p[1] for p in poly)


def make_layout(root):
    engine=json.loads((root/'docs/blender-chapter-1/geometry/gate-engine.json').read_text())
    assert engine['sceneId']=='gate' and engine['camera']=={'radius':70,'origin':{'x':140,'y':290},'angle':0,'groundScale':.65}
    byid={c['id']:c for c in engine['cells']}
    def world(point):return ((point['x']-140)/100,(290-point['y'])/65)
    goal=world(engine['goal']['pixel'])
    previous=min((byid[p['cellId']] for p in engine['solution']),key=lambda c:math.dist(world(c['center']),goal))
    prev=world(previous['center']); dx,dy=goal[0]-prev[0],goal[1]-prev[1]; length=math.hypot(dx,dy)
    direction=(dx/length,dy/length); normal=(-direction[1],direction[0])
    width=1.9; post=.16; post_height=1.10; height=1.00
    # Hinge on the right post: opening outward keeps the leaf inside the export frame.
    closed=math.atan2(-normal[1],-normal[0])-math.pi/2
    opened=closed+math.radians(95)
    def pixel(x,y,z):return (140+100*x,290-65*y-100*math.sqrt(1-.65**2)*z)
    free=[]
    for c in engine['cells']:
        if c['terrain']:continue
        poly=[(p['x'],p['y']) for p in c['polygon']]
        free.append((poly,bounds(poly)))
    def clear(poly):
        bb=bounds(poly)
        for cell,cb in free:
            if bb[0]>=cb[2] or cb[0]>=bb[2] or bb[1]>=cb[3] or cb[1]>=bb[3]:continue
            if overlap(poly,cell)>.01:return False
        return True
    def box_poly(center,size):
        return hull([pixel(center[0]+sx*size[0]/2,center[1]+sy*size[1]/2,z) for sx in [-1,1] for sy in [-1,1] for z in [0,size[2]]])
    candidates=[]
    # Search only a short continuation of the incoming route, with a small lateral bend.
    for step in range(60,151):
        distance=step*.025
        for shift in range(-14,5):
            lateral=shift*.05
            center=(goal[0]+distance*direction[0]+lateral*normal[0],goal[1]+distance*direction[1]+lateral*normal[1])
            left=(center[0]-width/2*normal[0],center[1]-width/2*normal[1])
            right=(center[0]+width/2*normal[0],center[1]+width/2*normal[1])
            if not all(clear(box_poly(p,(post+.04,post+.04,post_height+.04))) for p in [left,right]):continue
            valid=True
            for i in range(12):
                angle=closed+(opened-closed)*i/11
                ux,uy=-math.sin(angle),math.cos(angle)
                vx,vy=math.cos(angle),math.sin(angle)
                poly=hull([pixel(right[0]+t*ux+s*vx,right[1]+t*uy+s*vy,z) for t in [0,width] for s in [-.07,.07] for z in [0,height]])
                if not clear(poly) or any(not (2<x<1670 and 2<y<939) for x,y in poly):valid=False;break
            if valid:
                px,py=pixel(*center,0); gp=engine['goal']['pixel']
                score=math.hypot(px-gp['x'],py-gp['y'])+.03*abs(lateral)
                candidates.append((score,center,left,right,distance,lateral))
    assert candidates,'No gate layout preserves the full game field'
    score,center,left,right,distance,lateral=min(candidates)
    # Extra margin for render bevels and finite precision, along the outward route.
    margin=.08
    center=tuple(center[i]+margin*direction[i] for i in range(2))
    left=tuple(left[i]+margin*direction[i] for i in range(2)); right=tuple(right[i]+margin*direction[i] for i in range(2))
    goal_cell=byid[f"{engine['goal']['q']},{engine['goal']['r']}"]
    # A flat, walkable arrival court joins the whole goal hex to the opening.
    # It is compacted earth, not puzzle paving or a pre-built bridge.
    court=hull([world(p) for p in goal_cell['polygon']]+[(left[0]+.25*direction[0],left[1]+.25*direction[1]),(right[0]+.25*direction[0],right[1]+.25*direction[1])])
    return {'goal':goal,'incomingDirection':direction,'normal':normal,'openingCenter':center,'leftPost':left,'rightPost':right,'hinge':right,'latchPost':left,'width':width,'height':height,'postHeight':post_height,'closedAngle':closed,'openAngle':opened,'court':court,'approachLengthWorld':math.dist(goal,center),'searchCandidateCount':len(candidates)}
