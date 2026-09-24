from pathlib import Path
import re

p=Path('index.html')
t=p.read_text()

def once(old,new,label):
    global t
    if new in t and old not in t:
        return
    if old not in t:
        raise SystemExit(f'v0.45 patch marker missing: {label}')
    t=t.replace(old,new,1)

if 'v0.45 — Circuit Builder zoom + continuous drag' not in t:
    t=t.replace('v0.44','v0.45')

    css=r'''
/* v0.45 — Circuit Builder zoom + continuous drag. */
.cbZoomDock{position:absolute;right:10px;bottom:10px;z-index:5;display:flex;gap:5px;padding:5px;border:1px solid #cad6e1;border-radius:12px;background:#fffffff2;box-shadow:0 4px 16px #16283e20;backdrop-filter:blur(5px)}
.cbZoomDock button{min-width:38px;min-height:36px;padding:6px 9px;background:#edf2f7;font-size:15px}.cbZoomDock .fit{font-size:11px;min-width:44px}
.cbActions .complete{background:#c73d36;color:#fff}.cbActions .complete.ready{background:#25834e;color:#fff}
@media(max-width:600px){.cbZoomDock{right:6px;bottom:6px}.cbZoomDock button{min-width:40px;min-height:40px}}
'''
    t=t.replace('</style>',css+'</style>',1)

    once('<div id="cbBoardWrap" class="cbBoardWrap"><canvas id="cbCanvas"></canvas><div id="cbBoardHint" class="cbBoardHint"></div>',
         '<div id="cbBoardWrap" class="cbBoardWrap"><canvas id="cbCanvas"></canvas><div class="cbZoomDock" aria-label="Circuit zoom"><button id="cbZoomOut" title="Zoom out">−</button><button id="cbZoomFit" class="fit" title="Fit circuit to screen">Fit</button><button id="cbZoomIn" title="Zoom in">+</button></div><div id="cbBoardHint" class="cbBoardHint"></div>',
         'Circuit zoom controls')

    once("let cbScreen='home',cbCircuit=null,cbDrag=null,cbHover=null,cbSelection=new Set(),cbSelectBounds=null;",
         "let cbScreen='home',cbCircuit=null,cbDrag=null,cbHover=null,cbSelection=new Set(),cbSelectBounds=null,cbView={scale:1,panX:0,panY:0},cbPointers=new Map(),cbPinch=null,cbGestureLock=false;",
         'Circuit view state')

    old="function cbCanvasSize(c){const r=c.getBoundingClientRect(),dpr=Math.min(devicePixelRatio||1,2),w=Math.max(1,r.width),h=Math.max(1,r.height);if(c.width!==Math.round(w*dpr))c.width=Math.round(w*dpr);if(c.height!==Math.round(h*dpr))c.height=Math.round(h*dpr);const x=c.getContext('2d');x.setTransform(dpr,0,0,dpr,0,0);x.clearRect(0,0,w,h);return{x,w,h}}\nfunction cbBoardPx(p,w,h){const pad=28;return{x:pad+p.x*(w-pad*2),y:pad+p.y*(h-pad*2)}}\nfunction cbPxBoard(p,w,h){const pad=28;return{x:clamp((p.x-pad)/Math.max(1,w-pad*2)),y:clamp((p.y-pad)/Math.max(1,h-pad*2))}}"
    new="""function cbCanvasSize(c){const r=c.getBoundingClientRect(),dpr=Math.min(devicePixelRatio||1,2),w=Math.max(1,r.width),h=Math.max(1,r.height);if(c.width!==Math.round(w*dpr))c.width=Math.round(w*dpr);if(c.height!==Math.round(h*dpr))c.height=Math.round(h*dpr);const x=c.getContext('2d');x.setTransform(dpr,0,0,dpr,0,0);x.clearRect(0,0,w,h);return{x,w,h}}
function cbResetView(redraw=true){cbView={scale:1,panX:0,panY:0};cbPointers.clear();cbPinch=null;cbGestureLock=false;if(redraw)cbDrawBoard()}
function cbClampView(w,h){const pad=28,vw=Math.max(1,w-pad*2),vh=Math.max(1,h-pad*2),mx=Math.max(0,(cbView.scale-1)*vw/2),my=Math.max(0,(cbView.scale-1)*vh/2);cbView.panX=Math.max(-mx,Math.min(mx,cbView.panX));cbView.panY=Math.max(-my,Math.min(my,cbView.panY))}
function cbBoardPx(p,w,h){const pad=28,vw=Math.max(1,w-pad*2),vh=Math.max(1,h-pad*2),cx=pad+vw/2,cy=pad+vh/2,bx=pad+p.x*vw,by=pad+p.y*vh;return{x:cx+(bx-cx)*cbView.scale+cbView.panX,y:cy+(by-cy)*cbView.scale+cbView.panY}}
function cbPxBoardRaw(p,w,h){const pad=28,vw=Math.max(1,w-pad*2),vh=Math.max(1,h-pad*2),cx=pad+vw/2,cy=pad+vh/2,bx=cx+(p.x-cx-cbView.panX)/cbView.scale,by=cy+(p.y-cy-cbView.panY)/cbView.scale;return{x:(bx-pad)/vw,y:(by-pad)/vh}}
function cbPxBoard(p,w,h){const q=cbPxBoardRaw(p,w,h);return{x:clamp(q.x),y:clamp(q.y)}}
function cbSetViewAnchor(anchor,screen,w,h,scale){const pad=28,vw=Math.max(1,w-pad*2),vh=Math.max(1,h-pad*2),cx=pad+vw/2,cy=pad+vh/2,bx=pad+anchor.x*vw,by=pad+anchor.y*vh;cbView.scale=Math.max(1,Math.min(6,scale));cbView.panX=screen.x-cx-(bx-cx)*cbView.scale;cbView.panY=screen.y-cy-(by-cy)*cbView.scale;cbClampView(w,h)}
function cbZoomAt(factor,screen=null){const c=$('cbCanvas'),r=c.getBoundingClientRect(),w=r.width,h=r.height,at=screen||{x:w/2,y:h/2},anchor=cbPxBoardRaw(at,w,h);cbSetViewAnchor(anchor,at,w,h,cbView.scale*factor);cbDrawBoard()}
function cbBeginPinch(w,h){const a=[...cbPointers.values()].slice(0,2);if(a.length<2)return;const mid={x:(a[0].x+a[1].x)/2,y:(a[0].y+a[1].y)/2},dist=Math.max(8,Math.hypot(a[1].x-a[0].x,a[1].y-a[0].y));cbPinch={dist,scale:cbView.scale,anchor:cbPxBoardRaw(mid,w,h)};cbGestureLock=true;cbDrag=null;cbHover=null}
function cbUpdatePinch(w,h){const a=[...cbPointers.values()].slice(0,2);if(a.length<2||!cbPinch)return;const mid={x:(a[0].x+a[1].x)/2,y:(a[0].y+a[1].y)/2},dist=Math.max(8,Math.hypot(a[1].x-a[0].x,a[1].y-a[0].y));cbSetViewAnchor(cbPinch.anchor,mid,w,h,cbPinch.scale*dist/cbPinch.dist);cbDrawBoard()}"""
    once(old,new,'Circuit zoom math')

    # Keep the current layout exactly as-is, only reset the viewport when entering a circuit/selection screen.
    once("cbCircuit=c;cbDrag=null;cbHover=null;cbSelection.clear();$('cbCircuitTitle')",
         "cbCircuit=c;cbDrag=null;cbHover=null;cbSelection.clear();cbResetView(false);$('cbCircuitTitle')",
         'Reset view opening circuit')
    once("cbCircuit=null;cbSelection.clear();cbSelectBounds=cbBounds([...devices,...cbPanels()],.06);",
         "cbCircuit=null;cbSelection.clear();cbResetView(false);cbSelectBounds=cbBounds([...devices,...cbPanels()],.06);",
         'Reset view addressable selection')

    old="function cbValidTarget(id){const c=cbCircuit;if(!c||!id||id===c.sequence.at(-1))return false;const visited=new Set(c.sequence);if(id===c.panelId)return c.type==='addressable'&&c.deviceIds.every(x=>visited.has(x))&&c.sequence.length>1;return c.deviceIds.includes(id)&&!visited.has(id)}"
    new="function cbValidTarget(id){const c=cbCircuit;if(!c||!id)return false;const seq=[...c.sequence,...(cbDrag?.targets||[])];if(id===seq.at(-1))return false;const visited=new Set(seq);if(id===c.panelId)return c.type==='addressable'&&c.deviceIds.every(x=>visited.has(x))&&seq.length>1;return c.deviceIds.includes(id)&&!visited.has(id)}\nfunction cbSequenceReady(c,seq){if(!c)return false;const visited=new Set(seq),done=c.deviceIds.every(id=>visited.has(id));return c.type==='conventional'?done:(done&&seq.at(-1)===c.panelId&&seq.length>1)}\nfunction cbGameRouteColor(c,extra=[]){return cbSequenceReady(c,[...c.sequence,...extra])?'#239b57':'#df3f36'}"
    once(old,new,'Queued target validation and red green route state')

    # Replace board drawing so the live/finished game route is red until electrically complete, then green.
    pattern=r"function cbDrawBoard\(\)\{.*?\}\nfunction cbGameCounts"
    m=re.search(pattern,t,re.S)
    if not m: raise SystemExit('v0.45 patch marker missing: cbDrawBoard')
    draw="""function cbDrawBoard(){if($('cbGame').hidden)return;const c=$('cbCanvas'),{x,w,h}=cbCanvasSize(c),bounds=cbScreen==='select'?cbSelectBounds:cbCircuit?.bounds||{x1:0,y1:0,x2:1,y2:1};cbGhost(x,w,h,bounds,cbCircuit?.zoneId||null);let routeColor='#df3f36';if(cbScreen==='game'&&cbCircuit){routeColor=cbGameRouteColor(cbCircuit,cbDrag?.targets||[]);const committed=cbLegSegments({...cbCircuit,color:routeColor}),preview=cbDrag?.previewLegs?.length?cbLegSegments({legs:cbDrag.previewLegs,color:routeColor}):[];cbDrawBundled(x,[...committed,...preview],p=>cbBoardPx(p,w,h));if(cbDrag?.points?.length>1){x.save();x.strokeStyle=routeColor;x.lineWidth=5;x.lineCap='round';x.lineJoin='round';x.globalAlpha=.78;x.beginPath();cbDrag.points.forEach((p,i)=>i?x.lineTo(p.x,p.y):x.moveTo(p.x,p.y));x.stroke();x.restore()}}const ids=cbScreen==='select'?[...cbSurveyDevices().map(s=>s.id),...cbPanels().map(s=>s.id)]:[cbCircuit?.panelId,...(cbCircuit?.deviceIds||[])].filter(Boolean),visited=new Set(cbCircuit?.sequence||[]),queued=new Set(cbDrag?.targets||[]),current=(cbDrag?.targets||[]).at(-1)||cbCircuit?.sequence?.at(-1);for(const id of ids){const s=cbSymbol(id),p=cbNodePx(id,w,h);if(!s||!p)continue;let ring=null;if(cbScreen==='select'&&cbSelection.has(id))ring='#2675db';else if(cbScreen==='game'&&queued.has(id))ring='#dc9c16';else if(cbScreen==='game'&&id===current)ring='#20a36b';else if(cbScreen==='game'&&visited.has(id))ring='#8bbf9e';if(cbHover===id)ring=routeColor;cbDrawNode(x,s,p,s.type==='panel'?CB_PANEL_R:CB_DEVICE_R,ring,cbScreen==='select'&&s.type==='panel')}if(cbScreen==='select')$('cbBoardHint').textContent='Pinch to zoom · tap or sweep across the devices in this loop';else if(cbCircuit?.complete)$('cbBoardHint').textContent='Circuit complete · reopen or finish the As-Fit';else if(cbDrag?.targets?.length&&cbGameRouteColor(cbCircuit,cbDrag.targets)==='#239b57')$('cbBoardHint').textContent='Back at the fire panel · release, then Complete circuit';else if(cbDrag?.targets?.length){const s=cbSymbol(cbDrag.targets.at(-1));$('cbBoardHint').textContent='Release anywhere to finish at '+(s?.reference||symbolNames[s?.type]||'the last highlighted device');}else $('cbBoardHint').textContent='Hold on the green-ring device and drag through detectors · pinch with two fingers to zoom'}
function cbGameCounts"""
    t=t[:m.start()]+draw+t[m.end():]

    old="function cbUpdateGame(){if(cbScreen==='select'){$('cbSelectCount').textContent=cbSelection.size+' highlighted';$('cbBuildSelected').disabled=cbSelection.size<1;$('cbProgress').textContent='Swipe across devices to select them';$('cbReset').textContent='Clear highlighted';requestAnimationFrame(cbDrawBoard);return}if(!cbCircuit)return;const q=cbGameCounts();$('cbProgress').textContent=q.done+' / '+q.total+' devices connected'+(cbCircuit.type==='addressable'&&q.done===q.total&&cbCircuit.sequence.at(-1)!==cbCircuit.panelId?' · return to panel':'');$('cbComplete').disabled=!q.ready||cbCircuit.complete;$('cbUndoLeg').disabled=!cbCircuit.legs.length;$('cbReset').textContent='Reset circuit';requestAnimationFrame(cbDrawBoard)}"
    new="function cbUpdateGame(){if(cbScreen==='select'){$('cbSelectCount').textContent=cbSelection.size+' highlighted';$('cbBuildSelected').disabled=cbSelection.size<1;$('cbProgress').textContent='Pinch to zoom · swipe across devices to select them';$('cbReset').textContent='Clear highlighted';requestAnimationFrame(cbDrawBoard);return}if(!cbCircuit)return;const q=cbGameCounts();$('cbProgress').textContent=q.done+' / '+q.total+' devices connected'+(cbCircuit.type==='addressable'&&q.done===q.total&&cbCircuit.sequence.at(-1)!==cbCircuit.panelId?' · return to panel':'');$('cbComplete').disabled=!q.ready||cbCircuit.complete;$('cbComplete').classList.toggle('ready',q.ready&&!cbCircuit.complete);$('cbUndoLeg').disabled=!cbCircuit.legs.length;$('cbReset').textContent='Reset circuit';requestAnimationFrame(cbDrawBoard)}"
    once(old,new,'Complete button state')

    # Continuous hold-and-drag: every valid detector crossed becomes a preview leg. Releasing anywhere commits through the last crossed device and discards the trailing loose line.
    pattern=r"function cbFinishLeg\(target,w,h\)\{.*?\}\nfunction cbSelectAt\(pt,w,h\)\{.*?\}\nfunction cbCanvasDown\(e\)\{.*?\}\nfunction cbCanvasMove\(e\)\{.*?\}\nfunction cbCanvasUp\(e\)\{.*?\}"
    m=re.search(pattern,t,re.S)
    if not m: raise SystemExit('v0.45 patch marker missing: circuit pointer block')
    pointer_block="""function cbCaptureDragTarget(target,w,h){if(!cbDrag?.points?.length||!cbValidTarget(target))return false;const end=cbNodePx(target,w,h),pts=cbDrag.points.slice();if(!end)return false;const last=pts.at(-1),dx=end.x-last.x,dy=end.y-last.y;if(Math.abs(dx)>1&&Math.abs(dy)>1){const prev=pts.at(-2),horizontal=prev?Math.abs(last.y-prev.y)<Math.abs(last.x-prev.x):Math.abs(dx)>=Math.abs(dy);pts.push(horizontal?{x:end.x,y:last.y}:{x:last.x,y:end.y})}pts.push(end);cbDrag.previewLegs.push({from:cbDrag.from,to:target,points:cbSimplify(pts).map(p=>cbPxBoard(p,w,h))});cbDrag.targets.push(target);cbDrag.from=target;cbDrag.points=[end];cbHover=target;return true}
function cbCommitDrag(){if(!cbCircuit||!cbDrag?.targets?.length)return false;cbCircuit.legs.push(...cbDrag.previewLegs);cbCircuit.sequence.push(...cbDrag.targets);cbCircuit.complete=false;cbCircuit.updatedAt=Date.now();persist();cbDrag=null;cbHover=null;cbUpdateGame();return true}
function cbSelectAt(pt,w,h){const id=cbHitNode(pt,w,h,false),s=cbSymbol(id);if(!id||!s||s.type==='panel')return false;cbSelection.add(id);cbUpdateGame();return true}
function cbCanvasDown(e){const c=$('cbCanvas'),r=c.getBoundingClientRect(),w=r.width,h=r.height,p=cbPointInCanvas(e);cbPointers.set(e.pointerId,p);c.setPointerCapture?.(e.pointerId);if(cbPointers.size>=2){cbBeginPinch(w,h);cbUpdatePinch(w,h);return}if(cbGestureLock)return;if(cbScreen==='select'){cbDrag={select:true};cbSelectAt(p,w,h);return}if(cbScreen!=='game'||!cbCircuit||cbCircuit.complete)return;const start=cbCircuit.sequence.at(-1),sp=cbNodePx(start,w,h);if(!sp||Math.hypot(p.x-sp.x,p.y-sp.y)>34){$('cbBoardHint').textContent='Hold down on the green-ring device to start';return}cbDrag={points:[sp],previewLegs:[],targets:[],from:start,pointerId:e.pointerId};cbHover=null}
function cbCanvasMove(e){const r=$('cbCanvas').getBoundingClientRect(),w=r.width,h=r.height,p=cbPointInCanvas(e);if(cbPointers.has(e.pointerId))cbPointers.set(e.pointerId,p);if(cbPointers.size>=2){if(!cbPinch)cbBeginPinch(w,h);cbUpdatePinch(w,h);return}if(cbGestureLock)return;if(cbScreen==='select'&&cbDrag?.select){cbSelectAt(p,w,h);return}if(cbScreen!=='game'||!cbDrag?.points)return;cbAppendDrag(p,w,h);const target=cbHitNode(p,w,h,true);if(target)cbCaptureDragTarget(target,w,h);else cbHover=cbDrag.targets.at(-1)||null;cbDrawBoard()}
function cbCanvasUp(e){const r=$('cbCanvas').getBoundingClientRect(),w=r.width,h=r.height,p=cbPointInCanvas(e),gesture=cbGestureLock||!!cbPinch;if(cbPointers.has(e.pointerId))cbPointers.delete(e.pointerId);if(gesture){if(cbPointers.size<2)cbPinch=null;if(!cbPointers.size)cbGestureLock=false;return}if(cbScreen==='select'){cbDrag=null;return}if(cbScreen!=='game'||!cbDrag?.points)return;cbAppendDrag(p,w,h);const target=cbHitNode(p,w,h,true);if(target)cbCaptureDragTarget(target,w,h);if(!cbCommitDrag()){cbDrag=null;cbHover=null;$('cbBoardHint').textContent='Drag across a detector, then release anywhere to finish there';cbDrawBoard()}}
function cbCanvasCancel(e){if(cbPointers.has(e.pointerId))cbPointers.delete(e.pointerId);cbPinch=null;if(!cbPointers.size)cbGestureLock=false;cbDrag=null;cbHover=null;cbDrawBoard()}"""
    t=t[:m.start()]+pointer_block+t[m.end():]

    old="$('circuitModeBtn').onclick=openCircuitBuilder;$('cbBack').onclick=closeCircuitBuilder;$('cbGameHome').onclick=()=>{cbCircuit=null;cbDrag=null;cbShow('home')};$('cbAddressableStart').onclick=cbStartAddressable;$('cbBuildSelected').onclick=cbBuildAddressable;$('cbUndoLeg').onclick=cbUndo;$('cbReset').onclick=cbResetCurrent;$('cbComplete').onclick=cbCompleteCircuit;$('cbFinishAsFit').onclick=cbFinishAsFit;if($('cbFinishAsFitMain'))$('cbFinishAsFitMain').onclick=cbFinishAsFit;$('cbAsFitBack').onclick=()=>cbShow('home');$('cbExportAsFit').onclick=cbExportAsFit;$('cbCanvas').onpointerdown=cbCanvasDown;$('cbCanvas').onpointermove=cbCanvasMove;$('cbCanvas').onpointerup=cbCanvasUp;$('cbCanvas').onpointercancel=()=>{cbDrag=null;cbHover=null;cbDrawBoard()};window.addEventListener('resize',()=>{if(!$('circuitBuilder').hidden){if(cbScreen==='asfit')cbDrawAsFitPreview();else if(cbScreen==='game'||cbScreen==='select')cbDrawBoard()}});"
    new="$('circuitModeBtn').onclick=openCircuitBuilder;$('cbBack').onclick=closeCircuitBuilder;$('cbGameHome').onclick=()=>{cbCircuit=null;cbDrag=null;cbShow('home')};$('cbAddressableStart').onclick=cbStartAddressable;$('cbBuildSelected').onclick=cbBuildAddressable;$('cbUndoLeg').onclick=cbUndo;$('cbReset').onclick=cbResetCurrent;$('cbComplete').onclick=cbCompleteCircuit;$('cbFinishAsFit').onclick=cbFinishAsFit;if($('cbFinishAsFitMain'))$('cbFinishAsFitMain').onclick=cbFinishAsFit;$('cbAsFitBack').onclick=()=>cbShow('home');$('cbExportAsFit').onclick=cbExportAsFit;$('cbZoomIn').onclick=()=>cbZoomAt(1.35);$('cbZoomOut').onclick=()=>cbZoomAt(1/1.35);$('cbZoomFit').onclick=()=>cbResetView(true);$('cbCanvas').onpointerdown=cbCanvasDown;$('cbCanvas').onpointermove=cbCanvasMove;$('cbCanvas').onpointerup=cbCanvasUp;$('cbCanvas').onpointercancel=cbCanvasCancel;$('cbCanvas').addEventListener('wheel',e=>{e.preventDefault();cbZoomAt(e.deltaY<0?1.18:1/1.18,cbPointInCanvas(e))},{passive:false});window.addEventListener('resize',()=>{if(!$('circuitBuilder').hidden){if(cbScreen==='asfit')cbDrawAsFitPreview();else if(cbScreen==='game'||cbScreen==='select')cbDrawBoard()}});"
    once(old,new,'Circuit zoom event handlers')

p.write_text(t)
for q in [Path('ZoneSketch.html'),Path('Zone-Sketch-by-Will.html'),Path('app/src/main/assets/index.html')]:
    q.write_text(t)

g=Path('app/build.gradle')
s=g.read_text().replace('versionCode 45','versionCode 46').replace("versionName '0.44'","versionName '0.45'")
g.write_text(s)
print('Applied v0.45 Circuit Builder zoom, red/green route state and continuous drag capture')
