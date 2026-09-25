from pathlib import Path
import re

p=Path('index.html')
t=p.read_text()
original=t

def one(pattern,repl,flags=re.S,desc='patch'):
    global t
    t2,n=re.subn(pattern,repl,t,count=1,flags=flags)
    if n!=1:
        raise SystemExit(f'{desc}: expected 1 replacement, got {n}')
    t=t2

# Keep the existing v0.55 constants for backwards-compatible geometry tests, but add
# v0.57 thresholds for route cleanup and the independent swept touch corridor.
one(r"const CB_ROUTE_GRID=24,CB_ROUTE_TURN_CELLS=\.72,CB_ROUTE_ARM_CELLS=\.28,CB_ROUTE_SAMPLE_CELLS=\.30,CB_INSET=\.045,CB_SPAN=\.91,CB_DEVICE_R=11,CB_PANEL_R=16,CB_PAIR_GAP=9,CB_PAIR_RANGE=24,CB_COLORS=",
    "const CB_ROUTE_GRID=24,CB_ROUTE_TURN_CELLS=.72,CB_ROUTE_ARM_CELLS=.28,CB_ROUTE_SAMPLE_CELLS=.30,CB_ROUTE_DOGLEG_CELLS=.62,CB_HIT_MIN=27,CB_HIT_MAX=40,CB_INSET=.045,CB_SPAN=.91,CB_DEVICE_R=11,CB_PANEL_R=16,CB_PAIR_GAP=9,CB_PAIR_RANGE=24,CB_COLORS=",
    flags=0,desc='constants')

# Raw touch samples, device capture and display geometry are now deliberately separate.
one(r"function cbNodesAlong\(a,b,w,h,selection=false\)\{.*?\nfunction cbClearReward",
"""// v0.57 aggressive-touch input pipeline — raw samples find devices; only deliberate geometry is drawn/saved.
function cbRoutingState(){return cbDrag?.phase||'waiting-to-start'}
function cbSetRoutingState(next){if(cbDrag)cbDrag.phase=next;return next}
function cbRecordRawPoint(p){if(!cbDrag||!p)return;const list=cbDrag.rawPoints||(cbDrag.rawPoints=[]),last=list.at(-1);if(!last||Math.hypot(last.x-p.x,last.y-p.y)>.25)list.push({x:p.x,y:p.y});if(list.length>160)list.splice(0,list.length-160)}
function cbHitCorridorPx(w,h,selection=false){const cell=cbRouteCellPx(w,h),grid=Math.min(cell.x,cell.y),lo=selection?31:CB_HIT_MIN,hi=selection?45:CB_HIT_MAX;return Math.max(lo,Math.min(hi,grid*.66+CB_DEVICE_R*.78))}
function cbNodesAlong(a,b,w,h,selection=false){const dx=b.x-a.x,dy=b.y-a.y,l2=dx*dx+dy*dy,ids=selection?cbSurveyDevices().map(d=>d.id):[cbCircuit?.panelId,...(cbCircuit?.deviceIds||[])],hits=[],corridor=cbHitCorridorPx(w,h,selection);for(const id of ids){const p=cbNodePx(id,w,h);if(!p)continue;const tt=l2?clamp(((p.x-a.x)*dx+(p.y-a.y)*dy)/l2):0,d=Math.hypot(a.x+tt*dx-p.x,a.y+tt*dy-p.y);if(d<=corridor)hits.push({id,t:tt,p,d})}return hits.sort((a,b)=>a.t-b.t||a.d-b.d)}
function cbProcessPointer(p,w,h,renderTail=true){if(!cbDrag)return false;cbRecordRawPoint(p);const prev=cbDrag.lastPointer||p;if(cbDrag.select){for(const hit of cbNodesAlong(prev,p,w,h,true))cbSelection.add(hit.id);cbDrag.lastPointer=p;cbUpdateGame();return false}let captured=false,hits=cbNodesAlong(prev,p,w,h);if(hits.some(hit=>cbValidTarget(hit.id)))cbSetRoutingState('approaching-device');for(const hit of hits){if(!cbDrag||cbCircuit?.complete)break;if(cbValidTarget(hit.id)){const appended=cbAppendDrag(hit.p,w,h);if(appended===false)break;if(cbCaptureDragTarget(hit.id,w,h))captured=true}}if(cbDrag?.points){if(renderTail&&!captured)cbAppendDrag(p,w,h);cbDrag.lastPointer=p;cbHover=cbDrag.targets.at(-1)||null}return captured}
function cbProcessSamples(samples,w,h){if(!cbDrag||!samples?.length)return false;let captured=false;for(const p of samples)captured=cbProcessPointer(p,w,h,false)||captured;if(cbDrag?.points&&!captured){const last=samples.at(-1);cbAppendDrag(last,w,h);cbDrag.lastPointer=last}return captured}
function cbClearReward""",desc='raw input pipeline')

