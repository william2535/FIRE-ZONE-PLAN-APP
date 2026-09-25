const fs=require('fs'),assert=require('node:assert/strict'),vm=require('node:vm');
const html=fs.readFileSync('index.html','utf8');
assert.match(html,/v0\.57 aggressive-touch input pipeline/);
for(const marker of ['function cbRoutingState','function cbSetRoutingState','function cbRecordRawPoint','function cbHitCorridorPx','function cbProcessSamples','function cbGeometryIntent','function cbPruneRouteNoise','captureGuard','getCoalescedEvents'])assert(html.includes(marker),`missing Smart Route marker: ${marker}`);
for(const state of ['waiting-to-start','routing-normal','approaching-device','device-captured','corner-pending','corner-committed','returning'])assert(html.includes(state),`missing routing state: ${state}`);
function fn(name,next){const re=new RegExp(`function ${name}\\([\\s\\S]*?(?=\\nfunction ${next}\\()`),m=html.match(re);assert(m,`Could not extract ${name}`);return m[0]}
const hitSrc=fn('cbNodesAlong','cbProcessPointer');
const hitCtx={console,Math,cbCircuit:{panelId:null,deviceIds:['d']},cbSurveyDevices:()=>[],cbNodePx:id=>id==='d'?{x:150,y:100}:null,cbHitCorridorPx:()=>30,clamp:(v,a=0,b=1)=>Math.max(a,Math.min(b,v))};vm.createContext(hitCtx);vm.runInContext(hitSrc,hitCtx);
assert.equal(hitCtx.cbNodesAlong({x:100,y:129},{x:200,y:129},400,300,false)[0]?.id,'d','swept path must capture a device between sparse pointer samples');
assert.equal(hitCtx.cbNodesAlong({x:100,y:131},{x:200,y:131},400,300,false).length,0,'device corridor must stay bounded');
const cleanSrc=[fn('cbCollinear','cbSimplify'),fn('cbSimplify','cbRouteAxis'),fn('cbRouteAxis','cbPruneRouteNoise'),fn('cbPruneRouteNoise','cbGeometryIntent')].join('\n');
const cleanCtx={console,Math,cbRouteCellPx:()=>({x:24,y:24})};vm.createContext(cleanCtx);vm.runInContext(cleanSrc,cleanCtx);
const clean=JSON.parse(JSON.stringify(cleanCtx.cbPruneRouteNoise([{x:100,y:100},{x:220,y:100},{x:180,y:100}],400,300)));
assert.deepEqual(clean,[{x:100,y:100},{x:180,y:100}],'same-axis overshoot/backstep must collapse out of saved geometry');
console.log('PASS: v0.57 Smart Route keeps raw/coalesced input separate, uses a swept hit corridor, explicit routing states and route-noise cleanup');
