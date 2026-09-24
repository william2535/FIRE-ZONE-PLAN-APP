const {chromium}=require('playwright');
const fs=require('fs'),http=require('http'),assert=require('node:assert/strict');

(async()=>{
 const server=http.createServer((req,res)=>{
  const path=(req.url||'/').split('?')[0],file=path==='/'?'index.html':path.slice(1);
  try{
   const data=fs.readFileSync(file);
   res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':file.endsWith('.pdf')?'application/pdf':'text/html');
   res.end(data);
  }catch(e){res.statusCode=404;res.end('not found')}
 }).listen(0,'127.0.0.1');
 await new Promise(ok=>server.once('listening',ok));
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1180,height:820}}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  page.on('dialog',d=>d.accept(d.type()==='prompt'?'Favourites test':undefined));
  await page.goto('http://127.0.0.1:'+server.address().port);
  await page.waitForFunction(()=>!document.getElementById('homeNew').disabled);
  await page.locator('#homeNew').click();
  await page.locator('#projectsHome').waitFor({state:'hidden'});
  if(await page.locator('#emptyBlank').isVisible())await page.locator('#emptyBlank').click();
  await page.waitForFunction(()=>!document.getElementById('empty').offsetParent);

  await page.locator('#surveyModeBtn').click();
  assert.equal(await page.locator('.app').evaluate(el=>el.classList.contains('surveyMode')),true);
  assert.equal(await page.locator('#surveyFavouriteRail').isVisible(),true);

  await page.locator('#canvasOptionsBtn').click();
  const gridValues=await page.locator('#surveyGridSize option').evaluateAll(os=>os.map(o=>o.value));
  for(const value of ['5','10','20'])assert.equal(gridValues.includes(value),true,'Survey grid should keep '+value+' as a spacing choice');
  await page.locator('#surveyGridSize').selectOption('5');
  assert.equal(await page.locator('#surveyGridSize').inputValue(),'5');
  // Do not close this Survey popup by touching the canvas; that intentionally
  // places the currently selected device.
  await page.keyboard.press('Escape');

  await page.locator('#surveyDevice').click();
  assert.equal(await page.locator('[data-symbol="beam"]').isVisible(),true);
  assert.equal(await page.locator('[data-symbol="io"]').isVisible(),true);
  await page.locator('[data-symbol="beam"]').click();
  await page.locator('#surveyDevice').click();
  await page.locator('#symbolStampScale').fill('1.5');
  await page.locator('[aria-label="Symbol colour #e33a3a"]').click();
  await page.locator('#saveSurveyFavourite').click();
  let favs=await page.evaluate(()=>JSON.parse(localStorage.getItem('zoneSketchSurveyDeviceFavouritesV1')));
  assert.equal(favs.length,1);
  assert.equal(favs[0].type,'beam');
  assert.equal(favs[0].color.toLowerCase(),'#e33a3a');
  assert.equal(favs[0].scale,1.5);
  assert.equal(await page.locator('#surveyFavouriteButtons .surveyFavouriteQuick').count(),1);

  await page.locator('#surveyFavouriteButtons .surveyFavouriteQuick').first().click();
  const box=await page.locator('#canvas').boundingBox();
  await page.mouse.click(box.x+box.width*.56,box.y+box.height*.42);
  await page.waitForTimeout(300);

  await page.locator('#surveyDevice').click();
  await page.locator('[data-symbol="io"]').click();
  await page.locator('#surveyDevice').click();
  await page.locator('#symbolStampScale').fill('0.75');
  await page.locator('[aria-label="Symbol colour #2675db"]').click();
  await page.locator('#saveSurveyFavourite').click();
  favs=await page.evaluate(()=>JSON.parse(localStorage.getItem('zoneSketchSurveyDeviceFavouritesV1')));
  assert.equal(favs.length,2);
  assert.equal(favs[1].type,'io');
  assert.equal(favs[1].color.toLowerCase(),'#2675db');
  assert.equal(favs[1].scale,0.75);
  assert.equal(await page.locator('#surveyFavouriteButtons .surveyFavouriteQuick').count(),2);

  await page.locator('#surveyFavouriteButtons .surveyFavouriteQuick').nth(1).click();
  await page.mouse.click(box.x+box.width*.68,box.y+box.height*.52);
  await page.waitForTimeout(450);

  const saved=await page.evaluate(()=>new Promise(ok=>{
   const r=indexedDB.open('ZoneSketch-v1',1);
   r.onsuccess=()=>{const db=r.result,g=db.transaction('draft').objectStore('draft').get('state');g.onsuccess=()=>{ok(g.result);db.close()}};
  }));
  const surveySymbols=saved.symbols.filter(s=>s.scope==='survey');
  assert.equal(surveySymbols.some(s=>s.type==='beam'&&s.color.toLowerCase()==='#e33a3a'&&Math.abs(s.scale-1.5)<.001),true);
  assert.equal(surveySymbols.some(s=>s.type==='io'&&s.color.toLowerCase()==='#2675db'&&Math.abs(s.scale-.75)<.001),true);

  await page.locator('#countsMenuBtn').click();
  assert.match(await page.locator('#floorDeviceCounts').innerText(),/Beam detector/);
  assert.match(await page.locator('#floorDeviceCounts').innerText(),/I\/O unit/);

  await page.reload();
  await page.waitForFunction(()=>!document.getElementById('homeNew').disabled);
  if(await page.locator('#resumeProject').isVisible())await page.locator('#resumeProject').click();
  if(!await page.locator('.app').evaluate(el=>el.classList.contains('surveyMode')))await page.locator('#surveyModeBtn').click();
  assert.equal(await page.locator('#surveyFavouriteButtons .surveyFavouriteQuick').count(),2);
  assert.equal((await page.locator('#surveyFavouriteButtons .surveyFavouriteQuick').first().innerText()).includes('Beam'),true);

  await page.evaluate(()=>{
   const types=['smoke','heat','mcp','sounder','beacon','beam','io','panel','repeater'];
   localStorage.setItem('zoneSketchSurveyDeviceFavouritesV1',JSON.stringify(types.map((type,i)=>({type,color:['#172333','#e33a3a','#2675db'][i%3],scale:1}))));
  });
  await page.reload();
  await page.waitForFunction(()=>!document.getElementById('homeNew').disabled);
  if(await page.locator('#resumeProject').isVisible())await page.locator('#resumeProject').click();
  if(!await page.locator('.app').evaluate(el=>el.classList.contains('surveyMode')))await page.locator('#surveyModeBtn').click();
  assert.equal(await page.locator('#surveyFavouriteButtons .surveyFavouriteQuick').count(),9);
  await page.locator('#surveyDevice').click();
  assert.equal(await page.locator('#saveSurveyFavourite').isDisabled(),true);

  assert.deepEqual(errors,[]);
  console.log('PASS: survey grid choices, Beam/I-O devices, colour/size survey favourites, persistence and 9-slot side rail');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
