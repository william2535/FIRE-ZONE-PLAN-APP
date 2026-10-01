// Deterministic regressions for defects reproduced on 1 October 2026.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),{test}=require('node:test'),acorn=require('acorn');
const html=fs.readFileSync('index.html','utf8'),functions=new Map();
for(const match of html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)){
 if(!match[1].trim())continue;
 const walk=n=>{if(!n||typeof n!=='object')return;if(n.type==='FunctionDeclaration')functions.set(n.id.name,match[1].slice(n.start,n.end));for(const value of Object.values(n))if(Array.isArray(value))value.forEach(walk);else if(value&&typeof value==='object')walk(value)};walk(acorn.parse(match[1],{ecmaVersion:'latest'}));
}
function fixture(){
 const ctx={Math,Number,Map,Set,console,clamp:(x,a=0,b=1)=>Math.max(a,Math.min(b,x)),cbSnapPx:p=>({...p}),CB_PAIR_RANGE:24,CB_PAIR_GAP:9,CB_ROUTE_GRID:24,CB_ROUTE_TURN_CELLS:.72,CB_ROUTE_ARM_CELLS:.28,cbView:{scale:1},cbSelectBounds:null,cbCircuit:{id:'blue',color:'#2675db',type:'conventional',legs:[]},cbDrag:null,cbEdit:null,cbBuildBridge:false,cbPointers:new Map(),cbPinch:null,cbGestureLock:false,cbHover:null,cbBoardPx:p=>({...p}),cbEditCircuitPointPx:(c,p)=>({...p}),cbChallengeMapPointPx:(c,p)=>({...p}),cbFieldGridScreenStep:()=>({x:24,y:24}),cbCircuitIssue:()=>false,cbUpdateGame(){},cbDrawBoard(){},cbClearReward(){}};
 ctx.other={id:'red',color:'#e33a3a',type:'conventional',complete:true,legs:[{points:[{x:40,y:100},{x:340,y:100}]}]};ctx.cbCircuits=()=>[ctx.other,ctx.cbCircuit];ctx.cbChallengeCircuits=()=>[ctx.other];ctx.cbLegSegments=c=>c.legs.flatMap(l=>l.points.slice(1).map((b,i)=>({a:l.points[i],b})));
 vm.createContext(ctx);for(const name of ['cbPairSegmentsPx','cbRouteCellPx','cbPairSnapPx','cbRouteGridStep','cbCollinear','cbSimplify','cbCheckpointDrag','cbCanvasCancel','cbChallengeOwner','cbEditCleanStroke','cbEditOrthogonalPush','cbEditDoglegClean','cbPruneRouteNoise','cbRouteAxis'])vm.runInContext(functions.get(name),ctx);
 return ctx;
}
const copy=v=>JSON.parse(JSON.stringify(v));
test('another colour supplies a separate lane and never becomes a circuit association',()=>{
 const c=fixture(),before=JSON.stringify(c.other);c.cbDrag={points:[{x:40,y:100}],previewLegs:[],routeInput:{x:40,y:100}};
 const q=c.cbPairSnapPx({x:160,y:100},c.cbDrag.points[0],400,300,{x:160,y:102});
 assert.equal(c.cbDrag.pairSnap,true);assert.equal(q.y,109);assert.equal(JSON.stringify(c.other),before);assert.equal(c.cbCircuit.legs.length,0);
});
test('pairing into a new row keeps the connector orthogonal',()=>{
 const c=fixture();c.cbDrag={points:[{x:40,y:100},{x:120,y:100}],routeAxis:'h',pairSnap:true,pairAxis:'h',pairLine:109};
 c.cbRouteGridStep({x:170,y:109},400,300);
 assert.deepEqual(copy(c.cbDrag.points),[{x:40,y:100},{x:120,y:100},{x:120,y:109},{x:170,y:109}]);
});
test('shaky touches crossing the original line stay in the selected lane',()=>{
 const c=fixture();c.cbDrag={points:[{x:40,y:100}],previewLegs:[],routeInput:{x:40,y:100}};
 for(let x=70;x<=280;x+=10){const p={x,y:100+(x%20?3:-3)},q=c.cbPairSnapPx(p,c.cbDrag.points.at(-1),400,300,p);c.cbRouteGridStep(q,400,300,p);c.cbDrag.routeInput=p;assert.equal(q.y,109,'lane must not hop through the other cable with finger wobble')}
 assert(c.cbDrag.points.length<=3,'parallel run must remain one straight lane');
});
test('a third colour takes an unoccupied lane on the same side',()=>{
 const c=fixture(),green={id:'green',color:'#20a36b',type:'conventional',legs:[{points:[{x:40,y:109},{x:340,y:109}]}]};c.cbCircuits=()=>[c.other,green,c.cbCircuit];c.cbChallengeCircuits=()=>[c.other,green];
 c.cbDrag={points:[{x:40,y:100}],previewLegs:[],routeInput:{x:40,y:100}};
 const q=c.cbPairSnapPx({x:160,y:100},c.cbDrag.points[0],400,300,{x:160,y:102});assert.equal(q.y,118,'occupied first lane must not merge the new colour with it');
});
test('same-colour foreign circuits do not offer automatic pairing',()=>{
 const c=fixture();c.other.color=c.cbCircuit.color;c.cbDrag={points:[{x:40,y:100}],previewLegs:[],routeInput:{x:40,y:100}};c.cbPairSnapPx({x:160,y:100},c.cbDrag.points[0],400,300);assert.equal(c.cbDrag.pairSnap,false);
});
test('cancel checkpoints reached devices once and discards only the unfinished tail',()=>{
 const c=fixture();let commits=0;c.cbCommitDrag=()=>{commits++;c.cbDrag=null};c.cbDrag={targets:['d1'],previewLegs:[{from:'p',to:'d1'}],points:[{x:60,y:50},{x:90,y:50}]};c.cbPointers.set(7,{x:90,y:50});c.cbCanvasCancel({pointerId:7});c.cbCanvasCancel({pointerId:7});assert.equal(commits,1);assert.equal(c.cbDrag,null);assert.equal(c.cbPointers.size,0);
});

