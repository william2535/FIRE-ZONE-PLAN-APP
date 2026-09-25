from pathlib import Path
import re

MAIN = Path('index.html')
t = MAIN.read_text()


def sub_once(pattern, replacement, label):
    global t
    t2, n = re.subn(pattern, replacement, t, count=1, flags=re.S)
    if n != 1:
        if replacement.strip() in t:
            return
        raise SystemExit(f'v0.53 patch marker missing: {label} ({n})')
    t = t2

# Main Zone Sketch only. Company demo files are deliberately never touched here.
t = t.replace('v0.52', 'v0.53')

# Retracing a cable now works for either circuit type. The snap candidate must be local to
# the current endpoint, which prevents unrelated nearby cable runs from pulling the route.
pair_fn = r'''// v0.53 parallel retrace — drawing back over an existing cable creates a clean second lane.
function cbPairSnapPx(q,last,w,h){
 if(cbDrag){cbDrag.pairSnap=false;cbDrag.pairAxis=null;cbDrag.pairLine=null}
 if(!cbDrag||!last)return q;
 const dx=q.x-last.x,dy=q.y-last.y;if(Math.hypot(dx,dy)<8)return q;
 const wantH=Math.abs(dx)>=Math.abs(dy),scale=Math.max(1,cbView.scale),range=Math.min(38,CB_PAIR_RANGE*scale),gap=CB_PAIR_GAP*scale,nearEnd=Math.max(20,range);
 let best=null;
 for(const s of cbPairSegmentsPx(w,h)){
  const sx=s.b.x-s.a.x,sy=s.b.y-s.a.y;if(Math.min(Math.abs(sx),Math.abs(sy))>1)continue;
  const isH=Math.abs(sx)>=Math.abs(sy);if(isH!==wantH)continue;
  if(isH){
   const lo=Math.min(s.a.x,s.b.x),hi=Math.max(s.a.x,s.b.x),d=Math.abs(q.y-s.a.y),ld=Math.abs(last.y-s.a.y);
   if(q.x<lo-2*scale||q.x>hi+2*scale||last.x<lo-nearEnd||last.x>hi+nearEnd||d>range||ld>range)continue;
   const score=d+ld*.3;if(!best||score<best.score)best={score,isH:true,line:s.a.y}
  }else{
   const lo=Math.min(s.a.y,s.b.y),hi=Math.max(s.a.y,s.b.y),d=Math.abs(q.x-s.a.x),ld=Math.abs(last.x-s.a.x);
   if(q.y<lo-2*scale||q.y>hi+2*scale||last.y<lo-nearEnd||last.y>hi+nearEnd||d>range||ld>range)continue;
   const score=d+ld*.3;if(!best||score<best.score)best={score,isH:false,line:s.a.x}
  }
 }
 if(!best)return q;
 let side,line;
 if(best.isH){const delta=q.y-best.line;side=Math.abs(delta)<3*scale?(cbDrag.pairSide||1):(delta>=0?1:-1);line=best.line+side*gap;q={x:q.x,y:line}}
 else{const delta=q.x-best.line;side=Math.abs(delta)<3*scale?(cbDrag.pairSide||1):(delta>=0?1:-1);line=best.line+side*gap;q={x:line,y:q.y}}
 cbDrag.pairSide=side;cbDrag.pairSnap=true;cbDrag.pairAxis=best.isH?'h':'v';cbDrag.pairLine=line;return q
}
function cbRouteGridStep'''
sub_once(r"function cbPairSnapPx\(q,last,w,h\)\{.*?\}\nfunction cbRouteGridStep", pair_fn, 'parallel retrace snap')

