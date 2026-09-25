from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'index.html'
s = SRC.read_text(encoding='utf-8')


def once(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f'{label} marker not found')
    s = s.replace(old, new, 1)

# Visible version for the v0.58 development generation.
s = s.replace('ZONE SKETCH · v0.57', 'ZONE SKETCH · v0.58')
s = s.replace('BETA v0.57', 'BETA v0.58')
s = s.replace('<b>v0.57</b>', '<b>v0.58</b>')

# Circuit-row layout gains a compact edit affordance.
s = s.replace('grid-template-columns:10px minmax(0,1fr) auto auto;', 'grid-template-columns:10px minmax(0,1fr) auto auto auto;')

css = r'''

/* v0.58 Project Pineapple — local route editor foundation. */
.cbEditToggle.active,.cbEditDock button.active{background:#173f60!important;color:#fff!important;border-color:#173f60!important;box-shadow:0 0 0 3px #2c78b522}
.cbEditStatus{border-color:#d59d48!important;background:#fff4df!important;color:#87550f!important}.cbEditStatus.open{border-color:#d45d55!important;background:#fff0ef!important;color:#9b312c!important}
.cbEditDock{position:absolute;z-index:9;right:10px;top:54px;display:flex;align-items:center;gap:5px;max-width:calc(100% - 20px);padding:6px;border:1px solid #c7d5e2;border-radius:14px;background:#fffffff5;box-shadow:0 9px 28px #10263d24;backdrop-filter:blur(7px)}
.cbEditDock[hidden]{display:none!important}.cbEditDock button{min-width:39px;min-height:38px;padding:6px 9px;border:1px solid #cedae5;background:#edf3f8;font-size:11px}.cbEditDock .danger.active{background:#a53e38!important;border-color:#a53e38!important}.cbEditDock .done{background:#25834e;color:#fff;border-color:#25834e;font-weight:850}.cbEditDock .bridge{width:40px;min-width:40px;border-radius:50%;padding:0;font-size:17px}.cbEditDock .bridge.active{background:#8b5bc1!important;border-color:#8b5bc1!important}.cbEditOptions{position:relative}.cbEditOptions summary{list-style:none;cursor:pointer;min-height:38px;display:flex;align-items:center;padding:0 9px;border:1px solid #cedae5;border-radius:9px;background:#edf3f8;color:#304b64;font-size:10px;font-weight:850;white-space:nowrap}.cbEditOptions summary::-webkit-details-marker{display:none}.cbEditOptionsPanel{position:absolute;right:0;top:45px;width:210px;padding:11px;border:1px solid #c9d7e3;border-radius:13px;background:#fff;box-shadow:0 12px 34px #10263d2e}.cbEditOptionsPanel label{display:grid;gap:7px;color:#40566b;font-size:10px;font-weight:800}.cbEditOptionsPanel input{width:100%}.cbZoneEditRow{display:grid;grid-template-columns:minmax(0,1fr) 42px;gap:6px;margin-bottom:7px}.cbZoneEditRow .cbZoneButton{margin-bottom:0}.cbZoneEditButton{min-width:42px;padding:0;border:1px solid #d1dce6;border-radius:11px;background:#eef4f8;font-size:17px}.cbCircuitRow .cbRowEdit{min-width:38px;padding:6px 8px;font-size:15px}.cbBoardWrap.cbEditing{box-shadow:0 0 0 2px #2c78b538,0 12px 36px #10263d16}.cbBoardWrap.cbRouteOpen{box-shadow:0 0 0 2px #c34e473d,0 12px 36px #10263d16}.cbBoardWrap.cbDeleteTool{cursor:crosshair}
@media(max-width:760px){.cbEditDock{left:7px;right:7px;top:auto;bottom:7px;overflow-x:auto;justify-content:flex-start;padding:5px}.cbEditDock button{min-width:42px;min-height:42px}.cbEditOptionsPanel{position:fixed;left:12px;right:12px;bottom:64px;top:auto;width:auto}.cbZoomDock.editing{bottom:58px}.cbBoardHint.editing{bottom:108px}.cbZoneEditRow{grid-template-columns:minmax(0,1fr) 44px}}
'''
once('</style>', css + '\n</style>', 'style close')

