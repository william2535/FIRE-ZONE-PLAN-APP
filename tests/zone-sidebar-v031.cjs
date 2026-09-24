const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),path=require('path'),assert=require('node:assert/strict');

(async()=>{
  const root=process.cwd();
  const server=http.createServer((req,res)=>{
    const u=(req.url||'/').split('?')[0],rel=u==='/'?'index.html':decodeURIComponent(u.slice(1)),file=path.join(root,rel);
    if(!file.startsWith(root)){res.statusCode=403;return res.end('forbidden')}
    try{const data=fs.readFileSync(file);res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':file.endsWith('.css')?'text/css':'text/html');res.end(data)}catch(e){res.statusCode=404;res.end('not found')}
  }).listen(0,'127.0.0.1');
  await new Promise(ok=>server.once('listening',ok));
  const browser=await chromium.launch({headless:true});
  const errors=[];
  try{
    const p=await browser.newPage({viewport:{width:1180,height:900}});
    p.on('pageerror',e=>errors.push(e.message));
    p.on('dialog',d=>d.accept(d.type()==='prompt'?'Sidebar test':undefined));
    await p.goto('http://127.0.0.1:'+server.address().port,{waitUntil:'load'});
    await p.locator('#homeNew').waitFor({state:'visible'});
    await p.waitForFunction(()=>!document.querySelector('#homeNew').disabled);
    await p.locator('#homeNew').click();
    await p.locator('#projectsHome').waitFor({state:'hidden'});

    // v0.31 restores the visible Zones sidebar on tablet/desktop.
    const side=await p.locator('#zoneSide').boundingBox();
    assert(side&&side.width>180,'Zones sidebar should be visible and full width');
    assert.equal(await p.locator('#zoneSide').evaluate(el=>getComputedStyle(el).display),'flex');
    assert.equal(await p.locator('#closeZones').isVisible(),true,'Zones collapse arrow should be visible');

    // Create a zone and make sure its card is visible in the restored sidebar.
    await p.locator('#zoneMenuBtn').click();
    await p.locator('#zoneCreate').click();
    await p.locator('#zoneName').fill('Zone 1 test');
    await p.locator('#saveZone').click();
    await p.locator('#zones .zone').first().waitFor({state:'visible'});
    assert.match(await p.locator('#zones .zone').first().innerText(),/Zone 1 test/);

    // Collapse to the slim rail and reopen it again.
    await p.locator('#closeZones').click();
    await p.waitForTimeout(80);
    assert.equal(await p.locator('#workspace').evaluate(el=>el.classList.contains('zonesClosed')),true);
    const closed=await p.locator('#zoneSide').boundingBox();
    assert(closed&&closed.width<=50,'Collapsed Zones sidebar should become a slim rail');
    await p.locator('#closeZones').click();
    await p.waitForTimeout(80);
    const reopened=await p.locator('#zoneSide').boundingBox();
    assert(reopened&&reopened.width>180,'Zones sidebar should reopen');
    assert.equal(await p.locator('#zones .zone').first().isVisible(),true);

    // Keep the v0.30 wall-style Zone Box snapping behaviour.
    const saved=async()=>{await p.waitForTimeout(460);return p.evaluate(()=>new Promise(ok=>{const r=indexedDB.open('ZoneSketch-v1',1);r.onsuccess=()=>{const db=r.result,g=db.transaction('draft').objectStore('draft').get('state');g.onsuccess=()=>{ok(g.result);db.close()}}}))};
    const xy=async(x,y)=>p.locator('#canvas').evaluate((c,{x,y})=>{const b=c.getBoundingClientRect(),s=Math.min((b.width-48)/3200,(b.height-48)/2000);return{x:b.x+b.width/2+(x-.5)*3200*s,y:b.y+b.height/2+(y-.5)*2000*s}},{x,y});
    const drag=async(x1,y1,x2,y2)=>{const a=await xy(x1,y1),b=await xy(x2,y2);await p.mouse.move(a.x,a.y);await p.mouse.down();await p.mouse.move(b.x,b.y,{steps:12});await p.mouse.up();await p.waitForTimeout(100)};
    await p.locator('#layoutMenuBtn').click();
    await p.locator('[data-menu-tool="layoutRect"]').click();
    await drag(.20,.20,.70,.70);
    let d=await saved();
    const wallPts=d.walls.filter(w=>w.kind==='wall').flatMap(w=>w.points);
    const wallBox={x1:Math.min(...wallPts.map(q=>q.x)),x2:Math.max(...wallPts.map(q=>q.x)),y1:Math.min(...wallPts.map(q=>q.y)),y2:Math.max(...wallPts.map(q=>q.y))};
    await p.locator('#zoneMenuBtn').click();
    await p.locator('[data-menu-tool="rect"]').click();
    await drag(.207,.207,.693,.693);
    d=await saved();
    assert.equal(d.shapes.length,1,'one Zone Box should be created');
    const z=d.shapes[0].points,zoneBox={x1:Math.min(...z.map(q=>q.x)),x2:Math.max(...z.map(q=>q.x)),y1:Math.min(...z.map(q=>q.y)),y2:Math.max(...z.map(q=>q.y))};
    for(const k of ['x1','x2','y1','y2'])assert(Math.abs(zoneBox[k]-wallBox[k])<.0015,`Zone Box ${k} should still snap to the room wall`);

    await p.setViewportSize({width:390,height:844});
    await p.waitForTimeout(100);
    const mobile=await p.locator('#zoneSide').boundingBox();
    assert(mobile&&mobile.height>=90,'Zones strip should remain visible on phone');
    assert.equal(await p.locator('#zones .zone').first().isVisible(),true);

    fs.mkdirSync('test-results',{recursive:true});
    await p.screenshot({path:'test-results/v031-zones-sidebar-phone.png',fullPage:true});
    assert.deepEqual(errors,[],'No browser runtime errors');
    console.log('PASS v0.31: Zones sidebar restored, collapsible, and Zone Box still snaps to walls');
  }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