# Add an orthogonal cleanup pass. It removes only sub-grid reversals and doglegs; intended
# larger turns survive. Device endpoints remain unchanged.
one(r"function cbSimplify\(points\)\{.*?\}\nfunction cbPointClose",
"""function cbSimplify(points){const out=[];for(const p of points){const last=out.at(-1);if(last&&Math.hypot(last.x-p.x,last.y-p.y)<1)continue;out.push(p);while(out.length>=3&&cbCollinear(out.at(-3),out.at(-2),out.at(-1)))out.splice(out.length-2,1)}return out}
function cbRouteAxis(a,b){if(Math.abs(a.x-b.x)<=1.25)return'v';if(Math.abs(a.y-b.y)<=1.25)return'h';return null}
function cbPruneRouteNoise(points,w,h){let pts=cbSimplify((points||[]).map(q=>({...q})));if(pts.length<3)return pts;const cell=cbRouteCellPx(w,h),tiny=Math.max(6,Math.min(cell.x,cell.y)*CB_ROUTE_DOGLEG_CELLS);let changed=true,guard=0;while(changed&&guard++<10){changed=false;for(let i=1;i<pts.length-1;i++){const a=pts[i-1],b=pts[i],c=pts[i+1],ab=cbRouteAxis(a,b),bc=cbRouteAxis(b,c);if(!ab||ab!==bc)continue;const v1=ab==='h'?b.x-a.x:b.y-a.y,v2=ab==='h'?c.x-b.x:c.y-b.y;if(v1*v2<0&&Math.min(Math.abs(v1),Math.abs(v2))<=tiny){pts.splice(i,1);pts=cbSimplify(pts);changed=true;break}}if(changed)continue;for(let i=0;i<pts.length-3;i++){const a=pts[i],b=pts[i+1],c=pts[i+2],d=pts[i+3],ab=cbRouteAxis(a,b),bc=cbRouteAxis(b,c),cd=cbRouteAxis(c,d);if(!ab||!bc||!cd||ab!==cd||ab===bc)continue;const middle=Math.hypot(c.x-b.x,c.y-b.y),v1=ab==='h'?b.x-a.x:b.y-a.y,v2=cd==='h'?d.x-c.x:d.y-c.y;if(middle>tiny||v1*v2<=0)continue;const corner=ab==='h'?{x:d.x,y:a.y}:{x:a.x,y:d.y},candidate=cbSimplify([...pts.slice(0,i+1),corner,d,...pts.slice(i+4)]);if(candidate.every((q,j)=>j===0||cbRouteAxis(candidate[j-1],q))){pts=candidate;changed=true;break}}}return cbSimplify(pts)}
function cbPointClose""",desc='route cleanup')

# Mark a blocked route as an explicit routing state.
one(r"function cbMarkBlocked\(\)\{if\(!cbDrag\)return;cbDrag\.blocked=true;",
    "function cbMarkBlocked(){if(!cbDrag)return;cbDrag.blocked=true;cbDrag.phase='blocked';",
    flags=0,desc='blocked state')