# Add edit state pill to the game header.
once('<span id="cbCircuitType" class="cbPill"></span><span class="cbGrow"></span>', '<span id="cbCircuitType" class="cbPill"></span><span id="cbEditStatus" class="cbPill cbEditStatus" hidden>EDITING</span><span class="cbGrow"></span>', 'game header')

# Add Edit beside Fit and the compact edit toolbar.
old_zoom = '<div class="cbZoomDock" aria-label="Circuit zoom"><button id="cbZoomOut" title="Zoom out">−</button><button id="cbZoomFit" class="fit" title="Fit circuit to screen">Fit</button><button id="cbZoomIn" title="Zoom in">+</button></div>'
new_zoom = '''<div id="cbZoomDock" class="cbZoomDock" aria-label="Circuit zoom"><button id="cbZoomOut" title="Zoom out">−</button><button id="cbZoomFit" class="fit" title="Fit circuit to screen">Fit</button><button id="cbEditToggle" class="fit cbEditToggle" title="Edit this cable route">✎ Edit</button><button id="cbZoomIn" title="Zoom in">+</button></div><div id="cbEditDock" class="cbEditDock" aria-label="Route editing" hidden><button id="cbEditPencil" title="Draw a replacement route section">✎ Pencil</button><button id="cbEditBin" class="danger" title="Remove one local cable section">⌫ Bin</button><button id="cbEditUndo" title="Undo route edit">↶</button><button id="cbEditRedo" title="Redo route edit">↷</button><button id="cbEditBridge" class="bridge" aria-pressed="false" title="Bridge Mode — allow an intentional crossing">⌒</button><details id="cbEditOptions" class="cbEditOptions"><summary>Clean · <span id="cbEditCleanupValue">50%</span></summary><div class="cbEditOptionsPanel"><label>Bend cleaning strength<input id="cbEditCleanup" type="range" min="0" max="100" step="5" value="50"></label><small>Applied after a Pencil stroke is committed. Live drawing stays responsive.</small></div></details><button id="cbEditDone" class="done" title="Validate and finish editing">Done</button></div>'''
once(old_zoom, new_zoom, 'zoom dock')

# Editor state lives with the Circuit Builder state machine.
once("let cbSound=true,cbRewardTimer=null,cbRewardKey='',cbLastReward=0,cbLastBell=-Infinity;", "let cbSound=true,cbRewardTimer=null,cbRewardKey='',cbLastReward=0,cbLastBell=-Infinity;\nlet cbEditor={active:false,tool:'pencil',bridge:false,cleanup:50},cbEditUndo=[],cbEditRedo=[];", 'editor state')

