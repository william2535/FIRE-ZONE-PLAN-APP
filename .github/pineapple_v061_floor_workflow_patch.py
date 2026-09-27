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

# Visible app version for this focused floor workflow milestone.
text=text.replace('v0.60','v0.61')
text=text.replace('ZONE SKETCH · v0.58','ZONE SKETCH · v0.61')

# Keep the selected zone with each floor, and make the floor snapshot authoritative immediately.
replace_once(
"const fresh=()=>({site:'',meta:{drawingRef:'',revision:'',surveyedBy:'',surveyDate:''},zones:[],shapes:[],notes:[],walls:[],doors:[],windows:[],shutters:[],stairs:[],labels:[],symbols:[],pins:[],circuits:[],asFit:null,pictureOpacity:1,pictureVisible:true,pictureBrightness:1,pictureContrast:1,pictureGrayscale:0,isBlank:false,gridVisible:false,snapGrid:false,gridSize:100,wallWidth:3,locks:{background:false,building:false,zones:false},layers:{background:true,building:true,zones:true,symbols:true,labels:true,notes:true,grid:true}});",
"const fresh=()=>({site:'',meta:{drawingRef:'',revision:'',surveyedBy:'',surveyDate:''},zones:[],shapes:[],notes:[],walls:[],doors:[],windows:[],shutters:[],stairs:[],labels:[],symbols:[],pins:[],circuits:[],asFit:null,activeZoneId:null,pictureOpacity:1,pictureVisible:true,pictureBrightness:1,pictureContrast:1,pictureGrayscale:0,isBlank:false,gridVisible:false,snapGrid:false,gridSize:100,wallWidth:3,locks:{background:false,building:false,zones:false},layers:{background:true,building:true,zones:true,symbols:true,labels:true,notes:true,grid:true}});",
'fresh activeZoneId')
replace_once(
"const floorKeys=['zones','shapes','notes','walls','doors','windows','shutters','stairs','labels','symbols','pins','circuits','asFit','pictureOpacity','pictureVisible','pictureBrightness','pictureContrast','pictureGrayscale','isBlank','gridVisible','snapGrid','gridSize','wallWidth','locks','layers','image'];",
"const floorKeys=['zones','shapes','notes','walls','doors','windows','shutters','stairs','labels','symbols','pins','circuits','asFit','activeZoneId','pictureOpacity','pictureVisible','pictureBrightness','pictureContrast','pictureGrayscale','isBlank','gridVisible','snapGrid','gridSize','wallWidth','locks','layers','image'];",
'floor keys active zone')
replace_once(
"function syncFloor(){activeFloor().data=floorData()}",
"function syncFloor(){state.activeZoneId=selected||null;activeFloor().data=floorData()}",
'syncFloor selected zone')
replace_once(
"function resetInteraction(){selection=[];selected=state.zones[0]?.id||null;poly=[];drawing=null;pointers.clear();pinchIds.clear();gesture=null;opacityEditing=false;cleanupEditing=false;snapGuide=null;zoom=1;pan={x:0,y:0};closeToolMenus()}",
"function resetInteraction(){selection=[];selected=state.activeZoneId&&state.zones.some(z=>z.id===state.activeZoneId)?state.activeZoneId:(state.zones[0]?.id||null);state.activeZoneId=selected||null;poly=[];drawing=null;pointers.clear();pinchIds.clear();gesture=null;opacityEditing=false;cleanupEditing=false;snapGuide=null;zoom=1;pan={x:0,y:0};closeToolMenus()}",
'restore selected zone per floor')
replace_once(
"function changed(){if(typeof cbInvalidateSymbolIndex==='function')cbInvalidateSymbolIndex();syncBackground();",
"function changed(){syncFloor();if(typeof cbInvalidateSymbolIndex==='function')cbInvalidateSymbolIndex();syncBackground();",
'immediate floor snapshot')

# Make Circuit Builder explicitly floor-aware from every sub-screen.
replace_once(
"<header class=\"cbTop\"><div><strong>CIRCUIT BUILDER</strong><small>BY WILL FLOOD · ZONE PLAN + SURVEY → WIRING → AS-FIT</small></div><div class=\"cbGrow\"></div><button id=\"cbSoundToggle\" aria-pressed=\"true\" title=\"Toggle Circuit Builder sounds\">Sound on</button><button id=\"cbBack\">Back to plan</button></header>",
"<header class=\"cbTop\"><div><strong>CIRCUIT BUILDER</strong><small>BY WILL FLOOD · ZONE PLAN + SURVEY → WIRING → AS-FIT</small></div><div class=\"cbGrow\"></div><label class=\"cbFloorSwitch\" for=\"cbFloorSelect\"><span>Floor</span><select id=\"cbFloorSelect\" aria-label=\"Circuit Builder floor\"></select></label><button id=\"cbSoundToggle\" aria-pressed=\"true\" title=\"Toggle Circuit Builder sounds\">Sound on</button><button id=\"cbBack\">Back to plan</button></header>",
'circuit floor selector markup')

