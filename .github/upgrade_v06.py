from pathlib import Path
import re

p = Path('index.html')
s = p.read_text()

if 'id="zoneMenuBtn"' in s and 'data-menu-tool="layoutRect"' in s:
    print('Zone Sketch v0.6 already applied')
else:
    def need(old, new, count=1):
        global s
        if old not in s:
            raise SystemExit('Missing expected source fragment: ' + old[:140])
        s = s.replace(old, new, count)

    # Popup menu styling. Menus open upward from the bottom toolbar.
    need('.selectionBar .primary{background:#1c5e93;color:#fff}[hidden]{display:none!important}',
         '.selectionBar .primary{background:#1c5e93;color:#fff}.toolPopup{position:fixed;z-index:30;display:none;min-width:230px;max-width:min(92vw,360px);background:#fff;border:1px solid #c7d3df;border-radius:16px;padding:10px;box-shadow:0 16px 45px #15273e45}.toolPopup.open{display:block}.toolPopup h4{margin:2px 4px 8px;font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:#66788c}.toolPopup .menuRow{display:flex;gap:7px;flex-wrap:wrap}.toolPopup button{background:#eaf0f6;padding:9px 11px}.toolPopup button.active{background:#1c344f;color:#fff}.toolPopup .menuSep{height:1px;background:#dce4ec;margin:9px 0}.toolPopup .zoneChoice{display:flex;align-items:center;width:100%;text-align:left;margin-bottom:5px}.toolPopup .zoneChoice .swatch{margin-right:8px}.toolPopup .zoneChoice.active{background:#e9f2fc;color:#182332;box-shadow:inset 0 0 0 2px #2576b5}.toolPopup .zoneEmpty{font-size:12px;color:#66788c;padding:4px 5px 8px}.menuTool.active{background:#1c344f!important;color:#fff}[hidden]{display:none!important}')

    old_footer = '<footer class="tools"><button id="addZone" class="primary">+ Zone</button><span class="divider"></span><button data-tool="wall">Wall line</button><button data-tool="pen">Pen</button><button data-tool="door">Door</button><button data-tool="label">Room label</button><button data-tool="rect" class="active">▭ Box</button><button data-tool="poly">⬡ Outline</button><button id="finish" hidden>Finish outline</button><button data-tool="note">＋ Note</button><button data-tool="erase" class="danger">⌫ Delete</button><button data-tool="select">↖ Select / Move</button><button data-tool="group">▣ Box select</button><button id="makeGroup" disabled>Group</button><button id="breakGroup" disabled>Ungroup</button><button data-tool="pan">✋ Move plan</button><span class="divider"></span><button id="undo">↶ Undo</button><button id="redo">↷ Redo</button><button id="zoomOut">−</button><button id="zoomIn">＋</button><button id="fit">Fit</button><span class="status" id="status"></span></footer>'
    new_footer = '<footer class="tools"><button id="zoneMenuBtn" class="menuTool active">Zone · Box</button><button id="layoutMenuBtn" class="menuTool">Building layout</button><button id="finish" hidden>Finish outline</button><span class="divider"></span><button data-tool="note">＋ Note</button><button data-tool="erase" class="danger">⌫ Delete</button><button data-tool="select">↖ Select / Move</button><button data-tool="group">▣ Box select</button><button id="makeGroup" disabled>Group</button><button id="breakGroup" disabled>Ungroup</button><button data-tool="pan">✋ Move plan</button><span class="divider"></span><button id="undo">↶ Undo</button><button id="redo">↷ Redo</button><button id="zoomOut">−</button><button id="zoomIn">＋</button><button id="fit">Fit</button><span class="status" id="status"></span></footer>'
    need(old_footer, new_footer)

    # Keep the existing add-zone wiring alive with a hidden button, and add the two upward menus.
    need('</div>\n<input id="file" type="file" accept="image/*" hidden>',
         '''<div id="zoneMenu" class="toolPopup" aria-label="Zone tools"><h4>Zone</h4><div id="zoneMenuList"></div><div class="menuRow"><button id="zoneCreate">＋ Create zone</button></div><div class="menuSep"></div><div class="menuRow"><button data-menu-tool="rect">▭ Box</button><button data-menu-tool="poly">⬡ Outline</button></div></div>\n<div id="layoutMenu" class="toolPopup" aria-label="Building layout tools"><h4>Building layout</h4><div class="menuRow"><button data-menu-tool="wall">Wall</button><button data-menu-tool="pen">Pen</button><button data-menu-tool="door">Door</button><button data-menu-tool="layoutRect">▭ Box</button><button data-menu-tool="layoutPoly">⬡ Outline</button><button data-menu-tool="label">Room label</button></div></div>\n<button id="addZone" hidden></button>\n</div>\n<input id="file" type="file" accept="image/*" hidden>''')

    need("let opacityEditing=false,state=fresh(),img=null,tool='rect',selected=null,drawing=null,poly=[],zoom=1,pan={x:0,y:0},pointers=new Map(),gesture=null,pinchIds=new Set(),undo=[],redo=[],db=null,editId=null,chosenColor=colors[0],saveTimer,selection=[];",
         "let opacityEditing=false,state=fresh(),img=null,tool='rect',selected=null,drawing=null,poly=[],zoom=1,pan={x:0,y:0},pointers=new Map(),gesture=null,pinchIds=new Set(),undo=[],redo=[],db=null,editId=null,chosenColor=colors[0],saveTimer,selection=[],lastZoneTool='rect',lastLayoutTool='wall';")

    old_settool = "function setTool(t){tool=t;drawing=null;poly=[];if(t!=='group'&&t!=='select')clearSelection();document.querySelectorAll('[data-tool]').forEach(b=>b.classList.toggle('active',b.dataset.tool===t));$('finish').hidden=t!=='poly';hint();draw()}"
    new_settool = r"""const zoneTools=new Set(['rect','poly']),layoutTools=new Set(['wall','pen','door','layoutRect','layoutPoly','label']);
function toolLabel(t){return({rect:'Box',poly:'Outline',wall:'Wall',pen:'Pen',door:'Door',layoutRect:'Box',layoutPoly:'Outline',label:'Room label'})[t]||t}
function closeToolMenus(){document.querySelectorAll('.toolPopup.open').forEach(p=>p.classList.remove('open'))}
function placeMenu(panel,button){closeToolMenus();panel.classList.add('open');const r=button.getBoundingClientRect(),w=panel.offsetWidth,left=Math.max(8,Math.min(innerWidth-w-8,r.left));panel.style.left=left+'px';panel.style.bottom=Math.max(8,innerHeight-r.top+8)+'px'}
function toggleMenu(panel,button){if(panel.classList.contains('open'))closeToolMenus();else placeMenu(panel,button)}
function syncToolMenus(){const z=state.zones.find(z=>z.id===selected);$('zoneMenuBtn').textContent=z?'Zone '+z.number+' · '+toolLabel(lastZoneTool):'Zone · Create/select';$('layoutMenuBtn').textContent='Building · '+toolLabel(lastLayoutTool);$('zoneMenuBtn').classList.toggle('active',zoneTools.has(tool));$('layoutMenuBtn').classList.toggle('active',layoutTools.has(tool));document.querySelectorAll('[data-menu-tool]').forEach(b=>b.classList.toggle('active',b.dataset.menuTool===tool))}
function setTool(t){tool=t;drawing=null;poly=[];if(t!=='group'&&t!=='select')clearSelection();if(zoneTools.has(t))lastZoneTool=t;if(layoutTools.has(t))lastLayoutTool=t;document.querySelectorAll('[data-tool]').forEach(b=>b.classList.toggle('active',b.dataset.tool===t));document.querySelectorAll('[data-menu-tool]').forEach(b=>b.classList.toggle('active',b.dataset.menuTool===t));$('finish').hidden=!(t==='poly'||t==='layoutPoly');syncToolMenus();closeToolMenus();hint();draw()}"""
    need(old_settool, new_settool)

    old_hint = "function hint(){if(!img){setHint('');return}const h={wall:'Drag a wall · ends snap to nearby walls · intersections split into deletable pieces',pen:'Draw freehand with your finger or stylus',door:'Drag along an existing wall · orange highlight shows exactly what will be removed',label:'Tap a room and type its name',rect:'Drag a box over a zone area',poly:'Tap zone corners, then Finish outline',note:'Tap the plan to add a note',erase:'Tap a wall section, door, label, note or zone area to delete only that item',select:'Tap an object and drag it · grouped objects move together as one',group:'Drag a blue box around several objects · then press Group',pan:'Drag to move · pinch to zoom'};setHint(h[tool]||'')}"
    new_hint = "function hint(){if(!img){setHint('');return}const h={wall:'Drag a wall · ends snap to nearby walls · intersections split into deletable pieces',pen:'Draw freehand with your finger or stylus',door:'Drag along an existing wall · orange highlight shows exactly what will be removed',layoutRect:'Drag a box to create four black building walls',layoutPoly:'Tap building corners, then Finish outline to create black walls',label:'Tap a room and type its name',rect:'Drag a box over the selected zone area',poly:'Tap zone corners, then Finish outline',note:'Tap the plan to add a note',erase:'Tap a wall section, door, label, note or zone area to delete only that item',select:'Tap an object and drag it · grouped objects move together as one',group:'Drag a blue box around several objects · then press Group',pan:'Drag to move · pinch to zoom'};setHint(h[tool]||'')}"
    need(old_hint, new_hint)

    # Layout rectangle preview and distinct outline preview.
    need("if(drawing&&tool==='rect'){const z=state.zones.find(z=>z.id===selected);if(z){const a=drawing.start,b=drawing.now;shape(ctx,[a,{x:b.x,y:a.y},b,{x:a.x,y:b.y}].map(map),z.color,z.number,2,true)}}\nif(poly.length){const z=state.zones.find(z=>z.id===selected);ctx.beginPath();poly.map(map).forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.strokeStyle=z?.color||'#ee3333';ctx.lineWidth=3;ctx.setLineDash([7,5]);ctx.stroke();ctx.setLineDash([])}",
         "if(drawing&&tool==='rect'){const z=state.zones.find(z=>z.id===selected);if(z){const a=drawing.start,b=drawing.now;shape(ctx,[a,{x:b.x,y:a.y},b,{x:a.x,y:b.y}].map(map),z.color,z.number,2,true)}}\nif(drawing&&tool==='layoutRect'){const a=map(drawing.start),b=map(drawing.now);ctx.save();ctx.strokeStyle='#172333';ctx.lineWidth=3;ctx.setLineDash([7,5]);ctx.strokeRect(Math.min(a.x,b.x),Math.min(a.y,b.y),Math.abs(b.x-a.x),Math.abs(b.y-a.y));ctx.restore()}\nif(poly.length){const z=tool==='poly'?state.zones.find(z=>z.id===selected):null;ctx.beginPath();poly.map(map).forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.strokeStyle=tool==='layoutPoly'?'#172333':(z?.color||'#ee3333');ctx.lineWidth=3;ctx.setLineDash([7,5]);ctx.stroke();ctx.setLineDash([])}")

    # Zone list also drives the compact Zone menu and current-zone label.
    old_render = "function renderZones(){const box=$('zones');box.textContent='';for(const z of state.zones){const b=document.createElement('button');b.className='zone'+(z.id===selected?' active':'');const sw=document.createElement('i');sw.className='swatch';sw.style.background=z.color;const txt=document.createElement('span');txt.className='label';const strong=document.createElement('b');strong.textContent='Zone '+z.number;const small=document.createElement('small');small.textContent=z.name||'Unnamed area';txt.append(strong,small);const edit=document.createElement('span');edit.className='edit';edit.textContent='✎';edit.title='Edit zone';b.append(sw,txt,edit);b.onclick=e=>{if(e.target===edit)openModal(z);else{selected=z.id;renderZones();draw()}};box.append(b)}}"
    new_render = r"""function renderZoneMenu(){const box=$('zoneMenuList');if(!box)return;box.textContent='';if(!state.zones.length){const e=document.createElement('div');e.className='zoneEmpty';e.textContent='No zones yet — create one first.';box.append(e);return}for(const z of state.zones){const b=document.createElement('button');b.className='zoneChoice'+(z.id===selected?' active':'');const sw=document.createElement('i');sw.className='swatch';sw.style.background=z.color;const t=document.createElement('span');t.textContent='Zone '+z.number+(z.name?' — '+z.name:'');b.append(sw,t);b.onclick=()=>{selected=z.id;renderZones();draw();closeToolMenus()};box.append(b)}}
function renderZones(){const box=$('zones');box.textContent='';for(const z of state.zones){const b=document.createElement('button');b.className='zone'+(z.id===selected?' active':'');const sw=document.createElement('i');sw.className='swatch';sw.style.background=z.color;const txt=document.createElement('span');txt.className='label';const strong=document.createElement('b');strong.textContent='Zone '+z.number;const small=document.createElement('small');small.textContent=z.name||'Unnamed area';txt.append(strong,small);const edit=document.createElement('span');edit.className='edit';edit.textContent='✎';edit.title='Edit zone';b.append(sw,txt,edit);b.onclick=e=>{if(e.target===edit)openModal(z);else{selected=z.id;renderZones();draw()}};box.append(b)}renderZoneMenu();syncToolMenus()}"""
    need(old_render, new_render)

    # Finish now knows whether it is completing a coloured zone or a black building outline.
    old_finish = "function finish(){if(poly.length>=3&&selected){push();state.shapes.push({id:uid(),zone:selected,points:poly});changed()}poly=[];draw()}$('finish').onclick=finish;\ndocument.querySelectorAll('[data-tool]').forEach(b=>b.onclick=()=>setTool(b.dataset.tool));"
    new_finish = r"""function finish(){if(tool==='poly'){if(poly.length>=3&&selected){push();state.shapes.push({id:uid(),zone:selected,points:poly});changed()}}else if(tool==='layoutPoly'){if(poly.length>=3){push();const pts=poly.slice();for(let i=0;i<pts.length;i++)addWallSegment(pts[i],pts[(i+1)%pts.length]);changed()}}poly=[];draw()}$('finish').onclick=finish;
document.querySelectorAll('[data-tool]').forEach(b=>b.onclick=()=>setTool(b.dataset.tool));document.querySelectorAll('[data-menu-tool]').forEach(b=>b.onclick=()=>setTool(b.dataset.menuTool));
$('zoneMenuBtn').onclick=()=>toggleMenu($('zoneMenu'),$('zoneMenuBtn'));$('layoutMenuBtn').onclick=()=>toggleMenu($('layoutMenu'),$('layoutMenuBtn'));$('zoneCreate').onclick=()=>{closeToolMenus();openModal()};
document.addEventListener('pointerdown',e=>{if(!e.target.closest('.toolPopup')&&!e.target.closest('#zoneMenuBtn')&&!e.target.closest('#layoutMenuBtn'))closeToolMenus()},true);"""
    need(old_finish, new_finish)

    # Pointer handling for building boxes and outlines.
    need("if(tool==='rect'){if(!selected){openModal();return}const p=point(e.clientX,e.clientY);drawing={start:p,now:p};return}",
         "if(tool==='rect'){if(!selected){openModal();return}const p=point(e.clientX,e.clientY);drawing={start:p,now:p};return}if(tool==='layoutRect'){const p=point(e.clientX,e.clientY);drawing={start:p,now:p};return}")
    need("else if(tool==='rect'&&drawing){drawing.now=point(e.clientX,e.clientY);draw()}",
         "else if((tool==='rect'||tool==='layoutRect')&&drawing){drawing.now=point(e.clientX,e.clientY);draw()}")
    need("if(tool==='rect'&&drawing){const a=drawing.start,b=point(e.clientX,e.clientY);drawing=null;const dx=Math.abs(a.x-b.x),dy=Math.abs(a.y-b.y);if(dx>.012&&dy>.012){push();state.shapes.push({id:uid(),zone:selected,points:[a,{x:b.x,y:a.y},b,{x:a.x,y:b.y}]});changed()}else draw()}\nelse if(tool==='poly'){if(!selected){openModal();return}poly.push(point(e.clientX,e.clientY));draw()}",
         "if(tool==='rect'&&drawing){const a=drawing.start,b=point(e.clientX,e.clientY);drawing=null;const dx=Math.abs(a.x-b.x),dy=Math.abs(a.y-b.y);if(dx>.012&&dy>.012){push();state.shapes.push({id:uid(),zone:selected,points:[a,{x:b.x,y:a.y},b,{x:a.x,y:b.y}]});changed()}else draw()}\nelse if(tool==='layoutRect'&&drawing){const a=drawing.start,b=point(e.clientX,e.clientY);drawing=null;const dx=Math.abs(a.x-b.x),dy=Math.abs(a.y-b.y);if(dx>.012&&dy>.012){push();const pts=[a,{x:b.x,y:a.y},b,{x:a.x,y:b.y}];for(let i=0;i<4;i++)addWallSegment(pts[i],pts[(i+1)%4]);changed()}else draw()}\nelse if(tool==='poly'||tool==='layoutPoly'){if(tool==='poly'&&!selected){openModal();return}poly.push(point(e.clientX,e.clientY));draw()}")

    # Keep menu labels fresh after loading/restoring and explain the simplified toolbar.
    need("new ResizeObserver(draw).observe(wrap);updateButtons();load();draw();",
         "new ResizeObserver(draw).observe(wrap);updateButtons();syncToolMenus();renderZoneMenu();load();draw();")
    need('Walls snap together and are split at corners/intersections, so individual protruding sections can be deleted. Box select lets you choose several items, Group makes them one object, and Select / Move lets you move either one item or a saved group.',
         'Use the Zone and Building layout menus to keep the toolbar clear. Building boxes/outlines create black wall segments; zone boxes/outlines use the selected zone colour.')

    for out in [Path('index.html'), Path('ZoneSketch.html'), Path('app/src/main/assets/index.html')]:
        out.write_text(s)

readme = Path('README.md')
r = readme.read_text()
if '## Version 0.6 — grouped Zone and Building Layout menus' not in r:
    r += """
## Version 0.6 — grouped Zone and Building Layout menus

- The bottom toolbar is simplified into two main drawing menus: **Zone** and **Building layout**.
- **Zone** shows the currently selected/created zone and contains **Box** and **Outline** for coloured zone areas, plus **Create zone** and the existing zone list.
- **Building layout** contains **Wall, Pen, Door, Box, Outline and Room label**. Its Box and Outline tools create black wall segments rather than zone areas, so they work with Delete, Select / Move and Group.
- Both menus open upward from the bottom toolbar and remember the last drawing tool used. Common edit controls remain directly accessible.
"""
    readme.write_text(r)

print('v0.6 source prepared')
