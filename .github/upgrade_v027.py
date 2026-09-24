from pathlib import Path

ROOT=Path('.')
paths=[ROOT/'index.html',ROOT/'ZoneSketch.html',ROOT/'Zone-Sketch-by-Will.html',ROOT/'app/src/main/assets/index.html']
text=paths[0].read_text()

def rep(old,new,label):
    global text
    if old not in text:
        raise SystemExit(f'v0.27 marker missing: {label}')
    text=text.replace(old,new,1)

# Release identity.
rep('Zone Sketch by Will v0.26','Zone Sketch by Will v0.27','browser title')
rep('ON SITE ZONE PLANNER · v0.26','ON SITE ZONE PLANNER · v0.27','home version')

# Extra UI styling for plan cleanup and four-corner perspective straightening.
css="""
.cleanupGrid{display:grid;grid-template-columns:1fr;gap:8px}.cleanupGrid label{margin:0}.cleanupGrid .sliderLine{display:grid;grid-template-columns:82px 1fr 48px;align-items:center;gap:8px}.cleanupGrid input[type=range]{width:100%}.perspectiveBox{width:min(820px,100%)}#perspectiveCanvas{display:block;width:100%;max-height:62vh;background:#202b38;border-radius:12px;touch-action:none;cursor:crosshair}.perspectiveHelp{font-size:12px;color:#617184;line-height:1.4}.backgroundBar .planEdit{font-weight:750}.snapPill{pointer-events:none}
@media(max-width:720px){.cleanupGrid .sliderLine{grid-template-columns:72px 1fr 42px}.perspectiveBox{padding:14px}}
"""
rep('</style>',css+'</style>','cleanup css')

# Background controls stay compact: two editing actions beside existing opacity/hide controls.
rep(
'''<div class="backgroundBar" id="backgroundBar" hidden><label for="opacity">Picture opacity <input id="opacity" type="range" min="0" max="100" value="100"><output id="opacityValue">100%</output></label><button id="togglePicture">Hide picture</button><small id="backgroundHelp">Opacity also applies to the exported PNG.</small></div>''',
'''<div class="backgroundBar" id="backgroundBar" hidden><label for="opacity">Picture opacity <input id="opacity" type="range" min="0" max="100" value="100"><output id="opacityValue">100%</output></label><button id="togglePicture">Hide picture</button><button id="cleanupPicture" class="planEdit">Clean up</button><button id="straightenPicture" class="planEdit">Perspective</button><small id="backgroundHelp">Opacity also applies to the exported PNG.</small></div>''',
'background bar')

# Import images and PDFs from the same obvious button.
rep('<input id="file" type="file" accept="image/*" hidden>','<input id="file" type="file" accept="image/*,application/pdf,.pdf" hidden>','plan file accept')
rep('Import a photo, PNG or JPG, or start a blank canvas and sketch the building yourself.','Import a photo, PNG, JPG or PDF plan, or start a blank canvas and sketch the building yourself.','empty import wording')

