const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const {test} = require('node:test');
const source = fs.readFileSync('index.html', 'utf8');

function production(names, extra={}) {
  const sandbox = {
    cbBoardToPlan(p,b){return {x:b.x1+p.x*(b.x2-b.x1),y:b.y1+p.y*(b.y2-b.y1)}},
    cbPlanToBoard(p,b){return {x:(p.x-b.x1)/(b.x2-b.x1),y:(p.y-b.y1)/(b.y2-b.y1)}},
    cbMakeLayout(ids,bounds){sandbox.layoutCalls++;return {ids:[...ids],bounds:{...bounds}}},
    layoutCalls:0,
    ...extra,
  };
  vm.createContext(sandbox);
  for (const name of names) {
    const line = source.split('\n').find(line => line.startsWith(`function ${name}(`));
    assert(line, `Missing production function ${name}`);
    vm.runInContext(line, sandbox);
  }
  return sandbox;
}

function planPoint(s,p,b){const q=s.cbBoardToPlan(p,b);return [q.x,q.y].map(v=>Number(v.toFixed(9)))}
function collectPlanGeometry(s,c,bounds){
  const out=[];
  for(const leg of c.legs||[])for(const p of leg.points||[])out.push(['committed',...planPoint(s,p,bounds)]);
  for(const b of c.bridges||[])if(b?.point)out.push(['bridge',...planPoint(s,b.point,bounds)]);
  const d=c.editDraft;
  if(d){
    for(const leg of d.legs||[])for(const p of leg.points||[])out.push(['draft-leg',...planPoint(s,p,bounds)]);
    for(const g of d.gaps||[]){if(g?.a)out.push(['gap-a',...planPoint(s,g.a,bounds)]);if(g?.b)out.push(['gap-b',...planPoint(s,g.b,bounds)])}
    for(const b of d.bridges||[])if(b?.point)out.push(['draft-bridge',...planPoint(s,b.point,bounds)]);
    const p=d.pending;
    if(p){
      if(p.startPoint)out.push(['pending-start',...planPoint(s,p.startPoint,bounds)]);
      if(p.endPoint)out.push(['pending-end',...planPoint(s,p.endPoint,bounds)]);
      for(const q of p.points||[])out.push(['pending-point',...planPoint(s,q,bounds)]);
      for(const b of p.bridges||[])if(b?.point)out.push(['pending-bridge',...planPoint(s,b.point,bounds)]);
    }
  }
  return out;
}

test('conventional bounds rebase preserves committed bridges and every staged edit at the same plan coordinates',()=>{
  const s=production(['cbBoundsNear','cbRebaseCircuit']);
  const oldBounds={x1:.10,y1:.20,x2:.70,y2:.80},newBounds={x1:.02,y1:.08,x2:.92,y2:.96};
  const c={id:'z1',type:'conventional',panelId:'p',deviceIds:['d1','d2'],bounds:{...oldBounds},
    legs:[{from:'p',to:'d1',points:[{x:.1,y:.2},{x:.7,y:.2}]}],
    bridges:[{legIndex:0,point:{x:.45,y:.2},axis:'h'}],
    editDraft:{
      legs:[{from:'p',to:'d1',points:[{x:.1,y:.2},{x:.1,y:.62},{x:.7,y:.62},{x:.7,y:.2}]}],
      gaps:[{legIndex:0,segmentIndex:1,a:{x:.1,y:.62},b:{x:.7,y:.62}}],
      bridges:[{legIndex:0,point:{x:.1,y:.44},axis:'v'}],cleanup:65,
      pending:{legIndex:0,startPos:.35,endPos:2.4,startPoint:{x:.1,y:.347},endPoint:{x:.46,y:.62},points:[{x:.1,y:.347},{x:.32,y:.347},{x:.32,y:.62},{x:.46,y:.62}],bridges:[{point:{x:.32,y:.50},axis:'v'}]}
    }};
  const before=collectPlanGeometry(s,c,oldBounds),shape={cleanup:c.editDraft.cleanup,gapIndex:c.editDraft.gaps[0].segmentIndex,startPos:c.editDraft.pending.startPos,endPos:c.editDraft.pending.endPos};
  assert.equal(s.cbRebaseCircuit(c,newBounds),true);
  assert.deepEqual(collectPlanGeometry(s,c,newBounds),before,'all board-coordinate editor state must retain its original plan position');
  assert.deepEqual({cleanup:c.editDraft.cleanup,gapIndex:c.editDraft.gaps[0].segmentIndex,startPos:c.editDraft.pending.startPos,endPos:c.editDraft.pending.endPos},shape,'non-coordinate editor metadata must not be changed by rebase');
  assert.equal(JSON.stringify(c.bounds),JSON.stringify(newBounds));
  assert.equal(s.layoutCalls,1);
});

test('near-identical bounds only refresh layout and do not mutate route geometry',()=>{
  const s=production(['cbBoundsNear','cbRebaseCircuit']),bounds={x1:0,y1:0,x2:1,y2:1},c={type:'conventional',panelId:'p',deviceIds:['d'],bounds:{...bounds},legs:[{points:[{x:.2,y:.3},{x:.8,y:.3}]}],bridges:[{point:{x:.5,y:.3}}],editDraft:{legs:[{points:[{x:.2,y:.3},{x:.8,y:.3}]}],gaps:[],bridges:[],pending:null,cleanup:45}};
  const before=JSON.stringify({legs:c.legs,bridges:c.bridges,editDraft:c.editDraft});
  assert.equal(s.cbRebaseCircuit(c,{...bounds,x2:1+1e-9}),false);
  assert.equal(JSON.stringify({legs:c.legs,bridges:c.bridges,editDraft:c.editDraft}),before);
  assert.equal(s.layoutCalls,1);
});

test('mobile editor reserves the iPhone bottom safe area',()=>{
  assert(source.includes('.cbStage{padding:7px 7px calc(7px + env(safe-area-inset-bottom))}'),'mobile Circuit Builder stage must reserve the bottom safe area');
  assert(source.includes('.cbEditOptionsPanel{position:fixed;top:auto;bottom:calc(72px + env(safe-area-inset-bottom));right:8px;left:8px;width:auto}'),'mobile Cleanup sheet must sit above the iPhone home-indicator safe area');
});
