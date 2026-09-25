const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');
const source=fs.readFileSync('index.html','utf8');
for(const required of ['function cbEnterEdit','function cbEditAnchorAt','function cbEditStartStroke','function cbEditFinishStroke','function cbEditDeleteSegment','function cbEditUndo','function cbEditRedo','function cbEditDone'])assert(source.includes(required),`manual editor missing ${required}`);
const expose=`window.cbEditorTest={
 seed:async()=>{state=fresh();state.image=blankImage();state.isBlank=true;state.symbols=[
  {id:'panel',type:'panel',scope:'plan',x:.10,y:.25},{id:'d0',type:'smoke',scope:'survey',x:.38,y:.25},{id:'d1',type:'heat',scope:'survey',x:.70,y:.55}
 ];await setImage(state.image,false);ensureFloors();openCircuitBuilder();const c=cbNewCircuit('addressable',cbSurveyDevices());const P=id=>c.layout[id];
 c.sequence=['panel','d0','d1','panel'];c.legs=[
  {from:'panel',to:'d0',points:[P('panel'),{x:.18,y:.25},{x:.18,y:.33},{x:.29,y:.33},{x:.29,y:.25},P('d0')]},
  {from:'d0',to:'d1',points:[P('d0'),{x:.50,y:.25},{x:.50,y:.55},P('d1')]},
  {from:'d1',to:'panel',points:[P('d1'),{x:.70,y:.72},{x:.10,y:.72},P('panel')]}
 ];c.complete=true;c.updatedAt=Date.now();cbOpenCircuit(c);cbEnterEdit(c);cbDrawBoard();return c.id},
 read:()=>JSON.parse(JSON.stringify({c:cbCircuit,edit:cbEdit,status:document.querySelector('#cbEditStatus')?.textContent||'',draft:cbCircuit?.editDraft||null})),
 px:p=>{const r=$('cbCanvas').getBoundingClientRect(),q=cbBoardPx(p,r.width,r.height);return{x:q.x,y:q.y}},
 anchor:p=>{const r=$('cbCanvas').getBoundingClientRect(),q=cbBoardPx(p,r.width,r.height);return cbEditAnchorAt(q,r.width,r.height)},
 start:(anchor,p)=>{const r=$('cbCanvas').getBoundingClientRect(),q=cbBoardPx(p,r.width,r.height);return cbEditStartStroke(anchor,q,r.width,r.height)},
 move:p=>{const r=$('cbCanvas').getBoundingClientRect(),q=cbBoardPx(p,r.width,r.height);cbEditMoveStroke(q,r.width,r.height)},
 finish:(anchor)=>{const r=$('cbCanvas').getBoundingClientRect();return cbEditFinishStroke(anchor,r.width,r.height)},
 del:(legIndex,segmentIndex)=>cbEditDeleteSegment({legIndex,segmentIndex}),
 undo:()=>cbEditUndo(),redo:()=>cbEditRedo(),done:()=>cbEditDone(),
 clean:(raw,start,end,strength)=>{const r=$('cbCanvas').getBoundingClientRect(),toPx=p=>cbBoardPx(p,r.width,r.height),pts=cbEditCleanStroke(raw.map(toPx),toPx(start),toPx(end),r.width,r.height,strength);return pts.map(p=>cbPxBoard(p,r.width,r.height))}
};`;
const html=source.replace('ensureUiState();renderFloors();renderSymbolColors();',expose+'ensureUiState();renderFloors();renderSymbolColors();');
const server=http.createServer((q,r)=>{const f=(q.url||'/').split('?')[0]==='/'?'index.html':(q.url||'').split('?')[0].slice(1);try{r.setHeader('Content-Type',f.endsWith('.js')?'text/javascript':'text/html');r.end(f==='index.html'?html:fs.readFileSync(f))}catch{r.statusCode=404;r.end()}}).listen(0,'127.0.0.1');
function orthogonal(points){return points.every((p,i)=>!i||Math.abs(p.x-points[i-1].x)<1e-4||Math.abs(p.y-points[i-1].y)<1e-4)}
(async()=>{await new Promise(ok=>server.once('listening',ok));const browser=await chromium.launch({headless:true});try{
 const page=await browser.newPage({viewport:{width:768,height:1024}});page.on('dialog',d=>d.accept());await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);await page.evaluate(async()=>{document.querySelector('#projectsHome').hidden=true;await cbEditorTest.seed()});await page.waitForTimeout(50);
 for(const id of ['cbEditToggle','cbEditBar','cbEditPencil','cbEditBin','cbEditUndo','cbEditRedo','cbEditBridge','cbEditOptions','cbEditClean','cbEditDone'])assert(await page.locator('#'+id).count(),`missing editor UI #${id}`);
 let s=await page.evaluate(()=>cbEditorTest.read());assert(s.edit?.active,'edit session must start');assert(s.c.editDraft,'edit draft must persist on circuit');assert(/EDITING/.test(s.status),'editing state must be obvious');
 const pts=s.c.editDraft.legs[0].points,start={x:(pts[0].x+pts[1].x)/2,y:(pts[0].y+pts[1].y)/2},end={x:(pts.at(-2).x+pts.at(-1).x)/2,y:(pts.at(-2).y+pts.at(-1).y)/2};
 const a=await page.evaluate(p=>cbEditorTest.anchor(p),start),b=await page.evaluate(p=>cbEditorTest.anchor(p),end);assert(a&&b,'cable anchors must be hittable');
 await page.evaluate(({a,start})=>cbEditorTest.start(a,start),{a,start});
 for(const p of [{x:.20,y:.21},{x:.21,y:.29},{x:.23,y:.22},{x:.27,y:.26},{x:.31,y:.24},{x:.34,y:.25}])await page.evaluate(p=>cbEditorTest.move(p),p);
 const accepted=await page.evaluate(b=>cbEditorTest.finish(b),b);assert.equal(accepted,true,'replacement should stage successfully');
 s=await page.evaluate(()=>cbEditorTest.read());assert(s.edit.pending,'draw-first workflow must retain replacement before deleting old');assert(orthogonal(s.edit.pending.points),'saved replacement must be orthogonal');
 const oldCount=s.c.editDraft.legs[0].points.length;const midSeg=Math.max(0,Math.min(s.c.editDraft.legs[0].points.length-2,2));await page.evaluate(i=>cbEditorTest.del(0,i),midSeg);
 s=await page.evaluate(()=>cbEditorTest.read());assert(!s.edit.pending,'binning old span should commit staged replacement');assert.notEqual(s.c.editDraft.legs[0].points.length,oldCount,'local leg geometry should actually change');
 // Direct deletion without a replacement must create a safe open-route state, not silently reconnect the line.
 await page.evaluate(()=>cbEditorTest.del(1,1));s=await page.evaluate(()=>cbEditorTest.read());assert(s.c.editDraft.gaps?.length===1,'one local segment deletion should create one explicit gap');assert(/ROUTE OPEN/.test(s.status),'broken edit must read EDITING · ROUTE OPEN');
 await page.evaluate(()=>cbEditorTest.undo());s=await page.evaluate(()=>cbEditorTest.read());assert.equal(s.c.editDraft.gaps.length,0,'undo must restore exact connected state');await page.evaluate(()=>cbEditorTest.redo());s=await page.evaluate(()=>cbEditorTest.read());assert.equal(s.c.editDraft.gaps.length,1,'redo must restore gap');const rejected=await page.evaluate(()=>cbEditorTest.done());assert.equal(rejected,false,'Done must reject open route');await page.evaluate(()=>cbEditorTest.undo());const done=await page.evaluate(()=>cbEditorTest.done());assert.equal(done,true,'Done should accept repaired route');s=await page.evaluate(()=>cbEditorTest.read());assert.equal(s.c.editDraft,null,'valid Done removes draft');assert.equal(s.c.complete,true,'valid Done restores complete');
 // Cleanup is post-stroke geometry: stronger settings must not create more saved points and all outputs stay orthogonal.
 const raw=[{x:.2,y:.2},{x:.22,y:.24},{x:.24,y:.19},{x:.27,y:.25},{x:.30,y:.20},{x:.34,y:.24},{x:.38,y:.2}],cs=raw[0],ce=raw.at(-1),low=await page.evaluate(({raw,cs,ce})=>cbEditorTest.clean(raw,cs,ce,10),{raw,cs,ce}),high=await page.evaluate(({raw,cs,ce})=>cbEditorTest.clean(raw,cs,ce,90),{raw,cs,ce});assert(orthogonal(low)&&orthogonal(high),'cleanup output must remain orthogonal');assert(high.length<=low.length,'strong cleanup must be at least as simple as light cleanup');
 console.log(`EDITOR_CLEANUP low=${low.length} high=${high.length}`);console.log('PASS: v0.58 manual editor stages replacement, deletes locally, exposes route-open state, undoes/redoes and validates Done');
 }finally{await browser.close();server.close()}})().catch(e=>{console.error(e);server.close();process.exit(1)});