# Cleanup + perspective modals live with the existing modals, not as permanent toolbar clutter.
modal_marker='<div class="modal" id="propertyModal"><div class="box"><h2>Object properties</h2>'
if modal_marker not in text: raise SystemExit('v0.27 marker missing: property modal')
modals='''<div class="modal" id="cleanupModal"><div class="box"><h2>Clean up imported plan</h2><p class="small">These controls only change the imported background. Your walls, zones and symbols stay sharp.</p><div class="cleanupGrid"><label class="sliderLine"><span>Brightness</span><input id="planBrightness" type="range" min="50" max="160" step="1" value="100"><output id="planBrightnessValue">100%</output></label><label class="sliderLine"><span>Contrast</span><input id="planContrast" type="range" min="50" max="220" step="1" value="100"><output id="planContrastValue">100%</output></label><label class="sliderLine"><span>B&amp;W</span><input id="planGrayscale" type="range" min="0" max="100" step="1" value="0"><output id="planGrayscaleValue">0%</output></label></div><div class="row" style="justify-content:flex-start"><button id="planPreset">Plan preset</button><button id="planReset">Reset</button><button id="planRotate">Rotate 90°</button></div><div class="row"><button id="cleanupClose" class="primary">Done</button></div></div></div>
<div class="modal" id="perspectiveModal"><div class="box perspectiveBox"><h2>Perspective straighten</h2><p class="perspectiveHelp">Drag the four numbered corner handles onto the four corners of the floor plan, then Apply. Best used before tracing walls.</p><canvas id="perspectiveCanvas"></canvas><div class="row"><button id="perspectiveReset">Reset corners</button><button id="perspectiveCancel">Cancel</button><button id="perspectiveApply" class="primary">Apply</button></div></div></div>
'''
text=text.replace(modal_marker,modals+modal_marker,1)

# Bundle PDF.js locally so browser and Android builds do not need a network connection to open PDFs.
rep("<script>\n(()=>{'use strict';","<script src=\"vendor/pdf.min.js\"></script>\n<script>\n(()=>{'use strict';",'pdfjs script')

# Per-floor background cleanup state. Existing projects inherit the defaults.
rep(
"pins:[],pictureOpacity:1,pictureVisible:true,isBlank:false,gridVisible:false,",
"pins:[],pictureOpacity:1,pictureVisible:true,pictureBrightness:1,pictureContrast:1,pictureGrayscale:0,isBlank:false,gridVisible:false,",
'fresh background filters')
rep(
"'pins','pictureOpacity','pictureVisible','isBlank','gridVisible'",
"'pins','pictureOpacity','pictureVisible','pictureBrightness','pictureContrast','pictureGrayscale','isBlank','gridVisible'",
'floor keys background filters')
rep(
"pendingPhotoPin=null,navMode=false,tapStart=null,joinPending=null;",
"pendingPhotoPin=null,navMode=false,tapStart=null,joinPending=null,snapGuide=null,cleanupEditing=false,perspectiveCorners=null,perspectiveDrag=-1,perspectiveView=null;",
'new ui state')

# Apply cleanup filters consistently on screen and office exports.
rep(
"function picture(c,x,y,w,h){if(state.layers?.background!==false&&!state.isBlank&&state.pictureVisible){c.save();c.globalAlpha=state.pictureOpacity;c.drawImage(img,x,y,w,h);c.restore()}}",
"function pictureFilter(d=state){const br=Math.round((d.pictureBrightness??1)*100),ct=Math.round((d.pictureContrast??1)*100),gs=Math.round((d.pictureGrayscale??0)*100);return `brightness(${br}%) contrast(${ct}%) grayscale(${gs}%)`}\nfunction picture(c,x,y,w,h){if(state.layers?.background!==false&&!state.isBlank&&state.pictureVisible){c.save();c.globalAlpha=state.pictureOpacity;c.filter=pictureFilter(state);c.drawImage(img,x,y,w,h);c.restore()}}",
'onscreen picture filter')
rep(
"if(floorImg&&!d.isBlank&&d.pictureVisible){x.save();x.globalAlpha=d.pictureOpacity??1;x.drawImage(floorImg,pad,85,W,H);x.restore()}",
"if(floorImg&&!d.isBlank&&d.pictureVisible){x.save();x.globalAlpha=d.pictureOpacity??1;x.filter=pictureFilter(d);x.drawImage(floorImg,pad,85,W,H);x.restore()}",
'export picture filter')