css="""
.cbFloorSwitch{display:flex;align-items:center;gap:7px;padding:5px 7px 5px 10px;border:1px solid #ffffff26;border-radius:11px;background:#ffffff0d;color:#cbd9e7;font-size:11px;font-weight:800;letter-spacing:.05em;text-transform:uppercase}.cbFloorSwitch select{max-width:220px;min-width:132px;border:0;border-radius:8px;padding:8px 28px 8px 10px;background:#f8fbff;color:#1b3046;font-size:13px;font-weight:800;text-transform:none;letter-spacing:0}.cbFloorSwitch select:disabled{opacity:.72}.cbFloorSwitch select:focus-visible{outline:3px solid #83b8e7;outline-offset:2px}@media(max-width:720px){.cbTop{gap:6px;align-items:center;flex-wrap:wrap}.cbTop>div:first-child small{display:none}.cbTop>.cbGrow{display:none}.cbFloorSwitch{order:10;flex:1 0 100%;width:100%;min-width:0;justify-content:space-between}.cbFloorSwitch select{flex:1;max-width:none;min-width:0}.cbTop #cbBack,.cbTop #cbSoundToggle{padding:8px 10px}.cbTop>div:first-child{margin-right:auto}}
"""
replace_once('</style>\n</head>',css+'</style>\n</head>','circuit floor selector css')

floor_functions="""
function cbRenderFloorSelect(){const select=$('cbFloorSelect');if(!select)return;ensureFloors();const focus=document.activeElement===select;select.textContent='';for(const f of state.floors){const o=document.createElement('option');o.value=f.id;o.textContent=f.name;select.append(o)}select.value=state.activeFloor;select.disabled=state.floors.length<2;select.title=state.floors.length<2?'Add another floor in Plan / Zone Maker to switch here.':'Switch Circuit Builder to another floor';if(focus)select.focus()}
async function cbSwitchFloor(id){if(!id||id===state.activeFloor){cbRenderFloorSelect();return}cbCheckpointDrag(true);cbHideCelebrate();syncFloor();cbCircuit=null;cbSelection.clear();cbEdit=null;cbDrag=null;cbHover=null;cbEditSyncUi();await showFloor(id);const aligned=ensureSurveyFieldGrid(true);cbSyncChallengeBounds(true);cbResetView(false);cbShow('home');if(aligned)uiToast(aligned+' surveyed point'+(aligned===1?'':'s')+' aligned on '+activeFloor().name,'success');else uiToast(activeFloor().name+' loaded in Circuit Builder','success')}
"""
replace_once('function cbRenderLanding(){',floor_functions+'function cbRenderLanding(){','circuit floor functions')
replace_once(
"function cbShow(screen){cbCheckpointDrag(true);cbHideCelebrate();cbScreen=screen;",
"function cbShow(screen){cbCheckpointDrag(true);cbHideCelebrate();cbRenderFloorSelect();cbScreen=screen;",
'cbShow floor sync')
replace_once(
"function openCircuitBuilder(){if(!img){uiNotice('Start a project first','Import a floor plan or start a blank floor before opening Circuit Builder.');return}const aligned=ensureSurveyFieldGrid(true);if(aligned)uiToast(aligned+' surveyed point'+(aligned===1?'':'s')+' aligned to field grid','success');syncFloor();cbCircuits();cbSyncChallengeBounds(true);closeToolMenus();$('circuitBuilder').hidden=false;document.querySelector('.app').inert=true;cbCircuit=null;cbSelection.clear();cbShow('home')}",
"function openCircuitBuilder(){if(!img){uiNotice('Start a project first','Import a floor plan or start a blank floor before opening Circuit Builder.');return}const aligned=ensureSurveyFieldGrid(true);if(aligned)uiToast(aligned+' surveyed point'+(aligned===1?'':'s')+' aligned to field grid','success');syncFloor();cbCircuits();cbSyncChallengeBounds(true);closeToolMenus();$('circuitBuilder').hidden=false;document.querySelector('.app').inert=true;cbCircuit=null;cbSelection.clear();cbRenderFloorSelect();cbShow('home')}",
'open circuit builder floor selector')
replace_once(
"$('circuitModeBtn').onclick=openCircuitBuilder;",
"$('cbFloorSelect').onchange=e=>cbSwitchFloor(e.target.value);$('circuitModeBtn').onclick=openCircuitBuilder;",
'circuit floor onchange')

# Make the existing floor switch path explicit about saving the outgoing floor before loading the next one.
replace_once(
"b.onclick=async()=>{closeToolMenus();if(f.id===state.activeFloor)return;push();await showFloor(f.id)};",
"b.onclick=async()=>{closeToolMenus();if(f.id===state.activeFloor)return;push();syncFloor();await showFloor(f.id)};",
'floor menu outgoing snapshot')
replace_once(
"$('floorSelect').onchange=async e=>{const id=e.target.value;push();await showFloor(id)};",
"$('floorSelect').onchange=async e=>{const id=e.target.value;push();syncFloor();await showFloor(id)};",
'floor select outgoing snapshot')

INDEX.write_text(text,encoding='utf-8')
# Keep all packaged HTML copies byte-for-byte aligned.
for rel in ['ZoneSketch.html','Zone-Sketch-by-Will.html','app/src/main/assets/index.html']:
    (ROOT/rel).write_text(text,encoding='utf-8')

# Android app version for v0.61.
gradle=ROOT/'app/build.gradle'
g=gradle.read_text(encoding='utf-8').replace('versionCode 61','versionCode 62').replace("versionName '0.60'","versionName '0.61'")
gradle.write_text(g,encoding='utf-8')

print('Applied Pineapple v0.61 floor workflow patch')
