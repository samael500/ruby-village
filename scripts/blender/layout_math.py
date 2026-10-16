"""Convex geometry used for layout construction. Audit reads the saved meshes."""
import math


def signed(poly):
    return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1]))/2 if poly else 0


def area(poly):return abs(signed(poly))


def intersection(subject,clip):
    if signed(clip)<0:clip=list(reversed(clip))
    result=list(subject)
    for a,b in zip(clip,clip[1:]+clip[:1]):
        def side(p):return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
        previous=result[-1] if result else None; new=[]
        for p in result:
            before=side(previous); after=side(p)
            if (before>=0)!=(after>=0):
                t=before/(before-after)
                new.append((previous[0]+t*(p[0]-previous[0]),previous[1]+t*(p[1]-previous[1])))
            if after>=0:new.append(p)
            previous=p
        result=new
        if not result:break
    return result


def hull(points):
    points=sorted(set(points)); lower=[]; upper=[]
    def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    for p in points:
        while len(lower)>1 and cross(lower[-2],lower[-1],p)<=0:lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper)>1 and cross(upper[-2],upper[-1],p)<=0:upper.pop()
        upper.append(p)
    return lower[:-1]+upper[:-1]


def bounds(poly):return min(x for x,y in poly),min(y for x,y in poly),max(x for x,y in poly),max(y for x,y in poly)


def touching(a,b):
    aa,bb=bounds(a),bounds(b)
    return not (aa[0]>=bb[2] or bb[0]>=aa[2] or aa[1]>=bb[3] or bb[1]>=aa[3])


class Geometry:
    def __init__(self,engine):
        self.engine=engine; self.scale=engine['camera']['groundScale']; self.origin=engine['camera']['origin']
        self.polygons={c['id']:[(p['x'],p['y']) for p in c['polygon']] for c in engine['cells']}
        self.free=[self.polygons[c['id']] for c in engine['cells'] if not c['terrain']]
        self.blocked=[self.polygons[c['id']] for c in engine['cells'] if c['terrain']]
        self.water=[self.polygons[c['id']] for c in engine['cells'] if c['terrain']=='water']

    def world(self,p):return ((p['x']-self.origin['x'])/100,(self.origin['y']-p['y'])/(100*self.scale),0)

    def pixel(self,p):return (self.origin['x']+100*p[0],self.origin['y']-100*self.scale*p[1]-100*math.sqrt(1-self.scale**2)*p[2])

    def clear(self,vertices,water=True):
        for ground in [False,True]:
            poly=hull([self.pixel((x,y,0 if ground else z)) for x,y,z in vertices])
            if not ground and any(x<12 or y<12 or x>1660 or y>929 for x,y in poly):return False
            if any(touching(poly,c) and area(intersection(poly,c))>.03 for c in self.free+(self.water if water else [])):return False
        return True

    def court_clear(self,poly):
        pixels=[self.pixel((*p,0)) for p in poly]
        return all(not touching(pixels,c) or area(intersection(pixels,c))<.03 for c in self.blocked)

    def boundary(self):
        """Directed blocker edges with outward normals; internal edges excluded."""
        edges={}
        for c in self.engine['cells']:
            if not c['terrain'] or c['terrain']=='water':continue
            pts=[self.world(p)[:2] for p in c['polygon']]
            for a,b in zip(pts,pts[1:]+pts[:1]):
                key=tuple(sorted((tuple(round(v,5) for v in a),tuple(round(v,5) for v in b))))
                if key in edges:del edges[key]
                else:edges[key]=(a,b,c)
        for a,b,c in edges.values():
            center=self.world(c['center']); mid=((a[0]+b[0])/2,(a[1]+b[1])/2)
            dx,dy=b[0]-a[0],b[1]-a[1]; length=math.hypot(dx,dy); u=(dx/length,dy/length); n=(-u[1],u[0])
            if (center[0]-mid[0])*n[0]+(center[1]-mid[1])*n[1]>0:n=(-n[0],-n[1])
            yield mid,u,n,c


def box_vertices(mid,u,n,width,depth,height):
    """Front edge on a terrain boundary; body extends inward."""
    return [(mid[0]+t*u[0]-d*n[0],mid[1]+t*u[1]-d*n[1],z)
            for t in [-width/2,width/2] for d in [.002,depth] for z in [0,height]]


