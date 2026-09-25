from pathlib import Path
import re

MAIN = Path('index.html')
t = MAIN.read_text()


def once(old, new, label):
    global t
    if old in t:
        t = t.replace(old, new, 1)
    elif new not in t:
        raise SystemExit(f'v0.55 patch marker missing: {label}')


def sub_once(pattern, replacement, label):
    global t
    t2, n = re.subn(pattern, lambda m: replacement, t, count=1, flags=re.S)
    if n != 1:
        if replacement.strip() in t:
            return
        raise SystemExit(f'v0.55 regex marker missing: {label} ({n})')
    t = t2

# Visible product identity only. Historical feature comments remain on their original versions.
t = t.replace('Zone Sketch by Will Flood v0.54 —', 'Zone Sketch by Will Flood v0.55 —')
t = t.replace('ZONE SKETCH · v0.54', 'ZONE SKETCH · v0.55')
t = t.replace('BETA v0.54', 'BETA v0.55')
t = t.replace('<b>v0.54</b>', '<b>v0.55</b>')

# Survey now has a real field grid. It is not a disposable screen overlay: device positions are
# stored on this grid and Circuit Builder uses the same plan-space origin and spacing.
old_grid = """function gridStep(){return Math.max(2,Math.min(250,Number(state.gridSize)||100))}
function snapGridPoint(p){if(!state.snapGrid||!img)return p;const step=gridStep(),px=Math.round((p.x*img.width)/step)*step,py=Math.round((p.y*img.height)/step)*step;return{x:clamp(px/img.width),y:clamp(py/img.height)}}
function snapGridDelta(dx,dy){if(!state.snapGrid||!img)return{x:dx,y:dy};const gx=gridStep()/img.width,gy=gridStep()/img.height;return{x:Math.round(dx/gx)*gx,y:Math.round(dy/gy)*gy}}"""
new_grid = """function gridStep(){return Math.max(2,Math.min(250,Number(state.gridSize)||100))}
// v0.55 field grid — one plan-space grid shared by Survey and Circuit Builder.
function fieldGridPoint(p){if(!img)return p;const step=gridStep(),px=Math.round((p.x*img.width)/step)*step,py=Math.round((p.y*img.height)/step)*step;return{x:clamp(px/img.width),y:clamp(py/img.height)}}
function snapGridPoint(p){if(!state.snapGrid||!img)return p;return fieldGridPoint(p)}
function snapGridDelta(dx,dy){if(!state.snapGrid||!img)return{x:dx,y:dy};const gx=gridStep()/img.width,gy=gridStep()/img.height;return{x:Math.round(dx/gx)*gx,y:Math.round(dy/gy)*gy}}
function surveyFieldGridSymbols(){return(state.symbols||[]).filter(s=>s.type==='panel'||symbolScope(s)==='survey')}
function surveyFieldGridMisaligned(){if(!img)return 0;let n=0;for(const s of surveyFieldGridSymbols()){const q=fieldGridPoint(s);if(Math.hypot(q.x-s.x,q.y-s.y)>1e-8)n++;if(s.type==='beam'&&s.beamEnd){const b=fieldGridPoint(s.beamEnd);if(Math.hypot(b.x-s.beamEnd.x,b.y-s.beamEnd.y)>1e-8)n++}}return n}
function alignSurveyDevicesToFieldGrid(){if(!img)return 0;let moved=0;for(const s of surveyFieldGridSymbols()){const q=fieldGridPoint(s);if(Math.hypot(q.x-s.x,q.y-s.y)>1e-8){s.x=q.x;s.y=q.y;moved++}if(s.type==='beam'&&s.beamEnd){const b=fieldGridPoint(s.beamEnd);if(Math.hypot(b.x-s.beamEnd.x,b.y-s.beamEnd.y)>1e-8){s.beamEnd=b;moved++}}}if(moved)state.asFit=null;return moved}
function ensureSurveyFieldGrid(align=true){if(!img)return 0;const off=align?surveyFieldGridMisaligned():0,needs=!state.gridVisible||!state.snapGrid||off>0;if(!needs){syncGrid();return 0}push();state.gridVisible=true;state.snapGrid=true;const moved=align?alignSurveyDevicesToFieldGrid():0;changed();return moved}"""
once(old_grid, new_grid, 'shared field grid helpers')

# In Survey, pointer placement always uses the field grid. Hiding the grid only hides the lines;
# it does not silently put devices off-grid.
once(
    "function inputPoint(x,y){return snapGridPoint(point(x,y))}",
    "function inputPoint(x,y){const p=point(x,y);return surveyMode?fieldGridPoint(p):snapGridPoint(p)}",
    'survey input uses field grid',
)

