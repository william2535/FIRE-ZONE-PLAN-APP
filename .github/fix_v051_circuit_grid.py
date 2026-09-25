from pathlib import Path

MAIN = Path('index.html')
t = MAIN.read_text()


def once(old, new, label):
    global t
    if old in t:
        t = t.replace(old, new, 1)
    elif new not in t:
        raise SystemExit(f'v0.51 patch marker missing: {label}')

# Version the proven main build forward without touching any company demo copy.
t = t.replace('v0.50', 'v0.51')

once(
    "const CB_ROUTE_GRID=20,CB_INSET=.045,CB_SPAN=.91,CB_DEVICE_R=11,CB_PANEL_R=16,CB_PAIR_GAP=9,CB_PAIR_RANGE=24,CB_COLORS=",
    "const CB_ROUTE_GRID=24,CB_ROUTE_TURN_CELLS=1.45,CB_INSET=.045,CB_SPAN=.91,CB_DEVICE_R=11,CB_PANEL_R=16,CB_PAIR_GAP=9,CB_PAIR_RANGE=24,CB_COLORS=",
    'routing constants',
)

# Visible routing grid: deliberately only in Circuit Builder game mode.
grid_fn = r'''// v0.51 circuit grid routing — cable follows a visible orthogonal grid instead of every finger wobble.
function cbDrawRouteGrid(x,w,h){
 const spanW=Math.max(1,w-56),spanH=Math.max(1,h-56),gx=CB_ROUTE_GRID/spanW,gy=CB_ROUTE_GRID/spanH;
 x.save();x.beginPath();x.rect(18,18,w-36,h-36);x.clip();x.strokeStyle='#71869b';x.lineWidth=1;x.globalAlpha=.11;
 x.beginPath();
 for(let u=0;u<=1.0001;u+=gx){const p=cbBoardPx({x:u,y:0},w,h);if(p.x>=18&&p.x<=w-18){x.moveTo(p.x,18);x.lineTo(p.x,h-18)}}
 for(let v=0;v<=1.0001;v+=gy){const p=cbBoardPx({x:0,y:v},w,h);if(p.y>=18&&p.y<=h-18){x.moveTo(18,p.y);x.lineTo(w-18,p.y)}}
 x.stroke();x.restore()
}
'''
once('function cbGhost(x,w,h,bounds,zoneId){', grid_fn + 'function cbGhost(x,w,h,bounds,zoneId){', 'route grid renderer')

old_paint = "cbGhost(x,w,h,bounds,cbCircuit?.zoneId||null);let routeColor='#df3f36';"
new_paint = "cbGhost(x,w,h,bounds,cbCircuit?.zoneId||null);if(cbScreen==='game')cbDrawRouteGrid(x,w,h);let routeColor='#df3f36';"
once(old_paint, new_paint, 'paint route grid')

old_append = "function cbAppendDrag(p,w,h){if(!cbDrag)return;let q=cbSnapPx(p,w,h),last=cbDrag.points.at(-1);if(!last||Math.hypot(q.x-last.x,q.y-last.y)<8)return;q=cbPairSnapPx(q,last,w,h);const dx=q.x-last.x,dy=q.y-last.y;if(Math.abs(dx)>1&&Math.abs(dy)>1){const prev=cbDrag.points.at(-2),horizontal=prev?Math.abs(last.y-prev.y)<Math.abs(last.x-prev.x):Math.abs(dx)>=Math.abs(dy),corner=horizontal?{x:q.x,y:last.y}:{x:last.x,y:q.y};cbDrag.points.push(corner)}cbDrag.points.push(q);cbDrag.points=cbSimplify(cbDrag.points)}"
new_append = r'''function cbRouteGridStep(q,w,h){
 if(!cbDrag?.points?.length)return;
 const pts=cbDrag.points,grid=Math.max(8,CB_ROUTE_GRID*Math.max(1,cbView.scale));
 let axis=cbDrag.routeAxis||null,last=pts.at(-1);
 if(!axis){
  const dx=q.x-last.x,dy=q.y-last.y;
  if(Math.max(Math.abs(dx),Math.abs(dy))<grid*.55)return;
  axis=Math.abs(dx)>=Math.abs(dy)?'h':'v';cbDrag.routeAxis=axis;
  pts.push(axis==='h'?{x:q.x,y:last.y}:{x:last.x,y:q.y});cbDrag.points=cbSimplify(pts);return
 }
 const turn=grid*CB_ROUTE_TURN_CELLS,perp=axis==='h'?Math.abs(q.y-last.y):Math.abs(q.x-last.x);
 if(perp>=turn){
  if(axis==='h'){last.x=q.x;pts.push({x:q.x,y:q.y});cbDrag.routeAxis='v'}
  else{last.y=q.y;pts.push({x:q.x,y:q.y});cbDrag.routeAxis='h'}
 }else{
  if(axis==='h')last.x=q.x;else last.y=q.y
 }
 cbDrag.points=cbSimplify(pts)
}
function cbAppendDrag(p,w,h){if(!cbDrag)return;let q=cbSnapPx(p,w,h),last=cbDrag.points.at(-1);if(!last)return;q=cbPairSnapPx(q,last,w,h);cbRouteGridStep(q,w,h)}'''
once(old_append, new_append, 'grid-locked drag routing')

# Every device starts a fresh grid leg, so the next run is not forced to continue the previous axis.
old_capture = "cbDrag.targets.push(target);cbDrag.from=target;cbDrag.points=[end];cbDrag.pairSnap=false;"
new_capture = "cbDrag.targets.push(target);cbDrag.from=target;cbDrag.points=[end];cbDrag.routeAxis=null;cbDrag.pairSnap=false;"
once(old_capture, new_capture, 'reset grid axis at device')

old_start = "cbDrag={points:[sp],previewLegs:[],targets:[],from:start,pointerId:e.pointerId,lastPointer:p};cbHover=null"
new_start = "cbDrag={points:[sp],previewLegs:[],targets:[],from:start,routeAxis:null,pointerId:e.pointerId,lastPointer:p};cbHover=null"
once(old_start, new_start, 'initial grid axis')

# Make the behaviour discoverable without adding another toolbar control.
t = t.replace(
    "Hold on the green-ring device and drag through detectors · pinch with two fingers to zoom",
    "Hold on the green-ring device and drag through detectors · cable snaps to grid · pinch with two fingers to zoom",
)

# Keep all main entry points identical. Company demos are intentionally excluded.
for name in ['index.html', 'ZoneSketch.html', 'Zone-Sketch-by-Will.html', 'app/src/main/assets/index.html']:
    Path(name).write_text(t)

# Android release version.
g = Path('app/build.gradle').read_text()
g = g.replace('versionCode 51', 'versionCode 52').replace("versionName '0.50'", "versionName '0.51'")
Path('app/build.gradle').write_text(g)

# Keep the tester/download pages pointing at the current main build where those strings exist.
for name in ['beta.html', 'download.html']:
    p = Path(name)
    if p.exists():
        s = p.read_text().replace('v0.50', 'v0.51').replace('Zone-Sketch-by-Will-v0.50.apk', 'Zone-Sketch-by-Will-v0.51.apk')
        p.write_text(s)

assert 'v0.51 circuit grid routing' in t
assert 'CB_ROUTE_GRID=24' in t
assert 'CB_ROUTE_TURN_CELLS=1.45' in t
assert 'function cbRouteGridStep' in t
assert "indexedDB.open('ZoneSketch-v1',1)" in t
print('Applied v0.51 clean grid-snapped Circuit Builder routing to main build only')
