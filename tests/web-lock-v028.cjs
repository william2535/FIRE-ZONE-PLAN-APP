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
  try{
    const p=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
    const errors=[];p.on('pageerror',e=>errors.push(e.message));
    await p.goto('http://127.0.0.1:'+server.address().port,{waitUntil:'load'});
    await p.waitForTimeout(200);

    const styles=await p.evaluate(()=>{
      const html=getComputedStyle(document.documentElement),body=getComputedStyle(document.body),app=getComputedStyle(document.querySelector('.app')),canvas=getComputedStyle(document.querySelector('.canvasWrap'));
      return {htmlOverflow:html.overflow,bodyOverflow:body.overflow,bodyPosition:body.position,appHeight:document.querySelector('.app').getBoundingClientRect().height,canvasTouch:canvas.touchAction,innerHeight:innerHeight};
    });
    assert.equal(styles.htmlOverflow,'hidden');
    assert.equal(styles.bodyOverflow,'hidden');
    assert.equal(styles.bodyPosition,'fixed');
    assert(Math.abs(styles.appHeight-styles.innerHeight)<=2,`app should match dynamic viewport (${styles.appHeight} vs ${styles.innerHeight})`);
    assert.equal(styles.canvasTouch,'none');

    await p.evaluate(()=>window.scrollTo(0,200));
    await p.waitForTimeout(50);
    assert.equal(await p.evaluate(()=>window.scrollY),0,'main document must not scroll vertically');

    const touchCancelled=await p.locator('.canvasWrap').evaluate(el=>{
      const ev=new Event('touchmove',{bubbles:true,cancelable:true});
      return !el.dispatchEvent(ev) && ev.defaultPrevented;
    });
    assert.equal(touchCancelled,true,'canvas touchmove should be prevented from scrolling the page');

    const internal=await p.evaluate(()=>({popup:getComputedStyle(document.querySelector('.toolPopup')).overscrollBehavior,home:getComputedStyle(document.querySelector('#projectsHome')).overscrollBehavior}));
    assert(internal.popup.includes('contain'));
    assert(internal.home.includes('contain'));

    assert.deepEqual(errors,[],'No browser runtime errors');
    console.log('PASS v0.28: fixed dynamic viewport, no document scroll/rubber-band, canvas touch lock and contained internal scrolling');
  }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