old_segments = "function cbLegSegments(c){const out=[];for(const leg of c?.legs||[]){const pts=leg.points||[];for(let i=1;i<pts.length;i++)out.push({a:pts[i-1],b:pts[i],color:c.color||'#2675db'})}return out}"
editor_code = r'''function cbLegSegments(c){const out=[];for(let li=0;li<(c?.legs||[]).length;li++){const leg=c.legs[li],pts=leg.points||[];for(let i=1;i<pts.length;i++)out.push({a:pts[i-1],b:pts[i],color:c.color||'#2675db',legIndex:li,segmentIndex:i-1,key:li+':'+(i-1)})}return out}
function cbVisibleSegments(c,segments=cbLegSegments(c)){const cuts=new Set((c?.editCuts||[]).map(String));return(segments||[]).filter(seg=>!cuts.has(seg.key||seg.legIndex+':'+seg.segmentIndex))}
function cbEditorSnapshot(){if(!cbCircuit)return null;return JSON.parse(JSON.stringify({legs:cbCircuit.legs||[],sequence:cbCircuit.sequence||[],complete:!!cbCircuit.complete,eolId:cbCircuit.eolId??null,editOpen:!!cbCircuit.editOpen,editCuts:cbCircuit.editCuts||[],editCleanup:Number(cbCircuit.editCleanup??50),bridges:cbCircuit.bridges||[]}))}
function cbEditorRestore(snap){if(!cbCircuit||!snap)return;cbCircuit.legs=JSON.parse(JSON.stringify(snap.legs||[]));cbCircuit.sequence=[...(snap.sequence||[])];cbCircuit.complete=!!snap.complete;cbCircuit.eolId=snap.eolId??null;cbCircuit.editOpen=!!snap.editOpen;cbCircuit.editCuts=[...(snap.editCuts||[])];cbCircuit.editCleanup=Number(snap.editCleanup??50);cbCircuit.bridges=JSON.parse(JSON.stringify(snap.bridges||[]));cbCircuit.updatedAt=Date.now();state.asFit=null;persist();cbSyncEditorUi();cbRenderLanding();cbUpdateGame();cbDrawBoard()}
function cbEditorPush(){const snap=cbEditorSnapshot();if(!snap)return;cbEditUndo.push(snap);if(cbEditUndo.length>50)cbEditUndo.shift();cbEditRedo=[]}
function cbEditorUndoAction(){if(!cbEditUndo.length||!cbCircuit)return;const now=cbEditorSnapshot(),snap=cbEditUndo.pop();cbEditRedo.push(now);cbEditorRestore(snap)}
function cbEditorRedoAction(){if(!cbEditRedo.length||!cbCircuit)return;const now=cbEditorSnapshot(),snap=cbEditRedo.pop();cbEditUndo.push(now);cbEditorRestore(snap)}
function cbPointSegmentDistance(p,a,b){const dx=b.x-a.x,dy=b.y-a.y,l2=dx*dx+dy*dy;if(!l2)return Math.hypot(p.x-a.x,p.y-a.y);const t=Math.max(0,Math.min(1,((p.x-a.x)*dx+(p.y-a.y)*dy)/l2)),x=a.x+t*dx,y=a.y+t*dy;return Math.hypot(p.x-x,p.y-y)}
function cbNearestEditableSegment(pt,w,h){if(!cbCircuit)return null;let best=null;const hit=Math.max(11,Math.min(22,12*Math.sqrt(Math.max(1,cbView.scale))));for(const seg of cbVisibleSegments(cbCircuit)){const a=cbBoardPx(seg.a,w,h),b=cbBoardPx(seg.b,w,h),d=cbPointSegmentDistance(pt,a,b);if(d<=hit&&(!best||d<best.d))best={...seg,d}}return best}
function cbEditorSetTool(tool){if(!['pencil','bin'].includes(tool))return;cbEditor.tool=tool;cbSyncEditorUi();cbDrawBoard()}
function cbEnterEditor(){if(!cbCircuit||cbScreen!=='game')return;cbCheckpointDrag();cbEditor={active:true,tool:'pencil',bridge:false,cleanup:Number(cbCircuit.editCleanup??50)};cbEditUndo=[];cbEditRedo=[];cbCircuit.editCuts=Array.isArray(cbCircuit.editCuts)?cbCircuit.editCuts:[];cbCircuit.editOpen=!!cbCircuit.editOpen||cbCircuit.editCuts.length>0;cbSyncEditorUi();cbUpdateGame();cbDrawBoard()}
function cbExitEditor(silent=false){if(!cbEditor.active)return;cbEditor.active=false;cbEditor.bridge=false;cbEditor.tool='pencil';cbDrag=null;cbHover=null;cbSyncEditorUi();cbUpdateGame();cbDrawBoard();if(!silent&&cbCircuit?.editOpen)uiToast('Route left open · repair it before As-Fit','warn')}
function cbEditorDeleteAt(pt,w,h){if(!cbEditor.active||cbEditor.tool!=='bin'||!cbCircuit)return false;const seg=cbNearestEditableSegment(pt,w,h);if(!seg){uiToast('Tap closer to the cable section you want to remove','info');return false}cbEditorPush();const key=seg.key||seg.legIndex+':'+seg.segmentIndex;cbCircuit.editCuts=Array.isArray(cbCircuit.editCuts)?cbCircuit.editCuts:[];if(!cbCircuit.editCuts.includes(key))cbCircuit.editCuts.push(key);cbCircuit.editOpen=true;cbCircuit.complete=false;cbCircuit.updatedAt=Date.now();state.asFit=null;persist();cbSyncEditorUi();cbRenderLanding();cbUpdateGame();cbDrawBoard();uiToast('Cable section removed · route open','warn');return true}
function cbEditorValidation(c=cbCircuit){if(!c)return{ok:false,message:'No circuit selected'};const cuts=(c.editCuts||[]).length;if(cuts)return{ok:false,message:cuts+' open cable section'+(cuts===1?'':'s')+' still need repair'};if(cbCircuitIssue(c))return{ok:false,message:'Survey devices changed — rebuild or repair the circuit first'};const segs=cbVisibleSegments(c);if(!segs.length)return{ok:false,message:'No cable route remains'};for(const seg of segs)for(const p of [seg.a,seg.b])if(!Number.isFinite(p?.x)||!Number.isFinite(p?.y))return{ok:false,message:'Cable contains an invalid coordinate'};if(!cbSequenceReady(c,c.sequence||[]))return{ok:false,message:'The circuit is not connected through every assigned device'};return{ok:true,message:'Route validates'}}
function cbEditorDone(){if(!cbCircuit)return;const result=cbEditorValidation();if(!result.ok){cbCircuit.editOpen=true;cbCircuit.complete=false;state.asFit=null;persist();cbSyncEditorUi();cbUpdateGame();uiToast(result.message,'warn');return false}cbCircuit.editOpen=false;cbCircuit.editCuts=[];cbCircuit.complete=true;cbCircuit.updatedAt=Date.now();state.asFit=null;persist();cbExitEditor(true);cbRenderLanding();cbUpdateGame();uiToast('Route validated · circuit complete','success');return true}
function cbSyncEditorUi(){const active=!!(cbEditor.active&&cbCircuit&&cbScreen==='game'),open=!!cbCircuit?.editOpen;const dock=$('cbEditDock'),toggle=$('cbEditToggle'),status=$('cbEditStatus'),board=$('cbBoardWrap'),zoomDock=$('cbZoomDock'),hint=$('cbBoardHint');if(dock)dock.hidden=!active;if(toggle){toggle.hidden=cbScreen!=='game'||!cbCircuit;toggle.classList.toggle('active',active);toggle.textContent=active?'✎ Editing':'✎ Edit'}if(status){status.hidden=!active&&!open;status.textContent=open?'EDITING · ROUTE OPEN':active?'EDITING · ROUTE VALID':'EDITING · ROUTE OPEN';status.classList.toggle('open',open)}if(board){board.classList.toggle('cbEditing',active);board.classList.toggle('cbRouteOpen',open);board.classList.toggle('cbDeleteTool',active&&cbEditor.tool==='bin')}if(zoomDock)zoomDock.classList.toggle('editing',active);if(hint)hint.classList.toggle('editing',active);for(const [id,on] of [['cbEditPencil',cbEditor.tool==='pencil'],['cbEditBin',cbEditor.tool==='bin'],['cbEditBridge',cbEditor.bridge]]){const el=$(id);if(el)el.classList.toggle('active',active&&on)}if($('cbEditBridge')){$('cbEditBridge').setAttribute('aria-pressed',String(active&&cbEditor.bridge));$('cbEditBridge').title=cbEditor.bridge?'Bridge Mode ON — intentional crossings allowed for Pencil':'Bridge Mode OFF — crossings stay blocked'}if($('cbEditCleanup'))$('cbEditCleanup').value=String(Number(cbEditor.cleanup??50));if($('cbEditCleanupValue'))$('cbEditCleanupValue').textContent=Number(cbEditor.cleanup??50)+'%';if($('cbEditUndo'))$('cbEditUndo').disabled=!cbEditUndo.length;if($('cbEditRedo'))$('cbEditRedo').disabled=!cbEditRedo.length;if(cbScreen==='game'){if($('cbUndoLeg'))$('cbUndoLeg').hidden=active;if($('cbReset'))$('cbReset').hidden=active;if($('cbComplete'))$('cbComplete').hidden=active}if(active){if($('cbDetectorLeft'))$('cbDetectorLeft').textContent=open?'EDITING · ROUTE OPEN':'EDITING ROUTE';if($('cbProgress'))$('cbProgress').textContent=open?'Editing · route open · repair before Done':'Editing route · Pencil or Bin a local section'}}
$('cbEditToggle').onclick=()=>cbEditor.active?cbExitEditor():cbEnterEditor();
$('cbEditPencil').onclick=()=>cbEditorSetTool('pencil');
$('cbEditBin').onclick=()=>cbEditorSetTool('bin');
$('cbEditUndo').onclick=cbEditorUndoAction;
$('cbEditRedo').onclick=cbEditorRedoAction;
$('cbEditBridge').onclick=()=>{if(!cbEditor.active)return;cbEditor.bridge=!cbEditor.bridge;cbSyncEditorUi();uiToast('Bridge Mode '+(cbEditor.bridge?'on':'off'),cbEditor.bridge?'success':'info')};
$('cbEditCleanup').oninput=e=>{if(!cbEditor.active||!cbCircuit)return;cbEditor.cleanup=Math.max(0,Math.min(100,Number(e.target.value)||0));cbCircuit.editCleanup=cbEditor.cleanup;cbCircuit.updatedAt=Date.now();persist();cbSyncEditorUi()};
$('cbEditDone').onclick=cbEditorDone;'''
once(old_segments, editor_code, 'segment/editor functions')

