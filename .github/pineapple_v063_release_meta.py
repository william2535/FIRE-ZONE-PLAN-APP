from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

run=ROOT/'tests/run-regressions.cjs'
r=run.read_text(encoding='utf-8')
if "'zone-quick-edit-v063'" not in r:
    r=r.replace("'build-mode-v062'];","'build-mode-v062','zone-quick-edit-v063'];")
run.write_text(r,encoding='utf-8')

# Keep the long-running Zone Challenge compatibility test current with the new app version.
zone_game=ROOT/'tests/circuit-zone-game-v054.cjs'
z=zone_game.read_text(encoding='utf-8')
z=z.replace('/v0\\.(?:54|55|56|57|58|59|60|61|62)/','/v0\\.(?:54|55|56|57|58|59|60|61|62|63)/')
z=z.replace('PASS: v0.54-v0.62 Zone Challenge','PASS: v0.54-v0.63 Zone Challenge')
zone_game.write_text(z,encoding='utf-8')

launcher=(ROOT/'web-v062.html').read_text(encoding='utf-8').replace('v0.62','v0.63').replace('v062','v063')
(ROOT/'web-v063.html').write_text(launcher,encoding='utf-8')

for rel in ['beta.html','download.html']:
    p=ROOT/rel
    s=p.read_text(encoding='utf-8').replace('v0.62','v0.63').replace('v062','v063')
    old='This milestone adds a switchable Zone Plan build workflow: keep placement and moving separate on large drawings, or combine them on smaller plans so an existing zone can be dragged without leaving the active zone tool.'
    new='This milestone speeds up Zone Plan editing on small and dense drawings: Build mode OFF now supports tap-to-pick, drag-to-move and empty-space placement without changing tools, plus a per-floor Zone tint control for plan readability.'
    s=s.replace(old,new)
    anchor='<div class="update"><strong>Toggleable Build mode</strong><span>Build mode ON keeps zone placement and moving separate. Turn it OFF on smaller plans to place new zones and drag existing zones without swapping tools.</span></div>'
    quick='<div class="update"><strong>Zone quick edit + tint</strong><span>With Build mode OFF, tap an existing zone to make it active, drag it to move it, or drag empty space to place. Drawing settings now include a per-floor Zone tint slider from 4% to 40%.</span></div>'
    if quick not in s:
        s=s.replace(anchor,quick+anchor)
    s=s.replace('Please stress the new Zone Plan Build mode as well as multi-floor jobs. On a small plan, turn Build mode OFF and confirm you can drag an existing zone while the current zone tool stays ready to place on empty space. Turn it back ON and confirm placement/moving are deliberately separate. Also switch between floors and confirm each floor returns exactly as you left it.','Please stress Zone Plan quick edit on a phone-sized plan. With Build mode OFF, tap a coloured zone to pick that zone, drag it to move it, then drag empty space to place another area without changing tools. Try Zone tint at low and high values, switch floors, and confirm each floor keeps its own tint and zone state.')
    p.write_text(s,encoding='utf-8')

print('Prepared Pineapple v0.63 delivery metadata')
