from pathlib import Path

paths = [Path('index.html'), Path('ZoneSketch.html'), Path('app/src/main/assets/index.html')]
s = paths[0].read_text()


def replace_one(old, new, label):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly 1 match, found {count}')
    s = s.replace(old, new, 1)

# Compact section labels for the reorganised bottom toolbar.
replace_one(
    ".tools .divider{height:28px;border-left:1px solid #cbd5df;margin:0 2px}.status{font-size:11px;color:#66788c;white-space:nowrap}",
    ".tools .divider{height:28px;border-left:1px solid #cbd5df;margin:0 2px}.toolSection{font-size:10px;font-weight:800;letter-spacing:.08em;color:#728092;white-space:nowrap;padding:0 1px}.status{font-size:11px;color:#66788c;white-space:nowrap}",
    'toolbar section css',
)

# Grid controls: visibility, snapping and source-plan grid spacing.
replace_one(
    '<button id="gridBtn">Grid off</button><label class="wallControl" title="Building wall line thickness">Wall <input id="wallSize" type="range" min="0.75" max="5" step="0.25" value="3"><output id="wallSizeValue">3.00</output></label>',
    '<button id="gridBtn">Grid off</button><button id="snapGridBtn">Snap off</button><label class="wallControl" title="Grid spacing on the plan">Grid <input id="gridSize" type="range" min="20" max="250" step="10" value="100"><output id="gridSizeValue">100</output></label><label class="wallControl" title="Building wall line thickness">Wall <input id="wallSize" type="range" min="0.75" max="5" step="0.25" value="3"><output id="wallSizeValue">3.00</output></label>',
    'top grid controls',
)

replace_one(
    '<small>Box-select a room, then duplicate / rotate / mirror it with its objects.</small>',
    '<small>Select a room/group to move it, or drag one of the blue corner handles to resize it.</small>',
    'selection help',
)

# Put tools into a predictable onsite order: Draw -> Edit -> View -> History.
old_footer = '<footer class="tools"><button id="zoneMenuBtn" class="menuTool active">Zone · Box</button><button id="layoutMenuBtn" class="menuTool">Building layout</button><button id="objectMenuBtn" class="menuTool">Objects · Door</button><button id="symbolMenuBtn" class="menuTool">Symbols · Smoke</button><button id="detailMenuBtn" class="menuTool">Site details</button><button id="finish" hidden>Finish outline</button><span class="divider"></span><button data-tool="note">＋ Note</button><button data-tool="erase" class="danger">⌫ Delete</button><button data-tool="select">↖ Select / Move</button><button data-tool="group">▣ Box select</button><button id="makeGroup" disabled>Group</button><button id="breakGroup" disabled>Ungroup</button><button data-tool="pan">✋ Move plan</button><span class="divider"></span><button id="undo">↶ Undo</button><button id="redo">↷ Redo</button><button id="zoomOut">−</button><button id="zoomIn">＋</button><button id="fit">Fit</button><span class="status" id="status"></span></footer>'
new_footer = '<footer class="tools"><span class="toolSection">DRAW</span><button id="zoneMenuBtn" class="menuTool active">Zone · Box</button><button id="layoutMenuBtn" class="menuTool">Building layout</button><button id="objectMenuBtn" class="menuTool">Objects · Door</button><button id="symbolMenuBtn" class="menuTool">Symbols · Smoke</button><button id="detailMenuBtn" class="menuTool">Site details</button><button data-tool="note">＋ Note</button><button id="finish" hidden>Finish outline</button><span class="divider"></span><span class="toolSection">EDIT</span><button data-tool="select">↖ Select / Move</button><button data-tool="group">▣ Box select</button><button id="makeGroup" disabled>Group</button><button id="breakGroup" disabled>Ungroup</button><button data-tool="erase" class="danger">⌫ Delete</button><span class="divider"></span><span class="toolSection">VIEW</span><button data-tool="pan">✋ Move plan</button><button id="zoomOut">−</button><button id="zoomIn">＋</button><button id="fit">Fit</button><span class="divider"></span><span class="toolSection">HISTORY</span><button id="undo">↶ Undo</button><button id="redo">↷ Redo</button><span class="status" id="status"></span></footer>'
replace_one(old_footer, new_footer, 'footer order')

