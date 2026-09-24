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
    const html=fs.readFileSync('index.html','utf8');
    const shapeSource=html.match(/function shape\(c,pts,color,num,line=1\.4,fill=true\)\{.*?\}/)?.[0]||'';
    assert(shapeSource,'zone shape renderer should exist');
    assert(!shapeSource.includes('.stroke(')&&!shapeSource.includes('.stroke()'),'Zone renderer must be fill-only with no perimeter stroke');
    assert(html.includes("selection[0].type==='shapes'"),'single-zone selection should suppress the full selection rectangle');
    assert(html.includes("if(tool==='poly'){const z=state.zones.find"),'fill-only polygon zone preview should be present');
    assert(!html.includes("ctx.strokeStyle=tool==='layoutPoly'?'#172333':(z?.color||'#ee3333')"),'old coloured zone outline preview must be removed');

    const p=await browser.newPage({viewport:{width:1180,height:900}});
    p.on('pageerror',e=>errors.push(e.message));
    p.on('dialog',d=>d.accept(d.type()==='prompt'?'Fill only test':undefined));
    await p.goto('http://127.0.0.1:'+server.address().port,{waitUntil:'load'});
    await p.locator('#homeNew').waitFor({state:'visible'});
    await p.waitForFunction(()=>!document.querySelector('#homeNew').disabled);
    await p.locator('#homeNew').click();
    await p.locator('#projectsHome').waitFor({state:'hidden'});

    // Create a zone and draw it so the normal app rendering path is exercised.
    await p.locator('#zoneMenuBtn').click();
    await p.locator('#zoneCreate').click();
    await p.locator('#zoneName').fill('Green zone');
    await p.locator('#saveZone').click();
    await p.locator('#zoneMenuBtn').click();
    await p.locator('[data-menu-tool="rect"]').click();
    const xy=async(x,y)=>p.locator('#canvas').evaluate((c,{x,y})=>{const b=c.getBoundingClientRect(),s=Math.min((b.width-48)/3200,(b.height-48)/2000);return{x:b.x+b.width/2+(x-.5)*3200*s,y:b.y+b.height/2+(y-.5)*2000*s}},{x,y});
    const a=await xy(.24,.24),b=await xy(.66,.66);await p.mouse.move(a.x,a.y);await p.mouse.down();await p.mouse.move(b.x,b.y,{steps:10});await p.mouse.up();await p.waitForTimeout(180);

    // The sidebar restored in v0.31 must stay present.
    const side=await p.locator('#zoneSide').boundingBox();
    assert(side&&side.width>180,'Zones sidebar should remain visible');
    assert.equal(await p.locator('#zones .zone').first().isVisible(),true,'created zone should remain visible in sidebar');

    fs.mkdirSync('test-results',{recursive:true});
    await p.screenshot({path:'test-results/v032-fill-only-zones.png',fullPage:true});
    assert.deepEqual(errors,[],'No browser runtime errors');
    console.log('PASS v0.32: zones are translucent fill-only with no coloured perimeter stroke');
  }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
