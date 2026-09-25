from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'index.html'
COPIES = [
    ROOT / 'index.html',
    ROOT / 'ZoneSketch.html',
    ROOT / 'Zone-Sketch-by-Will.html',
    ROOT / 'app/src/main/assets/index.html',
]

text = SOURCE.read_text(encoding='utf-8')
original = text

# Visible build version only. Keep historic v0.55 engine comments intact for regression provenance.
text = text.replace('Zone Sketch by Will Flood v0.55 — Fire &amp; Security Field Workspace',
                    'Zone Sketch by Will Flood v0.56 — Fire &amp; Security Field Workspace')
text = text.replace('ZONE SKETCH · v0.55', 'ZONE SKETCH · v0.56')
text = text.replace('BETA v0.55', 'BETA v0.56')
text = text.replace('<b>v0.55</b>', '<b>v0.56</b>')

anchor = "function cbPairSegmentsPx(w,h){const out=[],legs=[...(cbCircuit?.legs||[]),...(cbDrag?.previewLegs||[])];for(const leg of legs){const pts=leg.points||[];for(let i=1;i<pts.length;i++){const a=cbBoardPx(pts[i-1],w,h),b=cbBoardPx(pts[i],w,h);if(Math.hypot(b.x-a.x,b.y-a.y)>28)out.push({a,b})}}return out}\n"
assert anchor in text, 'Could not find cbPairSegmentsPx insertion anchor'
return_helpers = r'''// v0.56 addressable return magnet — once every loop device is reached, the return is constrained to the outgoing cable instead of accepting a second freehand route.
function cbReturnPhase(){const c=cbCircuit;if(!c||c.type!=='addressable'||c.complete)return false;const seq=[...c.sequence,...(cbDrag?.targets||[])],visited=new Set(seq);return !!c.deviceIds?.length&&c.deviceIds.every(id=>visited.has(id))&&seq.at(-1)!==c.panelId}
function cbReturnGuidePx(w,h){if(!cbCircuit)return[];const out=[],legs=[...(cbCircuit.legs||[]),...(cbDrag?.previewLegs||[])];for(const leg of legs){if(leg?.to===cbCircuit.panelId&&leg?.from!==cbCircuit.panelId)continue;for(const p of leg?.points||[]){const q=cbBoardPx(p,w,h);if(!out.length||!cbPointClose(out.at(-1),q,1))out.push(q)}}return cbSimplify(out).reverse()}
function cbReturnMetrics(guide){const cumulative=[0];let total=0;for(let i=1;i<guide.length;i++){total+=Math.hypot(guide[i].x-guide[i-1].x,guide[i].y-guide[i-1].y);cumulative.push(total)}return{cumulative,total}}
function cbReturnPrefixPx(guide,progress){if(!guide?.length)return[];if(guide.length===1)return[{...guide[0]}];const out=[{...guide[0]}];let walked=0;for(let i=1;i<guide.length;i++){const a=guide[i-1],b=guide[i],len=Math.hypot(b.x-a.x,b.y-a.y);if(!len)continue;if(progress>=walked+len-.25){out.push({...b});walked+=len;continue}const t=clamp((progress-walked)/len,0,1);out.push({x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t});break}return cbSimplify(out)}
function cbAppendReturnDrag(p,w,h){if(!cbDrag)return false;let guide=cbDrag.returnGuide;if(!guide?.length){guide=cbReturnGuidePx(w,h);cbDrag.returnGuide=guide.map(q=>({...q}));cbDrag.returnProgress=0}if(guide.length<2)return false;cbDrag.returnMode=true;cbDrag.pairSnap=true;cbDrag.pairAxis=null;cbDrag.pairLine=null;const {cumulative,total}=cbReturnMetrics(guide),cell=cbRouteCellPx(w,h),grid=Math.min(cell.x,cell.y),current=Math.max(0,Math.min(total,Number(cbDrag.returnProgress)||0)),prev=cbDrag.routeInput||cbDrag.lastPointer||guide[0],move=Math.hypot(p.x-prev.x,p.y-prev.y),maxAdvance=Math.max(grid*1.7,move*1.9),minS=Math.max(0,current-grid*.25),maxS=Math.min(total,current+maxAdvance);let best=null;for(let i=1;i<guide.length;i++){const a=guide[i-1],b=guide[i],vx=b.x-a.x,vy=b.y-a.y,l2=vx*vx+vy*vy;if(!l2)continue;const t=clamp(((p.x-a.x)*vx+(p.y-a.y)*vy)/l2,0,1),s=cumulative[i-1]+Math.sqrt(l2)*t;if(s<minS||s>maxS)continue;const q={x:a.x+vx*t,y:a.y+vy*t},dist=Math.hypot(p.x-q.x,p.y-q.y),score=dist+Math.max(0,s-current)*.012;if(!best||score<best.score)best={s,dist,score}}let target=current,magnetRange=Math.max(52,grid*2.8);if(Math.hypot(p.x-guide.at(-1).x,p.y-guide.at(-1).y)<=Math.max(34,grid*.9))target=total;else if(best&&best.dist<=magnetRange)target=Math.max(current,best.s);else if(move>grid*.18)target=Math.min(total,current+Math.min(move*.45,grid*.75));cbDrag.returnProgress=target;cbDrag.points=cbReturnPrefixPx(guide,target);cbDrag.routeInput={...p};cbDrag.blocked=false;return true}
'''
text = text.replace(anchor, anchor + return_helpers, 1)

