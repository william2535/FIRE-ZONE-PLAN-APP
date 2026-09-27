from pathlib import Path

APP_COPIES = [
    Path('index.html'),
    Path('ZoneSketch.html'),
    Path('Zone-Sketch-by-Will.html'),
    Path('app/src/main/assets/index.html'),
]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old in text:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f'{label}: expected one anchor, found {count}')
        return text.replace(old, new)
    if new in text:
        return text
    raise SystemExit(f'{label}: anchor not found')


master = APP_COPIES[0].read_text()

old_issue = "function cbCircuitIssue(c){if(!c?.bounds||!c.layout||!Array.isArray(c.deviceIds)||!Array.isArray(c.sequence)||!Array.isArray(c.legs))return true;for(const id of [c.panelId,...c.deviceIds]){const device=cbSymbol(id),at=c.layout[id];if(!device||!at)return true;const original=cbBoardToPlan(at,c.bounds);if(Math.hypot(original.x-device.x,original.y-device.y)>.0001)return true}return false}"
new_issue = r"""function cbCircuitStoredPlanPoint(c,id){const at=c?.layout?.[id];return at&&c?.bounds?cbBoardToPlan(at,c.bounds):null}
function cbCircuitRepairTolerance(){if(!img)return .0025;const step=Math.max(1,Number(gridStep?.()||10)),side=Math.max(1,Math.min(img.width||1,img.height||1));return Math.max(.0015,Math.min(.012,step/side*1.6))}
function cbCircuitRemapId(c,oldId,newId){if(!c||!oldId||!newId||oldId===newId)return false;if(c.panelId===oldId)c.panelId=newId;if(Array.isArray(c.deviceIds))c.deviceIds=c.deviceIds.map(id=>id===oldId?newId:id);if(Array.isArray(c.sequence))c.sequence=c.sequence.map(id=>id===oldId?newId:id);if(c.eolId===oldId)c.eolId=newId;if(c.layout?.[oldId]){if(!c.layout[newId])c.layout[newId]=c.layout[oldId];delete c.layout[oldId]}const remapLegs=legs=>{for(const leg of legs||[]){if(leg?.from===oldId)leg.from=newId;if(leg?.to===oldId)leg.to=newId}};remapLegs(c.legs);const d=c.editDraft;if(d){remapLegs(d.legs);const p=d.pending;if(p){if(p.from===oldId)p.from=newId;if(p.to===oldId)p.to=newId;if(p.startDeviceId===oldId)p.startDeviceId=newId;if(p.endDeviceId===oldId)p.endDeviceId=newId}}return true}
function cbRepairConventionalRefs(c){if(c?.type!=='conventional'||!c.zoneId||!c?.bounds||!c.layout||!Array.isArray(c.deviceIds)||!c.deviceIds.length)return false;const current=cbZoneDevices(c.zoneId);if(current.length!==c.deviceIds.length)return false;const currentIds=new Set(current.map(d=>d.id)),used=new Set(),missing=[];for(const oldId of c.deviceIds){const live=cbSymbol(oldId);if(live){if(symbolScope(live)!=='survey'||!currentIds.has(oldId)||used.has(oldId))return false;used.add(oldId)}else missing.push(oldId)}const available=current.filter(d=>!used.has(d.id)),tol=cbCircuitRepairTolerance(),pairs=[];for(const oldId of missing){const expected=cbCircuitStoredPlanPoint(c,oldId);if(!expected)return false;let best=null;for(const d of available){if(pairs.some(p=>p.newId===d.id))continue;const dist=Math.hypot(expected.x-d.x,expected.y-d.y);if(!best||dist<best.dist)best={oldId,newId:d.id,dist}}if(!best||best.dist>tol)return false;pairs.push(best)}let panelPair=null;if(!cbSymbol(c.panelId)){const expected=cbCircuitStoredPlanPoint(c,c.panelId),panels=cbPanels();if(!expected||!panels.length)return false;let best=null;for(const p of panels){const dist=Math.hypot(expected.x-p.x,expected.y-p.y);if(!best||dist<best.dist)best={oldId:c.panelId,newId:p.id,dist}}if(!best||best.dist>Math.max(tol*2,.004))return false;panelPair=best}if(!pairs.length&&!panelPair)return false;for(const pair of pairs)cbCircuitRemapId(c,pair.oldId,pair.newId);if(panelPair)cbCircuitRemapId(c,panelPair.oldId,panelPair.newId);c.updatedAt=Date.now();return true}
function cbRepairConventionalCircuits(){let repaired=0;for(const c of cbCircuits())if(cbRepairConventionalRefs(c))repaired++;return repaired}
function cbCircuitIssue(c){if(!c?.bounds||!c.layout||!Array.isArray(c.deviceIds)||!Array.isArray(c.sequence)||!Array.isArray(c.legs))return true;for(const id of [c.panelId,...c.deviceIds]){const device=cbSymbol(id),at=c.layout[id];if(!device||!at)return true;const original=cbBoardToPlan(at,c.bounds);if(Math.hypot(original.x-device.x,original.y-device.y)>.0001)return true}return false}"""
master = replace_once(master, old_issue, new_issue, 'circuit reference repair helpers')

