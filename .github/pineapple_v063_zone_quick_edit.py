from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'index.html'
text=INDEX.read_text(encoding='utf-8')


def replace_once(old,new,label):
    global text
    count=text.count(old)
    if count!=1:
        raise SystemExit(f'{label}: expected exactly 1 anchor, found {count}')
    text=text.replace(old,new,1)

# Visible milestone version. Keep this scoped to the app copies; delivery pages are handled separately.
text=text.replace('v0.62','v0.63')
text=text.replace('ZONE SKETCH · <b>v0.58</b>','ZONE SKETCH · <b>v0.63</b>')

# Per-floor zone tint. This keeps dense/small plans readable without forcing the same colour strength on every floor.
replace_once(
"activeZoneId:null,buildMode:true,pictureOpacity:1",
"activeZoneId:null,buildMode:true,zoneOpacity:.14,pictureOpacity:1",
'fresh zone opacity default')
replace_once(
"function ensureUiState(){state.locks={...defaultLocks(),...(state.locks||{})};state.layers={...defaultLayers(),...(state.layers||{})};if(typeof state.buildMode!=='boolean')state.buildMode=true}",
"function ensureUiState(){state.locks={...defaultLocks(),...(state.locks||{})};state.layers={...defaultLayers(),...(state.layers||{})};if(typeof state.buildMode!=='boolean')state.buildMode=true;const zo=Number(state.zoneOpacity);state.zoneOpacity=Number.isFinite(zo)?Math.max(.04,Math.min(.4,zo)):.14}",
'zone opacity normalisation')
replace_once(
"'activeZoneId','pictureOpacity'",
"'activeZoneId','zoneOpacity','pictureOpacity'",
'zone opacity floor persistence')

replace_once(
"<button id=\"buildModeBtn\" class=\"toggleItem active\" aria-pressed=\"true\" title=\"Build mode ON keeps zone placement and moving separate\"><span>Build mode</span><span>ON · Separate</span></button><label class=\"wallControl\" title=\"Grid spacing on the plan\">Grid",
"<button id=\"buildModeBtn\" class=\"toggleItem active\" aria-pressed=\"true\" title=\"Build mode ON keeps zone placement and moving separate\"><span>Build mode</span><span>ON · Separate</span></button><label id=\"zoneOpacityControl\" class=\"wallControl\" title=\"Zone colour strength on this floor\">Zone tint <input id=\"zoneOpacity\" type=\"range\" min=\"4\" max=\"40\" step=\"1\" value=\"14\"><output id=\"zoneOpacityValue\">14%</output></label><label class=\"wallControl\" title=\"Grid spacing on the plan\">Grid",
'zone tint control markup')
replace_once(
"for(const id of ['gridSize','wallSize'])$('drawingSliders').append($(id).closest('label'));",
"for(const id of ['gridSize','wallSize','zoneOpacity'])$('drawingSliders').append($(id).closest('label'));",
'zone tint Drawing placement')

replace_once(
"function syncBuildMode(){ensureUiState();const b=$('buildModeBtn'),on=state.buildMode!==false;if(!b)return;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on));b.firstElementChild.textContent='Build mode';b.lastElementChild.textContent=on?'ON · Separate':'OFF · Place + move';b.title=on?'Build mode ON · zone placement and moving are separate':'Build mode OFF · drag an existing zone to move it while zone placement stays active';const h=$('buildModeHelp');if(h)h.textContent=on?'Build mode ON keeps placing and moving separate. Best for larger plans where deliberate tools prevent accidental moves.':'Build mode OFF combines zone placement + moving. Drag inside an existing zone to move it; drag empty space to place with the current zone tool.'}",
"function syncBuildMode(){ensureUiState();const b=$('buildModeBtn'),on=state.buildMode!==false;if(!b)return;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on));b.firstElementChild.textContent='Build mode';b.lastElementChild.textContent=on?'ON · Separate':'OFF · Place + move';b.title=on?'Build mode ON · zone placement and moving are separate':'Build mode OFF · tap a zone to pick it, drag it to move it, or drag empty space to place';const h=$('buildModeHelp');if(h)h.textContent=on?'Build mode ON keeps placing and moving separate. Best for larger plans where deliberate tools prevent accidental moves.':'Build mode OFF combines Zone Plan jobs: tap an existing zone to pick that zone, drag it to move it, or drag empty space to place with the current zone tool.'}",
'combined mode quick-pick help')

