const {chromium}=require('playwright');
const fs=require('fs'),http=require('http'),path=require('path'),assert=require('node:assert/strict');

(async()=>{
  const root=process.cwd();
  const server=http.createServer((req,res)=>{
    const u=(req.url||'/').split('?')[0];
    const rel=u==='/'?'index.html':decodeURIComponent(u.slice(1));
    const file=path.join(root,rel);
    if(!file.startsWith(root)){res.statusCode=403;return res.end('forbidden')}
    try{
      const data=fs.readFileSync(file);
      if(file.endsWith('.js'))res.setHeader('Content-Type','text/javascript');
      else if(file.endsWith('.css'))res.setHeader('Content-Type','text/css');
      else res.setHeader('Content-Type','text/html');
      res.end(data);
    }catch(e){res.statusCode=404;res.end('not found')}
  }).listen(0,'127.0.0.1');
  await new Promise(ok=>server.once('listening',ok));
  const browser=await chromium.launch({headless:true});
  const url='http://127.0.0.1:'+server.address().port;
  const errors=[];

  async function setup(viewport,isMobile=false){
    const p=await browser.newPage({viewport,isMobile,hasTouch:isMobile});
    p.on('pageerror',e=>errors.push(e.message));
    await p.goto(url,{waitUntil:'load'});
    await p.waitForTimeout(150);
    await p.evaluate(()=>{
      document.querySelector('#projectsHome').hidden=true;
      const zones=document.querySelector('#zones');
      zones.textContent='';
      for(let i=1;i<=3;i++){
        const b=document.createElement('button');
        b.className='zone'+(i===1?' active':'');
        const sw=document.createElement('i');sw.className='swatch';sw.style.background='#ef4444';
        const txt=document.createElement('span');txt.className='label';
        const strong=document.createElement('b');strong.textContent='Zone '+i;
        const small=document.createElement('small');small.textContent='Test area';
        txt.append(strong,small);
        const edit=document.createElement('span');edit.className='edit';edit.textContent='✎';
        b.append(sw,txt,edit);zones.append(b);
      }
    });
    await p.waitForTimeout(50);
    return p;
  }

  try{
    fs.mkdirSync('test-results',{recursive:true});

    const desktop=await setup({width:1080,height:620});
    const d=await desktop.evaluate(()=>{
      const side=document.querySelector('#zoneSide').getBoundingClientRect();
      const zone=document.querySelector('#zones .zone').getBoundingClientRect();
      const list=document.querySelector('#zones').getBoundingClientRect();
      return {side:{top:side.top,bottom:side.bottom,height:side.height},zone:{top:zone.top,bottom:zone.bottom,height:zone.height},list:{top:list.top,bottom:list.bottom,height:list.height},help:getComputedStyle(document.querySelector('#zoneSide .help')).display};
    });
    assert(d.zone.height>=48,`desktop zone card should keep usable height, got ${d.zone.height}`);
    assert(d.zone.top>=d.side.top-1 && d.zone.bottom<=d.side.bottom+1,`desktop zone card must be fully visible inside side panel: ${JSON.stringify(d)}`);
    assert(d.list.height>=58,`desktop zone list should reserve visible space, got ${d.list.height}`);
    assert.equal(d.help,'none','short desktop viewport should prioritise zone cards over help copy');
    await desktop.screenshot({path:'test-results/zones-v029-desktop.png',fullPage:true});
    await desktop.close();

    const mobile=await setup({width:390,height:844},true);
    const m=await mobile.evaluate(()=>{
      const side=document.querySelector('#zoneSide').getBoundingClientRect();
      const zone=document.querySelector('#zones .zone').getBoundingClientRect();
      const list=document.querySelector('#zones');
      const lr=list.getBoundingClientRect();
      return {side:{top:side.top,bottom:side.bottom,height:side.height},zone:{top:zone.top,bottom:zone.bottom,height:zone.height},list:{top:lr.top,bottom:lr.bottom,height:lr.height,clientWidth:list.clientWidth,scrollWidth:list.scrollWidth}};
    });
    assert(m.side.height>=115,`mobile zone panel should have enough height, got ${m.side.height}`);
    assert(m.zone.height>=50,`mobile zone card should keep usable height, got ${m.zone.height}`);
    assert(m.zone.top>=m.side.top-1 && m.zone.bottom<=m.side.bottom+1,`mobile zone card must be fully visible: ${JSON.stringify(m)}`);
    assert(m.list.scrollWidth>m.list.clientWidth,'multiple mobile zones should scroll horizontally rather than clip vertically');
    await mobile.screenshot({path:'test-results/zones-v029-mobile.png',fullPage:true});
    await mobile.close();

    const short=await setup({width:390,height:500},true);
    const s=await short.evaluate(()=>{
      const side=document.querySelector('#zoneSide').getBoundingClientRect();
      const zone=document.querySelector('#zones .zone').getBoundingClientRect();
      return {side:{top:side.top,bottom:side.bottom,height:side.height},zone:{top:zone.top,bottom:zone.bottom,height:zone.height}};
    });
    assert(s.side.height>=94,`short mobile zone panel should remain visible, got ${s.side.height}`);
    assert(s.zone.top>=s.side.top-1 && s.zone.bottom<=s.side.bottom+1,`short mobile zone card must be fully visible: ${JSON.stringify(s)}`);
    await short.screenshot({path:'test-results/zones-v029-short-mobile.png',fullPage:true});
    await short.close();

    assert.deepEqual(errors,[],'No browser runtime errors');
    console.log('PASS v0.29: zone cards remain fully visible on short desktop, phone and short-phone viewports');
  }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
