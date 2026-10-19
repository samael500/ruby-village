"""Derive headings once from accepted projected motion directions, not screen60deg."""
from pathlib import Path
import json,math,hashlib
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'public/assets/characters-walk-v1/animated-v3/manifest.json';j=json.loads(source.read_text());out={}
for key,variant in j['cameraVariants'].items():
 camera=variant['camera'];scale=camera['groundScale'];angle=camera['angle'];directions={}
 for name,spec in variant['directions'].items():
  screen=spec['screenAngleRadians'];native_after_camera=math.atan2(math.sin(screen)/scale,math.cos(screen));yaw=math.pi/2-native_after_camera
  projected=math.atan2(scale*math.cos(yaw),math.sin(yaw));err=math.atan2(math.sin(projected-screen),math.cos(projected-screen));assert abs(err)<1e-12
  directions[name]={'acceptedScreenAngleRadians':screen,'nativeHeadingAfterCameraRadians':native_after_camera,'stockForwardMinusYBlenderYawRadians':yaw,'reprojectionErrorRadians':err}
 out[key]={'camera':camera,'scenes':variant['scenes'],'directions':directions}
report={'status':'heading-contract-only-no-six-view-export','source':str(source.relative_to(ROOT)),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'erratum':'Original sixViewYawRadians unprojected artificial screen60deg increments. E was correct, diagonals were not accepted hex headings. Do not use old values as grid calibration.','rule':'Accepted motion screenAngleRadians -> one inverse groundScale projection -> stock forward -Y yaw. Includes camera angle exactly once; no second unprojection. Equivalently base yaw E minus native hex heading minus camera.angle.','variants':out}
(ROOT/'art/ready-character-walk-v1/heading-contract.json').write_text(json.dumps(report,indent=2)+'\n')
for folder in ['ready-character-walk-v1','ready-character-adapted-v1']:
 p=ROOT/'art'/folder/'contract.json'
 if p.exists():
  c=json.loads(p.read_text());c['sixViewCalibrationStatus']='old sixViewYawRadians prototype is invalid for grid diagonals; use ../ready-character-walk-v1/heading-contract.json before any six-view export';c['headingContract']='../ready-character-walk-v1/heading-contract.json';p.write_text(json.dumps(c,indent=2)+'\n')
