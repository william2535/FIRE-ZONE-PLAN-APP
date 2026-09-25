from pathlib import Path

p=Path('index.html')
t=p.read_text()
zone_fn="function cbZoneDevices(zoneId){const shapes=cbZoneShapes(zoneId);return cbSurveyDevices().filter(d=>shapes.some(sh=>pointInPoly(d,sh.points)))}\n"
simplify_fn="function cbSimplify(points){const out=[];for(const p of points){const last=out.at(-1);if(last&&Math.hypot(last.x-p.x,last.y-p.y)<1)continue;out.push(p);while(out.length>=3&&cbCollinear(out.at(-3),out.at(-2),out.at(-1)))out.splice(out.length-2,1)}return out}\n"
# The main v0.54 patch uses captured anchors. Repair literal backreference markers if the
# contents API / Python replacement path leaves them unexpanded.
t=t.replace('\\1function cbChallengeBounds',zone_fn+'function cbChallengeBounds',1)
t=t.replace('\\1function cbPointClose',simplify_fn+'function cbPointClose',1)
for name in ['index.html','ZoneSketch.html','Zone-Sketch-by-Will.html','app/src/main/assets/index.html']:
    Path(name).write_text(t)
assert '\\1function cbChallengeBounds' not in t
assert '\\1function cbPointClose' not in t
assert 'function cbZoneDevices' in t
assert 'function cbSimplify' in t
print('v0.54 helper anchors verified')