old_symbol = "let cbSymbolSource=null,cbSymbolCount=-1,cbSymbolIndex=new Map();function cbSymbol(id){const list=state.symbols||[];if(list!==cbSymbolSource||list.length!==cbSymbolCount){cbSymbolSource=list;cbSymbolCount=list.length;cbSymbolIndex=new Map(list.map(s=>[s.id,s]))}return cbSymbolIndex.get(id)||null}"
new_symbol = "let cbSymbolSource=null,cbSymbolCount=-1,cbSymbolEpoch=0,cbSymbolBuiltEpoch=-1,cbSymbolIndex=new Map();function cbInvalidateSymbolIndex(){cbSymbolEpoch++}function cbSymbol(id){const list=state.symbols||[];if(list!==cbSymbolSource||list.length!==cbSymbolCount||cbSymbolBuiltEpoch!==cbSymbolEpoch){cbSymbolSource=list;cbSymbolCount=list.length;cbSymbolBuiltEpoch=cbSymbolEpoch;cbSymbolIndex=new Map(list.map(s=>[s.id,s]))}return cbSymbolIndex.get(id)||null}"
master = replace_once(master, old_symbol, new_symbol, 'symbol lookup invalidation')

old_changed = "function changed(){syncBackground();syncGrid();renderFloors();renderZones();syncSelectionBar();syncWallSize();renderLockMenu();renderLayersMenu();renderDeviceCounts();draw();persist();updateButtons()}"
new_changed = "function changed(){if(typeof cbInvalidateSymbolIndex==='function')cbInvalidateSymbolIndex();syncBackground();syncGrid();renderFloors();renderZones();syncSelectionBar();syncWallSize();renderLockMenu();renderLayersMenu();renderDeviceCounts();draw();persist();updateButtons()}"
master = replace_once(master, old_changed, new_changed, 'symbol cache invalidation on state change')

old_sync = "function cbSyncChallengeBounds(save=false){const bounds=cbChallengeBounds();let touched=false;for(const c of cbCircuits())if(c.type==='conventional')touched=cbRebaseCircuit(c,bounds)||touched;if(save&&touched){state.asFit=null;persist()}return bounds}"
new_sync = "function cbSyncChallengeBounds(save=false){const repaired=cbRepairConventionalCircuits(),bounds=cbChallengeBounds();let touched=repaired>0;for(const c of cbCircuits())if(c.type==='conventional')touched=cbRebaseCircuit(c,bounds)||touched;if(save&&touched){state.asFit=null;persist()}return bounds}"
master = replace_once(master, old_sync, new_sync, 'challenge bounds reference recovery')

old_open = "function cbOpenCircuit(c){cbCheckpointDrag(true);if(cbCircuitIssue(c)){"
new_open = "function cbOpenCircuit(c){cbCheckpointDrag(true);if(c?.type==='conventional'&&cbRepairConventionalRefs(c)){state.asFit=null;persist()}if(cbCircuitIssue(c)){"
master = replace_once(master, old_open, new_open, 'open circuit reference recovery')

# Promote the matched Web + Android tester milestone.
master = master.replace('Zone Sketch by Will Flood v0.59', 'Zone Sketch by Will Flood v0.60')
master = master.replace('BETA v0.59', 'BETA v0.60')
for path in APP_COPIES:
    path.write_text(master)

gradle_path = Path('app/build.gradle')
gradle = gradle_path.read_text().replace('versionCode 60', 'versionCode 61').replace("versionName '0.59'", "versionName '0.60'")
gradle_path.write_text(gradle)

beta_path = Path('beta.html')
beta = beta_path.read_text()
beta = beta.replace('./web-v059.html', './web-v060.html')
beta = beta.replace('v0.59', 'v0.60')
beta = beta.replace(
    '<div class="update"><strong>Manual cable editing</strong><span>Pencil, Bin, Undo/Redo, Bridge and Cleanup now survive interruptions safely, preserve staged work, keep circuit status honest and protect edited geometry when plan bounds change.</span></div>',
    '<div class="update"><strong>Circuit recovery</strong><span>Completed conventional routes now repair stale device links when the same surveyed devices are still in the same zone, instead of wrongly blocking a clearly drawn circuit.</span></div><div class="update"><strong>Manual cable editing</strong><span>Pencil, Bin, Undo/Redo, Bridge and Cleanup survive interruptions safely, preserve staged work, keep circuit status honest and protect edited geometry when plan bounds change.</span></div>'
)
beta = beta.replace(
    'Please stress Manual Edit on iPhone/Android, switch between circuits, rotate/resize the screen, reload a saved draft and check the final As-Fit still follows the edited route.',
    'Please stress multi-zone Circuit Builder jobs: complete several zones, leave/reopen Circuit Builder, and confirm every clearly drawn route stays valid and available to the As-Fit. Manual Edit, rotation/resize and saved-draft reloads are still worth testing too.'
)
beta_path.write_text(beta)
Path('download.html').write_text(beta)

Path('web-v060.html').write_text('''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="0"><title>Zone Sketch Web v0.60 — Fresh Launch</title><meta name="theme-color" content="#10263d"><style>html,body{height:100%;margin:0;font-family:system-ui,-apple-system,sans-serif;background:#10263d;color:#fff}body{display:grid;place-items:center}.card{text-align:center;padding:24px;max-width:360px}.mark{font-size:42px}.title{font-size:21px;font-weight:900;margin:8px 0}.sub{color:#c6d7e6;font-size:13px;line-height:1.45}a{display:inline-block;margin-top:16px;padding:11px 15px;border-radius:11px;background:#fff;color:#10263d;text-decoration:none;font-weight:800}</style></head><body><div class="card"><div class="mark">🍍</div><div class="title">Opening Zone Sketch Web v0.60</div><div class="sub">Fresh Pineapple milestone launcher — bypassing older cached app documents.</div><a id="fallback" href="./index.html?pineapple=v060">Open v0.60</a></div><script>const target='./index.html?pineapple=v060&fresh='+Date.now();document.getElementById('fallback').href=target;location.replace(target);</script></body></html>''')

print('Prepared Pineapple v0.60 circuit-reference hotfix and matched Web/Android metadata.')
