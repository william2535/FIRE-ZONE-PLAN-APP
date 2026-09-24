from pathlib import Path

ROOT = Path('.')
MAIN = ROOT / 'index.html'

def replace_once(text, old, new, label):
    if new in text and old not in text:
        return text
    if old not in text:
        raise SystemExit(f'v0.40 patch marker missing: {label}')
    return text.replace(old, new, 1)

text = MAIN.read_text()

# Version labels.
text = text.replace('v0.39.1', 'v0.40')

# Smaller grid controls.
text = replace_once(
    text,
    '<label class="wallControl" title="Grid spacing on the plan">Grid <input id="gridSize" type="range" min="20" max="250" step="10" value="100"><output id="gridSizeValue">100</output></label>',
    '<label class="wallControl" title="Grid spacing on the plan">Grid <input id="gridSize" type="range" min="5" max="250" step="5" value="100"><output id="gridSizeValue">100</output></label>',
    'top grid slider'
)
text = replace_once(
    text,
    '<label for="surveyGridSize">Grid spacing</label><select id="surveyGridSize"><option value="40">Fine · 40</option><option value="50">50</option><option value="100">100</option><option value="200">Coarse · 200</option></select>',
    '<label for="surveyGridSize">Grid spacing</label><select id="surveyGridSize"><option value="5">Extra fine · 5</option><option value="10">10</option><option value="20">20</option><option value="40">Fine · 40</option><option value="50">50</option><option value="100">100</option><option value="200">Coarse · 200</option></select>',
    'survey grid choices'
)
text = replace_once(
    text,
    'function gridStep(){return Math.max(20,Number(state.gridSize)||100)}',
    'function gridStep(){return Math.max(5,Number(state.gridSize)||100)}',
    'grid minimum'
)

# Survey favourites rail beside the drawing.
rail_css = r"""
/* v0.40 — survey quick favourites. */
#surveyFavouriteRail{display:none;position:absolute;z-index:19;left:10px;top:10px;width:118px;max-height:calc(100% - 84px);padding:7px;border:1px solid #c8d4df;border-radius:14px;background:#fffffff2;box-shadow:0 5px 18px #16283e24;backdrop-filter:blur(5px)}
.app.surveyMode #surveyFavouriteRail{display:flex;flex-direction:column;gap:6px}
.surveyFavouriteHead{display:flex;align-items:center;gap:5px}.surveyFavouriteHead strong{flex:1;font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:#617184}.surveyFavouriteHead button{min-width:32px;min-height:30px;padding:4px 7px;background:#fff3cf;color:#6b4d00}
#surveyFavouriteButtons{display:flex;flex-direction:column;gap:5px;overflow-y:auto;overscroll-behavior:contain;scrollbar-width:thin}
.surveyFavouriteQuick{display:grid;grid-template-columns:16px minmax(0,1fr);align-items:center;gap:6px;width:100%;min-height:39px;padding:6px 7px!important;text-align:left;background:#edf2f7!important;border:1px solid #d8e1e9}
.surveyFavouriteQuick.active{background:#1c344f!important;color:#fff}.surveyFavouriteSwatch{width:14px;height:14px;border-radius:50%;background:var(--fav-color);box-shadow:0 0 0 1px #0002}.surveyFavouriteLabel{font-size:11px;font-weight:800;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.surveyFavouriteManageList{display:grid;gap:6px}.surveyFavouriteManageRow{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:6px}.surveyFavouriteManagePick{display:grid;grid-template-columns:18px minmax(0,1fr);gap:7px;align-items:center;text-align:left}.surveyFavouriteManagePick small{display:block;color:#6a7a8d;font-size:10px}.surveyFavouriteRemove{background:#fff0ee!important;color:#9f2f29!important;min-width:42px}
#saveSurveyFavourite,#saveSurveyFavouriteManager{background:#fff3cf;border:1px solid #ebd28a;color:#624900}
@media(max-width:600px){#surveyFavouriteRail{left:6px;top:6px;width:92px;max-height:calc(100% - 74px);padding:5px}.surveyFavouriteHead strong{font-size:9px}.surveyFavouriteQuick{min-height:35px;padding:5px!important;grid-template-columns:13px minmax(0,1fr)}.surveyFavouriteSwatch{width:11px;height:11px}.surveyFavouriteLabel{font-size:10px}}
"""
if '/* v0.40 — survey quick favourites. */' not in text:
    text = text.replace('</style>', rail_css + '\n</style>', 1)

