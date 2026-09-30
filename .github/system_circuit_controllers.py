#!/usr/bin/env python3
from pathlib import Path

PATH = Path("index.html")
text = PATH.read_text(encoding="utf-8")

def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly 1 match, found {count}")
    text = text.replace(old, new, 1)

# Install a project-system aware controller layer immediately before the Circuit Builder
# collection helpers. Internal route storage remains backwards compatible: existing Fire
# circuits still use panelId and addressable/conventional route types.
old = "function cbCircuits(){if(!Array.isArray(state.circuits))state.circuits=[];return state.circuits}\nfunction cbPanels(){return(state.symbols||[]).filter(s=>s.type==='panel')}\nfunction cbSurveyDevices(){return(state.symbols||[]).filter(s=>symbolScope(s)==='survey'&&s.type!=='panel'&&s.type!=='you')}"
new = """const CB_CONTROLLERS=Object.freeze({
 fire:{type:'panel',name:'Fire Alarm Panel',short:'FAP',runName:'Loop',runLabel:'addressable loop',highlightLabel:'addressable loop',returnToController:true},
 security:{type:'secPanel',name:'Intruder Panel',short:'Intruder Panel',runName:'Circuit',runLabel:'security circuit',highlightLabel:'security circuit',returnToController:false},
 access:{type:'accessAcu',name:'ACU',short:'ACU',runName:'Access Run',runLabel:'access run',highlightLabel:'access run',returnToController:false},
 cctv:{type:'cctvNvr',name:'NVR',short:'NVR',runName:'Camera Run',runLabel:'camera run',highlightLabel:'camera run',returnToController:false}
});
const CB_CONTROLLER_TYPES=new Set(Object.values(CB_CONTROLLERS).map(c=>c.type));
function cbControllerConfig(c=null){const key=systemFor(c?.systemType||state.systemType).key;return CB_CONTROLLERS[key]||CB_CONTROLLERS.fire}
function cbIsAnyControllerSymbol(s){return !!s&&CB_CONTROLLER_TYPES.has(s.type)}
function cbIsControllerSymbol(s,c=null){return !!s&&s.type===cbControllerConfig(c).type}
function cbCircuitNeedsReturn(c){return !!c&&c.type==='addressable'&&cbControllerConfig(c).returnToController}
function cbCircuitModeLabel(c){return c?.type==='addressable'?(cbCircuitNeedsReturn(c)?'Addressable loop':cbControllerConfig(c).runLabel):'Zone challenge'}
function cbCircuitControllerNotice(cfg=cbControllerConfig()){return{title:cfg.name+' required',body:'Add '+(cfg.type==='secPanel'?'an ':'a ')+cfg.name+' in Survey before building this circuit. Circuit Builder uses it as the start point'+(cfg.returnToController?' and return point.':'.')}}
function cbSyncSystemCircuitUi(){const cfg=cbControllerConfig(),key=systemFor(state.systemType).key,button=$('cbAddressableStart'),panel=button?.closest('.cbModePanel'),heading=panel?.querySelector('h2'),copy=panel?.querySelector('p'),hero=document.querySelector('#cbLanding .cbLandingHero h1');if(key==='fire'){if(hero)hero.textContent='Connect the zone';if(heading)heading.textContent='Addressable';if(copy)copy.textContent='Highlight the devices that belong to the loop by tapping or sweeping across them on the plan, then build the loop.';if(button)button.textContent='Highlight a loop';return}if(hero)hero.textContent=key==='security'?'Connect the circuit':key==='access'?'Connect the access run':'Connect the camera run';if(heading)heading.textContent=key==='security'?'Intruder circuits':key==='access'?'Access circuits':'Camera runs';if(copy)copy.textContent=key==='security'?'Highlight the intruder devices on this circuit, then route them from the Intruder Panel.':key==='access'?'Highlight the access devices on this run, then route them from the ACU.':'Highlight the cameras on this run, then route them from the NVR.';if(button)button.textContent='Highlight '+cfg.highlightLabel}
function cbCircuits(){if(!Array.isArray(state.circuits))state.circuits=[];return state.circuits}
function cbPanels(c=null){const type=cbControllerConfig(c).type;return(state.symbols||[]).filter(s=>s.type===type)}
function cbSurveyDevices(){return(state.symbols||[]).filter(s=>symbolScope(s)==='survey'&&!cbIsAnyControllerSymbol(s)&&s.type!=='you')}"""
replace_once(old, new, "controller layer")