# Symbol colour palette inside the Symbols dropdown.
replace_one(
    '<div id="symbolMenu" class="toolPopup" aria-label="Favourite symbols"><h4>Symbol favourites</h4><div class="menuRow"><button data-symbol="panel">Panel</button><button data-symbol="mcp">MCP</button><button data-symbol="smoke">Smoke</button><button data-symbol="heat">Heat</button><button data-symbol="sounder">Sounder</button><button data-symbol="you">You are here</button></div><div class="menuHint">Tap-to-repeat: choose a symbol once, then stamp as many positions as you need.</div></div>',
    '<div id="symbolMenu" class="toolPopup" aria-label="Favourite symbols"><h4>Symbol favourites</h4><div class="menuRow"><button data-symbol="panel">Panel</button><button data-symbol="mcp">MCP</button><button data-symbol="smoke">Smoke</button><button data-symbol="heat">Heat</button><button data-symbol="sounder">Sounder</button><button data-symbol="you">You are here</button></div><div class="menuHint">Tap-to-repeat: choose a symbol once, then stamp as many positions as you need.</div><div class="menuSep"></div><h4>Symbol colour</h4><div id="symbolColors" class="colorbar"></div></div>',
    'symbol palette html',
)

replace_one(
    "const fresh=()=>({site:'',zones:[],shapes:[],notes:[],walls:[],doors:[],windows:[],shutters:[],stairs:[],labels:[],symbols:[],pins:[],pictureOpacity:1,pictureVisible:true,isBlank:false,gridVisible:false,wallWidth:3});",
    "const fresh=()=>({site:'',zones:[],shapes:[],notes:[],walls:[],doors:[],windows:[],shutters:[],stairs:[],labels:[],symbols:[],pins:[],pictureOpacity:1,pictureVisible:true,isBlank:false,gridVisible:false,snapGrid:false,gridSize:100,wallWidth:3});",
    'fresh state grid fields',
)
replace_one(
    "let imageRequest=0,opacityEditing=false,state=fresh(),img=null,tool='rect',selected=null,drawing=null,poly=[],zoom=1,pan={x:0,y:0},pointers=new Map(),gesture=null,pinchIds=new Set(),undo=[],redo=[],db=null,editId=null,chosenColor=colors[0],saveTimer,selection=[],lastZoneTool='rect',lastLayoutTool='wall',lastObjectTool='door',lastDetailTool='pinNote',roomStamp='Office',symbolStamp='smoke',pendingPhotoPin=null;",
    "let imageRequest=0,opacityEditing=false,state=fresh(),img=null,tool='rect',selected=null,drawing=null,poly=[],zoom=1,pan={x:0,y:0},pointers=new Map(),gesture=null,pinchIds=new Set(),undo=[],redo=[],db=null,editId=null,chosenColor=colors[0],saveTimer,selection=[],lastZoneTool='rect',lastLayoutTool='wall',lastObjectTool='door',lastDetailTool='pinNote',roomStamp='Office',symbolStamp='smoke',symbolColor='#172333',pendingPhotoPin=null;",
    'symbol colour state',
)
replace_one(
    "const floorKeys=['zones','shapes','notes','walls','doors','windows','shutters','stairs','labels','symbols','pins','pictureOpacity','pictureVisible','isBlank','gridVisible','wallWidth','image'];",
    "const floorKeys=['zones','shapes','notes','walls','doors','windows','shutters','stairs','labels','symbols','pins','pictureOpacity','pictureVisible','isBlank','gridVisible','snapGrid','gridSize','wallWidth','image'];",
    'floor grid fields',
)
replace_one(
    "for(const k of ['walls','doors','windows','shutters','stairs','labels','wallWidth'])data[k]=source[k]",
    "for(const k of ['walls','doors','windows','shutters','stairs','labels','wallWidth','gridVisible','snapGrid','gridSize'])data[k]=source[k]",
    'copy floor grid settings',
)

# Symbol colour palette behaviour.
replace_one(
    "const symbolNames={panel:'Panel',mcp:'MCP',smoke:'Smoke',heat:'Heat',sounder:'Sounder',you:'You are here'};",
    "const symbolNames={panel:'Panel',mcp:'MCP',smoke:'Smoke',heat:'Heat',sounder:'Sounder',you:'You are here'};\nconst symbolColors=['#172333',...colors];\nfunction renderSymbolColors(){const box=$('symbolColors');if(!box)return;box.textContent='';for(const color of symbolColors){const b=document.createElement('button');b.style.background=color;b.className=color===symbolColor?'chosen':'';b.setAttribute('aria-label','Symbol colour '+color);b.onclick=e=>{e.stopPropagation();symbolColor=color;renderSymbolColors()};box.append(b)}}",
    'symbol colour logic',
)

