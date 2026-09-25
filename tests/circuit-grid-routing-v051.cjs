const {chromium}=require('playwright'),fs=require('fs'),http=require('http'),assert=require('node:assert/strict'),path=require('path');
(async()=>{
 const server=http.createServer((q,r)=>{let rel=decodeURIComponent((q.url||'/').split('?')[0]);if(rel.endsWith('/'))rel+='index.html';rel=rel.replace(/^\//,'');const file=path.join(process.cwd(),rel);try{const data=fs.readFileSync(file);if(file.endsWith('.js'))r.setHeader('Content-Type','text/javascript');else if(file.endsWith('.svg'))r.setHeader('Content-Type','image/svg+xml');else if(file.endsWith('.webmanifest'))r.setHeader('Content-Type','application/manifest+json');else r.setHeader('Content-Type','text/html');r.end(data)}catch(e){r.statusCode=404;r.end('not found')}}).listen(0,'127.0.0.1');
 await new Promise(r=>server.once('listening',r));const browser=await chromium.launch({headless:true});
 try{
  const p=await browser.newPage({viewport:{width:390,height:844}}),errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.goto('http://127.0.0.1:'+server.address().port+'/');
  const result=await p.evaluate(()=>{
   cbView={scale:1,panX:0,panY:0};cbCircuit={type:'conventional'};
   cbDrag={points:[{x:100,y:100}],routeAxis:null,pairSnap:false};
   cbRouteGridStep({x:124,y:100},390,500);
   cbRouteGridStep({x:148,y:112},390,500);
   cbRouteGridStep({x:172,y:118},390,500);
   const straight={points:cbDrag.points.map(q=>({...q})),axis:cbDrag.routeAxis};
   cbRouteGridStep({x:172,y:148},390,500);
   const turned={points:cbDrag.points.map(q=>({...q})),axis:cbDrag.routeAxis};
   cbRouteGridStep({x:184,y:172},390,500);
   const verticalJitter={points:cbDrag.points.map(q=>({...q})),axis:cbDrag.routeAxis};
   return {straight,turned,verticalJitter,grid:CB_ROUTE_GRID,turnCells:CB_ROUTE_TURN_CELLS,appendSource:cbAppendDrag.toString(),gridSource:cbDrawRouteGrid.toString()};
  });
  assert.equal(result.grid,24);
  assert.equal(result.turnCells,1.45);
  assert.equal(result.straight.axis,'h');
  assert.equal(result.straight.points.length,2,'minor finger wobble must stay on one straight grid segment');
  assert.equal(result.straight.points[1].y,100);
  assert.equal(result.turned.axis,'v');
  assert.equal(result.turned.points.length,3,'an intentional cross-grid move should add one clean corner');
  assert.equal(result.turned.points[1].y,100);
  assert.equal(result.turned.points[1].x,result.turned.points[2].x,'turn must stay orthogonal');
  assert.equal(result.verticalJitter.axis,'v');
  assert.equal(result.verticalJitter.points.length,3,'small sideways wobble on a vertical run must not add another bend');
  assert.match(result.appendSource,/cbSnapPx/,'drag input must snap to grid');
  assert.match(result.appendSource,/cbRouteGridStep/,'snapped drag must use clean grid routing');
  assert.match(result.gridSource,/CB_ROUTE_GRID/,'visible Circuit Builder grid must use the same route grid');
  assert.deepEqual(errors,[],'No runtime errors');
  console.log('PASS: v0.51 Circuit Builder keeps finger wobble straight and turns only on deliberate grid movement');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
