const fs=require('fs'),assert=require('node:assert/strict'),vm=require('node:vm');
const html=fs.readFileSync('index.html','utf8');
if(!/v0\.55/.test(html)){console.log('SKIP: v0.55 smooth-routing test only runs after the v0.55 patch');process.exit(0)}
assert.match(html,/v0\.55 smooth route engine/);
assert.match(html,/CB_ROUTE_TURN_CELLS=\.72/);
assert.match(html,/CB_ROUTE_ARM_CELLS=\.28/);
assert.match(html,/CB_ROUTE_SAMPLE_CELLS=\.30/);
assert.match(html,/turnAnchor:null,routeInput:sp/);

function fn(name,next){const re=new RegExp(`function ${name}\\([\\s\\S]*?(?=\\nfunction ${next})`),m=html.match(re);assert(m,`Could not extract ${name}`);return m[0]}
const source=[
 fn('cbCollinear','cbSimplify'),
 fn('cbSimplify','cbPointClose'),
 fn('cbPairSegmentsPx','cbRouteCellPx'),
 fn('cbRouteCellPx','cbRouteSnapshot'),
 fn('cbRouteSnapshot','cbRouteRestore'),
 fn('cbRouteRestore','cbPairSnapPx'),
 fn('cbPairSnapPx','cbRouteGridStep'),
 fn('cbRouteGridStep','cbAppendDrag')
].join('\n');
const ctx={console,Math,Number,CB_PAIR_RANGE:24,CB_PAIR_GAP:9,CB_ROUTE_GRID:24,CB_ROUTE_TURN_CELLS:.72,CB_ROUTE_ARM_CELLS:.28,CB_ROUTE_SAMPLE_CELLS:.30,cbView:{scale:1},cbCircuit:{type:'conventional',bounds:null,legs:[]},cbSelectBounds:null,cbDrag:null,cbBoardPx:p=>({...p}),cbFieldGridScreenStep:()=>({x:24,y:24})};
vm.createContext(ctx);vm.runInContext(source,ctx);
const clone=v=>JSON.parse(JSON.stringify(v));

// Minor finger wobble must not create bends. The horizontal cable should simply follow the
// active row while the raw pointer moves a few pixels above/below it.
ctx.cbDrag={points:[{x:100,y:100},{x:200,y:100}],routeAxis:'h',turnAnchor:null,routeInput:{x:200,y:100},pairSnap:false,pairAxis:null,pairLine:null,previewLegs:[]};
for(const p of [{x:224,y:104},{x:248,y:96},{x:272,y:105},{x:296,y:99}])ctx.cbRouteGridStep({x:p.x,y:100},400,300,p);
let pts=clone(ctx.cbDrag.points);assert.deepEqual(pts,[{x:100,y:100},{x:296,y:100}],'small wobble should remain one straight cable run');assert.equal(ctx.cbDrag.routeAxis,'h');

// Reproduce the field glitch: a sparse/diagonal corner event arrives far to the right while
// the engineer is actually turning down. The old code kept extending the horizontal leg toward
// that distant X before turning. v0.55 must freeze the corner at the last genuinely reached grid point.
ctx.cbDrag={points:[{x:100,y:200},{x:200,y:200}],routeAxis:'h',turnAnchor:null,routeInput:{x:200,y:200},pairSnap:false,pairAxis:null,pairLine:null,previewLegs:[]};
ctx.cbRouteGridStep({x:500,y:200},400,300,{x:500,y:208});
pts=clone(ctx.cbDrag.points);assert.deepEqual(pts,[{x:100,y:200},{x:200,y:200}],'once a turn is armed the old leg must freeze instead of shooting sideways');assert.deepEqual(clone(ctx.cbDrag.turnAnchor),{x:200,y:200});
ctx.cbRouteGridStep({x:500,y:224},400,300,{x:500,y:224});
pts=clone(ctx.cbDrag.points);assert.deepEqual(pts,[{x:100,y:200},{x:200,y:200},{x:200,y:224}],'confirmed corner must turn at the frozen grid point');assert.equal(ctx.cbDrag.routeAxis,'v');assert(Math.max(...pts.map(p=>p.x))<=200,'corner must never inherit the distant sparse-event X coordinate');

// If the engineer starts to turn but comes back onto the original row, the pending corner
// should cancel and drawing should continue naturally instead of leaving a stub.
ctx.cbDrag={points:[{x:100,y:260},{x:180,y:260}],routeAxis:'h',turnAnchor:null,routeInput:{x:180,y:260},pairSnap:false,pairAxis:null,pairLine:null,previewLegs:[]};
ctx.cbRouteGridStep({x:260,y:260},400,300,{x:260,y:268});assert(ctx.cbDrag.turnAnchor,'turn should arm during deliberate sideways movement');
ctx.cbRouteGridStep({x:280,y:260},400,300,{x:280,y:263});pts=clone(ctx.cbDrag.points);assert.equal(ctx.cbDrag.turnAnchor,null);assert.deepEqual(pts,[{x:100,y:260},{x:280,y:260}],'aborted turn must resume the original line with no phantom bend');

// Parallel retrace remains part of the smoother engine: return over the previous cable and it
// must form one clean offset lane with a short dogleg at the detector.
ctx.cbDrag={points:[{x:220,y:100}],routeAxis:null,turnAnchor:null,routeInput:{x:220,y:100},pairSide:null,pairSnap:false,pairAxis:null,pairLine:null,previewLegs:[{from:'panel',to:'d1',points:[{x:80,y:100},{x:220,y:100}]}]};
let q=ctx.cbPairSnapPx({x:180,y:100},ctx.cbDrag.points.at(-1),400,300,{x:180,y:100});assert.equal(ctx.cbDrag.pairSnap,true);assert.equal(ctx.cbDrag.pairAxis,'h');assert.equal(Math.round(q.y),109);
ctx.cbRouteGridStep(q,400,300,{x:180,y:100});pts=clone(ctx.cbDrag.points);assert.deepEqual(pts,[{x:220,y:100},{x:220,y:109},{x:180,y:109}]);
assert(pts.every((p,i)=>i===0||Math.abs(p.x-pts[i-1].x)<1e-9||Math.abs(p.y-pts[i-1].y)<1e-9),'all generated segments must remain orthogonal');

console.log('PASS: v0.55 smooth route engine suppresses wobble, freezes corners before sparse-event overshoot, cancels false turns and preserves parallel retrace');
