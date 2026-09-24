const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');
(async()=>{const server=http.createServer((q,r)=>r.end(fs.readFileSync('index.html'))).listen(0,'127.0.0.1');await new Promise(r=>server.once('listening',r));const browser=await chromium.launch({headless:true});try{
const p=await browser.newPage({viewport:{width:1180,height:900}}),errors=[];p.on('pageerror',e=>errors.push(e.message));p.on('dialog',d=>d.accept(d.type()==='prompt'?'Drawing tools test':undefined));await p.goto('http://127.0.0.1:'+server.address().port);await p.locator('#homeNew').click();await p.locator('#projectsHome').waitFor({state:'hidden'});await p.locator('#emptyBlank').click();await p.waitForTimeout(120);
const saved=async()=>{await p.waitForTimeout(420);return p.evaluate(()=>new Promise(ok=>{const r=indexedDB.open('ZoneSketch-v1',1);r.onsuccess=()=>{const db=r.result,g=db.transaction('draft').objectStore('draft').get('state');g.onsuccess=()=>{ok(g.result);db.close()}}}))};
const xy=async(x,y)=>p.locator('#canvas').evaluate((c,{x,y})=>{const b=c.getBoundingClientRect(),s=Math.min((b.width-48)/3200,(b.height-48)/2000);return{x:b.x+b.width/2+(x-.5)*3200*s,y:b.y+b.height/2+(y-.5)*2000*s}},{x,y});
const click=async(x,y)=>{const a=await xy(x,y);await p.mouse.click(a.x,a.y)};const drag=async(x1,y1,x2,y2)=>{const a=await xy(x1,y1),b=await xy(x2,y2);await p.mouse.move(a.x,a.y);await p.mouse.down();await p.mouse.move(b.x,b.y,{steps:12});await p.mouse.up();await p.waitForTimeout(80)};const layout=async t=>{await p.locator('#layoutMenuBtn').click();await p.locator(`[data-menu-tool="${t}"]`).click()};

// Corridor: one drag creates a grouped four-wall corridor plus its label.
await layout('corridor');await drag(.08,.12,.55,.28);let d=await saved();assert.equal(d.walls.length,4);assert.equal(d.labels.length,1);assert.equal(d.labels[0].text,'Corridor');const corridorGroup=d.labels[0].group;assert(corridorGroup&&d.walls.every(w=>w.group===corridorGroup));

// L-room: one drag creates six grouped wall sections.
await layout('layoutL');await drag(.62,.12,.92,.43);d=await saved();const lGroups=[...new Set(d.walls.map(w=>w.group).filter(g=>g&&g!==corridorGroup))];assert.equal(lGroups.length,1);assert.equal(d.walls.filter(w=>w.group===lGroups[0]).length,6);

// Split Wall turns one standalone section into two pieces.
await layout('wall');await drag(.10,.70,.42,.70);d=await saved();const beforeSplit=d.walls.length;await layout('splitWall');await click(.26,.70);d=await saved();assert.equal(d.walls.length,beforeSplit+1,'split wall should create one extra segment');

// Join Wall closes a visible gap between two standalone wall ends.
await layout('wall');await drag(.55,.70,.68,.70);await layout('wall');await drag(.76,.70,.90,.70);d=await saved();const beforeJoin=d.walls.length;await layout('joinWalls');await click(.68,.70);await click(.76,.70);d=await saved();assert.equal(d.walls.length,beforeJoin);const ends=d.walls.flatMap(w=>w.kind==='wall'?w.points:[]);const nearTarget=ends.filter(q=>Math.abs(q.x-.76)<.012&&Math.abs(q.y-.70)<.012);assert(nearTarget.length>=2,'joined wall ends should share the target point');

// Edit Wall Ends exposes draggable handles and moves an endpoint without redrawing the wall.
await layout('wallEnds');const a=await xy(.90,.70),b=await xy(.92,.78);await p.mouse.move(a.x,a.y);await p.mouse.down();await p.mouse.move(b.x,b.y,{steps:10});await p.mouse.up();d=await saved();const moved=d.walls.flatMap(w=>w.kind==='wall'?w.points:[]).some(q=>Math.abs(q.x-.92)<.02&&Math.abs(q.y-.78)<.02);assert(moved,'wall endpoint should move to the dragged location');

// New tools are available to favourites and remain usable on a phone-sized layout.
await p.setViewportSize({width:390,height:844});await p.locator('#layoutMenuBtn').click();for(const t of ['corridor','layoutL','wallEnds','joinWalls','splitWall'])assert.equal(await p.locator(`[data-menu-tool="${t}"]`).isVisible(),true);const box=await p.locator('#layoutMenu').boundingBox();assert(box&&box.x>=0&&box.y>=0&&box.x+box.width<=390&&box.y+box.height<=844);fs.mkdirSync('test-results',{recursive:true});await p.screenshot({path:'test-results/v026-drawing-tools-phone.png',fullPage:true});assert.deepEqual(errors,[]);console.log('PASS v0.26 drawing tools: corridor, L-room, split, join and wall-end editing');
}finally{await browser.close();server.close()}})().catch(e=>{console.error(e);process.exit(1)});
