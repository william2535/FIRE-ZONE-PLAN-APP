from pathlib import Path
import re

FILES = [Path('index.html'), Path('ZoneSketch.html'), Path('app/src/main/assets/index.html')]


def rep(s, old, new, label, count=1):
    n = s.count(old)
    if n < count:
        raise SystemExit(f'{label}: expected at least {count} match(es), found {n}')
    return s.replace(old, new, count)


def upgrade(s):
    if 'id="symbolMenuBtn"' in s and 'id="exportAllFloors"' in s and 'function duplicateSelection()' in s:
        print('v0.11 already applied')
        return s

    # Small reusable menu styling additions.
    s = rep(
        s,
        ".toolPopup .zoneEmpty{font-size:12px;color:#66788c;padding:4px 5px 8px}.menuTool.active",
        ".toolPopup .zoneEmpty{font-size:12px;color:#66788c;padding:4px 5px 8px}.toolPopup .menuHint{font-size:11px;line-height:1.35;color:#66788c;padding:4px 5px}.toolPopup .floorChoice{display:flex;width:100%;text-align:left;justify-content:space-between;margin-bottom:5px}.toolPopup .floorChoice.active{background:#e9f2fc;color:#182332;box-shadow:inset 0 0 0 2px #2576b5}.menuTool.active",
        'menu styling')

    old_floor_bar = '<div class="backgroundBar" id="floorBar"><label for="floorSelect">Floor <select id="floorSelect" aria-label="Current floor"></select></label><button id="addFloor">＋ Add floor</button><button id="renameFloor">Rename</button><button id="deleteFloor">Delete floor</button><small>Send to office exports the selected floor.</small></div>'
    new_floor_bar = '<div class="backgroundBar" id="floorBar"><button id="floorMenuBtn" class="menuTool">Floor · Ground floor</button><select id="floorSelect" aria-label="Current floor" hidden></select><small>Send to office exports this floor · use Floor menu for the whole building.</small></div>'
    s = rep(s, old_floor_bar, new_floor_bar, 'floor dropdown button')

    old_selection = '<div class="selectionBar" id="selectionBar" hidden><strong id="selectionText">0 items selected</strong><button class="primary" id="groupSelected">Make group</button><button id="ungroupSelected">Ungroup</button><button id="clearSelection">Clear selection</button><small>Grouped items act as one object in Select / Move.</small></div>'
    new_selection = '<div class="selectionBar" id="selectionBar" hidden><strong id="selectionText">0 items selected</strong><button class="primary" id="groupSelected">Make group</button><button id="ungroupSelected">Ungroup</button><button id="duplicateSelected">Duplicate</button><button id="rotateSelected">Rotate 90°</button><button id="mirrorSelected">Mirror ↔</button><button id="clearSelection">Clear selection</button><small>Box-select a room, then duplicate / rotate / mirror it with its objects.</small></div>'
    s = rep(s, old_selection, new_selection, 'selection transform buttons')

    old_footer = '<footer class="tools"><button id="zoneMenuBtn" class="menuTool active">Zone · Box</button><button id="layoutMenuBtn" class="menuTool">Building layout</button><button id="objectMenuBtn" class="menuTool">Objects · Door</button><button id="finish" hidden>Finish outline</button>'
    new_footer = '<footer class="tools"><button id="zoneMenuBtn" class="menuTool active">Zone · Box</button><button id="layoutMenuBtn" class="menuTool">Building layout</button><button id="objectMenuBtn" class="menuTool">Objects · Door</button><button id="symbolMenuBtn" class="menuTool">Symbols · Smoke</button><button id="detailMenuBtn" class="menuTool">Site details</button><button id="finish" hidden>Finish outline</button>'
    s = rep(s, old_footer, new_footer, 'new grouped menus')

    old_layout_menu = '<div id="layoutMenu" class="toolPopup" aria-label="Building layout tools"><h4>Building layout</h4><div class="menuRow"><button data-menu-tool="wall">Wall</button><button data-menu-tool="pen">Pen</button><button data-menu-tool="layoutRect">▭ Box</button><button data-menu-tool="layoutPoly">⬡ Outline</button><button data-menu-tool="label">Room label</button></div></div>'
    new_layout_menu = '<div id="layoutMenu" class="toolPopup" aria-label="Building layout tools"><h4>Building layout</h4><div class="menuRow"><button data-menu-tool="wall">Wall</button><button data-menu-tool="pen">Pen</button><button data-menu-tool="layoutRect">▭ Box</button><button data-menu-tool="layoutPoly">⬡ Outline</button><button data-menu-tool="label">Room label</button></div><div class="menuSep"></div><h4>Quick room names</h4><div class="menuRow"><button data-room-name="Office">Office</button><button data-room-name="Store">Store</button><button data-room-name="Corridor">Corridor</button><button data-room-name="WC">WC</button><button data-room-name="Plant room">Plant room</button><button data-room-name="Custom">Custom…</button></div><div class="menuHint">Choose once, then tap multiple rooms to repeat the label.</div></div>'
    s = rep(s, old_layout_menu, new_layout_menu, 'quick room names')

    old_object_menu = '<div id="objectMenu" class="toolPopup" aria-label="Objects"><h4>Objects</h4><div class="menuRow"><button data-menu-tool="door">Door</button><button data-menu-tool="window">Window</button><button data-menu-tool="shutter">Roller shutter</button><button data-menu-tool="stairs">Stairway</button></div></div>'
    new_object_menu = old_object_menu + '\n<div id="symbolMenu" class="toolPopup" aria-label="Favourite symbols"><h4>Symbol favourites</h4><div class="menuRow"><button data-symbol="panel">Panel</button><button data-symbol="mcp">MCP</button><button data-symbol="smoke">Smoke</button><button data-symbol="heat">Heat</button><button data-symbol="sounder">Sounder</button><button data-symbol="you">You are here</button></div><div class="menuHint">Tap-to-repeat: choose a symbol once, then stamp as many positions as you need.</div></div>\n<div id="detailMenu" class="toolPopup" aria-label="Pinned site details"><h4>Site details</h4><div class="menuRow"><button data-detail-tool="pinNote">Pinned note</button><button data-detail-tool="pinPhoto">Pinned photo</button></div><div class="menuHint">Pins stay exactly where you tap and are listed in the office export.</div></div>\n<div id="floorMenu" class="toolPopup" aria-label="Floors"><h4>Floors</h4><div id="floorMenuList"></div><div class="menuSep"></div><div class="menuRow"><button id="addFloor">＋ Add floor</button><button id="renameFloor">Rename</button><button id="deleteFloor">Delete</button><button id="exportAllFloors" class="primary">Send all floors</button></div></div>'
    s = rep(s, old_object_menu, new_object_menu, 'symbols details and floor menus')

    s = rep(
        s,
        '<input id="file" type="file" accept="image/*" hidden>',
        '<input id="file" type="file" accept="image/*" hidden><input id="pinPhotoFile" type="file" accept="image/*" hidden>',
        'pinned photo file input')

    s = rep(
        s,
        "const fresh=()=>({site:'',zones:[],shapes:[],notes:[],walls:[],doors:[],windows:[],shutters:[],stairs:[],labels:[],pictureOpacity:1,pictureVisible:true,isBlank:false,gridVisible:false,wallWidth:3});",
        "const fresh=()=>({site:'',zones:[],shapes:[],notes:[],walls:[],doors:[],windows:[],shutters:[],stairs:[],labels:[],symbols:[],pins:[],pictureOpacity:1,pictureVisible:true,isBlank:false,gridVisible:false,wallWidth:3});",
        'symbols and pins state')
    s = rep(
        s,
        "let imageRequest=0,opacityEditing=false,state=fresh(),img=null,tool='rect',selected=null,drawing=null,poly=[],zoom=1,pan={x:0,y:0},pointers=new Map(),gesture=null,pinchIds=new Set(),undo=[],redo=[],db=null,editId=null,chosenColor=colors[0],saveTimer,selection=[],lastZoneTool='rect',lastLayoutTool='wall',lastObjectTool='door';",
        "let imageRequest=0,opacityEditing=false,state=fresh(),img=null,tool='rect',selected=null,drawing=null,poly=[],zoom=1,pan={x:0,y:0},pointers=new Map(),gesture=null,pinchIds=new Set(),undo=[],redo=[],db=null,editId=null,chosenColor=colors[0],saveTimer,selection=[],lastZoneTool='rect',lastLayoutTool='wall',lastObjectTool='door',lastDetailTool='pinNote',roomStamp='Office',symbolStamp='smoke',pendingPhotoPin=null;",
        'stamp state')
    s = rep(
        s,
        "const floorKeys=['zones','shapes','notes','walls','doors','windows','shutters','stairs','labels','pictureOpacity','pictureVisible','isBlank','gridVisible','wallWidth','image'];",
        "const floorKeys=['zones','shapes','notes','walls','doors','windows','shutters','stairs','labels','symbols','pins','pictureOpacity','pictureVisible','isBlank','gridVisible','wallWidth','image'];",
        'floor-local new data')

    old_render_floors = "function renderFloors(){ensureFloors();const select=$('floorSelect');select.textContent='';for(const f of state.floors){const o=document.createElement('option');o.value=f.id;o.textContent=f.name;select.append(o)}select.value=state.activeFloor;$('deleteFloor').disabled=state.floors.length<2}"
    new_render_floors = "function renderFloors(){ensureFloors();const select=$('floorSelect'),list=$('floorMenuList');select.textContent='';if(list)list.textContent='';for(const f of state.floors){const o=document.createElement('option');o.value=f.id;o.textContent=f.name;select.append(o);if(list){const b=document.createElement('button');b.className='floorChoice'+(f.id===state.activeFloor?' active':'');const name=document.createElement('span');name.textContent=f.name;const mark=document.createElement('span');mark.textContent=f.id===state.activeFloor?'✓':'';b.append(name,mark);b.onclick=async()=>{closeToolMenus();if(f.id===state.activeFloor)return;push();await showFloor(f.id)};list.append(b)}}select.value=state.activeFloor;$('floorMenuBtn').textContent='Floor · '+activeFloor().name;$('deleteFloor').disabled=state.floors.length<2}"
    s = rep(s, old_render_floors, new_render_floors, 'floor popup rendering')

    # Make floor copying explicitly leave site-detail pins and fire symbols floor-specific.
    s = rep(
        s,
        "for(const k of ['walls','doors','windows','shutters','stairs','labels','wallWidth'])data[k]=source[k]",
        "for(const k of ['walls','doors','windows','shutters','stairs','labels','wallWidth'])data[k]=source[k]",
        'floor copy remains layout only')

    s = rep(
        s,
        "function ensureIds(){for(const key of ['walls','doors','windows','shutters','stairs','labels','notes','shapes'])for(const o of state[key]||[])if(!o.id)o.id=uid()}",
        "function ensureIds(){for(const key of ['walls','doors','windows','shutters','stairs','labels','symbols','pins','notes','shapes'])for(const o of state[key]||[])if(!o.id)o.id=uid()}",
        'ids for new objects')

    old_load = "state={...fresh(),...req.result,doors:req.result.doors||[],windows:req.result.windows||[],shutters:req.result.shutters||[],stairs:req.result.stairs||[],labels:req.result.labels||[]};"
    new_load = "state={...fresh(),...req.result,doors:req.result.doors||[],windows:req.result.windows||[],shutters:req.result.shutters||[],stairs:req.result.stairs||[],labels:req.result.labels||[],symbols:req.result.symbols||[],pins:req.result.pins||[]};"
    s = rep(s, old_load, new_load, 'load compatibility')

    # Pure drawing helpers for stamps and pinned details.
    draw_helpers = r"""
const symbolNames={panel:'Panel',mcp:'MCP',smoke:'Smoke',heat:'Heat',sounder:'Sounder',you:'You are here'};
function drawSymbol(c,p,type,size,color='#172333'){const r=Math.max(5,size),label={panel:'FAP',mcp:'MCP',smoke:'SD',heat:'HD',sounder:'S',you:'YOU'}[type]||'?';c.save();c.strokeStyle=color;c.fillStyle='#fff';c.lineWidth=Math.max(.8,r*.09);c.textAlign='center';c.textBaseline='middle';if(type==='panel'||type==='mcp'){const w=r*2.15,h=r*1.55;c.fillRect(p.x-w/2,p.y-h/2,w,h);c.strokeRect(p.x-w/2,p.y-h/2,w,h)}else if(type==='you'){c.beginPath();c.moveTo(p.x,p.y-r*1.1);c.lineTo(p.x+r*.78,p.y+r*.45);c.lineTo(p.x,p.y+r*.12);c.lineTo(p.x-r*.78,p.y+r*.45);c.closePath();c.fill();c.stroke()}else{c.beginPath();c.arc(p.x,p.y,r,0,Math.PI*2);c.fill();c.stroke()}c.fillStyle=color;c.font=`700 ${Math.max(5,r*.55)}px system-ui`;c.fillText(label,p.x,p.y+(type==='you'?r*.7:0));c.restore()}
function drawPin(c,p,index,size){const r=Math.max(7,size),photo=p.kind==='photo',label=(photo?'P':'N')+(index+1);c.save();c.fillStyle=photo?'#7b4fa3':'#1d6fa5';c.strokeStyle='#fff';c.lineWidth=Math.max(1.5,r*.15);c.beginPath();c.arc(p.x,p.y,r,0,Math.PI*2);c.fill();c.stroke();c.fillStyle='#fff';c.font=`700 ${Math.max(7,r*.72)}px system-ui`;c.textAlign='center';c.textBaseline='middle';c.fillText(label,p.x,p.y);c.restore()}
function loadDataImage(src){return new Promise((resolve,reject)=>{if(!src){resolve(null);return}const i=new Image();i.onload=()=>resolve(i);i.onerror=reject;i.src=src})}
"""
    s = rep(s, "function syncGrid(){", draw_helpers + "\nfunction syncGrid(){", 'symbol and pin drawing helpers')

    old_sets = "const zoneTools=new Set(['rect','poly','fill']),layoutTools=new Set(['wall','pen','layoutRect','layoutPoly','label']),objectTools=new Set(['door','window','shutter','stairs']),wallObjectTools=new Set(['door','window','shutter']);"
    new_sets = "const zoneTools=new Set(['rect','poly','fill']),layoutTools=new Set(['wall','pen','layoutRect','layoutPoly','label','quickLabel']),objectTools=new Set(['door','window','shutter','stairs']),symbolTools=new Set(['symbol']),detailTools=new Set(['pinNote','pinPhoto']),wallObjectTools=new Set(['door','window','shutter']);"
    s = rep(s, old_sets, new_sets, 'new tool groups')
    s = rep(
        s,
        "function toolLabel(t){return({rect:'Box',poly:'Outline',fill:'Fill area',wall:'Wall',pen:'Pen',door:'Door',window:'Window',shutter:'Roller shutter',stairs:'Stairway',layoutRect:'Box',layoutPoly:'Outline',label:'Room label'})[t]||t}",
        "function toolLabel(t){if(t==='quickLabel')return 'Room · '+roomStamp;return({rect:'Box',poly:'Outline',fill:'Fill area',wall:'Wall',pen:'Pen',door:'Door',window:'Window',shutter:'Roller shutter',stairs:'Stairway',layoutRect:'Box',layoutPoly:'Outline',label:'Room label',pinNote:'Pinned note',pinPhoto:'Pinned photo'})[t]||t}",
        'tool labels')
    s = rep(
        s,
        "function placeMenu(panel,button){closeToolMenus();panel.classList.add('open');const r=button.getBoundingClientRect(),w=panel.offsetWidth,left=Math.max(8,Math.min(innerWidth-w-8,r.left));panel.style.left=left+'px';panel.style.bottom=Math.max(8,innerHeight-r.top+8)+'px'}",
        "function placeMenu(panel,button){closeToolMenus();panel.classList.add('open');const r=button.getBoundingClientRect(),w=panel.offsetWidth,left=Math.max(8,Math.min(innerWidth-w-8,r.left));panel.style.left=left+'px';panel.style.top='';panel.style.bottom=Math.max(8,innerHeight-r.top+8)+'px'}function placeMenuBelow(panel,button){closeToolMenus();panel.classList.add('open');const r=button.getBoundingClientRect(),w=panel.offsetWidth,left=Math.max(8,Math.min(innerWidth-w-8,r.left)),top=Math.max(8,Math.min(innerHeight-panel.offsetHeight-8,r.bottom+8));panel.style.left=left+'px';panel.style.bottom='';panel.style.top=top+'px'}",
        'top dropdown placement')

    old_sync_tools = "function syncToolMenus(){const z=state.zones.find(z=>z.id===selected);$('zoneMenuBtn').textContent=z?'Zone '+z.number+' · '+toolLabel(lastZoneTool):'Zone · Create/select';$('layoutMenuBtn').textContent='Building · '+toolLabel(lastLayoutTool);$('objectMenuBtn').textContent='Objects · '+toolLabel(lastObjectTool);$('zoneMenuBtn').classList.toggle('active',zoneTools.has(tool));$('layoutMenuBtn').classList.toggle('active',layoutTools.has(tool));$('objectMenuBtn').classList.toggle('active',objectTools.has(tool));document.querySelectorAll('[data-menu-tool]').forEach(b=>b.classList.toggle('active',b.dataset.menuTool===tool))}"
    new_sync_tools = "function syncToolMenus(){const z=state.zones.find(z=>z.id===selected);$('zoneMenuBtn').textContent=z?'Zone '+z.number+' · '+toolLabel(lastZoneTool):'Zone · Create/select';$('layoutMenuBtn').textContent='Building · '+toolLabel(lastLayoutTool);$('objectMenuBtn').textContent='Objects · '+toolLabel(lastObjectTool);$('symbolMenuBtn').textContent='Symbols · '+symbolNames[symbolStamp];$('detailMenuBtn').textContent=detailTools.has(tool)?'Site details · '+toolLabel(lastDetailTool):'Site details';$('zoneMenuBtn').classList.toggle('active',zoneTools.has(tool));$('layoutMenuBtn').classList.toggle('active',layoutTools.has(tool));$('objectMenuBtn').classList.toggle('active',objectTools.has(tool));$('symbolMenuBtn').classList.toggle('active',tool==='symbol');$('detailMenuBtn').classList.toggle('active',detailTools.has(tool));document.querySelectorAll('[data-menu-tool]').forEach(b=>b.classList.toggle('active',b.dataset.menuTool===tool));document.querySelectorAll('[data-symbol]').forEach(b=>b.classList.toggle('active',tool==='symbol'&&b.dataset.symbol===symbolStamp));document.querySelectorAll('[data-detail-tool]').forEach(b=>b.classList.toggle('active',b.dataset.detailTool===tool))}"
    s = rep(s, old_sync_tools, new_sync_tools, 'sync all grouped menus')

    old_set_tool = "function setTool(t){tool=t;drawing=null;poly=[];if(t!=='group'&&t!=='select')clearSelection();if(zoneTools.has(t))lastZoneTool=t;if(layoutTools.has(t))lastLayoutTool=t;if(objectTools.has(t))lastObjectTool=t;document.querySelectorAll('[data-tool]').forEach(b=>b.classList.toggle('active',b.dataset.tool===t));document.querySelectorAll('[data-menu-tool]').forEach(b=>b.classList.toggle('active',b.dataset.menuTool===t));$('finish').hidden=!(t==='poly'||t==='layoutPoly');syncToolMenus();closeToolMenus();hint();draw()}"
    new_set_tool = "function setTool(t){tool=t;drawing=null;poly=[];if(t!=='group'&&t!=='select')clearSelection();if(zoneTools.has(t))lastZoneTool=t;if(layoutTools.has(t))lastLayoutTool=t;if(objectTools.has(t))lastObjectTool=t;if(detailTools.has(t))lastDetailTool=t;document.querySelectorAll('[data-tool]').forEach(b=>b.classList.toggle('active',b.dataset.tool===t));document.querySelectorAll('[data-menu-tool]').forEach(b=>b.classList.toggle('active',b.dataset.menuTool===t));$('finish').hidden=!(t==='poly'||t==='layoutPoly');syncToolMenus();closeToolMenus();hint();draw()}"
    s = rep(s, old_set_tool, new_set_tool, 'set new tools')

    old_hint_fragment = "label:'Tap a room and type its name',rect:'Drag a box over the selected zone area'"
    new_hint_fragment = "label:'Tap a room and type its name',quickLabel:'Tap rooms to repeatedly place “'+roomStamp+'”',symbol:'Tap repeatedly to stamp '+symbolNames[symbolStamp]+' symbols',pinNote:'Tap the exact point for a pinned office note',pinPhoto:'Tap the exact point, then choose a site photo',rect:'Drag a box over the selected zone area'"
    s = rep(s, old_hint_fragment, new_hint_fragment, 'new tool hints')

    # Object model support for selection/grouping/movement.
    s = rep(
        s,
        "for(const type of ['walls','doors','windows','shutters','stairs','labels','notes','shapes'])",
        "for(const type of ['walls','doors','windows','shutters','stairs','labels','symbols','pins','notes','shapes'])",
        'all refs new types')
    s = rep(
        s,
        "if(['doors','windows','shutters','stairs'].includes(ref.type))return[o.a,o.b];return[{x:o.x,y:o.y}]",
        "if(['doors','windows','shutters','stairs'].includes(ref.type))return[o.a,o.b];return[{x:o.x,y:o.y}]",
        'point objects naturally supported')
    s = s.replace("if(ref.type==='labels'||ref.type==='notes'){", "if(['labels','notes','symbols','pins'].includes(ref.type)){")

    # Selection transforms: duplicate, rotate and mirror.
    selection_helpers = r"""
function mapObjectPoints(type,o,fn){if(type==='walls'||type==='shapes')o.points=(o.points||[]).map(fn);else if(['doors','windows','shutters','stairs'].includes(type)){o.a=fn(o.a);o.b=fn(o.b)}else{const p=fn({x:o.x,y:o.y});o.x=p.x;o.y=p.y}}
function duplicateSelection(){if(!selection.length||!img)return;push();const v=transform(),dx=24/(img.width*v.s),dy=24/(img.height*v.s),groupMap=new Map(),common=selection.length>1?uid():null,newRefs=[];for(const r of selection){const src=getObj(r);if(!src)continue;const copy=JSON.parse(JSON.stringify(src));copy.id=uid();if(src.group){if(!groupMap.has(src.group))groupMap.set(src.group,uid());copy.group=groupMap.get(src.group)}else if(common)copy.group=common;mapObjectPoints(r.type,copy,p=>({x:clamp(p.x+dx),y:clamp(p.y+dy)}));state[r.type].push(copy);newRefs.push({type:r.type,id:copy.id})}selection=newRefs;changed();setHint('Duplicate created · drag it with Select / Move');setTimeout(hint,1000)}
function transformSelection(mode){if(!selection.length||!img)return;const b=selectionBounds();if(!b)return;const cx=(b.x1+b.x2)/2,cy=(b.y1+b.y2)/2;push();for(const r of selection){const o=getObj(r);if(!o)continue;const fn=p=>{let X=(p.x-cx)*img.width,Y=(p.y-cy)*img.height,nx=X,ny=Y;if(mode==='rotate'){nx=-Y;ny=X}else if(mode==='mirror')nx=-X;return{x:clamp(cx+nx/img.width),y:clamp(cy+ny/img.height)}};mapObjectPoints(r.type,o,fn);if(mode==='mirror'&&r.type==='doors')o.side=-(o.side||1)}changed();setHint(mode==='rotate'?'Selection rotated 90°':'Selection mirrored');setTimeout(hint,900)}
$('duplicateSelected').onclick=duplicateSelection;$('rotateSelected').onclick=()=>transformSelection('rotate');$('mirrorSelected').onclick=()=>transformSelection('mirror');
"""
    s = rep(s, "function snapshotSelection(){", selection_helpers + "\nfunction snapshotSelection(){", 'selection transforms')

    # Draw symbols and pin markers in plan-space so they stay anchored while zooming.
    old_label_draw = "for(const l of state.labels){const p=map(l),fs=Math.min(img.width,img.height)*.022*v.s;roomLabel(ctx,p.x,p.y,l.text,fs)}"
    new_label_draw = "const stampSize=Math.min(img.width,img.height)*.018*v.s;for(const sm of state.symbols||[]){const p=map(sm);drawSymbol(ctx,p,sm.type,stampSize)}for(let i=0;i<(state.pins||[]).length;i++){const pin=state.pins[i],p=map(pin);drawPin(ctx,p,i,stampSize*.72)}for(const l of state.labels){const p=map(l),fs=Math.min(img.width,img.height)*.022*v.s;roomLabel(ctx,p.x,p.y,l.text,fs)}"
    s = rep(s, old_label_draw, new_label_draw, 'draw stamps and pins')

    # Extend menu wiring and make the floor selector use the same popup language as the other menus.
    old_menu_handlers = "$('zoneMenuBtn').onclick=()=>toggleMenu($('zoneMenu'),$('zoneMenuBtn'));$('layoutMenuBtn').onclick=()=>toggleMenu($('layoutMenu'),$('layoutMenuBtn'));$('objectMenuBtn').onclick=()=>toggleMenu($('objectMenu'),$('objectMenuBtn'));$('zoneCreate').onclick=()=>{closeToolMenus();openModal()};"
    new_menu_handlers = "$('zoneMenuBtn').onclick=()=>toggleMenu($('zoneMenu'),$('zoneMenuBtn'));$('layoutMenuBtn').onclick=()=>toggleMenu($('layoutMenu'),$('layoutMenuBtn'));$('objectMenuBtn').onclick=()=>toggleMenu($('objectMenu'),$('objectMenuBtn'));$('symbolMenuBtn').onclick=()=>toggleMenu($('symbolMenu'),$('symbolMenuBtn'));$('detailMenuBtn').onclick=()=>toggleMenu($('detailMenu'),$('detailMenuBtn'));$('floorMenuBtn').onclick=()=>{if($('floorMenu').classList.contains('open'))closeToolMenus();else placeMenuBelow($('floorMenu'),$('floorMenuBtn'))};$('zoneCreate').onclick=()=>{closeToolMenus();openModal()};document.querySelectorAll('[data-room-name]').forEach(b=>b.onclick=()=>{let name=b.dataset.roomName;if(name==='Custom')name=prompt('Room name:')?.trim();if(!name)return;roomStamp=name.slice(0,35);setTool('quickLabel')});document.querySelectorAll('[data-symbol]').forEach(b=>b.onclick=()=>{symbolStamp=b.dataset.symbol;setTool('symbol')});document.querySelectorAll('[data-detail-tool]').forEach(b=>b.onclick=()=>setTool(b.dataset.detailTool));"
    s = rep(s, old_menu_handlers, new_menu_handlers, 'menu handlers')

    old_doc_close = "document.addEventListener('pointerdown',e=>{if(!e.target.closest('.toolPopup')&&!e.target.closest('#zoneMenuBtn')&&!e.target.closest('#layoutMenuBtn')&&!e.target.closest('#objectMenuBtn'))closeToolMenus()},true);"
    new_doc_close = "document.addEventListener('pointerdown',e=>{if(!e.target.closest('.toolPopup')&&!e.target.closest('#zoneMenuBtn')&&!e.target.closest('#layoutMenuBtn')&&!e.target.closest('#objectMenuBtn')&&!e.target.closest('#symbolMenuBtn')&&!e.target.closest('#detailMenuBtn')&&!e.target.closest('#floorMenuBtn'))closeToolMenus()},true);"
    s = rep(s, old_doc_close, new_doc_close, 'close dropdowns safely')

    # Stamp tools are intentionally repeat-on-tap and remain selected until another tool is chosen.
    old_label_up = "else if(tool==='label'){const value=prompt('Room name (e.g. Office, Store, Corridor):');if(value?.trim()){push();state.labels.push({id:uid(),...point(e.clientX,e.clientY),text:value.trim().slice(0,35)});changed()}}"
    new_label_up = "else if(tool==='quickLabel'){push();state.labels.push({id:uid(),...point(e.clientX,e.clientY),text:roomStamp,group:null});changed()}\nelse if(tool==='symbol'){push();state.symbols.push({id:uid(),...point(e.clientX,e.clientY),type:symbolStamp,group:null});changed()}\nelse if(tool==='pinNote'){const value=prompt('Pinned note for the office:');if(value?.trim()){push();state.pins.push({id:uid(),...point(e.clientX,e.clientY),kind:'note',text:value.trim().slice(0,80),group:null});changed()}}\nelse if(tool==='pinPhoto'){pendingPhotoPin=point(e.clientX,e.clientY);$('pinPhotoFile').click()}\n" + old_label_up
    s = rep(s, old_label_up, new_label_up, 'tap repeat and pin tools')

    # Pinned photo reader: downscale aggressively so offline drafts remain practical.
    photo_handler = r"""
$('pinPhotoFile').onchange=async e=>{const f=e.target.files?.[0];e.target.value='';const at=pendingPhotoPin;pendingPhotoPin=null;if(!f||!at)return;if(!f.type.startsWith('image/')){alert('Choose a photo or image.');return}try{const raw=await new Promise((ok,no)=>{const r=new FileReader();r.onload=()=>ok(r.result);r.onerror=no;r.readAsDataURL(f)}),source=await loadDataImage(raw),max=720,scale=Math.min(1,max/Math.max(source.width,source.height)),c=document.createElement('canvas');c.width=Math.max(1,Math.round(source.width*scale));c.height=Math.max(1,Math.round(source.height*scale));c.getContext('2d').drawImage(source,0,0,c.width,c.height);const fallback=f.name.replace(/\.[^.]+$/,'').slice(0,60),caption=(prompt('Photo note for the office:',fallback)||fallback).trim().slice(0,80);push();state.pins.push({id:uid(),...at,kind:'photo',text:caption||'Site photo',image:c.toDataURL('image/jpeg',.7),group:null});changed();setHint('Photo pinned to the plan');setTimeout(hint,900)}catch(err){alert('Could not add that photo. Try a JPG or PNG.')}};
"""
    s = rep(s, "canvas.onpointercancel=e=>", photo_handler + "\ncanvas.onpointercancel=e=>", 'photo pin handling')

    # Clear new floor-local content when replacing an imported plan.
    s = rep(
        s,
        "state.stairs=[];state.labels=[];selection=[];",
        "state.stairs=[];state.labels=[];state.symbols=[];state.pins=[];selection=[];",
        'clear new floor content on import')

    old_restore = "state={...fresh(),...next,doors:next.doors||[],windows:next.windows||[],shutters:next.shutters||[],stairs:next.stairs||[],labels:next.labels||[]};"
    new_restore = "state={...fresh(),...next,doors:next.doors||[],windows:next.windows||[],shutters:next.shutters||[],stairs:next.stairs||[],labels:next.labels||[],symbols:next.symbols||[],pins:next.pins||[]};"
    s = rep(s, old_restore, new_restore, 'undo restore compatibility')

    # Replace exporter with an async floor renderer, pinned-photo details and whole-building pack.
    start = s.index("function exportCanvas(){")
    end = s.index("renderFloors();new ResizeObserver", start)
    exporter = r"""
function floorView(f){return{...fresh(),...(f?.data||{}),doors:f?.data?.doors||[],windows:f?.data?.windows||[],shutters:f?.data?.shutters||[],stairs:f?.data?.stairs||[],labels:f?.data?.labels||[],symbols:f?.data?.symbols||[],pins:f?.data?.pins||[]}}
async function renderFloorCanvas(f,maxPlan=4500){const d=floorView(f),floorImg=await loadDataImage(d.image).catch(()=>null),cw=floorImg?.width||3200,ch=floorImg?.height||2000,pad=50,scale=Math.min(1,maxPlan/Math.max(cw,ch)),W=Math.round(cw*scale),H=Math.round(ch*scale),pinExtra=(d.pins?.length?42:0)+(d.pins||[]).reduce((n,p)=>n+(p.kind==='photo'?128:38),0),legendH=140+d.zones.length*40+Math.min(d.notes.length,10)*28+pinExtra,c=document.createElement('canvas');c.width=W+2*pad;c.height=H+legendH+pad;const x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);x.fillStyle='#18283d';x.fillRect(0,0,c.width,72);x.fillStyle='#fff';x.font='bold 26px system-ui';x.fillText(((state.site||'Untitled site')+' — '+f.name).slice(0,95),pad,33);x.font='14px system-ui';x.fillText('ZONE LAYOUT — SITE DRAFT FOR CAD · '+new Date().toLocaleDateString('en-GB'),pad,57);if(floorImg&&!d.isBlank&&d.pictureVisible){x.save();x.globalAlpha=d.pictureOpacity??1;x.drawImage(floorImg,pad,85,W,H);x.restore()}const map=p=>({x:pad+p.x*W,y:85+p.y*H});for(const sh of d.shapes){const z=d.zones.find(z=>z.id===sh.zone);if(z&&sh.points.length>2)shape(x,sh.points.map(map),z.color,z.number,Math.max(1.4,W/1800),true)}for(const wall of d.walls)stroke(x,wall.points.map(map),Math.max(.75,(d.wallWidth||3)*W/1600));for(const door of d.doors)drawDoor(x,map(door.a),map(door.b),Math.max(.75,(d.wallWidth||3)*.85*W/1600),door.side||1);for(const win of d.windows)drawWindow(x,map(win.a),map(win.b),Math.max(.75,(d.wallWidth||3)*W/1600));for(const sh of d.shutters)drawShutter(x,map(sh.a),map(sh.b),Math.max(.75,(d.wallWidth||3)*W/1600));for(const st of d.stairs)drawStairs(x,map(st.a),map(st.b),Math.max(.75,(d.wallWidth||3)*W/1600));const stampSize=Math.min(W,H)*.018;for(const sm of d.symbols){drawSymbol(x,map(sm),sm.type,stampSize)}for(let i=0;i<d.pins.length;i++)drawPin(x,map(d.pins[i]),i,stampSize*.72);for(const l of d.labels){const p=map(l);roomLabel(x,p.x,p.y,l.text,Math.max(11,W/120))}for(const n of d.notes){const p=map(n);badge(x,p.x,p.y,n.text,'#1b344e')}const start=H+111;x.fillStyle='#18283d';x.font='bold 20px system-ui';x.fillText('ZONE KEY',pad,start);x.font='16px system-ui';d.zones.forEach((z,i)=>{x.fillStyle=z.color;x.fillRect(pad,start+18+i*40,18,18);x.fillStyle='#18283d';x.fillText('Zone '+z.number+' — '+(z.name||'Description to confirm'),pad+30,start+34+i*40)});let ny=start+20+d.zones.length*40;if(d.notes.length){x.fillStyle='#18283d';x.font='bold 16px system-ui';x.fillText('SITE NOTES',pad,ny+13);ny+=25;x.font='14px system-ui';for(const n of d.notes.slice(0,10)){x.fillText('• '+n.text,pad,ny+14);ny+=28}}if(d.pins.length){x.fillStyle='#18283d';x.font='bold 16px system-ui';x.fillText('PINNED SITE DETAILS',pad,ny+16);ny+=30;for(let i=0;i<d.pins.length;i++){const p=d.pins[i],tag=(p.kind==='photo'?'P':'N')+(i+1);x.fillStyle=p.kind==='photo'?'#7b4fa3':'#1d6fa5';x.fillRect(pad,ny+4,30,24);x.fillStyle='#fff';x.font='bold 12px system-ui';x.fillText(tag,pad+6,ny+20);x.fillStyle='#18283d';x.font='14px system-ui';if(p.kind==='photo'&&p.image){const pi=await loadDataImage(p.image).catch(()=>null);if(pi){const tw=120,th=90,sc=Math.min(tw/pi.width,th/pi.height),dw=pi.width*sc,dh=pi.height*sc;x.drawImage(pi,pad+42,ny,dw,dh);x.fillText(p.text||'Site photo',pad+175,ny+22);ny+=128;continue}}x.fillText(p.text||'Pinned note',pad+42,ny+20);ny+=38}}x.fillStyle='#728092';x.font='13px system-ui';x.fillText('Draft for office verification and CAD redraw · Check all zones against the site and current fire strategy.',pad,c.height-25);return c}
async function exportCanvas(){syncFloor();return renderFloorCanvas(activeFloor(),4500)}
async function exportAllFloorsCanvas(){syncFloor();const floors=state.floors.slice(),maxPlan=Math.max(900,Math.min(1800,Math.floor(8500/Math.max(1,floors.length)))),pages=[];for(const f of floors)pages.push(await renderFloorCanvas(f,maxPlan));const indexRows=floors.reduce((n,f)=>n+1+(f.data?.zones?.length||0),0),indexH=90+indexRows*30,W=Math.max(1000,...pages.map(p=>p.width)),H=90+pages.reduce((n,p)=>n+p.height+28,0)+indexH,c=document.createElement('canvas');c.width=W;c.height=H;const x=c.getContext('2d');x.fillStyle='#e8edf3';x.fillRect(0,0,W,H);x.fillStyle='#16283e';x.fillRect(0,0,W,72);x.fillStyle='#fff';x.font='bold 28px system-ui';x.fillText((state.site||'Untitled site')+' — ALL FLOORS',40,31);x.font='14px system-ui';x.fillText('ZONE SKETCH BUILDING PACK · '+new Date().toLocaleDateString('en-GB'),40,55);let y=90;for(let i=0;i<pages.length;i++){const p=pages[i],px=Math.round((W-p.width)/2);x.drawImage(p,px,y);y+=p.height+28}x.fillStyle='#fff';x.fillRect(20,y-4,W-40,indexH-20);x.fillStyle='#18283d';x.font='bold 22px system-ui';x.fillText('BUILDING ZONE INDEX',40,y+26);y+=46;for(const f of floors){x.font='bold 16px system-ui';x.fillStyle='#18283d';x.fillText(f.name,40,y);y+=24;const zones=f.data?.zones||[];if(!zones.length){x.font='13px system-ui';x.fillStyle='#728092';x.fillText('No zones added',58,y);y+=28;continue}for(const z of zones){x.fillStyle=z.color;x.fillRect(58,y-13,15,15);x.fillStyle='#18283d';x.font='14px system-ui';x.fillText('Zone '+z.number+' — '+(z.name||'Description to confirm'),82,y);y+=28}}return c}
async function shareCanvas(c,name,title,text){if(window.AndroidBridge){window.AndroidBridge.sharePng(c.toDataURL('image/png'),name);return}const blob=await new Promise(ok=>c.toBlob(ok,'image/png'));if(!blob){alert('Could not export this image.');return}const file=new File([blob],name,{type:'image/png'});try{if(navigator.canShare?.({files:[file]})){await navigator.share({files:[file],title,text});return}}catch(e){if(e.name==='AbortError')return}const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=file.name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),60000);alert('PNG saved. Attach it to your email or office job notes.')}
$('shareBtn').onclick=async()=>{if(!img){alert('Import a plan or start a blank canvas first.');return}if(!state.shapes.length&&!state.walls.length&&!state.doors.length&&!state.windows.length&&!state.shutters.length&&!state.stairs.length&&!state.labels.length&&!state.symbols.length&&!state.pins.length&&!state.notes.length&&!confirm('Nothing has been drawn. Send the plan anyway?'))return;const c=await exportCanvas(),safe=(state.site||'site').replace(/[^a-z0-9 -]/gi,'').trim().replace(/\s+/g,'-').slice(0,45)||'site',name=safe+'-'+activeFloor().name.replace(/[^a-z0-9 -]/gi,'').trim().replace(/\s+/g,'-')+'-zone-draft.png';await shareCanvas(c,name,(state.site||'Site')+' '+activeFloor().name+' zone layout','Site zone layout draft for office CAD redraw. Please verify zones against the site.')};
$('exportAllFloors').onclick=async()=>{closeToolMenus();if(!state.floors?.length)return;setHint('Building all-floor export…');const c=await exportAllFloorsCanvas(),safe=(state.site||'site').replace(/[^a-z0-9 -]/gi,'').trim().replace(/\s+/g,'-').slice(0,45)||'site';setHint('');await shareCanvas(c,safe+'-all-floors-zone-pack.png',(state.site||'Site')+' all floors','All-floor Zone Sketch building pack with floor plans and zone index.')};
"""
    s = s[:start] + exporter + s[end:]

    readme_note = 'Zone Sketch v0.11 productivity tools'
    return s