def terminal(g,anchor,kind):
    cell=g.polygons[f"{anchor['q']},{anchor['r']}"]
    center=g.world(anchor['pixel']); goal=[g.world({'x':x,'y':y})[:2] for x,y in cell]
    sizes=([(1.8,1.2,1.35),(1.3,1,1.15),(.95,.8,1.0),(.65,.6,.80),(.48,.5,.65)] if kind=='house'
           else [(.95,.70,.70),(.70,.55,.55),(.48,.40,.40)])
    choices=[]
    for mid,u,n,c in g.boundary():
        if c['terrain']=='tree' and kind=='house':continue
        court=hull(goal+[(mid[0]+t*u[0],mid[1]+t*u[1]) for t in [-.22,.22]])
        if not g.court_clear(court):continue
        for width,depth,height in sizes:
            vertices=box_vertices(mid,u,n,width,depth,height)
            if not g.clear(vertices):continue
            distance=math.dist(mid,center[:2])
            # Prefer a human-sized proxy when several fit along the same boundary.
            score=distance+.30/(width*depth)
            choices.append((score,{'point':mid,'across':u,'outward':n,'width':width,'depth':depth,'height':height,'court':court,'distance':distance,'kind':kind,'boundaryCell':c['id']}))
            break
    if not choices:return exterior_terminal(g,anchor,kind)
    return min(choices,key=lambda v:v[0])[1]


def exterior(g,anchor,role):
    center=g.world(anchor['pixel'])[:2]
    cell=g.polygons[f"{anchor['q']},{anchor['r']}"]
    full=[g.world({'x':x,'y':y})[:2] for x,y in cell]
    board=hull([p for poly in g.polygons.values() for p in poly]); choices=[]
    for i in range(32):
        angle=math.tau*i/32; n=(math.cos(angle),math.sin(angle)); u=(-n[1],n[0])
        for step in range(10,121):
            distance=step*.05; point=(center[0]+distance*n[0],center[1]+distance*n[1])
            if area(intersection([g.pixel((*point,0)),g.pixel((point[0]+.001,point[1],0)),g.pixel((point[0],point[1]+.001,0))],board))>0:continue
            width=1.65; depth=.13; height=.85
            verts=[(point[0]+t*u[0]+d*n[0],point[1]+t*u[1]+d*n[1],z)
                   for t in [-width/2,width/2] for d in [-.08,.08] for z in [0,height]]
            # Only the two posts are solid; the full opening remains walkable.
            posts=[]
            for side in [-1,1]:
                p=(point[0]+side*width/2*u[0],point[1]+side*width/2*u[1])
                posts.append([(p[0]+dx,p[1]+dy,z) for dx in [-.075,.075] for dy in [-.075,.075] for z in [0,height]])
            if not all(g.clear(v) for v in posts):continue
            court=hull(full+[(point[0]+t*u[0]+.22*n[0],point[1]+t*u[1]+.22*n[1]) for t in [-.65,.65]])
            if not g.court_clear(court):continue
            score=math.dist(g.pixel((*point,0)),(anchor['pixel']['x'],anchor['pixel']['y']))
            choices.append((score,{'point':point,'across':u,'outward':n,'width':width,'depth':depth,'height':height,'court':court,'distance':distance,'kind':'portal','role':role}))
            break
    assert choices,('No exterior approach',g.engine['sceneId'],role)
    return min(choices,key=lambda v:v[0])[1]


def exterior_terminal(g,anchor,kind):
    center=g.world(anchor['pixel'])[:2]
    full=[g.world({'x':x,'y':y})[:2] for x,y in g.polygons[f"{anchor['q']},{anchor['r']}"]]
    sizes=[(1.20,.80,.75),(.90,.65,.60)]
    choices=[]
    for i in range(32):
        a=math.tau*i/32;travel=(math.cos(a),math.sin(a));u=(-travel[1],travel[0]);n=(-travel[0],-travel[1])
        for step in range(8,121):
            distance=step*.05;point=(center[0]+distance*travel[0],center[1]+distance*travel[1])
            court=hull(full+[(point[0]+t*u[0],point[1]+t*u[1]) for t in [-.35,.35]])
            if not g.court_clear(court):continue
            for w,d,h in sizes:
                if not g.clear(box_vertices(point,u,n,w,d,h)):continue
                score=math.dist(g.pixel((*point,0)),(anchor['pixel']['x'],anchor['pixel']['y']))+.15/w
                choices.append((score,{'point':point,'across':u,'outward':n,'width':w,'depth':d,'height':h,'court':court,'distance':distance,'kind':kind,'boundaryCell':None}))
                break
            if choices and choices[-1][1]['point']==point:break
    assert choices,('No exterior terminal',g.engine['sceneId'],kind)
    return min(choices,key=lambda v:v[0])[1]
