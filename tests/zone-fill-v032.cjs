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
    p.on('dialog',d=>d.accept(d.type()==='prompt'?'Fill only test':undefined));
    await p.goto('http://127.0.0.1:'+server.address().port,{waitUntil:'load'});
    await p.locator('#homeNew').waitFor({state:'visible'});
    await p.waitForFunction(()=>!document.querySelector('#homeNew').disabled);
    await p.locator('#homeNew').click();
    await p.locator('#projectsHome').waitFor({state:'hidden'});

    // The shared zone renderer must not call stroke at all. This covers the live
    // canvas, Zone Box preview and exported plans because they all use shape().
    const strokeCount=await p.evaluate(()=>{
      const c=document.createElement('canvas');c.width=200;c.height=200;const x=c.getContext('2d');
      const proto=CanvasRenderingContext2D.prototype,orig=proto.stroke;let n=0;
      proto.stroke=function(...a){n++;return orig.apply(this,a)};
      try{shape(x,[{x:20,y:20},{x:180,y:20},{x:180,y:180},{x:20,y:180}],'#4a9f60',1,2,true)}finally{proto.stroke=orig}
      return n;
    });
    assert.equal(strokeCount,0,'Zone renderer must be fill-only with no perimeter stroke');

    // Create a zone and draw it so the normal app path is exercised too.
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

    // A selected single zone uses handles without another full selection box.
    const selectionSource=await p.evaluate(()=>drawSelection.toString());
    assert(selectionSource.includes("selection[0].type==='shapes'"),'single-zone selection should suppress the full selection rectangle');

    // Zone Outline preview should not use a coloured stroke either.
    const html=fs.readFileSync('index.html','utf8');
    assert(html.includes("if(tool==='poly'){const z=state.zones.find"),'fill-only polygon zone preview should be present');
    assert(!html.includes("ctx.strokeStyle=tool==='layoutPoly'?'#172333':(z?.color||'#ee3333')"),'old coloured zone outline preview must be removed');

    fs.mkdirSync('test-results',{recursive:true});
    await p.screenshot({path:'test-results/v032-fill-only-zones.png',fullPage:true});
    assert.deepEqual(errors,[],'No browser runtime errors');
    console.log('PASS v0.32: zones are translucent fill-only with no coloured perimeter stroke');
  }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
