from pathlib import Path

ROOT = Path('.')
MAIN = ROOT / 'index.html'


def replace_once(text, old, new, label):
    if new in text and old not in text:
        return text
    if old not in text:
        raise SystemExit(f'v0.41 patch marker missing: {label}')
    return text.replace(old, new, 1)


text = MAIN.read_text()

# Version labels.
text = text.replace('v0.40', 'v0.41')

# Finer grid range. Keep the grid based on the source-plan pixel origin so the
# visible grid and the coordinates used for snapping are exactly the same.
text = replace_once(
    text,
    '<label class="wallControl" title="Grid spacing on the plan">Grid <input id="gridSize" type="range" min="5" max="250" step="5" value="100"><output id="gridSizeValue">100</output></label>',
    '<label class="wallControl" title="Grid spacing on the plan">Grid <input id="gridSize" type="range" min="2" max="250" step="1" value="100"><output id="gridSizeValue">100</output></label>',
    'top grid range'
)
text = replace_once(
    text,
    '<label for="surveyGridSize">Grid spacing</label><select id="surveyGridSize"><option value="5">Extra fine · 5</option><option value="10">10</option><option value="20">20</option><option value="40">Fine · 40</option><option value="50">50</option><option value="100">100</option><option value="200">Coarse · 200</option></select>',
    '<label for="surveyGridSize">Grid spacing</label><select id="surveyGridSize"><option value="2">Ultra fine · 2</option><option value="5">Extra fine · 5</option><option value="10">10</option><option value="20">20</option><option value="40">Fine · 40</option><option value="50">50</option><option value="100">100</option><option value="150">150</option><option value="200">Coarse · 200</option><option value="250">250</option></select>',
    'survey grid choices'
)
text = replace_once(
    text,
    'function gridStep(){return Math.max(5,Number(state.gridSize)||100)}',
    'function gridStep(){return Math.max(2,Math.min(250,Number(state.gridSize)||100))}',
    'grid step clamp'
)

# Give Survey mode proper - / + controls instead of making the engineer open
# another menu just to change spacing.
text = replace_once(
    text,
    '<nav id="surveyTools" aria-label="Survey tools"><button id="surveyMove" title="Show drawing grid">Grid</button><button id="surveySelect">Select / move</button>',
    '<nav id="surveyTools" aria-label="Survey tools"><button id="surveyGridDown" title="Make survey grid smaller">Grid −</button><button id="surveyMove" title="Show or hide drawing grid">Grid · 100</button><button id="surveyGridUp" title="Make survey grid larger">Grid +</button><button id="surveySelect">Select / move</button>',
    'survey grid controls'
)

# The current grid drawing already uses source-plan pixels. Make the snapping
# helper explicit and stable so every placement lands on the same intersections
# that are drawn on screen.
text = replace_once(
    text,
    "function snapGridPoint(p){if(!state.snapGrid||!img)return p;const step=gridStep();return{x:clamp(Math.round(p.x*img.width/step)*step/img.width),y:clamp(Math.round(p.y*img.height/step)*step/img.height)}}",
    "function snapGridPoint(p){if(!state.snapGrid||!img)return p;const step=gridStep(),px=Math.round((p.x*img.width)/step)*step,py=Math.round((p.y*img.height)/step)*step;return{x:clamp(px/img.width),y:clamp(py/img.height)}}",
    'exact grid point snapping'
)

