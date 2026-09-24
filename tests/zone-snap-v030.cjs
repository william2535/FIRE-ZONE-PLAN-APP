const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),path=require('path'),assert=require('node:assert/strict');

(async()=>{
  const root=process.cwd();
  const server=http.createServer((req,res)=>{
    const u=(req.url||'/').split('?')[0];
    const rel=u==='/'?'index.html':decodeURIComponent(u.slice(1));
    const file=path.join(root,rel);
    if(!file.startsWith(root)){res.statusCode=403;return res.end('forbidden')}
    try{
      const data=fs.readFileSync(file);
      if(file.endsWith('.js'))res.setHeader('Content-Type','text/javascript');
      else if(file.endsWith('.css'))res.setHeader('Content-Type','text/css');
      else res.setHeader('Content-Type','text/html');
      res.end(data);
    }catch(e){res.statusCode=404;res.end('not found')}
  }).listen(0,'127.0.0.1');
  await new Promise(ok=>server.once('listening',ok));
  const browser=await chromium.launch({headless:true});
  const errors=[];
  try{
    const p=await browser.newPage({viewport:{width:1180,height:900}});
    p.on('pageerror',e=>errors.push(e.message));
    await p.goto('http://127.0.0.1:'+server.address().port,{waitUntil:'load'});
    await p.locator('#homeNew').click();
    await p.locator('#projectsHome').waitFor({state:'hidden'});
    await p.waitForTimeout(180);

    // No permanent Zones barrier: the canvas should take the workspace width.
    const layout=await p.evaluate(()=>{
      const side=document.querySelector('#zoneSide'),wrap=document.querySelector('#wrap').getBoundingClientRect(),workspace=document.querySelector('#workspace').getBoundingClientRect();
      return {sideDisplay:getComputedStyle(side).display,wrapWidth:wrap.width,workspaceWidth:workspace.width,wrapLeft:wrap.left-workspace.left};
    });
    assert.equal(layout.sideDisplay,'none','Zones side panel should not occupy any permanent canvas space');
    assert(layout.wrapWidth>=layout.workspaceWidth-2,`canvas should fill workspace: ${JSON.stringify(layout)}`);
    assert(Math.abs(layout.wrapLeft)<2,`canvas should start at workspace edge: ${JSON.stringify(layout)}`);

    const saved=async()=>{await p.waitForTimeout(460);return p.evaluate(()=>new Promise(ok=>{const r=indexedDB.open('ZoneSketch-v1',1);r.onsuccess=()=>{const db=r.result,g=db.transaction('draft').objectStore('draft').get('state');g.onsuccess=()=>{ok(g.result);db.close()}}}))};
    const xy=async(x,y)=>p.locator('#canvas').evaluate((c,{x,y})=>{const b=c.getBoundingClientRect(),s=Math.min((b.width-48)/3200,(b.height-48)/2000);return{x:b.x+b.width/2+(x-.5)*3200*s,y:b.y+b.height/2+(y-.5)*2000*s}},{x,y});
    const drag=async(x1,y1,x2,y2)=>{const a=await xy(x1,y1),b=await xy(x2,y2);await p.mouse.move(a.x,a.y);await p.mouse.down();await p.mouse.move(b.x,b.y,{steps:12});await p.mouse.up();await p.waitForTimeout(100)};

    // Make a real room first.
    await p.locator('#layoutMenuBtn').click();
    await p.locator('[data-menu-tool="layoutRect"]').click();
    await drag(.20,.20,.70,.70);
    let d=await saved();
    assert(d.walls.length>=4,'room should create building walls');
    const wallPts=d.walls.filter(w=>w.kind==='wall').flatMap(w=>w.points);
    const wallBox={x1:Math.min(...wallPts.map(q=>q.x)),x2:Math.max(...wallPts.map(q=>q.x)),y1:Math.min(...wallPts.map(q=>q.y)),y2:Math.max(...wallPts.map(q=>q.y))};

    // Create a zone entirely from the bottom Zone menu, then drag slightly off
    // the room corners. v0.30 should pull the Zone Box onto the wall geometry.
    await p.locator('#zoneMenuBtn').click();
    await p.locator('#zoneCreate').click();
    await p.locator('#zoneName').fill('Snapped room');
    await p.locator('#saveZone').click();
    await p.locator('#zoneMenuBtn').click();
    await p.locator('[data-menu-tool="rect"]').click();
    await drag(.207,.207,.693,.693);
    d=await saved();
    assert.equal(d.shapes.length,1,'one Zone Box should be created');
    const z=d.shapes[0].points;
    const zoneBox={x1:Math.min(...z.map(q=>q.x)),x2:Math.max(...z.map(q=>q.x)),y1:Math.min(...z.map(q=>q.y)),y2:Math.max(...z.map(q=>q.y))};
    for(const k of ['x1','x2','y1','y2'])assert(Math.abs(zoneBox[k]-wallBox[k])<.0015,`Zone Box ${k} should snap to room wall (${zoneBox[k]} vs ${wallBox[k]})`);

    // The zone remains editable/selectable from the bottom menu with no sidebar.
    await p.locator('#zoneMenuBtn').click();
    assert.equal(await p.locator('#zoneMenu .zoneChoice').count(),1);
    assert.equal(await p.locator('#zoneMenu .zoneChoice').first().isVisible(),true);
    await p.locator('#zoneMenuBtn').click();

    await p.setViewportSize({width:390,height:844});
    await p.waitForTimeout(80);
    assert.equal(await p.locator('#zoneSide').evaluate(el=>getComputedStyle(el).display),'none');
    const mobile=await p.locator('#wrap').boundingBox();
    assert(mobile&&mobile.width>=388,'mobile canvas should use the full available width');
    await p.locator('#zoneMenuBtn').click();
    assert.equal(await p.locator('#zoneMenu .zoneChoice').first().isVisible(),true,'Zone menu must remain usable on phone');

    fs.mkdirSync('test-results',{recursive:true});
    await p.screenshot({path:'test-results/v030-full-canvas-zone-snap-phone.png',fullPage:true});
    assert.deepEqual(errors,[],'No browser runtime errors');
    console.log('PASS v0.30: no zone barrier and Zone Box snaps to building walls');
  }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
