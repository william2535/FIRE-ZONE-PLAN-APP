const {chromium,webkit}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');
(async()=>{
 const server=http.createServer((q,r)=>{const f=(q.url.split('?')[0]==='/'?'index.html':q.url.split('?')[0].slice(1));try{r.setHeader('Content-Type',f.endsWith('.js')?'text/javascript':f.endsWith('.png')?'image/png':f.endsWith('.webp')?'image/webp':f.endsWith('.svg')?'image/svg+xml':'text/html');r.end(fs.readFileSync(f))}catch{r.statusCode=404;r.end()}}).listen(0,'127.0.0.1');await new Promise(r=>server.once('listening',r));
 const engine=process.env.PINEAPPLE_BROWSER==='webkit'?webkit:chromium,browser=await engine.launch();
 try{for(const size of [[320,568],[375,812],[390,844],[430,932]]){
  const context=await browser.newContext({viewport:{width:size[0],height:size[1]},isMobile:true,hasTouch:true,deviceScaleFactor:2});const page=await context.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('dialog',d=>d.accept(d.type()==='prompt'?'Portrait menu QA':undefined));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);await page.locator('#zsSplash').waitFor({state:'hidden'});await page.locator('#homeNew').tap();await page.locator('#projectsHome').waitFor({state:'hidden'});
  const toggle=page.locator('#topCollapseBtn'),main=page.locator('#topMain');
  assert.equal(await toggle.getAttribute('aria-expanded'),'false');assert.equal(await main.isVisible(),false,'portrait Menu closed must hide topMain');
  const compact=async()=>{
   assert.equal(await page.locator('#moveModeTop').isVisible(),false,'Move hides with the menu');
   assert.deepEqual(await page.locator('#topEssential>button:visible').evaluateAll(els=>els.map(el=>el.id)),['deleteTop','undoTop','redoTop','topCollapseBtn']);
   const b=await toggle.boundingBox();assert.equal(b.width,44);assert(b.height>=44);
   assert.equal(await page.locator('#floorBar').isVisible(),false);
  };
  await compact();
  for(let i=0;i<3;i++){
   await toggle.tap();assert.equal(await toggle.getAttribute('aria-expanded'),'true');assert(await main.isVisible());assert(await page.locator('#moveModeTop').isVisible());
   const box=await toggle.boundingBox();assert(box.width>=84&&box.height>=44);assert(box.x>=0&&box.x+box.width<=size[0]+1);
   await page.locator('#projectMenuBtn').tap();await page.locator('#projectMenu').waitFor({state:'visible'});
   await toggle.tap();assert.equal(await toggle.getAttribute('aria-expanded'),'false');assert.equal(await main.isVisible(),false);assert.equal(await page.locator('#projectMenu').isVisible(),false);await compact();
  }
  await page.setViewportSize({width:size[1],height:size[0]});assert.equal(await main.isVisible(),false);await toggle.tap();assert(await main.isVisible());await page.setViewportSize({width:size[0],height:size[1]});await toggle.tap();assert.equal(await main.isVisible(),false);
  await toggle.tap();await page.locator('#headerHomeBtn').tap();await page.locator('#projectsHome').waitFor({state:'visible'});await page.locator('#resumeProject').tap();await page.locator('#projectsHome').waitFor({state:'hidden'});await toggle.tap();assert.equal(await main.isVisible(),false);
  await toggle.tap();await page.locator('#surveyModeBtn').tap();assert(await page.locator('#surveyTools').isVisible());await page.locator('#surveyModeBtn').tap();await toggle.tap();assert.equal(await main.isVisible(),false);
  assert.deepEqual(errors,[]);await page.screenshot({path:`test-results/iphone-menu-${process.env.PINEAPPLE_BROWSER||'chromium'}-${size[0]}.png`});await context.close();console.log('PASS real portrait taps, popup close, rotation, Home and Survey at '+size[0]);
 }}finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
