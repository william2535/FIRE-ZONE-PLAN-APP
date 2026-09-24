const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');
(async()=>{const server=http.createServer((q,r)=>r.end(fs.readFileSync('index.html'))).listen(0,'127.0.0.1');await new Promise(r=>server.once('listening',r));const browser=await chromium.launch({headless:true});try{
const p=await browser.newPage({viewport:{width:1180,height:900}}),errors=[];p.on('pageerror',e=>errors.push(e.message));p.on('dialog',d=>d.accept());await p.goto('http://127.0.0.1:'+server.address().port);await p.waitForTimeout(150);await p.locator('#emptyBlank').click();
const saved=async()=>{await p.waitForTimeout(500);return p.evaluate(()=>new Promise(ok=>{const r=indexedDB.open('ZoneSketch-v1',1);r.onsuccess=()=>{const db=r.result,g=db.transaction('draft').objectStore('draft').get('state');g.onsuccess=()=>{ok(g.result);db.close()}}}))};
const xy=async(x,y)=>p.locator('#canvas').evaluate((c,{x,y})=>{const b=c.getBoundingClientRect(),s=Math.min((b.width-48)/3200,(b.height-48)/2000);return{x:b.x+b.width/2+(x-.5)*3200*s,y:b.y+b.height/2+(y-.5)*2000*s}},{x,y});
const click=async(x,y)=>{const a=await xy(x,y);await p.mouse.click(a.x,a.y)};const drag=async(x1,y1,x2,y2)=>{const a=await xy(x1,y1),b=await xy(x2,y2);await p.mouse.move(a.x,a.y);await p.mouse.down();await p.mouse.move(b.x,b.y,{steps:16});await p.mouse.up()};const tool=async(menu,t)=>{await p.locator('#'+menu+'MenuBtn').click();await p.locator('[data-menu-tool="'+t+'"]').click()};

// A normal rectangular room gives us a straight wall for a double door.
await tool('layout','layoutRect');await drag(.08,.18,.62,.48);let d=await saved();assert.equal(d.walls.length,4);

// Double door: one wall opening, two leaves, swing side follows the finger and persists.
await tool('object','doubleDoor');await drag(.24,.18,.46,.12);d=await saved();assert.equal(d.doors.length,1);assert.equal(d.doors[0].double,true);assert.equal(d.doors[0].side,-1);assert.equal(d.walls.length,5,'double door splits only the wall opening');

// The second leaf must be selectable/deletable too, not only the first hinge side.
await p.locator('#deleteTop').click();await click(.46,.10);d=await saved();assert.equal(d.doors.length,0,'second double-door leaf can be deleted');assert.equal(d.walls.length,5,'deleting door preserves the intentional opening');await p.locator('#undoTop').click();d=await saved();assert.equal(d.doors.length,1);assert.equal(d.doors[0].double,true);

// Circular room creates actual editable wall sections, not a cosmetic ellipse.
await tool('layout','layoutEllipse');await drag(.66,.54,.92,.84);d=await saved();const curved=d.walls.filter(w=>w.group);assert(curved.length>=28,'circular room is built from many wall sections');assert(curved.every(w=>w.kind==='wall'&&w.points.length===2));

// Because it is genuine wall geometry, Zone Fill Area must recognise it as enclosed.
await p.locator('#zoneMenuBtn').click();await p.locator('#zoneCreate').click();await p.locator('#zoneName').fill('Circular office');await p.locator('#saveZone').click();await tool('zone','fill');await click(.79,.69);d=await saved();assert.equal(d.shapes.length,1,'circular room accepts automatic zone fill');assert(d.shapes[0].points.length>=20,'filled zone follows the curved wall polygon');

// Menus remain usable at phone width after adding the extra public-release tools.
await p.setViewportSize({width:390,height:844});await p.locator('#layoutMenuBtn').click();let box=await p.locator('#layoutMenu').boundingBox();assert(box&&box.x>=0&&box.y>=0&&box.x+box.width<=390&&box.y+box.height<=844);assert.equal(await p.locator('[data-menu-tool="layoutEllipse"]').isVisible(),true);await p.locator('#layoutMenuBtn').click();await p.locator('#objectMenuBtn').click();box=await p.locator('#objectMenu').boundingBox();assert(box&&box.x>=0&&box.y>=0&&box.x+box.width<=390&&box.y+box.height<=844);assert.equal(await p.locator('[data-menu-tool="doubleDoor"]').isVisible(),true);

fs.mkdirSync('test-results',{recursive:true});await p.screenshot({path:'test-results/v020-public-mobile.png',fullPage:true});assert.deepEqual(errors,[]);console.log('PASS v0.20: double-door geometry/hit testing, circular wall room, zone fill and mobile menus');
}finally{await browser.close();server.close()}})().catch(e=>{console.error(e);process.exit(1)});
