const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('index.html','utf8');
for(const m of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)){if(m[2].trim()&&!/application\//.test(m[1]))new vm.Script(m[2]);}
const elements=Object.fromEntries(['roomLabelScale','roomLabelScaleValue','applyRoomLabelSize'].map(id=>[id,{}]));
const presets=['0.25','0.5','1'].map(roomScale=>({dataset:{roomScale},classList:{toggle(){}},setAttribute(k,v){this[k]=v}}));
const saved=new Map(),snapshots=[],changes=[],toasts=[];
const ctx={state:{labels:[],locks:{}},roomLabelScale:1,surveyMode:false,document:{querySelectorAll:()=>presets},$:id=>elements[id],uid:()=>String(Math.random()),localStorage:{getItem:k=>saved.get(k)??null,setItem:(k,v)=>saved.set(k,v)},push:()=>snapshots.push(JSON.parse(JSON.stringify(ctx.state))),changed:()=>changes.push(true),uiToast:(...v)=>toasts.push(v),isRefLocked:()=>ctx.surveyMode||!!ctx.state.locks.building};
vm.createContext(ctx);
for(const name of ['loadRoomLabelScale','syncRoomLabelSize','setRoomLabelScale','makeRoomLabel','applyRoomLabelSize']){
 const line=html.split('\n').find(line=>line.startsWith('function '+name+'('));assert(line,name+' exists');vm.runInContext(line,ctx);
}
assert.equal(ctx.loadRoomLabelScale(),1);
saved.set('zoneSketchRoomLabelScale','broken');assert.equal(ctx.loadRoomLabelScale(),1);
ctx.state.labels=[{id:'legacy',x:.2,y:.3,text:'Office',group:'room'},{id:'sized',x:.6,y:.5,text:'WC',scale:.5}];
ctx.state.floors=[{id:'other',data:{labels:[{id:'other-label',scale:1}]}}];
ctx.setRoomLabelScale(.25);
assert.equal(elements.roomLabelScaleValue.textContent,'25%');assert.equal(presets[0]['aria-pressed'],'true');
assert.equal(ctx.loadRoomLabelScale(),.25,'size preference survives reload');
assert.equal(ctx.state.labels[0].scale,undefined,'preset does not silently resize existing labels');
const created=ctx.makeRoomLabel({x:.4,y:.7},'Store','group-1');
assert.equal(created.scale,.25);assert.equal(created.text,'Store');assert.equal(created.group,'group-1');assert.equal(created.x,.4);
ctx.applyRoomLabelSize();
assert.equal(snapshots.length,1,'one undo step for the whole floor');assert.equal(changes.length,1);
assert(ctx.state.labels.every(l=>l.scale===.25));assert.equal(ctx.state.labels[0].group,'room');assert.equal(ctx.state.labels[0].x,.2);
assert.equal(ctx.state.floors[0].data.labels[0].scale,1,'other floors unchanged');
ctx.applyRoomLabelSize();assert.equal(snapshots.length,1,'same size is a no-op');
ctx.state=JSON.parse(JSON.stringify(snapshots[0]));assert.equal(ctx.state.labels[0].scale,undefined);assert.equal(ctx.state.labels[1].scale,.5);
ctx.state.locks.building=true;ctx.syncRoomLabelSize();assert.equal(elements.applyRoomLabelSize.disabled,true);ctx.applyRoomLabelSize();assert.equal(changes.length,1);
ctx.state.locks.building=false;ctx.surveyMode=true;ctx.applyRoomLabelSize();assert.equal(changes.length,1);
ctx.surveyMode=false;ctx.setRoomLabelScale(.1);assert.equal(ctx.makeRoomLabel({x:0,y:0},'Office').scale,.1);
ctx.setRoomLabelScale(-5);assert.equal(ctx.roomLabelScale,.1);ctx.setRoomLabelScale(100);assert.equal(ctx.roomLabelScale,4);
ctx.setRoomLabelScale(NaN);assert.equal(ctx.roomLabelScale,1);
ctx.localStorage.getItem=()=>{throw Error('storage blocked')};ctx.localStorage.setItem=()=>{throw Error('storage blocked')};
assert.equal(ctx.loadRoomLabelScale(),1);ctx.setRoomLabelScale(.5);assert.equal(ctx.roomLabelScale,.5);
assert(html.includes('id="roomLabelScale"'));assert(html.includes('id="applyRoomLabelSize"'));
assert(html.includes('makeRoomLabel(inputPoint(e.clientX,e.clientY),roomStamp)'));
assert(html.includes('makeRoomLabel(inputPoint(e.clientX,e.clientY),value.trim().slice(0,35))'));
assert(html.includes('makeRoomLabel(c,labelText,gid)'));
console.log('PASS: room-label presets, remembered size, new labels, current-floor resizing, undo snapshot, locks, no-ops, limits and blocked storage');
