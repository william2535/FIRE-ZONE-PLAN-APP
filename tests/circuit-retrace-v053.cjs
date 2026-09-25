const fs=require('fs'),assert=require('node:assert/strict'),vm=require('node:vm');
const html=fs.readFileSync('index.html','utf8');
assert.match(html,/v0\.53 parallel retrace/);
assert.match(html,/if\(!captured\)cbAppendDrag\(p,w,h\)/,'detector capture must discard the sparse touch tail');
assert.match(html,/pairMode=cbScreen==='game'&&!!cbCircuit/,'parallel-cable feedback must be available on conventional circuits too');

function fn(name,next){
 const re=new RegExp(`function ${name}\\([\\s\\S]*?(?=\\nfunction ${next})`),m=html.match(re);
 assert(m,`Could not extract ${name}`);return m[0];
}
const source=[
 fn('cbCollinear','cbSimplify'),
 fn('cbSimplify','cbPairSegmentsPx'),
 fn('cbPairSegmentsPx','cbPairSnapPx'),
 fn('cbPairSnapPx','cbRouteGridStep'),
 fn('cbRouteGridStep','cbAppendDrag')
].join('\n');

const ctx={console,Math,Number,CB_PAIR_RANGE:24,CB_PAIR_GAP:9,CB_ROUTE_GRID:24,CB_ROUTE_TURN_CELLS:1.45,cbView:{scale:1},cbCircuit:{type:'conventional',legs:[]},cbDrag:null,cbBoardPx:p=>({...p}),cbSelectBounds:null,cbFieldGridScreenStep:()=>({x:24,y:24})};
vm.createContext(ctx);vm.runInContext(source,ctx);

// Simulate the exact field case: a completed horizontal leg ends at a detector, then the
// engineer keeps holding and runs backwards over the same physical route.
ctx.cbDrag={
 points:[{x:220,y:100}],routeAxis:null,pairSide:null,pairSnap:false,
 previewLegs:[{from:'panel',to:'d1',points:[{x:80,y:100},{x:220,y:100}]}]
};
let q=ctx.cbPairSnapPx({x:180,y:100},ctx.cbDrag.points.at(-1),400,300);
assert.equal(ctx.cbDrag.pairSnap,true,'retrace should be recognised as an existing cable run');
assert.equal(ctx.cbDrag.pairAxis,'h');
assert.equal(q.y,109,'same-line retrace should move onto a 9px parallel lane');
ctx.cbRouteGridStep(q,400,300);
assert.deepEqual(JSON.parse(JSON.stringify(ctx.cbDrag.points)),[{x:220,y:100},{x:220,y:109},{x:180,y:109}],'retrace should dogleg once at the detector and continue as a clean parallel line');

q=ctx.cbPairSnapPx({x:130,y:100},ctx.cbDrag.points.at(-1),400,300);ctx.cbRouteGridStep(q,400,300);
const pts=JSON.parse(JSON.stringify(ctx.cbDrag.points));
assert.equal(pts.at(-1).y,109,'paired return must stay on the offset lane instead of collapsing back onto the first cable');
assert.equal(pts.at(-1).x,130);
assert(pts.every((p,i)=>i===0||Math.abs(p.x-pts[i-1].x)<1e-9||Math.abs(p.y-pts[i-1].y)<1e-9),'paired route must remain orthogonal');

// Simulate a sparse corner event. The previous v0.51 turn code extended the horizontal
// leg all the way to q.x before turning, producing the long spikes seen onsite.
ctx.cbDrag={points:[{x:100,y:200},{x:200,y:200}],routeAxis:'h',pairSnap:false,pairAxis:null,pairLine:null,previewLegs:[]};
ctx.cbRouteGridStep({x:340,y:260},400,300);
const corner=JSON.parse(JSON.stringify(ctx.cbDrag.points));
assert.deepEqual(corner,[{x:100,y:200},{x:200,y:200},{x:200,y:260}],'corner must turn at the last reached grid point, not shoot the old leg out to a distant touch sample');
assert.equal(ctx.cbDrag.routeAxis,'v');

console.log('PASS: v0.53 retracing creates a true parallel cable lane and sparse corner events cannot create long cable spikes');
