from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'index.html'
s=SRC.read_text(encoding='utf-8')

helper="""function cbEditBridgePosOnLeg(bridge,pts){const p=bridge?.point;if(!p||!Array.isArray(pts)||pts.length<2)return null;let best=null;for(let si=0;si<pts.length-1;si++){const q=cbEditProjectToSegment(p,pts[si],pts[si+1]);if(q.d<=.00008&&(!best||q.d<best.d))best={pos:si+q.t,d:q.d}}return best?.pos??null}\nfunction cbEditBridgeTouchesSegment(bridge,a,b){const p=bridge?.point;if(!p||!a||!b)return false;return cbEditProjectToSegment(p,a,b).d<=.00008}\nfunction cbEditBridgeInsideSpan(bridge,pts,lo,hi){const pos=cbEditBridgePosOnLeg(bridge,pts);return Number.isFinite(pos)&&pos>=lo-.0001&&pos<=hi+.0001}\n"""

if 'function cbEditBridgePosOnLeg' not in s:
    marker='function cbEditSplicePending(){'
    if marker not in s:
        raise SystemExit('Bridge helper insertion marker not found')
    s=s.replace(marker,helper+marker,1)

old_delete="d.bridges=d.bridges.filter(b=>!(b.legIndex===hit.legIndex));"
new_delete="d.bridges=d.bridges.filter(b=>!(b.legIndex===hit.legIndex&&cbEditBridgeTouchesSegment(b,pts[si],pts[si+1])));"
if old_delete in s:
    s=s.replace(old_delete,new_delete,1)
elif new_delete not in s:
    raise SystemExit('Bridge-local delete marker not found')

old_leg="leg.points=cbEditSimplifyBoard(combined);"
new_leg="const keptBridges=d.bridges.filter(b=>!(b.legIndex===p.legIndex&&cbEditBridgeInsideSpan(b,pts,lo,hi)));leg.points=cbEditSimplifyBoard(combined);"
if new_leg not in s:
    if old_leg not in s:
        raise SystemExit('Bridge replacement-span marker not found')
    s=s.replace(old_leg,new_leg,1)

old_add="for(const b of p.bridges||[])d.bridges.push({legIndex:p.legIndex,point:b.point,axis:b.axis});"
new_add="d.bridges=keptBridges;for(const b of p.bridges||[]){const next={legIndex:p.legIndex,point:b.point,axis:b.axis};if(!d.bridges.some(x=>x.legIndex===next.legIndex&&Math.hypot(x.point.x-next.point.x,x.point.y-next.point.y)<=.00008))d.bridges.push(next)}"
if old_add in s:
    s=s.replace(old_add,new_add,1)
elif new_add not in s:
    raise SystemExit('Bridge replacement add marker not found')

SRC.write_text(s,encoding='utf-8')
for rel in ['Zone-Sketch-by-Will.html','ZoneSketch.html','app/src/main/assets/index.html']:
    shutil.copyfile(SRC,ROOT/rel)
print('Scoped bridge metadata to the local deleted/replaced cable geometry in all app copies')