# Fixed-size grid plus optional drawing snap.
old_grid = "function syncGrid(){const b=$('gridBtn');b.classList.toggle('active',!!state.gridVisible);b.textContent=state.gridVisible?'Grid on':'Grid off'}\nfunction drawGrid(c,v){if(!state.gridVisible||!img)return;const raw=Math.max(img.width,img.height)/32,step=Math.max(20,Math.round(raw/10)*10);const left=v.ox,top=v.oy,W=img.width*v.s,H=img.height*v.s;c.save();c.beginPath();c.rect(left,top,W,H);c.clip();c.lineWidth=1;c.strokeStyle='#486b8a32';c.beginPath();for(let x=0;x<=img.width+.001;x+=step){const sx=left+x*v.s;c.moveTo(sx,top);c.lineTo(sx,top+H)}for(let y=0;y<=img.height+.001;y+=step){const sy=top+y*v.s;c.moveTo(left,sy);c.lineTo(left+W,sy)}c.stroke();c.restore()}\nfunction syncBackground()"
new_grid = "function gridStep(){return Math.max(20,Number(state.gridSize)||100)}\nfunction snapGridPoint(p){if(!state.snapGrid||!img)return p;const step=gridStep();return{x:clamp(Math.round(p.x*img.width/step)*step/img.width),y:clamp(Math.round(p.y*img.height/step)*step/img.height)}}\nfunction snapGridDelta(dx,dy){if(!state.snapGrid||!img)return{x:dx,y:dy};const gx=gridStep()/img.width,gy=gridStep()/img.height;return{x:Math.round(dx/gx)*gx,y:Math.round(dy/gy)*gy}}\nfunction syncGrid(){const b=$('gridBtn'),snap=$('snapGridBtn'),size=$('gridSize'),out=$('gridSizeValue');b.classList.toggle('active',!!state.gridVisible);b.textContent=state.gridVisible?'Grid on':'Grid off';snap.classList.toggle('active',!!state.snapGrid);snap.textContent=state.snapGrid?'Snap on':'Snap off';size.value=gridStep();out.textContent=String(gridStep())}\nfunction drawGrid(c,v){if(!state.gridVisible||!img)return;const step=gridStep(),left=v.ox,top=v.oy,W=img.width*v.s,H=img.height*v.s;c.save();c.beginPath();c.rect(left,top,W,H);c.clip();c.lineWidth=1;c.strokeStyle='#486b8a32';c.beginPath();for(let x=0;x<=img.width+.001;x+=step){const sx=left+x*v.s;c.moveTo(sx,top);c.lineTo(sx,top+H)}for(let y=0;y<=img.height+.001;y+=step){const sy=top+y*v.s;c.moveTo(left,sy);c.lineTo(left+W,sy)}c.stroke();c.restore()}\nfunction syncBackground()"
replace_one(old_grid, new_grid, 'grid implementation')
replace_one(
    "$('opacity').oninput=e=>{if(!opacityEditing){push();opacityEditing=true}state.pictureOpacity=Number(e.target.value)/100;draw();persist()};$('opacity').onchange=()=>opacityEditing=false;$('togglePicture').onclick=()=>{push();state.pictureVisible=!state.pictureVisible;changed()};$('gridBtn').onclick=()=>{state.gridVisible=!state.gridVisible;syncGrid();draw();persist()};",
    "$('opacity').oninput=e=>{if(!opacityEditing){push();opacityEditing=true}state.pictureOpacity=Number(e.target.value)/100;draw();persist()};$('opacity').onchange=()=>opacityEditing=false;$('togglePicture').onclick=()=>{push();state.pictureVisible=!state.pictureVisible;changed()};$('gridBtn').onclick=()=>{state.gridVisible=!state.gridVisible;syncGrid();draw();persist()};$('snapGridBtn').onclick=()=>{state.snapGrid=!state.snapGrid;if(state.snapGrid)state.gridVisible=true;syncGrid();draw();persist()};$('gridSize').oninput=e=>{state.gridSize=Number(e.target.value);syncGrid();draw();persist()};",
    'grid handlers',
)

