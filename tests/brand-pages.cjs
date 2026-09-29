const {chromium,webkit}=require('playwright');
const fs=require('fs'),http=require('http'),assert=require('node:assert/strict');
const {openHeader}=require('./header-navigation.cjs');
(async()=>{
 const server=http.createServer((q,r)=>{const f=q.url.split('?')[0]==='/'?'index.html':q.url.split('?')[0].slice(1);try{const ext=f.split('.').pop();r.setHeader('Content-Type',({js:'text/javascript',svg:'image/svg+xml',png:'image/png',webp:'image/webp',json:'application/json'})[ext]||'text/html');r.end(fs.readFileSync(f))}catch{r.statusCode=404;r.end()}}).listen(0,'127.0.0.1');await new Promise(r=>server.once('listening',r));
 const browser=await (process.env.PINEAPPLE_BROWSER==='webkit'?webkit:chromium).launch({headless:true});const errors=[];
 const motion=async(p,selector,pseudo,name)=>{await p.waitForFunction(({selector,pseudo,name})=>{const el=document.querySelector(selector);if(!el)return false;const s=getComputedStyle(el,pseudo);return s.animationName===name&&parseFloat(s.animationDuration)>1&&s.animationIterationCount==='infinite'&&s.animationPlayState==='running'},{selector,pseudo,name});};
 try{for(const width of [320,390,768,1440]){
  const p=await browser.newPage({viewport:{width,height:width===1440?1000:844},reducedMotion:'reduce'});p.on('pageerror',e=>errors.push(e.message));p.on('dialog',d=>d.accept(d.type()==='prompt'?'Riverside School':undefined));const base='http://127.0.0.1:'+server.address().port;
  await p.goto(base);await p.waitForFunction(()=>!document.querySelector('#homeNew').disabled);await p.locator('#zsSplash').waitFor({state:'hidden'});assert.equal(await p.locator('#projectsHome [data-brand-motion]').count(),0);assert.equal(await p.locator('.homeBrandMark').count(),0,'Respect the Home-only logo removal');
  await motion(p,'.workflowStep','::before','zsBrandFlow');await p.screenshot({path:`test-results/brand-home-empty-${width}.png`});
  await p.locator('#homeNew').click();await p.locator('#newProjectName').fill('Riverside School');await p.locator('#newProjectCreate').click();await p.locator('#projectsHome').waitFor({state:'hidden'});await openHeader(p);
  await p.waitForFunction(()=>document.querySelector('#headerHomeBtn img').naturalWidth>0);await motion(p,'.zsHeaderHomeShine','::before','zsHeaderGlossV2');await motion(p,'#favouriteMenuBtn',null,'zsFavouriteShine');
  await p.screenshot({path:`test-results/brand-workspace-${width}.png`});
  if(width===390){
   await p.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))});assert.equal(await p.locator('.zsHeaderHomeShine').evaluate(el=>getComputedStyle(el,'::before').animationPlayState),'paused');
   await p.evaluate(()=>{delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))});await motion(p,'.zsHeaderHomeShine','::before','zsHeaderGlossV2');
   await p.locator('#surveyModeBtn').click();await p.screenshot({path:'test-results/brand-survey-390.png'});await p.locator('#surveyModeBtn').click();await openHeader(p);
   await p.locator('#circuitModeBtn').click();await motion(p,'.cbLandingHero','::after','zsWorkspaceSignal');await p.screenshot({path:'test-results/brand-circuits-390.png'});await p.locator('#cbBack').click();
  }
  await p.locator('#projectMenuBtn').click();await p.screenshot({path:`test-results/brand-menu-${width}.png`});await p.locator('#homeBtn').click();await p.locator('.projectCard').waitFor();
  assert(await p.evaluate(()=>{const e=document.querySelector('#projectsHome');return e.scrollWidth<=e.clientWidth}));await p.screenshot({path:`test-results/brand-home-${width}.png`});await p.locator('.projectCard').screenshot({path:`test-results/brand-card-${width}.png`});
  await p.locator('#projectSearch').fill('missing');await p.waitForFunction(()=>!document.querySelector('.projectCard'));await p.locator('#projectSearch').fill('Riverside');await p.locator('.projectCard').waitFor();
  await p.goto(base+'/beta.html');await p.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth));await motion(p,'.brandSweep',null,'zsBrandSweep');assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await p.screenshot({path:`test-results/brand-tester-${width}.png`,fullPage:true});
  if(width===390){const toggle=p.locator('[data-brand-motion]');await toggle.click();assert.equal(await toggle.getAttribute('aria-pressed'),'false');assert.equal(await p.locator('.brandSweep').evaluate(el=>getComputedStyle(el).animationName),'none');await p.reload();await p.waitForFunction(()=>document.body.classList.contains('zsMotionOff'));await toggle.click();await motion(p,'.brandSweep',null,'zsBrandSweep');}
  await p.locator('#notes').fill('Project branding test');const report=await p.evaluate(()=>report());assert(report.includes('\nDevice:')&&report.includes('\nFeedback:\nProject branding test'));await p.evaluate(()=>Object.defineProperty(navigator,'clipboard',{value:{writeText:async text=>window.copied=text},configurable:true}));await p.locator('#copyReport').click();assert((await p.evaluate(()=>window.copied)).includes('Project branding test'));await p.close();console.log('PASS app/portal artwork, forced decorative motion, lifecycle, feedback and layout at '+width);
 }assert.deepEqual(errors,[])}finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