replace_once(
    "const expected=cbCircuitStoredPlanPoint(c,c.panelId),panels=cbPanels();",
    "const expected=cbCircuitStoredPlanPoint(c,c.panelId),panels=cbPanels(c);",
    "conventional controller repair",
)

replace_once(
    "function cbNearestPanel(devices){const panels=cbPanels();if(!panels.length)return null;const pts=devices?.length?devices:panels,cx=pts.reduce((n,p)=>n+p.x,0)/pts.length,cy=pts.reduce((n,p)=>n+p.y,0)/pts.length;return panels.slice().sort((a,b)=>Math.hypot(a.x-cx,a.y-cy)-Math.hypot(b.x-cx,b.y-cy))[0]}",
    "function cbNearestPanel(devices,c=null){const panels=cbPanels(c);if(!panels.length)return null;const pts=devices?.length?devices:panels,cx=pts.reduce((n,p)=>n+p.x,0)/pts.length,cy=pts.reduce((n,p)=>n+p.y,0)/pts.length;return panels.slice().sort((a,b)=>Math.hypot(a.x-cx,a.y-cy)-Math.hypot(b.x-cx,b.y-cy))[0]}",
    "nearest project controller",
)

replace_once(
    "function cbNewCircuit(type,devices,zoneId=null){const panel=cbNearestPanel(devices);if(!panel){uiNotice('Fire panel required','Add a fire panel (FAP) in Survey before building this circuit. Circuit Builder uses it as the start and return point.');return null}const bounds=type==='conventional'?cbChallengeBounds():cbBoundsFor(zoneId,devices,panel),index=cbCircuits().filter(c=>c.type===type).length+1,z=zoneId?(state.zones||[]).find(z=>z.id===zoneId):null,c={id:uid(),type,zoneId,panelId:panel.id,deviceIds:devices.map(d=>d.id),bounds,layout:null,sequence:[panel.id],legs:[],complete:false,eolId:null,color:z?.color||CB_COLORS[(index-1)%CB_COLORS.length],name:type==='conventional'?'Zone '+(z?.number||index):'Loop '+index,updatedAt:Date.now()};c.layout=cbMakeLayout([panel.id,...c.deviceIds],bounds);push();cbCircuits().push(c);changed();return c}",
    "function cbNewCircuit(type,devices,zoneId=null){const systemType=systemFor(state.systemType).key,cfg=cbControllerConfig({systemType}),panel=cbNearestPanel(devices,{systemType});if(!panel){const notice=cbCircuitControllerNotice(cfg);uiNotice(notice.title,notice.body);return null}const bounds=type==='conventional'?cbChallengeBounds():cbBoundsFor(zoneId,devices,panel),index=cbCircuits().filter(c=>c.type===type).length+1,z=zoneId?(state.zones||[]).find(z=>z.id===zoneId):null,c={id:uid(),type,systemType,zoneId,panelId:panel.id,deviceIds:devices.map(d=>d.id),bounds,layout:null,sequence:[panel.id],legs:[],complete:false,eolId:null,color:z?.color||CB_COLORS[(index-1)%CB_COLORS.length],name:type==='conventional'?'Zone '+(z?.number||index):cfg.runName+' '+index,updatedAt:Date.now()};c.layout=cbMakeLayout([panel.id,...c.deviceIds],bounds);push();cbCircuits().push(c);changed();return c}",
    "new circuit controller",
)

replace_once(
    "(c.type==='addressable'?'Addressable loop':'Zone challenge')",
    "cbCircuitModeLabel(c)",
    "circuit management label",
)

