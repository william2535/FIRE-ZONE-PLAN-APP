const {chromium,webkit}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');

(async()=>{
  const server=http.createServer((q,r)=>{
    const p=(q.url||'/').split('?')[0],file=p==='/'?'index.html':p.slice(1);
    try{const data=fs.readFileSync(file);r.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':'text/html');r.end(data)}
    catch(e){r.statusCode=404;r.end('not found')}
  }).listen(0,'127.0.0.1');
  await new Promise(r=>server.once('listening',r));
  const engine=process.env.PINEAPPLE_BROWSER==='webkit'?webkit:chromium;
  const browser=await engine.launch({headless:true});
  try{
    const page=await browser.newPage({viewport:{width:375,height:812}}),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('dialog',d=>d.accept());
    await page.goto('http://127.0.0.1:'+server.address().port,{waitUntil:'load'});

    // Fresh launches intentionally place Projects + branded motion/splash layers over the editor.
    // Remove only those shells so this focused regression can exercise the editor header itself.
    await page.evaluate(()=>{
      const home=document.querySelector('#projectsHome');
      if(home){home.hidden=true;home.style.display='none';home.style.pointerEvents='none'}
      const splash=document.querySelector('#zsSplash');
      if(splash){splash.hidden=true;splash.style.display='none';splash.style.pointerEvents='none'}
      document.body.classList.remove('zsMotionActive');
    });
    await page.locator('#topCollapseBtn').waitFor({state:'visible'});

    const toggle=page.locator('#topCollapseBtn'),top=page.locator('#topBar'),floor=page.locator('#floorBar');
    assert.equal((await toggle.innerText()).trim(),'Menu ▼','collapsed phone header should expose a clearly labelled Menu button');
    assert.equal(await toggle.getAttribute('aria-expanded'),'false');
    let box=await toggle.boundingBox();
    assert(box&&box.width>=84&&box.height>=44,`collapsed Menu target must remain easy to tap; got ${box&&box.width}x${box&&box.height}`);

    await toggle.click({force:true});
    assert.equal((await toggle.innerText()).trim(),'Close ▲','expanded phone header should expose an obvious Close button');
    assert.equal(await toggle.getAttribute('aria-expanded'),'true');
    assert.equal(await top.evaluate(el=>el.classList.contains('collapsed')),false);
    assert.equal(await floor.evaluate(el=>getComputedStyle(el).display==='none'),false,'floor controls should be visible while menu is open');
    box=await toggle.boundingBox();
    assert(box&&box.width>=84&&box.height>=44,`expanded Close target must remain easy to tap; got ${box&&box.width}x${box&&box.height}`);
    const rowFits=await page.locator('#topEssential').evaluate(el=>el.scrollWidth<=el.clientWidth+1);
    assert.equal(rowFits,true,'iPhone utility row must fit without clipping the Close button');

    await toggle.click({force:true});
    assert.equal((await toggle.innerText()).trim(),'Menu ▼');
    assert.equal(await toggle.getAttribute('aria-expanded'),'false');
    assert.equal(await top.evaluate(el=>el.classList.contains('collapsed')),true);
    assert.equal(await page.locator('.app').evaluate(el=>el.classList.contains('topClosed')),true);
    assert.equal(await floor.evaluate(el=>getComputedStyle(el).display==='none'),true,'closing the menu should hide the floor controls');

    fs.mkdirSync('test-results',{recursive:true});
    await page.screenshot({path:`test-results/iphone-top-menu-v062-${process.env.PINEAPPLE_BROWSER||'chromium'}.png`,fullPage:true});
    assert.deepEqual(errors,[]);
    console.log(`PASS (${process.env.PINEAPPLE_BROWSER||'chromium'}): iPhone header has a full-size Menu/Close control and closes cleanly`);
  }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
