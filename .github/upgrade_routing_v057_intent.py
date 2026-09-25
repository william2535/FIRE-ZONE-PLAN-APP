from pathlib import Path

paths=[Path('index.html'),Path('ZoneSketch.html'),Path('Zone-Sketch-by-Will.html'),Path('app/src/main/assets/index.html')]

def patch(t):
    # Device hits stay driven by the raw swept corridor. Geometry gets an independently filtered
    # intention point, preventing high-frequency finger oscillation from becoming visible cable.
    anchor="function cbPointClose(a,b,e=2.25){"
    insert="""function cbGeometryIntent(p,w,h,force=false){if(!cbDrag||!p)return p;if(force){cbDrag.intentPoint={...p};return p}const cell=cbRouteCellPx(w,h),grid=Math.max(8,Math.min(cell.x,cell.y)),prev=cbDrag.intentPoint||cbDrag.routeInput||cbDrag.points?.at(-1)||p,dist=Math.hypot(p.x-prev.x,p.y-prev.y),alpha=dist>grid*2.5?.54:dist>grid*1.35?.43:.32,next={x:prev.x+(p.x-prev.x)*alpha,y:prev.y+(p.y-prev.y)*alpha};if(cbDrag.routeAxis&&!cbDrag.turnAnchor&&cbDrag.points?.length){const last=cbDrag.points.at(-1),axis=cbDrag.routeAxis,perp=axis==='h'?Math.abs(next.y-last.y):Math.abs(next.x-last.x),dead=(axis==='h'?cell.y:cell.x)*.52;if(perp<dead){if(axis==='h')next.y=last.y;else next.x=last.x}}cbDrag.intentPoint=next;return next}\n"""
    if anchor not in t: raise SystemExit('geometry intent insertion anchor missing')
    t=t.replace(anchor,insert+anchor,1)

    old="const appended=cbAppendDrag(hit.p,w,h);"
    if old not in t: raise SystemExit('device hit append anchor missing')
    t=t.replace(old,"const appended=cbAppendDrag(hit.p,w,h,true);",1)

    old="function cbAppendDrag(p,w,h){\n if(!cbDrag)return false;if(cbReturnPhase())return cbAppendReturnDrag(p,w,h);if(cbDrag.captureGuard){const g=cbDrag.captureGuard,d=Math.hypot(p.x-g.center.x,p.y-g.center.y);if(d<=g.radius){cbDrag.routeInput={...p};cbDrag.blocked=false;cbDrag.phase='device-captured';return true}cbDrag.captureGuard=null;cbDrag.routeInput={...g.center};cbDrag.phase='routing-normal'}const before=cbRouteSnapshot();let q=cbSnapPx(p,w,h),last=cbDrag.points.at(-1);if(!last)return false;\n q=cbPairSnapPx(q,last,w,h,p);cbRouteGridStep(q,w,h,p);"
    new="function cbAppendDrag(p,w,h,force=false){\n if(!cbDrag)return false;if(cbReturnPhase())return cbAppendReturnDrag(p,w,h);if(cbDrag.captureGuard){const g=cbDrag.captureGuard,d=Math.hypot(p.x-g.center.x,p.y-g.center.y);if(d<=g.radius&&!force){cbDrag.routeInput={...p};cbDrag.blocked=false;cbDrag.phase='device-captured';return true}cbDrag.captureGuard=null;cbDrag.routeInput={...g.center};cbDrag.intentPoint={...g.center};cbDrag.phase='routing-normal'}const intent=cbGeometryIntent(p,w,h,force),before=cbRouteSnapshot();let q=cbSnapPx(intent,w,h),last=cbDrag.points.at(-1);if(!last)return false;\n q=cbPairSnapPx(q,last,w,h,p);cbRouteGridStep(q,w,h,intent);"
    if old not in t: raise SystemExit('append intent replacement anchor missing')
    t=t.replace(old,new,1)

    # The route snapshot/restore is geometry-only. If a candidate is blocked, restore the filtered
    # intent as well so a rejected move cannot bias the next sample.
    old="if(cbChallengePointsBlocked(cbDrag.points,w,h)){cbRouteRestore(before);cbDrag.routeInput={...p};cbMarkBlocked();return false}\n cbDrag.routeInput={...p};cbDrag.blocked=false;"
    new="if(cbChallengePointsBlocked(cbDrag.points,w,h)){cbRouteRestore(before);cbDrag.intentPoint={...(before.routeInput||intent)};cbDrag.routeInput={...intent};cbMarkBlocked();return false}\n cbDrag.routeInput={...intent};cbDrag.blocked=false;"
    if old not in t: raise SystemExit('append routeInput anchor missing')
    t=t.replace(old,new,1)

    # Every captured device is a hard semantic anchor. Reset the geometry filter there, while raw
    # touch history continues independently for hit detection and the post-capture settle guard.
    old="cbDrag.routeInput=end;cbDrag.pairSnap=false;"
    new="cbDrag.routeInput=end;cbDrag.intentPoint={...end};cbDrag.pairSnap=false;"
    if old not in t: raise SystemExit('capture intent reset anchor missing')
    t=t.replace(old,new,1)

    old="returnGuide:null,phase:returning?'returning':'routing-normal',rawPoints:[{x:p.x,y:p.y}]};"
    new="returnGuide:null,phase:returning?'returning':'routing-normal',rawPoints:[{x:p.x,y:p.y}],intentPoint:{...sp}};"
    if old not in t: raise SystemExit('drag intent initialisation anchor missing')
    t=t.replace(old,new,1)

    return t

base=paths[0].read_text();updated=patch(base)
if updated==base: raise SystemExit('intent filter made no changes')
for p in paths:p.write_text(updated)
print('Applied independent low-pass geometry intent while preserving raw swept device capture')