# Keep raw point conversion for hit testing and movement, add a snapped input point for drawing/stamping.
replace_one(
    "function point(x,y){const r=canvas.getBoundingClientRect(),v=transform();return{x:clamp((x-r.left-v.ox)/(img.width*v.s)),y:clamp((y-r.top-v.oy)/(img.height*v.s))}}",
    "function point(x,y){const r=canvas.getBoundingClientRect(),v=transform();return{x:clamp((x-r.left-v.ox)/(img.width*v.s)),y:clamp((y-r.top-v.oy)/(img.height*v.s))}}\nfunction inputPoint(x,y){return snapGridPoint(point(x,y))}",
    'input point helper',
)

# Labels and symbols get real visual bounds, so individual labels/symbols can be resized too.
replace_one(
    "function itemBounds(ref){const pts=itemPoints(ref);if(!pts.length)return null;return{x1:Math.min(...pts.map(p=>p.x)),y1:Math.min(...pts.map(p=>p.y)),x2:Math.max(...pts.map(p=>p.x)),y2:Math.max(...pts.map(p=>p.y))}}",
    "function itemBounds(ref){const o=getObj(ref);if(!o)return null;if(ref.type==='labels'&&img){const sc=o.scale||1,fs=Math.min(img.width,img.height)*.022*sc,w=(Math.max(1,(o.text||'').length)*fs*.62+fs*.9)/img.width,h=fs*1.6/img.height;return{x1:clamp(o.x-w/2),y1:clamp(o.y-h/2),x2:clamp(o.x+w/2),y2:clamp(o.y+h/2)}}if(ref.type==='symbols'&&img){const r=Math.min(img.width,img.height)*.018*(o.scale||1),w=r*2.5/img.width,h=r*2.5/img.height;return{x1:clamp(o.x-w/2),y1:clamp(o.y-h/2),x2:clamp(o.x+w/2),y2:clamp(o.y+h/2)}}const pts=itemPoints(ref);if(!pts.length)return null;return{x1:Math.min(...pts.map(p=>p.x)),y1:Math.min(...pts.map(p=>p.y)),x2:Math.max(...pts.map(p=>p.x)),y2:Math.max(...pts.map(p=>p.y))}}",
    'visual item bounds',
)

replace_one(
    "function selectionBounds(){const bs=selection.map(itemBounds).filter(Boolean);if(!bs.length)return null;return{x1:Math.min(...bs.map(b=>b.x1)),y1:Math.min(...bs.map(b=>b.y1)),x2:Math.max(...bs.map(b=>b.x2)),y2:Math.max(...bs.map(b=>b.y2))}}",
    "function selectionBounds(){const bs=selection.map(itemBounds).filter(Boolean);if(!bs.length)return null;return{x1:Math.min(...bs.map(b=>b.x1)),y1:Math.min(...bs.map(b=>b.y1)),x2:Math.max(...bs.map(b=>b.x2)),y2:Math.max(...bs.map(b=>b.y2))}}\nfunction selectionScreenBox(){const b=selectionBounds();if(!b||!img)return null;const p1=screenPoint({x:b.x1,y:b.y1}),p2=screenPoint({x:b.x2,y:b.y2});return{x:Math.min(p1.x,p2.x)-8,y:Math.min(p1.y,p2.y)-8,w:Math.abs(p2.x-p1.x)+16,h:Math.abs(p2.y-p1.y)+16,bounds:b}}\nfunction selectionCanResize(){const b=selectionScreenBox();return !!b&&b.w>=28&&b.h>=28}\nfunction selectionHandleHit(clientX,clientY){if(!selectionCanResize())return null;const r=canvas.getBoundingClientRect(),p={x:clientX-r.left,y:clientY-r.top},b=selectionScreenBox(),corners={nw:{x:b.x,y:b.y},ne:{x:b.x+b.w,y:b.y},se:{x:b.x+b.w,y:b.y+b.h},sw:{x:b.x,y:b.y+b.h}};let best=null,d=18;for(const [name,c] of Object.entries(corners)){const dist=Math.hypot(p.x-c.x,p.y-c.y);if(dist<=d){best=name;d=dist}}return best}\nfunction resizeSelectionFromHandle(d,target){const old=d.bounds,t=snapGridPoint(target),minX=Math.max(.002,8/img.width),minY=Math.max(.002,8/img.height);let x1=old.x1,y1=old.y1,x2=old.x2,y2=old.y2;if(d.handle.includes('w'))x1=Math.min(t.x,x2-minX);if(d.handle.includes('e'))x2=Math.max(t.x,x1+minX);if(d.handle.includes('n'))y1=Math.min(t.y,y2-minY);if(d.handle.includes('s'))y2=Math.max(t.y,y1+minY);const ow=Math.max(minX,old.x2-old.x1),oh=Math.max(minY,old.y2-old.y1),nw=Math.max(minX,x2-x1),nh=Math.max(minY,y2-y1),sx=nw/ow,sy=nh/oh;for(const snap of d.snap){const o=getObj(snap.ref);if(!o)continue;const fn=p=>({x:clamp(x1+(p.x-old.x1)*sx),y:clamp(y1+(p.y-old.y1)*sy)});mapObjectPoints(snap.ref.type,o,fn);if(snap.ref.type==='labels'||snap.ref.type==='symbols')o.scale=Math.max(.25,Math.min(4,(snap.orig.scale||1)*Math.sqrt(Math.abs(sx*sy))))}}",
    'resize helpers',
)

