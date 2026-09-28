from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

run=ROOT/'tests/run-regressions.cjs'
r=run.read_text(encoding='utf-8')
if "'build-mode-v063'" not in r:
    r=r.replace("'build-mode-v062'];","'build-mode-v062','build-mode-v063'];")
run.write_text(r,encoding='utf-8')

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
    s=s.replace('This milestone adds a switchable Zone Plan build workflow: keep placement and moving separate on large drawings, or combine them on smaller plans so an existing zone can be dragged without leaving the active zone tool.','This milestone fixes the Build mode / Pan conflict. Place + move now owns one-finger editing on small plans, the old Pan control cannot override it, and two-finger navigation remains available.')
    s=s.replace('<div class="update"><strong>Toggleable Build mode</strong><span>Build mode ON keeps zone placement and moving separate. Turn it OFF on smaller plans to place new zones and drag existing zones without swapping tools.</span></div>','<div class="update"><strong>Build mode now really switches behaviour</strong><span>Build mode OFF gives Place + move and automatically prevents the old one-finger Pan mode from taking over. Use two fingers or the zoom controls to navigate. Build mode ON restores the deliberate separated workflow.</span></div>')
    s=s.replace('Please stress the new Zone Plan Build mode as well as multi-floor jobs. On a small plan, turn Build mode OFF and confirm you can drag an existing zone while the current zone tool stays ready to place on empty space. Turn it back ON and confirm placement/moving are deliberately separate. Also switch between floors and confirm each floor returns exactly as you left it.','Please stress Build mode OFF on a small Zone Plan: even if Pan was ON beforehand, switching Build mode OFF should force Pan out of the way. Drag an existing zone to move it, then drag empty space to place another without changing tools. Use two fingers or the zoom controls to navigate. Turn Build mode ON and confirm Pan becomes available again for the separated workflow.')
    p.write_text(s,encoding='utf-8')

print('Prepared Pineapple v0.63 delivery metadata')
