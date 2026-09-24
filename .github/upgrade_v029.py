from pathlib import Path

ROOT = Path('.')
html_paths = [
    ROOT/'index.html',
    ROOT/'ZoneSketch.html',
    ROOT/'Zone-Sketch-by-Will.html',
    ROOT/'app/src/main/assets/index.html',
]

text = html_paths[0].read_text()
if 'v0.28' not in text:
    raise SystemExit('v0.29 expected v0.28 HTML baseline was not found')

css = r'''

/* v0.29 — keep zone cards fully visible inside the locked viewport. */
#zoneSide{display:flex;flex-direction:column;min-height:0;overflow:hidden}
#zoneSide .sideHead{flex:0 0 auto}
#zoneSide .zoneList{flex:1 1 auto;min-height:58px;overflow-y:auto;overflow-x:hidden;padding:2px 1px 8px;-webkit-overflow-scrolling:touch}
#zoneSide .help{flex:0 0 auto;margin-bottom:0}
@media(max-height:700px){#zoneSide .help{display:none}}
@media(max-width:720px){
  #zoneSide{height:118px;min-height:118px;flex:0 0 118px;width:100%;padding:6px 8px;overflow:hidden}
  #zoneSide .sideHead{height:26px;min-height:26px}
  #zoneSide .zoneList{display:flex;flex:1 1 auto;min-height:58px;gap:7px;overflow-x:auto;overflow-y:hidden;padding:2px 0 5px}
  #zoneSide .zone{width:170px;min-width:170px;height:54px;min-height:54px;margin:0}
  #zoneSide .help{display:none}
  .workspace.zonesClosed #zoneSide{height:36px;min-height:36px;flex:0 0 36px;padding:3px 6px}
}
@media(max-width:720px) and (max-height:520px){
  #zoneSide{height:96px;min-height:96px;flex-basis:96px}
  #zoneSide .zoneList{min-height:52px}
  #zoneSide .zone{height:50px;min-height:50px}
  .workspace.zonesClosed #zoneSide{height:36px;min-height:36px;flex-basis:36px}
}
'''

if 'v0.29 — keep zone cards fully visible' not in text:
    if '</style>' not in text:
        raise SystemExit('v0.29 could not find closing style tag')
    text = text.replace('</style>', css + '\n</style>', 1)

# Only update the user-visible release labels. Keep the v0.28 viewport-lock
# comments intact so the regression guard can prove that fix is still present.
old_title = '<title>Zone Sketch by Will v0.28 — site survey draft</title>'
new_title = '<title>Zone Sketch by Will v0.29 — site survey draft</title>'
old_home = 'ON SITE ZONE PLANNER · v0.28'
new_home = 'ON SITE ZONE PLANNER · v0.29'
if old_title not in text or old_home not in text:
    raise SystemExit('v0.29 could not find the v0.28 visible version labels')
text = text.replace(old_title, new_title, 1)
text = text.replace(old_home, new_home, 1)

for path in html_paths:
    path.write_text(text)

build = ROOT/'app/build.gradle'
b = build.read_text()
if 'versionCode 28' not in b or "versionName '0.28'" not in b:
    raise SystemExit('v0.29 expected Android v0.28 baseline was not found')
b = b.replace('versionCode 28', 'versionCode 29', 1)
b = b.replace("versionName '0.28'", "versionName '0.29'", 1)
build.write_text(b)

print('Applied v0.29 zones panel visibility and responsive zone-list hotfix')
