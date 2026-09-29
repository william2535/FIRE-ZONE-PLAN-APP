from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

HOME_ACTIONS = '<div class="homeActions"><button id="homeNew" class="primary" disabled>Make a new plan</button><button id="homeImport" disabled>Import backup</button></div>'
if HOME_ACTIONS not in html:
    raise SystemExit('Expected Home actions were not found; refusing to alter Home.')

start = html.find('<div class="homeSystemPreview"')
end = html.find('</div></div><div class="homeHeading">', start)
if start < 0 or end < 0:
    raise SystemExit('Existing Home system preview was not found on the latest build.')

preview = '''<div class="homeSystemPreview" aria-label="Zone Sketch system range preview">
<div class="homeSystemTile homeSystemFire isSelected" aria-current="true"><img src="assets/home-system-fire.webp" alt=""><span><b>Fire</b><small>Selected</small></span></div>
<div class="homeSystemTile isFuture" aria-disabled="true"><img src="assets/home-system-intruder.webp" alt=""><span><b>Intruder</b><small>Future</small></span></div>
<div class="homeSystemTile isFuture" aria-disabled="true"><img src="assets/home-system-access-control.webp" alt=""><span><b>Access Control</b><small>Future</small></span></div>
<div class="homeSystemTile isFuture" aria-disabled="true"><img src="assets/home-system-cctv.webp" alt=""><span><b>CCTV</b><small>Future</small></span></div>
'''
html = html[:start] + preview + html[end:]

RASTER_MARKER = '/* Approved supplied Home system artwork — icons stay fully coloured; future text only is muted. */'
if RASTER_MARKER not in html:
    css = r'''
/* Approved supplied Home system artwork — icons stay fully coloured; future text only is muted. */
#projectsHome .homeSystemTile img{filter:none!important;opacity:1!important;object-fit:contain!important;image-rendering:auto!important}
#projectsHome .homeSystemTile.isFuture{opacity:1!important;filter:none!important;background:linear-gradient(145deg,#0d2838,#071923)!important;border-color:#2b596f!important;box-shadow:inset 0 1px rgba(255,255,255,.025)!important}
#projectsHome .homeSystemTile.isFuture img{filter:none!important;opacity:1!important}
#projectsHome .homeSystemTile.isFuture b,#projectsHome .homeSystemTile.isFuture small{color:#7896a6!important;opacity:.72!important}
#projectsHome .homeSystemTile.homeSystemFire.isSelected img{filter:none!important;opacity:1!important}
'''
    html = html.replace('</style>', css + '\n</style>', 1)

expected = (
    'assets/home-system-fire.webp',
    'assets/home-system-intruder.webp',
    'assets/home-system-access-control.webp',
    'assets/home-system-cctv.webp',
)
positions = [html.find(asset, start) for asset in expected]
if any(pos < 0 for pos in positions) or positions != sorted(positions):
    raise SystemExit('Approved Home system assets are missing or out of order.')
if '<b>Fire</b><small>Selected</small>' not in html:
    raise SystemExit('Fire selected state missing.')
for label in ('Intruder', 'Access Control', 'CCTV'):
    if f'<b>{label}</b><small>Future</small>' not in html:
        raise SystemExit(f'{label} future state missing.')
if HOME_ACTIONS not in html:
    raise SystemExit('Home controls changed unexpectedly.')

path.write_text(html, encoding='utf-8')
print('Applied supplied Home artwork in Fire / Intruder / Access Control / CCTV order.')
