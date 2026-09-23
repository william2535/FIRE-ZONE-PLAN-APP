from pathlib import Path

ROOT = Path('index.html')
s = ROOT.read_text()

def rep(old, new, label=None):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f"Expected exactly one {label or old[:50]!r}, found {count}")
    s = s.replace(old, new, 1)

def rep_first(old, new, label=None):
    global s
    if old not in s:
        raise SystemExit(f"Missing {label or old[:50]!r}")
    s = s.replace(old, new, 1)

# ---------- CSS ----------
rep(
    ".menuTool.active{background:#1c344f!important;color:#fff}[hidden]{display:none!important}",
    ".menuTool.active{background:#1c344f!important;color:#fff}.toolPopup .toggleItem{display:flex;width:100%;justify-content:space-between;align-items:center;margin-bottom:6px}.toolPopup .toggleItem.active{background:#1c344f;color:#fff}.toolPopup .countGrid{display:grid;grid-template-columns:1fr auto;gap:6px 14px;font-size:13px;padding:3px 5px}.toolPopup .countGrid strong{font-weight:800}.toolPopup .countSub{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#6b7b8d;margin:8px 5px 5px}.propertyReadout{font-size:12px;color:#627185;background:#eef3f8;padding:8px 10px;border-radius:9px}.box select{width:100%;border:1px solid #bfcbd7;border-radius:9px;padding:10px;background:#fff}.box input[type=color]{height:42px;padding:4px}.box input[type=range]{padding:0}.moveModeActive .canvasWrap{cursor:grab}.moveModeActive .canvasWrap:active{cursor:grabbing}[hidden]{display:none!important}",
    "precision CSS marker"
)

# ---------- Header controls ----------
rep(
    '<button id="zonesPanelBtn" title="Show or hide the Zones panel">Zones ◀</button><button id="gridBtn">Grid off</button>',
    '<button id="zonesPanelBtn" title="Show or hide the Zones panel">Zones ◀</button><button id="moveModeTop" title="When on, the canvas only pans/zooms and cannot edit">Move OFF</button><button id="locksMenuBtn">Locks</button><button id="layersMenuBtn">Layers</button><button id="countsMenuBtn">Devices · 0</button><button id="gridBtn">Grid off</button>',
    "top controls"
)

# Selection properties button.
rep(
    '<button id="mirrorSelected">Mirror ↔</button><button id="clearSelection">Clear selection</button>',
    '<button id="mirrorSelected">Mirror ↔</button><button id="propertiesSelected">Properties</button><button id="clearSelection">Clear selection</button>',
    "selection properties button"
)

# Replace old bottom pan tool with the same global mode toggle.
rep(
    '<button data-tool="pan">✋ Move plan</button>',
    '<button id="moveModeBottom">✋ Move mode</button>',
    "bottom move-plan button"
)

# Add Trim / Extend to Building layout.
rep(
    '<button data-menu-tool="layoutPoly">⬡ Outline</button><button data-menu-tool="label">Room label</button>',
    '<button data-menu-tool="layoutPoly">⬡ Outline</button><button data-menu-tool="label">Room label</button><button data-menu-tool="trim">Trim / Extend</button>',
    "trim extend building button"
)

# Add top dropdown menus after Site details popup.
rep(
    '<div id="detailMenu" class="toolPopup" aria-label="Pinned site details"><h4>Site details</h4><div class="menuRow"><button data-detail-tool="pinNote">Pinned note</button><button data-detail-tool="pinPhoto">Pinned photo</button></div><div class="menuHint">Pins stay exactly where you tap and are listed in the office export.</div></div>',
    '''<div id="detailMenu" class="toolPopup" aria-label="Pinned site details"><h4>Site details</h4><div class="menuRow"><button data-detail-tool="pinNote">Pinned note</button><button data-detail-tool="pinPhoto">Pinned photo</button></div><div class="menuHint">Pins stay exactly where you tap and are listed in the office export.</div></div>
<div id="locksMenu" class="toolPopup" aria-label="Drawing locks"><h4>Locks</h4><button class="toggleItem" data-lock="background" data-lock-label="Background"><span>Background</span><span>Unlocked</span></button><button class="toggleItem" data-lock="building" data-lock-label="Building"><span>Building</span><span>Unlocked</span></button><button class="toggleItem" data-lock="zones" data-lock-label="Zones"><span>Zones</span><span>Unlocked</span></button><div class="menuHint">Locked items cannot be changed, moved or deleted until unlocked.</div></div>
<div id="layersMenu" class="toolPopup" aria-label="Visible layers"><h4>Layers · view only</h4><button class="toggleItem" data-layer="background" data-layer-label="Background"><span>Background</span><span>Shown</span></button><button class="toggleItem" data-layer="building" data-layer-label="Building"><span>Building</span><span>Shown</span></button><button class="toggleItem" data-layer="zones" data-layer-label="Zones"><span>Zones</span><span>Shown</span></button><button class="toggleItem" data-layer="symbols" data-layer-label="Symbols"><span>Symbols</span><span>Shown</span></button><button class="toggleItem" data-layer="labels" data-layer-label="Labels"><span>Labels</span><span>Shown</span></button><button class="toggleItem" data-layer="notes" data-layer-label="Notes / Pins"><span>Notes / Pins</span><span>Shown</span></button><button class="toggleItem" data-layer="grid" data-layer-label="Grid"><span>Grid</span><span>Shown</span></button><div class="menuHint">Layer visibility is for working on the plan. Office exports still include the complete drawing.</div></div>
<div id="countsMenu" class="toolPopup" aria-label="Device counts"><h4>Device counts</h4><div class="countSub">Current floor</div><div id="floorDeviceCounts" class="countGrid"></div><div class="menuSep"></div><div class="countSub">Whole building</div><div id="buildingDeviceCounts" class="countGrid"></div></div>''',
    "precision dropdown menus"
)

