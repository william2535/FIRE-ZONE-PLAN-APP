const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict');
(async()=>{
 const server=http.createServer((q,r)=>{const path=(q.url||'/').split('?')[0],file=path==='/'?'index.html':path.slice(1);try{const data=fs.readFileSync(file);if(file.endsWith('.svg'))r.setHeader('Content-Type','image/svg+xml');else if(file.endsWith('.webmanifest'))r.setHeader('Content-Type','application/manifest+json');else r.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':'text/html');r.end(data)}catch(e){r.statusCode=404;r.end('not found')}}).listen(0,'127.0.0.1');
 await new Promise(r=>server.once('listening',r));const browser=await chromium.launch({headless:true});
 try{
  const base='http://127.0.0.1:'+server.address().port;
  const p=await browser.newPage({viewport:{width:390,height:844}}),errors=[];
  p.on('pageerror',e=>errors.push(e.message));
  p.on('dialog',d=>d.accept(d.type()==='prompt'?'Beta Portal Test':undefined));
  await p.goto(base+'/beta.html');
  assert.match(await p.title(),/Beta Tester Portal.*v0\.50.*Will Flood/i);
  assert.match(await p.locator('body').innerText(),/Designed & built by Will Flood/i);
  assert(await p.locator('a[href="./"]').isVisible());
  const release='https://github.com/william2535/FIRE-ZONE-PLAN-APP/releases/download/v0.50/Zone-Sketch-by-Will-v0.50.apk';
  assert.equal(await p.locator(`a[href="${release}"]`).count(),1);
  assert.equal(await p.locator('a[href="downloads/Zone-Sketch-by-Will-v0.50.apk"]').count(),1);
  assert.match(await p.locator('body').innerText(),/GitHub Release server/i);
  assert.equal(await p.locator('#feedback').count(),1);
  assert.equal(await p.locator('.brandPack img').count(),3);
  assert(fs.existsSync('assets/zone-sketch-by-will-flood-wordmark.svg'));
  assert(fs.existsSync('assets/zone-sketch-beta-tester-badge.svg'));
  assert(fs.existsSync('assets/zone-sketch-app-icon.svg'));
  assert(fs.existsSync('manifest.webmanifest'));
  await p.goto(base+'/');
  assert.match(await p.locator('.homeProductHero').innerText(),/Will Flood/i);
  assert.match(await p.locator('.brand').innerText(),/WILL FLOOD/i);
  await p.locator('#homeNew').click();
  await p.locator('#projectsHome').waitFor({state:'hidden'});
  await p.locator('#projectMenuBtn').click();
  assert(await p.locator('#betaPortalBtn').isVisible());
  await p.locator('#appSettingsBtn').click();
  assert.match(await p.locator('.settingsFooter').innerText(),/WILL FLOOD/i);
  assert.match(await p.locator('.settingsFooter').innerText(),/v0\.50/i);
  assert.deepEqual(errors,[],'No v0.50 portal/app branding runtime errors');
  console.log('PASS: v0.50 beta portal, reliable Android download, brand pack, PWA metadata and Will Flood attribution');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