# The Drawing-menu grid slider must also realign surveyed devices when changed while in Survey.
once(
    "$('gridSize').oninput=e=>{state.gridSize=Number(e.target.value);syncGrid();draw();persist()};",
    "$('gridSize').oninput=e=>{state.gridSize=Number(e.target.value);if(surveyMode){state.gridVisible=true;state.snapGrid=true;alignSurveyDevicesToFieldGrid()}syncGrid();draw();persist()};",
    'grid slider aligns survey devices',
)

# Survey controls: size remains adjustable, visual lines may be hidden, but device snapping is
# intentionally locked on so the later circuit game can always share exact intersections.
old_survey = """function syncSurveyTools(){if(!$('surveyUndo'))return;$('surveyUndo').disabled=!undo.length;$('surveyRedo').disabled=!redo.length;for(const [id,on] of [['surveySelect',!navMode&&tool==='select'],['surveyMove',!!state.gridVisible],['surveySnap',!!state.snapGrid],['surveyDelete',!navMode&&tool==='erase'],['surveyDevice',!navMode&&tool==='symbol'],['surveyRoom',!navMode&&tool==='layoutRect'],['surveyNote',!navMode&&tool==='pinNote']]){$(id).classList.toggle('active',on);$(id).setAttribute('aria-pressed',String(on))}const step=gridStep();$('surveyMove').textContent=(state.gridVisible?'Grid':'Grid off')+' · '+step;$('surveyGridDown').disabled=step<=SURVEY_GRID_STEPS[0];$('surveyGridUp').disabled=step>=SURVEY_GRID_STEPS[SURVEY_GRID_STEPS.length-1]}function changeSurveyGrid(direction){const current=gridStep(),steps=SURVEY_GRID_STEPS;let next;if(direction<0){next=[...steps].reverse().find(v=>v<current)??steps[0]}else next=steps.find(v=>v>current)??steps[steps.length-1];push();state.gridSize=next;state.gridVisible=true;state.snapGrid=true;changed();setHint('Survey grid '+next+' · snap ON');setTimeout(hint,800)}
function setSurveyMode(on){surveyMode=!!on;closeToolMenus();selection=[];syncSelectionBar();document.querySelector('.app').classList.toggle('surveyMode',surveyMode);$('surveyModeBtn').textContent=surveyMode?'Zone plan mode':'Survey mode';$('surveyModeBtn').setAttribute('aria-pressed',String(surveyMode));document.querySelector('.draftBadge').textContent=surveyMode?'SITE SURVEY · DEVICES':'PLAN / ZONE MAKER';syncModeUi();setMoveMode(false);if(surveyMode){symbolStamp='smoke';setTool('symbol')}renderSurveyDeviceFavourites();renderDeviceCounts();draw()}
$('surveyModeBtn').onclick=()=>setSurveyMode(!surveyMode);$('surveyGridDown').onclick=()=>changeSurveyGrid(-1);$('surveyGridUp').onclick=()=>changeSurveyGrid(1);$('surveyMove').onclick=()=>$('gridBtn').click();$('surveySnap').onclick=()=>$('snapGridBtn').click();"""
new_survey = """function syncSurveyTools(){if(!$('surveyUndo'))return;$('surveyUndo').disabled=!undo.length;$('surveyRedo').disabled=!redo.length;for(const [id,on] of [['surveySelect',!navMode&&tool==='select'],['surveyMove',!!state.gridVisible],['surveyDelete',!navMode&&tool==='erase'],['surveyDevice',!navMode&&tool==='symbol'],['surveyRoom',!navMode&&tool==='layoutRect'],['surveyNote',!navMode&&tool==='pinNote']]){$(id).classList.toggle('active',on);$(id).setAttribute('aria-pressed',String(on))}const step=gridStep();$('surveyMove').textContent=(state.gridVisible?'Field grid':'Grid hidden')+' · '+step;$('surveyGridDown').disabled=step<=SURVEY_GRID_STEPS[0];$('surveyGridUp').disabled=step>=SURVEY_GRID_STEPS[SURVEY_GRID_STEPS.length-1];$('surveySnap').textContent='Device snap · ON';$('surveySnap').classList.add('active');$('surveySnap').setAttribute('aria-pressed','true');$('surveySnap').disabled=true}function changeSurveyGrid(direction){const current=gridStep(),steps=SURVEY_GRID_STEPS;let next;if(direction<0){next=[...steps].reverse().find(v=>v<current)??steps[0]}else next=steps.find(v=>v>current)??steps[steps.length-1];push();state.gridSize=next;state.gridVisible=true;state.snapGrid=true;const moved=alignSurveyDevicesToFieldGrid();changed();setHint('Field grid '+next+' · device snap ON'+(moved?' · devices aligned':''));setTimeout(hint,900)}
function setSurveyMode(on){surveyMode=!!on;closeToolMenus();selection=[];syncSelectionBar();document.querySelector('.app').classList.toggle('surveyMode',surveyMode);$('surveyModeBtn').textContent=surveyMode?'Zone plan mode':'Survey mode';$('surveyModeBtn').setAttribute('aria-pressed',String(surveyMode));document.querySelector('.draftBadge').textContent=surveyMode?'SITE SURVEY · DEVICES':'PLAN / ZONE MAKER';if(surveyMode){const moved=ensureSurveyFieldGrid(true);if(moved)uiToast(moved+' surveyed point'+(moved===1?'':'s')+' aligned to field grid','success')}syncModeUi();setMoveMode(false);if(surveyMode){symbolStamp='smoke';setTool('symbol')}renderSurveyDeviceFavourites();renderDeviceCounts();draw()}
$('surveyModeBtn').onclick=()=>setSurveyMode(!surveyMode);$('surveyGridDown').onclick=()=>changeSurveyGrid(-1);$('surveyGridUp').onclick=()=>changeSurveyGrid(1);$('surveyMove').onclick=()=>$('gridBtn').click();$('surveySnap').onclick=()=>{};"""
once(old_survey, new_survey, 'constant survey field grid controls')