# Preserve the canonical v0.56 return magnet but make the state explicit.
one(r"function cbAppendReturnDrag\(p,w,h\)\{if\(!cbDrag\)return false;",
    "function cbAppendReturnDrag(p,w,h){if(!cbDrag)return false;cbDrag.phase='returning';",
    flags=0,desc='return state')

# Route geometry now consumes one final pointer intention per browser event. The old interpolation
# manufactured dozens of synthetic turns from a single fast diagonal swipe; device capture no
# longer needs that because cbNodesAlong owns the high-resolution swept corridor.
one(r"// v0\.55 smooth route engine — shared-grid routing with turn hysteresis and sparse-event sampling\.\nfunction cbRouteCellPx",
"""// v0.55 smooth route engine — shared-grid routing with turn hysteresis and sparse-event sampling.
// v0.57 aggressive-touch engine — raw input, hit corridor and saved geometry are independent layers.
function cbRouteCellPx""",desc='v057 engine marker')

# State labels live directly inside this low-level function so the older VM regression extraction
# remains self-contained.
one(r"function cbRouteGridStep\(q,w,h,intent=q\)\{.*?\n\}\nfunction cbAppendDrag\(p,w,h\)\{.*?\n\}",
"""function cbRouteGridStep(q,w,h,intent=q){
 if(!cbDrag?.points?.length)return;
 const pts=cbDrag.points,cell=cbRouteCellPx(w,h);let axis=cbDrag.routeAxis||null,last=pts.at(-1);
 const pairAxis=cbDrag.pairSnap?cbDrag.pairAxis:null,pairLine=cbDrag.pairSnap?cbDrag.pairLine:null,paired=!!pairAxis&&Number.isFinite(pairLine);
 if(!axis){
  const dx=q.x-last.x,dy=q.y-last.y,nx=Math.abs(dx)/cell.x,ny=Math.abs(dy)/cell.y;if(Math.max(nx,ny)<.28){cbDrag.phase='routing-normal';return}
  axis=paired?pairAxis:(nx>=ny?'h':'v');cbDrag.routeAxis=axis;cbDrag.turnAnchor=null;cbDrag.phase='routing-normal';
  if(paired&&axis===pairAxis){
   if(axis==='h'){if(Math.abs(last.y-pairLine)>.5)pts.push({x:last.x,y:pairLine});pts.push({x:q.x,y:pairLine})}
   else{if(Math.abs(last.x-pairLine)>.5)pts.push({x:pairLine,y:last.y});pts.push({x:pairLine,y:q.y})}
  }else pts.push(axis==='h'?{x:q.x,y:last.y}:{x:last.x,y:q.y});
  cbDrag.points=cbSimplify(pts);return
 }
 if(paired&&axis===pairAxis){
  cbDrag.turnAnchor=null;cbDrag.phase='routing-normal';
  if(axis==='h'){if(Math.abs(last.y-pairLine)>.5){pts.push({x:last.x,y:pairLine});last=pts.at(-1)}last.x=q.x;last.y=pairLine}
  else{if(Math.abs(last.x-pairLine)>.5){pts.push({x:pairLine,y:last.y});last=pts.at(-1)}last.x=pairLine;last.y=q.y}
  cbDrag.points=cbSimplify(pts);return
 }
 const raw=intent||q,perpCell=axis==='h'?cell.y:cell.x,perp=axis==='h'?Math.abs(raw.y-last.y):Math.abs(raw.x-last.x),arm=perpCell*CB_ROUTE_ARM_CELLS,turn=perpCell*CB_ROUTE_TURN_CELLS;
 if(perp<arm){
  cbDrag.turnAnchor=null;cbDrag.phase='routing-normal';if(axis==='h')last.x=q.x;else last.y=q.y
 }else{
  if(!cbDrag.turnAnchor)cbDrag.turnAnchor={x:last.x,y:last.y};const a=cbDrag.turnAnchor;last.x=a.x;last.y=a.y;cbDrag.phase='corner-pending';
  if(perp>=turn){const next=axis==='h'?{x:a.x,y:q.y}:{x:q.x,y:a.y};if(Math.hypot(next.x-a.x,next.y-a.y)>=1)pts.push(next);cbDrag.routeAxis=axis==='h'?'v':'h';cbDrag.turnAnchor=null;cbDrag.phase='corner-committed'}
 }
 cbDrag.points=cbSimplify(pts)
}
function cbAppendDrag(p,w,h){
 if(!cbDrag)return false;if(cbReturnPhase())return cbAppendReturnDrag(p,w,h);const before=cbRouteSnapshot();let q=cbSnapPx(p,w,h),last=cbDrag.points.at(-1);if(!last)return false;
 q=cbPairSnapPx(q,last,w,h,p);cbRouteGridStep(q,w,h,p);
 const cleaned=cbPruneRouteNoise(cbDrag.points,w,h);if(cleaned.length<=cbDrag.points.length&&!cbChallengePointsBlocked(cleaned,w,h))cbDrag.points=cleaned;
 if(cbChallengePointsBlocked(cbDrag.points,w,h)){cbRouteRestore(before);cbDrag.routeInput={...p};cbMarkBlocked();return false}
 cbDrag.routeInput={...p};cbDrag.blocked=false;if(cbDrag.phase==='corner-committed')cbDrag.phase='routing-normal';return true
}""",desc='geometry engine')

