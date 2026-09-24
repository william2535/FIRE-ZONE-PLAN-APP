const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');
(async()=>{
 const html=fs.readFileSync('index.html','utf8').replace("ensureUiState();renderFloors();renderSymbolColors();", "window.surveyTest={read:()=>({state:JSON.parse(JSON.stringify(state)),zoom,pan:{...pan},view:transform()}),screen:screenPoint};ensureUiState();renderFloors();renderSymbolColors();");
 const server=http.createServer((req,res)=>{if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(html)}else{res.statusCode=404;res.end()}}).listen(0,'127.0.0.1');
 await new Promise(r=>server.once('listening',r));const browser=await chromium.launch({headless:true});
 try{
 const p=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
 p.on('pageerror',e=>errors.push(e.message));p.on('dialog',d=>d.accept(d.type()==='prompt'?'Survey test':undefined));
 await p.goto('http://127.0.0.1:'+server.address().port);await p.locator('#homeNew').click();await p.locator('#projectsHome').waitFor({state:'hidden'});await p.locator('#surveyModeBtn').click();
 const read=()=>p.evaluate(()=>window.surveyTest.read());
 const devicePoint=()=>p.evaluate(()=>{const s=window.surveyTest.read().state.symbols[0],q=window.surveyTest.screen(s),r=document.querySelector('#canvas').getBoundingClientRect();return{x:q.x+r.left,y:q.y+r.top}});
 await p.locator('#surveyDevice').click();await p.locator('#symbolStampScale').fill('0.1');await p.locator('#symbolStampScale').dispatchEvent('input');await p.locator('[data-symbol="smoke"]').click();
 let b=await p.locator('#canvas').boundingBox();await p.mouse.click(b.x+b.width/2,b.y+b.height/2);assert.equal((await read()).state.symbols.length,1);
 await p.locator('#surveySelect').click();let q=await devicePoint();await p.mouse.click(q.x,q.y);await p.locator('#propertiesSelected').click();assert.equal(await p.locator('#propScale').inputValue(),'0.1');await p.locator('#propColor').fill('#2675db');await p.locator('#propDevice').fill('L1-043');await p.locator('#propSave').click();
 let s=(await read()).state.symbols[0];assert.equal(s.color,'#2675db');assert.equal(s.reference,'L1-043');assert.equal(s.scale,.1);
 q=await devicePoint();await p.mouse.move(q.x,q.y);await p.mouse.down();await p.mouse.move(q.x+40,q.y+20,{steps:6});await p.mouse.up();let moved=(await read()).state.symbols[0];assert(moved.x>s.x);assert(moved.y>s.y);
 await p.locator('#surveyUndo').click();assert.equal((await read()).state.symbols[0].x,s.x);await p.locator('#surveyRedo').click();assert.equal((await read()).state.symbols[0].x,moved.x);
 await p.locator('#surveyMove').click();b=await p.locator('#canvas').boundingBox();await p.mouse.move(b.x+b.width*.5,b.y+b.height*.5);await p.mouse.down();await p.mouse.move(b.x+b.width*.5+30,b.y+b.height*.5+20);await p.mouse.up();
 const before=await read();await p.locator('#viewZoom').fill('1');await p.locator('#viewZoom').dispatchEvent('input');let after=await read();assert.equal(after.zoom,2);assert(Math.abs(after.pan.x-before.pan.x*2)<.001);assert(Math.abs(after.pan.y-before.pan.y*2)<.001);assert.equal(await p.locator('#viewZoomValue').textContent(),'200%');
 // A symmetric off-centre pinch must anchor the same plan point to its midpoint.
 const pinchBefore=await read();b=await p.locator('#canvas').boundingBox();const mx=b.x+b.width*.4,my=b.y+b.height*.4;
 await p.evaluate(({mx,my})=>{const c=document.querySelector('#canvas');c.setPointerCapture=()=>{};const fire=(type,id,x,y)=>c.dispatchEvent(new PointerEvent(type,{pointerId:id,pointerType:'touch',clientX:x,clientY:y,bubbles:true}));fire('pointerdown',41,mx-30,my);fire('pointerdown',42,mx+30,my);fire('pointermove',41,mx-60,my);fire('pointermove',42,mx+60,my);fire('pointerup',41,mx-60,my);fire('pointerup',42,mx+60,my)},{mx,my});
 after=await read();assert.equal(after.zoom,4);const offsetX=mx-b.x-b.width/2,offsetY=my-b.y-b.height/2;assert(Math.abs(after.pan.x-(offsetX-(offsetX-pinchBefore.pan.x)*2))<.001);assert(Math.abs(after.pan.y-(offsetY-(offsetY-pinchBefore.pan.y)*2))<.001);assert.equal(after.state.symbols.length,1);
 await p.locator('#viewFit').click();after=await read();assert.equal(after.zoom,1);assert.deepEqual(after.pan,{x:0,y:0});
 await p.waitForTimeout(800);await p.reload();await p.locator('#resumeProject').click();assert.equal((await read()).state.symbols[0].reference,'L1-043');assert.equal((await read()).state.symbols[0].color,'#2675db');
 await p.locator('#surveyModeBtn').click();for(const width of [390,1024]){await p.setViewportSize({width,height:844});assert(await p.locator('#surveySelect').isVisible());assert(await p.locator('#viewZoom').isVisible());assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));fs.mkdirSync('test-results',{recursive:true});await p.screenshot({path:`test-results/survey-edit-${width}.png`})}
 assert.deepEqual(errors,[]);console.log('PASS: survey device move, properties, tiny size, undo/redo, persistence, centre zoom, pinch anchor, Fit and responsive layout');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