replace_once(
    "function cbRenderLanding(){const zones=$('cbConventionalZones'),side=$('cbExisting'),list=cbCircuits();",
    "function cbRenderLanding(){cbSyncSystemCircuitUi();const zones=$('cbConventionalZones'),side=$('cbExisting'),list=cbCircuits();",
    "landing system UI",
)

old_open = "function cbOpenCircuit(c){cbCheckpointDrag(true);if(c?.type==='conventional'&&cbRepairConventionalRefs(c)){state.asFit=null;persist()}if(cbCircuitIssue(c)){const devices=(c.deviceIds||[]).map(cbSymbol).filter(d=>d&&symbolScope(d)==='survey'&&d.type!=='panel'&&d.type!=='you'),panel=cbSymbol(c.panelId)||cbNearestPanel(devices);if(!devices.length||!panel){uiNotice('Circuit needs attention','This saved route is missing surveyed devices or its fire panel. Restore them in Survey, or remove this circuit and create a new route.');return}if(!confirm('The surveyed devices changed since this route was built. Rebuild this circuit using their current positions? The existing route will be cleared.'))return;push();c.deviceIds=devices.map(d=>d.id);c.panelId=panel.id;c.sequence=[panel.id];c.legs=[];delete c.editDraft;c.bridges=[];c.complete=false;c.eolId=null;state.asFit=null;persist()}if(c.type==='conventional')cbRebaseCircuit(c,cbSyncChallengeBounds(false));if(!(c.legs||[]).length&&!c.complete){const devices=(c.deviceIds||[]).map(cbSymbol).filter(Boolean),panel=cbSymbol(c.panelId);c.bounds=c.type==='conventional'?cbChallengeBounds():cbBoundsFor(c.zoneId,devices,panel);c.layout=cbMakeLayout([c.panelId,...c.deviceIds],c.bounds)}cbEdit=null;cbBuildBridge=false;cbCircuit=c;cbEditSyncUi();cbDrag=null;cbHover=null;cbSelection.clear();cbResetView(false);const z=c.zoneId?(state.zones||[]).find(z=>z.id===c.zoneId):null;$('cbCircuitTitle').textContent=c.type==='conventional'?'Zone '+(z?.number||'')+(z?.name?' · '+z.name:''):c.name;const pill=$('cbCircuitType');pill.textContent=c.type==='addressable'?'ADDRESSABLE LOOP':'ZONE CHALLENGE';pill.classList.toggle('zoneChallenge',c.type==='conventional');pill.style.setProperty('--cb-color',c.color||'#65768a');$('cbGame').classList.toggle('zoneChallenge',c.type==='conventional');$('cbSelectCount').hidden=true;$('cbBuildSelected').hidden=true;$('cbUndoLeg').hidden=false;$('cbReset').hidden=false;$('cbComplete').hidden=false;cbShow('game');cbRenderLanding();cbUpdateGame();cbDrawBoard();if(c.editDraft)cbEnterEdit(c)}"
new_open = "function cbOpenCircuit(c){cbCheckpointDrag(true);if(!c.systemType)c.systemType=systemFor(state.systemType).key;if(c?.type==='conventional'&&cbRepairConventionalRefs(c)){state.asFit=null;persist()}if(cbCircuitIssue(c)){const devices=(c.deviceIds||[]).map(cbSymbol).filter(d=>d&&symbolScope(d)==='survey'&&!cbIsAnyControllerSymbol(d)&&d.type!=='you');let panel=cbSymbol(c.panelId);if(!cbIsControllerSymbol(panel,c))panel=cbNearestPanel(devices,c);if(!devices.length||!panel){uiNotice('Circuit needs attention','This saved route is missing surveyed devices or its '+cbControllerConfig(c).name+'. Restore them in Survey, or remove this circuit and create a new route.');return}if(!confirm('The surveyed devices changed since this route was built. Rebuild this circuit using their current positions? The existing route will be cleared.'))return;push();c.deviceIds=devices.map(d=>d.id);c.panelId=panel.id;c.sequence=[panel.id];c.legs=[];delete c.editDraft;c.bridges=[];c.complete=false;c.eolId=null;state.asFit=null;persist()}if(c.type==='conventional')cbRebaseCircuit(c,cbSyncChallengeBounds(false));if(!(c.legs||[]).length&&!c.complete){const devices=(c.deviceIds||[]).map(cbSymbol).filter(Boolean),panel=cbSymbol(c.panelId);c.bounds=c.type==='conventional'?cbChallengeBounds():cbBoundsFor(c.zoneId,devices,panel);c.layout=cbMakeLayout([c.panelId,...c.deviceIds],c.bounds)}cbEdit=null;cbBuildBridge=false;cbCircuit=c;cbEditSyncUi();cbDrag=null;cbHover=null;cbSelection.clear();cbResetView(false);const z=c.zoneId?(state.zones||[]).find(z=>z.id===c.zoneId):null;$('cbCircuitTitle').textContent=c.type==='conventional'?'Zone '+(z?.number||'')+(z?.name?' · '+z.name:''):c.name;const pill=$('cbCircuitType');pill.textContent=c.type==='addressable'?(cbCircuitNeedsReturn(c)?'ADDRESSABLE LOOP':cbControllerConfig(c).runLabel.toUpperCase()):'ZONE CHALLENGE';pill.classList.toggle('zoneChallenge',c.type==='conventional');pill.style.setProperty('--cb-color',c.color||'#65768a');$('cbGame').classList.toggle('zoneChallenge',c.type==='conventional');$('cbSelectCount').hidden=true;$('cbBuildSelected').hidden=true;$('cbUndoLeg').hidden=false;$('cbReset').hidden=false;$('cbComplete').hidden=false;cbShow('game');cbRenderLanding();cbUpdateGame();cbDrawBoard();if(c.editDraft)cbEnterEdit(c)}"
replace_once(old_open, new_open, "open circuit controller")

