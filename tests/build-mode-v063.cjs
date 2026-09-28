const {chromium,webkit}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');

(async()=>{
  const server=http.createServer((q,r)=>{const p=(q.url||'/').split('?')[0],file=p==='/'?'index.html':p.slice(1);try{const data=fs.readFileSync(file);r.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':'text/html');r.end(data)}catch(e){r.statusCode=404;r.end('not found')}}).listen(0,'127.0.0.1');
  await new Promise(r=>server.once('listening',r));
  const engine=process.env.PINEAPPLE_BROWSER==='webkit'?webkit:chromium;
  const browser=await engine.launch({headless:true});
  try{
    const page=await browser.newPage({viewport:{width:980,height:760}}),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('dialog',d=>d.accept(d.type()==='prompt'?'Build mode integration test':undefined));
    await page.goto('http://127.0.0.1:'+server.address().port,{waitUntil:'load'});
    await page.locator('#homeNew').click();
    await page.locator('#projectsHome').waitFor({state:'hidden'});

    async function addZone(){
      await page.locator('#zoneMenuBtn').click();
      await page.locator('#zoneCreate').click();
      await page.locator('#zoneNo').fill('1');
      await page.locator('#zoneName').fill('Small office');
      await page.locator('#saveZone').click();
    }
    async function selectBox(){
      await page.locator('#zoneMenuBtn').click();
      await page.locator('[data-menu-tool="rect"]').click();
    }
    async function dragCanvas(x1,y1,x2,y2){
      const b=await page.locator('#canvas').boundingBox();
      await page.mouse.move(b.x+x1,b.y+y1);await page.mouse.down();
      await page.mouse.move(b.x+x2,b.y+y2,{steps:8});await page.mouse.up();
    }
    async function dragAbs(a,b){
      await page.mouse.move(a.x,a.y);await page.mouse.down();
      await page.mouse.move(b.x,b.y,{steps:8});await page.mouse.up();
    }
    async function saved(){
      await page.waitForTimeout(350);
      return page.evaluate(()=>new Promise(ok=>{const r=indexedDB.open('ZoneSketch-v1',1);r.onsuccess=()=>{const g=r.result.transaction('draft').objectStore('draft').get('state');g.onsuccess=()=>ok(g.result)}}));
    }
    async function shapeCentre(shape){
      const p={x:shape.points.reduce((n,q)=>n+q.x,0)/shape.points.length,y:shape.points.reduce((n,q)=>n+q.y,0)/shape.points.length};
      return page.locator('#canvas').evaluate((c,p)=>{const b=c.getBoundingClientRect(),w=3200,h=2000,s=Math.min((b.width-48)/w,(b.height-48)/h);return{x:b.x+b.width/2+(p.x-.5)*w*s,y:b.y+b.height/2+(p.y-.5)*h*s}},p);
    }

    await addZone();await selectBox();await dragCanvas(170,130,430,360);
    let s=await saved();
    assert.equal(s.shapes.length,1);
    assert.equal(s.buildMode,true);

    // Reproduce the real-device conflict: old Pan is ON before Build mode is turned OFF.
    await page.locator('#moveModeTop').click();
    assert.match(await page.locator('#moveModeTop').innerText(),/Pan ON/);
    await page.locator('#settingsMenuBtn').click();
    await page.locator('#buildModeBtn').click();
    await page.waitForTimeout(120);
    s=await saved();
    assert.equal(s.buildMode,false,'Build mode OFF must persist');
    assert.equal(await page.locator('#moveModeTop').isDisabled(),true,'combined Build mode must disable one-finger Pan so it cannot override Place + move');
    assert.match(await page.locator('#moveModeTop').innerText(),/Pan · 2 fingers/,'combined mode should explain the navigation path');

    // With Pan previously ON, the exact same existing-zone drag must now move instead of pan or place.
    const beforeMove=JSON.stringify(s.shapes[0].points),centre=await shapeCentre(s.shapes[0]);
    await dragAbs(centre,{x:centre.x+70,y:centre.y+55});
    s=await saved();
    assert.equal(s.shapes.length,1,'combined mode should not create another zone when dragging an existing zone');
    assert.notEqual(JSON.stringify(s.shapes[0].points),beforeMove,'existing zone must actually move after Build mode disables the old Pan override');
    assert.equal(await page.locator('[data-menu-tool="rect"]').getAttribute('class').then(v=>/active/.test(v||'')),true,'placement tool must stay armed after moving');

    await dragCanvas(650,150,820,300);
    s=await saved();
    assert.equal(s.shapes.length,2,'empty space must still place a new zone with the same armed tool');

    // Restore separated behaviour: Pan becomes available again and takes one-finger navigation deliberately.
    await page.locator('#settingsMenuBtn').click();
    await page.locator('#buildModeBtn').click();
    await page.waitForTimeout(100);
    assert.equal(await page.locator('#moveModeTop').isDisabled(),false,'Build mode ON should restore the explicit Pan control');
    assert.match(await page.locator('#moveModeTop').innerText(),/Pan OFF/);
    await page.locator('#moveModeTop').click();
    assert.match(await page.locator('#moveModeTop').innerText(),/Pan ON/);
    const beforePan=JSON.stringify((await saved()).shapes);
    const c2=await shapeCentre((await saved()).shapes[0]);
    await dragAbs(c2,{x:c2.x+60,y:c2.y+45});
    assert.equal(JSON.stringify((await saved()).shapes),beforePan,'separated Pan mode must navigate without editing zone geometry');
    await page.locator('#moveModeTop').click();

    await page.setViewportSize({width:390,height:844});
    await page.locator('#settingsMenuBtn').click();
    const build=page.locator('#buildModeBtn');
    await build.click();
    assert.equal(await page.locator('#moveModeTop').isDisabled(),true,'phone combined mode must also prevent Pan override');
    fs.mkdirSync('test-results',{recursive:true});
    await page.screenshot({path:`test-results/build-mode-v063-${process.env.PINEAPPLE_BROWSER||'chromium'}.png`});
    assert.deepEqual(errors,[]);
    console.log(`PASS v0.63 (${process.env.PINEAPPLE_BROWSER||'chromium'}): Build mode OFF defeats the old Pan override and keeps Place + move active`);
  }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
