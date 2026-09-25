from pathlib import Path
import re

MAIN = Path('index.html')
t = MAIN.read_text()


def sub_once(pattern, replacement, label):
    global t
    t2, n = re.subn(pattern, lambda m: replacement, t, count=1, flags=re.S)
    if n != 1:
        if replacement.strip() in t:
            return
        raise SystemExit(f'v0.54 patch marker missing: {label} ({n})')
    t = t2

# Keep feature-history comments intact so old regression tests remain meaningful; only move
# visible product/version identity forward.
t = t.replace('Zone Sketch by Will Flood v0.53 —', 'Zone Sketch by Will Flood v0.54 —')
t = t.replace('ZONE SKETCH · v0.53', 'ZONE SKETCH · v0.54')
t = t.replace('BETA v0.53', 'BETA v0.54')
t = t.replace('<b>v0.53</b>', '<b>v0.54</b>')

# Game-first wording and the simple zone-colour palette requested for the Circuit Builder.
t = t.replace('<aside class="cbSide"><h3>Circuits on this floor</h3>', '<aside class="cbSide"><h3>Zone challenges</h3>')
t = t.replace('<div class="eyebrow">SURVEY → VALIDATED ROUTE</div><h1>Build the circuit</h1><p>Trace the real installation while keeping the building recognisable. Circuit Builder validates every selected device and keeps the route ready for the As-Fit.</p>', '<div class="eyebrow">ZONE CHALLENGE · NO CROSSING</div><h1>Connect the zone</h1><p>Pick a zone colour and connect every surveyed device. Completed zone routes stay on the board, so each new zone becomes a harder puzzle. Crossings are blocked; a bridge tool can be added later.</p>')
t = t.replace('<div class="cbModePanel"><h2>Conventional</h2><p>Choose a zone. Circuit Builder automatically pulls in the surveyed devices that sit inside that zone.</p>', '<div class="cbModePanel"><h2>Zone Challenge</h2><p>Each zone uses its plan colour. SD, MCP, heat and other field-device symbols take that colour while you route the circuit.</p>')

# Challenge visual layer. Side menu is intentionally just colour + zone; detailed management
# remains in the main landing panel so the game board stays clean.
challenge_css = r'''
/* v0.54 — Zone Challenge game layer. */
.cbZoneButton{display:grid!important;grid-template-columns:18px minmax(0,1fr) auto;align-items:center;justify-content:stretch!important;gap:9px;position:relative;overflow:hidden}
.cbZoneButton:before{content:'';position:absolute;inset:0 auto 0 0;width:4px;background:var(--cb-color,#65768a)}
.cbZoneSwatch{width:15px;height:15px;border-radius:50%;background:var(--cb-color,#65768a);box-shadow:0 0 0 3px color-mix(in srgb,var(--cb-color,#65768a) 18%,transparent)}
.cbZoneLabel{min-width:0}.cbZoneLabel strong{display:block;font-size:12px}.cbZoneLabel small{display:block;margin-top:2px;color:#6a7b8d;font-size:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cbZoneState{font-size:12px;font-weight:950;color:var(--cb-color,#65768a)}
.cbZoneButton.active{border-color:var(--cb-color,#65768a);box-shadow:inset 0 0 0 2px color-mix(in srgb,var(--cb-color,#65768a) 28%,transparent);background:#fff}
.cbSide .cbZoneButton{width:100%;min-height:43px;margin-bottom:7px;background:#f6f8fb}.cbSide .cbZoneButton .cbZoneLabel small{display:none}.cbSide .cbZoneButton .cbZoneState{font-size:14px}
.cbPill.zoneChallenge{display:inline-flex;align-items:center;gap:6px;border-color:var(--cb-color,#65768a);box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--cb-color,#65768a) 22%,transparent)}
.cbPill.zoneChallenge:before{content:'';width:9px;height:9px;border-radius:50%;background:var(--cb-color,#65768a)}
.cbPairBadge.blocked{border-color:#df837d;background:#fff0ef;color:#a42f2a;box-shadow:0 0 0 4px #d94a4014,0 6px 22px #8a28231b;transform:scale(1.04)}
.cbGame.zoneChallenge .cbBoardWrap{background:#fbfcfe}.cbGame.zoneChallenge .cbBoardHint{box-shadow:0 5px 18px #10263d24}
@media(min-width:761px){.cbMainStatus{display:block!important}.cbSide{background:linear-gradient(180deg,#fff,#f7f9fc)}}
'''
t = t.replace('</style>', challenge_css + '\n</style>', 1)

