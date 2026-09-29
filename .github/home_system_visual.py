from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

CSS_MARKER = '/* Home system visual preview — visual only, no control changes. */'
HOME_ACTIONS = '<div class="homeActions"><button id="homeNew" class="primary" disabled>Make a new plan</button><button id="homeImport" disabled>Import backup</button></div>'

if HOME_ACTIONS not in html:
    raise SystemExit('Expected Home actions were not found; refusing to move or replace existing controls.')

brand_old = '<div class="homeBrandRow"><div><div class="homeEyebrow">YOUR FIELD WORKSPACE</div><h1><span>ZONE</span> SKETCH</h1><div class="homeBrandTagline">FIRE &amp; SECURITY FIELD APP</div></div></div>'
brand_new = '<div class="homeBrandRow"><img class="homeMainLogo" src="assets/zone-sketch-complete-house-v2.png" alt="Zone Sketch"><div><div class="homeEyebrow">YOUR FIELD WORKSPACE</div><h1><span>ZONE</span> SKETCH</h1><div class="homeBrandTagline">FIRE &amp; SECURITY FIELD APP</div></div></div>'

if brand_old in html:
    html = html.replace(brand_old, brand_new, 1)
elif brand_new not in html:
    raise SystemExit('Projects Home brand row did not match the expected latest build.')

badge = '<div class="homeHeroBadge"><strong>Ready for your next site</strong><small>Local autosave · touch-first controls · offline project data</small></div>'
preview = '''<div class="homeSystemPreview" aria-label="Zone Sketch system range preview">
<div class="homeSystemTile homeSystemFire isSelected"><img src="assets/zone-sketch-fire-icon.svg" alt=""><span><b>Fire</b><small>Selected</small></span></div>
<div class="homeSystemTile isFuture" aria-disabled="true"><img src="assets/zone-sketch-intruder-icon.svg" alt=""><span><b>Intruder</b><small>Future</small></span></div>
<div class="homeSystemTile isFuture" aria-disabled="true"><img src="assets/zone-sketch-cctv-icon.svg" alt=""><span><b>CCTV</b><small>Future</small></span></div>
<div class="homeSystemTile isFuture" aria-disabled="true"><img src="assets/zone-sketch-access-icon.svg" alt=""><span><b>Access control</b><small>Future</small></span></div>
</div>'''

if 'class="homeSystemPreview"' not in html:
    target = badge + '</div><div class="homeHeading">'
    replacement = badge + preview + '</div><div class="homeHeading">'
    if target not in html:
        raise SystemExit('Projects Home hero ending did not match the expected latest build.')
    html = html.replace(target, replacement, 1)

if CSS_MARKER not in html:
    css = r'''
/* Home system visual preview — visual only, no control changes. */
#projectsHome .homeBrandRow{display:flex;align-items:center;gap:22px}
#projectsHome .homeMainLogo{width:108px;height:108px;object-fit:contain;flex:0 0 auto;filter:drop-shadow(0 0 15px rgba(0,194,255,.18)) drop-shadow(0 0 18px rgba(155,255,63,.10))}
#projectsHome .homeBrandRow>div{min-width:0}
#projectsHome .homeSystemPreview{grid-column:1/-1;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px;margin-top:2px;padding-top:14px;border-top:1px solid rgba(94,171,204,.24);pointer-events:none;user-select:none}
#projectsHome .homeSystemTile{min-width:0;min-height:70px;display:flex;align-items:center;gap:10px;padding:9px 11px;border:1px solid #2b596f;border-radius:5px 13px 5px 13px;background:linear-gradient(145deg,#0d2838,#071923);color:#d8effb;box-shadow:inset 0 1px rgba(255,255,255,.025);overflow:hidden}
#projectsHome .homeSystemTile img{width:48px;height:48px;object-fit:contain;border-radius:8px;flex:0 0 auto}
#projectsHome .homeSystemTile span{min-width:0;display:block}
#projectsHome .homeSystemTile b{display:block;font:800 11px/1.15 ui-monospace,SFMono-Regular,Consolas,monospace;letter-spacing:.07em;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#projectsHome .homeSystemTile small{display:block;margin-top:5px;font:700 8px/1 ui-monospace,SFMono-Regular,Consolas,monospace;letter-spacing:.12em;text-transform:uppercase;color:#84a9bc}
#projectsHome .homeSystemTile.isSelected{border-color:#f04b42;background:linear-gradient(145deg,#28151a,#101b25);box-shadow:inset 0 -2px #f04b42,0 0 18px rgba(240,75,66,.08)}
#projectsHome .homeSystemTile.isSelected small{color:#ff8b84}
#projectsHome .homeSystemTile.isFuture{opacity:.34;filter:grayscale(.88) saturate(.25)}
#projectsHome .homeSystemTile.isFuture img{filter:grayscale(1)}
@media(max-width:720px){
 #projectsHome .homeBrandRow{gap:14px}
 #projectsHome .homeMainLogo{width:76px;height:76px}
 #projectsHome .homeSystemPreview{grid-template-columns:repeat(2,minmax(0,1fr));gap:7px;padding-top:11px}
 #projectsHome .homeSystemTile{min-height:58px;padding:7px 9px}
 #projectsHome .homeSystemTile img{width:39px;height:39px}
 #projectsHome .homeSystemTile b{font-size:10px}
}
@media(max-width:360px){#projectsHome .homeMainLogo{width:64px;height:64px}#projectsHome .homeBrandRow{gap:10px}}
/* End home system visual preview. */
'''
    if '</style>' not in html:
        raise SystemExit('Style close tag not found.')
    html = html.replace('</style>', css + '\n</style>', 1)

if HOME_ACTIONS not in html:
    raise SystemExit('Home controls changed unexpectedly.')
if 'id="homeNew"' not in html or 'id="homeImport"' not in html:
    raise SystemExit('Home controls missing after visual patch.')

path.write_text(html, encoding='utf-8')
print('Applied visual-only Home logo + four-system preview.')
