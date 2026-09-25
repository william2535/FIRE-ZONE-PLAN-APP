from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'index.html'
s=SRC.read_text(encoding='utf-8')

old="function cbPostCaptureGeometryPoint(p){if(!cbDrag?.geometryOffset||!p)return p;return{x:p.x+cbDrag.geometryOffset.x,y:p.y+cbDrag.geometryOffset.y}}"
new="""function cbPostCaptureGeometryPoint(p,w,h){
 if(!cbDrag?.geometryPointer||!cbDrag?.geometryRaw||!p)return p;
 const rawPrev=cbDrag.geometryRaw,rawStep=Math.hypot(p.x-rawPrev.x,p.y-rawPrev.y);cbDrag.geometryRaw={...p};
 const v=cbDrag.geometryPointer,dx=p.x-v.x,dy=p.y-v.y,dist=Math.hypot(dx,dy);if(dist<.5){cbDrag.geometryPointer=null;cbDrag.geometryRaw=null;return p}if(rawStep<.35)return{...v};
 const cell=cbRouteCellPx(w,h),grid=Math.max(8,Math.min(cell.x,cell.y)),maxStep=Math.max(rawStep*1.72,Math.min(grid*.42,rawStep+2));
 if(dist<=maxStep){cbDrag.geometryPointer=null;cbDrag.geometryRaw=null;return p}
 const q={x:v.x+dx/dist*maxStep,y:v.y+dy/dist*maxStep};cbDrag.geometryPointer=q;return q
}"""
if old not in s: raise SystemExit('virtual geometry function marker not found')
s=s.replace(old,new,1)

old="const geometry=force?raw:cbPostCaptureGeometryPoint(raw),intent=cbGeometryIntent(geometry,w,h,force)"
new="const geometry=force?raw:cbPostCaptureGeometryPoint(raw,w,h),intent=cbGeometryIntent(geometry,w,h,force)"
if old not in s: raise SystemExit('geometry call marker not found')
s=s.replace(old,new,1)

old="cbDrag.geometryOffset={x:end.x-raw.x,y:end.y-raw.y};cbDrag.captureGuard={center:{...end},raw:{...raw}};"
new="cbDrag.geometryPointer={...end};cbDrag.geometryRaw={...raw};cbDrag.captureGuard={center:{...end},raw:{...raw}};"
if old not in s: raise SystemExit('capture geometry state marker not found')
s=s.replace(old,new,1)

old="routeInput:sp,geometryOffset:null,pointerId:e.pointerId"
new="routeInput:sp,geometryPointer:null,geometryRaw:null,pointerId:e.pointerId"
if old not in s: raise SystemExit('drag geometry state init marker not found')
s=s.replace(old,new,1)

old='// v0.58 Project Pineapple: post-capture raw movement is translated into detector-relative geometry.'
new='// v0.58 Project Pineapple: a bounded virtual pointer absorbs sparse-hit overshoot, then catches back up to raw touch.'
if old not in s: raise SystemExit('v0.58 marker missing')
s=s.replace(old,new,1)

SRC.write_text(s,encoding='utf-8')
for rel in ['Zone-Sketch-by-Will.html','ZoneSketch.html','app/src/main/assets/index.html']:
    shutil.copyfile(SRC,ROOT/rel)
print('Refined Project Pineapple v0.58 post-capture virtual-pointer catch-up in all app copies')