# Object properties modal.
rep(
    '<button id="addZone" hidden></button>',
    '''<div class="modal" id="propertyModal"><div class="box"><h2>Object properties</h2><div id="propKind" class="propertyReadout"></div><label id="propTextWrap">Name / note<input id="propText" maxlength="80"></label><label id="propSymbolWrap">Symbol type<select id="propSymbolType"><option value="panel">Panel</option><option value="mcp">MCP</option><option value="smoke">Smoke</option><option value="heat">Heat</option><option value="sounder">Sounder</option><option value="you">You are here</option></select></label><label id="propColorWrap">Colour<input id="propColor" type="color" value="#172333"></label><label id="propScaleWrap">Size <output id="propScaleValue">1.00×</output><input id="propScale" type="range" min="0.25" max="4" step="0.05" value="1"></label><div class="row" style="justify-content:flex-start"><button id="propRotate">Rotate 90°</button><button id="propMirror">Mirror ↔</button></div><div class="row"><button id="propDelete">Delete</button><button id="propClose">Close</button><button id="propSave" class="primary">Save</button></div></div></div>
<button id="addZone" hidden></button>''',
    "properties modal"
)

# ---------- State ----------
rep(
    "const fresh=()=>({site:'',zones:[],shapes:[],notes:[],walls:[],doors:[],windows:[],shutters:[],stairs:[],labels:[],symbols:[],pins:[],pictureOpacity:1,pictureVisible:true,isBlank:false,gridVisible:false,snapGrid:false,gridSize:100,wallWidth:3});",
    "const fresh=()=>({site:'',zones:[],shapes:[],notes:[],walls:[],doors:[],windows:[],shutters:[],stairs:[],labels:[],symbols:[],pins:[],pictureOpacity:1,pictureVisible:true,isBlank:false,gridVisible:false,snapGrid:false,gridSize:100,wallWidth:3,locks:{background:false,building:false,zones:false},layers:{background:true,building:true,zones:true,symbols:true,labels:true,notes:true,grid:true}});",
    "fresh state"
)
rep(
    "let imageRequest=0,opacityEditing=false,state=fresh(),img=null,tool='rect',selected=null,drawing=null,poly=[],zoom=1,pan={x:0,y:0},pointers=new Map(),gesture=null,pinchIds=new Set(),undo=[],redo=[],db=null,editId=null,chosenColor=colors[0],saveTimer,selection=[],lastZoneTool='rect',lastLayoutTool='wall',lastObjectTool='door',lastDetailTool='pinNote',roomStamp='Office',symbolStamp='smoke',symbolColor='#172333',pendingPhotoPin=null;",
    "let imageRequest=0,opacityEditing=false,state=fresh(),img=null,tool='rect',selected=null,drawing=null,poly=[],zoom=1,pan={x:0,y:0},pointers=new Map(),gesture=null,pinchIds=new Set(),undo=[],redo=[],db=null,editId=null,chosenColor=colors[0],saveTimer,selection=[],lastZoneTool='rect',lastLayoutTool='wall',lastObjectTool='door',lastDetailTool='pinNote',roomStamp='Office',symbolStamp='smoke',symbolColor='#172333',pendingPhotoPin=null,navMode=false;",
    "nav mode variable"
)
rep(
    "const floorKeys=['zones','shapes','notes','walls','doors','windows','shutters','stairs','labels','symbols','pins','pictureOpacity','pictureVisible','isBlank','gridVisible','snapGrid','gridSize','wallWidth','image'];",
    "const floorKeys=['zones','shapes','notes','walls','doors','windows','shutters','stairs','labels','symbols','pins','pictureOpacity','pictureVisible','isBlank','gridVisible','snapGrid','gridSize','wallWidth','locks','layers','image'];",
    "floor keys"
)