# Shared challenge coordinate system. Every conventional zone is rebased onto the whole
# floor so completed routes/devices can stay visible while the next zone is played.
helpers = r'''
function cbChallengeBounds(){const pts=[];for(const w of state.walls||[])if(w.points?.length)pts.push(...w.points);for(const s of state.shapes||[])if(s.points?.length)pts.push(...s.points);pts.push(...cbSurveyDevices(),...cbPanels());return cbBounds(pts,.035)}
function cbBoundsNear(a,b){return !!a&&!!b&&Math.max(Math.abs(a.x1-b.x1),Math.abs(a.y1-b.y1),Math.abs(a.x2-b.x2),Math.abs(a.y2-b.y2))<1e-7}
function cbRebaseCircuit(c,bounds){if(!c||c.type!=='conventional'||!bounds)return false;const old=c.bounds;if(!old){c.bounds={...bounds};c.layout=cbMakeLayout([c.panelId,...(c.deviceIds||[])],c.bounds);return true}if(cbBoundsNear(old,bounds)){c.layout=cbMakeLayout([c.panelId,...(c.deviceIds||[])],bounds);return false}for(const leg of c.legs||[])leg.points=(leg.points||[]).map(p=>cbPlanToBoard(cbBoardToPlan(p,old),bounds));c.bounds={...bounds};c.layout=cbMakeLayout([c.panelId,...(c.deviceIds||[])],c.bounds);return true}
function cbSyncChallengeBounds(save=false){const bounds=cbChallengeBounds();let touched=false;for(const c of cbCircuits())if(c.type==='conventional')touched=cbRebaseCircuit(c,bounds)||touched;if(save&&touched){state.asFit=null;persist()}return bounds}
function cbChallengeCircuits(){if(!cbCircuit||cbCircuit.type!=='conventional')return[];return cbCircuits().filter(c=>c.id!==cbCircuit.id&&c.type==='conventional'&&!cbCircuitIssue(c)&&(c.complete||(c.legs||[]).length))}
function cbChallengeOwner(id){if(cbCircuit?.deviceIds?.includes(id))return cbCircuit;return cbChallengeCircuits().find(c=>c.deviceIds?.includes(id))||null}
function cbChallengeMapPointPx(c,p,w,h){if(!cbCircuit)return cbBoardPx(p,w,h);const plan=cbBoardToPlan(p,c?.bounds||cbCircuit.bounds);return cbPlanPx(plan,cbCircuit.bounds,w,h)}
'''
sub_once(r'(function cbZoneDevices\(zoneId\)\{.*?\}\n)', r'\1' + helpers, 'challenge shared bounds helpers')

# New conventional circuits start on the shared whole-floor challenge board. Addressable
# loops retain their existing focused bounds.
new_circuit = r'''function cbNewCircuit(type,devices,zoneId=null){const panel=cbNearestPanel(devices);if(!panel){uiNotice('Fire panel required','Add a fire panel (FAP) in Survey before building this circuit. Circuit Builder uses it as the start and return point.');return null}const bounds=type==='conventional'?cbChallengeBounds():cbBoundsFor(zoneId,devices,panel),index=cbCircuits().filter(c=>c.type===type).length+1,z=zoneId?(state.zones||[]).find(z=>z.id===zoneId):null,c={id:uid(),type,zoneId,panelId:panel.id,deviceIds:devices.map(d=>d.id),bounds,layout:null,sequence:[panel.id],legs:[],complete:false,eolId:null,color:z?.color||CB_COLORS[(index-1)%CB_COLORS.length],name:type==='conventional'?'Zone '+(z?.number||index):'Loop '+index,updatedAt:Date.now()};c.layout=cbMakeLayout([panel.id,...c.deviceIds],bounds);push();cbCircuits().push(c);changed();return c}
function cbExistingConventional'''
sub_once(r'function cbNewCircuit\(type,devices,zoneId=null\)\{.*?\}\nfunction cbExistingConventional', new_circuit, 'shared-bounds new circuit')

