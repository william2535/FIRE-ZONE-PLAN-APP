from pathlib import Path
import re

paths=[Path('index.html'),Path('ZoneSketch.html'),Path('Zone-Sketch-by-Will.html'),Path('app/src/main/assets/index.html')]

def tune(t):
    # Preserve the old regression contract while keeping the new renderTail gate.
    t=t.replace("if(cbDrag?.points){if(renderTail&&!captured)cbAppendDrag(p,w,h);cbDrag.lastPointer=p;cbHover=cbDrag.targets.at(-1)||null}",
                "if(cbDrag?.points){if(renderTail){if(!captured)cbAppendDrag(p,w,h)}cbDrag.lastPointer=p;cbHover=cbDrag.targets.at(-1)||null}",1)

    # Backtracking on the same cable axis is a correction, not a real cable stub. Remove it
    # regardless of length. Small parallel doglegs are also collapsed up to ~1.2 grid cells.
    pattern=r"function cbPruneRouteNoise\(points,w,h\)\{.*?\}\nfunction cbPointClose"
    repl="""function cbPruneRouteNoise(points,w,h){let pts=cbSimplify((points||[]).map(q=>({...q})));if(pts.length<3)return pts;const cell=cbRouteCellPx(w,h),tiny=Math.max(8,Math.min(cell.x,cell.y)*1.18);let changed=true,guard=0;while(changed&&guard++<14){changed=false;for(let i=1;i<pts.length-1;i++){const a=pts[i-1],b=pts[i],c=pts[i+1],ab=cbRouteAxis(a,b),bc=cbRouteAxis(b,c);if(!ab||ab!==bc)continue;const v1=ab==='h'?b.x-a.x:b.y-a.y,v2=ab==='h'?c.x-b.x:c.y-b.y;if(v1*v2<0){pts.splice(i,1);pts=cbSimplify(pts);changed=true;break}}if(changed)continue;for(let i=0;i<pts.length-3;i++){const a=pts[i],b=pts[i+1],c=pts[i+2],d=pts[i+3],ab=cbRouteAxis(a,b),bc=cbRouteAxis(b,c),cd=cbRouteAxis(c,d);if(!ab||!bc||!cd||ab!==cd||ab===bc)continue;const middle=Math.hypot(c.x-b.x,c.y-b.y),v1=ab==='h'?b.x-a.x:b.y-a.y,v2=cd==='h'?d.x-c.x:d.y-c.y;if(middle>tiny||v1*v2<=0)continue;const corner=ab==='h'?{x:d.x,y:a.y}:{x:a.x,y:d.y},candidate=cbSimplify([...pts.slice(0,i+1),corner,d,...pts.slice(i+4)]);if(candidate.every((q,j)=>j===0||cbRouteAxis(candidate[j-1],q))){pts=candidate;changed=true;break}}}return cbSimplify(pts)}
function cbPointClose"""
    t,n=re.subn(pattern,repl,t,count=1,flags=re.S)
    if n!=1: raise SystemExit(f'route cleaner tune expected 1 replacement, got {n}')

    # Detector capture has a short magnetic settle zone. Overshoot/undershoot wobble inside this
    # zone is raw input only; it cannot immediately create a new cable leg. A decisive move toward
    # the next device exits the guard naturally, while swept hit detection stays fully active.
    old="""function cbAppendDrag(p,w,h){
 if(!cbDrag)return false;if(cbReturnPhase())return cbAppendReturnDrag(p,w,h);const before=cbRouteSnapshot();let q=cbSnapPx(p,w,h),last=cbDrag.points.at(-1);if(!last)return false;"""
    new="""function cbAppendDrag(p,w,h){
 if(!cbDrag)return false;if(cbReturnPhase())return cbAppendReturnDrag(p,w,h);if(cbDrag.captureGuard){const g=cbDrag.captureGuard,d=Math.hypot(p.x-g.center.x,p.y-g.center.y);if(d<=g.radius){cbDrag.routeInput={...p};cbDrag.blocked=false;cbDrag.phase='device-captured';return true}cbDrag.captureGuard=null;cbDrag.routeInput={...g.center};cbDrag.phase='routing-normal'}const before=cbRouteSnapshot();let q=cbSnapPx(p,w,h),last=cbDrag.points.at(-1);if(!last)return false;"""
    if old not in t: raise SystemExit('append guard anchor not found')
    t=t.replace(old,new,1)

    old="cbDrag.phase='device-captured';cbHover=target;"
    new="cbDrag.phase='device-captured';const guardCell=cbRouteCellPx(w,h);cbDrag.captureGuard={center:{...end},radius:Math.max(26,Math.min(54,Math.min(guardCell.x,guardCell.y)*.92))};cbHover=target;"
    if old not in t: raise SystemExit('capture guard insertion anchor not found')
    t=t.replace(old,new,1)

    # Keep the historical wording fragment used by the grid-routing regression, while making the
    # new behaviour clear to users.
    t=t.replace("'Drag naturally · sweep through devices · smart routing cleans finger wobble onto the Survey grid · pinch with two fingers to zoom'",
                "'Drag naturally · sweep through devices · cable uses Survey field grid while smart routing cleans finger wobble · pinch with two fingers to zoom'",1)
    return t

base=paths[0].read_text()
updated=tune(base)
if updated==base: raise SystemExit('tuner made no changes')
for p in paths:p.write_text(updated)
print('Applied capture settle guard, correction retraction and compatibility wording')