text = replace_once(
    text,
    '<div class="canvasWrap" id="wrap"><canvas id="canvas"></canvas>',
    '<div class="canvasWrap" id="wrap"><aside id="surveyFavouriteRail" aria-label="Survey device favourites"><div class="surveyFavouriteHead"><strong>Favourites</strong><button id="surveyFavouriteManager" aria-haspopup="true" title="Manage survey favourites">★</button></div><div id="surveyFavouriteButtons"></div></aside><canvas id="canvas"></canvas>',
    'survey favourites rail'
)

# Add Beam and I/O devices.
text = replace_once(
    text,
    '<button data-symbol="beacon" data-symbol-scope="survey">Beacon</button><button data-symbol="repeater" data-symbol-scope="both">Repeater</button>',
    '<button data-symbol="beacon" data-symbol-scope="survey">Beacon</button><button data-symbol="beam" data-symbol-scope="survey">Beam detector</button><button data-symbol="io" data-symbol-scope="survey">I/O unit</button><button data-symbol="repeater" data-symbol-scope="both">Repeater</button>',
    'survey device buttons'
)
text = replace_once(
    text,
    '<option value="beacon">Beacon</option><option value="repeater">Repeater</option>',
    '<option value="beacon">Beacon</option><option value="beam">Beam detector</option><option value="io">I/O unit</option><option value="repeater">Repeater</option>',
    'property device choices'
)
text = replace_once(
    text,
    '<div id="symbolColors" class="colorbar"></div></div>',
    '<div id="symbolColors" class="colorbar"></div><div class="menuSep"></div><div class="menuRow"><button id="saveSurveyFavourite">☆ Save current to side</button></div><div id="surveyFavouriteHint" class="menuHint">Survey mode: pick a device, colour and size, then save it as a quick favourite.</div></div>',
    'save favourite button'
)

# Survey favourite manager popup.
manager_html = '<div id="surveyFavouriteMenu" class="toolPopup" aria-label="Survey device favourites"><h4>Survey favourites</h4><div class="menuRow"><button id="saveSurveyFavouriteManager">＋ Save current device</button></div><div id="surveyFavouriteManagerList" class="surveyFavouriteManageList"></div><div id="surveyFavouriteManagerCount" class="favouriteCount"></div><div class="holdHint">Up to 9 favourites. Each one remembers the device type, colour and size. Tap a side favourite to start placing it immediately.</div></div>\n'
if 'id="surveyFavouriteMenu"' not in text:
    marker = '<div id="settingsMenu" class="toolPopup" aria-label="Drawing settings">'
    if marker not in text:
        raise SystemExit('v0.40 patch marker missing: settings menu')
    text = text.replace(marker, manager_html + marker, 1)

