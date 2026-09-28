const {chromium,webkit}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');

(async()=>{
  const server=http.createServer((q,r)=>{const p=(q.url||'/').split('?')[0],file=p==='/'?'index.html':p.slice(1);try{const data=fs.readFileSync(file);r.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':'text/html');r.end(data)}catch(e){r.statusCode=404;r.end('not found')}}).listen(0,'127.0.0.1');
  await new Promise(r=>server.once('listening',r));
  const engine=process.env.PINEAPPLE_BROWSER==='webkit'?webkit:chromium;
  const browser=await engine.launch({headless:true});
  try{
    const page=await browser.newPage({viewport:{width:980,height:760}}),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('dialog',d=>d.accept(d.type()==='prompt'?'v0.63 test':undefined));
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
    async function shapeCentre(index){
      return page.evaluate(i=>{const pts=state.shapes[i].points,c={x:pts.reduce((n,p)=>n+p.x,0)/pts.length,y:pts.reduce((n,p)=>n+p.y,0)/pts.length},q=screenPoint(c),r=canvas.getBoundingClientRect();return{x:r.left+q.x,y:r.top+q.y,zone:state.shapes[i].zone}},index);
    }
    async function snapshot(){
      return page.evaluate(()=>({selected,tool,buildMode:state.buildMode,zoneOpacity:state.zoneOpacity,shapes:JSON.parse(JSON.stringify(state.shapes)),zones:JSON.parse(JSON.stringify(state.zones))}));
    }

    await addZone(1,'Offices');
    await selectBoxTool();
    await dragOnCanvas(130,130,360,330);
    await addZone(2,'Stores');
    await selectBoxTool();
    await dragOnCanvas(540,150,800,340);
    let s=await snapshot();
    assert.equal(s.shapes.length,2,'two zone areas should be ready for quick-edit testing');
    const zone1=s.shapes[0].zone,zone2=s.shapes[1].zone;
    assert.notEqual(zone1,zone2,'test fixture must contain two different zones');

    // Combined Build mode: one tap picks an existing zone without changing tools or geometry.
    await page.locator('#settingsMenuBtn').click();
    await page.locator('#buildModeBtn').click();
    await page.waitForTimeout(100);
    s=await snapshot();
    assert.equal(s.buildMode,false,'Build mode should be OFF for quick-edit workflow');
    assert.equal(s.selected,zone2,'Zone 2 should still be active before quick-pick');
    const first=await shapeCentre(0),beforeTap=JSON.stringify(s.shapes);
    await page.mouse.click(first.x,first.y);
    await page.waitForTimeout(100);
    s=await snapshot();
    assert.equal(s.selected,zone1,'tapping an existing area should make its zone active');
    assert.equal(s.tool,'rect','quick-pick must leave the placement tool armed');
    assert.equal(JSON.stringify(s.shapes),beforeTap,'quick-pick must not move or duplicate the tapped area');
    assert.match(await page.locator('#zoneMenuBtn').innerText(),/Zone 1/,'zone menu should immediately show the picked zone');

    // Dragging the same area still moves it and does not create another zone.
    const movedFrom=JSON.stringify(s.shapes[0].points);
    await page.mouse.move(first.x,first.y);
    await page.mouse.down();
    await page.mouse.move(first.x+70,first.y+45,{steps:8});
    await page.mouse.up();
    await page.waitForTimeout(100);
    s=await snapshot();
    assert.equal(s.shapes.length,2,'combined drag should move rather than add a third area');
    assert.notEqual(JSON.stringify(s.shapes[0].points),movedFrom,'existing zone area should move');
    assert.equal(s.tool,'rect','placement tool must remain armed after moving');

    // Zone tint is a per-floor drawing setting and feeds both live canvas and Zone Plan export rendering.
    await page.locator('#settingsMenuBtn').click();
    const tint=page.locator('#zoneOpacity');
    await tint.waitFor({state:'visible'});
    await tint.evaluate(el=>{el.value='29';el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}))});
    await page.waitForTimeout(80);
    assert.equal(await page.locator('#zoneOpacityValue').innerText(),'29%');
    const tintState=await page.evaluate(()=>({state:state.zoneOpacity,floor:floorData().zoneOpacity}));
    assert(Math.abs(tintState.state-.29)<1e-9,'zone tint should update state');
    assert(Math.abs(tintState.floor-.29)<1e-9,'zone tint should be included in floor persistence');
    const alphas=await page.evaluate(async()=>{
      const seen=[];const original=drawZoneLayer;
      drawZoneLayer=function(...args){seen.push(args[4]);return original(...args)};
      paint();syncFloor();await renderModeFloorCanvas(activeFloor(),700,'zone',1);
      drawZoneLayer=original;return seen;
    });
    assert(alphas.some(v=>Math.abs(v-.29)<1e-9),'29% tint should be used by live/export zone drawing');
    await page.keyboard.press('Escape').catch(()=>{});

    // The tint control is Zone Plan specific, then remains touch-friendly when returning on phone width.
    await page.locator('#surveyModeBtn').click();
    assert.equal(await page.locator('#zoneOpacityControl').isHidden(),true,'zone tint should stay out of Survey mode');
    await page.locator('#surveyModeBtn').click();
    await page.setViewportSize({width:390,height:844});
    await page.locator('#settingsMenuBtn').click();
    const box=await page.locator('#zoneOpacity').boundingBox();
    assert(box&&box.width>120,'zone tint slider should remain comfortably usable on a phone');

    fs.mkdirSync('test-results',{recursive:true});
    await page.screenshot({path:`test-results/zone-quick-edit-v063-${process.env.PINEAPPLE_BROWSER||'chromium'}.png`});
    assert.deepEqual(errors,[]);
    console.log(`PASS v0.63 (${process.env.PINEAPPLE_BROWSER||'chromium'}): Zone quick-pick, combined move/place and per-floor tint behave safely`);
  }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
