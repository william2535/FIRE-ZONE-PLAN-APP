const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');
const source=fs.readFileSync('index.html','utf8');
for(const required of ['function cbEnterEdit','function cbEditFinishStroke','function cbEditCrossingsForPath','function cbEditSplicePending','function cbEditDone','function cbDrawCircuitBridges'])assert(source.includes(required),`bridge regression missing ${required}`);
const expose=`window.cbBridgeTest={
 seed:async()=>{state=fresh();state.image=blankImage();state.isBlank=true;state.symbols=[
  {id:'panel',type:'panel',scope:'plan',x:.10,y:.25},{id:'d0',type:'smoke',scope:'survey',x:.38,y:.25},{id:'d1',type:'heat',scope:'survey',x:.70,y:.55}
 ];await setImage(state.image,false);ensureFloors();openCircuitBuilder();const c=cbNewCircuit('addressable',cbSurveyDevices());const P=id=>c.layout[id],A=P('panel'),B=P('d0'),C=P('d1'),x1=A.x+(B.x-A.x)*.30,x2=A.x+(B.x-A.x)*.70,yDetour=Math.max(.08,Math.min(.92,(A.y+B.y)/2+(A.y<.75?.10:-.10))),xBC=(B.x+C.x)/2,returnY=(C.y+A.y)/2;
 c.sequence=['panel','d0','d1','panel'];c.legs=[
  {from:'panel',to:'d0',points:[A,{x:x1,y:A.y},{x:x1,y:yDetour},{x:x2,y:yDetour},{x:x2,y:B.y},B]},
  {from:'d0',to:'d1',points:[B,{x:xBC,y:B.y},{x:xBC,y:C.y},C]},
  {from:'d1',to:'panel',points:[C,{x:C.x,y:returnY},{x:A.x,y:returnY},A]}
 ];c.bridges=[];c.complete=true;c.updatedAt=Date.now();cbOpenCircuit(c);cbEnterEdit(c);cbDrawBoard();return c.id},
 read:()=>JSON.parse(JSON.stringify({c:cbCircuit,edit:cbEdit,draft:cbCircuit?.editDraft||null,status:$('cbEditStatus')?.textContent||'',save:$('saveIndicator')?.textContent||''})),
 anchor:p=>{const r=$('cbCanvas').getBoundingClientRect(),q=cbBoardPx(p,r.width,r.height);return cbEditAnchorAt(q,r.width,r.height)},
 start:(anchor,p)=>{const r=$('cbCanvas').getBoundingClientRect(),q=cbBoardPx(p,r.width,r.height);return cbEditStartStroke(anchor,q,r.width,r.height)},
 move:p=>{const r=$('cbCanvas').getBoundingClientRect(),q=cbBoardPx(p,r.width,r.height);cbEditMoveStroke(q,r.width,r.height)},
 finish:anchor=>{const r=$('cbCanvas').getBoundingClientRect();return cbEditFinishStroke(anchor,r.width,r.height)},
 toggleBridge:()=>{cbEdit.bridge=!cbEdit.bridge;cbEditSyncUi();return cbEdit.bridge},
 del:(legIndex,segmentIndex)=>cbEditDeleteSegment({legIndex,segmentIndex}),
 validate:()=>cbEditValidateDraft(),
 done:()=>cbEditDone(),
 reopen:()=>{const ok=cbEnterEdit(cbCircuit);cbPaintBoard();return {ok,bridges:cbEditClone(cbCircuit?.editDraft?.bridges||[])}},
 paintProbe:()=>{const hits=[],old=cbPaintBridgeMark;cbPaintBridgeMark=(x,p,axis,color,width,scale)=>{hits.push({x:p.x,y:p.y,axis});return old(x,p,axis,color,width,scale)};try{cbPaintBoard()}finally{cbPaintBridgeMark=old}return hits}
};`;
const html=source.replace('ensureUiState();renderFloors();renderSymbolColors();',expose+'ensureUiState();renderFloors();renderSymbolColors();');
const server=http.createServer((q,r)=>{const f=(q.url||'/').split('?')[0]==='/'?'index.html':(q.url||'').split('?')[0].slice(1);try{r.setHeader('Content-Type',f.endsWith('.js')?'text/javascript':'text/html');r.end(f==='index.html'?html:fs.readFileSync(f))}catch{r.statusCode=404;r.end()}}).listen(0,'127.0.0.1');
const finiteBridge=b=>!!b&&Number.isFinite(b.point?.x)&&Number.isFinite(b.point?.y)&&['h','v'].includes(b.axis);
const near=(a,b,e=.0002)=>Math.hypot(a.x-b.x,a.y-b.y)<=e;
(async()=>{await new Promise(ok=>server.once('listening',ok));const browser=await chromium.launch({headless:true});try{
 const page=await browser.newPage({viewport:{width:768,height:1024}});page.on('dialog',d=>d.accept());await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);await page.evaluate(async()=>{document.querySelector('#projectsHome').hidden=true;await cbBridgeTest.seed()});await page.waitForTimeout(80);
 let s=await page.evaluate(()=>cbBridgeTest.read());assert(s.edit?.active,'edit session must start');assert.equal(s.edit.bridge,false,'Bridge must start OFF');
 const pts=s.draft.legs[0].points,start={x:(pts[0].x+pts[1].x)/2,y:(pts[0].y+pts[1].y)/2},end={x:(pts.at(-2).x+pts.at(-1).x)/2,y:(pts.at(-2).y+pts.at(-1).y)/2},returnY=s.draft.legs[2].points[1].y,routeY=Math.max(.08,Math.min(.92,returnY+(returnY<.78?.10:-.10)));
 const a=await page.evaluate(p=>cbBridgeTest.anchor(p),start),b=await page.evaluate(p=>cbBridgeTest.anchor(p),end);assert(a&&b,'replacement anchors must be hittable');
 const draw=async()=>{await page.evaluate(({a,start})=>cbBridgeTest.start(a,start),{a,start});for(const p of [{x:start.x,y:routeY},{x:end.x,y:routeY}])await page.evaluate(p=>cbBridgeTest.move(p),p);return page.evaluate(b=>cbBridgeTest.finish(b),b)};
 const blocked=await draw();assert.equal(blocked,false,'real geometric crossing must be rejected with Bridge OFF');s=await page.evaluate(()=>cbBridgeTest.read());assert.equal(s.draft.pending,null,'Bridge OFF rejection must not leave staged replacement');
 assert.equal(await page.evaluate(()=>cbBridgeTest.toggleBridge()),true,'Bridge must enable');assert.equal(await page.locator('#cbEditBridge').getAttribute('aria-pressed'),'true','Bridge control must expose enabled state');
 const accepted=await draw();assert.equal(accepted,true,'real geometric crossing must stage with Bridge ON');s=await page.evaluate(()=>cbBridgeTest.read());assert(s.draft.pending,'Bridge ON crossing must create a staged replacement');assert(s.draft.pending.bridges.length>=1,'staged replacement must contain at least one real crossing bridge');assert(s.draft.pending.bridges.every(finiteBridge),'every staged bridge coordinate must be finite');
 const staged=JSON.parse(JSON.stringify(s.draft.pending.bridges));const lo=Math.min(s.draft.pending.startPos,s.draft.pending.endPos),hi=Math.max(s.draft.pending.startPos,s.draft.pending.endPos),segmentIndex=Math.max(0,Math.min(s.draft.legs[0].points.length-2,Math.floor((lo+hi)/2)));
 assert.equal(await page.evaluate(i=>cbBridgeTest.del(0,i),segmentIndex),true,'deleting inside the old span must splice the staged replacement');s=await page.evaluate(()=>cbBridgeTest.read());assert.equal(s.draft.pending,null,'splice must clear staged replacement');assert(s.draft.bridges.length>=staged.length,'splice must persist bridge metadata in the draft');for(const b0 of staged)assert(s.draft.bridges.some(b1=>finiteBridge(b1)&&near(b0.point,b1.point)),`spliced draft lost bridge ${JSON.stringify(b0)}`);
 const valid=await page.evaluate(()=>cbBridgeTest.validate());assert.equal(valid.ok,true,'bridged replacement must validate: '+valid.message);
 assert.equal(await page.evaluate(()=>cbBridgeTest.done()),true,'Done must save a valid bridged route');s=await page.evaluate(()=>cbBridgeTest.read());assert.equal(!!s.c.editDraft,false,'Done must remove edit draft');assert(s.c.bridges.length>=staged.length,'saved circuit must retain real bridge metadata');assert(s.c.bridges.every(finiteBridge),'saved bridge coordinates must remain finite');for(const b0 of staged)assert(s.c.bridges.some(b1=>near(b0.point,b1.point)),`saved circuit lost bridge ${JSON.stringify(b0)}`);
 const painted=await page.evaluate(()=>cbBridgeTest.paintProbe());assert(painted.length>=staged.length,'saved bridge metadata must redraw as visible bridge marks');assert(painted.every(p=>Number.isFinite(p.x)&&Number.isFinite(p.y)),'redrawn bridge marks must use finite pixel coordinates');
 const reopened=await page.evaluate(()=>cbBridgeTest.reopen());assert.equal(reopened.ok,true,'saved circuit must reopen in Manual Edit');assert(reopened.bridges.length>=staged.length,'reopened edit draft must restore saved bridges');for(const b0 of staged)assert(reopened.bridges.some(b1=>near(b0.point,b1.point)),`reopened edit lost bridge ${JSON.stringify(b0)}`);
 const repainted=await page.evaluate(()=>cbBridgeTest.paintProbe());assert(repainted.length>=staged.length,'reopened editor must redraw persisted bridges');
 console.log('BRIDGE_POINTS '+JSON.stringify(staged));
 console.log('PASS: v0.58 real crossing is rejected with Bridge OFF, accepted with Bridge ON, then survives splice, Done/save, reopen and redraw');
 }finally{await browser.close();server.close()}})().catch(e=>{console.error(e);server.close();process.exit(1)});
