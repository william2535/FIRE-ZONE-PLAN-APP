const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');

const source=fs.readFileSync('index.html','utf8');
assert(source.includes('v0.57 aggressive-touch input pipeline'),'expected v0.57 Smart Route source');

const expose=`window.cbHardeningTest={
 read:()=>JSON.parse(JSON.stringify({c:cbCircuit,drag:cbDrag,view:cbView,state:typeof cbRoutingState==='function'?cbRoutingState():'unknown'})),
 node:id=>{const r=$('cbCanvas').getBoundingClientRect(),p=cbNodePx(id,r.width,r.height);return{x:r.left+p.x,y:r.top+p.y}},
 seed:async()=>{state=fresh();state.image=blankImage();state.isBlank=true;state.symbols=[
  {id:'panel',type:'panel',scope:'plan',x:.10,y:.20},
  {id:'d0',type:'smoke',scope:'survey',x:.25,y:.20},
  {id:'d1',type:'smoke',scope:'survey',x:.40,y:.20},
  {id:'d2',type:'smoke',scope:'survey',x:.56,y:.20},
  {id:'d3',type:'heat',scope:'survey',x:.56,y:.43},
  {id:'d4',type:'mcp',scope:'survey',x:.40,y:.43},
  {id:'d5',type:'smoke',scope:'survey',x:.24,y:.43}
 ];await setImage(state.image,false);ensureFloors();openCircuitBuilder();cbOpenCircuit(cbNewCircuit('addressable',cbSurveyDevices()));cbAudioCtx=null;},
 setView:scale=>{cbView={scale,panX:0,panY:0};cbClampView($('cbCanvas').getBoundingClientRect().width,$('cbCanvas').getBoundingClientRect().height);cbDrawBoard()},
 zoomFit:()=>cbZoomAt(1/Math.max(1,cbView.scale))
};`;