# Palette-style zone choices: swatch + zone label + simple state only. No device-count clutter
# in the side rail. Full circuit management stays below the landing cards.
landing = r'''function cbZoneChoice(z,c,compact=false){const devices=cbZoneDevices(z.id),b=document.createElement('button');b.className='cbZoneButton'+(c?.complete?' done':'')+(c?.id===cbCircuit?.id?' active':'');b.style.setProperty('--cb-color',z.color||c?.color||'#65768a');const sw=document.createElement('span');sw.className='cbZoneSwatch';const label=document.createElement('span');label.className='cbZoneLabel';const strong=document.createElement('strong');strong.textContent='Zone '+z.number+(compact&&z.name?' · '+z.name:'');label.append(strong);if(!compact){const small=document.createElement('small');small.textContent=z.name||(!devices.length?'No surveyed devices':c?.complete?'Complete':c?.legs?.length?'In progress':'Ready');label.append(small)}const status=document.createElement('span');status.className='cbZoneState';status.textContent=c?.complete?'✓':c?.legs?.length?'•':'›';b.append(sw,label,status);b.disabled=!devices.length;b.onclick=()=>{if(c)cbOpenCircuit(c);else{const made=cbNewCircuit('conventional',devices,z.id);if(made)cbOpenCircuit(made)}};return b}
function cbRenderCircuitManagement(target,list){if(!target)return;target.textContent='';for(const c of list){const row=document.createElement('div');row.className='cbCircuitRow'+(c.complete?' done':'');row.style.setProperty('--cb-color',c.color||'#65768a');const dot=document.createElement('span');dot.className='cbDot';const label=document.createElement('div');const s=document.createElement('strong');s.textContent=c.name;const small=document.createElement('small');small.textContent=(c.type==='addressable'?'Addressable loop':'Zone challenge')+' · '+(c.deviceIds?.length||0)+' devices'+(cbCircuitIssue(c)?' · survey changed':c.complete?' · complete':'');label.append(s,small);const open=document.createElement('button');open.textContent='Open';open.onclick=()=>cbOpenCircuit(c);const remove=document.createElement('button');remove.textContent='×';remove.setAttribute('aria-label','Remove '+c.name);remove.onclick=()=>{if(!confirm('Remove '+c.name+' and its cable route? Surveyed devices stay on the plan.'))return;push();state.circuits=cbCircuits().filter(x=>x.id!==c.id);state.asFit=null;persist();cbRenderLanding()};row.append(dot,label,open,remove);target.append(row)}if(!list.length){const e=document.createElement('div');e.className='cbEmpty';e.textContent='No circuits built yet.';target.append(e)}}
function cbRenderLanding(){const zones=$('cbConventionalZones'),side=$('cbExisting'),list=cbCircuits();zones.textContent='';side.textContent='';for(const z of state.zones||[]){const c=cbExistingConventional(z.id);zones.append(cbZoneChoice(z,c,false));side.append(cbZoneChoice(z,c,true))}if(!(state.zones||[]).length){for(const target of [zones,side]){const e=document.createElement('div');e.className='cbEmpty';e.textContent='Add zone areas in Plan / Zone Maker first.';target.append(e)}}cbRenderCircuitManagement($('cbExistingMain'),list);const ready=list.length>0&&list.every(c=>c.complete&&!cbCircuitIssue(c)),status=list.some(cbCircuitIssue)?'Survey devices have changed. Open the affected circuit to rebuild its route.':ready?'All created circuits are complete. Finish builds the As-Fit from the real surveyed positions.':list.length?'Complete every circuit above before finishing the As-Fit.':'Complete the circuits you create, then build the As-Fit.';$('cbFinishAsFit').disabled=!ready;$('cbFinishStatus').textContent=status;if($('cbFinishAsFitMain'))$('cbFinishAsFitMain').disabled=!ready;if($('cbFinishStatusMain'))$('cbFinishStatusMain').textContent=status}
function cbShow'''
sub_once(r'function cbRenderLanding\(\)\{.*?\}\nfunction cbShow', landing, 'zone-palette landing')