# Selection box gains four tactile resize handles.
old_draw_selection = "function drawSelection(c,map){if(drawing?.mode==='selectBox'){const a=drawing.startScreen,b=drawing.nowScreen;c.save();c.fillStyle='#2576b522';c.strokeStyle='#2576b5';c.lineWidth=2;c.setLineDash([7,5]);c.fillRect(Math.min(a.x,b.x),Math.min(a.y,b.y),Math.abs(b.x-a.x),Math.abs(b.y-a.y));c.strokeRect(Math.min(a.x,b.x),Math.min(a.y,b.y),Math.abs(b.x-a.x),Math.abs(b.y-a.y));c.restore()}const b=selectionBounds();if(!b)return;const p1=map({x:b.x1,y:b.y1}),p2=map({x:b.x2,y:b.y2});c.save();c.strokeStyle='#2576b5';c.fillStyle='#2576b511';c.lineWidth=2;c.setLineDash([8,5]);const x=Math.min(p1.x,p2.x)-8,y=Math.min(p1.y,p2.y)-8,w=Math.abs(p2.x-p1.x)+16,h=Math.abs(p2.y-p1.y)+16;c.fillRect(x,y,w,h);c.strokeRect(x,y,w,h);c.setLineDash([]);c.restore()}"
new_draw_selection = "function drawSelection(c,map){if(drawing?.mode==='selectBox'){const a=drawing.startScreen,b=drawing.nowScreen;c.save();c.fillStyle='#2576b522';c.strokeStyle='#2576b5';c.lineWidth=2;c.setLineDash([7,5]);c.fillRect(Math.min(a.x,b.x),Math.min(a.y,b.y),Math.abs(b.x-a.x),Math.abs(b.y-a.y));c.strokeRect(Math.min(a.x,b.x),Math.min(a.y,b.y),Math.abs(b.x-a.x),Math.abs(b.y-a.y));c.restore()}const box=selectionScreenBox();if(!box)return;c.save();c.strokeStyle='#2576b5';c.fillStyle='#2576b511';c.lineWidth=2;c.setLineDash([8,5]);c.fillRect(box.x,box.y,box.w,box.h);c.strokeRect(box.x,box.y,box.w,box.h);c.setLineDash([]);if(selectionCanResize()){c.fillStyle='#fff';c.strokeStyle='#2576b5';c.lineWidth=2;for(const p of [{x:box.x,y:box.y},{x:box.x+box.w,y:box.y},{x:box.x+box.w,y:box.y+box.h},{x:box.x,y:box.y+box.h}]){c.fillRect(p.x-6,p.y-6,12,12);c.strokeRect(p.x-6,p.y-6,12,12)}}c.restore()}"
replace_one(old_draw_selection, new_draw_selection, 'selection handles')

# Symbol and label scales/colours on screen and in export.
s = s.replace("drawSymbol(ctx,p,sm.type,stampSize)", "drawSymbol(ctx,p,sm.type,stampSize*(sm.scale||1),sm.color||'#172333')")
s = s.replace("roomLabel(ctx,p.x,p.y,l.text,fs)", "roomLabel(ctx,p.x,p.y,l.text,fs*(l.scale||1))")
s = s.replace("drawSymbol(x,map(sm),sm.type,stampSize)", "drawSymbol(x,map(sm),sm.type,stampSize*(sm.scale||1),sm.color||'#172333')")
s = s.replace("roomLabel(x,p.x,p.y,l.text,Math.max(11,W/120))", "roomLabel(x,p.x,p.y,l.text,Math.max(11,W/120)*(l.scale||1))")

