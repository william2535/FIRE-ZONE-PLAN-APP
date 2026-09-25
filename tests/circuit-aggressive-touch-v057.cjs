const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');

const phase=process.env.ROUTING_PHASE||'regression';
const baselinePath=process.env.ROUTING_BASELINE||'test-results/aggressive-touch-baseline.json';
const outPath=process.env.ROUTING_OUTPUT||`test-results/aggressive-touch-${phase}.json`;
const expose=`window.cbAggressiveTest={
 read:()=>JSON.parse(JSON.stringify({c:cbCircuit,drag:cbDrag,view:cbView,screen:cbScreen,state:typeof cbRoutingState==='function'?cbRoutingState():(cbDrag?'routing':'waiting-to-start')})),
 node:id=>{const r=$('cbCanvas').getBoundingClientRect(),p=cbNodePx(id,r.width,r.height);return{x:r.left+p.x,y:r.top+p.y}},
 seed:async()=>{state=fresh();state.image=blankImage();state.isBlank=true;state.symbols=[
  {id:'panel',type:'panel',scope:'plan',x:.10,y:.20},
  {id:'d0',type:'smoke',scope:'survey',x:.25,y:.20},
  {id:'d1',type:'smoke',scope:'survey',x:.40,y:.20},
  {id:'d2',type:'smoke',scope:'survey',x:.56,y:.20},
  {id:'d3',type:'heat',scope:'survey',x:.56,y:.43},
  {id:'d4',type:'mcp',scope:'survey',x:.40,y:.43},
  {id:'d5',type:'smoke',scope:'survey',x:.24,y:.43}
 ];await setImage(state.image,false);ensureFloors();openCircuitBuilder();cbOpenCircuit(cbNewCircuit('addressable',cbSurveyDevices()));cbAudioCtx=null;},
 setView:scale=>{cbView={scale,panX:0,panY:0};cbClampView($('cbCanvas').getBoundingClientRect().width,$('cbCanvas').getBoundingClientRect().height);cbDrawBoard()}
};`;

