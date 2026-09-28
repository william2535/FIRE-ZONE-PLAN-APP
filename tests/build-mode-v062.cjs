const {chromium,webkit}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');

(async()=>{
  const server=http.createServer((q,r)=>{const p=(q.url||'/').split('?')[0],file=p==='/'?'index.html':p.slice(1);try{const data=fs.readFileSync(file);r.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':'text/html');r.end(data)}catch(e){r.statusCode=404;r.end('not found')}}).listen(0,'127.0.0.1');
  await new Promise(r=>server.once('listening',r));
  const engine=process.env.PINEAPPLE_BROWSER==='webkit'?webkit:chromium;
  const browser=await engine.launch({headless:true});
  try{
    const page=await browser.newPage({viewport:{width:980,height:760}}),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('dialog',d=>d.accept(d.type()==='prompt'?'Build mode test':undefined));
    await page.goto('http://127.0.0.1:'+server.address().port,{waitUntil:'load'});
    await page.locator('#homeNew').click();
    await page.locator('#projectsHome').waitFor({state:'hidden'});

    async function addZone(number,name){
      await page.locator('#zoneMenuBtn').click();
      await page.locator('#zoneCreate').click();
      await page.locator('#zoneNo').fill(String(number));
      await page.locator('#zoneName').fill(name);
      await page.locator('#saveZone').click();
    }
    async function selectBoxTool(){
      await page.locator('#zoneMenuBtn').click();
      await page.locator('[data-menu-tool="rect"]').click();
    }
    async function dragOnCanvas(x1,y1,x2,y2){
      const b=await page.locator('#canvas').boundingBox();
      await page.mouse.move(b.x+x1,b.y+y1);
      await page.mouse.down();
      await page.mouse.move(b.x+x2,b.y+y2,{steps:8});
      await page.mouse.up();
    }
    async function dragAbs(a,b){
      await page.mouse.move(a.x,a.y);
      await page.mouse.down();
      await page.mouse.move(b.x,b.y,{steps:8});
      await page.mouse.up();
    }
    async function saved(){
      await page.waitForTimeout(400);
      return page.evaluate(()=>new Promise(ok=>{const r=indexedDB.open('ZoneSketch-v1',1);r.onsuccess=()=>{const g=r.result.transaction('draft').objectStore('draft').get('state');g.onsuccess=()=>ok(g.result)}}));
    }
    async function normalizedToScreen(p){
      return page.locator('#canvas').evaluate((c,p)=>{const b=c.getBoundingClientRect(),w=3200,h=2000,s=Math.min((b.width-48)/w,(b.height-48)/h);return{x:b.x+b.width/2+(p.x-.5)*w*s,y:b.y+b.height/2+(p.y-.5)*h*s}},p);
    }
    async function firstShapeCentre(snapshot){
      const pts=snapshot.shapes[0].points,p={x:pts.reduce((n,q)=>n+q.x,0)/pts.length,y:pts.reduce((n,q)=>n+q.y,0)/pts.length};
      return normalizedToScreen(p);
    }

    await addZone(1,'Small office');
    await selectBoxTool();
    await dragOnCanvas(170,130,430,360);
    let s=await saved();
    assert.equal(s.shapes.length,1,'initial zone box should exist');
    assert.equal(s.buildMode,true,'Build mode should default ON for existing separated behaviour');

    // Build mode ON: start deliberately inside the existing saved zone. The armed placement tool
    // still creates a new zone box, proving placement and moving remain separate.
    const firstBefore=JSON.stringify(s.shapes[0].points),insideOn=await firstShapeCentre(s);
    await dragAbs(insideOn,{x:insideOn.x+70,y:insideOn.y+55});
    s=await saved();
    assert.equal(s.shapes.length,2,'Build mode ON should keep the box placement tool armed rather than moving the old zone');
    assert.equal(JSON.stringify(s.shapes[0].points),firstBefore,'original zone must not move while Build mode is ON');
    await page.locator('#undoTop').click();
    await page.waitForTimeout(120);
    s=await saved();
    assert.equal(s.shapes.length,1,'undo should return to one zone before combined-mode test');

    // Toggle from Drawing, beside the grid controls.
    await page.locator('#settingsMenuBtn').click();
    const build=page.locator('#buildModeBtn');
    await build.waitFor({state:'visible'});
    assert.match(await build.innerText(),/Build mode[\s\S]*ON · Separate/);
    assert.match(await page.locator('#buildModeHelp').innerText(),/larger plans/i);
    await build.click();
    await page.waitForTimeout(120);
    assert.match(await page.locator('#buildModeBtn').innerText(),/OFF · Place \+ move/);
    assert.equal(await page.locator('#buildModeBtn').getAttribute('aria-pressed'),'false');
    s=await saved();
    assert.equal(s.buildMode,false,'Build mode OFF must persist in project state');

    // OFF: use the centre calculated from the actual saved zone so this test cannot hit blank canvas.
    // The existing zone moves, no second zone is created, and the rect placement tool stays armed.
    const beforeMove=JSON.stringify(s.shapes[0].points),insideOff=await firstShapeCentre(s);
    await dragAbs(insideOff,{x:insideOff.x+75,y:insideOff.y+55});
    s=await saved();
    assert.equal(s.shapes.length,1,'combined mode should move the existing zone instead of adding a new one');
    assert.notEqual(JSON.stringify(s.shapes[0].points),beforeMove,'existing zone should actually move in combined mode');
    assert.equal(await page.locator('[data-menu-tool="rect"]').getAttribute('class').then(v=>/active/.test(v||'')),true,'zone box tool should remain active after moving a zone');

    // Empty space still places with the same armed tool.
    await dragOnCanvas(650,150,820,300);
    s=await saved();
    assert.equal(s.shapes.length,2,'combined mode must still place a new zone on empty space');

    // Turn Build mode back on and verify the separated state is restored.
    await page.locator('#settingsMenuBtn').click();
    await page.locator('#buildModeBtn').click();
    await page.waitForTimeout(120);
    s=await saved();
    assert.equal(s.buildMode,true);
    await page.locator('#settingsMenuBtn').click();
    assert.match(await page.locator('#buildModeBtn').innerText(),/ON · Separate/);
    await page.keyboard.press('Escape').catch(()=>{});

    await page.setViewportSize({width:390,height:844});
    await page.locator('#settingsMenuBtn').click();
    const menu=await page.locator('#settingsMenu').boundingBox();
    const toggle=await page.locator('#buildModeBtn').boundingBox();
    assert(menu&&toggle&&toggle.width>180,'Build mode toggle should remain comfortably tappable on phone widths');
    fs.mkdirSync('test-results',{recursive:true});
    await page.screenshot({path:`test-results/build-mode-v062-${process.env.PINEAPPLE_BROWSER||'chromium'}.png`});
    assert.deepEqual(errors,[]);
    console.log(`PASS v0.62 (${process.env.PINEAPPLE_BROWSER||'chromium'}): Build mode toggles separate vs combined Zone Plan placement/moving and persists safely`);
  }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
