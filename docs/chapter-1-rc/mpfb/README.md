# MPFB Ruta — actual technical smoke, appearance not authored yet

Branch `art/36-mpfb-ruta`, base ff60cb1, issue36. User explicitly requested MPFB for character figure and motion. This is genuine MPFB mesh/weighted rig, not source-image deformation. Production is disabled; no artistic approval, final Ruta, gait or renderer evidence is claimed.

`art/characters-mpfb-v1/smoke/ruta-mpfb-smoke.blend` was created by an actual Blender4.5.3LTS run with MPFB2.0.18 from its existing source checkout. Result:19158vertices/18486faces, default standard rig163bones, armature modifier, height1.26191m. Child macro age.1875 (MPFB documented child preset), female gender0, moderate weight.45/muscle.3/proportions.35; these are starting settings, not matching accepted Ruta yet. See smoke.json and real smoke.log.

## Reproduce

```sh
BLENDER_USER_CONFIG=/tmp/ruby-mpfb-config/config \
BLENDER_USER_SCRIPTS=/tmp/ruby-mpfb-config/scripts \
BLENDER_USER_DATAFILES=/tmp/ruby-mpfb-config/datafiles \
PYTHONDONTWRITEBYTECODE=1 \
/tmp/blender-4.5.3-linux-x64/blender -b --factory-startup --python scripts/mpfb-smoke.py
```

Set RUBY_MPFB_SRC to a different MPFB2.0.18 `src` checkout if needed. The scoped source-mode extension-home adapter handles the source package `mpfb`, while ordinary Blender extension paths keep their native function. This process never installs or edits vendor code. MPFB data/cache/log/config all resolve under /tmp/ruby-mpfb-config, not ~/.config. Online-access is disabled by factory defaults; no external upload.

## Sources and rights

[Official guide](https://static.makehumancommunity.org/mpfb/docs/getting_started.html) requires Blender>=4.2, recommends system-assets pack, and specifies creating the rig before adding clothes/bodyparts; default/default-no-toes rigs support IK helpers. Next authoring must follow this ordering and preserve reusable presets.

MPFB source code is GPL3; its bundled basemesh, targets, rigs, weights and graphical assets are CC0 according to the bundled license statement, copied verbatim in licenses/. The statement also explicitly distinguishes generated meshes/renders from program logic. No third-party clothing/hair has been loaded yet. Shared ZIPs are only read/CRC-tested/hashed by scripts/mpfb-inventory.py: all three pass CRC; pack metadata and exact hashes retained in inventory.json. A separate session owns the downloads/shared extraction: we never extract to or modify that location. Individual selected assets still require provenance retention before model delivery.

## Next work and current limits

Before animation, make a dressed full-body E appearance pilot against accepted Ruta, with her proportions/face, long brown hair, white shirt/green vest/red scarf, brown trousers/boots and one satchel strap. Base mannequin is not final art. Then real IK contacts and root stride,720ms author cycle only if physically natural, fixed orthographic framing, whole-frame renders around24fps; six views come after pilot review. Current smoke does not verify any of those artistic/physical criteria. Common runtime/manifests unchanged. Family and actual phone checks not run.