replace_once(
    "function cbStartAddressable(){$('cbGame').classList.remove('zoneChallenge');$('cbCircuitType').classList.remove('zoneChallenge');const devices=cbSurveyDevices();if(!devices.length){uiNotice('No surveyed devices yet','Place the installed detectors and field devices in Survey before creating an addressable loop.');return}if(!cbPanels().length){uiNotice('Fire panel required','Add a fire panel (FAP) in Survey before creating an addressable loop.');return}cbCircuit=null;cbBuildBridge=false;cbSelection.clear();cbResetView(false);cbSelectBounds=cbBounds([...devices,...cbPanels()],.06);$('cbCircuitTitle').textContent='Highlight addressable loop';$('cbCircuitType').textContent='SWIPE / TAP DEVICES';$('cbSelectCount').hidden=false;$('cbBuildSelected').hidden=false;$('cbUndoLeg').hidden=true;$('cbReset').hidden=false;$('cbComplete').hidden=true;cbShow('select');cbUpdateGame();cbDrawBoard()}",
    "function cbStartAddressable(){$('cbGame').classList.remove('zoneChallenge');$('cbCircuitType').classList.remove('zoneChallenge');const cfg=cbControllerConfig(),devices=cbSurveyDevices();if(!devices.length){uiNotice('No surveyed devices yet','Place the installed field devices in Survey before creating this '+cfg.runLabel+'.');return}if(!cbPanels().length){const notice=cbCircuitControllerNotice(cfg);uiNotice(notice.title,notice.body);return}cbCircuit=null;cbBuildBridge=false;cbSelection.clear();cbResetView(false);cbSelectBounds=cbBounds([...devices,...cbPanels()],.06);$('cbCircuitTitle').textContent='Highlight '+cfg.highlightLabel;$('cbCircuitType').textContent='SWIPE / TAP DEVICES';$('cbSelectCount').hidden=false;$('cbBuildSelected').hidden=false;$('cbUndoLeg').hidden=true;$('cbReset').hidden=false;$('cbComplete').hidden=true;cbShow('select');cbUpdateGame();cbDrawBoard()}",
    "start system run",
)