# Device dictionaries and rendering.
text = replace_once(
    text,
    "const symbolNames={panel:'Panel',mcp:'MCP',smoke:'Smoke',heat:'Heat',sounder:'Sounder',beacon:'Beacon',repeater:'Repeater',you:'You are here'};",
    "const symbolNames={panel:'Panel',mcp:'MCP',smoke:'Smoke',heat:'Heat',sounder:'Sounder',beacon:'Beacon',beam:'Beam detector',io:'I/O unit',repeater:'Repeater',you:'You are here'};",
    'symbol names'
)
text = replace_once(
    text,
    "const zonePlanSymbolTypes=new Set(['panel','repeater','you']),surveyDeviceTypes=new Set(['panel','repeater','mcp','smoke','heat','sounder','beacon']);",
    "const zonePlanSymbolTypes=new Set(['panel','repeater','you']),surveyDeviceTypes=new Set(['panel','repeater','mcp','smoke','heat','sounder','beacon','beam','io']);",
    'survey device type set'
)
text = replace_once(
    text,
    "const r=Math.max(2,size),label={panel:'FAP',mcp:'MCP',smoke:'SD',heat:'HD',sounder:'S',beacon:'VAD',repeater:'REP',you:'YOU'}[type]||'?';",
    "const r=Math.max(2,size),label={panel:'FAP',mcp:'MCP',smoke:'SD',heat:'HD',sounder:'S',beacon:'VAD',beam:'BEAM',io:'I/O',repeater:'REP',you:'YOU'}[type]||'?';",
    'symbol labels'
)
text = replace_once(
    text,
    "if(type==='panel'||type==='mcp'||type==='repeater'){",
    "if(type==='panel'||type==='mcp'||type==='repeater'||type==='beam'||type==='io'){",
    'rectangular device symbols'
)
text = replace_once(
    text,
    "function countSymbols(list){const out={panel:0,mcp:0,smoke:0,heat:0,sounder:0,beacon:0,repeater:0,you:0};",
    "function countSymbols(list){const out={panel:0,mcp:0,smoke:0,heat:0,sounder:0,beacon:0,beam:0,io:0,repeater:0,you:0};",
    'device count object'
)
text = text.replace(
    "building={panel:0,mcp:0,smoke:0,heat:0,sounder:0,beacon:0,repeater:0,you:0}",
    "building={panel:0,mcp:0,smoke:0,heat:0,sounder:0,beacon:0,beam:0,io:0,repeater:0,you:0}"
)
text = text.replace(
    "const total={panel:0,repeater:0,mcp:0,smoke:0,heat:0,sounder:0,beacon:0,you:0}",
    "const total={panel:0,repeater:0,mcp:0,smoke:0,heat:0,sounder:0,beacon:0,beam:0,io:0,you:0}"
)
text = text.replace(
    "['panel','repeater','mcp','smoke','heat','sounder','beacon']",
    "['panel','repeater','mcp','smoke','heat','sounder','beacon','beam','io']"
)

# Let the old favourites catalogue know about the new survey devices too.
text = replace_once(
    text,
    "'symbol:beacon':{label:'Beacon',kind:'symbol',value:'beacon'},'symbol:panel':",
    "'symbol:beacon':{label:'Beacon',kind:'symbol',value:'beacon'},'symbol:beam':{label:'Beam detector',kind:'symbol',value:'beam'},'symbol:io':{label:'I/O unit',kind:'symbol',value:'io'},'symbol:panel':",
    'legacy favourites catalogue'
)

# Keep side-favourite active state in sync with device type, colour and scale.
text = replace_once(
    text,
    "function setSymbolStampScale(value){const v=Number(value);symbolStampScale=Number.isFinite(v)?Math.max(.10,Math.min(4,v)):1;try{localStorage.setItem('zoneSketchSymbolScale',String(symbolStampScale))}catch(e){}syncSymbolScale()}",
    "function setSymbolStampScale(value){const v=Number(value);symbolStampScale=Number.isFinite(v)?Math.max(.10,Math.min(4,v)):1;try{localStorage.setItem('zoneSketchSymbolScale',String(symbolStampScale))}catch(e){}syncSymbolScale();if(typeof syncSurveyDeviceFavouriteActive==='function')syncSurveyDeviceFavouriteActive()}",
    'symbol scale sync'
)
text = replace_once(
    text,
    "b.onclick=e=>{e.stopPropagation();symbolColor=color;renderSymbolColors()};",
    "b.onclick=e=>{e.stopPropagation();symbolColor=color;renderSymbolColors();if(typeof syncSurveyDeviceFavouriteActive==='function')syncSurveyDeviceFavouriteActive()};",
    'symbol colour sync'
)
text = replace_once(
    text,
    "function syncFavouriteActive(){document.querySelectorAll('.favouriteQuick').forEach(b=>{const item=favouriteCatalogue[b.dataset.favourite];b.classList.toggle('active',!!item&&favouriteIsActive(item))})}",
    "function syncFavouriteActive(){document.querySelectorAll('.favouriteQuick').forEach(b=>{const item=favouriteCatalogue[b.dataset.favourite];b.classList.toggle('active',!!item&&favouriteIsActive(item))});if(typeof syncSurveyDeviceFavouriteActive==='function')syncSurveyDeviceFavouriteActive()}",
    'favourite active sync'
)
text = replace_once(
    text,
    "syncToolMenus();renderFavourites()}",
    "syncToolMenus();renderFavourites();if(typeof renderSurveyDeviceFavourites==='function')renderSurveyDeviceFavourites()}",
    'mode UI favourites sync'
)

