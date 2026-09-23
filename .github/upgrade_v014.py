from pathlib import Path

paths = [Path('index.html'), Path('ZoneSketch.html'), Path('app/src/main/assets/index.html')]
s = paths[0].read_text()


def replace_one(old, new, label):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly 1 match, found {count}')
    s = s.replace(old, new, 1)

# Add compact controls for collapsing/reopening the Zones sidebar.
replace_one(
    ".side h3{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:#66788c;margin:14px 0 8px}",
    ".side h3{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:#66788c;margin:14px 0 8px}.sideHead{display:flex;align-items:center;gap:8px}.sideHead h3{flex:1}.sideHead button{padding:5px 9px;background:#e8eef5;color:#38506a;font-size:18px;line-height:1}.workspace.zonesClosed .side{display:none}",
    'zones panel css',
)

replace_one(
    '<button id="blankBtn">Blank this floor</button><button id="gridBtn">Grid off</button>',
    '<button id="blankBtn">Blank this floor</button><button id="zonesPanelBtn" title="Show or hide the Zones panel">Zones ◀</button><button id="gridBtn">Grid off</button>',
    'top zones toggle',
)

replace_one(
    '<div class="workspace"><aside class="side"><h3>Zones</h3><div id="zones" class="zoneList"></div>',
    '<div class="workspace" id="workspace"><aside class="side" id="zoneSide"><div class="sideHead"><h3>Zones</h3><button id="closeZones" aria-label="Hide Zones panel" title="Hide Zones panel">‹</button></div><div id="zones" class="zoneList"></div>',
    'zones sidebar header',
)

needle = "document.querySelectorAll('[data-tool]').forEach(b=>b.onclick=()=>setTool(b.dataset.tool));document.querySelectorAll('[data-menu-tool]').forEach(b=>b.onclick=()=>setTool(b.dataset.menuTool));"
insert = "let zonesPanelOpen=true;function syncZonesPanel(){const workspace=$('workspace'),b=$('zonesPanelBtn');workspace.classList.toggle('zonesClosed',!zonesPanelOpen);b.classList.toggle('active',zonesPanelOpen);b.textContent=zonesPanelOpen?'Zones ◀':'Zones ▶';b.setAttribute('aria-pressed',zonesPanelOpen?'true':'false');requestAnimationFrame(draw)}function setZonesPanel(open){zonesPanelOpen=!!open;syncZonesPanel()}$('zonesPanelBtn').onclick=()=>setZonesPanel(!zonesPanelOpen);$('closeZones').onclick=()=>setZonesPanel(false);syncZonesPanel();\n" + needle
replace_one(needle, insert, 'zones panel behaviour')

for marker in ['id="zonesPanelBtn"', 'id="closeZones"', 'id="workspace"', 'function syncZonesPanel', 'workspace.zonesClosed']:
    if marker not in s:
        raise SystemExit(f'missing v0.14 marker: {marker}')

for p in paths:
    p.write_text(s)