# Deep migration helpers after uid/clamp.
rep(
    "const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));",
    "const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));\nconst defaultLocks=()=>({background:false,building:false,zones:false}),defaultLayers=()=>({background:true,building:true,zones:true,symbols:true,labels:true,notes:true,grid:true});\nfunction ensureUiState(){state.locks={...defaultLocks(),...(state.locks||{})};state.layers={...defaultLayers(),...(state.layers||{})}}",
    "UI state migration"
)
rep(
    "Object.assign(state,JSON.parse(JSON.stringify(f.data)));resetInteraction();",
    "Object.assign(state,JSON.parse(JSON.stringify(f.data)));ensureUiState();resetInteraction();",
    "floor UI state migration"
)
rep(
    "state={...fresh(),...req.result,doors:req.result.doors||[],windows:req.result.windows||[],shutters:req.result.shutters||[],stairs:req.result.stairs||[],labels:req.result.labels||[],symbols:req.result.symbols||[],pins:req.result.pins||[]};normalizeWalls();",
    "state={...fresh(),...req.result,doors:req.result.doors||[],windows:req.result.windows||[],shutters:req.result.shutters||[],stairs:req.result.stairs||[],labels:req.result.labels||[],symbols:req.result.symbols||[],pins:req.result.pins||[]};ensureUiState();normalizeWalls();",
    "load UI state migration"
)
rep(
    "state={...fresh(),...next,doors:next.doors||[],windows:next.windows||[],shutters:next.shutters||[],stairs:next.stairs||[],labels:next.labels||[],symbols:next.symbols||[],pins:next.pins||[]};normalizeWalls();",
    "state={...fresh(),...next,doors:next.doors||[],windows:next.windows||[],shutters:next.shutters||[],stairs:next.stairs||[],labels:next.labels||[],symbols:next.symbols||[],pins:next.pins||[]};ensureUiState();normalizeWalls();",
    "restore UI state migration"
)

# changed() refreshes precision panels.
rep(
    "function changed(){renderFloors();renderZones();syncSelectionBar();syncWallSize();draw();persist();updateButtons()}",
    "function changed(){renderFloors();renderZones();syncSelectionBar();syncWallSize();renderLockMenu();renderLayersMenu();renderDeviceCounts();draw();persist();updateButtons()}",
    "changed precision refresh"
)

# ---------- Background lock ----------
rep(
    "function picture(c,x,y,w,h){if(!state.isBlank&&state.pictureVisible){",
    "function picture(c,x,y,w,h){if(state.layers?.background!==false&&!state.isBlank&&state.pictureVisible){",
    "background layer visibility"
)
rep(
    "function syncBackground(){$('backgroundBar').hidden=!img||state.isBlank;$('opacity').value=Math.round(state.pictureOpacity*100);$('opacityValue').textContent=Math.round(state.pictureOpacity*100)+'%';$('opacity').disabled=!state.pictureVisible;$('togglePicture').textContent=state.pictureVisible?'Hide picture':'Show picture';$('backgroundHelp').textContent=state.pictureVisible?'Opacity also applies to the exported PNG.':'Picture excluded from export. Your drawing stays in place.'}",
    "function syncBackground(){const locked=!!state.locks?.background;$('backgroundBar').hidden=!img||state.isBlank;$('opacity').value=Math.round(state.pictureOpacity*100);$('opacityValue').textContent=Math.round(state.pictureOpacity*100)+'%';$('opacity').disabled=!state.pictureVisible||locked;$('togglePicture').disabled=locked;$('importBtn').disabled=locked&&!!img;$('togglePicture').textContent=state.pictureVisible?'Hide picture':'Show picture';$('backgroundHelp').textContent=locked?'Background locked · unlock it from Locks to replace, hide or fade it.':(state.pictureVisible?'Opacity also applies to the exported PNG.':'Picture excluded from export. Your drawing stays in place.')}",
    "locked background controls"
)
rep(
    "function pick(){$('file').click()}",
    "function pick(){if(state.locks?.background&&img){setHint('Background is locked · unlock it from Locks first');setTimeout(hint,1400);return}$('file').click()}",
    "locked import guard"
)