# Use grid-snapped points for drawing/stamping while preserving wall-object snapping.
repls = [
    ("if(tool==='wall'){const p=snapToWalls(point(e.clientX,e.clientY));", "if(tool==='wall'){const p=snapToWalls(inputPoint(e.clientX,e.clientY));"),
    ("if(tool==='stairs'){const p=point(e.clientX,e.clientY);", "if(tool==='stairs'){const p=inputPoint(e.clientX,e.clientY);"),
    ("if(tool==='rect'){if(!selected){openModal();return}const p=point(e.clientX,e.clientY);", "if(tool==='rect'){if(!selected){openModal();return}const p=inputPoint(e.clientX,e.clientY);"),
    ("if(tool==='layoutRect'){const p=point(e.clientX,e.clientY);", "if(tool==='layoutRect'){const p=inputPoint(e.clientX,e.clientY);"),
    ("drawing.now=snappedAxis(drawing.start,snapToWalls(point(e.clientX,e.clientY)))", "drawing.now=snappedAxis(drawing.start,snapToWalls(inputPoint(e.clientX,e.clientY)))"),
    ("drawing.now=point(e.clientX,e.clientY);draw()}else if(tool==='group'", "drawing.now=inputPoint(e.clientX,e.clientY);draw()}else if(tool==='group'"),
    ("const a=drawing.start,b=snappedAxis(a,snapToWalls(point(e.clientX,e.clientY)))", "const a=drawing.start,b=snappedAxis(a,snapToWalls(inputPoint(e.clientX,e.clientY)))"),
]
# The wall pointer-up line has 'const a=' in current source, so patch it separately below if needed.
for old, new in repls:
    if old in s:
        s = s.replace(old, new, 1)

s = s.replace("const a=drawing.start,b=snappedAxis(a,snapToWalls(point(e.clientX,e.clientY)));", "const a=drawing.start,b=snappedAxis(a,snapToWalls(inputPoint(e.clientX,e.clientY)));", 1)
s = s.replace("if(tool==='stairs'&&drawing){const a=drawing.start,b=point(e.clientX,e.clientY);", "if(tool==='stairs'&&drawing){const a=drawing.start,b=inputPoint(e.clientX,e.clientY);", 1)
s = s.replace("if(tool==='rect'&&drawing){const a=drawing.start,b=point(e.clientX,e.clientY);", "if(tool==='rect'&&drawing){const a=drawing.start,b=inputPoint(e.clientX,e.clientY);", 1)
s = s.replace("else if(tool==='layoutRect'&&drawing){const a=drawing.start,b=point(e.clientX,e.clientY);", "else if(tool==='layoutRect'&&drawing){const a=drawing.start,b=inputPoint(e.clientX,e.clientY);", 1)
s = s.replace("poly.push(point(e.clientX,e.clientY));draw()", "poly.push(inputPoint(e.clientX,e.clientY));draw()", 1)
s = s.replace("state.labels.push({id:uid(),...point(e.clientX,e.clientY),text:roomStamp,group:null})", "state.labels.push({id:uid(),...inputPoint(e.clientX,e.clientY),text:roomStamp,scale:1,group:null})", 1)
s = s.replace("state.symbols.push({id:uid(),...point(e.clientX,e.clientY),type:symbolStamp,group:null})", "state.symbols.push({id:uid(),...inputPoint(e.clientX,e.clientY),type:symbolStamp,color:symbolColor,scale:1,group:null})", 1)
s = s.replace("state.pins.push({id:uid(),...point(e.clientX,e.clientY),kind:'note'", "state.pins.push({id:uid(),...inputPoint(e.clientX,e.clientY),kind:'note'", 1)
s = s.replace("pendingPhotoPin=point(e.clientX,e.clientY)", "pendingPhotoPin=inputPoint(e.clientX,e.clientY)", 1)
s = s.replace("state.labels.push({id:uid(),...point(e.clientX,e.clientY),text:value.trim().slice(0,35)})", "state.labels.push({id:uid(),...inputPoint(e.clientX,e.clientY),text:value.trim().slice(0,35),scale:1})", 1)
s = s.replace("state.notes.push({id:uid(),...point(e.clientX,e.clientY),text:value.trim().slice(0,50)})", "state.notes.push({id:uid(),...inputPoint(e.clientX,e.clientY),text:value.trim().slice(0,50)})", 1)

