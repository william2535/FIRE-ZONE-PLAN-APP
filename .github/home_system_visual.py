from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

HOME_ACTIONS = '<div class="homeActions"><button id="homeNew" class="primary" disabled>Make a new plan</button><button id="homeImport" disabled>Import backup</button></div>'
if HOME_ACTIONS not in html:
    raise SystemExit('Expected Home actions were not found; refusing to alter Home.')

# Keep the requested order fixed: Fire, Intruder, CCTV, Access Control.
start = html.find('<div class="homeSystemPreview"')
end = html.find('</div></div><div class="homeHeading">', start)
if start < 0 or end < 0:
    raise SystemExit('Existing Home system preview was not found on the latest build.')

preview = '''<div class="homeSystemPreview" aria-label="Zone Sketch system range preview">
<div class="homeSystemTile homeSystemFire isSelected"><img src="assets/zone-sketch-fire-icon.svg" alt=""><span><b>Fire</b><small>Selected</small></span></div>
<div class="homeSystemTile isFuture" aria-disabled="true"><img src="assets/zone-sketch-intruder-icon.svg" alt=""><span><b>Intruder</b><small>Future</small></span></div>
<div class="homeSystemTile isFuture" aria-disabled="true"><img src="assets/zone-sketch-cctv-icon.svg" alt=""><span><b>CCTV</b><small>Future</small></span></div>
<div class="homeSystemTile isFuture" aria-disabled="true"><img src="assets/zone-sketch-access-icon.svg" alt=""><span><b>Access control</b><small>Future</small></span></div>
'''
html = html[:start] + preview + html[end:]

MARKER = '/* Home system artwork v2 — keep icons fully coloured; future text only is muted. */'
if MARKER not in html:
    css = r'''
/* Home system artwork v2 — keep icons fully coloured; future text only is muted. */
#projectsHome .homeSystemTile.isFuture{opacity:1!important;filter:none!important;background:linear-gradient(145deg,#0d2838,#071923)!important;border-color:#2b596f!important;box-shadow:inset 0 1px rgba(255,255,255,.025)!important}
#projectsHome .homeSystemTile.isFuture img{filter:none!important;opacity:1!important}
#projectsHome .homeSystemTile.isFuture b,#projectsHome .homeSystemTile.isFuture small{color:#7896a6!important;opacity:.72}
#projectsHome .homeSystemTile img{border-radius:0!important}
#projectsHome .homeSystemTile.homeSystemFire.isSelected img{filter:none!important;opacity:1!important}
'''
    html = html.replace('</style>', css + '\n</style>', 1)

for asset in ('zone-sketch-fire-icon.svg','zone-sketch-intruder-icon.svg','zone-sketch-cctv-icon.svg','zone-sketch-access-icon.svg'):
    if asset not in html:
        raise SystemExit(f'Missing requested system asset: {asset}')
if HOME_ACTIONS not in html:
    raise SystemExit('Home controls changed unexpectedly.')

path.write_text(html, encoding='utf-8')
print('Applied coloured system assets in Fire / Intruder / CCTV / Access Control order.')
