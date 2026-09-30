const {chromium}=require('playwright');
const fs=require('node:fs'),http=require('node:http'),assert=require('node:assert/strict');
const source=fs.readFileSync('index.html','utf8');
for(const marker of [
  "security:{type:'secPanel'",
  "access:{type:'accessAcu'",
  "cctv:{type:'cctvNvr'",
  "function cbCircuitNeedsReturn(c)",
  "function cbPanels(c=null)",
  "systemType,zoneId,panelId:panel.id",
  "!cbIsAnyControllerSymbol(s)",
  "cbCircuitNeedsReturn(c)&&c.deviceIds.every",
  "cbCircuitNeedsReturn(cbCircuit)&&q.done===q.total"
])assert(source.includes(marker),'Missing '+marker);
assert(!source.includes("uiNotice('Fire panel required'"),'Circuit Builder still has unconditional Fire panel error');

const server=http.createServer((req,res)=>{try{const file=decodeURIComponent((req.url||'/').split('?')[0]).slice(1)||'index.html';res.end(fs.readFileSync(file))}catch{res.statusCode=404;res.end()}}).listen(0,'127.0.0.1');

(async()=>{
  await new Promise(ok=>server.once('listening',ok));
  const browser=await chromium.launch({headless:true});
  try{
    const p=await browser.newPage({viewport:{width:390,height:844},hasTouch:true}),errors=[];
    p.on('pageerror',e=>errors.push(e.message));
    await p.goto('http://127.0.0.1:'+server.address().port);
    await p.waitForFunction(()=>!document.querySelector('#homeNew').disabled);

    const result=await p.evaluate(()=>{
      const cases=[
        ['fire','panel','Fire Alarm Panel','FAP',true,'addressable loop'],
        ['security','secPanel','Intruder Panel','Intruder Panel',false,'security circuit'],
        ['access','accessAcu','ACU','ACU',false,'access run'],
        ['cctv','cctvNvr','NVR','NVR',false,'camera run']
      ];
      const out=[];
      for(const [key,type,name,short,needsReturn,runLabel] of cases){
        state.systemType=key;
        state.symbols=[
          {id:'controller',type,scope:'survey',x:.1,y:.1},
          {id:'device',type:key==='security'?'secPir':key==='access'?'accessReader':key==='cctv'?'cctvFixed':'smoke',scope:'survey',x:.4,y:.4},
          {id:'other-controller',type:key==='security'?'cctvNvr':'secPanel',scope:'survey',x:.8,y:.8}
        ];
        cbInvalidateSymbolIndex();
        const cfg=cbControllerConfig();
        const circuit={type:'addressable',systemType:key,panelId:'controller',deviceIds:['device']};
        const openReady=cbSequenceReady(circuit,['controller','device']);
        const closedReady=cbSequenceReady(circuit,['controller','device','controller']);
        cbSyncSystemCircuitUi();
        out.push({
          key,
          cfg:{type:cfg.type,name:cfg.name,short:cfg.short,returnToController:cfg.returnToController,runLabel:cfg.runLabel},
          panelTypes:cbPanels().map(s=>s.type),
          deviceIds:cbSurveyDevices().map(s=>s.id),
          openReady,
          closedReady,
          title:cbCircuitControllerNotice(cfg).title,
          button:document.querySelector('#cbAddressableStart').textContent.trim()
        });
      }
      return out;
    });

    const expected={
      fire:{type:'panel',name:'Fire Alarm Panel',short:'FAP',returnToController:true,runLabel:'addressable loop',button:'Highlight a loop'},
      security:{type:'secPanel',name:'Intruder Panel',short:'Intruder Panel',returnToController:false,runLabel:'security circuit',button:'Highlight security circuit'},
      access:{type:'accessAcu',name:'ACU',short:'ACU',returnToController:false,runLabel:'access run',button:'Highlight access run'},
      cctv:{type:'cctvNvr',name:'NVR',short:'NVR',returnToController:false,runLabel:'camera run',button:'Highlight camera run'}
    };

    for(const row of result){
      assert.deepEqual(row.cfg,{
        type:expected[row.key].type,
        name:expected[row.key].name,
        short:expected[row.key].short,
        returnToController:expected[row.key].returnToController,
        runLabel:expected[row.key].runLabel
      });
      assert.deepEqual(row.panelTypes,[expected[row.key].type]);
      assert.deepEqual(row.deviceIds,['device']);
      assert.equal(row.openReady,row.key!=='fire');
      assert.equal(row.closedReady,true);
      assert.equal(row.title,expected[row.key].name+' required');
      assert.equal(row.button,expected[row.key].button);
    }
    assert.deepEqual(errors,[]);
    console.log('PASS: Circuit Builder uses FAP / Intruder Panel / ACU / NVR and only Fire loops require controller return');
  }finally{
    await browser.close();
    server.close();
  }
})().catch(e=>{console.error(e);server.close();process.exit(1)});
