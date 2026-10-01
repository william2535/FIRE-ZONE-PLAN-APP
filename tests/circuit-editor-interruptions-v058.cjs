const fs = require('node:fs'), http = require('node:http'), assert = require('node:assert/strict');
const engine = process.env.PINEAPPLE_BROWSER || 'chromium';
const browserType = require('playwright')[engine];
assert(browserType, `Unknown browser ${engine}`);
const expose = `window.inputTest={
 seed:async()=>{state=fresh();state.site='Pineapple interruption benchmark';state.image=blankImage();state.isBlank=true;state.symbols=[
 {id:'panel',type:'panel',scope:'plan',x:.12,y:.20,reference:'FAP'},
 {id:'d0',type:'smoke',scope:'survey',x:.78,y:.20,reference:'L1/001'},
 {id:'d1',type:'heat',scope:'survey',x:.78,y:.80,reference:'L1/002'}];
 await activateProject(uid(),state);hideProjects();openCircuitBuilder();const c=cbNewCircuit('addressable',cbSurveyDevices()),A=c.layout.panel,B=c.layout.d0,C=c.layout.d1;
 c.sequence=['panel','d0','d1','panel'];c.legs=[{from:'panel',to:'d0',points:[A,B]},{from:'d0',to:'d1',points:[B,C]},{from:'d1',to:'panel',points:[C,{x:A.x,y:C.y},A]}];
 c.complete=true;c.bridges=[];c.updatedAt=Date.now();cbOpenCircuit(c);cbEnterEdit(c);return c.id},
 point:(t=.5)=>{const r=$('cbCanvas').getBoundingClientRect(),pts=cbCircuit.editDraft.legs[0].points,a=pts[0],b=pts.at(-1),q=cbBoardPx({x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t},r.width,r.height);return{x:r.left+q.x,y:r.top+q.y}},
 read:()=>JSON.parse(JSON.stringify({draft:cbCircuit?.editDraft,legs:cbCircuit?.legs,edit:cbEdit,ids:[...cbPointers.keys()],lock:cbGestureLock,pinch:!!cbPinch,hint:$('cbBoardHint').textContent,status:$('cbEditStatus').textContent,hud:$('cbDetectorLeft').textContent})),
 save:()=>saveNow(),
 reopen:()=>{openCircuitBuilder();cbOpenCircuit(cbCircuits()[0]);return cbCircuits().length},
 exportData:()=>({segments:cbAsFitSegments(),expected:cbCircuit.legs.flatMap(leg=>{const pts=cbPlanPathForLeg(cbCircuit,leg);return pts.slice(1).map((p,i)=>({a:pts[i],b:p,color:cbCircuit.color||'#2675db'}))})}),
 renderExport:()=>{const c=document.createElement('canvas');c.width=1600;c.height=1150;cbDrawAsFitOn(c,c.width,c.height,true);return c.toDataURL('image/png')},
 switchAway:()=>{const old=cbCircuit;cbEnterEdit(old);cbEditDeleteSegment({legIndex:0,segmentIndex:0});cbEdit.bridge=true;const saved=JSON.stringify(old.editDraft);state.symbols.push({id:'other',type:'smoke',scope:'survey',x:.5,y:.5});const next=cbNewCircuit('addressable',[cbSymbol('other')]);cbOpenCircuit(next);return{oldId:old.id,nextId:next.id,saved,current:cbCircuit.id,edit:cbEdit,draft:next.editDraft||null}},
 switchBack:id=>{cbOpenCircuit(cbCircuits().find(c=>c.id===id));return{draft:JSON.stringify(cbCircuit.editDraft),bridge:cbEdit?.bridge}},
 rebuild:()=>{cbSymbol('d0').x+=.05;cbOpenCircuit(cbCircuit);return{legs:cbCircuit.legs.length,draft:cbCircuit.editDraft||null,bridges:cbCircuit.bridges,complete:cbCircuit.complete,edit:cbEdit}}
};`;
const source = fs.readFileSync('index.html','utf8');
const releaseToastGuard = '#circuitBuilder:not([hidden])~.uiToastStack{bottom:calc(96px + env(safe-area-inset-bottom))}';
const enforceReleaseToastClearance = source.includes(releaseToastGuard);
const html = source.replace('ensureUiState();renderFloors();renderSymbolColors();', expose+'ensureUiState();renderFloors();renderSymbolColors();');
const server=http.createServer((q,r)=>{const f=(q.url||'/').split('?')[0].replace(/^\//,'')||'index.html';try{r.setHeader('Content-Type',f.endsWith('.js')?'text/javascript':'text/html');r.end(f==='index.html'?html:fs.readFileSync(f))}catch{r.statusCode=404;r.end()}});
const settle=page=>page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
const read=page=>page.evaluate(()=>inputTest.read());
async function touch(page,type,id,p,buttons=1){await page.evaluate(({type,id,p,buttons})=>{const c=document.querySelector('#cbCanvas');c.setPointerCapture=()=>{};c.releasePointerCapture=()=>{};c.dispatchEvent(new PointerEvent(type,{bubbles:true,pointerId:id,pointerType:'touch',button:0,buttons,clientX:p.x,clientY:p.y}))},{type,id,p,buttons})}
async function begin(page,id=7){const p=await page.evaluate(()=>inputTest.point());await touch(page,'pointerdown',id,p);await touch(page,'pointermove',id,{x:p.x+10,y:p.y+30});assert((await read(page)).edit.stroke,'Pencil must actually begin before interrupting');return p}
async function run(browser,viewport){
 const page=await browser.newPage({viewport,hasTouch:true,isMobile:viewport.width<700}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('dialog',d=>d.accept());
 await page.goto('http://127.0.0.1:'+server.address().port);
 await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);
 await page.evaluate(async()=>{document.querySelector('#projectsHome').hidden=true;await inputTest.seed()});await settle(page);
 const original=(await read(page)).draft;
 const actions={
  cancel:async p=>touch(page,'pointercancel',7,p,0),
  captureLoss:async p=>touch(page,'lostpointercapture',7,p,0),
  fit:async()=>page.locator('#cbZoomFit').click(),
  zoom:async()=>page.locator('#cbZoomIn').click(),
  blur:async()=>page.evaluate(()=>window.dispatchEvent(new Event('blur'))),
  hidden:async()=>page.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'));delete document.hidden}),
  resize:async()=>{await page.setViewportSize({width:viewport.height,height:viewport.width});await page.waitForTimeout(100)},
  pinch:async p=>{await touch(page,'pointerdown',8,{x:p.x+60,y:p.y+20});await touch(page,'pointermove',8,{x:p.x+80,y:p.y+40});await touch(page,'pointerdown',9,{x:p.x-35,y:p.y});await touch(page,'pointerup',9,p,0);await touch(page,'pointerup',8,p,0)},
 };
 for(const [name,action] of Object.entries(actions)){
  const p=await begin(page);await action(p);await settle(page);let s=await read(page);
  assert.equal(s.edit.stroke,null,`${name}: unfinished Pencil must be cancelled`);assert.equal(s.edit.tap,null,`${name}: stale Bin tap must be cleared`);
  await touch(page,'pointerup',7,p,0);await settle(page);s=await read(page);
  assert.deepEqual(s.draft,original,`${name}: route and staged work must not change`);assert.equal(s.ids.length,0,`${name}: no phantom pointer`);assert.equal(s.lock,false,`${name}: no stuck gesture lock`);assert.equal(s.pinch,false,`${name}: no stuck pinch`);
  await page.setViewportSize(viewport);await page.waitForTimeout(100);await page.locator('#cbZoomFit').click();await settle(page);
 }
 await page.locator('#cbEditBin').click();await settle(page);
 assert.match((await read(page)).hint,/Bin.*tap/i,'Bin hint must survive a redraw');
 assert.equal(await page.locator('#cbEditBin').getAttribute('aria-pressed'),'true');
 let p=await page.evaluate(()=>inputTest.point());
 await touch(page,'pointerdown',11,p);await touch(page,'pointermove',11,{x:p.x+35,y:p.y+25});await touch(page,'pointermove',11,p);await touch(page,'pointerup',11,p,0);
 assert.deepEqual((await read(page)).draft,original,'out-and-back Bin drag must not delete');
 // A real tap still deletes exactly one local section, followed by repeated history cycles.
 await touch(page,'pointerdown',12,p);await touch(page,'pointerup',12,p,0);await settle(page);
 assert.equal((await read(page)).draft.gaps.length,1);assert.match((await read(page)).status,/ROUTE OPEN/);assert.equal((await read(page)).hud,'ROUTE OPEN');
 for(let i=0;i<30;i++){
  await page.locator('#cbEditUndo').click();assert.deepEqual((await read(page)).draft,original,`undo cycle ${i}`);assert.equal((await read(page)).hud,'EDITING');
  await page.locator('#cbEditRedo').click();assert.equal((await read(page)).draft.gaps.length,1,`redo cycle ${i}`);
 }
 await page.locator('#cbEditUndo').click();await page.locator('#cbEditPencil').click();await settle(page);
 assert.match((await read(page)).hint,/Pencil.*same leg/i);
 // Stage an actual replacement, then interrupt a second live stroke. Only transient work is discarded.
 const a=await page.evaluate(()=>inputTest.point(.22)),b=await page.evaluate(()=>inputTest.point(.78));
 await touch(page,'pointerdown',13,a);
 for(const p of [{x:a.x,y:a.y+50},{x:b.x,y:b.y+50},b])await touch(page,'pointermove',13,p);
 await touch(page,'pointerup',13,b,0);await settle(page);
 const staged=(await read(page)).draft;assert(staged.pending,'Pencil must stage real replacement');assert.match((await read(page)).hint,/Replacement ready/);assert.equal((await read(page)).hud,'REPLACEMENT READY');
 await begin(page,14);await page.evaluate(()=>window.dispatchEvent(new Event('blur')));await touch(page,'pointerup',14,a,0);
 assert.deepEqual((await read(page)).draft,staged,'blur must preserve earlier staged replacement');
 assert.equal(await page.evaluate(()=>inputTest.save()),true,'named project must save successfully');await page.reload();await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);
 await page.evaluate(()=>{document.querySelector('#projectsHome').hidden=true;inputTest.reopen()});await settle(page);
 assert.deepEqual((await read(page)).draft,staged,'reload must restore exact staged route');
 await page.locator('#cbEditBin').click();p=await page.evaluate(()=>inputTest.point());await touch(page,'pointerdown',15,p);await touch(page,'pointerup',15,p,0);
 await page.locator('#cbEditDone').click();await settle(page);assert.equal((await read(page)).edit,null,'Done must validate after interruption recovery');
 const toastLayout=await page.evaluate(()=>{const toast=[...document.querySelectorAll('.uiToast')].find(el=>el.textContent.includes('Route edit validated and saved')),actions=document.querySelector('#cbGame .cbActions');if(!toast||!actions)return null;const t=toast.getBoundingClientRect(),a=actions.getBoundingClientRect();return{toastBottom:t.bottom,actionsTop:a.top,gap:a.top-t.bottom,text:toast.textContent}});
 assert(toastLayout,'successful route edit must show its confirmation toast');
 if(enforceReleaseToastClearance) assert(toastLayout.toastBottom<=toastLayout.actionsTop+1,`confirmation toast overlaps Circuit Builder actions by ${Math.ceil(toastLayout.toastBottom-toastLayout.actionsTop)}px at ${viewport.width}px`);
 const data=await page.evaluate(()=>inputTest.exportData());assert.deepEqual(data.segments.map(({a,b,color})=>({a,b,color})),data.expected,'As-Fit must use the committed edited route');
 fs.mkdirSync('test-results',{recursive:true});
 const png=await page.evaluate(()=>inputTest.renderExport());fs.writeFileSync(`test-results/pineapple-input-asfit-${engine}-${viewport.width}.png`,Buffer.from(png.split(',')[1],'base64'));
 await page.screenshot({path:`test-results/pineapple-input-${engine}-${viewport.width}.png`});
 const switched=await page.evaluate(()=>inputTest.switchAway());assert.equal(switched.edit,null,'switching circuits must leave the old edit session');assert.equal(switched.draft,null,'new circuit must not inherit a draft');assert.equal(switched.current,switched.nextId);
 const returned=await page.evaluate(id=>inputTest.switchBack(id),switched.oldId);assert.equal(returned.draft,switched.saved,'returning to old circuit must preserve its open edit');assert.equal(returned.bridge,false,'Bridge must reopen safely OFF');
 const rebuilt=await page.evaluate(()=>inputTest.rebuild());assert.equal(rebuilt.draft,null,'confirmed survey rebuild must remove obsolete draft');assert.equal(rebuilt.legs,0);assert.equal(rebuilt.bridges.length,0);assert.equal(rebuilt.complete,false);assert.equal(rebuilt.edit,null);
 assert.deepEqual(errors,[]);await page.close();const toastGate=enforceReleaseToastClearance?'toast clearance':'toast presence';console.log(`PASS ${engine} ${viewport.width}: eight interruptions, Bin gestures, 30 history cycles, staged reload, ${toastGate} and As-Fit fidelity`);
}
(async()=>{await new Promise(ok=>server.listen(0,'127.0.0.1',ok));const browser=await browserType.launch({headless:true});try{for(const viewport of [{width:375,height:667},{width:768,height:1024}])await run(browser,viewport)}finally{await browser.close();server.close()}})().catch(e=>{console.error(e);server.close();process.exit(1)});
