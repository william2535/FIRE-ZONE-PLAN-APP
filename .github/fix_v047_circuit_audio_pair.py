from pathlib import Path

p=Path('index.html')
t=p.read_text()

def once(old,new,label):
    global t
    if new in t and old not in t:
        return
    if old not in t:
        raise SystemExit(f'v0.47 patch marker missing: {label}')
    t=t.replace(old,new,1)

if 'v0.47 — Circuit Builder bells + pair snap' not in t:
    t=t.replace('v0.46','v0.47')

    css=r'''
/* v0.47 — Circuit Builder bells + pair snap. */
.cbDetectorHud{position:absolute;left:10px;top:10px;z-index:6;min-width:132px;padding:9px 11px 8px;border-radius:15px;background:#16283eea;color:#fff;box-shadow:0 8px 24px #10263d2e;backdrop-filter:blur(6px);pointer-events:none;overflow:hidden}
.cbDetectorHud .number{display:block;font-size:22px;line-height:1;font-weight:950;letter-spacing:-.03em;font-variant-numeric:tabular-nums}.cbDetectorHud .label{display:block;margin-top:3px;font-size:9px;font-weight:900;letter-spacing:.13em;color:#c8d9e8}.cbDetectorHud .left{display:block;margin-top:5px;font-size:10px;font-weight:800;color:#91e3b4}.cbHudBar{height:4px;margin-top:7px;border-radius:99px;background:#ffffff25;overflow:hidden}.cbHudBar i{display:block;width:0;height:100%;border-radius:99px;background:linear-gradient(90deg,#f5b93c,#36c978);transition:width .17s ease}.cbDetectorHud.pop{animation:cbHudPop .2s ease-out}
.cbPairBadge{position:absolute;right:10px;top:10px;z-index:6;padding:7px 10px;border:1px solid #72859a66;border-radius:999px;background:#ffffffd9;color:#6e7f91;font-size:9px;font-weight:900;letter-spacing:.09em;box-shadow:0 5px 18px #10263d16;backdrop-filter:blur(5px);pointer-events:none;transition:.16s ease}.cbPairBadge.on{border-color:#26a56288;background:#e9fff2;color:#16854c;box-shadow:0 0 0 4px #2aba6918,0 6px 22px #17834d24;transform:scale(1.04)}
@keyframes cbHudPop{0%{transform:scale(.93)}70%{transform:scale(1.06)}100%{transform:scale(1)}}
@media(max-width:520px){.cbDetectorHud{left:7px;top:7px;min-width:116px;padding:7px 9px}.cbDetectorHud .number{font-size:19px}.cbPairBadge{right:7px;top:7px;font-size:8px;padding:6px 8px}}
'''
    t=t.replace('</style>',css+'</style>',1)

    once('<canvas id="cbCanvas"></canvas><div class="cbZoomDock"',
         '<canvas id="cbCanvas"></canvas><div id="cbDetectorHud" class="cbDetectorHud" hidden><span id="cbDetectorCount" class="number">0 / 0</span><span class="label">LOOP DEVICES</span><span id="cbDetectorLeft" class="left">READY</span><div class="cbHudBar"><i id="cbDetectorFill"></i></div></div><div id="cbPairBadge" class="cbPairBadge" hidden>⇄ TWIN CABLE SNAP</div><div class="cbZoomDock"',
         'game HUD markup')

    once("let cbScreen='home',cbCircuit=null,cbDrag=null,cbHover=null,cbSelection=new Set(),cbSelectBounds=null,cbView={scale:1,panX:0,panY:0},cbPointers=new Map(),cbPinch=null,cbGestureLock=false;",
         "let cbScreen='home',cbCircuit=null,cbDrag=null,cbHover=null,cbSelection=new Set(),cbSelectBounds=null,cbView={scale:1,panX:0,panY:0},cbPointers=new Map(),cbPinch=null,cbGestureLock=false,cbAudioCtx=null;",
         'audio context state')

    once("const CB_ROUTE_GRID=20,CB_INSET=.045,CB_SPAN=.91,CB_DEVICE_R=11,CB_PANEL_R=16,CB_COLORS=['#e33a3a','#2675db','#20a36b','#dc9c16','#9957c5','#e26929','#1d9baa','#d04a88'];",
         "const CB_ROUTE_GRID=20,CB_INSET=.045,CB_SPAN=.91,CB_DEVICE_R=11,CB_PANEL_R=16,CB_PAIR_GAP=9,CB_PAIR_RANGE=24,CB_COLORS=['#e33a3a','#2675db','#20a36b','#dc9c16','#9957c5','#e26929','#1d9baa','#d04a88'];",
         'pair snap constants')

    # WebAudio bell. The AudioContext is primed from pointerdown so iOS/Safari treats it as a user gesture.
    anchor="function cbCircuits(){if(!Array.isArray(state.circuits))state.circuits=[];return state.circuits}"
    audio=r'''function cbEnsureAudio(){const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return null;try{if(!cbAudioCtx)cbAudioCtx=new AC();if(cbAudioCtx.state==='suspended')cbAudioCtx.resume().catch(()=>{});return cbAudioCtx}catch(e){return null}}
function cbBellTone(freq,delay=0,duration=.42,level=.105){const ctx=cbEnsureAudio();if(!ctx)return;const start=ctx.currentTime+delay;for(const [mul,vol] of [[1,1],[2.01,.2]]){const o=ctx.createOscillator(),g=ctx.createGain();o.type='sine';o.frequency.setValueAtTime(freq*mul,start);g.gain.setValueAtTime(.0001,start);g.gain.exponentialRampToValueAtTime(level*vol,start+.012);g.gain.exponentialRampToValueAtTime(.0001,start+duration);o.connect(g);g.connect(ctx.destination);o.start(start);o.stop(start+duration+.03)}}
function cbPlayProgressBell(done,total){if(!done||!total)return;const p=total<=1?1:(done-1)/(total-1),freq=500+520*Math.pow(p,.82);cbBellTone(freq,0,.4,.105)}
function cbPlayWinChime(){cbBellTone(1046,0,.34,.09);cbBellTone(1318,.075,.34,.08);cbBellTone(1568,.15,.42,.075)}
function cbPulseCounter(){const el=$('cbDetectorHud');if(!el||el.hidden)return;el.classList.remove('pop');void el.offsetWidth;el.classList.add('pop')}'''
    once(anchor,audio+'\n'+anchor,'audio helpers')

    # Live count includes targets already crossed while the finger is still down.
    old="function cbGameCounts(){if(!cbCircuit)return{done:0,total:0,ready:false};const visited=new Set(cbCircuit.sequence),done=cbCircuit.deviceIds.filter(id=>visited.has(id)).length,total=cbCircuit.deviceIds.length,ready=cbCircuit.type==='conventional'?done===total:(done===total&&cbCircuit.sequence.at(-1)===cbCircuit.panelId&&cbCircuit.sequence.length>1);return{done,total,ready}}"
    new="function cbGameCounts(){if(!cbCircuit)return{done:0,total:0,ready:false};const seq=[...cbCircuit.sequence,...(cbDrag?.targets||[])],visited=new Set(seq),done=cbCircuit.deviceIds.filter(id=>visited.has(id)).length,total=cbCircuit.deviceIds.length,ready=cbCircuit.type==='conventional'?done===total:(done===total&&seq.at(-1)===cbCircuit.panelId&&seq.length>1);return{done,total,ready}}"
    once(old,new,'live game counts')

    old="function cbUpdateGame(){if(cbScreen==='select'){$('cbSelectCount').textContent=cbSelection.size+' highlighted';$('cbBuildSelected').disabled=cbSelection.size<1;$('cbProgress').textContent='Pinch to zoom · swipe across devices to select them';$('cbReset').textContent='Clear highlighted';requestAnimationFrame(cbDrawBoard);return}if(!cbCircuit)return;const q=cbGameCounts();$('cbProgress').textContent=q.done+' / '+q.total+' devices connected'+(cbCircuit.type==='addressable'&&q.done===q.total&&cbCircuit.sequence.at(-1)!==cbCircuit.panelId?' · return to panel':'');$('cbComplete').disabled=!q.ready||cbCircuit.complete;$('cbComplete').classList.toggle('ready',q.ready&&!cbCircuit.complete);$('cbComplete').textContent=cbCircuit.complete?'Circuit complete ✓':'Complete circuit';$('cbUndoLeg').disabled=!cbCircuit.legs.length;$('cbReset').textContent='Reset circuit';requestAnimationFrame(cbDrawBoard)}"
    new="function cbUpdateGame(){const hud=$('cbDetectorHud');if(cbScreen==='select'){if(hud)hud.hidden=true;$('cbSelectCount').textContent=cbSelection.size+' highlighted';$('cbBuildSelected').disabled=cbSelection.size<1;$('cbProgress').textContent='Pinch to zoom · swipe across devices to select them';$('cbReset').textContent='Clear highlighted';requestAnimationFrame(cbDrawBoard);return}if(!cbCircuit){if(hud)hud.hidden=true;return}const q=cbGameCounts(),left=Math.max(0,q.total-q.done),seq=[...cbCircuit.sequence,...(cbDrag?.targets||[])],backNeeded=cbCircuit.type==='addressable'&&q.done===q.total&&seq.at(-1)!==cbCircuit.panelId;if(hud)hud.hidden=false;if($('cbDetectorCount'))$('cbDetectorCount').textContent=q.done+' / '+q.total;if($('cbDetectorLeft'))$('cbDetectorLeft').textContent=cbCircuit.complete?'LOOP CLOSED':backNeeded?'RETURN TO FAP':left?left+' LEFT':'ALL CONNECTED';if($('cbDetectorFill'))$('cbDetectorFill').style.width=(q.total?Math.round(q.done/q.total*100):0)+'%';$('cbProgress').textContent=q.done+' / '+q.total+' devices connected'+(backNeeded?' · return to panel':'');$('cbComplete').disabled=!q.ready||cbCircuit.complete;$('cbComplete').classList.toggle('ready',q.ready&&!cbCircuit.complete);$('cbComplete').textContent=cbCircuit.complete?'Circuit complete ✓':'Complete circuit';$('cbUndoLeg').disabled=!cbCircuit.legs.length;$('cbReset').textContent='Reset circuit';requestAnimationFrame(cbDrawBoard)}"
    once(old,new,'live count HUD update')

    # Addressable pair snapping: when a return run is drawn close and parallel to an existing cable,
    # magnet it into a consistent lane beside that route. The stored geometry is therefore already neat
    # when it is mapped back onto the As-Fit drawing.
    old="function cbAppendDrag(p,w,h){if(!cbDrag)return;const q=cbSnapPx(p,w,h),last=cbDrag.points.at(-1);if(!last||Math.hypot(q.x-last.x,q.y-last.y)<8)return;const dx=q.x-last.x,dy=q.y-last.y;if(Math.abs(dx)>1&&Math.abs(dy)>1){const prev=cbDrag.points.at(-2),horizontal=prev?Math.abs(last.y-prev.y)<Math.abs(last.x-prev.x):Math.abs(dx)>=Math.abs(dy),corner=horizontal?{x:q.x,y:last.y}:{x:last.x,y:q.y};cbDrag.points.push(corner)}cbDrag.points.push(q);cbDrag.points=cbSimplify(cbDrag.points)}"
    new=r'''function cbPairSegmentsPx(w,h){const out=[],legs=[...(cbCircuit?.legs||[]),...(cbDrag?.previewLegs||[])];for(const leg of legs){const pts=leg.points||[];for(let i=1;i<pts.length;i++){const a=cbBoardPx(pts[i-1],w,h),b=cbBoardPx(pts[i],w,h);if(Math.hypot(b.x-a.x,b.y-a.y)>28)out.push({a,b})}}return out}
function cbPairSnapPx(q,last,w,h){if(cbDrag)cbDrag.pairSnap=false;if(cbCircuit?.type!=='addressable'||!cbDrag||!last)return q;const dx=q.x-last.x,dy=q.y-last.y;if(Math.hypot(dx,dy)<8)return q;const wantH=Math.abs(dx)>=Math.abs(dy),scale=Math.max(1,cbView.scale),range=CB_PAIR_RANGE*scale,gap=CB_PAIR_GAP*scale,edge=13*scale;let best=null;for(const s of cbPairSegmentsPx(w,h)){const sx=s.b.x-s.a.x,sy=s.b.y-s.a.y,isH=Math.abs(sx)>=Math.abs(sy);if(isH!==wantH)continue;if(isH){const lo=Math.min(s.a.x,s.b.x),hi=Math.max(s.a.x,s.b.x);if(q.x<lo||q.x>hi)continue;const d=Math.abs(q.y-s.a.y),end=Math.min(Math.abs(q.x-s.a.x),Math.abs(q.x-s.b.x));if(end<edge||d>range)continue;if(!best||d<best.d)best={d,isH:true,line:s.a.y}}else{const lo=Math.min(s.a.y,s.b.y),hi=Math.max(s.a.y,s.b.y);if(q.y<lo||q.y>hi)continue;const d=Math.abs(q.x-s.a.x),end=Math.min(Math.abs(q.y-s.a.y),Math.abs(q.y-s.b.y));if(end<edge||d>range)continue;if(!best||d<best.d)best={d,isH:false,line:s.a.x}}}if(!best)return q;let side;if(best.isH){const delta=q.y-best.line;side=Math.abs(delta)<3*scale?(cbDrag.pairSide||1):(delta>=0?1:-1);q={x:q.x,y:best.line+side*gap}}else{const delta=q.x-best.line;side=Math.abs(delta)<3*scale?(cbDrag.pairSide||1):(delta>=0?1:-1);q={x:best.line+side*gap,y:q.y}}cbDrag.pairSide=side;cbDrag.pairSnap=true;return q}
function cbAppendDrag(p,w,h){if(!cbDrag)return;let q=cbSnapPx(p,w,h),last=cbDrag.points.at(-1);if(!last||Math.hypot(q.x-last.x,q.y-last.y)<8)return;q=cbPairSnapPx(q,last,w,h);const dx=q.x-last.x,dy=q.y-last.y;if(Math.abs(dx)>1&&Math.abs(dy)>1){const prev=cbDrag.points.at(-2),horizontal=prev?Math.abs(last.y-prev.y)<Math.abs(last.x-prev.x):Math.abs(dx)>=Math.abs(dy),corner=horizontal?{x:q.x,y:last.y}:{x:last.x,y:q.y};cbDrag.points.push(corner)}cbDrag.points.push(q);cbDrag.points=cbSimplify(cbDrag.points)}'''
    once(old,new,'addressable pair snap')

    # Show the twin-cable snap badge from the board renderer.
    old="function cbDrawBoard(){if($('cbGame').hidden)return;const c=$('cbCanvas'),{x,w,h}=cbCanvasSize(c),bounds=cbScreen==='select'?cbSelectBounds:cbCircuit?.bounds||{x1:0,y1:0,x2:1,y2:1};"
    new="function cbDrawBoard(){if($('cbGame').hidden)return;const pairBadge=$('cbPairBadge'),pairMode=cbScreen==='game'&&cbCircuit?.type==='addressable';if(pairBadge){pairBadge.hidden=!pairMode;pairBadge.classList.toggle('on',!!(pairMode&&cbDrag?.pairSnap));pairBadge.textContent=pairMode&&cbDrag?.pairSnap?'⇄ TWIN CABLE SNAPPED':'⇄ TWIN CABLE SNAP'}const c=$('cbCanvas'),{x,w,h}=cbCanvasSize(c),bounds=cbScreen==='select'?cbSelectBounds:cbCircuit?.bounds||{x1:0,y1:0,x2:1,y2:1};"
    once(old,new,'pair badge renderer')

    # Bell on each newly crossed loop device, rising in pitch as progress increases.
    old="function cbCaptureDragTarget(target,w,h){if(!cbDrag?.points?.length||!cbValidTarget(target))return false;const end=cbNodePx(target,w,h),pts=cbDrag.points.slice();if(!end)return false;const last=pts.at(-1),dx=end.x-last.x,dy=end.y-last.y;if(Math.abs(dx)>1&&Math.abs(dy)>1){const prev=pts.at(-2),horizontal=prev?Math.abs(last.y-prev.y)<Math.abs(last.x-prev.x):Math.abs(dx)>=Math.abs(dy);pts.push(horizontal?{x:end.x,y:last.y}:{x:last.x,y:end.y})}pts.push(end);cbDrag.previewLegs.push({from:cbDrag.from,to:target,points:cbSimplify(pts).map(p=>cbPxBoard(p,w,h))});cbDrag.targets.push(target);cbDrag.from=target;cbDrag.points=[end];cbHover=target;const ready=cbSequenceReady(cbCircuit,[...cbCircuit.sequence,...cbDrag.targets]);if(ready){cbCommitDrag();cbAutoCompleteCircuit();return true}return true}"
    new="function cbCaptureDragTarget(target,w,h){if(!cbDrag?.points?.length||!cbValidTarget(target))return false;const end=cbNodePx(target,w,h),pts=cbDrag.points.slice();if(!end)return false;const last=pts.at(-1),dx=end.x-last.x,dy=end.y-last.y;if(Math.abs(dx)>1&&Math.abs(dy)>1){const prev=pts.at(-2),horizontal=prev?Math.abs(last.y-prev.y)<Math.abs(last.x-prev.x):Math.abs(dx)>=Math.abs(dy);pts.push(horizontal?{x:end.x,y:last.y}:{x:last.x,y:end.y})}pts.push(end);cbDrag.previewLegs.push({from:cbDrag.from,to:target,points:cbSimplify(pts).map(p=>cbPxBoard(p,w,h))});cbDrag.targets.push(target);cbDrag.from=target;cbDrag.points=[end];cbDrag.pairSnap=false;cbHover=target;if(target!==cbCircuit.panelId){const q=cbGameCounts();cbPlayProgressBell(q.done,q.total);cbPulseCounter()}cbUpdateGame();const ready=cbSequenceReady(cbCircuit,[...cbCircuit.sequence,...cbDrag.targets]);if(ready){cbCommitDrag();cbAutoCompleteCircuit();return true}return true}"
    once(old,new,'progress bell on captured device')

    # Prime WebAudio on the actual touch/mouse gesture for iOS web-app compatibility.
    old="function cbCanvasDown(e){const c=$('cbCanvas'),r=c.getBoundingClientRect(),w=r.width,h=r.height,p=cbPointInCanvas(e);"
    new="function cbCanvasDown(e){cbEnsureAudio();const c=$('cbCanvas'),r=c.getBoundingClientRect(),w=r.width,h=r.height,p=cbPointInCanvas(e);"
    once(old,new,'prime audio on gesture')

    # Reward sound when the completed loop returns to the FAP.
    old="function cbCelebrate(text){$('cbCelebrateText').textContent=text;const q=cbGameCounts(),back=cbCircuit?.type==='addressable'?'Returned to the fire panel':'All devices connected';$('cbCelebrateSub').textContent=q.total+' device'+(q.total===1?'':'s')+' · '+back+'. Keep it, undo the last leg, or retry the run.';$('cbCelebrate').hidden=false;$('cbBoardWrap').classList.remove('cbWon');void $('cbBoardWrap').offsetWidth;$('cbBoardWrap').classList.add('cbWon');try{navigator.vibrate?.([35,35,70])}catch(e){}}"
    new="function cbCelebrate(text){$('cbCelebrateText').textContent=text;const q=cbGameCounts(),back=cbCircuit?.type==='addressable'?'Returned to the fire panel':'All devices connected';$('cbCelebrateSub').textContent=q.total+' device'+(q.total===1?'':'s')+' · '+back+'. Keep it, undo the last leg, or retry the run.';$('cbCelebrate').hidden=false;$('cbBoardWrap').classList.remove('cbWon');void $('cbBoardWrap').offsetWidth;$('cbBoardWrap').classList.add('cbWon');cbPlayWinChime();try{navigator.vibrate?.([35,35,70])}catch(e){}}"
    once(old,new,'completion chime')

for name in ['ZoneSketch.html','Zone-Sketch-by-Will.html','app/src/main/assets/index.html']:
    Path(name).write_text(t)
p.write_text(t)

g=Path('app/build.gradle')
s=g.read_text().replace('versionCode 47','versionCode 48').replace("versionName '0.46'","versionName '0.47'")
g.write_text(s)
print('Applied v0.47 rising bells, live loop counter and addressable twin-cable pair snap')
