"""Combine frozen painted clothing resources into the frozen head/hair actor.

Run in Blender with --python-exit-code 1. No runtime or source Blend is edited.
inputs.json pins both source paths and hashes; no latest-file discovery.
"""
from pathlib import Path
import hashlib
import json
import math

import bpy
import numpy as np
from mathutils import Matrix, Vector

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
PAINT_UVS = {"RutaPaint", "RutaPaintPaddedTrousers", "RutaPaintPaddedAccessories"}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(repr(value).encode()).hexdigest()


def actions():
    return {
        a.name: digest([
            (f.data_path, f.array_index, f.extrapolation,
             [(tuple(k.co), tuple(k.handle_left), tuple(k.handle_right),
               k.interpolation, k.handle_left_type, k.handle_right_type)
              for k in f.keyframe_points])
            for layer in a.layers for strip in layer.strips
            for bag in strip.channelbags for f in bag.fcurves
        ]) for a in bpy.data.actions
    }


def geometry(obj):
    mesh = obj.data
    return {
        "coordinates": hashlib.sha256(np.asarray([tuple(v.co) for v in mesh.vertices]).tobytes()).hexdigest(),
        "topology": digest([tuple(p.vertices) for p in mesh.polygons]),
        "weights": digest([[(g.group, g.weight) for g in v.groups] for v in mesh.vertices]),
        "groups": [g.name for g in obj.vertex_groups],
        "parent": obj.parent.name if obj.parent else None,
        "parentType": obj.parent_type,
        "parentBone": obj.parent_bone,
    }


def uv_hashes(mesh):
    return {u.name: digest([tuple(v.uv) for v in u.data]) for u in mesh.uv_layers}


def paint_uvs(material):
    if not material or not material.use_nodes:
        return set()
    return {node.uv_map for node in material.node_tree.nodes
            if node.type == "UVMAP" and node.uv_map in PAINT_UVS}


config = json.loads((OUT / "inputs.json").read_text())
paths = {key: ROOT / config[key]["path"] for key in ("head", "garment")}
for key, path in paths.items():
    assert sha(path) == config[key]["sha256"], (key, "SOURCE HASH MISMATCH")

# Read explicit source bindings and mesh names before opening the head scene.
bpy.ops.wm.open_mainfile(filepath=str(paths["garment"]))
records = []
for obj in sorted(bpy.context.scene.objects, key=lambda v: v.name):
    if obj.type != "MESH":
        continue
    used = set().union(*(paint_uvs(slot.material) for slot in obj.material_slots))
    if not used:
        continue
    assert all(slot.link == "DATA" for slot in obj.material_slots)
    assert "head" not in obj.name.lower() and "hair" not in obj.name.lower(), obj.name
    assert all(name in obj.data.uv_layers for name in used)
    records.append({
        "object": obj.name, "mesh": obj.data.name,
        "topology": geometry(obj)["topology"],
        "paintUVs": sorted(used),
        "sourceUVHashes": uv_hashes(obj.data),
        "sourceMaterialNames": [slot.material.name if slot.material else None
                                for slot in obj.material_slots],
        "faceMaterialIndices": [p.material_index for p in obj.data.polygons],
    })
assert records, "NO PAINTED GARMENT OBJECTS"
assert any("RutaPaintPaddedTrousers" in r["paintUVs"] for r in records)
assert any("RutaPaintPaddedAccessories" in r["paintUVs"] for r in records)

bpy.ops.wm.open_mainfile(filepath=str(paths["head"]))
scene = bpy.context.scene
before_geometry = {o.name: geometry(o) for o in scene.objects if o.type == "MESH"}
before_uvs = {o.name: uv_hashes(o.data) for o in scene.objects if o.type == "MESH"}
before_slots = {o.name: [s.material.name if s.material else None for s in o.material_slots]
                for o in scene.objects if o.type == "MESH"}
before_actions = actions()
rig = bpy.data.objects["CharacterArmature"]
before_bones = digest([(b.name, tuple(b.head_local), tuple(b.tail_local),
                        tuple(tuple(row) for row in b.matrix_local),
                        b.parent.name if b.parent else None) for b in rig.data.bones])
before_camera = ([list(row) for row in scene.camera.matrix_world],
                 scene.camera.data.ortho_scale, scene.render.resolution_x,
                 scene.render.resolution_y)
before_images = {image.name: hashlib.sha256(image.packed_file.data).hexdigest()
                 for image in bpy.data.images if image.packed_file}

names = tuple(dict.fromkeys(r["mesh"] for r in records))
with bpy.data.libraries.load(str(paths["garment"]), link=False) as (available, loaded):
    assert all(name in available.meshes for name in names)
    loaded.meshes = list(names)