# The left zone list and created-circuit rows both get an edit affordance.
once("side.append(cbZoneChoice(z,c,true))", "{const compact=cbZoneChoice(z,c,true);if(c){const wrap=document.createElement('div');wrap.className='cbZoneEditRow';const edit=document.createElement('button');edit.className='cbZoneEditButton';edit.textContent='✎';edit.title='Edit '+c.name+' cable route';edit.setAttribute('aria-label','Edit '+c.name+' cable route');edit.onclick=()=>{cbOpenCircuit(c);cbEnterEditor()};wrap.append(compact,edit);side.append(wrap)}else side.append(compact)}", 'side edit action')
old_row = "const open=document.createElement('button');open.textContent='Open';open.onclick=()=>cbOpenCircuit(c);const remove=document.createElement('button');"
new_row = "const edit=document.createElement('button');edit.className='cbRowEdit';edit.textContent='✎';edit.title='Edit cable route';edit.setAttribute('aria-label','Edit '+c.name+' cable route');edit.onclick=()=>{cbOpenCircuit(c);cbEnterEditor()};const open=document.createElement('button');open.textContent='Open';open.onclick=()=>cbOpenCircuit(c);const remove=document.createElement('button');"
once(old_row, new_row, 'management edit action')
once('row.append(dot,label,open,remove);', 'row.append(dot,label,edit,open,remove);', 'management row append')

