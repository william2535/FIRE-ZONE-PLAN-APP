const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict'),path=require('path');
(async()=>{
 const server=http.createServer((q,r)=>{let rel=decodeURIComponent((q.url||'/').split('?')[0]);if(rel.endsWith('/'))rel+='index.html';rel=rel.replace(/^\//,'');const file=path.join(process.cwd(),rel);try{const data=fs.readFileSync(file);if(file.endsWith('.js'))r.setHeader('Content-Type','text/javascript');else if(file.endsWith('.svg'))r.setHeader('Content-Type','image/svg+xml');else if(file.endsWith('.webmanifest'))r.setHeader('Content-Type','application/manifest+json');else r.setHeader('Content-Type','text/html');r.end(data)}catch(e){r.statusCode=404;r.end('not found')}}).listen(0,'127.0.0.1');
 await new Promise(r=>server.once('listening',r));const browser=await chromium.launch({headless:true});
 try{
  const p=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:3}),errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.goto('http://127.0.0.1:'+server.address().port+'/');
  const result=await p.evaluate(async()=>{
   const bundleSource=cbDrawBundled.toString(),drawSource=cbDrawAsFitOn.toString(),previewSource=cbDrawAsFitPreview.toString(),exportSource=cbExportAsFit.toString();
   const originalBundle=cbDrawBundled,originalShare=shareCanvas,originalImg=img;let cable=null,lo=null,hi=null;
   try{
    cbDrawBundled=(ctx,segments,map,lineWidth,bundleGap)=>{cable={lineWidth,bundleGap}};
    const sample=document.createElement('canvas');sample.width=1000;sample.height=700;cbDrawAsFitOn(sample,1000,700,false);
    cbDrawBundled=originalBundle;
    shareCanvas=async c=>{if(!lo)lo={w:c.width,h:c.height};else hi={w:c.width,h:c.height}};
    img=null;await cbExportAsFit();
    img={width:4000,height:2000};await cbExportAsFit();
   }finally{cbDrawBundled=originalBundle;shareCanvas=originalShare;img=originalImg}
   return {bundleSource,drawSource,previewSource,exportSource,cable,lo,hi};
  });
  assert.match(result.bundleSource,/lineWidth=5,bundleGap=7/,'Circuit Builder must retain its existing default cable look');
  assert.match(result.drawSource,/size\*\.13/,'As-Fit cable width must scale from detector size');
  assert.match(result.drawSource,/cbDrawBundled\(x,segments,map,cableWidth,bundleGap\)/,'As-Fit must pass the thinner cable sizing');
  assert(result.cable.lineWidth>1,'As-Fit cable should remain visible');
  assert(result.cable.lineWidth<3,'1000px preview cable should be much thinner than a detector');
  assert.match(result.previewSource,/devicePixelRatio\|\|1,3/,'preview must use a high-density backing canvas');
  assert.doesNotMatch(result.previewSource,/createElement\('canvas'\)/,'preview must not render through a low-resolution temporary canvas');
  assert.equal(result.lo.w,4800,'low-resolution source must still export at 4800px wide');
  assert.equal(result.hi.w,5600,'large source must export at the safe 5600px cap');
  assert.match(result.exportSource,/sourceW\*2/,'export should target about twice the imported-plan width');
  assert.deepEqual(errors,[],'No runtime errors');
  console.log('PASS: v0.52 As-Fit uses a thin proportional cable, retina preview and 4800–5600px PNG export');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