# ---------- Move/Edit mode ----------
rep(
    "function clearSelection(){selection=[];syncSelectionBar();draw()}",
    '''function clearSelection(){selection=[];syncSelectionBar();draw()}
function syncMoveMode(){for(const id of ['moveModeTop','moveModeBottom']){const b=$(id);if(!b)continue;b.classList.toggle('active',navMode);b.textContent=id==='moveModeTop'?(navMode?'Move ON':'Move OFF'):(navMode?'✋ Move ON':'✋ Move mode')}document.querySelector('.app')?.classList.toggle('moveModeActive',navMode)}
function setMoveMode(on){navMode=!!on;drawing=null;gesture=null;pointers.clear();pinchIds.clear();if(navMode){selection=[];syncSelectionBar();closeToolMenus();setHint('Move mode ON · drag or pinch the plan · drawing taps are disabled')}else hint();syncMoveMode();draw()}
function editToolLayer(t){if(zoneTools?.has?.(t))return'zones';if(layoutTools?.has?.(t)||objectTools?.has?.(t))return'building';if(t==='symbol')return'symbols';if(t==='note'||detailTools?.has?.(t))return'notes';return null}
function toolLockReason(t){if(state.locks?.building&&(layoutTools.has(t)||objectTools.has(t)))return'Building is locked';if(state.locks?.zones&&zoneTools.has(t))return'Zones are locked';return''}''',
    "move mode functions"
)

# Add trim to tool taxonomy and labels.
rep(
    "layoutTools=new Set(['wall','pen','layoutRect','layoutPoly','label','quickLabel'])",
    "layoutTools=new Set(['wall','pen','layoutRect','layoutPoly','label','quickLabel','trim'])",
    "trim tool taxonomy"
)
rep(
    "layoutPoly:'Outline',label:'Room label',pinNote:'Pinned note'",
    "layoutPoly:'Outline',label:'Room label',trim:'Trim / Extend',pinNote:'Pinned note'",
    "trim tool label"
)
rep(
    "function setTool(t){tool=t;drawing=null;poly=[];",
    "function setTool(t){if(navMode){navMode=false;syncMoveMode()}const layer=editToolLayer(t);if(layer&&state.layers?.[layer]===false){state.layers[layer]=true;renderLayersMenu()}tool=t;drawing=null;poly=[];",
    "set tool exits move mode"
)
rep(
    "label:'Tap a room and type its name',quickLabel:",
    "label:'Tap a room and type its name',trim:'Tap near a wall end · it automatically trims or extends to the nearest intersecting wall',quickLabel:",
    "trim tool hint"
)

# ---------- Layers / locks / device counts ----------
rep(
    "function allRefs(){const refs=[];for(const type of ['walls','doors','windows','shutters','stairs','labels','symbols','pins','notes','shapes'])for(const o of state[type]||[])refs.push({type,id:o.id});return refs}",
    '''function allRefs(){const refs=[];for(const type of ['walls','doors','windows','shutters','stairs','labels','symbols','pins','notes','shapes'])for(const o of state[type]||[])refs.push({type,id:o.id});return refs}
function refLayer(ref){if(['walls','doors','windows','shutters','stairs'].includes(ref.type))return'building';if(ref.type==='labels')return'labels';if(ref.type==='symbols')return'symbols';if(['pins','notes'].includes(ref.type))return'notes';if(ref.type==='shapes')return'zones';return null}
function refVisible(ref){const layer=refLayer(ref);return !layer||state.layers?.[layer]!==false}
function isRefLocked(ref){if(ref.type==='shapes')return!!state.locks?.zones;if(['walls','doors','windows','shutters','stairs','labels'].includes(ref.type))return!!state.locks?.building;return false}
function renderLockMenu(){document.querySelectorAll('[data-lock]').forEach(b=>{const key=b.dataset.lock,on=!!state.locks?.[key],label=b.dataset.lockLabel||key;b.classList.toggle('active',on);b.lastElementChild.textContent=on?'Locked':'Unlocked';b.firstElementChild.textContent=(on?'🔒 ':'🔓 ')+label})}
function renderLayersMenu(){document.querySelectorAll('[data-layer]').forEach(b=>{const key=b.dataset.layer,on=state.layers?.[key]!==false,label=b.dataset.layerLabel||key;b.classList.toggle('active',on);b.lastElementChild.textContent=on?'Shown':'Hidden';b.firstElementChild.textContent=(on?'✓ ':'○ ')+label})}
function countSymbols(list){const out={panel:0,mcp:0,smoke:0,heat:0,sounder:0,you:0};for(const sm of list||[])if(sm.type in out)out[sm.type]++;return out}
function fillCountBox(id,counts){const box=$(id);if(!box)return;box.textContent='';let total=0;for(const key of ['panel','mcp','smoke','heat','sounder','you']){const n=counts[key]||0;total+=n;const name=document.createElement('span');name.textContent=symbolNames[key];const value=document.createElement('strong');value.textContent=String(n);box.append(name,value)}const name=document.createElement('span');name.textContent='Total';const value=document.createElement('strong');value.textContent=String(total);box.append(name,value)}
function renderDeviceCounts(){ensureFloors();const floor=countSymbols(state.symbols),building={panel:0,mcp:0,smoke:0,heat:0,sounder:0,you:0};for(const f of state.floors){const list=f.id===state.activeFloor?state.symbols:(f.data?.symbols||[]),c=countSymbols(list);for(const k in building)building[k]+=c[k]||0}fillCountBox('floorDeviceCounts',floor);fillCountBox('buildingDeviceCounts',building);const total=Object.values(floor).reduce((a,b)=>a+b,0);$('countsMenuBtn').textContent='Devices · '+total}''',
    "locks layers counts functions"
)

