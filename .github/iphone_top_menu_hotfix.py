from pathlib import Path

APP_COPIES = [
    Path('index.html'),
    Path('ZoneSketch.html'),
    Path('Zone-Sketch-by-Will.html'),
    Path('app/src/main/assets/index.html'),
]

source = APP_COPIES[0]
text = source.read_text(encoding='utf-8')

old_button = '<button class="iconBtn" id="topCollapseBtn" aria-label="Collapse top controls" title="Collapse top controls">▲</button>'
new_button = '<button class="iconBtn" id="topCollapseBtn" aria-label="Close menu" title="Close menu">Close ▲</button>'
if old_button in text:
    text = text.replace(old_button, new_button, 1)
elif new_button not in text:
    raise SystemExit('Could not find the expected top menu button markup')

old_sync = "b.textContent=topSectionOpen?'▲':'Menu ▼';b.title=topSectionOpen?'Collapse top controls':'Show menu';"
new_sync = "b.textContent=topSectionOpen?'Close ▲':'Menu ▼';b.title=topSectionOpen?'Close menu':'Show menu';"
if old_sync in text:
    text = text.replace(old_sync, new_sync, 1)
elif new_sync not in text:
    raise SystemExit('Could not find the expected top menu sync logic')

css_marker = '/* iPhone top menu close control */'
css = '''/* iPhone top menu close control */
@media(max-width:720px){
  .app>.top #topCollapseBtn{
    min-width:88px;
    min-height:44px;
    padding-inline:12px;
    white-space:nowrap;
    flex:0 0 auto;
    font-size:15px;
    font-weight:800;
    touch-action:manipulation;
  }
}
'''
if css_marker not in text:
    anchor = '.app .saveIndicator{'
    if anchor not in text:
        raise SystemExit('Could not find the theme anchor for the iPhone menu CSS')
    text = text.replace(anchor, css + anchor, 1)

for path in APP_COPIES:
    path.write_text(text, encoding='utf-8')

print('Applied iPhone top-menu close-control hotfix and synced all app copies.')
