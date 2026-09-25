from pathlib import Path

p=Path('index.html')
t=p.read_text()

def once(old,new,label):
    global t
    if new in t and old not in t:
        return
    if old not in t:
        raise SystemExit(f'v0.46 patch marker missing: {label}')
    t=t.replace(old,new,1)

if 'v0.46 — instant Circuit Builder reward screen' not in t:
    t=t.replace('v0.45','v0.46')

    css=r'''
/* v0.46 — instant Circuit Builder reward screen. */
.cbCelebrate{pointer-events:auto!important;background:radial-gradient(circle at 50% 45%,#2ab26738 0,#16283e70 42%,#16283eb8 100%)!important;backdrop-filter:blur(2px)}
.cbCelebrateCard{position:relative;z-index:2;width:min(390px,88%);padding:22px 20px 18px!important;border:1px solid #ffffff90;border-radius:24px!important;text-align:center;background:linear-gradient(180deg,#ffffff 0,#f3fff7 100%)!important;box-shadow:0 24px 70px #10263d73,0 0 0 7px #34b76c20!important;animation:cbWinCard .34s cubic-bezier(.2,.9,.24,1.25)!important;overflow:hidden}
.cbCelebrateBadge{width:74px;height:74px;margin:-2px auto 10px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(145deg,#32bd6d,#16884a);color:#fff;font-size:42px;font-weight:950;box-shadow:0 9px 26px #218c504c,0 0 0 8px #31b96b18;animation:cbBadgeBounce .55s cubic-bezier(.2,.9,.2,1.3)}
.cbCelebrateKicker{font-size:10px;font-weight:900;letter-spacing:.18em;color:#25834e;margin-bottom:4px}.cbCelebrateTitle{font-size:23px;font-weight:900;color:#173a29}.cbCelebrateSub{font-size:12px;color:#587061;line-height:1.4;margin:7px auto 14px;max-width:290px}.cbCelebrateActions{display:grid;grid-template-columns:1fr 1fr;gap:7px}.cbCelebrateActions button{min-height:42px;background:#e8f0eb}.cbCelebrateActions .primary{grid-column:1/-1;background:#25834e;color:#fff;font-weight:850}.cbCelebrateActions .undo{background:#eef3f8}.cbCelebrateActions .retry{background:#fff0ea;color:#9b452a}.cbConfetti{position:absolute;inset:0;pointer-events:none;overflow:hidden}.cbConfetti i{position:absolute;left:50%;top:45%;width:9px;height:15px;border-radius:3px;background:var(--cc,#35b96c);transform:translate(-50%,-50%);animation:cbConfettiFly .9s ease-out both}.cbConfetti i:nth-child(2n){--cc:#ffb629}.cbConfetti i:nth-child(3n){--cc:#5e8dff}.cbConfetti i:nth-child(4n){--cc:#ef5b62}.cbConfetti i:nth-child(1){--x:-150px;--y:-120px;--r:220deg}.cbConfetti i:nth-child(2){--x:-115px;--y:135px;--r:300deg}.cbConfetti i:nth-child(3){--x:-70px;--y:-165px;--r:150deg}.cbConfetti i:nth-child(4){--x:-28px;--y:150px;--r:260deg}.cbConfetti i:nth-child(5){--x:22px;--y:-155px;--r:420deg}.cbConfetti i:nth-child(6){--x:72px;--y:145px;--r:240deg}.cbConfetti i:nth-child(7){--x:118px;--y:-125px;--r:370deg}.cbConfetti i:nth-child(8){--x:155px;--y:100px;--r:190deg}.cbConfetti i:nth-child(9){--x:-165px;--y:30px;--r:330deg}.cbConfetti i:nth-child(10){--x:165px;--y:-25px;--r:290deg}.cbConfetti i:nth-child(11){--x:-105px;--y:-65px;--r:410deg}.cbConfetti i:nth-child(12){--x:105px;--y:65px;--r:250deg}.cbBoardWrap.cbWon{animation:cbBoardWin .75s ease-out;box-shadow:0 0 0 3px #32b96b55,0 10px 38px #1c9a5530}
@keyframes cbWinCard{from{transform:scale(.72) translateY(18px);opacity:0}to{transform:scale(1);opacity:1}}@keyframes cbBadgeBounce{0%{transform:scale(.45) rotate(-18deg)}70%{transform:scale(1.13) rotate(3deg)}100%{transform:scale(1)}}@keyframes cbConfettiFly{0%{opacity:0;transform:translate(-50%,-50%) scale(.4)}15%{opacity:1}100%{opacity:0;transform:translate(calc(-50% + var(--x)),calc(-50% + var(--y))) rotate(var(--r)) scale(1)}}@keyframes cbBoardWin{0%{filter:none}35%{filter:drop-shadow(0 0 16px #36c274)}100%{filter:none}}
@media(max-width:520px){.cbCelebrateCard{width:min(350px,91%);padding:18px 14px 14px!important}.cbCelebrateBadge{width:64px;height:64px;font-size:36px}.cbCelebrateTitle{font-size:20px}.cbCelebrateActions{grid-template-columns:1fr}.cbCelebrateActions .primary{grid-column:auto}}
'''
    t=t.replace('</style>',css+'</style>',1)

    old='<div id="cbCelebrate" class="cbCelebrate" hidden><div id="cbCelebrateText">Circuit complete ✓</div></div>'
    new='<div id="cbCelebrate" class="cbCelebrate" hidden><div class="cbConfetti" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><div class="cbCelebrateCard"><div class="cbCelebrateBadge">✓</div><div class="cbCelebrateKicker">CIRCUIT COMPLETE</div><div id="cbCelebrateText" class="cbCelebrateTitle">Circuit complete!</div><div id="cbCelebrateSub" class="cbCelebrateSub">Nice run.</div><div class="cbCelebrateActions"><button id="cbCelebrateUndo" class="undo">↶ Undo last leg</button><button id="cbCelebrateRetry" class="retry">↻ Retry run</button><button id="cbCelebrateKeep" class="primary">Keep circuit ✓</button></div></div></div>'
    once(old,new,'celebration markup')

    old="function cbCaptureDragTarget(target,w,h){if(!cbDrag?.points?.length||!cbValidTarget(target))return false;const end=cbNodePx(target,w,h),pts=cbDrag.points.slice();if(!end)return false;const last=pts.at(-1),dx=end.x-last.x,dy=end.y-last.y;if(Math.abs(dx)>1&&Math.abs(dy)>1){const prev=pts.at(-2),horizontal=prev?Math.abs(last.y-prev.y)<Math.abs(last.x-prev.x):Math.abs(dx)>=Math.abs(dy);pts.push(horizontal?{x:end.x,y:last.y}:{x:last.x,y:end.y})}pts.push(end);cbDrag.previewLegs.push({from:cbDrag.from,to:target,points:cbSimplify(pts).map(p=>cbPxBoard(p,w,h))});cbDrag.targets.push(target);cbDrag.from=target;cbDrag.points=[end];cbHover=target;return true}"
    new="function cbCaptureDragTarget(target,w,h){if(!cbDrag?.points?.length||!cbValidTarget(target))return false;const end=cbNodePx(target,w,h),pts=cbDrag.points.slice();if(!end)return false;const last=pts.at(-1),dx=end.x-last.x,dy=end.y-last.y;if(Math.abs(dx)>1&&Math.abs(dy)>1){const prev=pts.at(-2),horizontal=prev?Math.abs(last.y-prev.y)<Math.abs(last.x-prev.x):Math.abs(dx)>=Math.abs(dy);pts.push(horizontal?{x:end.x,y:last.y}:{x:last.x,y:end.y})}pts.push(end);cbDrag.previewLegs.push({from:cbDrag.from,to:target,points:cbSimplify(pts).map(p=>cbPxBoard(p,w,h))});cbDrag.targets.push(target);cbDrag.from=target;cbDrag.points=[end];cbHover=target;const ready=cbSequenceReady(cbCircuit,[...cbCircuit.sequence,...cbDrag.targets]);if(ready){cbCommitDrag();cbAutoCompleteCircuit();return true}return true}"
    once(old,new,'instant auto complete on valid return')

    old="function cbUndo(){if(!cbCircuit?.legs?.length)return;cbCircuit.legs.pop();cbCircuit.sequence.pop();cbCircuit.complete=false;cbCircuit.eolId=null;persist();cbUpdateGame()}\nfunction cbResetCurrent(){if(cbScreen==='select'){cbSelection.clear();cbUpdateGame();return}if(!cbCircuit)return;cbCircuit.legs=[];cbCircuit.sequence=[cbCircuit.panelId];cbCircuit.complete=false;cbCircuit.eolId=null;persist();cbUpdateGame()}\nfunction cbCelebrate(text){$('cbCelebrateText').textContent=text;$('cbCelebrate').hidden=false;try{navigator.vibrate?.(35)}catch(e){}setTimeout(()=>{$('cbCelebrate').hidden=true},900)}\nfunction cbCompleteCircuit(){if(!cbCircuit)return;const q=cbGameCounts();if(!q.ready)return;push();cbCircuit.complete=true;cbCircuit.eolId=cbCircuit.type==='conventional'?cbCircuit.sequence.at(-1):null;cbCircuit.updatedAt=Date.now();changed();cbCelebrate(cbCircuit.type==='addressable'?'Loop complete ✓':'Circuit complete ✓');setTimeout(()=>{cbCircuit=null;cbShow('home')},850)}"
    new="""function cbHideCelebrate(){$('cbCelebrate').hidden=true;$('cbBoardWrap').classList.remove('cbWon')}
function cbUndo(){if(!cbCircuit?.legs?.length)return;cbHideCelebrate();cbCircuit.legs.pop();cbCircuit.sequence.pop();cbCircuit.complete=false;cbCircuit.eolId=null;cbCircuit.updatedAt=Date.now();persist();cbUpdateGame()}
function cbResetCurrent(){cbHideCelebrate();if(cbScreen==='select'){cbSelection.clear();cbUpdateGame();return}if(!cbCircuit)return;cbCircuit.legs=[];cbCircuit.sequence=[cbCircuit.panelId];cbCircuit.complete=false;cbCircuit.eolId=null;cbCircuit.updatedAt=Date.now();persist();cbUpdateGame()}
function cbCelebrate(text){$('cbCelebrateText').textContent=text;const q=cbGameCounts(),back=cbCircuit?.type==='addressable'?'Returned to the fire panel':'All devices connected';$('cbCelebrateSub').textContent=q.total+' device'+(q.total===1?'':'s')+' · '+back+'. Keep it, undo the last leg, or retry the run.';$('cbCelebrate').hidden=false;$('cbBoardWrap').classList.remove('cbWon');void $('cbBoardWrap').offsetWidth;$('cbBoardWrap').classList.add('cbWon');try{navigator.vibrate?.([35,35,70])}catch(e){}}
function cbAutoCompleteCircuit(){if(!cbCircuit||cbCircuit.complete)return false;const q=cbGameCounts();if(!q.ready)return false;push();cbCircuit.complete=true;cbCircuit.eolId=cbCircuit.type==='conventional'?cbCircuit.sequence.at(-1):null;cbCircuit.updatedAt=Date.now();changed();cbUpdateGame();cbCelebrate(cbCircuit.type==='addressable'?'Loop closed! ✓':'Circuit complete! ✓');return true}
function cbCompleteCircuit(){cbAutoCompleteCircuit()}
function cbKeepCompleteCircuit(){if(!cbCircuit?.complete)return;cbHideCelebrate();cbCircuit=null;cbShow('home')}
function cbRetryCompleteCircuit(){if(!cbCircuit)return;cbHideCelebrate();cbCircuit.legs=[];cbCircuit.sequence=[cbCircuit.panelId];cbCircuit.complete=false;cbCircuit.eolId=null;cbCircuit.updatedAt=Date.now();persist();cbUpdateGame()}"""
    once(old,new,'reward actions and undo-safe completion')

    old="$('circuitModeBtn').onclick=openCircuitBuilder;$('cbBack').onclick=closeCircuitBuilder;$('cbGameHome').onclick=()=>{cbCircuit=null;cbDrag=null;cbShow('home')};$('cbAddressableStart').onclick=cbStartAddressable;$('cbBuildSelected').onclick=cbBuildAddressable;$('cbUndoLeg').onclick=cbUndo;$('cbReset').onclick=cbResetCurrent;$('cbComplete').onclick=cbCompleteCircuit;$('cbFinishAsFit').onclick=cbFinishAsFit;if($('cbFinishAsFitMain'))$('cbFinishAsFitMain').onclick=cbFinishAsFit;$('cbAsFitBack').onclick=()=>cbShow('home');$('cbExportAsFit').onclick=cbExportAsFit;$('cbZoomIn').onclick=()=>cbZoomAt(1.35);$('cbZoomOut').onclick=()=>cbZoomAt(1/1.35);$('cbZoomFit').onclick=()=>cbResetView(true);"
    new="$('circuitModeBtn').onclick=openCircuitBuilder;$('cbBack').onclick=closeCircuitBuilder;$('cbGameHome').onclick=()=>{cbHideCelebrate();cbCircuit=null;cbDrag=null;cbShow('home')};$('cbAddressableStart').onclick=cbStartAddressable;$('cbBuildSelected').onclick=cbBuildAddressable;$('cbUndoLeg').onclick=cbUndo;$('cbReset').onclick=cbResetCurrent;$('cbComplete').onclick=cbCompleteCircuit;$('cbCelebrateUndo').onclick=cbUndo;$('cbCelebrateRetry').onclick=cbRetryCompleteCircuit;$('cbCelebrateKeep').onclick=cbKeepCompleteCircuit;$('cbFinishAsFit').onclick=cbFinishAsFit;if($('cbFinishAsFitMain'))$('cbFinishAsFitMain').onclick=cbFinishAsFit;$('cbAsFitBack').onclick=()=>cbShow('home');$('cbExportAsFit').onclick=cbExportAsFit;$('cbZoomIn').onclick=()=>cbZoomAt(1.35);$('cbZoomOut').onclick=()=>cbZoomAt(1/1.35);$('cbZoomFit').onclick=()=>cbResetView(true);"
    once(old,new,'reward button handlers')

    # Keep the existing Complete button as a fallback, but make its state read clearly after instant completion.
    old="$('cbComplete').disabled=!q.ready||cbCircuit.complete;$('cbComplete').classList.toggle('ready',q.ready&&!cbCircuit.complete);"
    new="$('cbComplete').disabled=!q.ready||cbCircuit.complete;$('cbComplete').classList.toggle('ready',q.ready&&!cbCircuit.complete);$('cbComplete').textContent=cbCircuit.complete?'Circuit complete ✓':'Complete circuit';"
    once(old,new,'complete button label')

for name in ['ZoneSketch.html','Zone-Sketch-by-Will.html','app/src/main/assets/index.html']:
    Path(name).write_text(t)
p.write_text(t)

g=Path('app/build.gradle')
s=g.read_text().replace('versionCode 46','versionCode 47').replace("versionName '0.45'","versionName '0.46'")
g.write_text(s)
print('Applied v0.46 instant reward screen, retry and undo-safe auto completion')
