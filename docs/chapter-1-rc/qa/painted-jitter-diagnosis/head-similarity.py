"""Analysis only: head-window similarity does not justify whole-body scaling."""
exec(open(__file__.replace('head-similarity.py','head-template.py')).read().split('upper=(55,25')[0])
t=json.loads((O/'head-template.json').read_text()); yy,xx=np.mgrid[25:72,55:102];target=c[0][25:72,55:102];cx,cy=80,48
# Whole-head diagnostic ROI; no image outputs, not used to modify pivots.
def score(img,p):
 dx,dy,scale,deg=p;rad=deg*np.pi/180;ux=xx-cx;uy=yy-cy;rx=cx+scale*(np.cos(rad)*ux-np.sin(rad)*uy)+dx;ry=cy+scale*(np.sin(rad)*ux+np.cos(rad)*uy)+dy
 q=sample(img,rx,ry,0,0);e=(q-target)**2;return float(e.mean()),float(e[:24].mean()),float(e[25:].mean())
rows=[]
for i in [0,8,16,24,25,26,27,28,29,30,31,32,40,47]:
 p=list(t['rows'][i]['cyclicGraphShift'])+[1.,0.];initial=score(c[i],p)
 for step in [.5,.125,.03125]:
  for _ in range(24):
   old=p.copy()
   for axis in [0,1]:
    opts=[]
    for k in [-1,0,1]:
     q=p.copy();q[axis]+=step*k;opts.append((score(c[i],q)[0],q))
    p=min(opts,key=lambda x:x[0])[1]
   if p==old:break
 translationOptimal=score(c[i],p)
 for steps in [[.5,.5,.01,1.],[.125,.125,.0025,.25],[.03125,.03125,.000625,.0625]]:
  for _ in range(24):
   old=p.copy();base=score(c[i],p)[0]
   for axis,step in enumerate(steps):
    opts=[]
    for k in [-1,0,1]:
     q=p.copy();q[axis]+=step*k
     if not(.85<=q[2]<=1.15 and abs(q[3])<=8):continue
     opts.append((score(c[i],q)[0],q))
    val,q=min(opts,key=lambda x:x[0]);p=q
   if p==old:break
 rows.append({'phase':i,'graphTranslationMseUpperLower':initial,'translationOnlyMseUpperLower':translationOptimal,'headSimilarityMseUpperLower':score(c[i],p),'headSimilarityParameters':{'dx':p[0],'dy':p[1],'scale':p[2],'rotationDegrees':p[3]},'notWholeActorEvidence':True})
report={'scope':'diagnostic only; head fitting no pixel or pivot changes; cannot justify global scale/rotation without torso/limb correspondence','fixedTemplate':0,'headROI':[55,25,102,72],'pivot':[cx,cy],'rows':rows};(O/'head-similarity.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
