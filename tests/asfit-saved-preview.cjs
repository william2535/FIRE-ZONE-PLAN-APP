const fs=require('node:fs'),http=require('node:http'),assert=require('node:assert/strict');
const {chromium}=require('playwright');
const expose=`window.asFitPreviewTest={
 seed:async(type)=>{const project=fresh();project.site='Saved As fit preview';project.image=blankImage();project.isBlank=true;project.symbols=[
  {id:'panel',type:'panel',scope:'plan',x:.12,y:.20},{id:'d0',type:'smoke',scope:'survey',x:.78,y:.20},{id:'d1',type:'heat',scope:'survey',x:.78,y:.80}];
  project.zones=[{id:'z',number:'1',name:'Test zone',color:'#d33'}];project.shapes=[{id:'area',zone:'z',points:[{x:0,y:0},{x:1,y:0},{x:1,y:1},{x:0,y:1}]}];await activateProject(uid(),project);hideProjects();openCircuitBuilder();const c=cbNewCircuit(type,cbSurveyDevices(),type==='conventional'?'z':null),A=c.layout.panel,B=c.layout.d0,C=c.layout.d1;
  c.sequence=['panel','d0','d1','panel'];c.legs=[{from:'panel',to:'d0',points:[A,B]},{from:'d0',to:'d1',points:[B,C]},{from:'d1',to:'panel',points:[C,{x:A.x,y:C.y},A]}];c.complete=true;
  if(type==='conventional'){c.sequence.pop();c.legs.pop();c.eolId='d1'}c.bridges=[{legIndex:0,point:{x:(A.x+B.x)/2,y:A.y},axis:'h'}];cbFinishAsFit();await saveNow();return state.activeFloor},
 read:()=>({screen:cbScreen,saved:cbHasSavedAsFit(),marker:JSON.stringify(state.asFit),bridges:JSON.stringify(cbCircuits()[0]?.bridges),segments:cbAsFitSegments().length}),
 reopen:()=>{closeCircuitBuilder();openCircuitBuilder()},
 openAfterReload:()=>{hideProjects();openCircuitBuilder()},
 probeDrawing:async()=>{let hits=0;const old=cbPaintBridgeMark;cbPaintBridgeMark=(...args)=>{hits++;return old(...args)};try{
  cbDrawAsFitPreview();const preview=hits,c=document.createElement('canvas');c.width=1200;c.height=900;cbDrawAsFitOn(c,1200,900,true);const png=hits;
  syncFloor();await renderModeFloorCanvas(activeFloor(),1200,'asfit');const record=hits;
  cbDrawCircuitBridges(c.getContext('2d'),cbCircuits()[0],1200,900,p=>({x:p.x*1200,y:p.y*900}));return{preview,png,record,editor:hits};
 }finally{cbPaintBridgeMark=old}},
 pureChecks:()=>{const data=recordCopy(state),c=data.circuits[0];const checks={saved:cbHasSavedAsFit(data)};
  c.editDraft={};checks.edit=cbHasSavedAsFit(data);delete c.editDraft;c.complete=false;checks.incomplete=cbHasSavedAsFit(data);c.complete=true;
  data.symbols.find(s=>s.id==='d0').x+=.1;checks.moved=cbHasSavedAsFit(data);data.symbols=recordCopy(state.symbols);
  data.circuits.push({...c,id:'new'});checks.added=cbHasSavedAsFit(data);data.circuits.pop();data.asFit.circuitIds=['old'];checks.wrongId=cbHasSavedAsFit(data);return checks},
 addEmptyFloor:async()=>{syncFloor();const data=fresh();data.image=blankImage();data.isBlank=true;const id=uid();state.floors.push({id,name:'Unfinished floor',data});await cbSwitchFloor(id);return id},
 switchFloor:id=>cbSwitchFloor(id),
 detachedRender:()=>{const data=recordCopy(state),project=recordCopy(state),floor=recordCopy(activeFloor()),floorImg=img,c=document.createElement('canvas');c.width=1200;c.height=900;
  cbDrawAsFitOn(c,1200,900,true);const original=c.toDataURL();const saved=state;try{state=fresh();cbDrawAsFitOn(c,1200,900,true,data,project,floor,floorImg);return original===c.toDataURL()}finally{state=saved}},
 staleReopen:()=>{cbSymbol('d0').x-=.10;closeCircuitBuilder();openCircuitBuilder();const first=cbScreen;closeCircuitBuilder();openCircuitBuilder();return{first,second:cbScreen,marker:state.asFit}},
 openEdit:()=>{cbOpenCircuit(cbCircuits()[0]);cbEnterEdit(cbCircuits()[0]);closeCircuitBuilder();openCircuitBuilder()}
};`;
const source=fs.readFileSync('index.html','utf8'),marker='ensureUiState();renderFloors();renderSymbolColors();';assert(source.includes(marker));
const html=source.replace(marker,expose+marker);
const server=http.createServer((q,r)=>{const file=(q.url||'/').split('?')[0].replace(/^\//,'')||'index.html';try{r.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':'text/html');r.end(file==='index.html'?html:fs.readFileSync(file))}catch{r.statusCode=404;r.end()}});
const settle=page=>page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
(async()=>{await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const browser=await chromium.launch({headless:true});try{
 for(const type of ['addressable','conventional'])for(const viewport of [{width:1280,height:900},{width:390,height:844}]){
  const page=await browser.newPage({viewport}),errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('dialog',d=>d.accept());
  await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);
  const floor=await page.evaluate(type=>asFitPreviewTest.seed(type),type);await settle(page);const original=await page.evaluate(()=>asFitPreviewTest.read());
  assert.equal(original.screen,'asfit');assert(original.saved&&original.segments>0);
  await page.evaluate(()=>asFitPreviewTest.reopen());await settle(page);
  assert.deepEqual(await page.evaluate(()=>asFitPreviewTest.read()),original,'Reopening must show the saved drawing without regenerating it');
  await page.locator('#cbAsFitBack').click();assert.equal(await page.locator('#cbFinishAsFitMain').textContent(),'View As fit drawing');
  await page.locator('#cbFinishAsFitMain').click();await settle(page);assert.deepEqual(await page.evaluate(()=>asFitPreviewTest.read()),original);
  assert.deepEqual(await page.evaluate(()=>asFitPreviewTest.pureChecks()),{saved:true,edit:false,incomplete:false,moved:false,added:false,wrongId:false});
  const probe=await page.evaluate(()=>asFitPreviewTest.probeDrawing());assert.equal(probe.preview,0);assert.equal(probe.png,0);assert.equal(probe.record,0);assert(probe.editor>0,'Bridge marks must still be available to the route editor');
  assert(await page.evaluate(()=>asFitPreviewTest.detachedRender()),'Home drawing must use its supplied floor, independently of the active project');
  await page.reload();await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);await page.evaluate(()=>asFitPreviewTest.openAfterReload());await settle(page);
  assert.deepEqual(await page.evaluate(()=>asFitPreviewTest.read()),original,'Saved drawing and bridge data must survive reload');
  await page.evaluate(()=>asFitPreviewTest.addEmptyFloor());assert.equal(await page.evaluate(()=>asFitPreviewTest.read().screen),'home');
  await page.evaluate(id=>asFitPreviewTest.switchFloor(id),floor);await settle(page);assert.deepEqual(await page.evaluate(()=>asFitPreviewTest.read()),original,'Returning to a completed floor must show its own drawing');
  await page.evaluate(()=>asFitPreviewTest.openEdit());assert.equal(await page.evaluate(()=>asFitPreviewTest.read().screen),'home','An open route edit must not appear as a completed drawing');
  await page.evaluate(type=>asFitPreviewTest.seed(type),type);assert.deepEqual(await page.evaluate(()=>asFitPreviewTest.staleReopen()),{first:'home',second:'home',marker:null},'Stale geometry must stay unavailable on repeated reopen');assert.deepEqual(errors,[]);await page.close();
 }
 console.log('PASS: saved As fit previews reopen on desktop/mobile and after reload, reject stale/open routes, render independently, and omit bridge glyphs while preserving editor bridges');
 }finally{await browser.close();server.close()}})().catch(e=>{console.error(e);server.close();process.exit(1)});
