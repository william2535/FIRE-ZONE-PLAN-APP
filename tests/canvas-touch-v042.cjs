const {chromium}=require('playwright');
const fs=require('fs'),http=require('http'),assert=require('node:assert/strict');
(async()=>{
 let html=fs.readFileSync('index.html','utf8');
 const marker="document.querySelector('.app').inert=true;\nensureUiState();renderFloors();renderSymbolColors();syncSymbolScale();";
 assert(html.includes(marker),'late touch test hook marker missing');
 html=html.replace(marker,`window.touchStable={read:()=>({zoom,state:JSON.parse(JSON.stringify(state)),pan:{...pan}}),start:async()=>{state=fresh();state.site='Touch';state.image=blankImage();state.isBlank=true;ensureUiState();ensureFloors();syncFloor();document.querySelector('#projectsHome').hidden=true;document.querySelector('.app').inert=false;await setImage(state.image,false);renderFloors();renderZones();syncGrid();updateButtons();draw()}};\n`+marker);
 const server=http.createServer((req,res)=>{const path=(req.url||'/').split('?')[0];if(path==='/'){res.setHeader('Content-Type','text/html');res.end(html);return}try{res.end(fs.readFileSync(path.slice(1)))}catch(e){res.statusCode=404;res.end('not found')}}).listen(0,'127.0.0.1');
 await new Promise(ok=>server.once('listening',ok));
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1024,height:860}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>!!window.touchStable);await page.evaluate(()=>window.touchStable.start());await page.waitForTimeout(80);
  const pinch=async(scale=1.5,panX=0,panY=0)=>page.evaluate(({scale,panX,panY})=>{const c=document.querySelector('#canvas'),r=c.getBoundingClientRect(),mx=r.left+r.width/2,my=r.top+r.height/2,d=50,nd=d*scale;c.setPointerCapture=()=>{};const f=(t,id,x,y)=>c.dispatchEvent(new PointerEvent(t,{pointerId:id,pointerType:'touch',clientX:x,clientY:y,bubbles:true,cancelable:true}));f('pointerdown',11,mx-d,my);f('pointerdown',12,mx+d,my);f('pointermove',11,mx-nd+panX,my+panY);f('pointermove',12,mx+nd+panX,my+panY);f('pointerup',11,mx-nd+panX,my+panY);f('pointerup',12,mx+nd+panX,my+panY)},{scale,panX,panY});
  await page.locator('[data-tool="select"]').click();await pinch();let r=await page.evaluate(()=>window.touchStable.read());assert.equal(r.zoom,1,'Zone Plan Move OFF must block pinch navigation');
  await page.locator('#moveModeTop').click();await pinch();r=await page.evaluate(()=>window.touchStable.read());assert(r.zoom>1.4,'Zone Plan Move ON must allow pinch zoom');
  await page.locator('#moveModeTop').click();await page.locator('#viewFit').click();await page.locator('#surveyModeBtn').click();await page.waitForFunction(()=>document.querySelector('.app')?.classList.contains('surveyMode')&&document.querySelector('#surveyModeBtn')?.getAttribute('aria-pressed')==='true');
  await pinch(1.7,18,22);r=await page.evaluate(()=>window.touchStable.read());assert(r.zoom>1.6,'Survey mode must allow two-finger zoom without a move toggle');assert.equal(r.state.symbols.length,0,'two-finger Survey navigation must not stamp a detector');
  const cb=await page.locator('#canvas').boundingBox();await page.mouse.click(cb.x+cb.width*.53,cb.y+cb.height*.51);await page.waitForTimeout(70);r=await page.evaluate(()=>window.touchStable.read());assert.equal(r.state.symbols.length,1,'one finger/click in Survey mode places the selected device');
  assert.deepEqual(errors,[]);fs.mkdirSync('test-results',{recursive:true});await page.screenshot({path:'test-results/touch-navigation-v042.png'});console.log('PASS: Zone Plan move toggle and Survey one-finger place / two-finger move-zoom are isolated');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