survey_favourites_js = r"""
const SURVEY_FAVOURITE_KEY='zoneSketchSurveyDeviceFavouritesV1',MAX_SURVEY_FAVOURITES=9;
let surveyDeviceFavourites=loadSurveyDeviceFavourites();
function normaliseSurveyDeviceFavourite(raw){if(!raw||!surveyDeviceTypes.has(raw.type))return null;const color=/^#[0-9a-f]{6}$/i.test(raw.color||'')?raw.color:'#172333',scale=Math.max(.10,Math.min(4,Number(raw.scale)||1));return{type:raw.type,color,scale}}
function loadSurveyDeviceFavourites(){try{const raw=JSON.parse(localStorage.getItem(SURVEY_FAVOURITE_KEY));if(Array.isArray(raw))return raw.map(normaliseSurveyDeviceFavourite).filter(Boolean).slice(0,MAX_SURVEY_FAVOURITES)}catch(e){}return[]}
function surveyFavouriteSame(a,b){return!!a&&!!b&&a.type===b.type&&String(a.color).toLowerCase()===String(b.color).toLowerCase()&&Math.abs((Number(a.scale)||1)-(Number(b.scale)||1))<.001}
function persistSurveyDeviceFavourites(){try{localStorage.setItem(SURVEY_FAVOURITE_KEY,JSON.stringify(surveyDeviceFavourites))}catch(e){}renderSurveyDeviceFavourites()}
function surveyFavouriteText(f){return symbolNames[f.type]||f.type}
function syncSurveyDeviceFavouriteActive(){document.querySelectorAll('.surveyFavouriteQuick').forEach((b,i)=>{const f=surveyDeviceFavourites[i];b.classList.toggle('active',!!f&&tool==='symbol'&&symbolStamp===f.type&&String(symbolColor).toLowerCase()===String(f.color).toLowerCase()&&Math.abs(symbolStampScale-f.scale)<.001)})}
function activateSurveyDeviceFavourite(index){const f=surveyDeviceFavourites[index];if(!f)return;symbolStamp=f.type;symbolColor=f.color;setSymbolStampScale(f.scale);renderSymbolColors();setTool('symbol');closeToolMenus();syncSurveyDeviceFavouriteActive();favouriteFeedback(surveyFavouriteText(f)+' ready')}
function addCurrentSurveyDeviceFavourite(){if(!surveyMode){favouriteFeedback('Switch to Survey mode to save a device favourite');return}const f=normaliseSurveyDeviceFavourite({type:symbolStamp,color:symbolColor,scale:symbolStampScale});if(!f){favouriteFeedback('Choose a survey device first');return}if(surveyDeviceFavourites.some(x=>surveyFavouriteSame(x,f))){favouriteFeedback('That device, colour and size is already saved');return}if(surveyDeviceFavourites.length>=MAX_SURVEY_FAVOURITES){favouriteFeedback('Maximum 9 survey favourites · remove one first');return}surveyDeviceFavourites.push(f);persistSurveyDeviceFavourites();favouriteFeedback(surveyFavouriteText(f)+' saved to the side')}
function removeSurveyDeviceFavourite(index){const f=surveyDeviceFavourites[index];if(!f)return;surveyDeviceFavourites.splice(index,1);persistSurveyDeviceFavourites();favouriteFeedback(surveyFavouriteText(f)+' removed')}
function renderSurveyDeviceFavourites(){const rail=$('surveyFavouriteButtons'),list=$('surveyFavouriteManagerList');if(!rail||!list)return;rail.textContent='';list.textContent='';surveyDeviceFavourites.forEach((f,index)=>{const b=document.createElement('button'),sw=document.createElement('span'),label=document.createElement('span');b.className='surveyFavouriteQuick';b.style.setProperty('--fav-color',f.color);b.title=surveyFavouriteText(f)+' · '+f.color+' · '+f.scale.toFixed(2)+'×';sw.className='surveyFavouriteSwatch';label.className='surveyFavouriteLabel';label.textContent=surveyFavouriteText(f);b.append(sw,label);b.onclick=()=>activateSurveyDeviceFavourite(index);rail.append(b);const row=document.createElement('div'),pick=document.createElement('button'),psw=document.createElement('span'),words=document.createElement('span'),name=document.createElement('strong'),meta=document.createElement('small'),remove=document.createElement('button');row.className='surveyFavouriteManageRow';pick.className='surveyFavouriteManagePick';psw.className='surveyFavouriteSwatch';psw.style.setProperty('--fav-color',f.color);name.textContent=surveyFavouriteText(f);meta.textContent=f.color.toUpperCase()+' · '+f.scale.toFixed(2)+'×';words.append(name,meta);pick.append(psw,words);pick.onclick=()=>activateSurveyDeviceFavourite(index);remove.className='surveyFavouriteRemove';remove.textContent='×';remove.title='Remove favourite';remove.onclick=e=>{e.stopPropagation();removeSurveyDeviceFavourite(index)};row.append(pick,remove);list.append(row)});$('surveyFavouriteManagerCount').textContent=surveyDeviceFavourites.length+' of '+MAX_SURVEY_FAVOURITES+' favourites';const hint=$('surveyFavouriteHint');if(hint)hint.textContent=surveyMode?(surveyDeviceFavourites.length+' of 9 saved · favourites remember device, colour and size'):'Survey mode only · switch to Survey to save device favourites';for(const id of ['saveSurveyFavourite','saveSurveyFavouriteManager'])if($(id))$(id).disabled=!surveyMode||surveyDeviceFavourites.length>=MAX_SURVEY_FAVOURITES;syncSurveyDeviceFavouriteActive()}
$('saveSurveyFavourite').onclick=e=>{e.stopPropagation();addCurrentSurveyDeviceFavourite()};
$('saveSurveyFavouriteManager').onclick=e=>{e.stopPropagation();addCurrentSurveyDeviceFavourite()};
$('surveyFavouriteManager').onclick=()=>{renderSurveyDeviceFavourites();if($('surveyFavouriteMenu').classList.contains('open'))closeToolMenus();else placeMenuBelow($('surveyFavouriteMenu'),$('surveyFavouriteManager'))};
renderSurveyDeviceFavourites();
"""
needle = "document.querySelectorAll('[data-menu-tool],[data-symbol],[data-detail-tool]').forEach(bindFavouriteHold);$('favouriteMenuBtn').onclick=()=>toggleMenu($('favouriteMenu'),$('favouriteMenuBtn'));$('resetFavourites').onclick=()=>{favourites=[...defaultFavourites];saveFavourites();favouriteFeedback('Default favourites restored')};renderFavourites();\nfunction syncSurveyTools()"
if 'SURVEY_FAVOURITE_KEY' not in text:
    if needle not in text:
        raise SystemExit('v0.40 patch marker missing: favourites JS')
    text = text.replace(needle, needle.replace('\nfunction syncSurveyTools()', '\n') + survey_favourites_js + '\nfunction syncSurveyTools()', 1)

