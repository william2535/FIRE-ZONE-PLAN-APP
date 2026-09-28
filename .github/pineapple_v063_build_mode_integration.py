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

# v0.63 is a focused correction to the v0.62 Build mode interaction model.
text=text.replace('v0.62','v0.63')
text=text.replace('ZONE SKETCH · <b>v0.58</b>','ZONE SKETCH · <b>v0.63</b>')

replace_once(
'<button id="moveModeTop" title="When on, the canvas only pans/zooms and cannot edit">Move OFF</button>',
'<button id="moveModeTop" title="Pan mode · when on, one-finger drags navigate instead of editing">Pan OFF</button>',
'pan control label')

replace_once(
'<div id="buildModeHelp" class="menuHint">Build mode ON keeps placing and moving separate. Turn it OFF on smaller plans to drag an existing zone while the current zone tool stays ready to place.</div>',
'<div id="buildModeHelp" class="menuHint">Build mode ON keeps placing and moving separate. Turn it OFF on smaller plans for Place + move; one-finger Pan is then disabled so it cannot override the combined workflow.</div>',
'build mode help')

old_helpers="""function syncBuildMode(){ensureUiState();const b=$('buildModeBtn'),on=state.buildMode!==false;if(!b)return;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on));b.firstElementChild.textContent='Build mode';b.lastElementChild.textContent=on?'ON · Separate':'OFF · Place + move';b.title=on?'Build mode ON · zone placement and moving are separate':'Build mode OFF · drag an existing zone to move it while zone placement stays active';const h=$('buildModeHelp');if(h)h.textContent=on?'Build mode ON keeps placing and moving separate. Best for larger plans where deliberate tools prevent accidental moves.':'Build mode OFF combines zone placement + moving. Drag inside an existing zone to move it; drag empty space to place with the current zone tool.'}
function setBuildMode(on){ensureUiState();state.buildMode=!!on;selection=[];drawing=null;syncSelectionBar();persist();syncBuildMode();draw();closeToolMenus();uiToast(state.buildMode?'Build mode ON · placement and moving are separate':'Build mode OFF · place + move zones together','success')}
function syncMoveMode(){syncSurveyTools();for(const id of ['moveModeTop','moveModeBottom']){const b=$(id);if(!b)continue;b.classList.toggle('active',navMode);b.textContent=id==='moveModeTop'?(navMode?'Move ON':'Move OFF'):(navMode?'✋ Move ON':'✋ Move mode')}document.querySelector('.app')?.classList.toggle('moveModeActive',navMode)}
function setMoveMode(on){navMode=!!on;drawing=null;gesture=null;pointers.clear();pinchIds.clear();if(navMode){selection=[];syncSelectionBar();closeToolMenus();setHint('Move mode ON · drag or pinch the plan · drawing taps are disabled')}else hint();syncMoveMode();draw()}"""
new_helpers="""function combinedBuildMode(){ensureUiState();return !surveyMode&&state.buildMode===false}
function syncBuildMode(){ensureUiState();const b=$('buildModeBtn'),on=state.buildMode!==false;if(!b)return;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on));b.firstElementChild.textContent='Build mode';b.lastElementChild.textContent=on?'ON · Separate':'OFF · Place + move';b.title=on?'Build mode ON · zone placement and moving are separate':'Build mode OFF · drag an existing zone to move it while zone placement stays active';const h=$('buildModeHelp');if(h)h.textContent=on?'Build mode ON keeps placing and moving separate. Best for larger plans where deliberate tools prevent accidental moves.':'Build mode OFF combines zone placement + moving. One-finger Pan is disabled so it cannot override this mode; drag an existing zone to move it, drag empty space to place, and use two fingers or the zoom controls to navigate.'}
function setBuildMode(on){ensureUiState();state.buildMode=!!on;if(combinedBuildMode()){navMode=false;gesture=null;pointers.clear();pinchIds.clear()}selection=[];drawing=null;syncSelectionBar();persist();syncBuildMode();syncMoveMode();draw();closeToolMenus();uiToast(state.buildMode?'Build mode ON · placement and moving are separate':'Build mode OFF · Place + move active · Pan cannot override it','success')}
function syncMoveMode(){syncSurveyTools();const combined=combinedBuildMode();if(combined&&navMode)navMode=false;for(const id of ['moveModeTop','moveModeBottom']){const b=$(id);if(!b)continue;b.disabled=combined;b.classList.toggle('active',!combined&&navMode);if(id==='moveModeTop')b.textContent=combined?'Pan · 2 fingers':(navMode?'Pan ON':'Pan OFF');else b.textContent=combined?'✋ Place + move':(navMode?'✋ Pan ON':'✋ Pan mode');b.title=combined?'Build mode OFF already combines placement and moving. Use two fingers or the zoom controls to navigate.':'Pan mode · when on, one-finger drags navigate instead of editing'}document.querySelector('.app')?.classList.toggle('moveModeActive',!combined&&navMode)}
function setMoveMode(on){if(combinedBuildMode()){navMode=false;drawing=null;gesture=null;pointers.clear();pinchIds.clear();syncMoveMode();setHint('Place + move is active · Pan cannot override it · use two fingers or zoom controls to navigate');setTimeout(hint,1400);draw();return}navMode=!!on;drawing=null;gesture=null;pointers.clear();pinchIds.clear();if(navMode){selection=[];syncSelectionBar();closeToolMenus();setHint('Pan mode ON · drag or pinch the plan · drawing taps are disabled')}else hint();syncMoveMode();draw()}"""
replace_once(old_helpers,new_helpers,'integrated build/pan helpers')

replace_once(
"function combinedZoneAt(clientX,clientY){if(surveyMode||state.buildMode!==false||!zoneTools.has(tool)||state.locks?.zones)return null;",
"function combinedZoneAt(clientX,clientY){if(!combinedBuildMode()||!zoneTools.has(tool)||state.locks?.zones)return null;",
'combined build predicate')

# In combined mode, two fingers are the navigation escape hatch. In separated mode the historical
# safety behaviour remains: adding a second touch cancels an in-progress Zone Plan edit.
replace_once(
"if(pointers.size>=2){if(!surveyMode&&!navMode){const contacts=[...pointers.entries()];cancelGesture();for(const [id,p] of contacts){pointers.set(id,p);pinchIds.add(id)}return}if(pointers.size===2){",
"if(pointers.size>=2){if(!surveyMode&&!navMode&&!combinedBuildMode()){const contacts=[...pointers.entries()];cancelGesture();for(const [id,p] of contacts){pointers.set(id,p);pinchIds.add(id)}return}if(pointers.size===2){",
'two-finger combined navigation')

INDEX.write_text(text,encoding='utf-8')
for rel in ['ZoneSketch.html','Zone-Sketch-by-Will.html','app/src/main/assets/index.html']:
    (ROOT/rel).write_text(text,encoding='utf-8')

gradle=ROOT/'app/build.gradle'
g=gradle.read_text(encoding='utf-8').replace('versionCode 63','versionCode 64').replace("versionName '0.62'","versionName '0.63'")
gradle.write_text(g,encoding='utf-8')

print('Applied Pineapple v0.63 Build mode / Pan integration fix')
