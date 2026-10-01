const fs=require('node:fs'),http=require('node:http'),assert=require('node:assert/strict');
const {chromium,webkit}=require('playwright');
const {openHeader}=require('./header-navigation.cjs');
const server=http.createServer((req,res)=>{try{const file=(req.url||'/').split('?')[0].slice(1)||'index.html';res.end(fs.readFileSync(file))}catch{res.statusCode=404;res.end()}}).listen(0,'127.0.0.1');
(async()=>{
 await new Promise(r=>server.once('listening',r));
 const browser=await(process.env.BROWSER==='webkit'?webkit:chromium).launch();
 try{
  const page=await browser.newPage({viewport:{width:390,height:844},hasTouch:true});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.locator('#zsSplash').waitFor({state:'detached'});
  await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);
  for(const system of ['cctv','security','access','fire']){
   await page.locator('#homeNew').tap();await page.locator('.newProjectChoice[data-system="'+system+'"]').tap();
   await page.locator('#newProjectName').fill('Survey menu '+system);
   await page.locator('#newProjectCreate').tap();
   await page.locator('#projectsHome').waitFor({state:'hidden'});
   await openHeader(page);
   await page.locator('#surveyModeBtn').tap();
   const sizes=system==='cctv'?[[320,568],[375,812],[412,915],[768,1024],[1280,800]]:[[390,844]];
   for(const [width,height] of sizes){
    await page.setViewportSize({width,height});
    await openHeader(page);
    assert(await page.locator('#floorBar').isVisible());
    assert(await page.locator('#shareBtn').isVisible());
    const expanded=await page.locator('#canvas').boundingBox();
    const toggle=page.locator('#topCollapseBtn');
    const target=await toggle.boundingBox();
    assert(target.width>=44&&target.height>=44&&target.x>=0&&target.x+target.width<=width+1);
    await toggle.tap();
    assert.equal(await toggle.getAttribute('aria-expanded'),'false');
    assert.equal(await toggle.innerText(),'Menu ▼');
    assert(!(await page.locator('#topMain').isVisible()));
    assert(!(await page.locator('#floorBar').isVisible()));
    assert(await page.locator('#surveyDevice').isVisible());
    const compact=await page.locator('#topBar').boundingBox(),drawing=await page.locator('#canvas').boundingBox();
    assert(compact.height<=64,'Collapsed survey header remains compact');
    assert(drawing.height>expanded.height+40,'Closing gives space back to the drawing');
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
    // The bottom device controls remain usable while the top menu is closed.
    await page.locator('#surveyDevice').tap();
    await page.locator('#symbolMenu.open').waitFor();
    await page.locator('#symbolMenu [data-symbol]:visible').first().tap();
    assert.equal(await page.locator('.toolPopup.open').count(),0,'Choosing a device closes the palette');
    await toggle.tap();
    assert.equal(await toggle.getAttribute('aria-expanded'),'true');
    assert(await page.locator('#surveyModeBtn').isVisible());
    if(system==='cctv'&&width===375){
     await toggle.tap();
     await page.screenshot({path:'/tmp/survey-menu-phone.png'});
     await page.setViewportSize({width:812,height:375});
     assert(!(await page.locator('#topMain').isVisible()));
     await toggle.tap();
     assert(await page.locator('#shareBtn').isVisible());
    }
   }
   await page.setViewportSize({width:390,height:844});
   await page.locator('#surveyModeBtn').tap();
   assert(await page.locator('#moveModeTop').isVisible(),'Plan controls restored');
   await page.locator('#headerHomeBtn').tap();
   await page.locator('#projectsHome').waitFor({state:'visible'});
  }
  assert.deepEqual(errors,[]);
  console.log('PASS survey menu: four systems, five layouts, touch close/reopen, drawing space, floor visibility, usable device tools, orientation change and return to plan');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);server.close();process.exit(1)});