# Hidden/locked refs do not get selected/edited.
rep(
    "for(const ref of allRefs()){const bb=itemBounds(ref);",
    "for(const ref of allRefs()){if(!refVisible(ref)||isRefLocked(ref))continue;const bb=itemBounds(ref);",
    "box selection lock/layer filtering"
)
rep(
    "for(const ref of allRefs()){const o=getObj(ref);let d=Infinity;",
    "for(const ref of allRefs()){if(!refVisible(ref)||isRefLocked(ref))continue;const o=getObj(ref);let d=Infinity;",
    "hit testing lock/layer filtering"
)

# Selection bar properties state.
rep(
    "function syncSelectionBar(){const bar=$('selectionBar');bar.hidden=!selection.length;const st=selectionState();$('makeGroup').disabled=!st.canGroup;$('breakGroup').disabled=!st.canUngroup;if(!selection.length)return;",
    "function syncSelectionBar(){const bar=$('selectionBar');bar.hidden=!selection.length;const st=selectionState();$('makeGroup').disabled=!st.canGroup;$('breakGroup').disabled=!st.canUngroup;$('propertiesSelected').disabled=selection.length!==1;if(!selection.length)return;",
    "selection properties state"
)

# Object properties implementation after transform selection handlers.
rep(
    "$('duplicateSelected').onclick=duplicateSelection;$('rotateSelected').onclick=()=>transformSelection('rotate');$('mirrorSelected').onclick=()=>transformSelection('mirror');",
    '''$('duplicateSelected').onclick=duplicateSelection;$('rotateSelected').onclick=()=>transformSelection('rotate');$('mirrorSelected').onclick=()=>transformSelection('mirror');
const refNames={walls:'Wall',doors:'Door',windows:'Window',shutters:'Roller shutter',stairs:'Stairway',labels:'Room label',symbols:'Symbol',pins:'Pinned detail',notes:'Note',shapes:'Zone area'};
function openProperties(){if(selection.length!==1)return;const ref=selection[0],o=getObj(ref);if(!o)return;if(isRefLocked(ref)){setHint('That item is locked');setTimeout(hint,1000);return}$('propKind').textContent=refNames[ref.type]||ref.type;const hasText=['labels','notes','pins'].includes(ref.type),isSymbol=ref.type==='symbols',hasScale=['labels','symbols'].includes(ref.type),canTransform=['walls','doors','windows','shutters','stairs','shapes'].includes(ref.type);$('propTextWrap').hidden=!hasText;$('propText').value=hasText?(o.text||''):'';$('propSymbolWrap').hidden=!isSymbol;$('propColorWrap').hidden=!isSymbol;$('propScaleWrap').hidden=!hasScale;if(isSymbol){$('propSymbolType').value=o.type||'smoke';$('propColor').value=o.color||'#172333'}$('propScale').value=o.scale||1;$('propScaleValue').textContent=Number(o.scale||1).toFixed(2)+'×';$('propRotate').disabled=!canTransform;$('propMirror').disabled=!canTransform;$('propertyModal').classList.add('open')}
function closeProperties(){$('propertyModal').classList.remove('open')}
$('propertiesSelected').onclick=openProperties;$('propClose').onclick=closeProperties;$('propertyModal').onclick=e=>{if(e.target===$('propertyModal'))closeProperties()};$('propScale').oninput=e=>$('propScaleValue').textContent=Number(e.target.value).toFixed(2)+'×';
$('propSave').onclick=()=>{if(selection.length!==1)return;const ref=selection[0],o=getObj(ref);if(!o||isRefLocked(ref))return;push();if(['labels','notes','pins'].includes(ref.type))o.text=$('propText').value.trim().slice(0,80)||o.text;if(ref.type==='symbols'){o.type=$('propSymbolType').value;o.color=$('propColor').value}if(['labels','symbols'].includes(ref.type))o.scale=Number($('propScale').value)||1;closeProperties();changed();setHint('Properties updated');setTimeout(hint,800)};
$('propRotate').onclick=()=>{if(selection.length===1)transformSelection('rotate')};$('propMirror').onclick=()=>{if(selection.length===1)transformSelection('mirror')};
$('propDelete').onclick=()=>{if(selection.length!==1)return;const ref=selection[0],o=getObj(ref);if(!o||isRefLocked(ref))return;if(!confirm('Delete this '+(refNames[ref.type]||'object').toLowerCase()+'?'))return;push();const arr=state[ref.type],i=arr.findIndex(x=>x.id===ref.id);if(i>=0)arr.splice(i,1);selection=[];closeProperties();changed()};''',
    "object properties logic"
)

