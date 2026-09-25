from pathlib import Path
import re

MAIN = Path('index.html')
t = MAIN.read_text()

if '// v0.55 smooth route engine' not in t:
    # Keep the shared Survey/Circuit grid from the first v0.55 patch, but make the
    # gesture engine much less prone to overshooting corners. The old 1.45-cell
    # threshold encouraged the current leg to keep travelling while the engineer
    # was already turning. These thresholds use the raw finger position as intent
    # while the cable itself remains snapped to the shared field grid.
    t = t.replace(
        'CB_ROUTE_GRID=24,CB_ROUTE_TURN_CELLS=1.45,CB_INSET=.045',
        'CB_ROUTE_GRID=24,CB_ROUTE_TURN_CELLS=.72,CB_ROUTE_ARM_CELLS=.28,CB_ROUTE_SAMPLE_CELLS=.30,CB_INSET=.045',
        1,
    )

    new_block = r'''// v0.55 smooth route engine — shared-grid routing with turn hysteresis and sparse-event sampling.
function cbRouteCellPx(w,h){
 const bounds=cbCircuit?.bounds||cbSelectBounds,scale=Math.max(1,cbView.scale),fallback=CB_ROUTE_GRID*scale;
 const c=typeof cbFieldGridScreenStep==='function'?cbFieldGridScreenStep(bounds,w,h):null;
 return{x:Math.max(6,Number(c?.x)||fallback),y:Math.max(6,Number(c?.y)||fallback)}
}
function cbRouteSnapshot(){return{points:(cbDrag?.points||[]).map(p=>({...p})),routeAxis:cbDrag?.routeAxis||null,turnAnchor:cbDrag?.turnAnchor?{...cbDrag.turnAnchor}:null,pairSide:cbDrag?.pairSide??null,pairSnap:!!cbDrag?.pairSnap,pairAxis:cbDrag?.pairAxis||null,pairLine:Number.isFinite(cbDrag?.pairLine)?cbDrag.pairLine:null,routeInput:cbDrag?.routeInput?{...cbDrag.routeInput}:null}}
function cbRouteRestore(s){if(!cbDrag||!s)return;cbDrag.points=s.points.map(p=>({...p}));cbDrag.routeAxis=s.routeAxis;cbDrag.turnAnchor=s.turnAnchor?{...s.turnAnchor}:null;cbDrag.pairSide=s.pairSide;cbDrag.pairSnap=s.pairSnap;cbDrag.pairAxis=s.pairAxis;cbDrag.pairLine=s.pairLine;cbDrag.routeInput=s.routeInput?{...s.routeInput}:null}
function cbPairSnapPx(q,last,w,h,raw=q){
 if(!cbDrag||!last)return q;
 const cell=cbRouteCellPx(w,h),grid=Math.min(cell.x,cell.y),prev=cbDrag.routeInput||last,rx=Number(raw?.x)??q.x,ry=Number(raw?.y)??q.y,dx=rx-prev.x,dy=ry-prev.y,move=Math.hypot(dx,dy);
 let wantH=Math.abs(dx)>=Math.abs(dy);if(move<grid*.24&&cbDrag.pairAxis)wantH=cbDrag.pairAxis==='h';
 const scale=Math.max(1,cbView.scale),range=Math.max(10,Math.min(42,grid*1.05,CB_PAIR_RANGE*scale)),gap=Math.max(7,Math.min(12,CB_PAIR_GAP*Math.max(1,Math.min(1.2,scale)),grid*.42)),reach=Math.max(18,grid*.70);
 let best=null;
 for(const s of cbPairSegmentsPx(w,h)){
  const sx=s.b.x-s.a.x,sy=s.b.y-s.a.y;if(Math.min(Math.abs(sx),Math.abs(sy))>1.25)continue;
  const isH=Math.abs(sx)>=Math.abs(sy);if(isH!==wantH)continue;
  let dist,inside=false,opposite=false;
  if(isH){inside=q.x>=Math.min(s.a.x,s.b.x)-reach&&q.x<=Math.max(s.a.x,s.b.x)+reach;dist=Math.abs(q.y-s.a.y);opposite=dx*sx<0}
  else{inside=q.y>=Math.min(s.a.y,s.b.y)-reach&&q.y<=Math.max(s.a.y,s.b.y)+reach;dist=Math.abs(q.x-s.a.x);opposite=dy*sy<0}
  if(!inside||dist>range)continue;
  const score=dist+(opposite?0:grid*.10);if(!best||score<best.score)best={s,isH,line:isH?s.a.y:s.a.x,score}
 }
 if(!best){cbDrag.pairSnap=false;cbDrag.pairAxis=null;cbDrag.pairLine=null;return q}
 let side,line;
 if(best.isH){const delta=ry-best.line;side=Math.abs(delta)>Math.max(2,grid*.08)?(delta>=0?1:-1):(cbDrag.pairSide||1);line=best.line+side*gap;q={x:q.x,y:line}}
 else{const delta=rx-best.line;side=Math.abs(delta)>Math.max(2,grid*.08)?(delta>=0?1:-1):(cbDrag.pairSide||1);line=best.line+side*gap;q={x:line,y:q.y}}
 cbDrag.pairSide=side;cbDrag.pairSnap=true;cbDrag.pairAxis=best.isH?'h':'v';cbDrag.pairLine=line;return q
}
function cbRouteGridStep(q,w,h,intent=q){
 if(!cbDrag?.points?.length)return;
 const pts=cbDrag.points,cell=cbRouteCellPx(w,h);let axis=cbDrag.routeAxis||null,last=pts.at(-1);
 const pairAxis=cbDrag.pairSnap?cbDrag.pairAxis:null,pairLine=cbDrag.pairSnap?cbDrag.pairLine:null,paired=!!pairAxis&&Number.isFinite(pairLine);
 if(!axis){
  const dx=q.x-last.x,dy=q.y-last.y,nx=Math.abs(dx)/cell.x,ny=Math.abs(dy)/cell.y;if(Math.max(nx,ny)<.28)return;
  axis=paired?pairAxis:(nx>=ny?'h':'v');cbDrag.routeAxis=axis;cbDrag.turnAnchor=null;
  if(paired&&axis===pairAxis){
   if(axis==='h'){if(Math.abs(last.y-pairLine)>.5)pts.push({x:last.x,y:pairLine});pts.push({x:q.x,y:pairLine})}
   else{if(Math.abs(last.x-pairLine)>.5)pts.push({x:pairLine,y:last.y});pts.push({x:pairLine,y:q.y})}
  }else pts.push(axis==='h'?{x:q.x,y:last.y}:{x:last.x,y:q.y});
  cbDrag.points=cbSimplify(pts);return
 }
 if(paired&&axis===pairAxis){
  cbDrag.turnAnchor=null;
  if(axis==='h'){if(Math.abs(last.y-pairLine)>.5){pts.push({x:last.x,y:pairLine});last=pts.at(-1)}last.x=q.x;last.y=pairLine}
  else{if(Math.abs(last.x-pairLine)>.5){pts.push({x:pairLine,y:last.y});last=pts.at(-1)}last.x=pairLine;last.y=q.y}
  cbDrag.points=cbSimplify(pts);return
 }
 const raw=intent||q,perpCell=axis==='h'?cell.y:cell.x,perp=axis==='h'?Math.abs(raw.y-last.y):Math.abs(raw.x-last.x),arm=perpCell*CB_ROUTE_ARM_CELLS,turn=perpCell*CB_ROUTE_TURN_CELLS;
 if(perp<arm){
  cbDrag.turnAnchor=null;if(axis==='h')last.x=q.x;else last.y=q.y
 }else{
  if(!cbDrag.turnAnchor)cbDrag.turnAnchor={x:last.x,y:last.y};const a=cbDrag.turnAnchor;last.x=a.x;last.y=a.y;
  if(perp>=turn){const next=axis==='h'?{x:a.x,y:q.y}:{x:q.x,y:a.y};if(Math.hypot(next.x-a.x,next.y-a.y)>=1)pts.push(next);cbDrag.routeAxis=axis==='h'?'v':'h';cbDrag.turnAnchor=null}
 }
 cbDrag.points=cbSimplify(pts)
}
function cbAppendDrag(p,w,h){
 if(!cbDrag)return false;const cell=cbRouteCellPx(w,h),sample=Math.max(4,Math.min(cell.x,cell.y)*CB_ROUTE_SAMPLE_CELLS),start=cbDrag.routeInput||cbDrag.points.at(-1)||p,dist=Math.hypot(p.x-start.x,p.y-start.y),steps=Math.max(1,Math.min(64,Math.ceil(dist/sample)));
 for(let i=1;i<=steps;i++){
  const raw={x:start.x+(p.x-start.x)*i/steps,y:start.y+(p.y-start.y)*i/steps},before=cbRouteSnapshot();let q=cbSnapPx(raw,w,h),last=cbDrag.points.at(-1);if(!last)return false;
  q=cbPairSnapPx(q,last,w,h,raw);cbRouteGridStep(q,w,h,raw);
  if(cbChallengePointsBlocked(cbDrag.points,w,h)){cbRouteRestore(before);cbDrag.routeInput=raw;cbMarkBlocked();return false}
  cbDrag.routeInput=raw
 }
 cbDrag.blocked=false;return true
}
'''

    pattern = r'function cbPairSnapPx\(q,last,w,h\)\{.*?\nfunction cbCaptureDragTarget\(target,w,h\)\{'
    replacement = new_block + 'function cbCaptureDragTarget(target,w,h){'
    t2, n = re.subn(pattern, lambda m: replacement, t, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f'Could not replace Circuit Builder routing block ({n})')
    t = t2

    # Starting, hitting a device, and continuing while the finger is still down must reset
    # gesture intent at the exact device/grid intersection. This prevents the previous touch
    # tail from creating a phantom leg after a detector is captured.
    old_start = "cbDrag={points:[sp],previewLegs:[],targets:[],from:start,routeAxis:null,pointerId:e.pointerId,lastPointer:p}"
    new_start = "cbDrag={points:[sp],previewLegs:[],targets:[],from:start,routeAxis:null,turnAnchor:null,routeInput:sp,pointerId:e.pointerId,lastPointer:p}"
    if old_start not in t:
        raise SystemExit('Could not update Circuit Builder drag start state')
    t = t.replace(old_start, new_start, 1)

    old_capture = "cbDrag.points=[end];cbDrag.routeAxis=null;cbDrag.pairSnap=false;cbHover=target;"
    new_capture = "cbDrag.points=[end];cbDrag.routeAxis=null;cbDrag.turnAnchor=null;cbDrag.routeInput=end;cbDrag.pairSnap=false;cbDrag.pairAxis=null;cbDrag.pairLine=null;cbHover=target;"
    if old_capture not in t:
        raise SystemExit('Could not update Circuit Builder device-capture reset')
    t = t.replace(old_capture, new_capture, 1)

    # Field hint: tell the engineer why the line feels steadier than a freehand trace.
    t = t.replace(
        'cable uses Survey field grid · retracing makes a parallel cable',
        'cable uses Survey field grid · corners lock cleanly · retracing makes a parallel cable',
        1,
    )

# Main app copies only. The 24/7 Protection experiment is intentionally never generated from
# this patch and remains protected by the checksum gate in the release workflow.
for name in ['index.html', 'ZoneSketch.html', 'Zone-Sketch-by-Will.html', 'app/src/main/assets/index.html']:
    Path(name).write_text(t)

assert '// v0.55 smooth route engine' in t
assert 'CB_ROUTE_ARM_CELLS=.28' in t
assert 'CB_ROUTE_SAMPLE_CELLS=.30' in t
assert 'function cbRouteSnapshot' in t
assert 'turnAnchor:null,routeInput:sp' in t
print('Applied v0.55 smooth shared-grid Circuit Builder routing; 24/7 demo untouched')