test('a zero-length paired tail cannot turn its perpendicular connector into a diagonal',()=>{
 const c=fixture();c.cbDrag={points:[{x:254,y:88},{x:263,y:88}],routeAxis:'v',pairSnap:true,pairAxis:'v',pairLine:263};
 c.cbRouteGridStep({x:263,y:96},400,300);
 assert.deepEqual(copy(c.cbDrag.points),[{x:254,y:88},{x:263,y:88},{x:263,y:96}]);
});

test('shared FAP remains the active start node when other coloured circuits are visible',()=>{
 const c=fixture();c.cbCircuit.panelId='p';c.cbCircuit.deviceIds=['b'];c.other.panelId='p';c.other.deviceIds=['a'];assert.equal(c.cbChallengeOwner('p'),c.cbCircuit);assert.equal(c.cbChallengeOwner('a'),c.other);
});

test('Pencil cleanup uses the same separate lane without leaving a staircase',()=>{
 const c=fixture(),start={x:40,y:150},end={x:300,y:150},raw=[start,{x:40,y:110},{x:80,y:103},{x:120,y:99},{x:170,y:102},{x:240,y:100},{x:300,y:103},end];
 const points=copy(c.cbEditCleanStroke(raw,start,end,400,300,80));assert.deepEqual(points[0],start);assert.deepEqual(points.at(-1),end);assert(points.length<=5,JSON.stringify(points));assert(points.every((p,i)=>!i||p.x===points[i-1].x||p.y===points[i-1].y));assert(points.some((p,i)=>i&&p.y===109&&points[i-1].y===109&&Math.abs(p.x-points[i-1].x)>150));
});
test('a full lane bank refuses to silently overlap another colour',()=>{
 const c=fixture(),lanes=Array.from({length:14},(_,i)=>({a:{x:40,y:100+i*9},b:{x:340,y:100+i*9},foreign:true}));c.cbDrag={points:[{x:40,y:100}],routeInput:{x:40,y:100}};const q=c.cbPairSnapPx({x:160,y:102},c.cbDrag.points[0],400,300,{x:160,y:102},c.cbDrag,lanes);assert.equal(c.cbDrag.pairSnap,false);assert.deepEqual(copy(q),{x:160,y:102});
});
