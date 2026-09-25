const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');

const source=fs.readFileSync('index.html','utf8');
const expose=`window.cbCaptureTransitionTest={
 read:()=>{const r=$('cbCanvas').getBoundingClientRect(),cell=cbRouteCellPx(r.width,r.height);return JSON.parse(JSON.stringify({c:cbCircuit,drag:cbDrag,cell,state:cbRoutingState()}))},
 node:id=>{const r=$('cbCanvas').getBoundingClientRect(),p=cbNodePx(id,r.width,r.height);return{x:r.left+p.x,y:r.top+p.y}},
 seed:async()=>{state=fresh();state.image=blankImage();state.isBlank=true;state.symbols=[
  {id:'panel',type:'panel',scope:'plan',x:.10,y:.42},
  {id:'d0',type:'smoke',scope:'survey',x:.34,y:.42},
  {id:'d1',type:'heat',scope:'survey',x:.78,y:.74}
 ];await setImage(state.image,false);ensureFloors();openCircuitBuilder();cbOpenCircuit(cbNewCircuit('addressable',cbSurveyDevices()));cbAudioCtx=null;}
};`;
assert(source.includes('function cbProcessPointer'),'Circuit Builder source missing');
const html=source.replace('ensureUiState();renderFloors();renderSymbolColors();',expose+'ensureUiState();renderFloors();renderSymbolColors();');
const server=http.createServer((q,r)=>{const file=(q.url||'/').split('?')[0]==='/'?'index.html':(q.url||'').split('?')[0].slice(1);try{r.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':'text/html');r.end(file==='index.html'?html:fs.readFileSync(file))}catch{r.statusCode=404;r.end()}}).listen(0,'127.0.0.1');

(async()=>{
 await new Promise(ok=>server.once('listening',ok));
 const browser=await chromium.launch({headless:true});
 try{
  for(const viewport of [{name:'tablet',width:768,height:1024},{name:'iphone',width:430,height:932}]){
   const page=await browser.newPage({viewport:{width:viewport.width,height:viewport.height}});page.on('dialog',d=>d.accept());
   await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);
   await page.evaluate(async()=>{document.querySelector('#projectsHome').hidden=true;await cbCaptureTransitionTest.seed()});await page.waitForTimeout(40);
   const node=async id=>page.evaluate(id=>cbCaptureTransitionTest.node(id),id);
   const fire=(type,pt)=>page.evaluate(({type,pt})=>{const c=document.querySelector('#cbCanvas');c.setPointerCapture=()=>{};c.dispatchEvent(new PointerEvent(type,{pointerId:7,pointerType:'touch',clientX:pt.x,clientY:pt.y,button:0,bubbles:true}))},{type,pt});
   const panel=await node('panel'),d0=await node('d0');
   await fire('pointerdown',panel);
   // One sparse sample crosses d0 and keeps travelling a long way beyond it. This is the real-tablet failure shape.
   const overshoot={x:d0.x+Math.min(220,viewport.width*.32),y:d0.y+18};
   await fire('pointermove',overshoot);await page.waitForTimeout(20);
   let snap=await page.evaluate(()=>cbCaptureTransitionTest.read());
   assert.equal(snap.drag.targets.at(-1),'d0',viewport.name+': swept path must capture the detector');
   assert.equal(snap.drag.points.length,1,viewport.name+': capture frame should be anchored at detector only');
   // A tiny real movement after capture must not suddenly render the stale pre-capture overshoot as a giant new leg.
   const next={x:overshoot.x+12,y:overshoot.y+3};
   await fire('pointermove',next);await page.waitForTimeout(20);
   snap=await page.evaluate(()=>cbCaptureTransitionTest.read());
   const localD0={x:d0.x-(await page.locator('#cbCanvas').boundingBox()).x,y:d0.y-(await page.locator('#cbCanvas').boundingBox()).y};
   const maxTail=Math.max(0,...snap.drag.points.map(p=>Math.hypot(p.x-localD0.x,p.y-localD0.y)));
   const grid=Math.min(snap.cell.x,snap.cell.y);
   console.log(`CAPTURE_TRANSITION ${viewport.name} grid=${grid.toFixed(2)} maxTail=${maxTail.toFixed(2)} points=${snap.drag.points.length} phase=${snap.state}`);
   assert(maxTail<=Math.max(34,grid*1.35),`${viewport.name}: post-capture live tail jumped ${maxTail.toFixed(1)}px after only 12px of new movement (grid ${grid.toFixed(1)}px)`);
   // Now make deliberate post-capture movement: geometry should begin extending from d0, not from the old overshoot coordinate.
   const deliberate={x:overshoot.x+95,y:overshoot.y+5};await fire('pointermove',deliberate);await page.waitForTimeout(20);
   snap=await page.evaluate(()=>cbCaptureTransitionTest.read());
   const tailStart=snap.drag.points[0];assert(Math.hypot(tailStart.x-localD0.x,tailStart.y-localD0.y)<2,viewport.name+': next leg must remain anchored to captured detector');
   await fire('pointerup',deliberate);await page.close();
  }
 }finally{await browser.close();server.close()}
 console.log('PASS: detector-capture transition never turns swept-hit overshoot into a rubber-band leg');
})().catch(e=>{console.error(e);server.close();process.exit(1)});
