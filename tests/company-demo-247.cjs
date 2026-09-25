const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict'),path=require('path');
(async()=>{
 const server=http.createServer((q,r)=>{let rel=decodeURIComponent((q.url||'/').split('?')[0]);if(rel.endsWith('/'))rel+='index.html';rel=rel.replace(/^\//,'');const file=path.join(process.cwd(),rel);try{const data=fs.readFileSync(file);if(file.endsWith('.js'))r.setHeader('Content-Type','text/javascript');else if(file.endsWith('.svg'))r.setHeader('Content-Type','image/svg+xml');else if(file.endsWith('.webmanifest'))r.setHeader('Content-Type','application/manifest+json');else r.setHeader('Content-Type','text/html');r.end(data)}catch(e){r.statusCode=404;r.end('not found')}}).listen(0,'127.0.0.1');
 await new Promise(r=>server.once('listening',r));const browser=await chromium.launch({headless:true});
 try{
  const file='company-demos/247-protection/index.html',html=fs.readFileSync(file,'utf8');
  assert.match(html,/24\/7 Protection · Zone Sketch Company Demo/);
  assert.match(html,/ZoneSketch-247Protection-v1/);
  assert(!html.includes("indexedDB.open('ZoneSketch-v1',1)"),'demo must not use original project database');
  assert.match(html,/24\/7 PROTECTION · .*ZONE PLAN/);
  assert.match(html,/24\/7 Protection · Generated from Zone Plan/);
  assert(fs.existsSync('company-demos/247-protection/logo.svg'));
  assert(fs.existsSync('company-demos/247-protection/manifest.webmanifest'));
  const p=await browser.newPage({viewport:{width:390,height:844}}),errors=[];p.on('pageerror',e=>errors.push(e.message));p.on('dialog',d=>d.accept(d.type()==='prompt'?'Company Demo Test':undefined));
  await p.goto('http://127.0.0.1:'+server.address().port+'/company-demos/247-protection/');
  assert.match(await p.title(),/24\/7 Protection/i);
  assert(await p.locator('.companyHeroBrand').isVisible());
  const logo=await p.locator('.companyBrandLogo').boundingBox();assert(logo&&logo.width<=80&&logo.height<=58,'header logo must stay compact');
  assert.match(await p.locator('.creatorLine').innerText(),/24\/7 Protection branded demo/i);
  await p.locator('#homeNew').click();await p.locator('#projectsHome').waitFor({state:'hidden'});
  assert(await p.locator('.companyBrandLogo').isVisible());
  const dbs=await p.evaluate(async()=>indexedDB.databases?await indexedDB.databases():[]);if(dbs.length)assert(dbs.some(d=>d.name==='ZoneSketch-247Protection-v1')&&!dbs.some(d=>d.name==='ZoneSketch-v1'));
  assert.deepEqual(errors,[],'No runtime errors in company demo');
  console.log('PASS: isolated 24/7 Protection duplicate loads, fits mobile and uses separate project storage');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