# Clearer snap behaviour: endpoints, midpoints and wall bodies get a visible guide.
old_snap="function snapToWalls(p,maxPx=14){let best={p,d:maxPx+1};for(const w of state.walls){if(w.kind!=='wall'||w.points.length!==2)continue;for(const ep of w.points){const d=Math.hypot(screenPoint(p).x-screenPoint(ep).x,screenPoint(p).y-screenPoint(ep).y);if(d<best.d)best={p:{...ep},d}}const q=proj(p,w.points[0],w.points[1]),d=segDistScreen(p,w.points[0],w.points[1]);if(d<best.d)best={p:q.p,d}}return best.d<=maxPx?best.p:p}"
new_snap="function snapToWalls(p,maxPx=14){let best={p,d:maxPx+1,kind:null};for(const w of state.walls){if(w.kind!=='wall'||w.points.length!==2)continue;for(const ep of w.points){const d=Math.hypot(screenPoint(p).x-screenPoint(ep).x,screenPoint(p).y-screenPoint(ep).y);if(d<best.d)best={p:{...ep},d,kind:'END'}}const mid=lerp(w.points[0],w.points[1],.5),md=Math.hypot(screenPoint(p).x-screenPoint(mid).x,screenPoint(p).y-screenPoint(mid).y);if(md<best.d)best={p:mid,d:md,kind:'MID'};const q=proj(p,w.points[0],w.points[1]),d=segDistScreen(p,w.points[0],w.points[1]);if(d<best.d)best={p:q.p,d,kind:'WALL'}}if(best.d<=maxPx){snapGuide={p:best.p,kind:best.kind};return best.p}snapGuide=null;return p}"
rep(old_snap,new_snap,'wall snapping guide')
old_end="function snapWallEndPoint(p,excludeId,maxPx=18){let best={p:snapGridPoint(p),d:maxPx+1};for(const w of state.walls){if(w.id===excludeId||w.kind!=='wall'||w.points?.length!==2)continue;for(const ep of w.points){const d=Math.hypot(screenPoint(p).x-screenPoint(ep).x,screenPoint(p).y-screenPoint(ep).y);if(d<best.d)best={p:{...ep},d}}const mid=lerp(w.points[0],w.points[1],.5),md=Math.hypot(screenPoint(p).x-screenPoint(mid).x,screenPoint(p).y-screenPoint(mid).y);if(md<best.d)best={p:mid,d:md};const q=proj(p,w.points[0],w.points[1]),d=segDistScreen(p,w.points[0],w.points[1]);if(d<best.d)best={p:q.p,d}}return best.d<=maxPx?best.p:snapGridPoint(p)}"
new_end="function snapWallEndPoint(p,excludeId,maxPx=18){let best={p:snapGridPoint(p),d:maxPx+1,kind:null};for(const w of state.walls){if(w.id===excludeId||w.kind!=='wall'||w.points?.length!==2)continue;for(const ep of w.points){const d=Math.hypot(screenPoint(p).x-screenPoint(ep).x,screenPoint(p).y-screenPoint(ep).y);if(d<best.d)best={p:{...ep},d,kind:'END'}}const mid=lerp(w.points[0],w.points[1],.5),md=Math.hypot(screenPoint(p).x-screenPoint(mid).x,screenPoint(p).y-screenPoint(mid).y);if(md<best.d)best={p:mid,d:md,kind:'MID'};const q=proj(p,w.points[0],w.points[1]),d=segDistScreen(p,w.points[0],w.points[1]);if(d<best.d)best={p:q.p,d,kind:'WALL'}}if(best.d<=maxPx){snapGuide={p:best.p,kind:best.kind};return best.p}snapGuide=null;return snapGridPoint(p)}"
rep(old_end,new_end,'wall endpoint snapping guide')
rep("function setTool(t){joinPending=null;if(navMode){","function setTool(t){joinPending=null;snapGuide=null;if(navMode){",'clear snap guide on tool')
rep("canvas.onpointermove=e=>{if(!pointers.has(e.pointerId))return;pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});","canvas.onpointermove=e=>{if(!pointers.has(e.pointerId))return;snapGuide=null;pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});",'clear snap guide on move')

