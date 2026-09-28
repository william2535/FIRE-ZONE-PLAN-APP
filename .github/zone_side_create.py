from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
original = text

old_side = '<aside class="side" id="zoneSide"><div class="sideHead"><h3>Zones</h3><button id="closeZones" aria-label="Hide Zones panel" title="Hide Zones panel">‹</button></div><div id="zones" class="zoneList"></div>'
new_side = '<aside class="side" id="zoneSide"><div class="sideHead"><h3>Zones</h3><button id="sideZoneCreate" class="sideZoneCreate" type="button" aria-label="Add zone" title="Add zone">＋ Zone</button><button id="closeZones" aria-label="Hide Zones panel" title="Hide Zones panel">‹</button></div><div id="zones" class="zoneList"></div>'

if 'id="sideZoneCreate"' not in text:
    if old_side not in text:
        raise SystemExit('Zone side-panel markup anchor not found')
    text = text.replace(old_side, new_side, 1)

handler_anchor = "$('zoneCreate').onclick=()=>{closeToolMenus();openModal()};"
handler = handler_anchor + "if($('sideZoneCreate'))$('sideZoneCreate').onclick=()=>{closeToolMenus();openModal()};"
if "$('sideZoneCreate').onclick" not in text:
    if handler_anchor not in text:
        raise SystemExit('Zone-create handler anchor not found')
    text = text.replace(handler_anchor, handler, 1)

# Selecting a zone from the side list should immediately arm the existing room
# Fill Area tool. The bottom Zone menu remains the manual/custom shape workflow.
side_pick_old = "else{selected=z.id;renderZones();draw()}"
side_pick_new = "else{selected=z.id;renderZones();setTool('fill')}"
if side_pick_old in text:
    text = text.replace(side_pick_old, side_pick_new, 1)
elif side_pick_new not in text:
    raise SystemExit('Side-panel zone selection anchor not found')

CSS_START = '/* Zone side-panel add action. */'
CSS = r'''
/* Zone side-panel add action. */
#sideZoneCreate{
  margin-left:auto;
  margin-right:4px;
  padding:6px 9px;
  min-height:30px;
  border:1px solid rgba(0,194,255,.28);
  background:linear-gradient(145deg,#eef8fc,#e8f3f8);
  color:#18536e;
  font-size:11px;
  font-weight:800;
  letter-spacing:.02em;
  white-space:nowrap;
}
#sideZoneCreate:active{transform:translateY(1px)}
.workspace.zonesClosed #sideZoneCreate,.app.surveyMode #sideZoneCreate{display:none!important}
@media(max-width:720px){
  #sideZoneCreate{padding:4px 8px;min-height:24px;font-size:10px;margin-right:3px}
}
/* End zone side-panel add action. */
'''.strip()

if CSS_START not in text:
    if '</style>' not in text:
        raise SystemExit('Closing style tag not found')
    text = text.replace('</style>', CSS + '\n</style>', 1)

if text != original:
    p.write_text(text, encoding='utf-8')
    print('index.html: side-panel zone selection now arms Fill Area')
else:
    print('index.html: side-panel Zone action and auto-fill selection already current')
