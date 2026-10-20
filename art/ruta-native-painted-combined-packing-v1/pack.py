"""Lossless ONE union-ROI atlas, no per-frame transforms. Explicit --run only."""
from pathlib import Path
import argparse,hashlib,json,math
from PIL import Image
O=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-loop-v1'));p.add_argument('--run',action='store_true');a=p.parse_args();expected='b14cfb5bfd8f15922c3c736c7b827b9d1ca6c5d1143d257012443fbf140a2db7';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if not a.run:print('PREPARED ONLY; use --run after root render-complete trigger');return
 cpath=a.input/'source-contract.json';contracthash=sha(cpath);contract=json.loads(cpath.read_text());assert contract['sourceSha256']==expected and contract['sourceUnchanged'];assert contract['renderedFrameCount']==48;clip=contract['cameraVariants']['base']['directions']['e']['clips']['walk'];assert len(clip['frames'])==48
 images=[];rows=[];boxes=[];anchors=[]
 for i,row in enumerate(clip['frames']):
  assert row['index']==i and abs(row['sourceFrame']-40*i/48)<1e-8;f=a.input/row['file'];assert f.is_file() and sha(f)==row['sha256'];im=Image.open(f);assert im.size==(512,640) and im.mode=='RGBA';im.load();images.append(im);box=im.getchannel('A').getbbox();assert box;boxes.append(box);anchors.append(row['worldOriginAnchorPx']);rows.append({'index':i,'sourceFile':str(f),'sourceSha256':row['sha256'],'sourceFrame':row['sourceFrame'],'alphaBoundsAny':box})
 assert all(x==anchors[0]for x in anchors)
 raw=[min(b[0]for b in boxes)-8,min(b[1]for b in boxes)-8,max(b[2]for b in boxes)+8,max(b[3]for b in boxes)+8];assert raw[0]>=0 and raw[1]>=0 and raw[2]<=512 and raw[3]<=640,'Margin would cross originalcanvas: explicit decision required';roi=tuple(raw);w,h=roi[2]-roi[0],roi[3]-roi[1];cols=min(8,4096//w);assert cols>0;nr=math.ceil(48/cols);assert nr*h<=4096,'Single atlas exceeds4096; no silent split';atlas=Image.new('RGBA',(cols*w,nr*h))
 for i,im in enumerate(images):
  crop=im.crop(roi);restored=Image.new('RGBA',(512,640));restored.paste(crop,roi[:2]);# OutsideROI may contain invisibleRGB; losslessness is asserted for kept rectangle and nonzeroalpha only.
  assert restored.getchannel('A').tobytes()==im.getchannel('A').tobytes();atlas.paste(crop,((i%cols)*w,(i//cols)*h));rows[i]['atlasRect']=[(i%cols)*w,(i//cols)*h,w,h];rows[i]['roiRGBAHash']=hashlib.sha256(crop.tobytes()).hexdigest()
 out=O/'atlas.png';atlas.save(out,compress_level=9);decoded=Image.open(out).convert('RGBA')
 for i,im in enumerate(images):
  x,y,_,_=rows[i]['atlasRect'];assert decoded.crop((x,y,x+w,y+h)).tobytes()==im.crop(roi).tobytes()
 assert sha(cpath)==contracthash;assert all(sha(Path(row['sourceFile']))==row['sourceSha256']for row in rows);r={'status':'MECHANICAL LOSSLESS GLOBAL ROI, NOT ART/RUNTIME ACCEPTANCE','sourceSha256':expected,'sourceContractSha256':sha(cpath),'sourceCanvas':[512,640],'globalCropRectXYWH':[roi[0],roi[1],w,h],'marginPixels':8,'fixedRootAnchorOriginalPx':anchors[0],'fixedRootAnchorCroppedPx':[anchors[0][0]-roi[0],anchors[0][1]-roi[1]],'durationSeconds':40/24,'frameCount':48,'atlas':{'file':'atlas.png','sha256':sha(out),'size':list(atlas.size),'bytes':out.stat().st_size,'columns':cols},'decodedFrameBytesBefore':48*512*640*4,'decodedFrameBytesAfter':48*w*h*4,'atlasDecodedBytes':atlas.width*atlas.height*4,'pixelPolicy':'All retained RGBA bytes exact; discarded pixels alpha0. InvisibleRGB outsideROI discarded, not claiming originalfullcanvasRGBAhashidentity.','alphaRestorationExactAll48':True,'decodedAtlasROIRGBAExactAll48':True,'frames':rows};(O/'manifest.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k]for k in ['globalCropRectXYWH','decodedFrameBytesBefore','decodedFrameBytesAfter','atlasDecodedBytes']},indent=2))
if __name__=='__main__':main()