const viewports=[
 {name:'iphone-small',width:375,height:667},
 {name:'iphone-large',width:430,height:932},
 {name:'android',width:412,height:915},
 {name:'tablet-small',width:768,height:1024},
 {name:'landscape',width:1180,height:820}
];
const styles={
 clean:{zoom:1,fractions:[.18,.38,.60,.82,1],noise:[0,1,-1,1,0],cross:[0,0,0,0,0]},
 rough:{zoom:2.15,fractions:[.12,.33,.68,1.12,.88,1],noise:[4,-6,7,-5,3,0],cross:[-2,4,-5,7,-3,0]},
 abusive:{zoom:1,fractions:[.08,.56,1.28,.72,1.12,.92,1],noise:[10,-14,17,-12,15,-8,0],cross:[7,-11,14,-16,12,-7,0]}
};
function orientation(a,b){const dx=b.x-a.x,dy=b.y-a.y;if(Math.abs(dx)<1e-7&&Math.abs(dy)<1e-7)return 'z';return Math.abs(dx)>=Math.abs(dy)?'h':'v'}
function sign(v){return v>1e-7?1:v<-1e-7?-1:0}
function metricCircuit(c){
 const legs=c?.legs||[],segments=[];let points=0,corners=0,shortLegs=0,reversals=0,length=0,direct=0;
 for(const leg of legs){const pts=leg.points||[];points+=pts.length;if(pts.length>1){const a=pts[0],b=pts.at(-1);direct+=Math.abs(b.x-a.x)+Math.abs(b.y-a.y)}
  for(let i=1;i<pts.length;i++){const a=pts[i-1],b=pts[i],len=Math.hypot(b.x-a.x,b.y-a.y);segments.push({a,b,leg});length+=len;if(len<.022)shortLegs++}
  for(let i=2;i<pts.length;i++){const a=pts[i-2],b=pts[i-1],d=pts[i],o1=orientation(a,b),o2=orientation(b,d);if(o1!=='z'&&o2!=='z'&&o1!==o2)corners++;if(o1===o2&&o1!=='z'){const v1=o1==='h'?b.x-a.x:b.y-a.y,v2=o2==='h'?d.x-b.x:d.y-b.y;if(sign(v1)&&sign(v2)&&sign(v1)!==sign(v2))reversals++}}
 }
 function close(a,b){return Math.hypot(a.x-b.x,a.y-b.y)<1e-5}
 function cross(s,t){
  if(close(s.a,t.a)||close(s.a,t.b)||close(s.b,t.a)||close(s.b,t.b))return false;
  const sh=orientation(s.a,s.b)==='h',th=orientation(t.a,t.b)==='h';if(sh===th)return false;
  const h=sh?s:t,v=sh?t:s,p={x:v.a.x,y:h.a.y};
  return p.x>Math.min(h.a.x,h.b.x)+1e-6&&p.x<Math.max(h.a.x,h.b.x)-1e-6&&p.y>Math.min(v.a.y,v.b.y)+1e-6&&p.y<Math.max(v.a.y,v.b.y)-1e-6
 }
 let intersections=0;for(let i=0;i<segments.length;i++)for(let j=0;j<i-1;j++)if(cross(segments[i],segments[j]))intersections++;
 const deviceIds=new Set(c?.deviceIds||[]),captured=new Set((c?.sequence||[]).filter(id=>deviceIds.has(id))).size;
 return{points,segments:segments.length,corners,shortLegs,reversals,intersections,routeLength:+length.toFixed(5),simplifiedEquivalent:+direct.toFixed(5),excessRatio:+(direct?length/direct:1).toFixed(4),devicesCaptured:captured,totalDevices:deviceIds.size,complete:!!c?.complete};
}
function aggregate(rows,filter=()=>true){const use=rows.filter(filter),keys=['points','segments','corners','shortLegs','reversals','intersections','routeLength','simplifiedEquivalent'];const out={cases:use.length};for(const k of keys)out[k]=+use.reduce((n,r)=>n+r.metrics[k],0).toFixed(5);out.excessRatio=+(use.reduce((n,r)=>n+r.metrics.excessRatio,0)/Math.max(1,use.length)).toFixed(4);out.devicesCaptured=use.reduce((n,r)=>n+r.metrics.devicesCaptured,0);out.totalDevices=use.reduce((n,r)=>n+r.metrics.totalDevices,0);out.complete=use.filter(r=>r.metrics.complete).length;return out}
function tracePoints(a,b,style,legIndex){const dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy)||1,nx=-dy/L,ny=dx/L,ux=dx/L,uy=dy/L;return style.fractions.map((f,i)=>{const lateral=style.noise[(i+legIndex)%style.noise.length],along=style.cross[(i*2+legIndex)%style.cross.length];return{x:a.x+dx*f+nx*lateral+ux*along,y:a.y+dy*f+ny*lateral+uy*along}})}