# Keep all conventional routes on a single board even when the project existed before v0.54.
t = t.replace("function openCircuitBuilder(){if(!img){uiNotice('Start a project first','Import a floor plan or start a blank floor before opening Circuit Builder.');return}syncFloor();cbCircuits();closeToolMenus();", "function openCircuitBuilder(){if(!img){uiNotice('Start a project first','Import a floor plan or start a blank floor before opening Circuit Builder.');return}syncFloor();cbCircuits();cbSyncChallengeBounds(true);closeToolMenus();")

open_circuit = r'''function cbOpenCircuit(c){cbCheckpointDrag(true);if(cbCircuitIssue(c)){const devices=(c.deviceIds||[]).map(cbSymbol).filter(d=>d&&symbolScope(d)==='survey'&&d.type!=='panel'&&d.type!=='you'),panel=cbSymbol(c.panelId)||cbNearestPanel(devices);if(!devices.length||!panel){uiNotice('Circuit needs attention','This saved route is missing surveyed devices or its fire panel. Restore them in Survey, or remove this circuit and create a new route.');return}if(!confirm('The surveyed devices changed since this route was built. Rebuild this circuit using their current positions? The existing route will be cleared.'))return;push();c.deviceIds=devices.map(d=>d.id);c.panelId=panel.id;c.sequence=[panel.id];c.legs=[];c.complete=false;c.eolId=null;state.asFit=null;persist()}if(c.type==='conventional')cbRebaseCircuit(c,cbSyncChallengeBounds(false));if(!(c.legs||[]).length&&!c.complete){const devices=(c.deviceIds||[]).map(cbSymbol).filter(Boolean),panel=cbSymbol(c.panelId);c.bounds=c.type==='conventional'?cbChallengeBounds():cbBoundsFor(c.zoneId,devices,panel);c.layout=cbMakeLayout([c.panelId,...c.deviceIds],c.bounds)}cbCircuit=c;cbDrag=null;cbHover=null;cbSelection.clear();cbResetView(false);const z=c.zoneId?(state.zones||[]).find(z=>z.id===c.zoneId):null;$('cbCircuitTitle').textContent=c.type==='conventional'?'Zone '+(z?.number||'')+(z?.name?' · '+z.name:''):c.name;const pill=$('cbCircuitType');pill.textContent=c.type==='addressable'?'ADDRESSABLE LOOP':'ZONE CHALLENGE';pill.classList.toggle('zoneChallenge',c.type==='conventional');pill.style.setProperty('--cb-color',c.color||'#65768a');$('cbGame').classList.toggle('zoneChallenge',c.type==='conventional');$('cbSelectCount').hidden=true;$('cbBuildSelected').hidden=true;$('cbUndoLeg').hidden=false;$('cbReset').hidden=false;$('cbComplete').hidden=false;cbShow('game');cbRenderLanding();cbUpdateGame();cbDrawBoard()}
function cbStartAddressable'''
sub_once(r'function cbOpenCircuit\(c\)\{.*?\}\nfunction cbStartAddressable', open_circuit, 'challenge open circuit')

t = t.replace("function cbStartAddressable(){const devices=cbSurveyDevices();", "function cbStartAddressable(){$('cbGame').classList.remove('zoneChallenge');$('cbCircuitType').classList.remove('zoneChallenge');const devices=cbSurveyDevices();")

# The route itself now stays the circuit/zone colour, like a connect-the-dots puzzle, rather
# than being red-until-complete and green-after-complete.
t = re.sub(r"function cbGameRouteColor\(c,extra=\[\]\)\{.*?\}", "function cbGameRouteColor(c,extra=[]){return c?.color||'#df3f36'}", t, count=1)

