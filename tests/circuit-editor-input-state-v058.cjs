const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const {test} = require('node:test');
const source = fs.readFileSync('index.html', 'utf8');
function fixture() {
  const sandbox = {
    cbDrag: null, cbHover: null, cbPinch: null, cbGestureLock: false,
    cbPointers: new Map([[7, {x: 50, y: 50}]]),
    cbEdit: {active: true, mode: 'pencil', stroke: {pointerId: 7, raw: [{x: 50, y: 50}]}, tap: {pointerId: 7, start: {x: 50, y: 50}}},
    cbCircuit: {editDraft: {legs: [{points: [{x: 0, y: 0}, {x: 1, y: 0}]}], pending: {points: [{x: .2, y: 0}, {x: .8, y: 0}]}}},
    cbUpdateGame() {}, cbBuildBridgeSyncUi() {}, cbDrawBoard() {}, cbCommitDrag() {}, cbEditMoveStroke() {}, uiToast() {},
    cbEditHitSegment: () => ({legIndex: 0, segmentIndex: 0}),
    deletions: 0,
  };
  sandbox.cbEditDeleteSegment = () => sandbox.deletions++;
  vm.createContext(sandbox);
  for (const name of ['cbCheckpointDrag', 'cbEditPointerMove', 'cbEditPointerUp']) {
    const line = source.split('\n').find(line => line.startsWith(`function ${name}(`));
    assert(line, `Missing production function ${name}`);
    vm.runInContext(line, sandbox);
  }
  return sandbox;
}
for (const clear of [false, true]) test(`interrupt cancels transient input and preserves staged route (clear=${clear})`, () => {
  const s = fixture(), saved = JSON.stringify(s.cbCircuit.editDraft);
  s.cbCheckpointDrag(clear);
  assert.equal(s.cbEdit.stroke, null, 'view/app interruption must cancel the live screen-coordinate stroke');
  assert.equal(s.cbEdit.tap, null, 'interruption must disarm Bin');
  assert.equal(JSON.stringify(s.cbCircuit.editDraft), saved, 'staged and saved route work must survive');
  assert.equal(s.cbPointers.size, clear ? 0 : 1);
  assert.equal(s.cbGestureLock, !clear);
});
test('Bin cannot delete after dragging away then returning to its starting point', () => {
  const s = fixture(); s.cbEdit.mode = 'bin'; s.cbEdit.stroke = null;
  s.cbEditPointerMove({pointerId: 7}, [{x: 80, y: 50}, {x: 50, y: 50}], 300, 400);
  s.cbEditPointerUp({pointerId: 7}, {x: 50, y: 50}, 300, 400);
  assert.equal(s.deletions, 0, 'coalesced out-and-back drag is not an intentional deletion tap');
  assert.equal(s.cbEdit.tap, null);
});
test('Bin still accepts a deliberate tap with minor finger wobble', () => {
  const s = fixture(); s.cbEdit.mode = 'bin'; s.cbEdit.stroke = null;
  s.cbEditPointerMove({pointerId: 7}, [{x: 53, y: 54}], 300, 400);
  s.cbEditPointerUp({pointerId: 7}, {x: 51, y: 52}, 300, 400);
  assert.equal(s.deletions, 1);
});
test('editing an open route must not keep the LOOP CLOSED completion badge', () => {
  const s = fixture(), elements = new Map();
  s.cbScreen = 'game';
  s.cbCircuit = {complete: true, type: 'addressable', panelId: 'p', sequence: ['p','d','p'], legs: [{}], editDraft: {gaps: [{}]}};
  s.cbGameCounts = () => ({total: 1, done: 1, ready: true});
  s.cbEditRouteOpen = () => s.cbCircuit.editDraft.gaps.length > 0;
  s.$ = id => {
    if (!elements.has(id)) elements.set(id, {textContent: '', style: {}, classList: {toggle(){}}, setAttribute(){}, querySelector:()=>({textContent:''})});
    return elements.get(id);
  };
  vm.runInContext(source.split('\n').find(line=>line.startsWith('function cbUpdateGame(')), s);
  s.cbUpdateGame();
  assert.equal(s.$('cbDetectorLeft').textContent, 'ROUTE OPEN');
  s.cbCircuit.editDraft.gaps = [];
  s.cbUpdateGame();
  assert.equal(s.$('cbDetectorLeft').textContent, 'EDITING');
  s.cbEdit = null;
  s.cbUpdateGame();
  assert.equal(s.$('cbDetectorLeft').textContent, 'LOOP CLOSED');
});
function openFixture() {
  const s=fixture();
  Object.assign(s, {state:{zones:[],asFit:null},cbSelection:new Set(),
    cbCircuitIssue:()=>false,cbResetView(){},cbShow(){},cbRenderLanding(){},cbEditSyncUi(){},
    cbEnterEdit(){throw Error('A clean circuit must not inherit another circuit edit')},
    $:()=>({textContent:'',hidden:false,classList:{toggle(){}},style:{setProperty(){}}})});
  vm.runInContext(source.split('\n').find(line=>line.startsWith('function cbOpenCircuit(')),s);
  return s;
}
test('opening another circuit clears the prior editor session without touching its draft',()=>{
  const s=openFixture(),old=s.cbCircuit,saved=JSON.stringify(old.editDraft),next={id:'next',type:'addressable',complete:true,legs:[{}],name:'Loop 2'};
  s.cbOpenCircuit(next);
  assert.equal(s.cbCircuit,next);
  assert.equal(s.cbEdit,null,'old editor must never handle input for the new circuit');
  assert.equal(JSON.stringify(old.editDraft),saved);
  assert.equal(next.editDraft,undefined);
});
test('confirmed survey rebuild removes obsolete edit geometry and bridges',()=>{
  const s=openFixture(),c={id:'changed',type:'addressable',panelId:'p',deviceIds:['d'],sequence:['p','d','p'],legs:[{}],complete:true,bridges:[{}],editDraft:{legs:[{}],gaps:[{}]}};
  Object.assign(s,{cbCircuitIssue:()=>true,cbSymbol:id=>({id,type:id==='p'?'panel':'smoke',scope:'survey'}),symbolScope:d=>d.scope,confirm:()=>true,push(){},persist(){},cbBoundsFor:()=>({x1:0,y1:0,x2:1,y2:1}),cbMakeLayout:()=>({})});
  s.cbEnterEdit=()=>false;
  s.cbOpenCircuit(c);
  assert.equal(c.editDraft,undefined,'old manual edit must not survive an explicitly confirmed circuit rebuild');
  assert.equal(c.bridges.length,0);
  assert.equal(c.legs.length,0);
  assert.equal(c.complete,false);
});
