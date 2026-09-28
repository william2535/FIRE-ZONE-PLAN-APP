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

# Visible version for the focused Zone Plan build-mode milestone.
text=text.replace('v0.61','v0.62')
text=text.replace('ZONE SKETCH · v0.58','ZONE SKETCH · v0.62')

# Build mode is a project preference (not floor data): ON keeps placement and moving separate,
# OFF lets zone tools place on empty space or drag an existing zone without changing tools.
replace_once(
"activeZoneId:null,pictureOpacity:1",
"activeZoneId:null,buildMode:true,pictureOpacity:1",
'fresh build mode default')
replace_once(
"function ensureUiState(){state.locks={...defaultLocks(),...(state.locks||{})};state.layers={...defaultLayers(),...(state.layers||{})}}",
"function ensureUiState(){state.locks={...defaultLocks(),...(state.locks||{})};state.layers={...defaultLayers(),...(state.layers||{})};if(typeof state.buildMode!=='boolean')state.buildMode=true}",
'ensure build mode default')

replace_once(
"<button id=\"gridBtn\">Grid off</button><button id=\"snapGridBtn\">Snap off</button>",
"<button id=\"gridBtn\">Grid off</button><button id=\"snapGridBtn\">Snap off</button><button id=\"buildModeBtn\" class=\"toggleItem active\" aria-pressed=\"true\" title=\"Build mode ON keeps zone placement and moving separate\"><span>Build mode</span><span>ON · Separate</span></button>",
'build mode control markup')
replace_once(
"<div id=\"settingsMenu\" class=\"toolPopup\" aria-label=\"Drawing settings\"><h4>Drawing settings</h4><div id=\"drawingActions\" class=\"menuRow\"></div><div id=\"drawingSliders\"></div></div>",
"<div id=\"settingsMenu\" class=\"toolPopup\" aria-label=\"Drawing settings\"><h4>Drawing settings</h4><div id=\"drawingActions\" class=\"menuRow\"></div><div id=\"buildModeHelp\" class=\"menuHint\">Build mode ON keeps placing and moving separate. Turn it OFF on smaller plans to drag an existing zone while the current zone tool stays ready to place.</div><div id=\"drawingSliders\"></div></div>",
'build mode drawing help')
replace_once(
"for(const id of ['gridBtn','snapGridBtn'])$('drawingActions').append($(id));",
"for(const id of ['gridBtn','snapGridBtn','buildModeBtn'])$('drawingActions').append($(id));",
'build mode drawing menu placement')

replace_once(
"function clearSelection(){selection=[];syncSelectionBar();draw()}\nfunction syncMoveMode(){",
"function clearSelection(){selection=[];syncSelectionBar();draw()}\nfunction syncBuildMode(){ensureUiState();const b=$('buildModeBtn'),on=state.buildMode!==false;if(!b)return;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on));b.firstElementChild.textContent='Build mode';b.lastElementChild.textContent=on?'ON · Separate':'OFF · Place + move';b.title=on?'Build mode ON · zone placement and moving are separate':'Build mode OFF · drag an existing zone to move it while zone placement stays active';const h=$('buildModeHelp');if(h)h.textContent=on?'Build mode ON keeps placing and moving separate. Best for larger plans where deliberate tools prevent accidental moves.':'Build mode OFF combines zone placement + moving. Drag inside an existing zone to move it; drag empty space to place with the current zone tool.'}\nfunction setBuildMode(on){ensureUiState();state.buildMode=!!on;selection=[];drawing=null;syncSelectionBar();persist();syncBuildMode();draw();closeToolMenus();uiToast(state.buildMode?'Build mode ON · placement and moving are separate':'Build mode OFF · place + move zones together','success')}\nfunction syncMoveMode(){",
'build mode state helpers')

replace_once(
"function syncModeUi(){$('rotateCanvas').disabled=surveyMode;",
"function syncModeUi(){syncBuildMode();$('rotateCanvas').disabled=surveyMode;",
'build mode mode-sync')

# When combined mode is enabled, only an existing zone polygon is intercepted. Walls and other
# geometry remain untouched so starting a zone near a building wall still behaves predictably.
replace_once(
"function selectByScreenRect(a,b){const x1=Math.min(a.x,b.x),x2=Math.max(a.x,b.x),y1=Math.min(a.y,b.y),y2=Math.max(a.y,b.y),v=transform(),toScreen=p=>({x:v.ox+p.x*img.width*v.s,y:v.oy+p.y*img.height*v.s}),picked=[];for(const ref of allRefs()){if(!refVisible(ref)||isRefLocked(ref))continue;const bb=itemBounds(ref);if(!bb)continue;const p1=toScreen({x:bb.x1,y:bb.y1}),p2=toScreen({x:bb.x2,y:bb.y2}),ix1=Math.min(p1.x,p2.x),ix2=Math.max(p1.x,p2.x),iy1=Math.min(p1.y,p2.y),iy2=Math.max(p1.y,p2.y);if(ix2>=x1&&ix1<=x2&&iy2>=y1&&iy1<=y2)picked.push(ref)}selection=picked;syncSelectionBar()}\ncanvas.onpointerdown=e=>{",
"function selectByScreenRect(a,b){const x1=Math.min(a.x,b.x),x2=Math.max(a.x,b.x),y1=Math.min(a.y,b.y),y2=Math.max(a.y,b.y),v=transform(),toScreen=p=>({x:v.ox+p.x*img.width*v.s,y:v.oy+p.y*img.height*v.s}),picked=[];for(const ref of allRefs()){if(!refVisible(ref)||isRefLocked(ref))continue;const bb=itemBounds(ref);if(!bb)continue;const p1=toScreen({x:bb.x1,y:bb.y1}),p2=toScreen({x:bb.x2,y:bb.y2}),ix1=Math.min(p1.x,p2.x),ix2=Math.max(p1.x,p2.x),iy1=Math.min(p1.y,p2.y),iy2=Math.max(p1.y,p2.y);if(ix2>=x1&&ix1<=x2&&iy2>=y1&&iy1<=y2)picked.push(ref)}selection=picked;syncSelectionBar()}\nfunction combinedZoneAt(clientX,clientY){if(surveyMode||state.buildMode!==false||!zoneTools.has(tool)||state.locks?.zones)return null;const p=point(clientX,clientY);for(let i=state.shapes.length-1;i>=0;i--){const o=state.shapes[i],ref={type:'shapes',id:o.id};if(refVisible(ref)&&!isRefLocked(ref)&&Array.isArray(o.points)&&o.points.length>=3&&pointInPoly(p,o.points))return ref}return null}\ncanvas.onpointerdown=e=>{",
'combined zone hit helper')

