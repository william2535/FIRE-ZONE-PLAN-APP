const {chromium}=require('playwright');
const fs=require('fs'),http=require('http'),assert=require('node:assert/strict');

(async()=>{
  let html=fs.readFileSync('index.html','utf8');
  const marker="document.querySelector('.app').inert=true;\nensureUiState();renderFloors();renderSymbolColors();syncSymbolScale();";
  assert(html.includes(marker),'late v0.42 test hook marker missing');
  const hook=`window.v042Test={
    read:()=>({state:JSON.parse(JSON.stringify(state)),zoom,imgW:img?.width||0,imgH:img?.height||0}),
    screen:p=>screenPoint(p),
    start:async()=>{state=fresh();state.site='v0.42 test';state.image=blankImage();state.isBlank=true;ensureUiState();ensureFloors();syncFloor();document.querySelector('#projectsHome').hidden=true;document.querySelector('.app').inert=false;await setImage(state.image,false);renderFloors();renderZones();syncGrid();syncWallSize();updateButtons();draw()}
  };\n`;
  html=html.replace(marker,hook+marker);

  const server=http.createServer((req,res)=>{
    const path=(req.url||'/').split('?')[0];
    if(path==='/'){res.setHeader('Content-Type','text/html');res.end(html);return}
    try{const data=fs.readFileSync(path.slice(1));res.setHeader('Content-Type',path.endsWith('.js')?'text/javascript':'application/octet-stream');res.end(data)}catch(e){res.statusCode=404;res.end('not found')}
  }).listen(0,'127.0.0.1');
  await new Promise(ok=>server.once('listening',ok));
  const browser=await chromium.launch({headless:true});
  try{
    const page=await browser.newPage({viewport:{width:1180,height:820}}),errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    await page.goto('http://127.0.0.1:'+server.address().port);
    await page.waitForFunction(()=>!!window.v042Test);
    await page.evaluate(()=>window.v042Test.start());
    await page.waitForTimeout(100);

    // The zoom slider must track a dragged pointer rather than acting like a
    // tap-only native control inside the touch-locked canvas wrapper.
    const slider=page.locator('#viewZoom'),sr=await slider.boundingBox();
    assert(sr&&sr.width>40);
    await page.evaluate(({x1,x2,y})=>{
      const el=document.querySelector('#viewZoom');
      const fire=(type,x)=>el.dispatchEvent(new PointerEvent(type,{pointerId:77,pointerType:'touch',clientX:x,clientY:y,bubbles:true,cancelable:true}));
      fire('pointerdown',x1);fire('pointermove',(x1+x2)/2);fire('pointermove',x2);fire('pointerup',x2);
    },{x1:sr.x+sr.width*.2,x2:sr.x+sr.width*.8,y:sr.y+sr.height/2});
    let read=await page.evaluate(()=>window.v042Test.read());
    assert(read.zoom>8,'finger drag should move zoom well beyond the start value');
    assert(Number(await slider.inputValue())>3.5,'slider thumb value should follow the finger');
    await page.locator('#viewFit').click();

    // Survey grid is exact and both beam endpoints should use it when snap is on.
    await page.locator('#surveyModeBtn').click();
    await page.locator('#canvasOptionsBtn').click();
    await page.locator('#surveyGridSize').selectOption('20');
    await page.locator('#surveyGridSize').dispatchEvent('change');
    await page.locator('#canvasOptionsBtn').click();
    read=await page.evaluate(()=>window.v042Test.read());
    if(!read.state.gridVisible)await page.locator('#surveyMove').click();
    read=await page.evaluate(()=>window.v042Test.read());
    if(!read.state.snapGrid)await page.locator('#surveySnap').click();

    await page.locator('#surveyDevice').click();
    await page.locator('[data-symbol="beam"]').click();
    const cb=await page.locator('#canvas').boundingBox();
    const sx=cb.x+cb.width*.30,sy=cb.y+cb.height*.34,tx=cb.x+cb.width*.57,ty=cb.y+cb.height*.43;
    await page.mouse.move(sx,sy);await page.mouse.down();await page.mouse.move(tx,ty,{steps:8});await page.mouse.up();
    await page.waitForTimeout(100);
    read=await page.evaluate(()=>window.v042Test.read());
    const beam=read.state.symbols.find(s=>s.type==='beam');
    assert(beam&&beam.beamEnd,'dragging Beam must create a directional endpoint');
    const multiple=(v,step)=>Math.abs(v/step-Math.round(v/step))<1e-7;
    assert(multiple(beam.x*read.imgW,20),'beam base must snap to visible grid');
    assert(multiple(beam.y*read.imgH,20),'beam base must snap to visible grid');
    assert(multiple(beam.beamEnd.x*read.imgW,20),'beam tip must snap to visible grid');
    assert(multiple(beam.beamEnd.y*read.imgH,20),'beam tip must snap to visible grid');
    assert(Math.hypot((beam.beamEnd.x-beam.x)*read.imgW,(beam.beamEnd.y-beam.y)*read.imgH)>100,'beam should stretch in the drag direction');

    // Ordinary detector duplication must land on a real grid intersection.
    await page.locator('#surveyDevice').click();
    await page.locator('[data-symbol="smoke"]').click();
    await page.mouse.click(cb.x+cb.width*.72,cb.y+cb.height*.66);
    await page.waitForTimeout(80);
    read=await page.evaluate(()=>window.v042Test.read());
    let smokes=read.state.symbols.filter(s=>s.type==='smoke');
    assert.equal(smokes.length,1);
    await page.locator('#surveySelect').click();
    const sp=await page.evaluate(s=>{const p=window.v042Test.screen(s),r=document.querySelector('#canvas').getBoundingClientRect();return{x:r.left+p.x,y:r.top+p.y}},smokes[0]);
    await page.mouse.click(sp.x,sp.y);
    await page.locator('#duplicateSelected').click();
    await page.waitForTimeout(80);
    read=await page.evaluate(()=>window.v042Test.read());
    smokes=read.state.symbols.filter(s=>s.type==='smoke');
    assert.equal(smokes.length,2);
    const copy=smokes[1];
    assert(multiple(copy.x*read.imgW,20),'duplicated detector x must be on grid');
    assert(multiple(copy.y*read.imgH,20),'duplicated detector y must be on grid');
    const dx=Math.round(Math.abs((smokes[1].x-smokes[0].x)*read.imgW));
    const dy=Math.round(Math.abs((smokes[1].y-smokes[0].y)*read.imgH));
    assert(dx%20===0&&dy%20===0&&(dx||dy),'duplicate offset must be an exact grid increment');

    fs.mkdirSync('test-results',{recursive:true});
    await page.screenshot({path:'test-results/v042-zoom-beam-grid-duplicate.png'});
    assert.deepEqual(errors,[]);
    console.log('PASS v0.42: finger zoom slider, stretched directional beam triangle and detector duplication on exact grid');
  }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
