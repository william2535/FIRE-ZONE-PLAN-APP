from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

run=ROOT/'tests/run-regressions.cjs'
r=run.read_text(encoding='utf-8')
if "'build-mode-v062'" not in r:
    r=r.replace("'floor-workflow-v061'];","'floor-workflow-v061','build-mode-v062'];")
run.write_text(r,encoding='utf-8')

launcher=(ROOT/'web-v061.html').read_text(encoding='utf-8').replace('v0.61','v0.62').replace('v061','v062')
(ROOT/'web-v062.html').write_text(launcher,encoding='utf-8')

for rel in ['beta.html','download.html']:
    p=ROOT/rel
    s=p.read_text(encoding='utf-8').replace('v0.61','v0.62').replace('v061','v062')
    s=s.replace('This milestone makes the full Plan → Survey → Circuit workflow floor-aware and preserves each floor’s zone state while switching.','This milestone adds a switchable Zone Plan build workflow: keep placement and moving separate on large drawings, or combine them on smaller plans so an existing zone can be dragged without leaving the active zone tool.')
    anchor='<div class="update"><strong>Floor-aware Circuit Builder</strong><span>Switch Ground, First, Second and other floors directly inside Circuit Builder. Each floor keeps its own zones, surveyed devices, circuits and As-Fit state.</span></div>'
    build='<div class="update"><strong>Toggleable Build mode</strong><span>Build mode ON keeps zone placement and moving separate. Turn it OFF on smaller plans to place new zones and drag existing zones without swapping tools.</span></div>'
    if build not in s:
        s=s.replace(anchor,build+anchor)
    s=s.replace('Please stress multi-floor jobs: make different zones on two floors, switch between them in Zone Plan and Circuit Builder, and confirm each floor returns exactly as you left it. Also confirm completed routes stay valid and available to the As-Fit.','Please stress the new Zone Plan Build mode as well as multi-floor jobs. On a small plan, turn Build mode OFF and confirm you can drag an existing zone while the current zone tool stays ready to place on empty space. Turn it back ON and confirm placement/moving are deliberately separate. Also switch between floors and confirm each floor returns exactly as you left it.')
    p.write_text(s,encoding='utf-8')

print('Prepared Pineapple v0.62 delivery metadata')
