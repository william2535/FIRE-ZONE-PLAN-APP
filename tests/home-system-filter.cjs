const fs=require('node:fs'),http=require('node:http'),assert=require('node:assert/strict');
const {chromium,webkit}=require('playwright');
const {openHeader}=require('./header-navigation.cjs');
const server=http.createServer((req,res)=>{try{const file=(req.url||'/').split('?')[0].slice(1)||'index.html';res.end(fs.readFileSync(file))}catch{res.statusCode=404;res.end()}}).listen(0,'127.0.0.1');
(async()=>{await new Promise(r=>server.once('listening',r));const browser=await(process.env.BROWSER==='webkit'?webkit:chromium).launch();try{
 const page=await browser.newPage({viewport:{width:390,height:844},hasTouch:true}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.locator('#zsSplash').waitFor({state:'detached'});await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);
 const home=async()=>{await openHeader(page);await page.locator('#headerHomeBtn').tap();await page.locator('#projectsHome').waitFor({state:'visible'})};
 const count=async n=>page.waitForFunction(n=>document.querySelectorAll('.projectCard').length===n,n);
 for(const system of ['fire','security','cctv','access']){await page.locator('#homeNew').tap();await page.locator('.newProjectChoice[data-system="'+system+'"]').tap();await page.locator('#newProjectName').fill(system==='fire'?'Legacy Fire':'Depot '+system);await page.locator('#newProjectCreate').tap();await page.locator('#projectsHome').waitFor({state:'hidden'});await home()}
 // Simulate a genuine old backup record with no system field: it belongs in Fire.
 await page.evaluate(()=>new Promise((resolve,reject)=>{const r=indexedDB.open('ZoneSketch-v1',1);r.onsuccess=()=>{const tx=r.result.transaction('draft','readwrite'),cursor=tx.objectStore('draft').openCursor();cursor.onsuccess=()=>{const c=cursor.result;if(!c)return;if(String(c.key).startsWith('project:')&&c.value.site==='Legacy Fire'){const record=c.value;delete record.systemType;delete record.project.systemType;c.update(record)}c.continue()};tx.oncomplete=resolve;tx.onerror=()=>reject(tx.error)}}));
 await page.reload();await page.locator('#zsSplash').waitFor({state:'detached'});await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);await count(4);
 const records=()=>page.evaluate(()=>new Promise(resolve=>{const r=indexedDB.open('ZoneSketch-v1',1);r.onsuccess=()=>{const data=[],cursor=r.result.transaction('draft').objectStore('draft').openCursor();cursor.onsuccess=()=>{const c=cursor.result;if(!c)return resolve(data);if(String(c.key).startsWith('project:'))data.push(c.value);c.continue()}}}));const before=await records();
 for(const [width,height] of [[320,568],[390,844],[412,915],[768,1024],[1280,800]]){
  await page.setViewportSize({width,height});
  for(const [system,name] of [['fire','Fire'],['security','Security'],['cctv','CCTV'],['access','Access Control']]){
   const tile=page.locator('.homeSystemTile[data-system="'+system+'"]');await tile.tap();await count(1);
   assert(await page.locator('#newProjectDialog').isHidden());assert.equal(await tile.getAttribute('aria-pressed'),'true');assert.equal(await page.locator('.homeSystemTile[aria-pressed="true"]').count(),1);
   assert.equal(await page.locator('.projectIdentity').textContent(),name);assert((await page.locator('#homeMessage').innerText()).includes('1 of 4'));
   const box=await tile.boundingBox();assert(box.height>=44&&box.x>=0&&box.x+box.width<=width+1);
  }
  await page.locator('#homeShowAll').tap();await count(4);assert.equal(await page.locator('.homeSystemTile[aria-pressed="true"]').count(),0);
 }
 // Search combines with the system filter, including an honest empty result.
 await page.locator('.homeSystemTile[data-system="cctv"]').tap();await count(1);await page.locator('#projectSearch').fill('DEPOT');await count(1);await page.locator('#projectSearch').fill('Legacy');await count(0);assert.match(await page.locator('#homeMessage').textContent(),/No CCTV plans match/);
 await page.locator('#homeShowAll').tap();await count(4);assert.equal(await page.locator('#projectSearch').inputValue(),'');
 // Keyboard and rapid selections obey the final selected system.
 await page.locator('.homeSystemTile[data-system="security"]').focus();await page.keyboard.press('Enter');await count(1);assert.equal(await page.locator('.projectIdentity').textContent(),'Security');
 await page.evaluate(()=>{for(const type of ['fire','access','security','cctv'])document.querySelector('.homeSystemTile[data-system="'+type+'"]').click()});await count(1);await page.waitForFunction(()=>document.querySelector('.projectIdentity')?.textContent==='CCTV');assert.deepEqual(await records(),before,'Filtering does not rewrite project data');
 await page.locator('#homeNew').tap();assert.equal(await page.locator('.newProjectChoice[aria-pressed="true"]').getAttribute('data-system'),'cctv');await page.locator('#newProjectCancel').tap();await count(1);
 await page.getByRole('button',{name:'Duplicate',exact:true}).tap();await count(2);assert((await page.locator('.projectIdentity').allTextContents()).every(x=>x==='CCTV'));
 await page.locator('#homeNew').tap();await page.locator('#newProjectName').fill('New CCTV job');await page.locator('#newProjectCreate').tap();await page.locator('#projectsHome').waitFor({state:'hidden'});await home();await count(3);assert.equal(await page.locator('.homeSystemTile[data-system="cctv"]').getAttribute('aria-pressed'),'true');
 await page.setViewportSize({width:390,height:844});await page.locator('.homeSystemTile[data-system="cctv"]').scrollIntoViewIfNeeded();await page.screenshot({path:'/tmp/home-system-filter-phone.png'});
 assert.deepEqual(errors,[]);console.log('PASS Home system filters: four systems, legacy Fire default, five touch layouts, counts, search/empty state, Show all, keyboard/rapid selection, unchanged data, duplication and new-project preselection');
 }finally{await browser.close();server.close()}})().catch(e=>{console.error(e);server.close();process.exit(1)});
