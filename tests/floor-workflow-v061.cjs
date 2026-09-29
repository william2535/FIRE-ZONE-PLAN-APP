const {openHeader}=require('./header-navigation.cjs');
const {chromium,webkit}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');

(async()=>{
  const server=http.createServer((q,r)=>{const p=(q.url||'/').split('?')[0],file=p==='/'?'index.html':p.slice(1);try{const data=fs.readFileSync(file);r.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':'text/html');r.end(data)}catch(e){r.statusCode=404;r.end('not found')}}).listen(0,'127.0.0.1');
  await new Promise(r=>server.once('listening',r));
  const engine=process.env.PINEAPPLE_BROWSER==='webkit'?webkit:chromium;
  const browser=await engine.launch({headless:true});
  try{
    const page=await browser.newPage({viewport:{width:1180,height:820}}),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('dialog',d=>d.accept(d.type()==='prompt'?'Floor workflow':undefined));
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
    async function drawZoneBox(x1,y1,x2,y2){
      await page.locator('#zoneMenuBtn').click();
      await page.locator('[data-menu-tool="rect"]').click();
      const b=await page.locator('#canvas').boundingBox();
      await page.mouse.move(b.x+x1,b.y+y1);await page.mouse.down();await page.mouse.move(b.x+x2,b.y+y2,{steps:5});await page.mouse.up();
    }
    async function saved(){
      await page.waitForTimeout(450);
      return page.evaluate(()=>new Promise(ok=>{const r=indexedDB.open('ZoneSketch-v1',1);r.onsuccess=()=>{const g=r.result.transaction('draft').objectStore('draft').get('state');g.onsuccess=()=>ok(g.result)}}));
    }

    // Ground floor: two zones, a drawn zone area, and Zone 2 intentionally selected.
    await addZone(1,'Ground offices');
    await drawZoneBox(160,130,430,360);
    await addZone(2,'Ground store');
    await page.locator('#zones .zone').filter({hasText:'Zone 2'}).click();
    let s=await saved();
    const groundId=s.activeFloor;
    assert.equal(s.zones.length,2);
    assert.equal(s.shapes.length,1);
    assert.equal(s.floors.find(f=>f.id===groundId).data.zones.length,2,'active floor snapshot should update immediately');
    assert.equal(s.floors.find(f=>f.id===groundId).data.activeZoneId,s.zones.find(z=>z.number==='2').id,'selected zone should be stored with the floor');

    // Create First floor, give it different zone data, then switch rapidly back and forth.
    await openHeader(page);await page.locator('#floorMenuBtn').click();await page.locator('#addFloor').click();await page.locator('#saveFloor').click();
    await addZone(11,'First offices');
    await drawZoneBox(520,160,760,390);
    s=await saved();
    const firstId=s.activeFloor;
    assert.notEqual(firstId,groundId);
    assert.deepEqual(s.zones.map(z=>z.number),['11']);
    assert.equal(s.shapes.length,1);

    await openHeader(page);await page.locator('#floorMenuBtn').click();await page.locator('.floorChoice').filter({hasText:'Ground floor'}).click();
    await page.waitForFunction(id=>document.querySelector('#floorSelect').value===id,groundId);
    await page.waitForFunction(()=>[...document.querySelectorAll('#zones .zone b')].map(n=>n.textContent).join('|')==='Zone 1|Zone 2');
    assert.deepEqual(await page.locator('#zones .zone b').allTextContents(),['Zone 1','Zone 2']);
    assert.match(await page.locator('#zones .zone.active').innerText(),/Zone 2/,'Ground floor should restore its last selected zone instead of resetting to Zone 1');
    s=await saved();
    assert.equal(s.shapes.length,1,'Ground floor zone geometry should survive floor switches');

    await openHeader(page);await page.locator('#floorMenuBtn').click();await page.locator('.floorChoice').filter({hasText:'First floor'}).click();
    await page.waitForFunction(id=>document.querySelector('#floorSelect').value===id,firstId);
    await page.waitForFunction(()=>[...document.querySelectorAll('#zones .zone b')].map(n=>n.textContent).join('|')==='Zone 11');
    assert.deepEqual(await page.locator('#zones .zone b').allTextContents(),['Zone 11']);
    s=await saved();
    assert.equal(s.shapes.length,1,'First floor zone geometry should remain isolated and saved');

    // Circuit Builder now owns the same floor switch, without leaving the workflow.
    await openHeader(page);await page.locator('#circuitModeBtn').click();
    await page.locator('#circuitBuilder').waitFor({state:'visible'});
    assert.equal(await page.locator('#cbFloorSelect option').count(),2);
    assert.equal(await page.locator('#cbFloorSelect').inputValue(),firstId);
    assert.match(await page.locator('#cbConventionalZones').innerText(),/Zone 11/);

    await page.locator('#cbFloorSelect').selectOption(groundId);
    await page.waitForFunction(id=>document.querySelector('#cbFloorSelect').value===id,groundId);
    await page.waitForFunction(()=>document.querySelector('#cbConventionalZones').innerText.includes('Zone 2'));
    const groundCircuitText=await page.locator('#cbConventionalZones').innerText();
    assert.match(groundCircuitText,/Zone 1/);assert.match(groundCircuitText,/Zone 2/);assert.doesNotMatch(groundCircuitText,/Zone 11/);

    await page.locator('#cbFloorSelect').selectOption(firstId);
    await page.waitForFunction(id=>document.querySelector('#cbFloorSelect').value===id,firstId);
    await page.waitForFunction(()=>document.querySelector('#cbConventionalZones').innerText.includes('Zone 11'));
    const firstCircuitText=await page.locator('#cbConventionalZones').innerText();
    assert.match(firstCircuitText,/Zone 11/);assert.doesNotMatch(firstCircuitText,/Zone 1\b/);

    await page.setViewportSize({width:390,height:844});
    const floorSwitch=await page.locator('.cbFloorSwitch').boundingBox();
    assert(floorSwitch&&floorSwitch.width>300,'Circuit floor switch should remain usable on phone/tablet widths');
    fs.mkdirSync('test-results',{recursive:true});
    await page.screenshot({path:`test-results/floor-workflow-v061-${process.env.PINEAPPLE_BROWSER||'chromium'}.png`});
    assert.deepEqual(errors,[]);
    console.log(`PASS v0.61 (${process.env.PINEAPPLE_BROWSER||'chromium'}): zone data and selected zone survive floor switches; Circuit Builder can switch floors in place`);
  }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
