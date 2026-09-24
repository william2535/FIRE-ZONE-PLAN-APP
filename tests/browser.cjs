const { chromium }=require('playwright');
const fs=require('fs'), http=require('http'), assert=require('node:assert/strict');
(async()=>{
 const html=fs.readFileSync('index.html');
 const server=http.createServer((req,res)=>{res.setHeader('Content-Type','text/html');res.end(html)}).listen(0,'127.0.0.1');
 await new Promise(ok=>server.once('listening',ok));
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1024,height:768}}), errors=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('dialog',d=>d.accept(d.type()==='prompt'?'Test survey':undefined));
  await page.addInitScript(()=>{window.AndroidBridge={sharePng:(data,name)=>{window.exported={data,name}}}});
  const url='http://127.0.0.1:'+server.address().port;
  await page.goto(url);await page.locator('#homeNew').click();await page.locator('#projectsHome').waitFor({state:'hidden'});await page.waitForTimeout(200);
  const svg='<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500"><rect width="800" height="500" fill="black"/></svg>';
  await page.locator('#file').setInputFiles({name:'plan.svg',mimeType:'image/svg+xml',buffer:Buffer.from(svg)});
  await page.waitForFunction(()=>document.getElementById('empty').hidden);
  const xy=async(x,y,w=800,h=500)=>page.locator('#canvas').evaluate((c,{x,y,w,h})=>{const b=c.getBoundingClientRect(),s=Math.min((b.width-48)/w,(b.height-48)/h);return {x:b.x+b.width/2+(x-.5)*w*s,y:b.y+b.height/2+(y-.5)*h*s}},{x,y,w,h});
  const drag=async(a,b)=>{await page.mouse.move(a.x,a.y);await page.mouse.down();await page.mouse.move(b.x,b.y,{steps:12});await page.mouse.up()};
  await page.locator('#layoutMenuBtn').click();await page.locator('[data-menu-tool="wall"]').click();await drag(await xy(.1,.15),await xy(.75,.15));
  await page.locator('#zoneMenuBtn').click();await page.locator('#zoneCreate').click();await page.locator('#zoneName').fill('Offices');await page.locator('#saveZone').click();
  await page.locator('#zoneMenuBtn').click();await page.locator('[data-menu-tool="rect"]').click();await drag(await xy(.1,.2),await xy(.45,.5));
  await page.locator('#opacity').fill('25');
  await page.evaluate(()=>window.exported=null);await page.locator('#shareBtn').click();await page.locator('#exportPng').click();await page.waitForFunction(()=>window.exported?.data);
  const pixel=async()=>page.evaluate(async()=>{const i=new Image();i.src=window.exported.data;await i.decode();const c=document.createElement('canvas');c.width=i.width;c.height=i.height;const ctx=c.getContext('2d');ctx.drawImage(i,0,0);return [...ctx.getImageData(690,485,1,1).data]});
  let rgba=await pixel();assert(rgba[0]>=189&&rgba[0]<=193,'Export should fade black picture to 25%');
  await page.locator('#togglePicture').click();await page.evaluate(()=>window.exported=null);await page.locator('#shareBtn').click();await page.locator('#exportPng').click();await page.waitForFunction(()=>window.exported?.data);rgba=await pixel();assert.deepEqual(rgba,[255,255,255,255],'Hidden background exports white');
  // Check a wall survives removal of the imported background.
  const wall=await page.evaluate(async()=>{const i=new Image();i.src=window.exported.data;await i.decode();const c=document.createElement('canvas');c.width=i.width;c.height=i.height;const x=c.getContext('2d');x.drawImage(i,0,0);return Math.min(...Array.from(x.getImageData(250,156,1,9).data).filter((_,i)=>i%4===0))});assert(wall<180,'Wall remains in exported drawing');
  await page.waitForTimeout(700);await page.reload();await page.locator('#resumeProject').click();await page.waitForFunction(()=>document.getElementById('togglePicture').textContent==='Show picture');
  assert.equal(await page.locator('#opacity').inputValue(),'25');assert.equal(await page.locator('.zone').count(),1);
  await page.locator('#togglePicture').click();assert.equal(await page.locator('#opacity').isEnabled(),true);
  // Selected-zone panning must not throw or turn into a rectangle.
  await page.locator('#moveModeTop').click();await drag(await xy(.5,.5),await xy(.55,.55));
  await page.locator('#projectMenuBtn').click();await page.locator('#blankBtn').click();await page.waitForTimeout(200);assert.equal(await page.locator('#backgroundBar').isVisible(),false);
  await drag(await xy(.1,.2,1600,1000),await xy(.8,.2,1600,1000));
  await page.locator('#layoutMenuBtn').click();await page.locator('[data-menu-tool="pen"]').click();await drag(await xy(.3,.35,1600,1000),await xy(.6,.6,1600,1000));
  await page.locator('#undo').click();await page.locator('#redo').click();
  await page.evaluate(()=>window.exported=null);await page.locator('#shareBtn').click();await page.locator('#exportPng').click();await page.waitForFunction(()=>window.exported?.data);assert(await page.evaluate(()=>window.exported.data.startsWith('data:image/png')));
  await page.waitForTimeout(700);await page.reload();await page.locator('#resumeProject').click();await page.waitForFunction(()=>document.getElementById('empty').hidden);
  const saved=await page.evaluate(()=>new Promise(ok=>{const r=indexedDB.open('ZoneSketch-v1',1);r.onsuccess=()=>{const g=r.result.transaction('draft').objectStore('draft').get('state');g.onsuccess=()=>ok(g.result)}}));
  assert.equal(saved.isBlank,true);assert.equal(saved.walls.length,2);assert.equal(saved.shapes.length,0);
  await page.locator('#site').fill('Blank canvas test');
  fs.mkdirSync('test-results',{recursive:true});await page.screenshot({path:'test-results/tablet.png'});
  await page.setViewportSize({width:390,height:844});await page.screenshot({path:'test-results/phone.png'});
  assert.deepEqual(errors,[],'No browser runtime errors');
  console.log('PASS: trace lines, zones, faded export, picture-free export, restore picture, persistence, blank drawing, undo/redo and phone layout');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});