# Make initial copy self-explanatory before the first sync pass, and keep the locked control
# visually positive rather than looking unavailable/broken.
t = t.replace('title="Show or hide drawing grid">Grid · 100</button>', 'title="Show or hide the field grid; device snap stays on">Field grid · 100</button>', 1)
t = t.replace('<button id="surveySnap">Snap</button>', '<button id="surveySnap" disabled>Device snap · ON</button>', 1)
t = t.replace(
    '.app.surveyMode #surveyGridDown,.app.surveyMode #surveyGridUp{font-weight:800;background:#e5edf5}',
    '.app.surveyMode #surveyGridDown,.app.surveyMode #surveyGridUp{font-weight:800;background:#e5edf5}.app.surveyMode #surveySnap:disabled{opacity:1;background:#e7f7ee!important;color:#187144;border-color:#b9dec8}',
    1,
)

# If the user reaches Circuit Builder with an old/off-grid project, migrate the relevant survey
# symbols to the chosen field grid first. Existing routes then correctly show as stale and use
# the app's existing rebuild flow instead of retaining mismatched geometry.
old_open = "function openCircuitBuilder(){if(!img){uiNotice('Start a project first','Import a floor plan or start a blank floor before opening Circuit Builder.');return}syncFloor();cbCircuits();cbSyncChallengeBounds(true);closeToolMenus();"
new_open = "function openCircuitBuilder(){if(!img){uiNotice('Start a project first','Import a floor plan or start a blank floor before opening Circuit Builder.');return}const aligned=ensureSurveyFieldGrid(true);if(aligned)uiToast(aligned+' surveyed point'+(aligned===1?'':'s')+' aligned to field grid','success');syncFloor();cbCircuits();cbSyncChallengeBounds(true);closeToolMenus();"
once(old_open, new_open, 'align before Circuit Builder')

# Circuit Builder's visible grid is now the exact plan-space Survey grid, not a separate fixed
# 24-pixel screen grid. This works through crop, whole-floor challenge bounds, and pinch zoom.
new_route_grid = r'''// v0.55 shared Survey/Circuit field grid — same origin, same spacing, same device intersections.
function cbFieldGridScreenStep(bounds,w,h){if(!img||!bounds)return{x:CB_ROUTE_GRID*Math.max(1,cbView.scale),y:CB_ROUTE_GRID*Math.max(1,cbView.scale)};const step=gridStep(),a=cbPlanPx({x:0,y:0},bounds,w,h),bx=cbPlanPx({x:step/img.width,y:0},bounds,w,h),by=cbPlanPx({x:0,y:step/img.height},bounds,w,h);return{x:Math.max(4,Math.abs(bx.x-a.x)),y:Math.max(4,Math.abs(by.y-a.y))}}
function cbDrawRouteGrid(x,w,h){
 const bounds=cbCircuit?.bounds||cbSelectBounds;if(!img||!bounds)return;const step=gridStep(),x1=Math.max(0,Math.ceil(bounds.x1*img.width/step)*step),x2=Math.min(img.width,Math.floor(bounds.x2*img.width/step)*step),y1=Math.max(0,Math.ceil(bounds.y1*img.height/step)*step),y2=Math.min(img.height,Math.floor(bounds.y2*img.height/step)*step);
 x.save();x.beginPath();x.rect(18,18,w-36,h-36);x.clip();x.strokeStyle='#71869b';x.lineWidth=1;x.globalAlpha=.13;x.beginPath();
 for(let px=x1;px<=x2+.001;px+=step){const a=cbPlanPx({x:px/img.width,y:bounds.y1},bounds,w,h),b=cbPlanPx({x:px/img.width,y:bounds.y2},bounds,w,h);x.moveTo(a.x,a.y);x.lineTo(b.x,b.y)}
 for(let py=y1;py<=y2+.001;py+=step){const a=cbPlanPx({x:bounds.x1,y:py/img.height},bounds,w,h),b=cbPlanPx({x:bounds.x2,y:py/img.height},bounds,w,h);x.moveTo(a.x,a.y);x.lineTo(b.x,b.y)}
 x.stroke();x.restore()
}
'''
sub_once(r'// v0\.53 circuit grid routing — cable follows a visible orthogonal grid instead of every finger wobble\.\nfunction cbDrawRouteGrid\(x,w,h\)\{.*?\n\}\n(?=function cbGhost)', new_route_grid, 'shared route grid renderer')

