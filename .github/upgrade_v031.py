from pathlib import Path

ROOT = Path('.')
html_paths = [
    ROOT/'index.html',
    ROOT/'ZoneSketch.html',
    ROOT/'Zone-Sketch-by-Will.html',
    ROOT/'app/src/main/assets/index.html',
]

text = html_paths[0].read_text()
if 'Zone Sketch by Will v0.30' not in text:
    raise SystemExit('v0.31 expected v0.30 HTML baseline was not found')

# v0.30 accidentally hid the existing Zones sidebar while adding wall-aware
# Zone Box snapping. Restore the original v0.29 sidebar/collapse behaviour while
# leaving all of the v0.30 snapping code intact.
old_css = r'''

/* v0.30 — full-canvas zone workflow: no permanent Zones side/bottom barrier. */
#zoneSide{display:none!important}
#zonesPanelBtn,#closeZones{display:none!important}
.workspace{width:100%}
.canvasWrap{width:100%;flex:1 1 auto}
'''
if old_css not in text:
    raise SystemExit('v0.31 could not find the v0.30 Zones-hiding CSS')
text = text.replace(old_css, '\n\n/* v0.31 — restore the collapsible Zones sidebar; keep v0.30 wall snapping. */\n', 1)

# Visible release strings only. Historical comments stay unchanged.
text = text.replace('<title>Zone Sketch by Will v0.30 — site survey draft</title>', '<title>Zone Sketch by Will v0.31 — site survey draft</title>', 1)
text = text.replace('ON SITE ZONE PLANNER · v0.30', 'ON SITE ZONE PLANNER · v0.31', 1)

for path in html_paths:
    path.write_text(text)

build = ROOT/'app/build.gradle'
b = build.read_text()
if 'versionCode 30' not in b or "versionName '0.30'" not in b:
    raise SystemExit('v0.31 expected Android v0.30 baseline was not found')
b = b.replace('versionCode 30', 'versionCode 31', 1)
b = b.replace("versionName '0.30'", "versionName '0.31'", 1)
build.write_text(b)

print('Applied v0.31: restored Zones sidebar and retained wall-snapping Zone Box')