replace_once(
    "function cbValidTarget(id){const c=cbCircuit;if(!c||!id)return false;const seq=[...c.sequence,...(cbDrag?.targets||[])];if(id===seq.at(-1))return false;const visited=new Set(seq);if(id===c.panelId)return c.type==='addressable'&&c.deviceIds.every(x=>visited.has(x))&&seq.length>1;return c.deviceIds.includes(id)&&!visited.has(id)}",
    "function cbValidTarget(id){const c=cbCircuit;if(!c||!id)return false;const seq=[...c.sequence,...(cbDrag?.targets||[])];if(id===seq.at(-1))return false;const visited=new Set(seq);if(id===c.panelId)return cbCircuitNeedsReturn(c)&&c.deviceIds.every(x=>visited.has(x))&&seq.length>1;return c.deviceIds.includes(id)&&!visited.has(id)}",
    "controller route target",
)

replace_once(
    "function cbSequenceReady(c,seq){if(!c)return false;const visited=new Set(seq),done=c.deviceIds.every(id=>visited.has(id));return c.type==='conventional'?done:(done&&seq.at(-1)===c.panelId&&seq.length>1)}",
    "function cbSequenceReady(c,seq){if(!c)return false;const visited=new Set(seq),done=c.deviceIds.every(id=>visited.has(id));return c.type==='conventional'||!cbCircuitNeedsReturn(c)?done:(done&&seq.at(-1)===c.panelId&&seq.length>1)}",
    "system route completion",
)

replace_once(
    "captured=cbScreen==='game'&&s.type!=='panel'&&(seq.has(s.id)||queued.has(s.id))",
    "captured=cbScreen==='game'&&!cbIsAnyControllerSymbol(s)&&(seq.has(s.id)||queued.has(s.id))",
    "controller captured badge",
)
replace_once(
    "panelReady=s.type==='panel'&&allDone&&!cbCircuit?.complete",
    "panelReady=cbIsControllerSymbol(s,cbCircuit)&&cbCircuitNeedsReturn(cbCircuit)&&allDone&&!cbCircuit?.complete",
    "controller return ring",
)

replace_once(
    "const symbolColor=s.type==='panel'?null:(owner?.color||routeColor);cbDrawNode(x,s,p,s.type==='panel'?CB_PANEL_R:CB_DEVICE_R,ring,cbScreen==='select'&&s.type==='panel',symbolColor)",
    "const controller=cbIsAnyControllerSymbol(s),symbolColor=controller?null:(owner?.color||routeColor);cbDrawNode(x,s,p,controller?CB_PANEL_R:CB_DEVICE_R,ring,cbScreen==='select'&&controller,symbolColor)",
    "controller rendering",
)

replace_once(
    "else if(cbScreen==='select')$('cbBoardHint').textContent='Pinch to zoom · tap or sweep across the devices in this loop';",
    "else if(cbScreen==='select')$('cbBoardHint').textContent='Pinch to zoom · tap or sweep across devices for this '+cbControllerConfig().runLabel;",
    "selection hint",
)

replace_once(
    "else if(cbCircuit?.type==='addressable'&&cbSequenceReady(cbCircuit,[...cbCircuit.sequence,...(cbDrag?.targets||[])]))$('cbBoardHint').textContent='Back at the fire panel · loop complete';else if(returning)$('cbBoardHint').textContent='Return to the green-ring FAP · the cable is magnetically following the outgoing route';",
    "else if(cbCircuit?.type==='addressable'&&cbSequenceReady(cbCircuit,[...cbCircuit.sequence,...(cbDrag?.targets||[])]))$('cbBoardHint').textContent=cbCircuitNeedsReturn(cbCircuit)?'Back at the '+cbControllerConfig(cbCircuit).name+' · loop complete':'All devices connected · complete the '+cbControllerConfig(cbCircuit).runLabel;else if(returning)$('cbBoardHint').textContent='Return to the green-ring '+cbControllerConfig(cbCircuit).short+' · the cable is magnetically following the outgoing route';",
    "system route hints",
)