old_snap = "function cbSnapPx(p,w,h){const q=cbPxBoardRaw(p,w,h),gx=CB_ROUTE_GRID/Math.max(1,w-56),gy=CB_ROUTE_GRID/Math.max(1,h-56);return cbBoardPx({x:clamp(Math.round(q.x/gx)*gx),y:clamp(Math.round(q.y/gy)*gy)},w,h)}"
new_snap = "function cbSnapPx(p,w,h){const bounds=cbCircuit?.bounds||cbSelectBounds||{x1:0,y1:0,x2:1,y2:1},board=cbPxBoardRaw(p,w,h),plan=cbBoardToPlan(board,bounds);return cbPlanPx(fieldGridPoint(plan),bounds,w,h)}"
once(old_snap, new_snap, 'circuit snap uses survey field grid')

once(
    "const pts=cbDrag.points,grid=Math.max(8,CB_ROUTE_GRID*Math.max(1,cbView.scale));",
    "const pts=cbDrag.points,cell=cbFieldGridScreenStep(cbCircuit?.bounds||cbSelectBounds,w,h),grid=Math.max(8,Math.min(cell.x,cell.y));",
    'turn threshold uses field grid cell',
)

# Make the shared grid visible in the game UI and explain that paired/retraced runs are based on
# the same Survey grid rather than a separate Circuit Builder lattice.
once(
    "pairBadge.textContent=blocked?'✕ NO CROSSING':pairMode&&cbDrag?.pairSnap?'⇄ CABLES PAIRED':challenge?'GRID · NO CROSSING':'⇄ TWIN CABLE SNAP'",
    "pairBadge.textContent=blocked?'✕ NO CROSSING':pairMode&&cbDrag?.pairSnap?'⇄ CABLES PAIRED':challenge?'GRID '+gridStep()+' · NO CROSSING':'⇄ TWIN CABLE · GRID '+gridStep()",
    'field grid badge',
)
t = t.replace('cable snaps to grid · retracing makes a parallel cable', 'cable uses Survey field grid · retracing makes a parallel cable')

# New regression joins the normal full suite only once this patch is applied by the release job.
r = Path('tests/run-regressions.cjs').read_text()
if "'circuit-survey-grid-v055'" not in r:
    r = r.replace("'circuit-zone-game-v054'", "'circuit-zone-game-v054','circuit-survey-grid-v055'")
Path('tests/run-regressions.cjs').write_text(r)

# Keep all main app entry points identical. The protected 24/7 company build is deliberately
# outside this list and is additionally checksum-locked by verify_247_protected.py.
for name in ['index.html', 'ZoneSketch.html', 'Zone-Sketch-by-Will.html', 'app/src/main/assets/index.html']:
    Path(name).write_text(t)

# Android release version.
g = Path('app/build.gradle').read_text()
g = g.replace('versionCode 55', 'versionCode 56').replace("versionName '0.54'", "versionName '0.55'")
Path('app/build.gradle').write_text(g)

assert 'v0.55 field grid' in t
assert 'function fieldGridPoint' in t
assert 'function cbFieldGridScreenStep' in t
assert 'return cbPlanPx(fieldGridPoint(plan),bounds,w,h)' in t
assert "'circuit-survey-grid-v055'" in r
print('Applied v0.55 shared Survey/Circuit field grid to main build only; 24/7 demo untouched')
