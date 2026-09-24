from pathlib import Path

ROOT = Path('.')
html_paths = [
    ROOT/'index.html',
    ROOT/'ZoneSketch.html',
    ROOT/'Zone-Sketch-by-Will.html',
    ROOT/'app/src/main/assets/index.html',
]

text = html_paths[0].read_text()
if 'Zone Sketch by Will v0.33' not in text:
    raise SystemExit('v0.34 expected v0.33 HTML baseline was not found')

old_menu = '<div id="symbolMenu" class="toolPopup" aria-label="Favourite symbols"><h4>Symbol favourites</h4><div class="symbolGrid"><button data-symbol="panel">Panel</button><button data-symbol="mcp">MCP</button><button data-symbol="smoke">Smoke</button><button data-symbol="heat">Heat</button><button data-symbol="sounder">Sounder</button><button data-symbol="beacon">Beacon</button><button data-symbol="repeater">Repeater</button><button data-symbol="you">You are here</button></div><div class="menuHint">Tap-to-repeat: choose a symbol once, then stamp as many positions as you need.</div><div class="menuSep"></div><h4>Symbol colour</h4><div id="symbolColors" class="colorbar"></div></div>'
new_menu = '<div id="symbolMenu" class="toolPopup" aria-label="Favourite symbols"><h4>Symbol favourites</h4><div class="symbolGrid"><button data-symbol="panel">Panel</button><button data-symbol="mcp">MCP</button><button data-symbol="smoke">Smoke</button><button data-symbol="heat">Heat</button><button data-symbol="sounder">Sounder</button><button data-symbol="beacon">Beacon</button><button data-symbol="repeater">Repeater</button><button data-symbol="you">You are here</button></div><div class="menuHint">Tap-to-repeat: choose a symbol once, then stamp as many positions as you need.</div><div class="menuSep"></div><h4>Symbol size</h4><label class="symbolSizeLine"><span>Size</span><input id="symbolStampScale" type="range" min="0.25" max="4" step="0.05" value="1" aria-label="New symbol size"><output id="symbolStampScaleValue">1.00×</output></label><div class="menuHint">Sets the size of new symbols. Symbols already on the plan keep their current size.</div><div class="menuSep"></div><h4>Symbol colour</h4><div id="symbolColors" class="colorbar"></div></div>'
if old_menu not in text:
    raise SystemExit('v0.34 could not find Symbols menu')
text = text.replace(old_menu, new_menu, 1)

css_anchor = '.symbolGrid{display:grid;grid-template-columns:1fr 1fr;gap:6px}.symbolGrid button{display:flex;gap:7px;align-items:center;text-align:left}.symbolGrid canvas{width:30px;height:30px}'
css_new = css_anchor + '.symbolSizeLine{display:grid;grid-template-columns:38px 1fr 48px;align-items:center;gap:8px;padding:4px 5px 6px;font-size:12px;font-weight:750}.symbolSizeLine input[type=range]{width:100%;accent-color:#ec493b}.symbolSizeLine output{text-align:right;color:#53667b;font-variant-numeric:tabular-nums}'
if css_anchor not in text:
    raise SystemExit('v0.34 could not find symbol grid CSS')
text = text.replace(css_anchor, css_new, 1)

old_vars = "roomStamp='Office',symbolStamp='smoke',symbolColor='#172333',pendingPhotoPin=null"
new_vars = "roomStamp='Office',symbolStamp='smoke',symbolColor='#172333',symbolStampScale=loadSymbolScale(),pendingPhotoPin=null"
if old_vars not in text:
    raise SystemExit('v0.34 could not find symbol stamp variables')
text = text.replace(old_vars, new_vars, 1)

