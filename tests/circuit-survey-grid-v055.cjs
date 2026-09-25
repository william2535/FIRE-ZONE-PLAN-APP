const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict'),path=require('path');
(async()=>{
 const raw=fs.readFileSync('index.html','utf8');
 if(!/v0\.55/.test(raw)){console.log('SKIP: v0.55 shared field-grid test only runs after the v0.55 patch');return}
 assert.match(raw,/function fieldGridPoint/);assert.match(raw,/function cbFieldGridScreenStep/);assert.match(raw,/return cbPlanPx\(fieldGridPoint\(plan\),bounds,w,h\)/);assert.match(raw,/Device snap · ON/);
 const hook=`window.gridProbe={read:()=>({size:gridStep(),visible:state.gridVisible,snap:state.snapGrid,misaligned:surveyFieldGridMisaligned(),symbols:(state.symbols||[]).map(s=>({type:s.type,x:s.x,y:s.y,scope:s.scope}))}),start:()=>{const c=cbNewCircuit('addressable',cbSurveyDevices());if(c)cbOpenCircuit(c);return !!c},geometry:()=>{const c=$('cbCanvas'),r=c.getBoundingClientRect(),w=r.width,h=r.height,b=cbCircuit.bounds,d=cbSymbol(cbCircuit.deviceIds[0]),node=cbNodePx(d.id,w,h),mapped=cbPlanPx(fieldGridPoint(d),b,w,h),q=cbSnapPx({x:w*.487,y:h*.533},w,h),plan=cbBoardToPlan(cbPxBoardRaw(q,w,h),b),step=gridStep(),cell=cbFieldGridScreenStep(b,w,h);return{nodeDelta:Math.hypot(node.x-mapped.x,node.y-mapped.y),snapX:plan.x*img.width/step,snapY:plan.y*img.height/step,cell,step}}};`;
 const html=raw.replace('ensureUiState();renderFloors();renderSymbolColors();',hook+'ensureUiState();renderFloors();renderSymbolColors();');
 const server=http.createServer((q,r)=>{let rel=decodeURIComponent((q.url||'/').split('?')[0]);if(rel.endsWith('/'))rel+='index.html';rel=rel.replace(/^\//,'');const file=path.join(process.cwd(),rel);try{const data=rel==='index.html'?Buffer.from(html):fs.readFileSync(file);if(file.endsWith('.js'))r.setHeader('Content-Type','text/javascript');else if(file.endsWith('.svg'))r.setHeader('Content-Type','image/svg+xml');else if(file.endsWith('.webmanifest'))r.setHeader('Content-Type','application/manifest+json');else r.setHeader('Content-Type','text/html');r.end(data)}catch(e){r.statusCode=404;r.end('not found')}}).listen(0,'127.0.0.1');
 await new Promise(r=>server.once('listening',r));const browser=await chromium.launch({headless:true});
 try{
  const p=await browser.newPage({viewport:{width:1050,height:820}}),errors=[];p.on('pageerror',e=>errors.push(e.message));p.on('dialog',d=>d.accept(d.type()==='prompt'?'Shared grid test':undefined));
  await p.goto('http://127.0.0.1:'+server.address().port+'/');await p.locator('#homeNew').click();await p.locator('#projectsHome').waitFor({state:'hidden'});
  await p.locator('#surveyModeBtn').click();
  assert.equal(await p.locator('#surveySnap').isDisabled(),true);assert.match(await p.locator('#surveySnap').innerText(),/Device snap · ON/);assert.match(await p.locator('#surveyMove').innerText(),/Field grid · 100/);
  let state=await p.evaluate(()=>gridProbe.read());assert.equal(state.visible,true);assert.equal(state.snap,true);assert.equal(state.size,100);
  const xy=async(x,y)=>p.locator('#canvas').evaluate((c,{x,y})=>{const b=c.getBoundingClientRect(),w=3200,h=2000,s=Math.min((b.width-48)/w,(b.height-48)/h);return{x:b.x+b.width/2+(x-.5)*w*s,y:b.y+b.height/2+(y-.5)*h*s}},{x,y});
  const place=async(type,q)=>{await p.locator('#surveyDevice').click();await p.locator(`[data-symbol="${type}"]`).click();const pt=await xy(q.x,q.y);await p.mouse.click(pt.x,pt.y)};
  await place('panel',{x:.137,y:.234});await place('smoke',{x:.613,y:.417});await place('mcp',{x:.782,y:.638});
  state=await p.evaluate(()=>gridProbe.read());assert.equal(state.misaligned,0,'new Survey devices must land on the field grid');
  for(const s of state.symbols){assert(Math.abs(s.x*3200/100-Math.round(s.x*3200/100))<1e-8);assert(Math.abs(s.y*2000/100-Math.round(s.y*2000/100))<1e-8)}
  await p.locator('#surveyGridUp').click();await p.waitForTimeout(60);state=await p.evaluate(()=>gridProbe.read());assert.equal(state.size,150);assert.equal(state.misaligned,0,'changing field-grid size must realign existing surveyed devices');
  for(const s of state.symbols){assert(Math.abs(s.x*3200/150-Math.round(s.x*3200/150))<1e-8);assert(Math.abs(s.y*2000/150-Math.round(s.y*2000/150))<1e-8)}
  await p.locator('#circuitModeBtn').click();assert.equal(await p.evaluate(()=>gridProbe.start()),true);await p.waitForTimeout(80);
  const g=await p.evaluate(()=>gridProbe.geometry());assert(g.nodeDelta<1e-6,'Circuit device node must sit on the exact mapped Survey-grid intersection');assert(Math.abs(g.snapX-Math.round(g.snapX))<1e-6,'Circuit cable X must snap to Survey grid');assert(Math.abs(g.snapY-Math.round(g.snapY))<1e-6,'Circuit cable Y must snap to Survey grid');assert(g.cell.x>0&&g.cell.y>0);assert.equal(g.step,150);assert.match(await p.locator('#cbPairBadge').innerText(),/GRID 150/);
  assert.deepEqual(errors,[],'No shared-grid runtime errors');console.log('PASS: v0.55 Survey devices and Circuit Builder cable share the same resizable plan-space grid');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
