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
 vm.createContext(ctx);for(const name of ['cbPairSegmentsPx','cbRouteCellPx','cbPairSnapPx','cbRouteGridStep','cbCollinear','cbSimplify','cbCheckpointDrag','cbCanvasCancel','cbChallengeOwner','cbEditCleanStroke','cbEditOrthogonalPush','cbEditDoglegClean','cbPruneRouteNoise','cbRouteAxis','cbDrawBundled','cbBundlePaths','cbSegKey'])vm.runInContext(functions.get(name),ctx);
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

test('reversed outgoing/return segments draw on distinct sides in board and export',()=>{
 const c=fixture();for(const [a,b] of [[{x:20,y:100},{x:220,y:100}],[{x:100,y:20},{x:100,y:220}]])for(const scale of [1,3]){
 const drawn=[],ctx={save(){},restore(){},beginPath(){this.path=[]},moveTo(x,y){this.path.push({x,y})},lineTo(x,y){this.path.push({x,y})},stroke(){drawn.push(this.path)}};
 c.cbDrawBundled(ctx,[{a,b,color:'red'},{a:b,b:a,color:'blue'}],p=>({x:p.x*scale,y:p.y*scale}),5,9*scale);assert.equal(Math.hypot(drawn[0][1].x-drawn[1].at(-2).x,drawn[0][1].y-drawn[1].at(-2).y),9*scale,'reversed paths must not land on the same visual lane');
 }
});

function panelFixture(){
 const c=fixture();c.CB_DEVICE_R=11;c.CB_PANEL_R=16;c.cbCircuit.panelId='p';c.cbNodePx=()=>({x:200,y:100});c.other.panelId='p';c.other.legs=[{from:'p',to:'a',points:[{x:200,y:100},{x:200,y:136},{x:80,y:136},{x:80,y:240}]}];
 for(const name of ['cbPointClose','cbSegmentConflict','cbPanelExitStems','cbPanelExitAllows','cbChallengeObstacleSegmentsPx','cbChallengePointsBlocked','cbEditSegmentIntersection'])vm.runInContext(functions.get(name),c);
 c.cbDrag={from:'p',points:[{x:200,y:100}],previewLegs:[],routeInput:{x:200,y:100}};return c;
}
test('shared panel exit permits down and right, but left across the blue cable needs a bridge',()=>{
 const c=panelFixture(),p={x:200,y:100};
 assert.equal(c.cbChallengePointsBlocked([p,{x:200,y:132}],400,300),false,'shared stem');
 assert.equal(c.cbChallengePointsBlocked([p,{x:200,y:165},{x:250,y:165}],400,300),false,'continue down and peel right');
 const left=[p,{x:200,y:165},{x:60,y:165}];assert.equal(c.cbChallengePointsBlocked(left,400,300),true,'left crosses blue vertical cable');c.cbBuildBridge=true;assert.equal(c.cbChallengePointsBlocked(left,400,300),false);
});
test('panel sharing is bounded and never exempts an unrelated panel or later crossing',()=>{
 const c=panelFixture();c.other.legs[0].points=[{x:200,y:100},{x:200,y:280}];assert.equal(c.cbChallengePointsBlocked([{x:200,y:100},{x:200,y:180}],400,300),true,'long overlap is not a panel exit');c.other.panelId='other';assert.equal(c.cbChallengePointsBlocked([{x:200,y:100},{x:200,y:136}],400,300),true,'different panel');
});
test('more than four zones can reuse a short shared panel tail without merging IDs',()=>{
 const c=panelFixture(),others=Array.from({length:8},(_,i)=>({...copy(c.other),id:'zone'+i,color:'#'+i+'23456'}));c.cbCircuits=()=>[...others,c.cbCircuit];c.cbChallengeCircuits=()=>others;
 const before=JSON.stringify(others),q=c.cbPairSnapPx({x:200,y:130},{x:200,y:100},400,300,{x:201,y:130});assert.deepEqual(copy(q),{x:200,y:130});assert.equal(c.cbChallengePointsBlocked([{x:200,y:100},q,{x:245,y:130}],400,300),false);assert.equal(JSON.stringify(others),before);
});
test('sampled drag leaves a busy panel and turns right without a false crossing',()=>{
 const c=panelFixture();Object.assign(c,{cbReturnPhase:()=>false,uiHaptics:false});for(const name of ['cbAppendDrag','cbGeometryIntent','cbRouteSnapshot','cbRouteRestore','cbMarkBlocked'])vm.runInContext(functions.get(name),c);
 for(let y=104;y<=164;y+=4)assert.equal(c.cbAppendDrag({x:200,y},400,300,true),true,'down at '+y+' '+JSON.stringify(c.cbDrag.points));
 for(let x=204;x<=260;x+=4)assert.equal(c.cbAppendDrag({x,y:164},400,300,true),true,'right at '+x+' '+JSON.stringify(c.cbDrag.points));
 assert(c.cbDrag.points.at(-1).x>=250);assert.equal(c.cbDrag.blocked,false);
});
test('a zero-length legacy panel segment cannot become an unlimited shared exit',()=>{
 const c=panelFixture();c.other.legs[0].points=[{x:200,y:100},{x:200,y:100},{x:80,y:100}];assert.equal(c.cbPanelExitStems(400,300).length,0);const q=c.cbPairSnapPx({x:200,y:280},{x:200,y:100},400,300,{x:200,y:280});assert.equal(c.cbDrag.pairSnap,false);assert.equal(q.y,280);
});