# Keep manager render current when switching modes.
text = replace_once(
    text,
    "if(surveyMode){symbolStamp='smoke';setTool('symbol')}renderDeviceCounts();draw()}",
    "if(surveyMode){symbolStamp='smoke';setTool('symbol')}renderSurveyDeviceFavourites();renderDeviceCounts();draw()}",
    'survey mode refresh'
)

# Write source copies in sync.
MAIN.write_text(text)
for target in [Path('ZoneSketch.html'), Path('Zone-Sketch-by-Will.html'), Path('app/src/main/assets/index.html')]:
    target.write_text(text)

# Android version.
gradle = Path('app/build.gradle')
g = gradle.read_text()
g = g.replace('versionCode 40', 'versionCode 41')
g = g.replace("versionName '0.39.1'", "versionName '0.40'")
gradle.write_text(g)

# Future generic builds should run the new regression test.
wf = Path('.github/workflows/build-apk.yml')
w = wf.read_text()
marker = '          node tests/survey-edit-zoom.cjs\n'
if 'node tests/survey-favourites-v040.cjs' not in w:
    if marker not in w:
        raise SystemExit('v0.40 patch marker missing: generic workflow tests')
    w = w.replace(marker, marker + '          node tests/survey-favourites-v040.cjs\n', 1)
    wf.write_text(w)

print('Applied v0.40: smaller grid, Beam/I-O devices and 9 colour/size survey favourites')