replace_once(
"function syncModeUi(){syncBuildMode();$('rotateCanvas').disabled=surveyMode;",
"function syncModeUi(){syncBuildMode();syncZoneOpacity();$('zoneOpacityControl').hidden=surveyMode;$('rotateCanvas').disabled=surveyMode;",
'zone tint mode sync')
replace_once(
"function changed(){syncFloor();if(typeof cbInvalidateSymbolIndex==='function')cbInvalidateSymbolIndex();syncBackground();syncGrid();renderFloors();renderZones();syncSelectionBar();syncWallSize();renderLockMenu();",
"function changed(){syncFloor();if(typeof cbInvalidateSymbolIndex==='function')cbInvalidateSymbolIndex();syncBackground();syncGrid();renderFloors();renderZones();syncSelectionBar();syncWallSize();syncZoneOpacity();renderLockMenu();",
'zone tint changed sync')

replace_once(
"function drawGrid(c,v){",
"function zoneTint(d=state){const v=Number(d?.zoneOpacity);return Number.isFinite(v)?Math.max(.04,Math.min(.4,v)):.14}\nfunction syncZoneOpacity(){const input=$('zoneOpacity'),out=$('zoneOpacityValue');if(!input||!out)return;const v=zoneTint();input.value=String(Math.round(v*100));out.textContent=Math.round(v*100)+'%'}\nfunction drawGrid(c,v){",
'zone tint helpers')
replace_once(
"$('gridSize').oninput=e=>{state.gridSize=Number(e.target.value);if(surveyMode){state.gridVisible=true;state.snapGrid=true;alignSurveyDevicesToFieldGrid()}syncGrid();draw();persist()};\nfunction syncWallSize(){",
"$('gridSize').oninput=e=>{state.gridSize=Number(e.target.value);if(surveyMode){state.gridVisible=true;state.snapGrid=true;alignSurveyDevicesToFieldGrid()}syncGrid();draw();persist()};\nlet zoneOpacityEditing=false;$('zoneOpacity').oninput=e=>{if(!zoneOpacityEditing){push();zoneOpacityEditing=true}state.zoneOpacity=Math.max(.04,Math.min(.4,Number(e.target.value)/100));syncZoneOpacity();draw();persist()};$('zoneOpacity').onchange=()=>zoneOpacityEditing=false;\nfunction syncWallSize(){",
'zone tint input handler')

replace_once(
"drawZoneLayer(ctx,zonePaint,state.zones,map,.14)",
"drawZoneLayer(ctx,zonePaint,state.zones,map,zoneTint())",
'zone tint live canvas')
count=text.count("drawZoneLayer(x,d.shapes,d.zones,map,.14)")
if count!=2:
    raise SystemExit(f'zone tint export anchors: expected 2, found {count}')
text=text.replace("drawZoneLayer(x,d.shapes,d.zones,map,.14)","drawZoneLayer(x,d.shapes,d.zones,map,zoneTint(d))")

# Build mode OFF now has three distinct gestures without changing tools:
# tap an existing zone = make its zone active, drag an existing zone = move it,
# drag empty space = place with the currently armed zone tool.
replace_once(
"else if(((tool==='group'||tool==='select')||drawing?.combinedZone)&&drawing?.mode==='moveSelection'){const combined=!!drawing.combinedZone,moved=drawing.moved;drawing=null;if(moved){changed();setHint(combined?'Zone moved · placement tool still active':(selectionState().allSame?'Grouped object moved':'Object moved'));setTimeout(hint,800)}else draw();if(combined)return}",
"else if(((tool==='group'||tool==='select')||drawing?.combinedZone)&&drawing?.mode==='moveSelection'){const combined=!!drawing.combinedZone,moved=drawing.moved,picked=combined&&!moved?getObj(selection[0]):null;drawing=null;if(moved){changed();setHint(combined?'Zone moved · placement tool still active':(selectionState().allSame?'Grouped object moved':'Object moved'));setTimeout(hint,800)}else if(combined&&picked?.zone){const z=state.zones.find(o=>o.id===picked.zone);selected=picked.zone;state.activeZoneId=selected;renderZones();syncToolMenus();persist();draw();setHint('Zone '+(z?.number||'')+' picked · drag empty space to place it');setTimeout(hint,1000)}else draw();if(combined)return}",
'combined mode tap-to-pick')

INDEX.write_text(text,encoding='utf-8')
for rel in ['ZoneSketch.html','Zone-Sketch-by-Will.html','app/src/main/assets/index.html']:
    (ROOT/rel).write_text(text,encoding='utf-8')

gradle=ROOT/'app/build.gradle'
g=gradle.read_text(encoding='utf-8').replace('versionCode 63','versionCode 64').replace("versionName '0.62'","versionName '0.63'")
gradle.write_text(g,encoding='utf-8')

print('Applied Pineapple v0.63 Zone Plan quick-edit patch')