# ---------- Layer-aware canvas rendering ----------
rep("picture(ctx,v.ox,v.oy,img.width*v.s,img.height*v.s);drawGrid(ctx,v);", "picture(ctx,v.ox,v.oy,img.width*v.s,img.height*v.s);if(state.layers.grid!==false)drawGrid(ctx,v);", "grid layer")
rep("for(const sh of state.shapes){const z=state.zones.find", "if(state.layers.zones!==false)for(const sh of state.shapes){const z=state.zones.find", "zone layer draw")
rep("for(const wall of state.walls)stroke(ctx,wall.points.map(map),state.wallWidth);", "if(state.layers.building!==false)for(const wall of state.walls)stroke(ctx,wall.points.map(map),state.wallWidth);", "wall layer draw")
rep("for(const door of state.doors)drawDoor(ctx,", "if(state.layers.building!==false)for(const door of state.doors)drawDoor(ctx,", "door layer draw")
rep("for(const win of state.windows)drawWindow(ctx,", "if(state.layers.building!==false)for(const win of state.windows)drawWindow(ctx,", "window layer draw")
rep("for(const sh of state.shutters)drawShutter(ctx,", "if(state.layers.building!==false)for(const sh of state.shutters)drawShutter(ctx,", "shutter layer draw")
rep("for(const st of state.stairs)drawStairs(ctx,", "if(state.layers.building!==false)for(const st of state.stairs)drawStairs(ctx,", "stairs layer draw")
rep(
    "const stampSize=Math.min(img.width,img.height)*.018*v.s;for(const sm of state.symbols||[]){const p=map(sm);drawSymbol(ctx,p,sm.type,stampSize*(sm.scale||1),sm.color||'#172333')}for(let i=0;i<(state.pins||[]).length;i++){const pin=state.pins[i],p=map(pin);drawPin(ctx,p,i,stampSize*.72)}for(const l of state.labels){const p=map(l),fs=Math.min(img.width,img.height)*.022*v.s;roomLabel(ctx,p.x,p.y,l.text,fs*(l.scale||1))}",
    "const stampSize=Math.min(img.width,img.height)*.018*v.s;if(state.layers.symbols!==false)for(const sm of state.symbols||[]){const p=map(sm);drawSymbol(ctx,p,sm.type,stampSize*(sm.scale||1),sm.color||'#172333')}if(state.layers.notes!==false)for(let i=0;i<(state.pins||[]).length;i++){const pin=state.pins[i],p=map(pin);drawPin(ctx,p,i,stampSize*.72)}if(state.layers.labels!==false)for(const l of state.labels){const p=map(l),fs=Math.min(img.width,img.height)*.022*v.s;roomLabel(ctx,p.x,p.y,l.text,fs*(l.scale||1))}",
    "symbol pin label layers"
)
rep("for(const n of state.notes){const p=map(n);badge(ctx,p.x,p.y,n.text,'#1b344e')}", "if(state.layers.notes!==false)for(const n of state.notes){const p=map(n);badge(ctx,p.x,p.y,n.text,'#1b344e')}", "notes layer draw")