# Surface route-open state in list rows and prevent As-Fit treating it as valid.
s = s.replace("c.complete?' done':''", "c.complete&&!c.editOpen?' done':''")
s = s.replace("c?.complete?' done':''", "c?.complete&&!c?.editOpen?' done':''")
s = s.replace("cbCircuitIssue(c)?' · survey changed':c.complete?' · complete':'')", "cbCircuitIssue(c)?' · survey changed':c.editOpen?' · EDITING · ROUTE OPEN':c.complete?' · complete':'')")
s = s.replace("c.complete&&!cbCircuitIssue(c)", "c.complete&&!c.editOpen&&!cbCircuitIssue(c)")
once("status=list.some(cbCircuitIssue)?'Survey devices have changed. Open the affected circuit to rebuild its route.':ready?", "status=list.some(c=>c.editOpen)?'A circuit is EDITING · ROUTE OPEN. Repair and validate it before As-Fit.':list.some(cbCircuitIssue)?'Survey devices have changed. Open the affected circuit to rebuild its route.':ready?", 'landing open status')

# Render a cut as an actual visible gap, not a cosmetic status flag.
s = s.replace('const oldSegs=cbLegSegments(old);', 'const oldSegs=cbVisibleSegments(old,cbLegSegments(old));')
s = s.replace('const committed=cbLegSegments({...cbCircuit,color:routeColor})', 'const committed=cbVisibleSegments(cbCircuit,cbLegSegments({...cbCircuit,color:routeColor}))')

