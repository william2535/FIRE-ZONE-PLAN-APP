const {chromium}=require('playwright');
const fs=require('node:fs');
const http=require('node:http');
const assert=require('node:assert/strict');
const sets={
 fire:['panel','repeater','mcp','smoke','heat','sounder','beacon','beam','io'],
 security:['secPir','secDualTech','secDoorContact','secPanic','secKeypad','secBell','secExpander','secPsu','secPanel'],
 cctv:['cctvFixed','cctvDome','cctvTurret','cctvPtz','cctvAnpr','cctvNvr','cctvPoe','cctvSwitch'],
 access:['accessReader','accessKeypad','accessMaglock','accessStrike','accessRte','accessBreakGlass','accessDoorContact','accessAcu','accessPsu']
};
const server=http.createServer((req,res)=>{try{const path=decodeURIComponent((req.url||'/').split('?')[0]);const file=path==='/'?'index.html':path.slice(1);res.end(fs.readFileSync(file))}catch{res.statusCode=404;res.end()}}).listen(0,'127.0.0.1');
(async()=>{await new Promise(ok=>server.once('listening',ok));const browser=await chromium.launch({headless:true});try{
 const page=await browser.newPage({viewport:{width:1280,height:800}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{window.AndroidBridge={shareFile:(data,name,mime)=>window.shared={data,name,mime}}});
 await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);
 const record=site=>page.evaluate(async site=>{const db=await new Promise((ok,no)=>{const r=indexedDB.open('ZoneSketch-v1',1);r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error)});return new Promise((ok,no)=>{const r=db.transaction('draft').objectStore('draft').openCursor();r.onsuccess=()=>{const c=r.result;if(!c)return ok(null);if(String(c.key).startsWith('project:')&&c.value.site===site)return ok(c.value);c.continue()};r.onerror=()=>no(r.error)})},site);
 const home=async()=>{await page.locator('#headerHomeBtn').click();await page.locator('#projectsHome').waitFor({state:'visible'})};
 for(const [system,types] of Object.entries(sets)){
  const site='Library '+system;await page.locator('.homeSystemTile[data-system="'+system+'"]').click();await page.locator('#newProjectName').fill(site);await page.locator('#newProjectCreate').click();await page.locator('#projectsHome').waitFor({state:'hidden'});
  await page.locator('#surveyModeBtn').click();await page.locator('#surveyDevice').click();
  const visible=await page.locator('#symbolMenu [data-symbol]:visible').evaluateAll(buttons=>buttons.map(b=>b.dataset.symbol));
  assert.deepEqual(new Set(visible),new Set(types),system+' palette');
  assert.equal(visible.length,types.length,system+' palette length');
  const first=types[0];await page.locator('#symbolMenu [data-symbol="'+first+'"]').click();
  await page.locator('#canvas').click({position:{x:330,y:220}});
  await page.waitForFunction(({site,first})=>document.querySelector('#saveIndicator').textContent.startsWith('Saved'),{site,first});
  await page.waitForTimeout(450);
  let saved=await record(site);assert.equal(saved.project.systemType,system);
  const symbols=saved.project.floors[0].data.symbols;assert(symbols.some(s=>s.type===first&&s.scope==='survey'),system+' placement');
  if(system!=='fire'){
   assert.equal(await page.evaluate(type=>{const c=document.createElement('canvas');c.width=c.height=80;drawSymbol(c.getContext('2d'),{x:40,y:40},type,15,'#346fdd');return [...c.getContext('2d').getImageData(0,0,80,80).data].some((v,i)=>i%4===3&&v>0)},first),true,system+' vector rendering');
  }
  await home();await page.reload();await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);
  const card=page.locator('.projectCard').filter({has:page.getByRole('heading',{name:site,exact:true})});await card.getByRole('button',{name:'Open',exact:true}).click();await page.locator('#projectsHome').waitFor({state:'hidden'});
  await page.locator('#surveyModeBtn').click();await page.locator('#surveyDevice').click();assert.deepEqual(new Set(await page.locator('#symbolMenu [data-symbol]:visible').evaluateAll(bs=>bs.map(b=>b.dataset.symbol))),new Set(types),system+' reopened palette');
  saved=await record(site);assert(saved.project.floors[0].data.symbols.some(s=>s.type===first),system+' reload');await home();
 }
 const card=page.locator('.projectCard').filter({has:page.getByRole('heading',{name:'Library cctv',exact:true})});
 await card.getByRole('button',{name:'Duplicate'}).click();assert((await record('Library cctv (copy)')).project.floors[0].data.symbols.some(s=>s.type==='cctvFixed'));
 await card.getByRole('button',{name:'Export'}).click();await page.waitForFunction(()=>!!window.shared);
 const backup=await page.evaluate(()=>JSON.parse(atob(window.shared.data.split(',')[1])));assert.equal(backup.project.systemType,'cctv');assert(backup.project.floors[0].data.symbols.some(s=>s.type==='cctvFixed'));
 await page.locator('#projectFile').setInputFiles({name:'library.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(backup))});await page.locator('#projectsHome').waitFor({state:'hidden'});assert.equal((await page.locator('#editorSystemIdentity').textContent()).trim(),'CCTV');await home();
 assert.equal(await page.locator('.projectCard').filter({has:page.getByRole('heading',{name:'Library cctv',exact:true})}).count(),2);
 assert.deepEqual(errors,[]);console.log('PASS: four isolated palettes, placement, vector rendering, reload, duplicate and backup import/export');
 }finally{await browser.close();server.close()}})().catch(e=>{console.error(e);server.close();process.exit(1)});