# The route engine now honours the paired lane instead of snapping the point and then
# immediately flattening it back onto the original cable. Turns lock at the last known
# grid point, rather than extending the old leg to a far-away touch sample.
route_fn = r'''function cbRouteGridStep(q,w,h){
 if(!cbDrag?.points?.length)return;
 const pts=cbDrag.points,grid=Math.max(8,CB_ROUTE_GRID*Math.max(1,cbView.scale));
 let axis=cbDrag.routeAxis||null,last=pts.at(-1);
 const pairAxis=cbDrag.pairSnap?cbDrag.pairAxis:null,pairLine=cbDrag.pairSnap?cbDrag.pairLine:null,paired=!!pairAxis&&Number.isFinite(pairLine);
 if(!axis){
  const dx=q.x-last.x,dy=q.y-last.y;if(Math.max(Math.abs(dx),Math.abs(dy))<grid*.55)return;
  axis=paired?pairAxis:(Math.abs(dx)>=Math.abs(dy)?'h':'v');cbDrag.routeAxis=axis;
  if(paired&&axis===pairAxis){
   if(axis==='h'){if(Math.abs(last.y-pairLine)>.5)pts.push({x:last.x,y:pairLine});pts.push({x:q.x,y:pairLine})}
   else{if(Math.abs(last.x-pairLine)>.5)pts.push({x:pairLine,y:last.y});pts.push({x:pairLine,y:q.y})}
  }else pts.push(axis==='h'?{x:q.x,y:last.y}:{x:last.x,y:q.y});
  cbDrag.points=cbSimplify(pts);return
 }
 if(paired&&axis===pairAxis){
  if(axis==='h'){
   if(Math.abs(last.y-pairLine)>.5){pts.push({x:last.x,y:pairLine});last=pts.at(-1)}
   last.x=q.x;last.y=pairLine
  }else{
   if(Math.abs(last.x-pairLine)>.5){pts.push({x:pairLine,y:last.y});last=pts.at(-1)}
   last.x=pairLine;last.y=q.y
  }
  cbDrag.points=cbSimplify(pts);return
 }
 const turn=grid*CB_ROUTE_TURN_CELLS,perp=axis==='h'?Math.abs(q.y-last.y):Math.abs(q.x-last.x);
 if(perp>=turn){
  // Corner starts from the route endpoint already reached. Do not shoot the old leg out
  // to the latest (possibly sparse) touch event before turning.
  if(axis==='h'){pts.push({x:last.x,y:q.y});cbDrag.routeAxis='v'}
  else{pts.push({x:q.x,y:last.y});cbDrag.routeAxis='h'}
 }else{
  if(axis==='h')last.x=q.x;else last.y=q.y
 }
 cbDrag.points=cbSimplify(pts)
}
function cbAppendDrag'''
sub_once(r"function cbRouteGridStep\(q,w,h\)\{.*?\}\nfunction cbAppendDrag", route_fn, 'stable grid turns')

# A sparse touch event can cross a detector and continue far beyond it. Once a target is
# captured, discard that event's tail so the next leg starts exactly at the detector.
process_fn = r'''function cbProcessPointer(p,w,h){if(!cbDrag)return;const prev=cbDrag.lastPointer||p;if(cbDrag.select){for(const hit of cbNodesAlong(prev,p,w,h,true))cbSelection.add(hit.id);cbDrag.lastPointer=p;cbUpdateGame();return}let captured=false;for(const hit of cbNodesAlong(prev,p,w,h)){if(!cbDrag||cbCircuit?.complete)break;if(cbValidTarget(hit.id)){cbAppendDrag(hit.p,w,h);cbCaptureDragTarget(hit.id,w,h);captured=true}}if(cbDrag?.points){if(!captured)cbAppendDrag(p,w,h);cbDrag.lastPointer=p;cbHover=cbDrag.targets.at(-1)||null}}
function cbClearReward'''
sub_once(r"function cbProcessPointer\(p,w,h\)\{.*?\}\nfunction cbClearReward", process_fn, 'capture tail suppression')

# Show the pairing feedback for conventional shared runs as well as addressable returns.
t = t.replace("pairMode=cbScreen==='game'&&cbCircuit?.type==='addressable'", "pairMode=cbScreen==='game'&&!!cbCircuit")
t = t.replace('cable snaps to grid · pinch with two fingers to zoom', 'cable snaps to grid · retracing makes a parallel cable · pinch with two fingers to zoom')

# Keep every main entry point identical; separate company demos are intentionally excluded.
for name in ['index.html', 'ZoneSketch.html', 'Zone-Sketch-by-Will.html', 'app/src/main/assets/index.html']:
    Path(name).write_text(t)

# Android release metadata.
g = Path('app/build.gradle').read_text()
g = g.replace('versionCode 53', 'versionCode 54').replace("versionName '0.52'", "versionName '0.53'")
Path('app/build.gradle').write_text(g)

# Add the new field regression to the normal suite.
rp = Path('tests/run-regressions.cjs')
r = rp.read_text()
if "'circuit-retrace-v053'" not in r:
    r = r.replace("'asfit-quality-v052']", "'asfit-quality-v052','circuit-retrace-v053']")
    rp.write_text(r)

assert 'v0.53 parallel retrace' in t
assert "cbDrag.pairAxis=best.isH?'h':'v'" in t
assert 'if(!captured)cbAppendDrag(p,w,h)' in t
assert "pairMode=cbScreen==='game'&&!!cbCircuit" in t
assert "versionName '0.53'" in g
print('Applied v0.53 parallel retrace and stable corner routing to main build only')