state_anchor = "function ensureUiState(){state.locks={...defaultLocks(),...(state.locks||{})};state.layers={...defaultLayers(),...(state.layers||{})}}"
state_new = state_anchor + "\nfunction loadSymbolScale(){try{const v=Number(localStorage.getItem('zoneSketchSymbolScale'));if(Number.isFinite(v)&&v>=.25&&v<=4)return v}catch(e){}return 1}\nfunction syncSymbolScale(){const input=$('symbolStampScale'),out=$('symbolStampScaleValue');if(!input||!out)return;input.value=String(symbolStampScale);out.textContent=symbolStampScale.toFixed(2)+'×'}\nfunction setSymbolStampScale(value){const v=Number(value);symbolStampScale=Number.isFinite(v)?Math.max(.25,Math.min(4,v)):1;try{localStorage.setItem('zoneSketchSymbolScale',String(symbolStampScale))}catch(e){}syncSymbolScale()}"
if state_anchor not in text:
    raise SystemExit('v0.34 could not find UI state anchor')
text = text.replace(state_anchor, state_new, 1)

old_menu_click = "$('symbolMenuBtn').onclick=()=>toggleMenu($('symbolMenu'),$('symbolMenuBtn'));"
new_menu_click = "$('symbolMenuBtn').onclick=()=>{syncSymbolScale();toggleMenu($('symbolMenu'),$('symbolMenuBtn'))};$('symbolStampScale').oninput=e=>{e.stopPropagation();setSymbolStampScale(e.target.value)};"
if old_menu_click not in text:
    raise SystemExit('v0.34 could not find Symbols menu click handler')
text = text.replace(old_menu_click, new_menu_click, 1)

old_survey = "$('surveyDevice').onclick=()=>toggleMenu($('symbolMenu'),$('surveyDevice'));"
new_survey = "$('surveyDevice').onclick=()=>{syncSymbolScale();toggleMenu($('symbolMenu'),$('surveyDevice'))};"
if old_survey not in text:
    raise SystemExit('v0.34 could not find Survey device handler')
text = text.replace(old_survey, new_survey, 1)

old_place = "state.symbols.push({id:uid(),...inputPoint(e.clientX,e.clientY),type:symbolStamp,color:symbolColor,scale:1,rotation:0,group:null})"
new_place = "state.symbols.push({id:uid(),...inputPoint(e.clientX,e.clientY),type:symbolStamp,color:symbolColor,scale:symbolStampScale,rotation:0,group:null})"
if old_place not in text:
    raise SystemExit('v0.34 could not find symbol placement')
text = text.replace(old_place, new_place, 1)

old_init = 'ensureUiState();renderFloors();renderSymbolColors();renderLockMenu();renderLayersMenu();renderDeviceCounts();syncMoveMode();'
new_init = 'ensureUiState();renderFloors();renderSymbolColors();syncSymbolScale();renderLockMenu();renderLayersMenu();renderDeviceCounts();syncMoveMode();'
if old_init not in text:
    raise SystemExit('v0.34 could not find app initialization')
text = text.replace(old_init, new_init, 1)

marker = "\n\n/* v0.34 — Symbols menu controls the default size of newly stamped symbols. */\n"
if 'v0.34 — Symbols menu controls the default size' not in text:
    text = text.replace('</style>', marker + '</style>', 1)

text = text.replace('<title>Zone Sketch by Will v0.33 — site survey draft</title>', '<title>Zone Sketch by Will v0.34 — site survey draft</title>', 1)
text = text.replace('ON SITE ZONE PLANNER · v0.33', 'ON SITE ZONE PLANNER · v0.34', 1)

for path in html_paths:
    path.write_text(text)

build = ROOT/'app/build.gradle'
b = build.read_text()
if 'versionCode 33' not in b or "versionName '0.33'" not in b:
    raise SystemExit('v0.34 expected Android v0.33 baseline was not found')
b = b.replace('versionCode 33', 'versionCode 34', 1)
b = b.replace("versionName '0.33'", "versionName '0.34'", 1)
build.write_text(b)

print('Applied v0.34: Symbols menu size slider for newly stamped symbols')