old_append = "function cbAppendDrag(p,w,h){if(!cbDrag)return false;const cell=cbRouteCellPx(w,h),sample=Math.max(4,Math.min(cell.x,cell.y)*CB_ROUTE_SAMPLE_CELLS),start=cbDrag.routeInput||cbDrag.points.at(-1)||p,dist=Math.hypot(p.x-start.x,p.y-start.y),steps=Math.max(1,Math.ceil(dist/sample));"
new_append = "function cbAppendDrag(p,w,h){if(!cbDrag)return false;if(cbReturnPhase())return cbAppendReturnDrag(p,w,h);const cell=cbRouteCellPx(w,h),sample=Math.max(4,Math.min(cell.x,cell.y)*CB_ROUTE_SAMPLE_CELLS),start=cbDrag.routeInput||cbDrag.points.at(-1)||p,dist=Math.hypot(p.x-start.x,p.y-start.y),steps=Math.max(1,Math.ceil(dist/sample));"
assert old_append in text, 'Could not patch cbAppendDrag return magnet hook'
text = text.replace(old_append, new_append, 1)

old_capture = "function cbCaptureDragTarget(target,w,h){if(!cbDrag?.points?.length||!cbValidTarget(target))return false;const end=cbNodePx(target,w,h),pts=cbDrag.points.slice();"
new_capture = "function cbCaptureDragTarget(target,w,h){if(!cbDrag?.points?.length||!cbValidTarget(target))return false;const returning=target===cbCircuit?.panelId&&cbReturnPhase(),end=cbNodePx(target,w,h),pts=returning?cbReturnGuidePx(w,h):cbDrag.points.slice();"
assert old_capture in text, 'Could not make final return leg canonical'
text = text.replace(old_capture, new_capture, 1)

# Fix NaN fallback in the existing pair-snap input parser while this route engine is being touched.
old_pair = "prev=cbDrag.routeInput||last,rx=Number(raw?.x)??q.x,ry=Number(raw?.y)??q.y,dx=rx-prev.x,dy=ry-prev.y,move=Math.hypot(dx,dy);"
new_pair = "prev=cbDrag.routeInput||last,rawX=Number(raw?.x),rawY=Number(raw?.y),rx=Number.isFinite(rawX)?rawX:q.x,ry=Number.isFinite(rawY)?rawY:q.y,dx=rx-prev.x,dy=ry-prev.y,move=Math.hypot(dx,dy);"
assert old_pair in text, 'Could not patch pair-snap numeric fallback'
text = text.replace(old_pair, new_pair, 1)

# Paint state: magnetic return gets an explicit badge, only the FAP is green, and completed twin cable gets an 8–12 px visible lane gap as zoom increases.
old_paint_head = "function cbPaintBoard(){if($('cbGame').hidden)return;const challenge=cbScreen==='game'&&cbCircuit?.type==='conventional',pairBadge=$('cbPairBadge'),pairMode=cbScreen==='game'&&!!cbCircuit,blocked=!!(challenge&&cbDrag?.blocked);if(pairBadge){pairBadge.hidden=!pairMode;pairBadge.classList.toggle('on',!!(pairMode&&cbDrag?.pairSnap&&!blocked));pairBadge.classList.toggle('blocked',blocked);pairBadge.textContent=blocked?'✕ NO CROSSING':pairMode&&cbDrag?.pairSnap?'⇄ CABLES PAIRED':challenge?'GRID '+gridStep()+' · NO CROSSING':'⇄ TWIN CABLE · GRID '+gridStep()}"
new_paint_head = "function cbPaintBoard(){if($('cbGame').hidden)return;const challenge=cbScreen==='game'&&cbCircuit?.type==='conventional',pairBadge=$('cbPairBadge'),pairMode=cbScreen==='game'&&!!cbCircuit,blocked=!!(challenge&&cbDrag?.blocked),returning=cbScreen==='game'&&cbReturnPhase();if(pairBadge){pairBadge.hidden=!pairMode;pairBadge.classList.toggle('on',!!(returning||(pairMode&&cbDrag?.pairSnap&&!blocked)));pairBadge.classList.toggle('blocked',blocked);pairBadge.textContent=blocked?'✕ NO CROSSING':returning?'⇄ RETURN MAGNET · FOLLOW CABLE':pairMode&&cbDrag?.pairSnap?'⇄ CABLES PAIRED':challenge?'GRID '+gridStep()+' · NO CROSSING':'⇄ TWIN CABLE · GRID '+gridStep()}"
assert old_paint_head in text, 'Could not patch Circuit Builder paint state'
text = text.replace(old_paint_head, new_paint_head, 1)