# Device symbol colour can now be overridden by the owning zone/loop colour.
draw_node = r'''function cbDrawNode(x,s,p,r,ring,muted=false,symbolColor=null){x.save();const seq=new Set(cbCircuit?.sequence||[]),queued=new Set(cbDrag?.targets||[]),captured=cbScreen==='game'&&s.type!=='panel'&&(seq.has(s.id)||queued.has(s.id)),allDone=cbScreen==='game'&&cbCircuit?.deviceIds?.length&&cbCircuit.deviceIds.every(id=>seq.has(id)||queued.has(id)),panelReady=s.type==='panel'&&allDone&&!cbCircuit?.complete,current=((cbDrag?.targets||[]).at(-1)||cbCircuit?.sequence?.at(-1))===s.id;if(panelReady){x.beginPath();x.arc(p.x,p.y,r+13,0,Math.PI*2);x.fillStyle='#28a66020';x.fill();x.beginPath();x.arc(p.x,p.y,r+9,0,Math.PI*2);x.strokeStyle='#28a660';x.lineWidth=3;x.globalAlpha=.9;x.stroke()}if(ring){x.beginPath();x.arc(p.x,p.y,r+8,0,Math.PI*2);x.strokeStyle=ring;x.lineWidth=current?4.5:3.5;x.globalAlpha=.82;x.stroke()}x.globalAlpha=muted?.42:1;drawSymbol(x,p,s.type,r,symbolColor||s.color||'#172333',s.rotation||0);if(captured){const bx=p.x+r*.82,by=p.y-r*.82,br=Math.max(5,r*.46);x.globalAlpha=1;x.beginPath();x.arc(bx,by,br,0,Math.PI*2);x.fillStyle='#238655';x.fill();x.strokeStyle='#fff';x.lineWidth=1.4;x.stroke();x.fillStyle='#fff';x.font=`900 ${Math.max(7,br*1.15)}px system-ui`;x.textAlign='center';x.textBaseline='middle';x.fillText('✓',bx,by+.4)}if(s.reference){x.globalAlpha=1;x.font='700 10px system-ui';x.fillStyle=symbolColor||'#40546a';x.textAlign='center';x.textBaseline='alphabetic';x.fillText(s.reference,p.x,p.y+r+15)}x.restore()}
function cbSegKey'''
sub_once(r'function cbDrawNode\(x,s,p,r,ring,muted=false\)\{.*?\}\nfunction cbSegKey', draw_node, 'zone-coloured devices')

# Non-crossing rule. Parallel retrace remains legal because the paired lane is physically
# offset before this check. Crossing or overlapping another zone route is rejected.
cross_helpers = r'''
function cbPointClose(a,b,e=2.25){return Math.hypot(a.x-b.x,a.y-b.y)<=e}
function cbSegmentConflict(a,b,c,d){const e=2.25,ah=Math.abs(a.y-b.y)<=1.25,av=Math.abs(a.x-b.x)<=1.25,ch=Math.abs(c.y-d.y)<=1.25,cv=Math.abs(c.x-d.x)<=1.25;if(Math.hypot(a.x-b.x,a.y-b.y)<2||Math.hypot(c.x-d.x,c.y-d.y)<2)return false;if(ah&&ch){if(Math.abs(a.y-c.y)>e)return false;const overlap=Math.min(Math.max(a.x,b.x),Math.max(c.x,d.x))-Math.max(Math.min(a.x,b.x),Math.min(c.x,d.x));return overlap>Math.max(12,CB_DEVICE_R)}if(av&&cv){if(Math.abs(a.x-c.x)>e)return false;const overlap=Math.min(Math.max(a.y,b.y),Math.max(c.y,d.y))-Math.max(Math.min(a.y,b.y),Math.min(c.y,d.y));return overlap>Math.max(12,CB_DEVICE_R)}let h1,h2,v1,v2;if(ah&&cv){h1=a;h2=b;v1=c;v2=d}else if(ch&&av){h1=c;h2=d;v1=a;v2=b}else return false;const p={x:v1.x,y:h1.y};if(p.x<Math.min(h1.x,h2.x)-e||p.x>Math.max(h1.x,h2.x)+e||p.y<Math.min(v1.y,v2.y)-e||p.y>Math.max(v1.y,v2.y)+e)return false;const hEnd=cbPointClose(p,h1,e)||cbPointClose(p,h2,e),vEnd=cbPointClose(p,v1,e)||cbPointClose(p,v2,e);return !(hEnd&&vEnd)}
function cbChallengeObstacleSegmentsPx(w,h){const out=[];if(!cbCircuit||cbCircuit.type!=='conventional')return out;for(const c of cbChallengeCircuits())for(const s of cbLegSegments(c))out.push({a:cbChallengeMapPointPx(c,s.a,w,h),b:cbChallengeMapPointPx(c,s.b,w,h)});for(const leg of [...(cbCircuit.legs||[]),...(cbDrag?.previewLegs||[])]){const pts=leg.points||[];for(let i=1;i<pts.length;i++)out.push({a:cbBoardPx(pts[i-1],w,h),b:cbBoardPx(pts[i],w,h)})}return out}
function cbChallengePointsBlocked(points,w,h){if(cbCircuit?.type!=='conventional'||!points?.length)return false;const segs=[];for(let i=1;i<points.length;i++)segs.push({a:points[i-1],b:points[i]});const obstacles=cbChallengeObstacleSegmentsPx(w,h);for(const s of segs)for(const o of obstacles)if(cbSegmentConflict(s.a,s.b,o.a,o.b))return true;for(let i=0;i<segs.length;i++)for(let j=0;j<i-1;j++)if(cbSegmentConflict(segs[i].a,segs[i].b,segs[j].a,segs[j].b))return true;return false}
function cbMarkBlocked(){if(!cbDrag)return;cbDrag.blocked=true;const now=Date.now();if(!cbMarkBlocked.last||now-cbMarkBlocked.last>320){cbMarkBlocked.last=now;if(uiHaptics)try{navigator.vibrate?.(18)}catch(e){}}}
'''
sub_once(r'(function cbSimplify\(points\)\{.*?\}\n)', r'\1' + cross_helpers, 'no-cross helpers')

