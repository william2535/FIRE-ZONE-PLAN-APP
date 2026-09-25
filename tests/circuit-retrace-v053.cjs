const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict'),path=require('path');
(async()=>{
 const html=fs.readFileSync('index.html','utf8');
 assert.match(html,/v0\.53 parallel retrace/);
 assert.match(html,/if\(!captured\)cbAppendDrag\(p,w,h\)/);
 const server=http.createServer((q,r)=>{let rel=decodeURIComponent((q.url||'/').split('?')[0]);if(rel.endsWith('/'))rel+='index.html';rel=rel.replace(/^\//,'');const file=path.join(process.cwd(),rel);try{const data=fs.readFileSync(file);if(file.endsWith('.js'))r.setHeader('Content-Type','text/javascript');else if(file.endsWith('.svg'))r.setHeader('Content-Type','image/svg+xml');else if(file.endsWith('.webmanifest'))r.setHeader('Content-Type','application/manifest+json');else r.setHeader('Content-Type','text/html');r.end(data)}catch(e){r.statusCode=404;r.end('not found')}}).listen(0,'127.0.0.1');
 await new Promise(r=>server.once('listening',r));const browser=await chromium.launch({headless:true});
 try{
  const p=await browser.newPage({viewport:{width:1100,height:800}}),errors=[];p.on('pageerror',e=>errors.push(e.message));p.on('dialog',d=>d.accept(d.type()==='prompt'?'Retrace field test':undefined));
  await p.goto('http://127.0.0.1:'+server.address().port+'/');await p.locator('#homeNew').click();await p.locator('#projectsHome').waitFor({state:'hidden'});
  const xy=async(x,y)=>p.locator('#canvas').evaluate((c,{x,y})=>{const b=c.getBoundingClientRect(),w=3200,h=2000,s=Math.min((b.width-48)/w,(b.height-48)/h);return{x:b.x+b.width/2+(x-.5)*w*s,y:b.y+b.height/2+(y-.5)*h*s}},{x,y});
  const drag=async(a,b)=>{await p.mouse.move(a.x,a.y);await p.mouse.down();await p.mouse.move(b.x,b.y,{steps:8});await p.mouse.up()};
  const zoneA={x:.10,y:.25},zoneB={x:.68,y:.72};
  await p.locator('#zoneMenuBtn').click();await p.locator('#zoneCreate').click();await p.locator('#zoneName').fill('Retrace');await p.locator('#saveZone').click();await p.locator('#zoneMenuBtn').click();await p.locator('[data-menu-tool="rect"]').click();await drag(await xy(zoneA.x,zoneA.y),await xy(zoneB.x,zoneB.y));
  const panel={x:.16,y:.45},d1={x:.58,y:.45},d2={x:.22,y:.64};
  await p.locator('#surveyModeBtn').click();
  const place=async(type,q)=>{await p.locator('#surveyDevice').click();await p.locator(`[data-symbol="${type}"]`).click();const pt=await xy(q.x,q.y);await p.mouse.click(pt.x,pt.y)};
  await place('panel',panel);await place('smoke',d1);await place('smoke',d2);
  await p.locator('#circuitModeBtn').click();await p.locator('#cbConventionalZones .cbZoneButton').first().click();assert.equal(await p.locator('#cbCircuitType').innerText(),'CONVENTIONAL');
  const mkBounds=(pts,margin)=>{let x1=Math.min(...pts.map(q=>q.x)),x2=Math.max(...pts.map(q=>q.x)),y1=Math.min(...pts.map(q=>q.y)),y2=Math.max(...pts.map(q=>q.y)),cx=(x1+x2)/2,cy=(y1+y2)/2,w=Math.max(.22,x2-x1),h=Math.max(.22,y2-y1);x1=cx-w/2-margin;x2=cx+w/2+margin;y1=cy-h/2-margin;y2=cy+h/2+margin;if(x1<0){x2-=x1;x1=0}if(y1<0){y2-=y1;y1=0}if(x2>1){x1-=x2-1;x2=1}if(y2>1){y1-=y2-1;y2=1}return{x1:Math.max(0,x1),y1:Math.max(0,y1),x2:Math.min(1,x2),y2:Math.min(1,y2)}};
  const zonePts=[zoneA,{x:zoneB.x,y:zoneA.y},zoneB,{x:zoneA.x,y:zoneB.y}],bounds=mkBounds([...zonePts,panel,d1,d2],.04);
  const boardPoint=async q=>{const r=await p.locator('#cbCanvas').boundingBox(),bx=.045+(q.x-bounds.x1)/(bounds.x2-bounds.x1)*.91,by=.045+(q.y-bounds.y1)/(bounds.y2-bounds.y1)*.91;return{x:r.x+28+bx*(r.width-56),y:r.y+28+by*(r.height-56)}};
  const panelPt=await boardPoint(panel),d1Pt=await boardPoint(d1),d2Pt=await boardPoint(d2),returnPt=await boardPoint({x:.25,y:.45});
  const canvasBox=await p.locator('#cbCanvas').boundingBox(),beyond={x:Math.min(canvasBox.x+canvasBox.width-35,d1Pt.x+85),y:d1Pt.y};
  // One sparse event intentionally crosses D1 and lands well beyond it. The new engine must
  // capture at D1 and throw away the event tail instead of creating a long spike.
  await p.mouse.move(panelPt.x,panelPt.y);await p.mouse.down();await p.mouse.move(beyond.x,beyond.y,{steps:1});await p.waitForTimeout(50);assert.equal(await p.locator('#cbDetectorCount').innerText(),'1 / 2');
  // Still holding: run backwards directly over the first cable, then turn down to D2.
  // This must become a second parallel lane rather than an overlapping line/T junction.
  await p.mouse.move(returnPt.x,returnPt.y,{steps:8});await p.mouse.move(d2Pt.x,d2Pt.y,{steps:6});await p.locator('#cbCelebrate').waitFor({state:'visible'});await p.mouse.up();
  await p.locator('#cbCelebrateKeep').click();await p.locator('#cbBack').click();
  await p.locator('#projectMenuBtn').click();const downloadPromise=p.waitForEvent('download');await p.locator('#backupProject').click();const download=await downloadPromise,saved=await download.path(),backup=JSON.parse(fs.readFileSync(saved,'utf8'));
  const circuit=backup.project.floors[0].data.circuits[0];assert(circuit&&circuit.legs.length===2,'expected the conventional run to save two cable legs');
  const segs=leg=>(leg.points||[]).slice(1).map((b,i)=>({a:leg.points[i],b}));
  for(const leg of circuit.legs)for(const s of segs(leg))assert(Math.abs(s.a.x-s.b.x)<1e-6||Math.abs(s.a.y-s.b.y)<1e-6,'stored route must stay orthogonal');
  const h1=segs(circuit.legs[0]).filter(s=>Math.abs(s.a.y-s.b.y)<1e-6).sort((a,b)=>Math.abs(b.b.x-b.a.x)-Math.abs(a.b.x-a.a.x))[0];
  const h2=segs(circuit.legs[1]).filter(s=>Math.abs(s.a.y-s.b.y)<1e-6).sort((a,b)=>Math.abs(b.b.x-b.a.x)-Math.abs(a.b.x-a.a.x))[0];
  assert(h1&&h2,'both outward and retraced legs need a horizontal cable section');
  assert(Math.abs(h1.a.y-h2.a.y)>.004,'retracing the same run must create a visibly separate parallel lane');
  const firstEnd=circuit.legs[0].points.at(-1),secondMaxX=Math.max(...circuit.legs[1].points.map(q=>q.x));
  assert(secondMaxX<=firstEnd.x+.035,`second leg contains an overshoot/spike beyond D1: ${secondMaxX-firstEnd.x}`);
  assert.deepEqual(errors,[],'No Circuit Builder runtime errors');
  console.log('PASS: v0.53 held retrace creates a parallel cable lane and sparse detector crossings do not leave long corner spikes');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
