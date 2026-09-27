from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

run=ROOT/'tests/run-regressions.cjs'
r=run.read_text(encoding='utf-8')
if "'floor-workflow-v061'" not in r:
    r=r.replace("'circuit-reference-repair-v060'];","'circuit-reference-repair-v060','floor-workflow-v061'];")
    r=r.replace('// v0.60 keeps all older Circuit Builder compatibility gates and adds stale-reference recovery for completed conventional circuits.','// v0.61 keeps all older compatibility gates and adds floor-state persistence plus in-place Circuit Builder floor switching.')
run.write_text(r,encoding='utf-8')

launcher=(ROOT/'web-v060.html').read_text(encoding='utf-8').replace('v0.60','v0.61').replace('v060','v061')
(ROOT/'web-v061.html').write_text(launcher,encoding='utf-8')

for rel in ['beta.html','download.html']:
    p=ROOT/rel
    s=p.read_text(encoding='utf-8').replace('v0.60','v0.61').replace('v060','v061')
    s=s.replace('This milestone includes the hardened Manual Edit workflow and the latest mobile safety fixes.','This milestone makes the full Plan → Survey → Circuit workflow floor-aware and preserves each floor’s zone state while switching.')
    s=s.replace('<div class="update"><strong>Circuit recovery</strong><span>Completed conventional routes now repair stale device links when the same surveyed devices are still in the same zone, instead of wrongly blocking a clearly drawn circuit.</span></div>','<div class="update"><strong>Floor-aware Circuit Builder</strong><span>Switch Ground, First, Second and other floors directly inside Circuit Builder. Each floor keeps its own zones, surveyed devices, circuits and As-Fit state.</span></div><div class="update"><strong>Zone state protection</strong><span>Changing floors now snapshots zone data immediately and restores the floor’s last selected zone instead of dropping you back to a different zone.</span></div><div class="update"><strong>Circuit recovery</strong><span>Completed conventional routes still repair safe stale device links instead of wrongly blocking a clearly drawn circuit.</span></div>')
    s=s.replace('Please stress multi-zone Circuit Builder jobs: complete several zones, leave/reopen Circuit Builder, and confirm every clearly drawn route stays valid and available to the As-Fit.','Please stress multi-floor jobs: make different zones on two floors, switch between them in Zone Plan and Circuit Builder, and confirm each floor returns exactly as you left it. Also confirm completed routes stay valid and available to the As-Fit.')
    p.write_text(s,encoding='utf-8')

print('Prepared Pineapple v0.61 delivery metadata')