# Selection movement snaps by grid increments when Snap is enabled.
replace_one(
    "const now=point(e.clientX,e.clientY),dx=now.x-drawing.start.x,dy=now.y-drawing.start.y;if(!drawing.moved&&Math.hypot(dx,dy)>.003)",
    "const now=point(e.clientX,e.clientY),delta=snapGridDelta(now.x-drawing.start.x,now.y-drawing.start.y),dx=delta.x,dy=delta.y;if(!drawing.moved&&Math.hypot(dx,dy)>.003)",
    'snap selection movement',
)

# Corner-handle resize starts before normal selection/group hit testing.
needle = "if(tool==='select'){const hit=hitRefAt(e.clientX,e.clientY,28);"
insert = "if((tool==='select'||tool==='group')&&selection.length){const handle=selectionHandleHit(e.clientX,e.clientY);if(handle){drawing={mode:'resizeSelection',handle,bounds:selectionBounds(),snap:snapshotSelection(),startClient:{x:e.clientX,y:e.clientY},moved:false};draw();return}}if(tool==='select'){const hit=hitRefAt(e.clientX,e.clientY,28);"
replace_one(needle, insert, 'resize pointer down')

replace_one(
    "else if((tool==='group'||tool==='select')&&drawing?.mode==='moveSelection'){const now=point(e.clientX,e.clientY)",
    "else if((tool==='group'||tool==='select')&&drawing?.mode==='resizeSelection'){if(!drawing.moved&&Math.hypot(e.clientX-drawing.startClient.x,e.clientY-drawing.startClient.y)>3){push();drawing.moved=true}if(drawing.moved){resizeSelectionFromHandle(drawing,point(e.clientX,e.clientY));draw()}}else if((tool==='group'||tool==='select')&&drawing?.mode==='moveSelection'){const now=point(e.clientX,e.clientY)",
    'resize pointer move',
)
replace_one(
    "else if((tool==='group'||tool==='select')&&drawing?.mode==='moveSelection'){const moved=drawing.moved;drawing=null;if(moved){changed();setHint(selectionState().allSame?'Grouped object moved':'Object moved');setTimeout(hint,800)}else draw()}",
    "else if((tool==='group'||tool==='select')&&drawing?.mode==='resizeSelection'){const moved=drawing.moved;drawing=null;if(moved){changed();setHint('Selection resized from the corner');setTimeout(hint,900)}else draw()}else if((tool==='group'||tool==='select')&&drawing?.mode==='moveSelection'){const moved=drawing.moved;drawing=null;if(moved){changed();setHint(selectionState().allSame?'Grouped object moved':'Object moved');setTimeout(hint,800)}else draw()}",
    'resize pointer up',
)

# Keep colour palette initialised and expose corner-resize hint.
s = s.replace("select:'Tap an object and drag it · grouped objects move together as one'", "select:'Tap and drag to move · drag a blue corner handle to resize the selection'", 1)
s = s.replace("renderFloors();new ResizeObserver(draw).observe(wrap);", "renderFloors();renderSymbolColors();new ResizeObserver(draw).observe(wrap);", 1)

# Guard that the important replacements happened.
required = [
    'id="snapGridBtn"', 'id="gridSize"', 'id="symbolColors"',
    'function snapGridPoint', 'function resizeSelectionFromHandle',
    "color:symbolColor", "scale:1,group:null", 'toolSection',
]
for marker in required:
    if marker not in s:
        raise SystemExit(f'missing v0.12 marker: {marker}')

for p in paths:
    p.write_text(s)

readme = Path('README.md')
r = readme.read_text()
if '## Version 0.12' not in r:
    r += '''\n\n## Version 0.12\n\n- Selected rooms/groups can be resized by dragging blue corner handles. Quick room labels and favourite symbols scale with the selection.\n- Bottom toolbar is ordered into Draw, Edit, View and History sections for faster onsite use.\n- Grid spacing is adjustable and an optional Snap mode aligns new drawing points, stamps and selection movement to the grid.\n- Favourite symbols have a colour palette; the selected colour is stored on each placed symbol and is preserved in exports.\n'''
    readme.write_text(r)