# Draw endpoint/midpoint snap markers plus full-width horizontal/vertical alignment guides while drawing walls.
preview_marker="if(!navMode&&drawing&&tool==='layoutEllipse'){const a=map(drawing.start),b=map(drawing.now),cx=(a.x+b.x)/2,cy=(a.y+b.y)/2,rx=Math.abs(b.x-a.x)/2,ry=Math.abs(b.y-a.y)/2;ctx.save();ctx.strokeStyle='#172333';ctx.lineWidth=state.wallWidth;ctx.setLineDash([7,5]);ctx.beginPath();ctx.ellipse(cx,cy,rx,ry,0,0,Math.PI*2);ctx.stroke();ctx.restore()}"
if preview_marker not in text: raise SystemExit('v0.27 marker missing: preview marker')
preview_extra="""\nif(!navMode&&drawing&&tool==='wall'){const a=drawing.start,b=drawing.now;ctx.save();ctx.strokeStyle='#2a88c9aa';ctx.lineWidth=1;ctx.setLineDash([6,5]);if(Math.abs(a.x-b.x)<1e-7){const p1=map({x:b.x,y:0}),p2=map({x:b.x,y:1});ctx.beginPath();ctx.moveTo(p1.x,p1.y);ctx.lineTo(p2.x,p2.y);ctx.stroke()}if(Math.abs(a.y-b.y)<1e-7){const p1=map({x:0,y:b.y}),p2=map({x:1,y:b.y});ctx.beginPath();ctx.moveTo(p1.x,p1.y);ctx.lineTo(p2.x,p2.y);ctx.stroke()}ctx.restore()}\nif(!navMode&&snapGuide){const p=map(snapGuide.p);ctx.save();ctx.strokeStyle='#0b7fc0';ctx.fillStyle='#fff';ctx.lineWidth=2.5;ctx.beginPath();ctx.arc(p.x,p.y,snapGuide.kind==='END'?8:6,0,Math.PI*2);ctx.fill();ctx.stroke();const label=snapGuide.kind||'SNAP';ctx.font='bold 10px system-ui';const tw=ctx.measureText(label).width+10;ctx.fillStyle='#0b7fc0';ctx.fillRect(p.x+10,p.y-10,tw,18);ctx.fillStyle='#fff';ctx.fillText(label,p.x+15,p.y+3);ctx.restore()}"""
text=text.replace(preview_marker,preview_marker+preview_extra,1)

# Plan cleanup controls, PDF rendering and perspective correction helpers.
sync_old="function syncBackground(){const locked=!!state.locks?.background;$('backgroundBar').hidden=!img||state.isBlank;$('opacity').value=Math.round(state.pictureOpacity*100);$('opacityValue').textContent=Math.round(state.pictureOpacity*100)+'%';$('opacity').disabled=!state.pictureVisible||locked;$('togglePicture').disabled=locked;$('importBtn').disabled=locked&&!!img;$('togglePicture').textContent=state.pictureVisible?'Hide picture':'Show picture';$('backgroundHelp').textContent=locked?'Background locked · unlock it from Locks to replace, hide or fade it.':(state.pictureVisible?'Opacity also applies to the exported PNG.':'Picture excluded from export. Your drawing stays in place.')}"
sync_new="function syncBackground(){const locked=!!state.locks?.background;$('backgroundBar').hidden=!img||state.isBlank;$('opacity').value=Math.round(state.pictureOpacity*100);$('opacityValue').textContent=Math.round(state.pictureOpacity*100)+'%';$('opacity').disabled=!state.pictureVisible||locked;$('togglePicture').disabled=locked;$('cleanupPicture').disabled=locked;$('straightenPicture').disabled=locked;$('importBtn').disabled=locked&&!!img;$('togglePicture').textContent=state.pictureVisible?'Hide picture':'Show picture';$('backgroundHelp').textContent=locked?'Background locked · unlock it from Locks to replace, hide or edit it.':(state.pictureVisible?'Fade, clean up or straighten the imported plan before tracing.':'Picture excluded from export. Your drawing stays in place.')}"
rep(sync_old,sync_new,'sync background')

