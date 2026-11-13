const fs = require('node:fs');
const http = require('node:http');
const assert = require('node:assert/strict');
const {chromium} = require('playwright');

const source = fs.readFileSync('index.html', 'utf8');
const marker = "document.querySelector('.app').inert=true;\nensureUiState();";
const hook = `window.additionalHoldTest={
 seed:async(required=1)=>{
  const p=fresh();p.site='Additional cable return';p.fireWorkType='additional';p.image=blankImage();p.isBlank=true;
  p.symbols=[['a',.2,.25,'Existing start'],['d',.7,.25,'New detector'],['b',.85,.85,'Existing return'],['x',.2,.6,'Cable start'],['o',.5,.6,'Existing cable device'],['y',.85,.6,'Cable end'],['e',.7,.85,'Second new detector']].map(([id,x,y,reference])=>({id,type:'smoke',scope:'survey',x,y,reference,recordState:{state:['d','e'].includes(id)?'proposed':'existing'}}));
  p.walls=[{id:'wall',kind:'wall',points:[{x:.1,y:.1},{x:.9,y:.1}]}];
  await activateProject('additional-hold',p);$('projectsHome').hidden=true;document.querySelector('.app').inert=false;openCircuitBuilder();cbSound=false;
  const bounds={x1:0,y1:0,x2:1,y2:1},layout=Object.fromEntries(state.symbols.map(s=>[s.id,cbPlanToBoard(s,bounds)]));
  const old={id:'existing-cable',type:'additional',name:'Original cable',startRef:{kind:'device',id:'x'},returnRef:{kind:'device',id:'y'},deviceIds:['o'],bounds:{...bounds},layout:{x:layout.x,o:layout.o,y:layout.y},sequence:['x','o','y'],legs:[{from:'x',to:'o',points:[layout.x,layout.o]},{from:'o',to:'y',points:[layout.o,layout.y]}],bridges:[],complete:true,color:'#55758c'};
  const c={id:'added-section',type:'additional',name:'Additional section',startRef:{kind:'device',id:'a'},returnRef:{kind:'device',id:'a'},deviceIds:required===1?['d']:['d','e'],bounds:{...bounds},layout:{a:layout.a,d:layout.d,...(required===1?{}:{e:layout.e})},sequence:['a'],legs:[],bridges:[],complete:false,color:'#df3f36'};
  state.cableJoints=[];state.circuits=[old,c];state.asFit=null;cbOpenCircuit(c);changed();await saveNow();return c.id;
 },
 setup:async()=>{await additionalHoldTest.seed();state.circuits=[];state.cableJoints=[];state.additionalSetup=null;cbCircuit=null;cbShow('home');changed();await saveNow()},
 setupPoint:id=>{const r=$('cbCanvas').getBoundingClientRect(),s=state.symbols.find(s=>s.id===id),p=cbPlanPx(s,cbSelectBounds,r.width,r.height);return{x:r.left+p.x,y:r.top+p.y}},
 point:id=>{const r=$('cbCanvas').getBoundingClientRect(),p=cbNodePx(id,r.width,r.height);return{x:r.left+p.x,y:r.top+p.y}},
 plan:p=>{const r=$('cbCanvas').getBoundingClientRect(),q=cbPlanPx(p,['endpoints','select'].includes(cbScreen)?cbSelectBounds:cbCircuit.bounds,r.width,r.height);return{x:r.left+q.x,y:r.top+q.y}},
 read:()=>JSON.parse(JSON.stringify({c:cbCircuit,joints:state.cableJoints||[],symbols:state.symbols,drag:cbDrag,hold:typeof cbCableHold==='undefined'?null:cbCableHold,holdVisible:!$('cbCableHold')?.hidden,screen:cbScreen,setup:state.additionalSetup,pointers:cbPointers.size,project:clone(),ready:cbCircuit?cbSequenceReady(cbCircuit,cbCircuit.sequence):false})),
 reopen:()=>{openCircuitBuilder();cbOpenCircuit(cbCircuits().find(c=>c.id==='added-section'))},
 probe:p=>{const r=$('cbCanvas').getBoundingClientRect(),q={x:p.x-r.left,y:p.y-r.top};return{hit:cbAdditionalCableHit(q,r.width,r.height),candidate:cbCableHoldCandidate(q,r.width,r.height),tail:cbDrag?.points?.at(-1),q}},
 end:()=>{const c=cbCircuit,p=c.legs.at(-1).points.at(-1);return cbBoardToPlan(p,c.bounds)},
 busy:()=>projectBusy||restoringProject,
 save:saveNow,
 backup:()=>validateProject(JSON.parse(JSON.stringify({format:'ZoneSketchByWill',version:1,project:clone()}))),
 export:()=>{const c=document.createElement('canvas');c.width=1200;c.height=1000;cbDrawAsFitOn(c,c.width,c.height,true);return{png:c.toDataURL(),segments:cbAsFitSegments()}},
 finish:()=>{cbHideCelebrate();cbFinishAsFit()},
 cancel:()=>cbCanvasAbort()
};`;
const html = source.replace(marker, hook + marker);
assert.notEqual(html, source, 'test hooks must be installed');
const server = http.createServer((req, res) => {
  const name = (req.url || '/').split('?')[0].slice(1) || 'index.html';
  try {
    res.setHeader('Content-Type', name.endsWith('.js') ? 'text/javascript' : name.endsWith('.png') ? 'image/png' : name.endsWith('.webp') ? 'image/webp' : 'text/html');
    res.end(name === 'index.html' ? html : fs.readFileSync(name));
  } catch { res.statusCode = 404; res.end(); }
}).listen(0, '127.0.0.1');
const touch = (page, type, id, point) => page.evaluate(({type,id,point}) => {
  const canvas = document.querySelector('#cbCanvas');
  canvas.setPointerCapture = () => {};
  canvas.dispatchEvent(new PointerEvent(type, {pointerId:id,pointerType:'touch',button:0,buttons:type==='pointerup'?0:1,bubbles:true,clientX:point.x,clientY:point.y}));
}, {type,id,point});
const interpolate = async (page,id,a,b,steps=18) => {
  for(let i=1;i<=steps;i++)await touch(page,'pointermove',id,{x:a.x+(b.x-a.x)*i/steps,y:a.y+(b.y-a.y)*i/steps});
};