loaded_by_name = dict(zip(names, loaded.meshes))
for record in records:
    obj = scene.objects.get(record["object"])
    assert obj is not None and obj.type == "MESH", record["object"]
    assert geometry(obj)["topology"] == record["topology"], obj.name
    target = obj.data
    source = loaded_by_name[record["mesh"]]
    assert len(source.polygons) == len(target.polygons)
    old_active = target.uv_layers.active.name if target.uv_layers.active else None
    old_render = [layer.name for layer in target.uv_layers if layer.active_render]
    for name in record["paintUVs"]:
        source_layer = source.uv_layers[name]
        target_layer = target.uv_layers.get(name) or target.uv_layers.new(name=name)
        assert len(source_layer.data) == len(target_layer.data)
        values = np.empty(len(source_layer.data) * 2, dtype=np.float32)
        source_layer.data.foreach_get("uv", values)
        target_layer.data.foreach_set("uv", values)
    if old_active:
        target.uv_layers.active_index = target.uv_layers.find(old_active)
    for layer in target.uv_layers:
        layer.active_render = layer.name in old_render
    # Transfer only painted slots; leave native skin and all other faces untouched.
    remap = {}
    for index, material in enumerate(source.materials):
        if paint_uvs(material):
            remap[index] = len(target.materials)
            target.materials.append(material)
    for face, index in zip(target.polygons, record["faceMaterialIndices"]):
        if index in remap:
            face.material_index = remap[index]
    current = uv_hashes(target)
    assert all(current[name] == record["sourceUVHashes"][name]
               for name in record["paintUVs"])
    assert all(current[name] == value for name, value in before_uvs[obj.name].items()
               if name not in PAINT_UVS), (obj.name, "ORIGINAL UV CHANGED")
for mesh in loaded_by_name.values():
    bpy.data.meshes.remove(mesh)

after_geometry = {o.name: geometry(o) for o in scene.objects if o.type == "MESH"}
assert after_geometry == before_geometry, "HEAD/HAIR/BODY GEOMETRY OR WEIGHTS CHANGED"
assert actions() == before_actions and len(before_actions) == 50
assert before_bones == digest([(b.name, tuple(b.head_local), tuple(b.tail_local),
                               tuple(tuple(row) for row in b.matrix_local),
                               b.parent.name if b.parent else None) for b in rig.data.bones])
selected = {r["object"] for r in records}
assert all([s.material.name if s.material else None for s in scene.objects[name].material_slots] == slots
           for name, slots in before_slots.items() if name not in selected)
assert before_camera == ([list(row) for row in scene.camera.matrix_world],
                         scene.camera.data.ortho_scale, scene.render.resolution_x,
                         scene.render.resolution_y)
assert all(hashlib.sha256(bpy.data.images[name].packed_file.data).hexdigest() == value
           for name, value in before_images.items())

# Canonical saved pose; render views use only documented source action/yaw changes.
rest = Vector((0, -0.050602056086063385, 0))
rig.animation_data.action = bpy.data.actions["Walk_ProportionProposal"]
rig.animation_data.action_slot = rig.animation_data.action.slots[0]
rig.matrix_world = Matrix.Rotation(math.pi / 2, 4, "Z") @ Matrix.Translation(-rest)
scene.frame_set(0)
bpy.context.view_layer.update()
bpy.ops.file.pack_all()
output = OUT / "ruta-native-painted-combined.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(output), compress=True)
report = {
    "status": "COMBINED-SOURCE-INVARIANTS-PASS-ART-AND-LOOP-PENDING",
    "inputs": config, "outputSha256": sha(output), "transfers": records,
    "allSceneMeshGeometryTopologyWeightsParentsExact": True,
    "all50ActionCurvesAndHandlesExact": True, "allBoneRestMatricesExact": True,
    "allNonPaintUVLayersExact": True, "allNonGarmentMaterialSlotsExact": True,
    "allOriginalHeadHairImagesExact": True, "cameraAndResolutionExact": True,
    "noRuntimeInstall": True, "views": [],
}
(OUT / "assembly-contract.json").write_text(json.dumps(report, indent=2) + "\n")
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.eevee.taa_render_samples = 128
views = [("e-walk00", math.pi / 2, "Walk_ProportionProposal", 0),
         ("e-walk30", math.pi / 2, "Walk_ProportionProposal", 25),
         ("front-neutral", 0, "Idle_Neutral_ProportionProposal", 0),
         ("threequarter-neutral", -math.pi / 4, "Idle_Neutral_ProportionProposal", 0)]
for name, yaw, action, frame in views:
    rig.animation_data.action = bpy.data.actions[action]
    rig.animation_data.action_slot = rig.animation_data.action.slots[0]
    rig.matrix_world = Matrix.Rotation(yaw, 4, "Z") @ Matrix.Translation(-rest)
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    scene.render.filepath = str(OUT / (name + ".png"))
    bpy.ops.render.render(write_still=True)
    report["views"].append({"file": name + ".png", "yaw": yaw, "action": action,
                            "sourceFrame": frame, "sha256": sha(OUT / (name + ".png"))})
    (OUT / "assembly-contract.json").write_text(json.dumps(report, indent=2) + "\n")
assert all(sha(path) == config[key]["sha256"] for key, path in paths.items())
print("COMBINED PAINTED ACTOR ASSEMBLED; FOUR ACTUAL VIEWS; NO RUNTIME/48 CLAIM", flush=True)
