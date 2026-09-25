const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');

const source=fs.readFileSync('index.html','utf8');
assert(source.includes('function cbEditorDeleteAt'),'editor foundation was not generated into index.html');
const expose=`window.cbEditorFoundationTest={
 read:()=>JSON.parse(JSON.stringify({c:cbCircuit,editor:cbEditor,undo:cbEditUndo.length,redo:cbEditRedo.length,visible:cbVisibleSegments(cbCircuit).map(s=>s.key),asFit:state.asFit})),
 seed:async()=>{state=fresh();state.image=blankImage();state.isBlank=true;state.symbols=[
  {id:'panel',type:'panel',scope:'plan',x:.10,y:.42},
  {id:'d0',type:'smoke',scope:'survey',x:.42,y:.42},
  {id:'d1',type:'heat',scope:'survey',x:.76,y:.67}
 ];await setImage(state.image,false);ensureFloors();openCircuitBuilder();const c=cbNewCircuit('conventional',cbSurveyDevices());const p=c.layout.panel,d0=c.layout.d0,d1=c.layout.d1;c.sequence=['panel','d0','d1'];c.legs=[
  {from:'panel',to:'d0',points:[{...p},{x:d0.x,y:p.y},{...d0}]},
  {from:'d0',to:'d1',points:[{...d0},{x:d1.x,y:d0.y},{...d1}]}
 ];c.complete=true;c.editOpen=false;c.editCuts=[];state.asFit={stale:true};cbOpenCircuit(c);cbUpdateGame();},
 firstSegmentMid:()=>{const r=$('cbCanvas').getBoundingClientRect(),s=cbVisibleSegments(cbCircuit)[0],a=cbBoardPx(s.a,r.width,r.height),b=cbBoardPx(s.b,r.width,r.height);return{x:r.left+(a.x+b.x)/2,y:r.top+(a.y+b.y)/2}},
 validate:()=>cbEditorValidation()
};`;
const html=source.replace('ensureUiState();renderFloors();renderSymbolColors();',expose+'ensureUiState();renderFloors();renderSymbolColors();');
const server=http.createServer((q,r)=>{const file=(q.url||'/').split('?')[0]==='/'?'index.html':(q.url||'').split('?')[0].slice(1);try{r.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':'text/html');r.end(file==='index.html'?html:fs.readFileSync(file))}catch{r.statusCode=404;r.end()}}).listen(0,'127.0.0.1');

(async()=>{
 await new Promise(ok=>server.once('listening',ok));
 const browser=await chromium.launch({headless:true});
 try{
  for(const viewport of [{name:'iphone',width:390,height:844},{name:'tablet',width:820,height:1180}]){
   const page=await browser.newPage({viewport});page.on('dialog',d=>d.accept());
   await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);
   await page.evaluate(async()=>{document.querySelector('#projectsHome').hidden=true;await cbEditorFoundationTest.seed()});await page.waitForTimeout(40);
   assert.equal(await page.locator('#cbEditToggle').isVisible(),true,viewport.name+': Edit must sit beside zoom controls');
   await page.click('#cbEditToggle');
   let snap=await page.evaluate(()=>cbEditorFoundationTest.read());
   assert.equal(snap.editor.active,true,viewport.name+': Edit must enter explicit editor state');
   assert.equal(snap.editor.bridge,false,viewport.name+': Bridge must default OFF');
   assert.equal(await page.locator('#cbEditDock').isVisible(),true,viewport.name+': editor controls must be visible');
   assert.equal(await page.locator('#cbEditStatus').textContent(),'EDITING · ROUTE VALID');
   assert.equal(await page.locator('#cbEditUndo').isDisabled(),true);
   assert.equal(await page.locator('#cbEditRedo').isDisabled(),true);

   // Bridge is explicit and does not silently persist after leaving edit mode.
   await page.click('#cbEditBridge');snap=await page.evaluate(()=>cbEditorFoundationTest.read());assert.equal(snap.editor.bridge,true,viewport.name+': Bridge toggle must become explicit ON state');
   assert.equal(await page.locator('#cbEditBridge').getAttribute('aria-pressed'),'true');
   await page.click('#cbEditBridge');snap=await page.evaluate(()=>cbEditorFoundationTest.read());assert.equal(snap.editor.bridge,false);

   // Cleaning strength is stored as a circuit/editor setting, independent of live pointer geometry.
   await page.locator('#cbEditCleanup').evaluate(el=>{el.value='75';el.dispatchEvent(new Event('input',{bubbles:true}))});
   snap=await page.evaluate(()=>cbEditorFoundationTest.read());assert.equal(snap.editor.cleanup,75);assert.equal(snap.c.editCleanup,75);assert.equal(await page.locator('#cbEditCleanupValue').textContent(),'75%');

   // Bin is local cable surgery: one intentional tap removes exactly one segment and no device.
   const devicesBefore=snap.c.deviceIds.slice();const visibleBefore=snap.visible.length;
   await page.click('#cbEditBin');const mid=await page.evaluate(()=>cbEditorFoundationTest.firstSegmentMid());await page.mouse.click(mid.x,mid.y);await page.waitForTimeout(30);
   snap=await page.evaluate(()=>cbEditorFoundationTest.read());
   assert.deepEqual(snap.c.deviceIds,devicesBefore,viewport.name+': Bin must never delete a device');
   assert.equal(snap.c.editCuts.length,1,viewport.name+': one tap must cut one local cable segment');
   assert.equal(snap.visible.length,visibleBefore-1,viewport.name+': exactly one rendered cable segment must disappear');
   assert.equal(snap.c.complete,false,viewport.name+': a broken route cannot remain COMPLETE');
   assert.equal(snap.c.editOpen,true,viewport.name+': a cut must persist EDITING · ROUTE OPEN');
   assert.equal(snap.asFit,null,viewport.name+': a route cut must invalidate stale As-Fit output');
   assert.equal(await page.locator('#cbEditStatus').textContent(),'EDITING · ROUTE OPEN');
   assert.equal(await page.locator('#cbEditUndo').isDisabled(),false);
   assert.match((await page.evaluate(()=>cbEditorFoundationTest.validate())).message,/open cable section/);

   // Done must reject an open topology.
   await page.click('#cbEditDone');snap=await page.evaluate(()=>cbEditorFoundationTest.read());assert.equal(snap.editor.active,true);assert.equal(snap.c.editOpen,true);assert.equal(snap.c.complete,false);

   // Dedicated editor undo/redo restores exact topology/completion state.
   await page.click('#cbEditUndo');snap=await page.evaluate(()=>cbEditorFoundationTest.read());assert.equal(snap.c.editCuts.length,0);assert.equal(snap.c.complete,true);assert.equal(snap.c.editOpen,false);assert.equal(snap.visible.length,visibleBefore);
   await page.click('#cbEditRedo');snap=await page.evaluate(()=>cbEditorFoundationTest.read());assert.equal(snap.c.editCuts.length,1);assert.equal(snap.c.complete,false);assert.equal(snap.c.editOpen,true);assert.equal(snap.visible.length,visibleBefore-1);
   await page.click('#cbEditUndo');await page.click('#cbEditDone');snap=await page.evaluate(()=>cbEditorFoundationTest.read());assert.equal(snap.editor.active,false);assert.equal(snap.c.complete,true);assert.equal(snap.c.editOpen,false);

   // Reopening editor starts safe: Bridge OFF and persisted cleanup strength retained.
   await page.click('#cbEditToggle');snap=await page.evaluate(()=>cbEditorFoundationTest.read());assert.equal(snap.editor.bridge,false);assert.equal(snap.editor.cleanup,75);
   assert.equal((await page.locator('.cbRowEdit').count())>=1,true,viewport.name+': created circuit list needs edit affordance');
   assert.equal((await page.locator('.cbZoneEditButton').count())>=1,true,viewport.name+': left zone list needs edit affordance');
   await page.close();
  }
 }finally{await browser.close();server.close()}
 console.log('PASS: Circuit Builder editor foundation preserves topology/state invariants across phone and tablet');
})().catch(e=>{console.error(e);server.close();process.exit(1)});
