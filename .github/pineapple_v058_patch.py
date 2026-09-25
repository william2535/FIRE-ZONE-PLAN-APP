from pathlib import Path
import re, shutil

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'index.html'
s=SRC.read_text(encoding='utf-8')
original=s

def sub(pattern,repl,count=1,flags=0,label='replacement'):
    global s
    s2,n=re.subn(pattern,repl,s,count=count,flags=flags)
    if n!=count:
        raise SystemExit(f'{label}: expected {count} replacement(s), got {n}')
    s=s2

s=s.replace(
"const CB_ROUTING_STATES=Object.freeze(['waiting-to-start','routing-normal','approaching-device','device-captured','corner-pending','corner-committed','returning','blocked']);",
"const CB_ROUTING_STATES=Object.freeze(['waiting-to-start','routing-normal','approaching-device','device-captured','departing-device','corner-pending','corner-committed','returning','blocked']);"
)
if s==original: raise SystemExit('routing states marker not found')

# Raw touch samples continue to drive swept device detection. Geometry after a capture uses
# a virtual origin at the captured device so pre-capture overshoot cannot become a giant new leg.
sub(r"function cbProcessPointer\(p,w,h,renderTail=true\)\{.*?\}\nfunction cbProcessSamples",
"""function cbProcessPointer(p,w,h,renderTail=true){if(!cbDrag)return false;cbRecordRawPoint(p);const prev=cbDrag.lastPointer||p;if(cbDrag.select){for(const hit of cbNodesAlong(prev,p,w,h,true))cbSelection.add(hit.id);cbDrag.lastPointer=p;cbUpdateGame();return false}let captured=false,hits=cbNodesAlong(prev,p,w,h);if(hits.some(hit=>cbValidTarget(hit.id)))cbSetRoutingState('approaching-device');for(const hit of hits){if(!cbDrag||cbCircuit?.complete)break;if(cbValidTarget(hit.id)){const appended=cbAppendDrag(hit.p,w,h,true);if(appended===false)break;if(cbCaptureDragTarget(hit.id,w,h,p))captured=true}}if(cbDrag?.points){if(renderTail){if(!captured)cbAppendDrag(p,w,h)}cbDrag.lastPointer=p;cbHover=cbDrag.targets.at(-1)||null}return captured}
function cbProcessSamples""",flags=re.S,label='cbProcessPointer')

sub(r"function cbAppendDrag\(p,w,h,force=false\)\{.*?\n\}\nfunction cbCaptureDragTarget",
"""function cbPostCaptureGeometryPoint(p){if(!cbDrag?.geometryOffset||!p)return p;return{x:p.x+cbDrag.geometryOffset.x,y:p.y+cbDrag.geometryOffset.y}}
function cbAppendDrag(p,w,h,force=false){
 if(!cbDrag)return false;if(cbReturnPhase())return cbAppendReturnDrag(p,w,h);const raw=p;
 if(cbDrag.captureGuard&&!force){const g=cbDrag.captureGuard,cell=cbRouteCellPx(w,h),depart=Math.max(8,Math.min(24,Math.min(cell.x,cell.y)*.46)),moved=Math.hypot(raw.x-g.raw.x,raw.y-g.raw.y);if(moved<depart){cbDrag.routeInput={...g.center};cbDrag.intentPoint={...g.center};cbDrag.blocked=false;cbDrag.phase='device-captured';return true}cbDrag.captureGuard=null;cbDrag.routeInput={...g.center};cbDrag.intentPoint={...g.center};cbDrag.phase='departing-device'}
 const geometry=force?raw:cbPostCaptureGeometryPoint(raw),intent=cbGeometryIntent(geometry,w,h,force),before=cbRouteSnapshot();let q=cbSnapPx(intent,w,h),last=cbDrag.points.at(-1);if(!last)return false;
 q=cbPairSnapPx(q,last,w,h,geometry);cbRouteGridStep(q,w,h,intent);
 const cleaned=cbPruneRouteNoise(cbDrag.points,w,h);if(cleaned.length<=cbDrag.points.length&&!cbChallengePointsBlocked(cleaned,w,h))cbDrag.points=cleaned;
 if(cbChallengePointsBlocked(cbDrag.points,w,h)){cbRouteRestore(before);cbDrag.intentPoint={...(before.routeInput||intent)};cbDrag.routeInput={...intent};cbMarkBlocked();return false}
 cbDrag.routeInput={...intent};cbDrag.blocked=false;if(cbDrag.phase==='corner-committed'||cbDrag.phase==='departing-device')cbDrag.phase='routing-normal';return true
}
function cbCaptureDragTarget""",flags=re.S,label='cbAppendDrag')