const html=source.replace('ensureUiState();renderFloors();renderSymbolColors();',expose+'ensureUiState();renderFloors();renderSymbolColors();');
const server=http.createServer((q,r)=>{const file=(q.url||'/').split('?')[0]==='/'?'index.html':(q.url||'').split('?')[0].slice(1);try{r.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':'text/html');r.end(file==='index.html'?html:fs.readFileSync(file))}catch{r.statusCode=404;r.end()}}).listen(0,'127.0.0.1');

function orientation(a,b){return Math.abs(b.x-a.x)>=Math.abs(b.y-a.y)?'h':'v'}
function crossings(c){const segs=[];for(const leg of c?.legs||[])for(let i=1;i<(leg.points||[]).length;i++)segs.push({a:leg.points[i-1],b:leg.points[i]});let n=0;const close=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y)<1e-5;for(let i=0;i<segs.length;i++)for(let j=0;j<i-1;j++){const s=segs[i],t=segs[j];if(close(s.a,t.a)||close(s.a,t.b)||close(s.b,t.a)||close(s.b,t.b))continue;const sh=orientation(s.a,s.b)==='h',th=orientation(t.a,t.b)==='h';if(sh===th)continue;const h=sh?s:t,v=sh?t:s,p={x:v.a.x,y:h.a.y};if(p.x>Math.min(h.a.x,h.b.x)+1e-6&&p.x<Math.max(h.a.x,h.b.x)-1e-6&&p.y>Math.min(v.a.y,v.b.y)+1e-6&&p.y<Math.max(v.a.y,v.b.y)-1e-6)n++}return n}

async function readyPage(browser,viewport){const page=await browser.newPage({viewport});page.on('dialog',d=>d.accept());await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);await page.evaluate(async()=>{document.querySelector('#projectsHome').hidden=true;await cbHardeningTest.seed()});await page.waitForTimeout(50);return page}
const node=(page,id)=>page.evaluate(id=>cbHardeningTest.node(id),id);
const fire=(page,type,id,pt)=>page.evaluate(({type,id,pt})=>{const c=document.querySelector('#cbCanvas');c.setPointerCapture=()=>{};c.dispatchEvent(new PointerEvent(type,{pointerId:id,pointerType:'touch',clientX:pt.x,clientY:pt.y,button:0,bubbles:true}))},{type,id,pt});
async function roughTo(page,pointerId,id,jitter=7){const target=await node(page,id);await fire(page,'pointermove',pointerId,{x:target.x-jitter,y:target.y+jitter});await fire(page,'pointermove',pointerId,{x:target.x+jitter*.45,y:target.y-jitter*.55});await fire(page,'pointermove',pointerId,target);return target}
async function finishReturn(page,pointerId){const panel=await node(page,'panel');await fire(page,'pointermove',pointerId,{x:panel.x+24,y:panel.y+16});await fire(page,'pointermove',pointerId,{x:panel.x-9,y:panel.y+5});await fire(page,'pointermove',pointerId,panel);await fire(page,'pointerup',pointerId,panel);await page.waitForTimeout(40)}
function assertComplete(read,label){assert.equal(read.c.complete,true,label+' must complete');assert.equal(read.c.sequence[0],'panel',label+' must start at panel');assert.equal(read.c.sequence.at(-1),'panel',label+' must return to panel');assert.deepEqual(new Set(read.c.sequence.slice(1,-1)),new Set(['d0','d1','d2','d3','d4','d5']),label+' must capture all six devices');assert.equal(read.c.legs.length,7,label+' must save exactly seven device-to-device legs');assert.equal(crossings(read.c),0,label+' must save no self-intersections')}

(async()=>{
 await new Promise(ok=>server.once('listening',ok));const browser=await chromium.launch({headless:true}),errors=[];
 try{
  // 1) One deliberately sparse fit-view swipe crosses multiple devices between pointer samples.
  {
   const page=await readyPage(browser,{width:375,height:667});page.on('pageerror',e=>errors.push('sparse-sweep: '+e.message));
   const panel=await node(page,'panel'),d2=await node(page,'d2'),d3=await node(page,'d3'),d5=await node(page,'d5');
   await fire(page,'pointerdown',11,panel);
   await fire(page,'pointermove',11,{x:d2.x+42,y:d2.y+6}); // d0+d1+d2 in one sparse segment
   await fire(page,'pointermove',11,{x:d3.x+5,y:d3.y+18}); // d3 on the vertical sweep
   await fire(page,'pointermove',11,{x:d5.x-36,y:d5.y+5}); // d4+d5 in one sparse segment
   await finishReturn(page,11);
   const read=await page.evaluate(()=>cbHardeningTest.read());assertComplete(read,'sparse multi-device sweep');
   await page.close();
  }

  // 2) Route one loop while zoomed in, then use the real zoom-to-fit path and continue at 1x.
  {
   const page=await readyPage(browser,{width:430,height:932});page.on('pageerror',e=>errors.push('zoom-cycle: '+e.message));await page.evaluate(()=>cbHardeningTest.setView(2.15));await page.waitForTimeout(30);
   let p=await node(page,'panel');await fire(page,'pointerdown',21,p);for(const id of ['d0','d1','d2'])p=await roughTo(page,21,id,9);await fire(page,'pointerup',21,p);
   let mid=await page.evaluate(()=>cbHardeningTest.read());assert.equal(mid.c.sequence.at(-1),'d2','zoomed-in half must checkpoint at d2');assert.equal(mid.view.scale,2.15,'first half must run zoomed in');
   await page.evaluate(()=>cbHardeningTest.zoomFit());await page.waitForTimeout(35);mid=await page.evaluate(()=>cbHardeningTest.read());assert.equal(mid.view.scale,1,'zoom-to-fit must return to 1x');
   p=await node(page,'d2');await fire(page,'pointerdown',22,p);for(const id of ['d3','d4','d5'])p=await roughTo(page,22,id,8);await fire(page,'pointerup',22,p);
   p=await node(page,'d5');await fire(page,'pointerdown',23,p);await finishReturn(page,23);
   const read=await page.evaluate(()=>cbHardeningTest.read());assertComplete(read,'zoom-in then zoom-fit route');assert.equal(read.view.scale,1,'completed zoom-cycle route must remain at fit view');
   await page.close();
  }

  // 3) A genuine viewport change during an active drag must checkpoint captured devices, clear stale pointer state and allow a clean resume.
  {
   const page=await readyPage(browser,{width:412,height:915});page.on('pageerror',e=>errors.push('resize-resume: '+e.message));
   let p=await node(page,'panel');await fire(page,'pointerdown',31,p);p=await roughTo(page,31,'d0',6);p=await roughTo(page,31,'d1',7);
   await page.setViewportSize({width:768,height:1024});await page.waitForTimeout(80);
   let mid=await page.evaluate(()=>cbHardeningTest.read());assert.equal(mid.c.sequence.at(-1),'d1','resize must preserve devices already captured');assert.equal(mid.drag,null,'resize must discard stale in-progress pointer geometry');
   p=await node(page,'d1');await fire(page,'pointerdown',32,p);for(const id of ['d2','d3','d4','d5'])p=await roughTo(page,32,id,7);await fire(page,'pointerup',32,p);
   p=await node(page,'d5');await fire(page,'pointerdown',33,p);await finishReturn(page,33);
   const read=await page.evaluate(()=>cbHardeningTest.read());assertComplete(read,'resize-resume route');
   await page.close();
  }
 }finally{await browser.close();server.close()}
 assert.deepEqual(errors,[],'routing hardening browser cases must not raise runtime errors');
 console.log('PASS: v0.57 routing hardening covers sparse multi-device sweeps, zoom-in→fit routing, and resize checkpoint/resume');
})().catch(e=>{console.error(e);process.exit(1)});