(async()=>{
 const source=fs.readFileSync('index.html','utf8');
 assert(source.includes('function cbProcessPointer'),'Circuit Builder source missing');
 const html=source.replace('ensureUiState();renderFloors();renderSymbolColors();',expose+'ensureUiState();renderFloors();renderSymbolColors();');
 const server=http.createServer((q,r)=>{const file=(q.url||'/').split('?')[0]==='/'?'index.html':(q.url||'').split('?')[0].slice(1);try{r.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':'text/html');r.end(file==='index.html'?html:fs.readFileSync(file))}catch{r.statusCode=404;r.end()}}).listen(0,'127.0.0.1');
 await new Promise(ok=>server.once('listening',ok));const browser=await chromium.launch({headless:true});const rows=[],errors=[];
 try{
  for(const viewport of viewports){for(const [traceName,style] of Object.entries(styles)){
   const page=await browser.newPage({viewport:{width:viewport.width,height:viewport.height}});page.on('pageerror',e=>errors.push(`${viewport.name}/${traceName}: ${e.message}`));page.on('dialog',d=>d.accept());
   await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>!document.querySelector('#homeNew').disabled);await page.evaluate(async()=>{document.querySelector('#projectsHome').hidden=true;await cbAggressiveTest.seed()});await page.waitForTimeout(35);await page.evaluate(scale=>cbAggressiveTest.setView(scale),style.zoom);await page.waitForTimeout(25);
   const node=async id=>page.evaluate(id=>cbAggressiveTest.node(id),id),fire=(type,id,pt)=>page.evaluate(({type,id,pt})=>{const c=document.querySelector('#cbCanvas');c.setPointerCapture=()=>{};c.dispatchEvent(new PointerEvent(type,{pointerId:id,pointerType:'touch',clientX:pt.x,clientY:pt.y,button:0,bubbles:true}))},{type,id,pt});
   let current=await node('panel');await fire('pointerdown',1,current);let samples=1;
   for(const [legIndex,id] of ['d0','d1','d2','d3','d4','d5'].entries()){
    const target=await node(id);for(const pt of tracePoints(current,target,style,legIndex)){await fire('pointermove',1,pt);samples++}current=tracePoints(current,target,style,legIndex).at(-1)
   }
   const panel=await node('panel');const returnStyle=traceName==='clean'?styles.clean:traceName==='rough'?styles.rough:styles.abusive;for(const pt of tracePoints(current,panel,returnStyle,8)){await fire('pointermove',1,pt);samples++}await fire('pointermove',1,panel);samples++;await fire('pointerup',1,panel);await page.waitForTimeout(30);
   const read=await page.evaluate(()=>cbAggressiveTest.read()),metrics=metricCircuit(read.c);rows.push({viewport:viewport.name,width:viewport.width,height:viewport.height,trace:traceName,zoom:style.zoom,samples,routingState:read.state,metrics});
   await page.close();
  }}
 }finally{await browser.close();server.close()}
 assert.deepEqual(errors,[],'No browser runtime errors expected');
 const report={phase,generatedAt:new Date().toISOString(),rows,aggregate:aggregate(rows),noisy:aggregate(rows,r=>r.trace!=='clean'),clean:aggregate(rows,r=>r.trace==='clean')};
 fs.mkdirSync('test-results',{recursive:true});fs.writeFileSync(outPath,JSON.stringify(report,null,2));if(phase==='baseline'&&outPath!==baselinePath)fs.writeFileSync(baselinePath,JSON.stringify(report,null,2));
 console.log('AGGRESSIVE_TOUCH_REPORT '+JSON.stringify(report));
 if(phase==='after'){
  const base=JSON.parse(fs.readFileSync(baselinePath,'utf8'));
  assert.equal(report.aggregate.devicesCaptured,report.aggregate.totalDevices,'all deterministic traces must capture every device');
  assert.equal(report.aggregate.complete,report.aggregate.cases,'all deterministic addressable traces must return to the panel and complete');
  assert(report.noisy.corners<=base.noisy.corners,'noisy traces must not produce more corners than baseline');
  assert(report.noisy.shortLegs<=base.noisy.shortLegs,'noisy traces must not produce more very short legs than baseline');
  assert(report.noisy.reversals<=base.noisy.reversals,'noisy traces must not produce more immediate reversals than baseline');
  assert(report.noisy.intersections<=base.noisy.intersections,'noisy traces must not produce more self-intersections than baseline');
  assert(report.noisy.excessRatio<=base.noisy.excessRatio+.0001,'noisy-route excess length must improve or stay equal');
  assert(report.noisy.points<=base.noisy.points,'noisy traces must use no more route points than baseline');
  assert(report.noisy.reversals<=Math.floor(base.noisy.reversals*.55),'Smart Route must cut noisy immediate reversals by at least 45%');
  assert.equal(report.noisy.intersections,0,'Smart Route must remove noisy self-intersections');
 }else if(phase==='regression'){
  assert.equal(report.aggregate.devicesCaptured,report.aggregate.totalDevices,'all deterministic traces must capture every device');
  assert.equal(report.aggregate.complete,report.aggregate.cases,'all deterministic traces must complete');
  assert.equal(report.noisy.intersections,0,'aggressive touch must not self-intersect');
  assert(report.noisy.reversals<=38,`too many noisy immediate reversals: ${report.noisy.reversals}`);
  assert(report.noisy.corners<=132,`too many noisy corners: ${report.noisy.corners}`);
  assert(report.noisy.points<=330,`too many noisy route points: ${report.noisy.points}`);
  assert(report.noisy.excessRatio<=1.54,`noisy route length is too inflated: ${report.noisy.excessRatio}`);
 }
 console.log(`PASS: ${phase} aggressive-touch replay across ${viewports.length} viewports × ${Object.keys(styles).length} deterministic traces`);
})().catch(e=>{console.error(e);process.exit(1)});