# ---------- Trim / Extend ----------
rep(
    "function eraseAt(clientX,clientY){",
    '''function infiniteLineSegmentHit(a,b,c,d){const r={x:b.x-a.x,y:b.y-a.y},q={x:d.x-c.x,y:d.y-c.y},den=r.x*q.y-r.y*q.x;if(Math.abs(den)<1e-10)return null;const ca={x:c.x-a.x,y:c.y-a.y},t=(ca.x*q.y-ca.y*q.x)/den,u=(ca.x*r.y-ca.y*r.x)/den;if(u<-.0001||u>1.0001)return null;return{t,u,p:{x:a.x+r.x*t,y:a.y+r.y*t}}}
function trimExtendAt(clientX,clientY){if(state.locks?.building){setHint('Building is locked · unlock it first');setTimeout(hint,1200);return}const p=point(clientX,clientY),hit=nearestWall(p,34);if(!hit){setHint('Tap close to the END of the wall you want to trim or extend');setTimeout(hint,1400);return}const w=hit.wall,A=screenPoint(w.points[0]),B=screenPoint(w.points[1]),r=canvas.getBoundingClientRect(),C={x:clientX-r.left,y:clientY-r.top},d0=Math.hypot(C.x-A.x,C.y-A.y),d1=Math.hypot(C.x-B.x,C.y-B.y),end=d0<=d1?0:1;if(Math.min(d0,d1)>38){setHint('Tap closer to a wall end');setTimeout(hint,1200);return}const fixed=w.points[1-end],moving=w.points[end];let best=null;for(const other of state.walls){if(other.id===w.id||other.kind!=='wall'||other.points?.length!==2)continue;const x=infiniteLineSegmentHit(fixed,moving,other.points[0],other.points[1]);if(!x||x.t<=.002)continue;const px=screenPoint(x.p),pm=screenPoint(moving),dist=Math.hypot(px.x-pm.x,px.y-pm.y);if(dist<4)continue;if(!best||dist<best.dist)best={...x,dist}}if(!best){setHint('No intersecting wall found in line with that wall end');setTimeout(hint,1500);return}push();w.points[end]=snapGridPoint(best.p);const action=best.t<1?'trimmed':'extended';mergeOverlappingWalls();changed();setHint('Wall '+action+' to the nearest intersection');setTimeout(hint,1000)}
function eraseAt(clientX,clientY){''',
    "trim extend logic"
)

# ---------- Menu handlers ----------
rep(
    "$('zoneMenuBtn').onclick=()=>toggleMenu($('zoneMenu'),$('zoneMenuBtn'));",
    "$('zoneMenuBtn').onclick=()=>toggleMenu($('zoneMenu'),$('zoneMenuBtn'));$('locksMenuBtn').onclick=()=>{if($('locksMenu').classList.contains('open'))closeToolMenus();else placeMenuBelow($('locksMenu'),$('locksMenuBtn'))};$('layersMenuBtn').onclick=()=>{if($('layersMenu').classList.contains('open'))closeToolMenus();else placeMenuBelow($('layersMenu'),$('layersMenuBtn'))};$('countsMenuBtn').onclick=()=>{renderDeviceCounts();if($('countsMenu').classList.contains('open'))closeToolMenus();else placeMenuBelow($('countsMenu'),$('countsMenuBtn'))};",
    "top precision menu handlers"
)
rep(
    "document.querySelectorAll('[data-detail-tool]').forEach(b=>b.onclick=()=>setTool(b.dataset.detailTool));",
    "document.querySelectorAll('[data-detail-tool]').forEach(b=>b.onclick=()=>setTool(b.dataset.detailTool));document.querySelectorAll('[data-lock]').forEach(b=>b.onclick=()=>{const k=b.dataset.lock;state.locks[k]=!state.locks[k];renderLockMenu();syncBackground();persist();draw()});document.querySelectorAll('[data-layer]').forEach(b=>b.onclick=()=>{const k=b.dataset.layer;state.layers[k]=state.layers[k]===false;renderLayersMenu();persist();draw()});",
    "lock layer event handlers"
)
rep(
    "!e.target.closest('#detailMenuBtn')&&!e.target.closest('#floorMenuBtn')",
    "!e.target.closest('#detailMenuBtn')&&!e.target.closest('#locksMenuBtn')&&!e.target.closest('#layersMenuBtn')&&!e.target.closest('#countsMenuBtn')&&!e.target.closest('#floorMenuBtn')",
    "precision popup click-away"
)

# Prevent zone modal changes while locked.
rep(
    "function openModal(z=null){editId=z?.id||null;",
    "function openModal(z=null){if(state.locks?.zones){setHint('Zones are locked · unlock them from Locks first');setTimeout(hint,1300);return}editId=z?.id||null;",
    "zone lock modal guard"
)