old_bundle = "cbDrawBundled(x,[...committed,...preview],p=>cbBoardPx(p,w,h));"
new_bundle = "cbDrawBundled(x,[...committed,...preview],p=>cbBoardPx(p,w,h),5,Math.max(8,Math.min(12,8*Math.sqrt(Math.max(1,cbView.scale)))));"
assert old_bundle in text, 'Could not patch twin cable display gap'
text = text.replace(old_bundle, new_bundle, 1)

old_current_ring = "else if(cbScreen==='game'&&owner?.id===cbCircuit?.id&&id===current)ring='#20a36b';"
new_current_ring = "else if(cbScreen==='game'&&owner?.id===cbCircuit?.id&&id===current&&!returning)ring='#20a36b';"
assert old_current_ring in text, 'Could not suppress stale final-device green ring'
text = text.replace(old_current_ring, new_current_ring, 1)

old_hint = "else if(cbCircuit?.type==='addressable'&&cbSequenceReady(cbCircuit,[...cbCircuit.sequence,...(cbDrag?.targets||[])]))$('cbBoardHint').textContent='Back at the fire panel · loop complete';else if(cbDrag?.targets?.length){"
new_hint = "else if(cbCircuit?.type==='addressable'&&cbSequenceReady(cbCircuit,[...cbCircuit.sequence,...(cbDrag?.targets||[])]))$('cbBoardHint').textContent='Back at the fire panel · loop complete';else if(returning)$('cbBoardHint').textContent='Return to the green-ring FAP · the cable is magnetically following the outgoing route';else if(cbDrag?.targets?.length){"
assert old_hint in text, 'Could not patch return-to-FAP board hint'
text = text.replace(old_hint, new_hint, 1)

old_complete_text = "$('cbComplete').textContent=cbCircuit.complete?'Circuit complete ✓':'Complete circuit';"
new_complete_text = "$('cbComplete').textContent=cbCircuit.complete?'Circuit complete ✓':backNeeded?'Return to FAP':'Complete circuit';"
assert old_complete_text in text, 'Could not patch return-to-FAP action label'
text = text.replace(old_complete_text, new_complete_text, 1)

old_down = "const start=cbCircuit.sequence.at(-1),sp=cbNodePx(start,w,h);if(!sp||Math.hypot(p.x-sp.x,p.y-sp.y)>34){$('cbBoardHint').textContent='Start on the green-ring device';return}cbDrag={points:[sp],previewLegs:[],targets:[],from:start,routeAxis:null,turnAnchor:null,routeInput:sp,pointerId:e.pointerId,lastPointer:p};cbHover=null"
new_down = "const start=cbCircuit.sequence.at(-1),sp=cbNodePx(start,w,h),returning=cbReturnPhase();if(!sp||(!returning&&Math.hypot(p.x-sp.x,p.y-sp.y)>34)){$('cbBoardHint').textContent=returning?'Drag toward the green-ring FAP':'Start on the green-ring device';return}cbDrag={points:[sp],previewLegs:[],targets:[],from:start,routeAxis:null,turnAnchor:null,routeInput:sp,pointerId:e.pointerId,lastPointer:returning?sp:p,returnMode:returning,returnProgress:0,returnGuide:null};if(returning){cbAppendReturnDrag(p,w,h);cbDrag.lastPointer=p;$('cbBoardHint').textContent='Return to the green-ring FAP · magnetic twin cable is on';}cbHover=null"
assert old_down in text, 'Could not patch forgiving return gesture start'
text = text.replace(old_down, new_down, 1)

# The old generic addressable hint should no longer claim the current detector is the only green-ring target during the return phase.
old_generic_hint = "'Hold on the green-ring device and drag through detectors · cable uses Survey field grid · corners lock cleanly · retracing makes a parallel cable · pinch with two fingers to zoom'"
new_generic_hint = "'Hold on the green-ring device and drag through detectors · cable uses Survey field grid · corners lock cleanly · the final return magnetically follows the outgoing cable · pinch with two fingers to zoom'"
assert old_generic_hint in text, 'Could not refresh generic addressable hint'
text = text.replace(old_generic_hint, new_generic_hint, 1)

assert text != original, 'v0.56 patch made no changes'
assert '// v0.56 addressable return magnet' in text
assert "backNeeded?'Return to FAP':'Complete circuit'" in text
assert '⇄ RETURN MAGNET · FOLLOW CABLE' in text
assert "id===current&&!returning" in text
assert "returning?cbReturnGuidePx(w,h):cbDrag.points.slice()" in text

for path in COPIES:
    path.write_text(text, encoding='utf-8')

build = ROOT / 'app/build.gradle'
gradle = build.read_text(encoding='utf-8')
gradle = re.sub(r'versionCode\s+\d+', 'versionCode 57', gradle, count=1)
gradle = re.sub(r"versionName\s+'[^']+'", "versionName '0.56'", gradle, count=1)
build.write_text(gradle, encoding='utf-8')

print('Applied v0.56 magnetic return routing, return-state UX and twin-cable cleanup to all main app copies.')
