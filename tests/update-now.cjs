const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('index.html','utf8');
const start=html.indexOf('async function updateAppNow(){'),end=html.indexOf("$('homeUpdate').onclick=updateAppNow;",start);
assert(start>0&&end>start);
function setup(options={}){
 const elements={homeUpdate:{disabled:false,setAttribute(){},removeAttribute(){}},homeUpdateLabel:{},homeUpdateStatus:{}},home={inert:false},calls=[];
 const ctx={projectBusy:false,projectsReady:true,$:id=>elements[id],document:{querySelector:()=>home},saveNow:async()=>{calls.push('save');return options.save!==false},location:{protocol:options.native?'file:':'https:',href:'https://example.com/FIRE-ZONE-PLAN-APP/ZoneSketch.html?old=1',replace:url=>calls.push(['navigate',url])},openBetaPortal:()=>calls.push('android'),URL,AbortController,TypeError,setTimeout,clearTimeout,fetch:async(url,config)=>{calls.push(['fetch',url,config.cache]);if(options.offline)throw new TypeError('offline');return{ok:!options.httpError,text:async()=>options.badHtml?'not an app':'<div id="projectsHome"></div><canvas id="canvas"></canvas>'}}};
 vm.createContext(ctx);vm.runInContext(html.slice(start,end),ctx);return{ctx,elements,home,calls};
}
(async()=>{
 const good=setup();await good.ctx.updateAppNow();assert.equal(good.calls[0],'save');assert.equal(good.calls[1][0],'fetch');assert.equal(good.calls[1][2],'no-store');assert.equal(good.calls[2][0],'navigate');const url=new URL(good.calls[2][1]);assert.equal(url.origin,'https://example.com');assert.equal(url.pathname,'/FIRE-ZONE-PLAN-APP/index.html');assert(url.searchParams.has('fresh'));assert.equal(good.home.inert,false);
 for(const options of [{save:false},{offline:true},{httpError:true},{badHtml:true}]){const t=setup(options);await t.ctx.updateAppNow();assert(!t.calls.some(c=>Array.isArray(c)&&c[0]==='navigate'));assert(t.elements.homeUpdateStatus.textContent.length);assert.equal(t.elements.homeUpdate.disabled,false);assert.equal(t.home.inert,false);assert.equal(t.ctx.projectBusy,false);if(options.save===false)assert.deepEqual(t.calls,['save']);}
 const native=setup({native:true});await native.ctx.updateAppNow();assert.deepEqual(native.calls,['save','android']);
 const busy=setup();busy.ctx.projectBusy=true;await busy.ctx.updateAppNow();assert.equal(busy.calls.length,0);
 assert(html.indexOf('class="homeUpdateFooter"')>html.indexOf('id="projectGrid"'),'Update control belongs at the bottom of Home');
 console.log('PASS: save-before-update, same-origin fresh URL, cache bypass, save failure, offline/error response, invalid page, native app routing and repeated-click guard');
})().catch(e=>{console.error(e);process.exit(1)});