# ---------- Pointer interaction mode + trim guard ----------
rep(
    "if(pointers.size===2){for(const id of pointers.keys())pinchIds.add(id);drawing=null;gesture={a:[...pointers.values()],zoom,pan:{...pan}};draw();return}if(tool==='pan'){drawing={mode:'pan',at:{x:e.clientX,y:e.clientY},pan:{...pan}};return}",
    "if(navMode){if(pointers.size===2){for(const id of pointers.keys())pinchIds.add(id);drawing=null;gesture={a:[...pointers.values()],zoom,pan:{...pan}};draw();return}if(pointers.size===1){drawing={mode:'navPan',at:{x:e.clientX,y:e.clientY},pan:{...pan}};return}}if(pointers.size>1)return;const lockedReason=toolLockReason(tool);if(lockedReason){setHint(lockedReason+' · use the Locks menu to unlock it');setTimeout(hint,1300);return}",
    "pointer move/edit mode split"
)
rep_first(
    "if(tool==='pen'){drawing={points:[point(e.clientX,e.clientY)]};return}",
    "if(tool==='trim'){trimExtendAt(e.clientX,e.clientY);return}if(tool==='pen'){drawing={points:[point(e.clientX,e.clientY)]};return}",
    "trim pointer action"
)
rep(
    "if(pointers.size===2&&gesture){",
    "if(navMode&&pointers.size===2&&gesture){",
    "pinch only in move mode"
)
rep(
    "if(tool==='pan'&&drawing?.mode==='pan'){pan={x:drawing.pan.x+e.clientX-drawing.at.x,y:drawing.pan.y+e.clientY-drawing.at.y};draw()}",
    "if(navMode&&drawing?.mode==='navPan'){pan={x:drawing.pan.x+e.clientX-drawing.at.x,y:drawing.pan.y+e.clientY-drawing.at.y};draw()}",
    "one-finger pan only in move mode"
)

# Move mode buttons near zones-panel controls.
rep(
    "$('zonesPanelBtn').onclick=()=>setZonesPanel(!zonesPanelOpen);$('closeZones').onclick=()=>setZonesPanel(false);syncZonesPanel();",
    "$('zonesPanelBtn').onclick=()=>setZonesPanel(!zonesPanelOpen);$('closeZones').onclick=()=>setZonesPanel(false);$('moveModeTop').onclick=()=>setMoveMode(!navMode);$('moveModeBottom').onclick=()=>setMoveMode(!navMode);syncZonesPanel();syncMoveMode();",
    "move mode button wiring"
)

# ---------- Office export device count ----------
rep(
    "legendH=140+d.zones.length*40+Math.min(d.notes.length,10)*28+pinExtra",
    "legendH=210+d.zones.length*40+Math.min(d.notes.length,10)*28+pinExtra",
    "export legend space"
)
rep(
    "let ny=start+20+d.zones.length*40;if(d.notes.length){",
    "let ny=start+20+d.zones.length*40;const dc=countSymbols(d.symbols);x.fillStyle='#18283d';x.font='bold 16px system-ui';x.fillText('DEVICE COUNT',pad,ny+13);ny+=28;x.font='14px system-ui';const deviceLine=['panel','mcp','smoke','heat','sounder','you'].map(k=>symbolNames[k]+' ×'+dc[k]).join('   ·   ');x.fillText(deviceLine.slice(0,150),pad,ny+12);ny+=34;if(d.notes.length){",
    "export device count"
)

# Initial rendering.
rep(
    "renderFloors();renderSymbolColors();new ResizeObserver(draw).observe(wrap);syncWallSize();updateButtons();syncToolMenus();renderZoneMenu();load();draw();",
    "ensureUiState();renderFloors();renderSymbolColors();renderLockMenu();renderLayersMenu();renderDeviceCounts();syncMoveMode();new ResizeObserver(draw).observe(wrap);syncWallSize();updateButtons();syncToolMenus();renderZoneMenu();load();draw();",
    "initial precision rendering"
)

# README note.
readme = Path('README.md')
rt = readme.read_text() if readme.exists() else '# Zone Sketch\n'
if '## Version 0.15' not in rt:
    rt += '''\n\n## Version 0.15\n- Global Move mode: ON pans/zooms without editing; OFF edits without canvas panning.\n- Trim / Extend wall tool.\n- Object Properties for selected items.\n- Background, Building and Zone locks.\n- View-only Layers menu for background, building, zones, symbols, labels, notes/pins and grid.\n- Current-floor and whole-building device counts, also included in office exports.\n'''
    readme.write_text(rt)

# Synchronise all app copies.
for path in [Path('index.html'), Path('ZoneSketch.html'), Path('app/src/main/assets/index.html')]:
    path.write_text(s)

print('Zone Sketch v0.15 precision editing upgrade applied')