background_helpers=r'''function hasDrawingObjects(){return ['shapes','notes','walls','doors','windows','shutters','stairs','labels','symbols','pins'].some(k=>(state[k]||[]).length)}
function syncCleanupModal(){const vals=[['planBrightness','planBrightnessValue',(state.pictureBrightness??1)*100],['planContrast','planContrastValue',(state.pictureContrast??1)*100],['planGrayscale','planGrayscaleValue',(state.pictureGrayscale??0)*100]];for(const [id,out,v] of vals){$(id).value=Math.round(v);$(out).textContent=Math.round(v)+'%'}}
function cleanupChanged(){if(!cleanupEditing){push();cleanupEditing=true}state.pictureBrightness=Number($('planBrightness').value)/100;state.pictureContrast=Number($('planContrast').value)/100;state.pictureGrayscale=Number($('planGrayscale').value)/100;syncCleanupModal();draw();persist()}
for(const id of ['planBrightness','planContrast','planGrayscale'])$(id).oninput=cleanupChanged;
$('cleanupPicture').onclick=()=>{if(!img||state.isBlank)return;cleanupEditing=false;syncCleanupModal();$('cleanupModal').classList.add('open')};
$('cleanupClose').onclick=()=>{cleanupEditing=false;$('cleanupModal').classList.remove('open');changed()};
$('planPreset').onclick=()=>{if(!cleanupEditing){push();cleanupEditing=true}state.pictureBrightness=1.10;state.pictureContrast=1.50;state.pictureGrayscale=1;syncCleanupModal();draw();persist()};
$('planReset').onclick=()=>{if(!cleanupEditing){push();cleanupEditing=true}state.pictureBrightness=1;state.pictureContrast=1;state.pictureGrayscale=0;syncCleanupModal();draw();persist()};
async function planBusy(label,fn){if(!$('busyOverlay').hidden)return;$('busyOverlay').textContent=label;$('busyOverlay').hidden=false;try{await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));return await fn()}finally{$('busyOverlay').hidden=true}}
async function rotateBackground90(){if(!img||state.isBlank)return;if(hasDrawingObjects()&&!confirm('Rotate the imported plan? Existing drawing objects will stay in their current relative positions, so this is best done before tracing.'))return;push();const c=document.createElement('canvas');c.width=img.height;c.height=img.width;const x=c.getContext('2d');x.translate(c.width/2,c.height/2);x.rotate(Math.PI/2);x.drawImage(img,-img.width/2,-img.height/2);await setImage(c.toDataURL('image/jpeg',.92));state.isBlank=false;changed()}
$('planRotate').onclick=()=>planBusy('Rotating imported plan…',rotateBackground90);
function resetPerspectiveCorners(){perspectiveCorners=[{x:.02,y:.02},{x:.98,y:.02},{x:.98,y:.98},{x:.02,y:.98}]}
function drawPerspectiveEditor(){if(!img||!$('perspectiveModal').classList.contains('open'))return;const c=$('perspectiveCanvas'),x=c.getContext('2d'),maxW=900,maxH=560,s=Math.min(maxW/img.width,maxH/img.height,1),w=Math.max(220,Math.round(img.width*s)),h=Math.max(150,Math.round(img.height*s));c.width=w+40;c.height=h+40;perspectiveView={x:20,y:20,w,h};x.fillStyle='#202b38';x.fillRect(0,0,c.width,c.height);x.save();x.filter=pictureFilter(state);x.drawImage(img,20,20,w,h);x.restore();const pts=perspectiveCorners.map(q=>({x:20+q.x*w,y:20+q.y*h}));x.save();x.strokeStyle='#1fa3e5';x.lineWidth=3;x.beginPath();pts.forEach((p,i)=>i?x.lineTo(p.x,p.y):x.moveTo(p.x,p.y));x.closePath();x.stroke();pts.forEach((p,i)=>{x.fillStyle='#fff';x.strokeStyle='#0878b6';x.lineWidth=3;x.beginPath();x.arc(p.x,p.y,13,0,Math.PI*2);x.fill();x.stroke();x.fillStyle='#0878b6';x.font='bold 12px system-ui';x.textAlign='center';x.textBaseline='middle';x.fillText(String(i+1),p.x,p.y)});x.restore()}
function openPerspective(){if(!img||state.isBlank)return;resetPerspectiveCorners();$('perspectiveModal').classList.add('open');requestAnimationFrame(drawPerspectiveEditor)}
$('straightenPicture').onclick=openPerspective;$('perspectiveCancel').onclick=()=>{$('perspectiveModal').classList.remove('open');perspectiveDrag=-1};$('perspectiveReset').onclick=()=>{resetPerspectiveCorners();drawPerspectiveEditor()};
const pc=$('perspectiveCanvas');pc.onpointerdown=e=>{if(!perspectiveView)return;const r=pc.getBoundingClientRect(),sx=pc.width/r.width,sy=pc.height/r.height,p={x:(e.clientX-r.left)*sx,y:(e.clientY-r.top)*sy};let best=-1,bd=32;perspectiveCorners.forEach((q,i)=>{const a={x:perspectiveView.x+q.x*perspectiveView.w,y:perspectiveView.y+q.y*perspectiveView.h},d=Math.hypot(p.x-a.x,p.y-a.y);if(d<bd){bd=d;best=i}});if(best>=0){perspectiveDrag=best;pc.setPointerCapture(e.pointerId)}};
pc.onpointermove=e=>{if(perspectiveDrag<0||!perspectiveView)return;const r=pc.getBoundingClientRect(),sx=pc.width/r.width,sy=pc.height/r.height,x=(e.clientX-r.left)*sx,y=(e.clientY-r.top)*sy;perspectiveCorners[perspectiveDrag]={x:clamp((x-perspectiveView.x)/perspectiveView.w),y:clamp((y-perspectiveView.y)/perspectiveView.h)};drawPerspectiveEditor()};
pc.onpointerup=pc.onpointercancel=()=>{perspectiveDrag=-1};
function warpPerspectiveApprox(source,corners){const sc=document.createElement('canvas');sc.width=source.width;sc.height=source.height;const sx=sc.getContext('2d',{willReadFrequently:true});sx.drawImage(source,0,0);const src=sx.getImageData(0,0,sc.width,sc.height),S=new Uint32Array(src.data.buffer),P=corners.map(q=>({x:q.x*(sc.width-1),y:q.y*(sc.height-1)})),dist=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y),rawW=(dist(P[0],P[1])+dist(P[3],P[2]))/2,rawH=(dist(P[0],P[3])+dist(P[1],P[2]))/2,scale=Math.min(1,1800/Math.max(rawW,rawH)),W=Math.max(160,Math.round(rawW*scale)),H=Math.max(120,Math.round(rawH*scale)),out=document.createElement('canvas');out.width=W;out.height=H;const ox=out.getContext('2d'),dst=ox.createImageData(W,H),D=new Uint32Array(dst.data.buffer);for(let y=0;y<H;y++){const v=H===1?0:y/(H-1),iv=1-v;for(let x=0;x<W;x++){const u=W===1?0:x/(W-1),iu=1-u,px=iu*iv*P[0].x+u*iv*P[1].x+u*v*P[2].x+iu*v*P[3].x,py=iu*iv*P[0].y+u*iv*P[1].y+u*v*P[2].y+iu*v*P[3].y,ix=Math.max(0,Math.min(sc.width-1,Math.round(px))),iy=Math.max(0,Math.min(sc.height-1,Math.round(py)));D[y*W+x]=S[iy*sc.width+ix]}}ox.putImageData(dst,0,0);return out}
$('perspectiveApply').onclick=async()=>{if(!img)return;if(hasDrawingObjects()&&!confirm('Apply perspective correction now? This changes the imported plan shape, so it is best done before tracing.'))return;const corners=perspectiveCorners.map(q=>({...q}));$('perspectiveModal').classList.remove('open');await planBusy('Straightening imported plan…',async()=>{push();const out=warpPerspectiveApprox(img,corners);await setImage(out.toDataURL('image/jpeg',.92));state.isBlank=false;changed()})};
async function renderPdfPlan(file){if(!window.pdfjsLib)throw Error('PDF renderer unavailable');if(file.size>30*1024*1024)throw Error('PDF too large');pdfjsLib.GlobalWorkerOptions.workerSrc='vendor/pdf.worker.min.js';const bytes=new Uint8Array(await file.arrayBuffer()),pdf=await pdfjsLib.getDocument({data:bytes}).promise;let pageNo=1;if(pdf.numPages>1){const raw=prompt(`This PDF has ${pdf.numPages} pages. Which page contains the floor plan?`,'1');if(raw===null)throw Error('cancelled');pageNo=Math.max(1,Math.min(pdf.numPages,parseInt(raw,10)||1))}const page=await pdf.getPage(pageNo),base=page.getViewport({scale:1}),scale=Math.min(4,3000/Math.max(base.width,base.height)),vp=page.getViewport({scale}),c=document.createElement('canvas');c.width=Math.max(1,Math.round(vp.width));c.height=Math.max(1,Math.round(vp.height));const x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);await page.render({canvasContext:x,viewport:vp}).promise;return c.toDataURL('image/jpeg',.94)}
async function renderImagePlan(file){const raw=await new Promise((ok,no)=>{const r=new FileReader();r.onload=()=>ok(r.result);r.onerror=no;r.readAsDataURL(file)}),i=await new Promise((ok,no)=>{const p=new Image();p.onload=()=>ok(p);p.onerror=no;p.src=raw}),max=3000,scale=Math.min(1,max/Math.max(i.width,i.height)),c=document.createElement('canvas');c.width=Math.max(1,Math.round(i.width*scale));c.height=Math.max(1,Math.round(i.height*scale));c.getContext('2d').drawImage(i,0,0,c.width,c.height);return c.toDataURL('image/jpeg',.90)}
async function installImportedPlan(src){push();state.shapes=[];state.notes=[];state.walls=[];state.doors=[];state.windows=[];state.shutters=[];state.stairs=[];state.labels=[];state.symbols=[];state.pins=[];selection=[];state.isBlank=false;state.pictureVisible=true;state.pictureOpacity=1;state.pictureBrightness=1;state.pictureContrast=1;state.pictureGrayscale=0;poly=[];drawing=null;await setImage(src);changed()}
'''
# Insert helpers immediately before existing opacity wiring so all referenced elements already exist.
wire_marker="$ ('opacity')"  # unused guard for readability
opacity_line="$('opacity').oninput=e=>{if(!opacityEditing){push();opacityEditing=true}state.pictureOpacity=Number(e.target.value)/100;draw();persist()}"
if opacity_line not in text: raise SystemExit('v0.27 marker missing: opacity wiring')
text=text.replace(opacity_line,background_helpers+'\n'+opacity_line,1)