sub(r"function cbCaptureDragTarget\(target,w,h\)\{.*?\nfunction cbCommitDrag",
"""function cbCaptureDragTarget(target,w,h,rawPointer=null){if(!cbDrag?.points?.length||!cbValidTarget(target))return false;cbDrag.phase='approaching-device';const returning=target===cbCircuit?.panelId&&cbReturnPhase(),end=cbNodePx(target,w,h),pts=returning?cbReturnGuidePx(w,h):cbDrag.points.slice();if(!end)return false;const last=pts.at(-1),dx=end.x-last.x,dy=end.y-last.y;if(Math.abs(dx)>1&&Math.abs(dy)>1){const prev=pts.at(-2),horizontal=prev?Math.abs(last.y-prev.y)<Math.abs(last.x-prev.x):Math.abs(dx)>=Math.abs(dy);pts.push(horizontal?{x:end.x,y:last.y}:{x:last.x,y:end.y})}pts.push(end);let clean=cbPruneRouteNoise(pts,w,h);if(cbChallengePointsBlocked(clean,w,h)){clean=cbSimplify(pts);if(cbChallengePointsBlocked(clean,w,h)){cbMarkBlocked();return false}}cbDrag.blocked=false;cbDrag.previewLegs.push({from:cbDrag.from,to:target,points:clean.map(p=>cbPxBoard(p,w,h))});cbDrag.targets.push(target);cbDrag.from=target;cbDrag.points=[end];cbDrag.routeAxis=null;cbDrag.turnAnchor=null;cbDrag.routeInput=end;cbDrag.intentPoint={...end};cbDrag.pairSnap=false;cbDrag.pairAxis=null;cbDrag.pairLine=null;cbDrag.phase='device-captured';const raw=rawPointer&&Number.isFinite(rawPointer.x)&&Number.isFinite(rawPointer.y)?rawPointer:end;cbDrag.geometryOffset={x:end.x-raw.x,y:end.y-raw.y};cbDrag.captureGuard={center:{...end},raw:{...raw}};cbHover=target;if(target!==cbCircuit.panelId){const q=cbGameCounts();cbPlayProgressBell(q.done,q.total);cbPulseCounter();cbMilestone(q)}cbUpdateGame();const ready=cbSequenceReady(cbCircuit,[...cbCircuit.sequence,...cbDrag.targets]);if(ready){cbCommitDrag();cbAutoCompleteCircuit();return true}return true}
function cbCommitDrag""",flags=re.S,label='cbCaptureDragTarget')

old="cbDrag={points:[sp],previewLegs:[],targets:[],from:start,routeAxis:null,turnAnchor:null,routeInput:sp,pointerId:e.pointerId,lastPointer:returning?sp:p,returnMode:returning,returnProgress:0,returnGuide:null,phase:returning?'returning':'routing-normal',rawPoints:[{x:p.x,y:p.y}],intentPoint:{...sp}};"
new="cbDrag={points:[sp],previewLegs:[],targets:[],from:start,routeAxis:null,turnAnchor:null,routeInput:sp,geometryOffset:null,pointerId:e.pointerId,lastPointer:returning?sp:p,returnMode:returning,returnProgress:0,returnGuide:null,phase:returning?'returning':'routing-normal',rawPoints:[{x:p.x,y:p.y}],intentPoint:{...sp}};"
if old not in s: raise SystemExit('cbCanvasDown drag init marker not found')
s=s.replace(old,new,1)

# Mark the generation in source for tests/debugging without changing the public version yet.
marker='// v0.57 aggressive-touch input pipeline — raw samples find devices; only deliberate geometry is drawn/saved.'
if marker not in s: raise SystemExit('v0.57 pipeline marker missing')
s=s.replace(marker,marker+'\n// v0.58 Project Pineapple: post-capture raw movement is translated into detector-relative geometry.',1)

SRC.write_text(s,encoding='utf-8')
for rel in ['Zone-Sketch-by-Will.html','ZoneSketch.html','app/src/main/assets/index.html']:
    shutil.copyfile(SRC,ROOT/rel)
print('Applied Project Pineapple v0.58 post-capture geometry-origin fix to all app copies')