# Validate every new snapped segment before accepting it. If blocked, keep the last legal
# grid point so moving around the obstacle naturally resumes the route.
append_drag = r'''function cbAppendDrag(p,w,h){if(!cbDrag)return false;let q=cbSnapPx(p,w,h),last=cbDrag.points.at(-1);if(!last)return false;const snap={points:cbDrag.points.map(p=>({...p})),routeAxis:cbDrag.routeAxis,pairSide:cbDrag.pairSide,pairSnap:cbDrag.pairSnap,pairAxis:cbDrag.pairAxis,pairLine:cbDrag.pairLine};q=cbPairSnapPx(q,last,w,h);cbRouteGridStep(q,w,h);if(cbChallengePointsBlocked(cbDrag.points,w,h)){cbDrag.points=snap.points;cbDrag.routeAxis=snap.routeAxis;cbDrag.pairSide=snap.pairSide;cbDrag.pairSnap=snap.pairSnap;cbDrag.pairAxis=snap.pairAxis;cbDrag.pairLine=snap.pairLine;cbMarkBlocked();return false}cbDrag.blocked=false;return true}
function cbCaptureDragTarget'''
sub_once(r'function cbAppendDrag\(p,w,h\)\{.*?\}\nfunction cbCaptureDragTarget', append_drag, 'blocked route append')

capture_target = r'''function cbCaptureDragTarget(target,w,h){if(!cbDrag?.points?.length||!cbValidTarget(target))return false;const end=cbNodePx(target,w,h),pts=cbDrag.points.slice();if(!end)return false;const last=pts.at(-1),dx=end.x-last.x,dy=end.y-last.y;if(Math.abs(dx)>1&&Math.abs(dy)>1){const prev=pts.at(-2),horizontal=prev?Math.abs(last.y-prev.y)<Math.abs(last.x-prev.x):Math.abs(dx)>=Math.abs(dy);pts.push(horizontal?{x:end.x,y:last.y}:{x:last.x,y:end.y})}pts.push(end);const clean=cbSimplify(pts);if(cbChallengePointsBlocked(clean,w,h)){cbMarkBlocked();return false}cbDrag.blocked=false;cbDrag.previewLegs.push({from:cbDrag.from,to:target,points:clean.map(p=>cbPxBoard(p,w,h))});cbDrag.targets.push(target);cbDrag.from=target;cbDrag.points=[end];cbDrag.routeAxis=null;cbDrag.pairSnap=false;cbHover=target;if(target!==cbCircuit.panelId){const q=cbGameCounts();cbPlayProgressBell(q.done,q.total);cbPulseCounter();cbMilestone(q)}cbUpdateGame();const ready=cbSequenceReady(cbCircuit,[...cbCircuit.sequence,...cbDrag.targets]);if(ready){cbCommitDrag();cbAutoCompleteCircuit();return true}return true}
function cbCommitDrag'''
sub_once(r'function cbCaptureDragTarget\(target,w,h\)\{.*?\}\nfunction cbCommitDrag', capture_target, 'blocked target connector')

