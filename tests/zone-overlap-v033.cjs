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
    p.on('dialog',d=>d.accept(d.type()==='prompt'?'Overlap opacity test':undefined));
    await p.goto('http://127.0.0.1:'+server.address().port,{waitUntil:'load'});
    await p.locator('#homeNew').waitFor({state:'visible'});
    await p.waitForFunction(()=>!document.querySelector('#homeNew').disabled);
    await p.locator('#homeNew').click();
    await p.locator('#projectsHome').waitFor({state:'hidden'});

    await p.locator('#zoneMenuBtn').click();
    await p.locator('#zoneCreate').click();
    await p.locator('#zoneName').fill('Overlap test');
    await p.locator('#saveZone').click();
    await p.locator('#zoneMenuBtn').click();
    await p.locator('[data-menu-tool="rect"]').click();

    const pos=async(x,y)=>p.locator('#canvas').evaluate((c,{x,y})=>{
      const b=c.getBoundingClientRect(),s=Math.min((b.width-48)/3200,(b.height-48)/2000);
      return{x:b.x+b.width/2+(x-.5)*3200*s,y:b.y+b.height/2+(y-.5)*2000*s};
    },{x,y});
    const drag=async(a,b)=>{const A=await pos(...a),B=await pos(...b);await p.mouse.move(A.x,A.y);await p.mouse.down();await p.mouse.move(B.x,B.y,{steps:8});await p.mouse.up();await p.waitForTimeout(90)};

    await drag([.20,.24],[.56,.62]);
    await drag([.40,.24],[.76,.62]);
    await drag([.46,.30],[.64,.56]);
    await p.waitForTimeout(180);

    const pixels=await p.locator('#canvas').evaluate((c)=>{
      const b=c.getBoundingClientRect(),sx=c.width/b.width,sy=c.height/b.height;
      const sample=(x,y)=>{
        const s=Math.min((b.width-48)/3200,(b.height-48)/2000),cx=b.width/2+(x-.5)*3200*s,cy=b.height/2+(y-.5)*2000*s;
        return Array.from(c.getContext('2d').getImageData(Math.round(cx*sx),Math.round(cy*sy),1,1).data);
      };
      return{single:sample(.28,.40),triple:sample(.50,.40)};
    });
    const delta=pixels.single.slice(0,3).map((v,i)=>Math.abs(v-pixels.triple[i]));
    assert(Math.max(...delta)<=2,`overlap darkened: single=${pixels.single} triple=${pixels.triple}`);

    const html=fs.readFileSync('index.html','utf8');
    assert(html.includes('function drawZoneLayer('),'constant-opacity zone layer renderer should exist');
    assert(html.includes('drawZoneLayer(ctx,zonePaint,state.zones,map,.14)'),'live canvas should use the combined zone layer');
    assert(html.includes('drawZoneLayer(x,d.shapes,d.zones,map,.14)'),'export should use the same combined zone layer');
    assert(!html.includes('for(const sh of d.shapes){const z=d.zones.find'),'old per-shape export alpha stacking must be removed');

    fs.mkdirSync('test-results',{recursive:true});
    await p.screenshot({path:'test-results/v033-zone-overlap-constant-opacity.png',fullPage:true});
    assert.deepEqual(errors,[],'No browser runtime errors');
    console.log('PASS v0.33: single, double and triple overlapping zones keep the same shade');
  }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
