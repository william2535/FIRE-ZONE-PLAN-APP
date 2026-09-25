const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');
(async()=>{
 const server=http.createServer((q,r)=>{const path=(q.url||'/').split('?')[0],file=path==='/'?'index.html':path.slice(1);try{const data=fs.readFileSync(file);r.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':'text/html');r.end(data)}catch(e){r.statusCode=404;r.end('not found')}}).listen(0,'127.0.0.1');
 await new Promise(r=>server.once('listening',r));const browser=await chromium.launch({headless:true});
 try{
  const p=await browser.newPage({viewport:{width:390,height:844}}),errors=[],alerts=[];
  p.on('pageerror',e=>errors.push(e.message));p.on('dialog',async d=>{if(d.type()==='alert')alerts.push(d.message());await d.accept(d.type()==='prompt'?'Site Ready Test':undefined)});
  await p.goto('http://127.0.0.1:'+server.address().port);
  assert(await p.locator('.homeProductHero').isVisible());
  assert.equal(await p.locator('.workflowStep').count(),4);
  assert.match(await p.locator('.homeVersion').innerText(),/v0\.49/i);
  await p.locator('#homeNew').click();await p.locator('#projectsHome').waitFor({state:'hidden'});

  // Settings live in the Project menu and persist their field preferences.
  await p.locator('#projectMenuBtn').click();await p.locator('#appSettingsBtn').click();await p.locator('#appSettingsModal').waitFor({state:'visible'});
  assert.match(await p.locator('.settingsFooter').innerText(),/v0\.49/i);
  await p.locator('#appHapticsSetting').click();
  assert.equal(await p.evaluate(()=>localStorage.getItem('zoneSketchHaptics')),'off');
  await p.locator('#appMotionSetting').click();
  assert.equal(await p.evaluate(()=>localStorage.getItem('zoneSketchReducedMotion')),'on');
  assert(await p.locator('body').evaluate(el=>el.classList.contains('reduceMotion')));
  await p.locator('#appSettingsClose').click();

  // Empty Circuit Builder states use an in-app notice rather than a browser alert.
  await p.locator('#circuitModeBtn').click();await p.locator('#cbAddressableStart').click();await p.locator('#appNoticeModal').waitFor({state:'visible'});
  assert.match(await p.locator('#appNoticeTitle').innerText(),/No surveyed devices/i);
  await p.locator('#appNoticeClose').click();await p.locator('#cbBack').click();

  // Survey picker is grouped, but device buttons remain the same stable controls.
  await p.locator('#surveyModeBtn').click();await p.locator('#surveyDevice').click();
  assert((await p.locator('.symbolCategory:visible').count())>=3);
  assert(await p.locator('[data-symbol="smoke"]').isVisible());
  const canvas=await p.locator('#canvas').boundingBox();
  await p.locator('[data-symbol="smoke"]').click();await p.mouse.click(canvas.x+canvas.width*.56,canvas.y+canvas.height*.48);
  const smokeToast=p.locator('.uiToast.success').filter({hasText:'Smoke added'});await smokeToast.waitFor({state:'visible'});assert.match(await smokeToast.innerText(),/Smoke added/);
  assert.match(await p.locator('#saveIndicator').getAttribute('data-state'),/saving|saved/);

  // The Circuit Builder still exposes the polished field controls and As-Fit validation surface.
  await p.locator('#surveyDevice').click();await p.locator('[data-symbol="panel"]').click();await p.mouse.click(canvas.x+canvas.width*.28,canvas.y+canvas.height*.48);
  await p.locator('#circuitModeBtn').click();
  assert(await p.locator('.cbLandingHero').isVisible());
  assert(await p.locator('#cbAsFitSummary').count()===1);
  assert.deepEqual(alerts,[],'Common v0.49 field states should not use browser alerts');
  assert.deepEqual(errors,[],'No v0.49 runtime errors');
  console.log('PASS: v0.49 presents a professional site-ready shell, saved preferences, notices, survey feedback and Circuit Builder polish');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