# Replace old image-only importer with image/PDF importer.
old_import="function pick(){if(state.locks?.background&&img){setHint('Background is locked · unlock it from Locks first');setTimeout(hint,1400);return}$('file').click()}$('importBtn').onclick=pick;$('emptyImport').onclick=pick;$('file').onchange=async e=>{const f=e.target.files?.[0];e.target.value='';if(!f)return;if(!f.type.startsWith('image/')){alert('Please choose a photo, PNG or JPG. For a PDF, take a screenshot of its plan page.');return}if(img&&!confirm('Replace this floor’s plan? Its drawing and labels will be cleared. Other floors stay saved.'))return;try{const raw=await new Promise((ok,no)=>{const r=new FileReader();r.onload=()=>ok(r.result);r.onerror=no;r.readAsDataURL(f)});const i=await new Promise((ok,no)=>{const p=new Image();p.onload=()=>ok(p);p.onerror=no;p.src=raw});const max=3000,scale=Math.min(1,max/Math.max(i.width,i.height)),c=document.createElement('canvas');c.width=Math.round(i.width*scale);c.height=Math.round(i.height*scale);c.getContext('2d').drawImage(i,0,0,c.width,c.height);push();state.shapes=[];state.notes=[];state.walls=[];state.doors=[];state.windows=[];state.shutters=[];state.stairs=[];state.labels=[];state.symbols=[];state.pins=[];selection=[];state.isBlank=false;state.pictureVisible=true;state.pictureOpacity=1;poly=[];drawing=null;await setImage(c.toDataURL('image/jpeg',.88));changed()}catch(err){alert('Could not open that image. Try a JPG or PNG.')}};"
new_import="function pick(){if(state.locks?.background&&img){setHint('Background is locked · unlock it from Locks first');setTimeout(hint,1400);return}$('file').click()}$('importBtn').onclick=pick;$('emptyImport').onclick=pick;$('file').onchange=async e=>{const f=e.target.files?.[0];e.target.value='';if(!f)return;const isPdf=f.type==='application/pdf'||/\\.pdf$/i.test(f.name||'');if(!isPdf&&!f.type.startsWith('image/')){alert('Choose a photo, PNG, JPG or PDF floor plan.');return}if(img&&!confirm('Replace this floor’s plan? Its drawing and labels will be cleared. Other floors stay saved.'))return;try{const src=await planBusy(isPdf?'Opening PDF plan…':'Opening floor plan…',()=>isPdf?renderPdfPlan(f):renderImagePlan(f));if(src)await installImportedPlan(src)}catch(err){if(String(err?.message||err)==='cancelled')return;console.error(err);alert(isPdf?'Could not open that PDF. Try a smaller PDF or export the plan page as an image.':'Could not open that image. Try a JPG or PNG.')}};"
rep(old_import,new_import,'pdf/image importer')

