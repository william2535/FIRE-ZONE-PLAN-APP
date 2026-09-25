const fs=require('fs'),assert=require('node:assert/strict'),vm=require('node:vm');
const html=fs.readFileSync('index.html','utf8');
assert.match(html,/v0\.53 parallel retrace/);
assert.match(html,/if\(!captured\)cbAppendDrag\(p,w,h\)/,'detector capture must discard the sparse touch tail');
assert.match(html,/pairMode=cbScreen==='game'&&!!cbCircuit/,'parallel-cable feedback must be available on conventional circuits too');

function fn(name,next){const re=new RegExp(`function ${name}\\([\\s\\S]*?(?=\\nfunction ${next})`),m=html.match(re);assert(m,`Could not extract ${name}`);return m[0]}
const smooth=/v0\.55 smooth route engine/.test(html);
const source=smooth?[
 fn('cbCollinear','cbSimplify'),fn('cbSimplify','cbPointClose'),fn('cbPairSegmentsPx','cbRouteCellPx'),fn('cbRouteCellPx','cbRouteSnapshot'),fn('cbRouteSnapshot','cbRouteRestore'),fn('cbRouteRestore','cbPairSnapPx'),fn('cbPairSnapPx','cbRouteGridStep'),fn('cbRouteGridStep','cbAppendDrag')
].join('\n'):[
 fn('cbCollinear','cbSimplify'),fn('cbSimplify','cbPairSegmentsPx'),fn('cbPairSegmentsPx','cbPairSnapPx'),fn('cbPairSnapPx','cbRouteGridStep'),fn('cbRouteGridStep','cbAppendDrag')
].join('\n');

const ctx={console,Math,Number,CB_PAIR_RANGE:24,CB_PAIR_GAP:9,CB_ROUTE_GRID:24,CB_ROUTE_TURN_CELLS:smooth?.72:1.45,CB_ROUTE_ARM_CELLS:.28,CB_ROUTE_SAMPLE_CELLS:.30,cbView:{scale:1},cbCircuit:{type:'conventional',bounds:null,legs:[]},cbDrag:null,cbBoardPx:p=>({...p}),cbSelectBounds:null,cbFieldGridScreenStep:()=>({x:24,y:24})};
vm.createContext(ctx);vm.runInContext(source,ctx);

// Simulate the exact field case: a completed horizontal leg ends at a detector, then the
// engineer keeps holding and runs backwards over the same physical route.
ctx.cbDrag={points:[{x:220,y:100}],routeAxis:null,turnAnchor:null,routeInput:{x:220,y:100},pairSide:null,pairSnap:false,pairAxis:null,pairLine:null,previewLegs:[{from:'panel',to:'d1',points:[{x:80,y:100},{x:220,y:100}]}]};
let q=ctx.cbPairSnapPx({x:180,y:100},ctx.cbDrag.points.at(-1),400,300,{x:180,y:100});
assert.equal(ctx.cbDrag.pairSnap,true,'retrace should be recognised as an existing cable run');assert.equal(ctx.cbDrag.pairAxis,'h');assert.equal(Math.round(q.y),109,'same-line retrace should move onto a parallel lane');
ctx.cbRouteGridStep(q,400,300,{x:180,y:100});
assert.deepEqual(JSON.parse(JSON.stringify(ctx.cbDrag.points)),[{x:220,y:100},{x:220,y:109},{x:180,y:109}],'retrace should dogleg once at the detector and continue as a clean parallel line');
ctx.cbDrag.routeInput={x:180,y:100};
q=ctx.cbPairSnapPx({x:130,y:100},ctx.cbDrag.points.at(-1),400,300,{x:130,y:100});ctx.cbRouteGridStep(q,400,300,{x:130,y:100});
const pts=JSON.parse(JSON.stringify(ctx.cbDrag.points));assert.equal(Math.round(pts.at(-1).y),109,'paired return must stay on the offset lane instead of collapsing back onto the first cable');assert.equal(pts.at(-1).x,130);assert(pts.every((p,i)=>i===0||Math.abs(p.x-pts[i-1].x)<1e-9||Math.abs(p.y-pts[i-1].y)<1e-9),'paired route must remain orthogonal');

// Sparse corner events must never extend the old leg toward a distant touch sample before
// turning. Both the v0.53 engine and the smoother v0.55 engine must turn at the last reached point.
ctx.cbDrag={points:[{x:100,y:200},{x:200,y:200}],routeAxis:'h',turnAnchor:null,routeInput:{x:200,y:200},pairSnap:false,pairAxis:null,pairLine:null,previewLegs:[]};
ctx.cbRouteGridStep({x:340,y:260},400,300,{x:340,y:260});
const corner=JSON.parse(JSON.stringify(ctx.cbDrag.points));assert.deepEqual(corner,[{x:100,y:200},{x:200,y:200},{x:200,y:260}],'corner must turn at the last reached grid point, not shoot the old leg out to a distant touch sample');assert.equal(ctx.cbDrag.routeAxis,'v');
console.log('PASS: retracing creates a true parallel cable lane and sparse corner events cannot create long cable spikes');