# Moving a survey device used to snap only the movement delta. If a device was
# even slightly off-grid, that preserved the offset and felt random. In Survey
# mode snap the final anchor coordinate instead.
old_move = "else if((tool==='group'||tool==='select')&&drawing?.mode==='moveSelection'){const now=point(e.clientX,e.clientY),rawDelta=snapGridDelta(now.x-drawing.start.x,now.y-drawing.start.y),delta=boundedDelta(drawing.snap,rawDelta.x,rawDelta.y),dx=delta.x,dy=delta.y;if(!drawing.moved&&Math.hypot(dx,dy)>.003){push();drawing.moved=true}if(drawing.moved){for(const s of drawing.snap)shiftObj(s.ref,s.orig,dx,dy);draw()}}"
new_move = "else if((tool==='group'||tool==='select')&&drawing?.mode==='moveSelection'){const now=point(e.clientX,e.clientY),rawX=now.x-drawing.start.x,rawY=now.y-drawing.start.y;let rawDelta={x:rawX,y:rawY};if(surveyMode&&state.snapGrid&&drawing.snap.length){const anchor=drawing.snap.find(s=>s.ref.type==='symbols')?.orig||drawing.snap[0].orig;if(anchor&&Number.isFinite(anchor.x)&&Number.isFinite(anchor.y)){const snapped=snapGridPoint({x:anchor.x+rawX,y:anchor.y+rawY});rawDelta={x:snapped.x-anchor.x,y:snapped.y-anchor.y}}else rawDelta=snapGridDelta(rawX,rawY)}else rawDelta=snapGridDelta(rawX,rawY);const delta=boundedDelta(drawing.snap,rawDelta.x,rawDelta.y),dx=delta.x,dy=delta.y;if(!drawing.moved&&Math.hypot(dx,dy)>.003){push();drawing.moved=true}if(drawing.moved){for(const s of drawing.snap)shiftObj(s.ref,s.orig,dx,dy);draw()}}"
text = replace_once(text, old_move, new_move, 'survey absolute grid movement')

# Survey grid +/- behaviour. Changing the spacing from these buttons turns the
# grid and snap on because they are specifically Survey placement controls.
old_sync = "function syncSurveyTools(){if(!$('surveyUndo'))return;$('surveyUndo').disabled=!undo.length;$('surveyRedo').disabled=!redo.length;for(const [id,on] of [['surveySelect',!navMode&&tool==='select'],['surveyMove',!!state.gridVisible],['surveySnap',!!state.snapGrid],['surveyDelete',!navMode&&tool==='erase'],['surveyDevice',!navMode&&tool==='symbol'],['surveyRoom',!navMode&&tool==='layoutRect'],['surveyNote',!navMode&&tool==='pinNote']]){$(id).classList.toggle('active',on);$(id).setAttribute('aria-pressed',String(on))}}"
new_sync = "const SURVEY_GRID_STEPS=[2,5,10,20,40,50,100,150,200,250];function syncSurveyTools(){if(!$('surveyUndo'))return;$('surveyUndo').disabled=!undo.length;$('surveyRedo').disabled=!redo.length;for(const [id,on] of [['surveySelect',!navMode&&tool==='select'],['surveyMove',!!state.gridVisible],['surveySnap',!!state.snapGrid],['surveyDelete',!navMode&&tool==='erase'],['surveyDevice',!navMode&&tool==='symbol'],['surveyRoom',!navMode&&tool==='layoutRect'],['surveyNote',!navMode&&tool==='pinNote']]){$(id).classList.toggle('active',on);$(id).setAttribute('aria-pressed',String(on))}const step=gridStep();$('surveyMove').textContent=(state.gridVisible?'Grid':'Grid off')+' · '+step;$('surveyGridDown').disabled=step<=SURVEY_GRID_STEPS[0];$('surveyGridUp').disabled=step>=SURVEY_GRID_STEPS[SURVEY_GRID_STEPS.length-1]}function changeSurveyGrid(direction){const current=gridStep(),steps=SURVEY_GRID_STEPS;let next;if(direction<0){next=[...steps].reverse().find(v=>v<current)??steps[0]}else next=steps.find(v=>v>current)??steps[steps.length-1];push();state.gridSize=next;state.gridVisible=true;state.snapGrid=true;changed();setHint('Survey grid '+next+' · snap ON');setTimeout(hint,800)}"
text = replace_once(text, old_sync, new_sync, 'survey grid sync')
text = replace_once(
    text,
    "$('surveyModeBtn').onclick=()=>setSurveyMode(!surveyMode);$('surveyMove').onclick=()=>$('gridBtn').click();$('surveySnap').onclick=()=>$('snapGridBtn').click();",
    "$('surveyModeBtn').onclick=()=>setSurveyMode(!surveyMode);$('surveyGridDown').onclick=()=>changeSurveyGrid(-1);$('surveyGridUp').onclick=()=>changeSurveyGrid(1);$('surveyMove').onclick=()=>$('gridBtn').click();$('surveySnap').onclick=()=>$('snapGridBtn').click();",
    'survey grid button handlers'
)