process_pointer = r'''function cbProcessPointer(p,w,h){if(!cbDrag)return;const prev=cbDrag.lastPointer||p;if(cbDrag.select){for(const hit of cbNodesAlong(prev,p,w,h,true))cbSelection.add(hit.id);cbDrag.lastPointer=p;cbUpdateGame();return}let captured=false;for(const hit of cbNodesAlong(prev,p,w,h)){if(!cbDrag||cbCircuit?.complete)break;if(cbValidTarget(hit.id)){const appended=cbAppendDrag(hit.p,w,h);if(appended===false)break;if(cbCaptureDragTarget(hit.id,w,h))captured=true}}if(cbDrag?.points){if(!captured)cbAppendDrag(p,w,h);cbDrag.lastPointer=p;cbHover=cbDrag.targets.at(-1)||null}}
function cbClearReward'''
sub_once(r'function cbProcessPointer\(p,w,h\)\{.*?\}\nfunction cbClearReward', process_pointer, 'crossing-safe pointer capture')

# Flow-style board: previous zone routes and their coloured devices stay visible while the
# current zone is played. Current route and symbols use the zone colour from Plan mode.
paint = r'''function cbPaintBoard(){if($('cbGame').hidden)return;const challenge=cbScreen==='game'&&cbCircuit?.type==='conventional',pairBadge=$('cbPairBadge'),pairMode=cbScreen==='game'&&!!cbCircuit,blocked=!!(challenge&&cbDrag?.blocked);if(pairBadge){pairBadge.hidden=!pairMode;pairBadge.classList.toggle('on',!!(pairMode&&cbDrag?.pairSnap&&!blocked));pairBadge.classList.toggle('blocked',blocked);pairBadge.textContent=blocked?'✕ NO CROSSING':pairMode&&cbDrag?.pairSnap?'⇄ CABLES PAIRED':challenge?'GRID · NO CROSSING':'⇄ TWIN CABLE SNAP'}const c=$('cbCanvas'),{x,w,h}=cbCanvasSize(c),bounds=cbScreen==='select'?cbSelectBounds:cbCircuit?.bounds||{x1:0,y1:0,x2:1,y2:1};cbGhost(x,w,h,bounds,cbCircuit?.zoneId||null);if(cbScreen==='game')cbDrawRouteGrid(x,w,h);let routeColor='#df3f36',history=challenge?cbChallengeCircuits():[];if(cbScreen==='game'&&cbCircuit){routeColor=cbGameRouteColor(cbCircuit,cbDrag?.targets||[]);for(const old of history){const oldSegs=cbLegSegments(old);cbDrawBundled(x,oldSegs,p=>cbChallengeMapPointPx(old,p,w,h),4.5,6.5)}const committed=cbLegSegments({...cbCircuit,color:routeColor}),preview=cbDrag?.previewLegs?.length?cbLegSegments({legs:cbDrag.previewLegs,color:routeColor}):[];cbDrawBundled(x,[...committed,...preview],p=>cbBoardPx(p,w,h));if(cbDrag?.points?.length>1){x.save();x.strokeStyle=routeColor;x.lineWidth=5;x.lineCap='round';x.lineJoin='round';x.globalAlpha=.88;x.beginPath();cbDrag.points.forEach((p,i)=>i?x.lineTo(p.x,p.y):x.moveTo(p.x,p.y));x.stroke();x.restore()}}let ids;if(cbScreen==='select')ids=[...cbSurveyDevices().map(s=>s.id),...cbPanels().map(s=>s.id)];else if(challenge)ids=[...new Set([cbCircuit?.panelId,...history.flatMap(c=>c.deviceIds||[]),...(cbCircuit?.deviceIds||[])].filter(Boolean))];else ids=[cbCircuit?.panelId,...(cbCircuit?.deviceIds||[])].filter(Boolean);const visited=new Set(cbCircuit?.sequence||[]),queued=new Set(cbDrag?.targets||[]),current=(cbDrag?.targets||[]).at(-1)||cbCircuit?.sequence?.at(-1);for(const id of ids){const s=cbSymbol(id),owner=challenge?cbChallengeOwner(id):cbCircuit,p=challenge&&s?cbPlanPx(s,bounds,w,h):cbNodePx(id,w,h);if(!s||!p)continue;let ring=null;if(cbScreen==='select'&&cbSelection.has(id))ring='#2675db';else if(cbScreen==='game'&&owner?.id===cbCircuit?.id&&queued.has(id))ring=routeColor;else if(cbScreen==='game'&&owner?.id===cbCircuit?.id&&id===current)ring='#20a36b';else if(cbScreen==='game'&&owner?.id===cbCircuit?.id&&visited.has(id))ring=routeColor;if(cbHover===id)ring=routeColor;const symbolColor=s.type==='panel'?null:(owner?.color||routeColor);cbDrawNode(x,s,p,s.type==='panel'?CB_PANEL_R:CB_DEVICE_R,ring,cbScreen==='select'&&s.type==='panel',symbolColor)}if(cbScreen==='select')$('cbBoardHint').textContent='Pinch to zoom · tap or sweep across the devices in this loop';else if(blocked)$('cbBoardHint').textContent='Blocked — cables cannot cross · route around it (bridge tool later)';else if(cbCircuit?.complete)$('cbBoardHint').textContent='Circuit complete · choose another zone to keep the puzzle going';else if(cbCircuit?.type==='addressable'&&cbSequenceReady(cbCircuit,[...cbCircuit.sequence,...(cbDrag?.targets||[])]))$('cbBoardHint').textContent='Back at the fire panel · loop complete';else if(cbDrag?.targets?.length){const s=cbSymbol(cbDrag.targets.at(-1));$('cbBoardHint').textContent='Keep holding · route from '+(s?.reference||symbolNames[s?.type]||'the last device')+' without crossing another cable';}else $('cbBoardHint').textContent=challenge?'Start at the green-ring device · connect the zone colour · no crossings':'Hold on the green-ring device and drag through detectors · cable snaps to grid · retracing makes a parallel cable · pinch with two fingers to zoom'}
function cbGameCounts'''
sub_once(r'function cbPaintBoard\(\)\{.*?\}\nfunction cbGameCounts', paint, 'Flow-style challenge paint')