replace_once(
    "function cbGameCounts(){if(!cbCircuit)return{done:0,total:0,ready:false};const seq=[...cbCircuit.sequence,...(cbDrag?.targets||[])],visited=new Set(seq),done=cbCircuit.deviceIds.filter(id=>visited.has(id)).length,total=cbCircuit.deviceIds.length,ready=cbCircuit.type==='conventional'?done===total:(done===total&&seq.at(-1)===cbCircuit.panelId&&seq.length>1);return{done,total,ready}}",
    "function cbGameCounts(){if(!cbCircuit)return{done:0,total:0,ready:false};const seq=[...cbCircuit.sequence,...(cbDrag?.targets||[])],visited=new Set(seq),done=cbCircuit.deviceIds.filter(id=>visited.has(id)).length,total=cbCircuit.deviceIds.length,ready=cbCircuit.type==='conventional'||!cbCircuitNeedsReturn(cbCircuit)?done===total:(done===total&&seq.at(-1)===cbCircuit.panelId&&seq.length>1);return{done,total,ready}}",
    "system game counts",
)

replace_once(
    "backNeeded=cbCircuit.type==='addressable'&&q.done===q.total&&seq.at(-1)!==cbCircuit.panelId",
    "backNeeded=cbCircuitNeedsReturn(cbCircuit)&&q.done===q.total&&seq.at(-1)!==cbCircuit.panelId",
    "return needed",
)
replace_once(
    "if(label)label.textContent=cbCircuit.type==='conventional'?'ZONE DEVICES':'LOOP DEVICES'",
    "if(label)label.textContent=cbCircuit.type==='conventional'?'ZONE DEVICES':cbCircuitNeedsReturn(cbCircuit)?'LOOP DEVICES':'RUN DEVICES'",
    "hud mode label",
)
replace_once(
    "cbCircuit.complete?(cbCircuit.type==='addressable'?'LOOP CLOSED':'CIRCUIT COMPLETE'):backNeeded?'RETURN TO FAP':left?left+' LEFT':'ALL CONNECTED'",
    "cbCircuit.complete?(cbCircuitNeedsReturn(cbCircuit)?'LOOP CLOSED':'CIRCUIT COMPLETE'):backNeeded?'RETURN TO '+cbControllerConfig(cbCircuit).short.toUpperCase():left?left+' LEFT':'ALL CONNECTED'",
    "hud completion label",
)
replace_once(
    "q.done+' / '+q.total+' devices connected'+(backNeeded?' · return to panel':'')",
    "q.done+' / '+q.total+' devices connected'+(backNeeded?' · return to '+cbControllerConfig(cbCircuit).name:'')",
    "progress controller label",
)
replace_once(
    "cbCircuit.complete?'Circuit complete ✓':backNeeded?'Return to FAP':'Complete circuit'",
    "cbCircuit.complete?'Circuit complete ✓':backNeeded?'Return to '+cbControllerConfig(cbCircuit).short:'Complete circuit'",
    "complete button controller label",
)

replace_once(
    "if(!remaining)text=cbCircuit.type==='addressable'?'ALL CONNECTED · BRING IT HOME':'ALL DEVICES CONNECTED';",
    "if(!remaining)text=cbCircuitNeedsReturn(cbCircuit)?'ALL CONNECTED · BRING IT HOME':'ALL DEVICES CONNECTED';",
    "milestone return behavior",
)

replace_once(
    "function cbReturnPhase(){const c=cbCircuit;if(!c||c.type!=='addressable'||c.complete)return false;",
    "function cbReturnPhase(){const c=cbCircuit;if(!c||!cbCircuitNeedsReturn(c)||c.complete)return false;",
    "return magnet system guard",
)

PATH.write_text(text, encoding="utf-8")
print("Applied system-aware Circuit Builder controllers.")