# Clean once more at a device anchor before converting to persistent board coordinates.
one(r"function cbCaptureDragTarget\(target,w,h\)\{.*?\nfunction cbCommitDrag",
"""function cbCaptureDragTarget(target,w,h){if(!cbDrag?.points?.length||!cbValidTarget(target))return false;cbDrag.phase='approaching-device';const returning=target===cbCircuit?.panelId&&cbReturnPhase(),end=cbNodePx(target,w,h),pts=returning?cbReturnGuidePx(w,h):cbDrag.points.slice();if(!end)return false;const last=pts.at(-1),dx=end.x-last.x,dy=end.y-last.y;if(Math.abs(dx)>1&&Math.abs(dy)>1){const prev=pts.at(-2),horizontal=prev?Math.abs(last.y-prev.y)<Math.abs(last.x-prev.x):Math.abs(dx)>=Math.abs(dy);pts.push(horizontal?{x:end.x,y:last.y}:{x:last.x,y:end.y})}pts.push(end);let clean=cbPruneRouteNoise(pts,w,h);if(cbChallengePointsBlocked(clean,w,h)){clean=cbSimplify(pts);if(cbChallengePointsBlocked(clean,w,h)){cbMarkBlocked();return false}}cbDrag.blocked=false;cbDrag.previewLegs.push({from:cbDrag.from,to:target,points:clean.map(p=>cbPxBoard(p,w,h))});cbDrag.targets.push(target);cbDrag.from=target;cbDrag.points=[end];cbDrag.routeAxis=null;cbDrag.turnAnchor=null;cbDrag.routeInput=end;cbDrag.pairSnap=false;cbDrag.pairAxis=null;cbDrag.pairLine=null;cbDrag.phase='device-captured';cbHover=target;if(target!==cbCircuit.panelId){const q=cbGameCounts();cbPlayProgressBell(q.done,q.total);cbPulseCounter();cbMilestone(q)}cbUpdateGame();const ready=cbSequenceReady(cbCircuit,[...cbCircuit.sequence,...cbDrag.targets]);if(ready){cbCommitDrag();cbAutoCompleteCircuit();return true}return true}
function cbCommitDrag""",desc='capture cleanup')

# Add raw sample/state fields without disturbing the historical static-regression substring.
one(r"cbDrag=\{points:\[sp\],previewLegs:\[\],targets:\[\],from:start,routeAxis:null,turnAnchor:null,routeInput:sp,pointerId:e\.pointerId,lastPointer:returning\?sp:p,returnMode:returning,returnProgress:0,returnGuide:null\};",
    "cbDrag={points:[sp],previewLegs:[],targets:[],from:start,routeAxis:null,turnAnchor:null,routeInput:sp,pointerId:e.pointerId,lastPointer:returning?sp:p,returnMode:returning,returnProgress:0,returnGuide:null,phase:returning?'returning':'routing-normal',rawPoints:[{x:p.x,y:p.y}]};",
    flags=0,desc='drag state')