# Zone-vs-loop wording in the HUD.
t = t.replace("if(hud){hud.hidden=false;hud.setAttribute('aria-label',q.done+' of '+q.total+' devices connected')}", "if(hud){hud.hidden=false;hud.setAttribute('aria-label',q.done+' of '+q.total+' devices connected');const label=hud.querySelector('.label');if(label)label.textContent=cbCircuit.type==='conventional'?'ZONE DEVICES':'LOOP DEVICES'}")

# Main entry points remain identical. The separate 24/7 company demo is intentionally never
# touched by this patch.
for name in ['index.html', 'ZoneSketch.html', 'Zone-Sketch-by-Will.html', 'app/src/main/assets/index.html']:
    Path(name).write_text(t)

# Android release metadata.
g = Path('app/build.gradle').read_text()
g = g.replace('versionCode 54', 'versionCode 55').replace("versionName '0.53'", "versionName '0.54'")
Path('app/build.gradle').write_text(g)

# Register the new regression.
rp = Path('tests/run-regressions.cjs')
r = rp.read_text()
if "'circuit-zone-game-v054'" not in r:
    r = r.replace("'circuit-retrace-v053']", "'circuit-retrace-v053','circuit-zone-game-v054']")
    rp.write_text(r)

assert 'ZONE CHALLENGE · NO CROSSING' in t
assert 'function cbChallengePointsBlocked' in t
assert "return c?.color||'#df3f36'" in t
assert 'symbolColor||s.color' in t
assert "versionName '0.54'" in g
print('Applied v0.54 Zone Challenge game layer to main build only')
