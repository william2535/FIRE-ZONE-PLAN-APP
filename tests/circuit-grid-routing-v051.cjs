const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict'),path=require('path');
(async()=>{
 const html=fs.readFileSync('index.html','utf8');
 assert.match(html,/CB_ROUTE_GRID=24/);
 assert.match(html,/CB_ROUTE_TURN_CELLS=(?:1\.45|\.72)/);
 if(/v0\.55/.test(html)){assert.match(html,/CB_ROUTE_ARM_CELLS=\.28/);assert.match(html,/CB_ROUTE_SAMPLE_CELLS=\.30/)}
 assert.match(html,/function cbRouteGridStep/);
 assert.match(html,/function cbDrawRouteGrid/);
 assert.match(html,/cable (?:snaps to grid|uses Survey field grid)/);
 const server=http.createServer((q,r)=>{let rel=decodeURIComponent((q.url||'/').split('?')[0]);if(rel.endsWith('/'))rel+='index.html';rel=rel.replace(/^\//,'');const file=path.join(process.cwd(),rel);try{const data=fs.readFileSync(file);if(file.endsWith('.js'))r.setHeader('Content-Type','text/javascript');else if(file.endsWith('.svg'))r.setHeader('Content-Type','image/svg+xml');else if(file.endsWith('.webmanifest'))r.setHeader('Content-Type','application/manifest+json');else r.setHeader('Content-Type','text/html');r.end(data)}catch(e){r.statusCode=404;r.end('not found')}}).listen(0,'127.0.0.1');
 await new Promise(r=>server.once('listening',r));const browser=await chromium.launch({headless:true});
 try{
  const p=await browser.newPage({viewport:{width:390,height:844}}),errors=[];p.on('pageerror',e=>errors.push(e.message));p.on('dialog',d=>d.accept(d.type()==='prompt'?'Grid route test':undefined));
  await p.goto('http://127.0.0.1:'+server.address().port+'/');
  await p.locator('#homeNew').click();await p.locator('#projectsHome').waitFor({state:'hidden'});
  const xy=async(x,y)=>p.locator('#canvas').evaluate((c,{x,y})=>{const b=c.getBoundingClientRect(),w=3200,h=2000,s=Math.min((b.width-48)/w,(b.height-48)/h);return{x:b.x+b.width/2+(x-.5)*w*s,y:b.y+b.height/2+(y-.5)*h*s}},{x,y});
  const panel={x:.20,y:.40},device={x:.70,y:.40},all=[panel,device];
  await p.locator('#surveyModeBtn').click();
  const place=async(type,q)=>{await p.locator('#surveyDevice').click();await p.locator(`[data-symbol="${type}"]`).click();const pt=await xy(q.x,q.y);await p.mouse.click(pt.x,pt.y)};
  await place('panel',panel);await place('smoke',device);
  await p.locator('#circuitModeBtn').click();await p.locator('#cbAddressableStart').click();
  const mkBounds=(pts,margin)=>{let x1=Math.min(...pts.map(q=>q.x)),x2=Math.max(...pts.map(q=>q.x)),y1=Math.min(...pts.map(q=>q.y)),y2=Math.max(...pts.map(q=>q.y)),cx=(x1+x2)/2,cy=(y1+y2)/2,w=Math.max(.22,x2-x1),h=Math.max(.22,y2-y1);x1=cx-w/2-margin;x2=cx+w/2+margin;y1=cy-h/2-margin;y2=cy+h/2+margin;if(x1<0){x2-=x1;x1=0}if(y1<0){y2-=y1;y1=0}if(x2>1){x1-=x2-1;x2=1}if(y2>1){y1-=y2-1;y2=1}return{x1:Math.max(0,x1),y1:Math.max(0,y1),x2:Math.min(1,x2),y2:Math.min(1,y2)}};
  const boardPoint=async(q,b)=>{const r=await p.locator('#cbCanvas').boundingBox(),bx=.045+(q.x-b.x1)/(b.x2-b.x1)*.91,by=.045+(q.y-b.y1)/(b.y2-b.y1)*.91;return{x:r.x+28+bx*(r.width-56),y:r.y+28+by*(r.height-56)}};
  const selectBounds=mkBounds(all,.06),selectPt=await boardPoint(device,selectBounds);await p.mouse.click(selectPt.x,selectPt.y);await p.locator('#cbBuildSelected').click();
  const gameBounds=mkBounds(all,.04),panelPt=await boardPoint(panel,gameBounds),devicePt=await boardPoint(device,gameBounds);
  await p.mouse.move(panelPt.x,panelPt.y);await p.mouse.down();
  const wiggles=[{f:.16,dy:10},{f:.32,dy:-11},{f:.48,dy:12},{f:.64,dy:-10},{f:.80,dy:11}];
  for(const q of wiggles)await p.mouse.move(panelPt.x+(devicePt.x-panelPt.x)*q.f,panelPt.y+q.dy,{steps:3});
  await p.mouse.move(devicePt.x,devicePt.y,{steps:5});await p.waitForTimeout(50);assert.equal(await p.locator('#cbDetectorCount').innerText(),'1 / 1');await p.mouse.up();
  await p.locator('#cbBack').click();await p.waitForTimeout(120);
  await p.locator('#projectMenuBtn').click();const downloadPromise=p.waitForEvent('download');await p.locator('#backupProject').click();const download=await downloadPromise;const saved=await download.path();const backup=JSON.parse(fs.readFileSync(saved,'utf8'));
  const circuit=backup.project.floors[0].data.circuits[0];assert(circuit,'circuit must be saved in backup');assert(circuit.legs.length>=1,'drag to detector must save a cable leg');const pts=circuit.legs[0].points;
  assert(pts.length<=3,`minor finger wobble created too many route points: ${pts.length}`);
  for(let i=1;i<pts.length;i++){const a=pts[i-1],b=pts[i];assert(Math.abs(a.x-b.x)<1e-6||Math.abs(a.y-b.y)<1e-6,'every stored cable segment must remain orthogonal')}
  assert.deepEqual(errors,[],'No runtime errors');
  console.log('PASS: real Circuit Builder drag ignores finger wobble and stores a clean grid-snapped route');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