(async()=>{
 await new Promise(resolve=>server.once('listening',resolve));
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage({viewport:{width:390,height:844},hasTouch:true}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('dialog',d=>d.accept());
  await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);
  const read=()=>page.evaluate(()=>additionalHoldTest.read());
  const node=id=>page.evaluate(id=>additionalHoldTest.point(id),id);
  const target=()=>page.evaluate(()=>additionalHoldTest.plan({x:.7,y:.6}));
  const seed=async(required=1)=>{await page.evaluate(required=>additionalHoldTest.seed(required),required);await page.waitForTimeout(80)};
  const reachDetector=async()=>{const a=await node('a'),d=await node('d');await touch(page,'pointerdown',1,a);await interpolate(page,1,a,d);await touch(page,'pointerup',1,d);const s=await read();assert.deepEqual(s.c.sequence,['a','d'],'actual routing must capture the selected detector');assert.equal(s.c.complete,false,'same-point return still requires an actual return route');assert.equal(s.c.panelId,undefined,'additional work has no dummy panel')};
  const approachCable=async(id=2,expectHold=true)=>{const d=await node('d'),p=await target();await touch(page,'pointerdown',id,d);await interpolate(page,id,d,p,24);if(expectHold)assert.equal((await read()).holdVisible,true,'route must reach cable and arm the visible hold before testing completion/cancellation '+JSON.stringify(await page.evaluate(p=>additionalHoldTest.probe(p),p)));return p};

  let p,s;
  if(!process.env.HOLD_ONLY){
  // Endpoint setup uses two ordinary taps, never a timing-sensitive double click.
  const setupPoint=id=>page.evaluate(id=>additionalHoldTest.setupPoint(id),id);
  const tap=async(point,id=71)=>{await touch(page,'pointerdown',id,point);await touch(page,'pointerup',id,point)};
  const startSetup=async()=>{await page.evaluate(()=>additionalHoldTest.setup());await page.locator('#cbAddressableStart').click();assert.equal((await read()).screen,'endpoints')};
  await startSetup();let a=await setupPoint('a'),b=await setupPoint('b');
  // A pan and pinch must not accidentally choose a point.
  await touch(page,'pointerdown',70,a);await touch(page,'pointermove',70,{x:a.x+30,y:a.y+25});await touch(page,'pointerup',70,{x:a.x+30,y:a.y+25});assert.equal((await read()).setup?.startRef||null,null);
  await touch(page,'pointerdown',70,a);await touch(page,'pointerdown',71,b);await touch(page,'pointermove',71,{x:b.x-20,y:b.y-20});await touch(page,'pointerup',70,a);await touch(page,'pointerup',71,b);assert.equal((await read()).setup?.startRef||null,null);
  await page.locator('#cbZoomFit').click();a=await setupPoint('a');b=await setupPoint('b');await tap(a);let endpointState=await read();assert.deepEqual(endpointState.setup.startRef,{kind:'device',id:'a'});assert.equal(endpointState.c,null);await page.waitForTimeout(500);await tap(b);endpointState=await read();assert.deepEqual(endpointState.setup.returnRef,{kind:'device',id:'b'});assert.equal(endpointState.screen,'select');assert.equal(endpointState.project.circuits.length,0,'two taps only prepare a route');
  await tap(await setupPoint('d'));await page.locator('#cbBuildSelected').click();endpointState=await read();assert.equal(endpointState.c.startRef.id,'a');assert.equal(endpointState.c.returnRef.id,'b');assert.equal(endpointState.c.panelId,undefined);assert.equal(endpointState.c.complete,false);assert.equal(endpointState.c.legs.length,0,'setup tap cannot draw cable');
  await startSetup();a=await setupPoint('a');await tap(a);await page.waitForTimeout(650);await tap(a);endpointState=await read();assert.equal(endpointState.setup.startRef.id,'a');assert.equal(endpointState.setup.returnRef.id,'a');assert.equal(endpointState.symbols.length,7,'same-point return must not duplicate the device');assert.equal(endpointState.joints.length,0);
  await startSetup();const jointPoint=await page.evaluate(()=>additionalHoldTest.plan({x:.4,y:.42}));await tap(jointPoint);const firstJoint=(await read()).setup.startRef;assert.equal(firstJoint.kind,'joint');await page.waitForTimeout(650);await tap(jointPoint);endpointState=await read();assert.deepEqual(endpointState.setup.returnRef,firstJoint);assert.equal(endpointState.joints.length,1,'same standalone joint is reused');assert.equal(endpointState.screen,'select');assert.equal(endpointState.project.circuits.length,0);

  console.log('PASS: two-tap device and standalone-joint setup, no duplicates/premature route, pan/pinch rejection');
  // Ending a normal gesture on a cable does not create a connection.
  await seed();await reachDetector();p=await approachCable();await touch(page,'pointerup',2,p);s=await read();assert.equal(s.joints.length,0);assert.equal(s.c.returnRef.id,'a');assert.equal(s.c.complete,false);
  // An intentional Bridge crossing remains a crossing, not a cable joint.
  await seed();await reachDetector();await page.locator('#cbBridgeToggle').click();p=await approachCable();await touch(page,'pointermove',2,{x:p.x,y:p.y+45});await touch(page,'pointerup',2,{x:p.x,y:p.y+45});s=await read();assert.equal(s.joints.length,0,'ordinary cable crossings do not create joints');assert.equal(s.c.returnRef.id,'a');assert.equal(s.c.complete,false);
  // A short hold is cancelled on release and cannot fire later.
  await seed();await reachDetector();p=await approachCable();await page.waitForTimeout(900);await touch(page,'pointerup',2,p);await page.waitForTimeout(4300);s=await read();assert.equal(s.joints.length,0,'release must cancel the hold timer');assert.equal(s.c.complete,false);
  // Pointer cancellation and movement away cannot leave a live timer behind.
  await seed();await reachDetector();p=await approachCable();await page.waitForTimeout(300);await touch(page,'pointercancel',2,p);await page.waitForTimeout(5100);s=await read();assert.equal(s.joints.length,0,'cancelled pointer cannot connect');assert.equal(s.c.complete,false);
  await seed();await reachDetector();p=await approachCable();await page.waitForTimeout(300);await touch(page,'pointermove',2,{x:p.x+45,y:p.y-45});await page.waitForTimeout(5100);s=await read();assert.equal(s.joints.length,0,'moving away must cancel hold');await touch(page,'pointerup',2,{x:p.x+45,y:p.y-45});
  // A second finger begins a pinch; neither finger may complete the old hold.
  await seed();await reachDetector();p=await approachCable();await page.waitForTimeout(300);const second={x:p.x-60,y:p.y-70};await touch(page,'pointerdown',3,second);await touch(page,'pointermove',3,{x:second.x-15,y:second.y-15});await page.waitForTimeout(5100);s=await read();assert.equal(s.joints.length,0,'pinch must cancel hold');assert.equal(s.c.complete,false);await touch(page,'pointerup',2,p);await touch(page,'pointerup',3,second);

  }
  // The full five seconds creates one explicit, attached return at the drawn tail.
  await seed();await reachDetector();const originals=(await read()).symbols;p=await approachCable();await touch(page,'pointerup',2,p);let partial=await read();assert(partial.c.routeDraft?.points.length>1,'released cable tail is kept as unfinished route progress');assert.equal(partial.joints.length,0);await page.evaluate(()=>additionalHoldTest.save());await page.reload();await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);await page.getByRole('button',{name:'Open',exact:true}).click();await page.waitForFunction(()=>!additionalHoldTest.busy());await page.evaluate(()=>additionalHoldTest.reopen());assert.deepEqual((await read()).c.routeDraft,partial.c.routeDraft,'unfinished cable tail survives save and reload');p=await target();await touch(page,'pointerdown',2,p);assert.equal((await read()).holdVisible,true,'pressing the saved route tip resumes its deliberate hold');const started=Date.now();if(process.env.HOLD_ONLY)console.log('HOLD PROBE',JSON.stringify(await page.evaluate(p=>additionalHoldTest.probe(p),p)));await page.waitForTimeout(4200);s=await read();assert.equal(s.c.complete,false,'must not complete before five seconds');assert.equal(s.joints.length,0,'must not create a premature cable joint');
  await page.screenshot({path:'/tmp/additional-cable-hold-phone.png'});const progress=await page.locator('[role="progressbar"]:visible').count();assert(progress>0,'hold has visible progress '+JSON.stringify({c:s.c,drag:s.drag,hold:s.hold,pointers:s.pointers,joints:s.joints}));
  await touch(page,'pointermove',2,{x:p.x+2,y:p.y-1});await page.waitForTimeout(1100);s=await read();assert(Date.now()-started>=5000);assert.equal(s.c.complete,true,'full hold completes the routed return '+JSON.stringify({c:s.c,hold:s.hold,drag:s.drag,joints:s.joints}));assert.equal(s.joints.length,1);assert.equal(s.c.returnRef.kind,'joint');const joint=s.joints[0];assert.equal(s.c.returnRef.id,joint.id);assert.equal(joint.attachment.circuitId,'existing-cable');assert.equal(joint.attachment.legIndex,1);assert(Math.abs(joint.x-.7)<.015&&Math.abs(joint.y-.6)<1e-6,'joint must lie on actual target cable');assert.deepEqual(s.symbols,originals,'connections preserve original device identities and references');
  const last=s.c.legs.at(-1);assert.equal(last.to,joint.id);const end=await page.evaluate(()=>additionalHoldTest.end());assert(Math.hypot(end.x-joint.x,end.y-joint.y)<1e-6,'saved route must physically end at cable joint');const legs=JSON.stringify(s.c.legs);await touch(page,'pointerup',2,p);await page.waitForTimeout(100);s=await read();assert.equal(s.joints.length,1,'successful hold fires once');assert.equal(JSON.stringify(s.c.legs),legs,'release after hold cannot add stray cable points');
  const backup=await page.evaluate(()=>additionalHoldTest.backup());assert.equal(backup.fireWorkType,'additional');assert.deepEqual(backup.cableJoints,s.joints);const savedCircuit=s.c;assert.deepEqual(s.project.circuits.find(c=>c.id==='added-section'),savedCircuit,'active route reference must belong to current project before save');assert.equal(await page.evaluate(()=>additionalHoldTest.save()),true,'completed additional route saves successfully');await page.reload();await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);await page.getByRole('button',{name:'Open',exact:true}).click();await page.waitForFunction(()=>!additionalHoldTest.busy());await page.evaluate(()=>additionalHoldTest.reopen());s=await read();assert.deepEqual(s.c,savedCircuit,'reload preserves endpoints, attachment and all route geometry');assert.equal(s.ready,true);const exported=await page.evaluate(()=>additionalHoldTest.export());assert(exported.segments.some(segment=>segment.color==='#df3f36'&&Math.hypot(segment.b.x-joint.x,segment.b.y-joint.y)<1e-6)&&exported.png.length>10000,'added route reaches its cable joint in As fit');await page.evaluate(()=>additionalHoldTest.finish());assert.equal((await read()).screen,'asfit');await page.waitForTimeout(100);await page.screenshot({path:'/tmp/additional-asfit-phone.png'});
  // Holding continuously at the end of a drawn route uses the same deliberate connection.
  await seed();await reachDetector();p=await approachCable();await page.waitForTimeout(5300);s=await read();assert.equal(s.c.complete,true,'continuous routing hold also completes after five seconds');assert.equal(s.joints.length,1);await touch(page,'pointerup',2,p);assert.equal((await read()).joints.length,1);
  // A return can attach to an earlier leg of this same additional section.
  await seed();await reachDetector();let from=await node('d');await touch(page,'pointerdown',8,from);
  for(const plan of [{x:.6875,y:.45},{x:.45,y:.45},{x:.45,y:.25}]){const next=await page.evaluate(plan=>additionalHoldTest.plan(plan),plan);await interpolate(page,8,from,next,24);from=next}
  assert.equal((await read()).holdVisible,true,'earlier cable of the active circuit can arm a hold');await page.waitForTimeout(5300);s=await read();assert.equal(s.c.complete,true,'hold can attach to own earlier cable');assert.equal(s.joints[0].attachment.circuitId,'added-section');assert.equal(s.joints[0].attachment.legIndex,0);await touch(page,'pointerup',8,from);
  // Selected devices cannot be skipped by holding a cable after only the first.
  await seed(2);await reachDetector();p=await approachCable(2,false);await page.waitForTimeout(5300);s=await read();assert.equal(s.c.complete,false,'hold cannot skip required devices');assert.equal(s.ready,false);await touch(page,'pointerup',2,p);
  assert.deepEqual(errors,[]);console.log('PASS: phone additional-work routing, deliberate five-second cable return, early release/move/cancel/pinch rejection, one-shot release, required devices, persistence and As fit');
 }finally{await browser.close();server.close()}
})().catch(error=>{console.error(error);server.close();process.exit(1)});
