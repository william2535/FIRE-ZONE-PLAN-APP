const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');
const source=fs.readFileSync('index.html','utf8');
for(const required of ['id="cbBridgeToggle"','function cbBuildBridgeSyncUi','function cbBuildBridgeHits'])assert(source.includes(required),`build bridge regression missing ${required}`);
const expose=`window.cbBuildBridgeTest={
 seed:async()=>{state=fresh();state.image=blankImage();state.isBlank=true;state.zones=[{id:'z1',number:1,name:'Test zone',color:'#df3f36'}];state.symbols=[
  {id:'panel',type:'panel',scope:'plan',x:.12,y:.50},{id:'d0',type:'smoke',scope:'survey',zoneId:'z1',x:.35,y:.50},{id:'d1',type:'heat',scope:'survey',zoneId:'z1',x:.70,y:.75}
 ];await setImage(state.image,false);ensureFloors();openCircuitBuilder();const c=cbNewCircuit('conventional',[cbSymbol('d0'),cbSymbol('d1')],'z1');c.sequence=['panel','d0'];c.legs=[{from:'panel',to:'d0',points:[{x:.18,y:.50},{x:.82,y:.50}]}];c.bridges=[];cbOpenCircuit(c);cbPaintBoard();return c.id},
 probe:()=>{const r=$('cbCanvas').getBoundingClientRect(),path=[cbBoardPx({x:.50,y:.18},r.width,r.height),cbBoardPx({x:.50,y:.82},r.width,r.height)],blocked=cbChallengePointsBlocked(path,r.width,r.height),hits=cbBuildBridgeHits(path,r.width,r.height);return JSON.parse(JSON.stringify({blocked,hits,path:path.map(p=>cbPxBoard(p,r.width,r.height)),on:cbBuildBridge,button:{hidden:$('cbBridgeToggle').hidden,pressed:$('cbBridgeToggle').getAttribute('aria-pressed'),text:$('cbBridgeToggle').textContent}}))},
 commit:()=>{const p=cbBuildBridgeTest.probe();cbDrag={targets:['d1'],previewLegs:[{from:'d0',to:'d1',points:p.path,bridges:p.hits}]};return cbCommitDrag()},
 read:()=>JSON.parse(JSON.stringify({bridges:cbCircuit.bridges||[],legs:cbCircuit.legs||[],on:cbBuildBridge})),
 undo:()=>cbUndo()
};`;
const html=source.replace('ensureUiState();renderFloors();renderSymbolColors();',expose+'ensureUiState();renderFloors();renderSymbolColors();');
const server=http.createServer((q,r)=>{const f=(q.url||'/').split('?')[0]==='/'?'index.html':(q.url||'').split('?')[0].slice(1);try{r.end(f==='index.html'?html:fs.readFileSync(f))}catch{r.statusCode=404;r.end()}}).listen(0,'127.0.0.1');
(async()=>{await new Promise(ok=>server.once('listening',ok));const browser=await chromium.launch({headless:true});try{
 const page=await browser.newPage({viewport:{width:390,height:844}});page.on('dialog',d=>d.accept());await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);await page.evaluate(async()=>{document.querySelector('#projectsHome').hidden=true;await cbBuildBridgeTest.seed()});await page.waitForTimeout(80);
 let p=await page.evaluate(()=>cbBuildBridgeTest.probe());assert.equal(p.button.hidden,false,'Bridge button must be visible while building a conventional circuit');assert.equal(p.button.pressed,'false');assert.equal(p.blocked,true,'crossing must remain blocked with Bridge OFF');assert.equal(p.hits.length,0,'Bridge OFF must not stage bridge marks');
 await page.locator('#cbBridgeToggle').click();p=await page.evaluate(()=>cbBuildBridgeTest.probe());assert.equal(p.on,true);assert.equal(p.button.pressed,'true');assert.match(p.button.text,/Bridge ON/);assert.equal(p.blocked,false,'Bridge ON must allow a real perpendicular crossing');assert(p.hits.length>=1,'Bridge ON must produce bridge metadata');
 assert.equal(await page.evaluate(()=>cbBuildBridgeTest.commit()),true,'bridged build leg must commit');let s=await page.evaluate(()=>cbBuildBridgeTest.read());assert.equal(s.legs.length,2);assert(s.bridges.length>=1,'committed build leg must retain bridge metadata');assert(s.bridges.every(b=>Number.isFinite(b.point?.x)&&Number.isFinite(b.point?.y)&&['h','v'].includes(b.axis)));
 await page.evaluate(()=>cbBuildBridgeTest.undo());s=await page.evaluate(()=>cbBuildBridgeTest.read());assert.equal(s.legs.length,1);assert.equal(s.bridges.length,0,'undo must remove bridge marks belonging to the undone leg');
 console.log('PASS: mobile Circuit Builder exposes Bridge, keeps OFF crossings blocked, records ON crossings, and cleans metadata on undo');
 }finally{await browser.close();server.close()}})().catch(e=>{console.error(e);server.close();process.exit(1)});