# Keep cleanup state sane when the user swaps floors or restores old projects.
rep("opacityEditing=false;zoom=1;pan={x:0,y:0};","opacityEditing=false;cleanupEditing=false;snapGuide=null;zoom=1;pan={x:0,y:0};",'reset interaction filters')

# Keep browser/standalone/Android HTML copies identical.
for p in paths:p.write_text(text)

# Bundle pinned PDF.js 3.x legacy build locally for offline use.
node_pdf=ROOT/'node_modules/pdfjs-dist/build/pdf.min.js';node_worker=ROOT/'node_modules/pdfjs-dist/build/pdf.worker.min.js'
if not node_pdf.exists() or not node_worker.exists(): raise SystemExit('Run npm install pdfjs-dist@3.11.174 before upgrade script')
for base in [ROOT/'vendor',ROOT/'app/src/main/assets/vendor']:
    base.mkdir(parents=True,exist_ok=True)
    (base/'pdf.min.js').write_bytes(node_pdf.read_bytes())
    (base/'pdf.worker.min.js').write_bytes(node_worker.read_bytes())

# Android version.
build=ROOT/'app/build.gradle';b=build.read_text()
if 'versionCode 26' not in b or "versionName '0.26'" not in b: raise SystemExit('Expected Android v0.26 baseline')
b=b.replace('versionCode 26','versionCode 27',1).replace("versionName '0.26'","versionName '0.27'",1);build.write_text(b)
print('Applied v0.27 PDF import, plan cleanup, perspective correction and snap guides')