# Close parallel walls in small rooms were being treated as if they were the
# same wall because 0.003 normalized units can be several source-image pixels.
# Use a source-pixel tolerance instead, which keeps true duplicates merged but
# never merges opposite walls in a small room.
text = replace_once(
    text,
    "function mergeOverlappingWalls(){const tol=.003,fixed=[],diag=[],hs=[],vs=[];",
    "function wallMergeTolerance(){const shortSide=Math.max(1,Math.min(img?.width||1600,img?.height||1000));return Math.min(.00075,1.25/shortSide)}\nfunction mergeOverlappingWalls(){const tol=wallMergeTolerance(),fixed=[],diag=[],hs=[],vs=[];",
    'safe wall merge tolerance'
)

# Roller-shutter hatch depth was clamped to a minimum screen-pixel size. That
# made the shutter look physically wider as the drawing was zoomed out. Scale
# the hatch depth from the shutter's current on-screen length instead.
old_shutter = "function drawShutter(c,a,b,width=2,color='#172333'){const dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy);if(L<2)return;const nx=-dy/L,ny=dx/L,tick=Math.max(3,width*1.7),count=Math.max(4,Math.min(14,Math.round(L/13)));c.save();c.strokeStyle=color;c.lineWidth=Math.max(.8,width*.42);c.lineCap='round';c.beginPath();c.moveTo(a.x,a.y);c.lineTo(b.x,b.y);c.stroke();for(let i=0;i<=count;i++){const t=i/count,x=a.x+dx*t,y=a.y+dy*t;c.beginPath();c.moveTo(x-nx*tick,y-ny*tick);c.lineTo(x+nx*tick,y+ny*tick);c.stroke()}c.restore()}"
new_shutter = "function shutterVisualMetrics(length){const L=Math.max(0,Number(length)||0),tick=Math.max(.45,Math.min(5.5,L*.055)),count=Math.max(3,Math.min(16,Math.round(L/10)));return{tick,count}}\nfunction drawShutter(c,a,b,width=2,color='#172333'){const dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy);if(L<2)return;const nx=-dy/L,ny=dx/L,{tick,count}=shutterVisualMetrics(L);c.save();c.strokeStyle=color;c.lineWidth=Math.max(.65,width*.42);c.lineCap='round';c.beginPath();c.moveTo(a.x,a.y);c.lineTo(b.x,b.y);c.stroke();for(let i=0;i<=count;i++){const t=i/count,x=a.x+dx*t,y=a.y+dy*t;c.beginPath();c.moveTo(x-nx*tick,y-ny*tick);c.lineTo(x+nx*tick,y+ny*tick);c.stroke()}c.restore()}"
text = replace_once(text, old_shutter, new_shutter, 'roller shutter zoom scaling')

# Keep the Survey toolbar usable with the extra two grid buttons.
extra_css = """
/* v0.41 — exact survey grid controls and object zoom stability. */
.app.surveyMode #surveyTools{grid-template-columns:repeat(9,minmax(0,1fr))}
.app.surveyMode #surveyGridDown,.app.surveyMode #surveyGridUp{font-weight:800;background:#e5edf5}
@media(max-width:600px){.app.surveyMode #surveyTools{grid-template-columns:repeat(3,minmax(0,1fr))}}
"""
if '/* v0.41 — exact survey grid controls and object zoom stability. */' not in text:
    text = text.replace('</style>', extra_css + '\n</style>', 1)

# Android version.
gradle = Path('app/build.gradle').read_text()
gradle = gradle.replace('versionCode 41', 'versionCode 42').replace("versionName '0.40'", "versionName '0.41'")
Path('app/build.gradle').write_text(gradle)

# Keep every app copy byte-identical.
MAIN.write_text(text)
for path in ['ZoneSketch.html', 'Zone-Sketch-by-Will.html', 'app/src/main/assets/index.html']:
    Path(path).write_text(text)

print('Applied v0.41: exact Survey grid snapping, safe small-room walls, stable roller shutter zoom')
