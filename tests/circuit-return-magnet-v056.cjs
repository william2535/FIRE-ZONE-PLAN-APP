const fs=require('fs'),assert=require('node:assert/strict'),vm=require('node:vm');
const html=fs.readFileSync('index.html','utf8');
if(!/v0\.56/.test(html)){console.log('SKIP: v0.56 return-magnet test only runs after the v0.56 patch');process.exit(0)}

assert.match(html,/v0\.56 addressable return magnet/);
assert.match(html,/function cbReturnPhase\(/);
assert.match(html,/function cbReturnGuidePx\(/);
assert.match(html,/function cbAppendReturnDrag\(/);
assert.match(html,/⇄ RETURN MAGNET · FOLLOW CABLE/);
assert.match(html,/backNeeded\?'Return to FAP':'Complete circuit'/);
assert.match(html,/id===current&&!returning/);
assert.match(html,/returning\?cbReturnGuidePx\(w,h\):cbDrag\.points\.slice\(\)/);
assert.match(html,/Math\.max\(8,Math\.min\(12,8\*Math\.sqrt\(Math\.max\(1,cbView\.scale\)\)\)\)/);
assert.match(html,/rawX=Number\(raw\?\.x\).*Number\.isFinite\(rawX\)/);

function fn(name,next){const re=new RegExp(`function ${name}\\([\\s\\S]*?(?=\\nfunction ${next})`),m=html.match(re);assert(m,`Could not extract ${name}`);return m[0]}
const source=[
 fn('cbCollinear','cbSimplify'),
 fn('cbSimplify','cbPointClose'),
 fn('cbPointClose','cbSegmentConflict'),
 fn('cbReturnPhase','cbReturnGuidePx'),
 fn('cbReturnGuidePx','cbReturnMetrics'),
 fn('cbReturnMetrics','cbReturnPrefixPx'),
 fn('cbReturnPrefixPx','cbAppendReturnDrag')
].join('\n');
const ctx={
 console,Math,Number,Set,
 clamp:(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),
 cbBoardPx:p=>({...p}),
 cbDrag:null,
 cbCircuit:{type:'addressable',complete:false,panelId:'p',deviceIds:['d1','d2'],sequence:['p','d1','d2'],legs:[
   {from:'p',to:'d1',points:[{x:20,y:40},{x:120,y:40},{x:120,y:100}]},
   {from:'d1',to:'d2',points:[{x:120,y:100},{x:220,y:100}]}
 ]}
};
vm.createContext(ctx);vm.runInContext(source,ctx);
assert.equal(ctx.cbReturnPhase(),true,'all devices reached without panel return must enter return phase');
const guide=JSON.parse(JSON.stringify(ctx.cbReturnGuidePx(400,300)));
assert.deepEqual(guide,[{x:220,y:100},{x:120,y:100},{x:120,y:40},{x:20,y:40}], 'return guide must be the exact outgoing route reversed back to the FAP');
const {total}=ctx.cbReturnMetrics(guide);assert.equal(total,260);
const prefix=JSON.parse(JSON.stringify(ctx.cbReturnPrefixPx(guide,150)));
assert.deepEqual(prefix,[{x:220,y:100},{x:120,y:100},{x:120,y:50}], 'partial magnetic return must stay on the canonical outgoing geometry and never invent a freehand dogleg');
ctx.cbCircuit.sequence.push('p');
assert.equal(ctx.cbReturnPhase(),false,'return phase must end once the loop closes at the panel');

console.log('PASS: v0.56 addressable return is canonical, magnetic, visibly paired and has correct return-to-FAP UI state');
