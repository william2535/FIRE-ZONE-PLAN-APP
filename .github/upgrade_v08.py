from pathlib import Path

FILES = [Path('index.html'), Path('ZoneSketch.html'), Path('app/src/main/assets/index.html')]


def rep(s, old, new, label, count=1):
    n = s.count(old)
    if n < count:
        raise SystemExit(f'{label}: expected at least {count} match(es), found {n}')
    return s.replace(old, new, count)


def upgrade(s):
    if 'id="wallSize"' in s and 'id="undoTop"' in s:
        print('v0.8 already applied')
        return s

    s = rep(
        s,
        ".top button.active{background:#47749f;color:#fff;box-shadow:inset 0 0 0 2px #8db4d8}.spacer{flex:1}",
        ".top button.active{background:#47749f;color:#fff;box-shadow:inset 0 0 0 2px #8db4d8}.top .wallControl{display:flex;align-items:center;gap:6px;background:#2a415d;border-radius:9px;padding:6px 9px;font-size:12px;font-weight:700;white-space:nowrap}.top .wallControl input{width:82px;padding:0;margin:0;background:transparent;border:0;accent-color:#ec493b}.top .wallControl output{min-width:28px;text-align:right;color:#dbe8f5}.top .iconBtn{min-width:42px;padding:9px 11px;font-size:18px;line-height:1}.spacer{flex:1}",
        'top controls css')

    old_header = '<header class="top"><div class="brand">ZONE SKETCH<small>ON-SITE DRAFT</small></div><input id="site" placeholder="Site / building name" aria-label="Site name"><div class="spacer"></div><button id="importBtn">Import plan</button><button id="newBtn">New</button><button id="blankBtn">New blank</button><button id="gridBtn">Grid off</button><button class="primary" id="shareBtn">Send to office</button></header>'
    new_header = '<header class="top"><div class="brand">ZONE SKETCH<small>ON-SITE DRAFT</small></div><input id="site" placeholder="Site / building name" aria-label="Site name"><div class="spacer"></div><button id="importBtn">Import plan</button><button id="newBtn">New</button><button id="blankBtn">New blank</button><button id="gridBtn">Grid off</button><label class="wallControl" title="Building wall line thickness">Wall <input id="wallSize" type="range" min="0.75" max="5" step="0.25" value="3"><output id="wallSizeValue">3.00</output></label><button class="primary" id="shareBtn">Send to office</button><button class="iconBtn" id="undoTop" aria-label="Undo" title="Undo">↶</button><button class="iconBtn" id="redoTop" aria-label="Redo" title="Redo">↷</button></header>'
    s = rep(s, old_header, new_header, 'top undo redo and wall size')

    s = rep(
        s,
        "const fresh=()=>({site:'',zones:[],shapes:[],notes:[],walls:[],doors:[],labels:[],pictureOpacity:1,pictureVisible:true,isBlank:false,gridVisible:false});",
        "const fresh=()=>({site:'',zones:[],shapes:[],notes:[],walls:[],doors:[],labels:[],pictureOpacity:1,pictureVisible:true,isBlank:false,gridVisible:false,wallWidth:3});",
        'wall width state')

    s = rep(
        s,
        "function updateButtons(){$('undo').disabled=!undo.length;$('redo').disabled=!redo.length}",
        "function updateButtons(){const noUndo=!undo.length,noRedo=!redo.length;$('undo').disabled=noUndo;$('redo').disabled=noRedo;$('undoTop').disabled=noUndo;$('redoTop').disabled=noRedo}",
        'top undo redo state')

    s = rep(
        s,
        "function changed(){renderZones();syncSelectionBar();draw();persist();updateButtons()}",
        "function changed(){renderZones();syncSelectionBar();syncWallSize();draw();persist();updateButtons()}",
        'sync wall control')

    grid_handler = "$('opacity').oninput=e=>{if(!opacityEditing){push();opacityEditing=true}state.pictureOpacity=Number(e.target.value)/100;draw();persist()};$('opacity').onchange=()=>opacityEditing=false;$('togglePicture').onclick=()=>{push();state.pictureVisible=!state.pictureVisible;changed()};$('gridBtn').onclick=()=>{state.gridVisible=!state.gridVisible;syncGrid();draw();persist()};"
    grid_new = grid_handler + "\nfunction syncWallSize(){const v=Number(state.wallWidth||3);$('wallSize').value=v;$('wallSizeValue').textContent=v.toFixed(2)}\n$('wallSize').oninput=e=>{state.wallWidth=Number(e.target.value);syncWallSize();draw();persist()};"
    s = rep(s, grid_handler, grid_new, 'wall size control logic')

    s = rep(
        s,
        "function drawDoor(c,a,b,width=3,side=1){const dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy);if(L<2)return;const nx=(-dy/L)*side,ny=(dx/L)*side,leaf={x:a.x+nx*L,y:a.y+ny*L};c.save();c.lineCap='round';c.lineJoin='round';c.strokeStyle='#172333';c.lineWidth=width;",
        "function drawDoor(c,a,b,width=3,side=1,color='#172333'){const dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy);if(L<2)return;const nx=(-dy/L)*side,ny=(dx/L)*side,leaf={x:a.x+nx*L,y:a.y+ny*L};c.save();c.lineCap='round';c.lineJoin='round';c.strokeStyle=color;c.lineWidth=width;",
        'door preview colour support')

    old_split = "function splitWallForDoor(wallId,startT,endT){const idx=state.walls.findIndex(w=>w.id===wallId);if(idx<0)return false;const w=state.walls[idx],a=w.points[0],b=w.points[1],lo=Math.min(startT,endT),hi=Math.max(startT,endT);if(hi-lo<.02)return false;const low=lerp(a,b,lo),high=lerp(a,b,hi),hinge=startT<=endT?low:high,other=startT<=endT?high:low;state.walls.splice(idx,1);if(lo>.001)state.walls.push({id:uid(),kind:'wall',group:w.group||null,points:[a,low]});if(hi<.999)state.walls.push({id:uid(),kind:'wall',group:w.group||null,points:[high,b]});state.doors.push({id:uid(),group:w.group||null,a:hinge,b:other,side:1});return true}"
    new_split = "function splitWallForDoor(wallId,startT,endT,side=1){const idx=state.walls.findIndex(w=>w.id===wallId);if(idx<0)return false;const w=state.walls[idx],a=w.points[0],b=w.points[1],lo=Math.min(startT,endT),hi=Math.max(startT,endT);if(hi-lo<.02)return false;const low=lerp(a,b,lo),high=lerp(a,b,hi),hinge=startT<=endT?low:high,other=startT<=endT?high:low;state.walls.splice(idx,1);if(lo>.001)state.walls.push({id:uid(),kind:'wall',group:w.group||null,points:[a,low]});if(hi<.999)state.walls.push({id:uid(),kind:'wall',group:w.group||null,points:[high,b]});state.doors.push({id:uid(),group:w.group||null,a:hinge,b:other,side:side>=0?1:-1});return true}"
    s = rep(s, old_split, new_split, 'door side storage')

    marker = "function segDistPx(p,a,b){const dx=b.x-a.x,dy=b.y-a.y,l2=dx*dx+dy*dy;if(!l2)return Math.hypot(p.x-a.x,p.y-a.y);let t=((p.x-a.x)*dx+(p.y-a.y)*dy)/l2;t=clamp(t);return Math.hypot(p.x-(a.x+t*dx),p.y-(a.y+t*dy))}"
    helper = marker + "\nfunction doorSideFromPointer(w,q,clientX,clientY){const r=canvas.getBoundingClientRect(),finger={x:clientX-r.left,y:clientY-r.top},a=screenPoint(w.points[0]),b=screenPoint(w.points[1]),m=screenPoint(q.p),cross=(b.x-a.x)*(finger.y-m.y)-(b.y-a.y)*(finger.x-m.x);if(Math.abs(cross)<3)return 1;return cross>=0?1:-1}"
    s = rep(s, marker, helper, 'door finger side helper')

    s = rep(
        s,
        "door:'Drag along an existing wall · orange highlight shows exactly what will be removed'",
        "door:'Drag along an existing wall · move your finger to either side of the wall to choose the door swing · orange shows the opening'",
        'door hint')

    s = rep(
        s,
        "drawing={wallId:hit.wall.id,startT:hit.t,endT:hit.t,a:hit.p,b:hit.p};return",
        "drawing={wallId:hit.wall.id,startT:hit.t,endT:hit.t,a:hit.p,b:hit.p,side:1};return",
        'door initial side')

    old_move = "const q=proj(point(e.clientX,e.clientY),w.points[0],w.points[1]);drawing.endT=q.t;drawing.a=lerp(w.points[0],w.points[1],drawing.startT);drawing.b=q.p;draw()"
    new_move = "const q=proj(point(e.clientX,e.clientY),w.points[0],w.points[1]);drawing.endT=q.t;drawing.a=lerp(w.points[0],w.points[1],drawing.startT);drawing.b=q.p;drawing.side=doorSideFromPointer(w,q,e.clientX,e.clientY);draw()"
    s = rep(s, old_move, new_move, 'live door swing side')

    old_up = "push();if(splitWallForDoor(d.wallId,d.startT,q.t)){changed();setHint('Door snapped into wall');setTimeout(hint,900)}"
    new_up = "const side=doorSideFromPointer(w,q,e.clientX,e.clientY);push();if(splitWallForDoor(d.wallId,d.startT,q.t,side)){changed();setHint(side>0?'Door placed · swing side 1':'Door placed · swing side 2');setTimeout(hint,900)}"
    s = rep(s, old_up, new_up, 'save door swing side')

    old_preview = "if(drawing&&tool==='door'&&drawing.wallId){const a=map(drawing.a),b=map(drawing.b);ctx.save();ctx.strokeStyle='#f59e0b';ctx.lineWidth=8;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();ctx.fillStyle='#f59e0b';for(const p of [a,b]){ctx.beginPath();ctx.arc(p.x,p.y,6,0,Math.PI*2);ctx.fill()}ctx.restore()}"
    new_preview = "if(drawing&&tool==='door'&&drawing.wallId){const a=map(drawing.a),b=map(drawing.b);ctx.save();ctx.strokeStyle='#f59e0b';ctx.lineWidth=8;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();ctx.fillStyle='#f59e0b';for(const p of [a,b]){ctx.beginPath();ctx.arc(p.x,p.y,6,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=.78;drawDoor(ctx,a,b,Math.max(1,state.wallWidth*.85),drawing.side||1,'#f59e0b');ctx.restore()}"
    s = rep(s, old_preview, new_preview, 'live door swing preview')

    s = rep(s, "for(const wall of state.walls)stroke(ctx,wall.points.map(map),Math.max(2,3*Math.min(zoom,2)));", "for(const wall of state.walls)stroke(ctx,wall.points.map(map),state.wallWidth);", 'wall screen thickness')
    s = rep(s, "for(const door of state.doors)drawDoor(ctx,map(door.a),map(door.b),Math.max(2,2.4*Math.min(zoom,2)),door.side||1);", "for(const door of state.doors)drawDoor(ctx,map(door.a),map(door.b),Math.max(1,state.wallWidth*.85),door.side||1);", 'door screen thickness')
    s = rep(s, "if(drawing&&tool==='pen')stroke(ctx,drawing.points.map(map),3);", "if(drawing&&tool==='pen')stroke(ctx,drawing.points.map(map),state.wallWidth);", 'pen preview thickness')
    s = rep(s, "if(drawing&&tool==='wall')stroke(ctx,[drawing.start,drawing.now].map(map),3,'#2576b5');", "if(drawing&&tool==='wall')stroke(ctx,[drawing.start,drawing.now].map(map),state.wallWidth,'#2576b5');", 'wall preview thickness')
    s = rep(s, "ctx.strokeStyle='#172333';ctx.lineWidth=3;ctx.setLineDash([7,5]);ctx.strokeRect", "ctx.strokeStyle='#172333';ctx.lineWidth=state.wallWidth;ctx.setLineDash([7,5]);ctx.strokeRect", 'building box preview thickness')
    s = rep(s, "ctx.lineWidth=3;ctx.setLineDash([7,5]);ctx.stroke();", "ctx.lineWidth=tool==='layoutPoly'?state.wallWidth:1.4;ctx.setLineDash([7,5]);ctx.stroke();", 'outline preview thickness')

    s = rep(s, "for(const wall of state.walls)stroke(x,wall.points.map(map),Math.max(3,W/500));", "for(const wall of state.walls)stroke(x,wall.points.map(map),Math.max(.75,state.wallWidth*W/1600));", 'export wall thickness')
    s = rep(s, "for(const door of state.doors)drawDoor(x,map(door.a),map(door.b),Math.max(2.5,W/750),door.side||1);", "for(const door of state.doors)drawDoor(x,map(door.a),map(door.b),Math.max(.75,state.wallWidth*.85*W/1600),door.side||1);", 'export door thickness')

    s = rep(s, "c.width=1600;c.height=1000;", "c.width=3200;c.height=2000;", 'four-times blank canvas area')
    s = s.replace("Math.min(8,gesture.zoom", "Math.min(32,gesture.zoom")
    s = s.replace("zoom=Math.min(8,zoom*1.3)", "zoom=Math.min(32,zoom*1.3)")

    old_undo = "$('undo').onclick=()=>{if(!undo.length)return;redo.push(clone());restore(undo.pop())};$('redo').onclick=()=>{if(!redo.length)return;undo.push(clone());restore(redo.pop())};"
    new_undo = "function doUndo(){if(!undo.length)return;redo.push(clone());restore(undo.pop())}function doRedo(){if(!redo.length)return;undo.push(clone());restore(redo.pop())}$('undo').onclick=doUndo;$('undoTop').onclick=doUndo;$('redo').onclick=doRedo;$('redoTop').onclick=doRedo;"
    s = rep(s, old_undo, new_undo, 'shared top and bottom undo redo')

    s = rep(s, "new ResizeObserver(draw).observe(wrap);updateButtons();syncToolMenus();renderZoneMenu();load();draw();", "new ResizeObserver(draw).observe(wrap);syncWallSize();updateButtons();syncToolMenus();renderZoneMenu();load();draw();", 'initial wall control sync')

    return s


for path in FILES:
    original = path.read_text(encoding='utf-8')
    updated = upgrade(original)
    path.write_text(updated, encoding='utf-8')
    print(f'updated {path}: {len(original)} -> {len(updated)} bytes')

readme = Path('README.md')
r = readme.read_text(encoding='utf-8')
section = """

## Version 0.8 — detail drawing controls

- Undo and redo are duplicated in the top-right so they remain easy to reach while drawing.
- Door placement now uses the finger side of the wall to choose the swing direction, with a live orange opening and swing preview before release.
- Blank plans use a 3200 × 2000 working canvas (four times the previous pixel area), and maximum zoom is increased from 8× to 32× for intricate rooms and corners.
- A Wall size slider in the top bar controls building wall/pen/door thickness from 0.75 to 5 px without the old automatic thickening while zooming.
- The selected wall thickness is also respected in the exported office PNG.
"""
if '## Version 0.8 — detail drawing controls' not in r:
    readme.write_text(r.rstrip() + section + '\n', encoding='utf-8')
    print('updated README.md')