# Editor state owns the pointer while active. Bin performs one bounded segment hit; Pencil comes next.
once("function cbCanvasDown(e){if(e.button!==0||", "function cbCanvasDown(e){if(cbEditor?.active){if(e.button!==0)return;const c=$('cbCanvas'),r=c.getBoundingClientRect(),w=r.width,h=r.height,p=cbPointInCanvas(e);if(cbEditor.tool==='bin')cbEditorDeleteAt(p,w,h);else uiToast('Pencil redraw foundation ready · draw/repair milestone is next','info');return}if(e.button!==0||", 'canvas editor interception')

# Switching away safely leaves any broken edit persisted but Bridge always resets off.
once("function cbShow(screen){cbCheckpointDrag(true);", "function cbShow(screen){if(screen!=='game'&&cbEditor?.active)cbExitEditor(true);cbCheckpointDrag(true);", 'screen editor exit')
once("function closeCircuitBuilder(){cbCheckpointDrag(true);", "function closeCircuitBuilder(){if(cbEditor?.active)cbExitEditor(true);cbCheckpointDrag(true);", 'close editor exit')
once("function cbOpenCircuit(c){cbCheckpointDrag(true);", "function cbOpenCircuit(c){if(cbEditor?.active)cbExitEditor(true);cbCheckpointDrag(true);", 'circuit editor exit')

# Keep editor controls/status synchronized with normal game UI updates.
s = s.replace("$('cbReset').textContent='Clear highlighted';cbDrawBoard();return", "$('cbReset').textContent='Clear highlighted';cbSyncEditorUi();cbDrawBoard();return")
s = s.replace("if(!cbCircuit){if(hud)hud.hidden=true;return}", "if(!cbCircuit){if(hud)hud.hidden=true;cbSyncEditorUi();return}")
once("$('cbReset').textContent='Reset circuit';cbDrawBoard()}", "$('cbReset').textContent='Reset circuit';cbSyncEditorUi();cbDrawBoard()}", 'game UI sync')

# Editor-specific board hint wins over routing/completion hints.
once("if(cbScreen==='select')$('cbBoardHint').textContent='Pinch to zoom · tap or sweep across the devices in this loop';else if(blocked)", "if(cbScreen==='select')$('cbBoardHint').textContent='Pinch to zoom · tap or sweep across the devices in this loop';else if(cbEditor?.active)$('cbBoardHint').textContent=cbCircuit?.editOpen?(cbEditor.tool==='bin'?'Route open · remove another local section or switch to Pencil to repair':'Route open · Pencil a replacement section, then Done validates it'):(cbEditor.tool==='bin'?'Bin removes one local cable section only':'Pencil can start/end on cable or device · Bridge is explicit');else if(blocked)", 'editor board hint')

SRC.write_text(s, encoding='utf-8')
for rel in ['Zone-Sketch-by-Will.html', 'ZoneSketch.html', 'app/src/main/assets/index.html']:
    shutil.copyfile(SRC, ROOT / rel)
print('Applied Project Pineapple v0.58 editor foundation to all app copies')
