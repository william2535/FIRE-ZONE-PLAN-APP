const {chromium}=require('playwright');
const fs=require('fs'),http=require('http'),assert=require('node:assert/strict');

(async()=>{
 const source=fs.readFileSync('index.html','utf8');
 const html=source.replace(
  'ensureUiState();renderFloors();renderSymbolColors();',
  `window.v041Test={
    read:()=>({state:JSON.parse(JSON.stringify(state)),imgW:img?.width||0,imgH:img?.height||0,zoom}),
    screen:p=>screenPoint(p),
    setWalls:walls=>{state.walls=walls.map((w,i)=>({id:'test-wall-'+i,kind:'wall',group:null,points:w.map(p=>({...p}))}));mergeOverlappingWalls();return JSON.parse(JSON.stringify(state.walls))},
    splitDoor:(wallId,a,b)=>{const ok=splitWallForObject(wallId,a,b,'door',1);return{ok,walls:JSON.parse(JSON.stringify(state.walls)),doors:JSON.parse(JSON.stringify(state.doors))}},
    shutter:length=>shutterVisualMetrics(length)
  };ensureUiState();renderFloors();renderSymbolColors();`
 );
 const server=http.createServer((req,res)=>{
  const path=(req.url||'/').split('?')[0];
  if(path==='/'){res.setHeader('Content-Type','text/html');res.end(html);return}
  const file=path.slice(1);
  try{const data=fs.readFileSync(file);res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':'application/octet-stream');res.end(data)}catch(e){res.statusCode=404;res.end('not found')}
 }).listen(0,'127.0.0.1');
 await new Promise(ok=>server.once('listening',ok));
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1180,height:820}}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  page.on('dialog',d=>d.accept(d.type()==='prompt'?'v0.41 test':undefined));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.waitForFunction(()=>!document.getElementById('homeNew').disabled);
  await page.locator('#homeNew').click();
  await page.locator('#projectsHome').waitFor({state:'hidden'});
  if(await page.locator('#emptyBlank').isVisible())await page.locator('#emptyBlank').click();
  await page.waitForFunction(()=>!document.getElementById('empty').offsetParent);

  // Survey grid has direct smaller/larger controls. Changing spacing from them
  // also enables snap because these controls are specifically for placement.
  await page.locator('#surveyModeBtn').click();
  await page.locator('#canvasOptionsBtn').click();
  await page.locator('#surveyGridSize').selectOption('20');
  await page.mouse.click(760,300);
  await page.locator('#surveyGridDown').click();
  let read=await page.evaluate(()=>window.v041Test.read());
  assert.equal(read.state.gridSize,10);
  assert.equal(read.state.gridVisible,true);
  assert.equal(read.state.snapGrid,true);
  assert.match(await page.locator('#surveyMove').innerText(),/10/);
  await page.locator('#surveyGridUp').click();
  read=await page.evaluate(()=>window.v041Test.read());
  assert.equal(read.state.gridSize,20);

  // A new survey device must land on an actual visible grid intersection.
  await page.locator('#surveyDevice').click();
  await page.locator('[data-symbol="smoke"]').click();
  const box=await page.locator('#canvas').boundingBox();
  await page.mouse.click(box.x+box.width*.573,box.y+box.height*.417);
  await page.waitForTimeout(120);
  read=await page.evaluate(()=>window.v041Test.read());
  assert.equal(read.state.symbols.length,1);
  let sm=read.state.symbols[0];
  const isMultiple=(value,step)=>Math.abs(value/step-Math.round(value/step))<1e-7;
  assert.equal(isMultiple(sm.x*read.imgW,20),true,'placed device x should be on grid');
  assert.equal(isMultiple(sm.y*read.imgH,20),true,'placed device y should be on grid');

  // Moving an existing device must snap its FINAL coordinate, not merely its
  // movement delta (which used to preserve an arbitrary off-grid offset).
  await page.locator('#surveySelect').click();
  let q=await page.evaluate(()=>{const s=window.v041Test.read().state.symbols[0],p=window.v041Test.screen(s),r=document.querySelector('#canvas').getBoundingClientRect();return{x:p.x+r.left,y:p.y+r.top}});
  await page.mouse.click(q.x,q.y);
  await page.mouse.move(q.x,q.y);await page.mouse.down();await page.mouse.move(q.x+37,q.y+23,{steps:5});await page.mouse.up();
  read=await page.evaluate(()=>window.v041Test.read());sm=read.state.symbols[0];
  assert.equal(isMultiple(sm.x*read.imgW,20),true,'moved device x should be on grid');
  assert.equal(isMultiple(sm.y*read.imgH,20),true,'moved device y should be on grid');

  // Small-room parallel walls must stay separate. The old .003 normalized
  // tolerance could collapse these into one wall on a large plan.
  const room=await page.evaluate(()=>window.v041Test.setWalls([
   [{x:.30,y:.30},{x:.3025,y:.30}],
   [{x:.3025,y:.30},{x:.3025,y:.32}],
   [{x:.3025,y:.32},{x:.30,y:.32}],
   [{x:.30,y:.32},{x:.30,y:.30}]
  ]));
  assert.equal(room.length,4,'all four small-room walls should survive merging');
  const verticalXs=room.filter(w=>Math.abs(w.points[0].x-w.points[1].x)<1e-8).map(w=>w.points[0].x).sort();
  assert.equal(verticalXs.length,2);
  assert(verticalXs[1]-verticalXs[0]>.002,'opposite walls must remain distinct');

  // Cutting a door into the tiny room must only split its target wall and must
  // not consume either perpendicular side wall.
  const top=room.find(w=>Math.abs(w.points[0].y-.30)<1e-8&&Math.abs(w.points[1].y-.30)<1e-8);
  assert(top);
  const afterDoor=await page.evaluate(({id})=>window.v041Test.splitDoor(id,.2,.8),{id:top.id});
  assert.equal(afterDoor.ok,true);
  assert.equal(afterDoor.doors.length>=1,true);
  const afterVertical=afterDoor.walls.filter(w=>Math.abs(w.points[0].x-w.points[1].x)<1e-8);
  assert.equal(afterVertical.length,2,'door cut must preserve both side walls');

  // Roller-shutter hatch depth must shrink with zoom instead of keeping a
  // fixed 3px minimum and appearing to grow as the plan gets smaller.
  const metrics=await page.evaluate(()=>({far:window.v041Test.shutter(20),near:window.v041Test.shutter(100)}));
  assert(metrics.far.tick<metrics.near.tick);
  assert(metrics.far.tick/20<.08);
  assert(metrics.near.tick/100<.08);

  assert.deepEqual(errors,[]);
  fs.mkdirSync('test-results',{recursive:true});
  await page.screenshot({path:'test-results/v041-grid-door-shutter.png'});
  console.log('PASS v0.41: exact Survey grid snap, absolute snapped moves, small-room door wall preservation and zoom-stable roller shutter');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