for path in FILES:
    original = path.read_text(encoding='utf-8')
    updated = upgrade(original)
    path.write_text(updated, encoding='utf-8')
    print(f'updated {path}: {len(original)} -> {len(updated)} bytes')

readme = Path('README.md')
r = readme.read_text(encoding='utf-8')
section = """

## Version 0.11 — faster onsite workflow

- Floor selection now uses the same compact dropdown/popover style as Zone, Building, Objects and Symbols instead of a native floor select popup.
- Symbol favourites: Panel, MCP, Smoke, Heat, Sounder and You are here. Symbols are tap-to-repeat until another tool is selected.
- Quick room-name stamps for Office, Store, Corridor, WC, Plant room and custom names.
- Box-selected rooms/objects can be duplicated, rotated 90 degrees or mirrored; duplicates are kept together for immediate moving.
- Pinned notes and compressed pinned site photos stay at exact plan positions and are listed (with photo thumbnails) in office exports.
- Send all floors creates one combined building-pack PNG containing every floor plus a building-wide zone index.
- New objects remain floor-local, autosaved, undoable, groupable, selectable and movable.
"""
if '## Version 0.11 — faster onsite workflow' not in r:
    readme.write_text(r.rstrip() + section + '\n', encoding='utf-8')
    print('updated README.md')
