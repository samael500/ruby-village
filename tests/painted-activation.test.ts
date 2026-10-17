import {test} from 'node:test';
import assert from 'node:assert/strict';
import {paintedActivationBlockers} from '../src/painted-activation.ts';
const camera={radius:70,origin:{x:140,y:290},angle:0,groundScale:.65};
const anchors={start:{x:100,y:200},goal:{x:1200,y:600}};
const accepted={gate:{camera,groundAnchors:anchors},stream:{camera,groundAnchors:anchors}};
const scene=()=>({background:'gate/background.webp',camera,anchors,semanticAnchors:{residentFeet:{x:1400,y:225}},checks:{fullPolygonVisualAudit:'passed'},wide:{file:'gate/wide.webp',canvas:{width:4096,height:1600},originalRect:{x:1212,y:329,width:1672,height:941}}});
test('atomic activation rejects one missing, misaligned or failed scene',()=>{
 assert.equal(paintedActivationBlockers({scenes:{gate:scene(),stream:scene()}},accepted).length,0);
 assert.ok(paintedActivationBlockers({scenes:{gate:scene()}},accepted).includes('stream: missing scene'));
 const stream=scene();stream.checks.fullPolygonVisualAudit='failed-water-location';stream.camera={...camera,origin:{x:150,y:290}};
 const blockers=paintedActivationBlockers({scenes:{gate:scene(),stream}},accepted);
 assert.ok(blockers.includes('stream: full-polygon visual audit not passed'));assert.ok(blockers.includes('stream: camera differs from accepted geometry'));
});
test('wide crop cannot shift or shrink the immutable native center',()=>{
 const gate=scene();gate.wide.originalRect.width=1600;
 assert.ok(paintedActivationBlockers({scenes:{gate,stream:scene()}},accepted).includes('gate: invalid wide original rectangle'));
});
test('mill cannot activate while the squirrel has no separate grounded placement',()=>{
 const blockers=paintedActivationBlockers({scenes:{mill:scene()}},{mill:{camera,groundAnchors:anchors}});
 assert.ok(blockers.includes('mill: missing secondResidentFeet'));
});
