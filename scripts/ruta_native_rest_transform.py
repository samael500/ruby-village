"""Pure-Python read-only point mapping for root-owned accessories on source coordinates."""
def transform_point(point,bone_name,contract):
 b=contract['bones'][bone_name]
 return tuple(b['newHead'][j]+b['scale']*(point[j]-b['oldHead'][j])for j in range(3))
def transform_weighted_point(point,weights,contract):
 valid=[(name,w)for name,w in weights.items()if name in contract['bones'] and w>0];total=sum(w for name,w in valid)
 if not total:return tuple(x*contract['parameters']['body']for x in point)
 return tuple(sum(transform_point(point,name,contract)[j]*w for name,w in valid)/total for j in range(3))