replace_once(
"if(lockedReason){setHint(lockedReason+' · use the Locks menu to unlock it');setTimeout(hint,1300);return}if(tool==='joinWalls')",
"if(lockedReason){setHint(lockedReason+' · use the Locks menu to unlock it');setTimeout(hint,1300);return}const combinedHit=combinedZoneAt(e.clientX,e.clientY);if(combinedHit){selection=[combinedHit];syncSelectionBar();drawing={mode:'moveSelection',start:point(e.clientX,e.clientY),snap:snapshotSelection(),moved:false,combinedZone:true};setHint('Place + move · drag this zone to move it · drag empty space to place');draw();return}if(tool==='joinWalls')",
'combined zone pointer down')

# A combined move still uses a zone placement tool such as rect. Keep the normal rect preview/move/up
# handlers from stealing that gesture before the move-selection branch gets it.
replace_once(
"if(!surveyMode&&state.layers.zones!==false){const zonePaint=state.shapes.slice();if(!navMode&&drawing&&tool==='rect'&&selected){",
"if(!surveyMode&&state.layers.zones!==false){const zonePaint=state.shapes.slice();if(!navMode&&drawing&&!drawing.combinedZone&&tool==='rect'&&selected){",
'combined zone rect preview guard')
replace_once(
"else if(tool==='rect'&&drawing){drawing.now=snapZoneCorner(inputPoint(e.clientX,e.clientY));draw()}",
"else if(tool==='rect'&&drawing&&!drawing.combinedZone){drawing.now=snapZoneCorner(inputPoint(e.clientX,e.clientY));draw()}",
'combined zone rect pointer-move guard')
replace_once(
"if(tool==='rect'&&drawing){const a=drawing.start,b=snapZoneCorner(inputPoint(e.clientX,e.clientY));",
"if(tool==='rect'&&drawing&&!drawing.combinedZone){const a=drawing.start,b=snapZoneCorner(inputPoint(e.clientX,e.clientY));",
'combined zone rect pointer-up guard')

replace_once(
"else if((tool==='group'||tool==='select')&&drawing?.mode==='moveSelection'){const now=point(e.clientX,e.clientY)",
"else if(((tool==='group'||tool==='select')||drawing?.combinedZone)&&drawing?.mode==='moveSelection'){const now=point(e.clientX,e.clientY)",
'combined zone pointer move')
replace_once(
"else if((tool==='group'||tool==='select')&&drawing?.mode==='moveSelection'){const moved=drawing.moved;drawing=null;if(moved){changed();setHint(selectionState().allSame?'Grouped object moved':'Object moved');setTimeout(hint,800)}else draw()}",
"else if(((tool==='group'||tool==='select')||drawing?.combinedZone)&&drawing?.mode==='moveSelection'){const combined=!!drawing.combinedZone,moved=drawing.moved;drawing=null;if(moved){changed();setHint(combined?'Zone moved · placement tool still active':(selectionState().allSame?'Grouped object moved':'Object moved'));setTimeout(hint,800)}else draw();if(combined)return}",
'combined zone pointer up')
replace_once(
"if(tool==='group'||tool==='select')drawSelection(ctx,map)",
"if(tool==='group'||tool==='select'||(!surveyMode&&state.buildMode===false&&zoneTools.has(tool)&&selection.some(r=>r.type==='shapes')))drawSelection(ctx,map)",
'combined zone selection drawing')

replace_once(
"$('topCollapseBtn').onclick=()=>setTopSection(!topSectionOpen);$('moveModeTop').onclick=()=>setMoveMode(!navMode);$('moveModeBottom').onclick=()=>setMoveMode(!navMode);syncZonesPanel();syncTopSection();syncMoveMode();",
"$('topCollapseBtn').onclick=()=>setTopSection(!topSectionOpen);$('moveModeTop').onclick=()=>setMoveMode(!navMode);$('moveModeBottom').onclick=()=>setMoveMode(!navMode);$('buildModeBtn').onclick=()=>setBuildMode(state.buildMode===false);syncZonesPanel();syncTopSection();syncBuildMode();syncMoveMode();",
'build mode click binding')

INDEX.write_text(text,encoding='utf-8')
for rel in ['ZoneSketch.html','Zone-Sketch-by-Will.html','app/src/main/assets/index.html']:
    (ROOT/rel).write_text(text,encoding='utf-8')

gradle=ROOT/'app/build.gradle'
g=gradle.read_text(encoding='utf-8').replace('versionCode 62','versionCode 63').replace("versionName '0.61'","versionName '0.62'")
gradle.write_text(g,encoding='utf-8')

print('Applied Pineapple v0.62 Zone Plan build-mode patch')
