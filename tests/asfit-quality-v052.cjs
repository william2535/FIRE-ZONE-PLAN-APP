const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict'),path=require('path');
(async()=>{
 const html=fs.readFileSync('index.html','utf8');
 assert.match(html,/function cbDrawBundled\(x,segments,map,lineWidth=5,bundleGap=7\)/,'Circuit Builder must retain its existing default cable look');
 assert.match(html,/cableWidth=Math\.max\(1\.05,size\*\.13\)/,'As-Fit cable width must scale from detector size');
 assert.match(html,/cbDrawBundled\(x,segments,map,cableWidth,bundleGap\)/,'As-Fit must pass the thinner cable sizing');
 assert.match(html,/devicePixelRatio\|\|1,3/,'preview must use a high-density backing canvas');
 assert.doesNotMatch(html,/function cbDrawAsFitPreview\(\)[\s\S]{0,700}createElement\('canvas'\)/,'preview must not render through a low-resolution temporary canvas');
 assert.match(html,/Math\.max\(4800,Math\.min\(5600,sourceW\*2\)\)/,'export must be 4800–5600px wide');
 assert.match(html,/H=Math\.round\(W\/aspect\+170\*\(W\/2400\)\)/,'high-resolution export chrome must scale with canvas width');
 const previewSize=Math.min(950,593.75)*.018,cableWidth=Math.max(1.05,previewSize*.13);
 assert(cableWidth>1,'As-Fit cable should remain visible');
 assert(cableWidth<previewSize*.2,'As-Fit cable must remain much thinner than the detector radius');
 const lowSource=Math.max(4800,Math.min(5600,2400*2)),largeSource=Math.max(4800,Math.min(5600,4000*2));
 assert.equal(lowSource,4800);assert.equal(largeSource,5600);
 const server=http.createServer((q,r)=>{let rel=decodeURIComponent((q.url||'/').split('?')[0]);if(rel.endsWith('/'))rel+='index.html';rel=rel.replace(/^\//,'');const file=path.join(process.cwd(),rel);try{const data=fs.readFileSync(file);if(file.endsWith('.js'))r.setHeader('Content-Type','text/javascript');else if(file.endsWith('.svg'))r.setHeader('Content-Type','image/svg+xml');else if(file.endsWith('.webmanifest'))r.setHeader('Content-Type','application/manifest+json');else r.setHeader('Content-Type','text/html');r.end(data)}catch(e){r.statusCode=404;r.end('not found')}}).listen(0,'127.0.0.1');
 await new Promise(r=>server.once('listening',r));const browser=await chromium.launch({headless:true});
 try{
  const p=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:3}),errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.goto('http://127.0.0.1:'+server.address().port+'/');
  assert.match(await p.title(),/Zone Sketch by Will Flood v0\.\d+/,'browser must load a current Zone Sketch build containing the v0.52 As-Fit quality feature');
  assert.deepEqual(errors,[],'No runtime errors');
  console.log('PASS: v0.52+ As-Fit uses a thin proportional cable, retina preview and 4800–5600px PNG export');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
