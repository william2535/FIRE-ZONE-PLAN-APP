from pathlib import Path
import re

paths = [Path('index.html'), Path('ZoneSketch.html'), Path('app/src/main/assets/index.html')]
p = paths[0]
s = p.read_text(encoding='utf-8')

# CSS: replace old all-or-nothing zones collapse and add compact top/side chrome.
s = s.replace('.workspace.zonesClosed .side{display:none}', '.workspace.zonesClosed .side{width:42px;padding:8px 4px;overflow:hidden}.workspace.zonesClosed .sideHead{justify-content:flex-end}.workspace.zonesClosed .sideHead h3,.workspace.zonesClosed .zoneList,.workspace.zonesClosed .help{display:none}.workspace.zonesClosed .sideHead button{margin-left:auto}')

css_extra = '''
.topMain{display:flex;gap:8px;align-items:center;flex-wrap:wrap;flex:1;min-width:0}.topEssential{display:flex;gap:8px;align-items:center;margin-left:auto;flex:none}.topEssential .iconBtn{min-width:42px}.top.collapsed{padding:calc(5px + env(safe-area-inset-top)) 8px 5px;min-height:48px}.top.collapsed .topMain{display:none}.top.collapsed .topEssential{width:100%;justify-content:flex-end}.top #topCollapseBtn{font-size:15px}.app.topClosed #floorBar,.app.topClosed #backgroundBar{display:none!important}.sideHead button{margin-left:auto}.workspace.zonesClosed .sideHead{width:100%}
@media(max-width:720px){.topMain{gap:6px}.topEssential{gap:6px}.top.collapsed .topEssential{width:100%}.workspace.zonesClosed .side{display:block;width:100%;height:36px;padding:3px 6px;border-top:1px solid #ccd8e2}.workspace.zonesClosed .sideHead{height:100%;align-items:center;justify-content:flex-end}.workspace.zonesClosed .sideHead button{margin-left:auto}.workspace.zonesClosed .zoneList{display:none}}
'''
if '.topMain{display:flex' not in s:
    s = s.replace('</style>', css_extra + '</style>')

# Rebuild header so only Move/Delete/Undo/Redo + collapse arrow are permanent.
new_header = '''<header class="top" id="topBar"><div class="topMain" id="topMain"><div class="brand">ZONE SKETCH<small>ON-SITE DRAFT</small></div><input id="site" placeholder="Site / building name" aria-label="Site name"><div class="spacer"></div><button id="importBtn">Import plan</button><button id="newBtn">New</button><button id="blankBtn">Blank this floor</button><button id="locksMenuBtn">Locks</button><button id="layersMenuBtn">Layers</button><button id="countsMenuBtn">Devices · 0</button><button id="gridBtn">Grid off</button><button id="snapGridBtn">Snap off</button><label class="wallControl" title="Grid spacing on the plan">Grid <input id="gridSize" type="range" min="20" max="250" step="10" value="100"><output id="gridSizeValue">100</output></label><label class="wallControl" title="Building wall line thickness">Wall <input id="wallSize" type="range" min="0.75" max="5" step="0.25" value="3"><output id="wallSizeValue">3.00</output></label><button class="primary" id="shareBtn">Send to office</button></div><div class="topEssential" id="topEssential"><button id="moveModeTop" title="When on, the canvas only pans/zooms and cannot edit">Move OFF</button><button class="iconBtn" id="deleteTop" data-tool="erase" aria-label="Delete" title="Delete">⌫</button><button class="iconBtn" id="undoTop" aria-label="Undo" title="Undo">↶</button><button class="iconBtn" id="redoTop" aria-label="Redo" title="Redo">↷</button><button class="iconBtn" id="topCollapseBtn" aria-label="Collapse top controls" title="Collapse top controls">▲</button></div></header><button id="zonesPanelBtn" hidden aria-hidden="true"></button>'''
s, n = re.subn(r'<header class="top">.*?</header>', new_header, s, count=1, flags=re.S)
if n != 1:
    raise SystemExit('Could not replace top header')

# Zones collapse now leaves a slim edge rail and the arrow itself toggles both ways.
old_block = re.compile(r"let zonesPanelOpen=true;function syncZonesPanel\(\)\{.*?syncZonesPanel\(\);syncMoveMode\(\);", re.S)
new_block = """let zonesPanelOpen=true;function syncZonesPanel(){const workspace=$('workspace'),b=$('closeZones'),legacy=$('zonesPanelBtn');workspace.classList.toggle('zonesClosed',!zonesPanelOpen);b.textContent=zonesPanelOpen?'‹':'›';b.title=zonesPanelOpen?'Hide Zones panel':'Show Zones panel';b.setAttribute('aria-label',b.title);b.setAttribute('aria-expanded',zonesPanelOpen?'true':'false');if(legacy){legacy.textContent=zonesPanelOpen?'Zones ◀':'Zones ▶';legacy.setAttribute('aria-pressed',zonesPanelOpen?'true':'false')}requestAnimationFrame(draw)}function setZonesPanel(open){zonesPanelOpen=!!open;syncZonesPanel()}$('closeZones').onclick=()=>setZonesPanel(!zonesPanelOpen);if($('zonesPanelBtn'))$('zonesPanelBtn').onclick=()=>setZonesPanel(!zonesPanelOpen);let topSectionOpen=true;function syncTopSection(){const app=document.querySelector('.app'),top=$('topBar'),b=$('topCollapseBtn');app.classList.toggle('topClosed',!topSectionOpen);top.classList.toggle('collapsed',!topSectionOpen);b.textContent=topSectionOpen?'▲':'▼';b.title=topSectionOpen?'Collapse top controls':'Show top controls';b.setAttribute('aria-label',b.title);b.setAttribute('aria-expanded',topSectionOpen?'true':'false');requestAnimationFrame(draw)}function setTopSection(open){topSectionOpen=!!open;closeToolMenus();syncTopSection()}$('topCollapseBtn').onclick=()=>setTopSection(!topSectionOpen);$('moveModeTop').onclick=()=>setMoveMode(!navMode);$('moveModeBottom').onclick=()=>setMoveMode(!navMode);syncZonesPanel();syncTopSection();syncMoveMode();"""
s, n = old_block.subn(new_block, s, count=1)
if n != 1:
    raise SystemExit('Could not replace zones/top collapse JS block')

# Explicit edit tool selection exits navigation mode, so permanent Delete is immediately usable.
old_tools = "document.querySelectorAll('[data-tool]').forEach(b=>b.onclick=()=>setTool(b.dataset.tool));"
new_tools = "document.querySelectorAll('[data-tool]').forEach(b=>b.onclick=()=>{if(navMode)setMoveMode(false);setTool(b.dataset.tool)});"
if old_tools not in s:
    raise SystemExit('Could not find data-tool handler')
s = s.replace(old_tools, new_tools, 1)

# Ensure the zone arrow is the only visible thing in the rail when closed.
if 'id="closeZones"' not in s:
    raise SystemExit('closeZones control missing')

for out in paths:
    out.write_text(s, encoding='utf-8')

print('Zone Sketch v0.16 collapsible chrome applied')