# Coalesced touch samples are used for hit detection only. The displayed geometry consumes one
# final intention per browser event, so high-frequency iOS samples cannot become visible spaghetti.
one(r"function cbCanvasMove\(e\)\{.*?\nfunction cbCanvasCancel",
"""function cbCoalescedCanvasPoints(e){let events=[];try{events=typeof e.getCoalescedEvents==='function'?e.getCoalescedEvents():[]}catch(err){}if(!events?.length)events=[e];return events.map(cbPointInCanvas)}
function cbCanvasMove(e){if(!cbPointers.has(e.pointerId))return;const r=$('cbCanvas').getBoundingClientRect(),w=r.width,h=r.height,samples=cbCoalescedCanvasPoints(e),p=samples.at(-1)||cbPointInCanvas(e);cbPointers.set(e.pointerId,p);if(cbPinch){cbUpdatePinch(w,h);return}if(cbGestureLock||cbDrag?.pointerId!==e.pointerId)return;cbProcessSamples(samples,w,h);cbDrawBoard()}
function cbCanvasUp(e){if(!cbPointers.has(e.pointerId))return;const r=$('cbCanvas').getBoundingClientRect(),p=cbPointInCanvas(e),locked=cbGestureLock||!!cbPinch;cbPointers.delete(e.pointerId);if(locked){if(cbPinch?.ids.includes(e.pointerId))cbPinch=null;if(!cbPointers.size)cbGestureLock=false;return}if(cbDrag?.pointerId!==e.pointerId)return;if(cbScreen==='select'){cbDrag=null;return}cbProcessSamples([p],r.width,r.height);if(cbCircuit?.complete)return;if(!cbCommitDrag()){cbDrag=null;cbHover=null;cbUpdateGame()}}
function cbCanvasCancel""",desc='coalesced pointer handling')

# More accurate feedback: this is now a smart route pipeline, not literal finger tracing.
t=t.replace("challenge?'GRID '+gridStep()+' · NO CROSSING':'⇄ TWIN CABLE · GRID '+gridStep()",
            "challenge?'SMART GRID '+gridStep()+' · NO CROSSING':'SMART ROUTE · GRID '+gridStep()",1)
t=t.replace("'Hold on the green-ring device and drag through detectors · cable uses Survey field grid · corners lock cleanly · the final return magnetically follows the outgoing cable · pinch with two fingers to zoom'",
            "'Drag naturally · sweep through devices · smart routing cleans finger wobble onto the Survey grid · pinch with two fingers to zoom'",1)

if t==original:
    raise SystemExit('No source changes made')
p.write_text(t)

# Keep all four runtime copies byte-identical.
for name in ['ZoneSketch.html','Zone-Sketch-by-Will.html','app/src/main/assets/index.html']:
    Path(name).write_text(t)

# Make the aggressive replay part of the permanent suite after the engine marker lands.
test=Path('tests/circuit-aggressive-touch-v057.cjs')
s=test.read_text()
s=s.replace("const phase=process.env.ROUTING_PHASE||'baseline';", "const phase=process.env.ROUTING_PHASE||(fs.readFileSync('index.html','utf8').includes('v0.57 aggressive-touch engine')?'after':'baseline');")
s=s.replace("const baselinePath=process.env.ROUTING_BASELINE||'test-results/aggressive-touch-baseline.json';", "const baselinePath=process.env.ROUTING_BASELINE||'tests/fixtures/aggressive-touch-v056-baseline.json';")
test.write_text(s)

runner=Path('tests/run-regressions.cjs')
r=runner.read_text()
if "'circuit-aggressive-touch-v057'" not in r:
    r=r.replace("'circuit-return-magnet-v056'", "'circuit-return-magnet-v056','circuit-aggressive-touch-v057'")
runner.write_text(r)

print('Applied v0.57 aggressive-touch routing engine and synced runtime mirrors')
