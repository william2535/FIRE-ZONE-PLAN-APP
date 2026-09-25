from pathlib import Path
import json,re

SRC=Path('index.html')
OLD_DEMO=Path('247-protection-demo.html')
OUT_DIR=Path('company-demos/247-protection')
OUT=OUT_DIR/'index.html'

base=SRC.read_text()
old=OLD_DEMO.read_text() if OLD_DEMO.exists() else ''
m=re.search(r"const LOGO='(data:image/png;base64,[^']+)'",old)
if not m and (OUT_DIR/'logo.svg').exists():
    m=re.search(r'href="(data:image/png;base64,[^"]+)"',(OUT_DIR/'logo.svg').read_text())
if not m:
    raise SystemExit('Could not recover the supplied 24/7 Protection logo from the earlier demo or generated logo')
logo=m.group(1)
t=base

def once(old,new,label):
    global t
    if old not in t:
        raise SystemExit(f'24/7 demo marker missing: {label}')
    t=t.replace(old,new,1)

# IMPORTANT: this script reads the proven main app and writes a separate generated copy only.
# It never writes index.html, ZoneSketch.html, the Android assets, or any original app file.
once('<body>','<body class="company247">','body class')
once('<title>Zone Sketch by Will Flood v0.50 — Fire &amp; Security Field Workspace</title>','<title>24/7 Protection · Zone Sketch Company Demo v0.50</title>','title')
once('<meta name="apple-mobile-web-app-title" content="Zone Sketch by Will">','<meta name="apple-mobile-web-app-title" content="24/7 Protection">','apple title')
once('<meta name="application-name" content="Zone Sketch by Will Flood">','<meta name="application-name" content="24/7 Protection Zone Sketch Demo">','app name')
once('<meta name="description" content="Zone Sketch by Will Flood — a touch-first fire &amp; security site survey, circuit and As-Fit workspace.">','<meta name="description" content="24/7 Protection company-branded Zone Sketch demo for fire &amp; security site surveys, circuits and As-Fit drawings.">','description')
once('<link rel="apple-touch-icon" href="assets/on-site-zone-planner-icon.webp">','<link rel="apple-touch-icon" href="logo.svg">','touch icon')

# Nested copy needs vendor paths back to the root repo assets.
t=t.replace('src="vendor/','src="../../vendor/')
t=t.replace("workerSrc='vendor/","workerSrc='../../vendor/")

css='''
/* 24/7 Protection COMPANY DEMO — scoped only to this generated copy. */
.company247 .companyBrand{display:flex;align-items:center;gap:7px;flex:0 0 auto;min-width:0}
.company247 .companyBrandLogo{width:76px;height:54px;object-fit:contain;display:block;background:#fff;border-radius:12px;padding:2px;box-shadow:0 5px 18px #06182b4d;border:1px solid #ffffff55}
.company247 .companyBrandTag{display:inline-flex;align-items:center;min-height:24px;padding:5px 8px;border-radius:999px;background:#b51f2a;color:#fff;font-size:8px;font-weight:950;letter-spacing:.12em;white-space:nowrap;box-shadow:0 4px 12px #6e10182e}
.company247 .top{background:linear-gradient(135deg,#0d2741,#173e60 58%,#102b46)}
.company247 .top button.primary,.company247 .row button.primary,.company247 .tools button.primary{background:#c8272f}
.company247 .companyHeroBrand{display:flex;align-items:center;gap:16px;margin-bottom:12px}
.company247 .companyHeroBrand img{width:116px;height:92px;object-fit:contain;background:#fff;border-radius:18px;padding:5px;box-shadow:0 10px 26px #071d352b}
.company247 .companyHeroBrand strong{display:block;font-size:clamp(24px,4vw,40px);letter-spacing:-.03em;color:#fff}
.company247 .companyHeroBrand small{display:block;margin-top:4px;color:#bed4e6;font-weight:800;letter-spacing:.08em}
.company247 .companyIsolationNote{margin-top:10px;color:#bfd2e1;font-size:11px;font-weight:750;letter-spacing:.02em}
.company247 .settingsMark{font-size:0;background:#fff;padding:4px}
.company247 .settingsMark:before{content:'24/7';font-size:12px;color:#12385b;font-weight:950}
.company247 .cbTop{background:linear-gradient(135deg,#0d2741,#173e60)}
@media(max-width:720px){.company247 .companyBrandLogo{width:66px;height:48px;border-radius:10px}.company247 .companyBrandTag{font-size:7px;padding:4px 6px}.company247 .companyHeroBrand img{width:90px;height:72px}.company247 .topMain{align-items:center}}
@media(max-width:430px){.company247 .companyBrandTag{display:none}.company247 .companyBrandLogo{width:62px;height:44px}}
'''
once('</style>',css+'\n</style>','brand css')

# Compact header branding: same layout engine, no oversized logo block.
once('<div class="brand">ZONE SKETCH<small>BY WILL FLOOD · PLAN / ZONE MAKER · BETA v0.50</small></div>',
     '<div class="brand companyBrand" aria-label="24/7 Protection company demo"><img class="companyBrandLogo" src="logo.svg" alt="24/7 Protection"><span class="companyBrandTag">COMPANY DEMO</span></div>',
     'top brand')

# Company-facing identity while still retaining small platform attribution.
once('FIRE &amp; SECURITY · FIELD WORKSPACE · BETA','24/7 PROTECTION · FIRE &amp; SECURITY FIELD WORKSPACE · COMPANY DEMO','home eyebrow')
once('<h1>Zone Sketch <span class="byWill">by Will</span></h1>',
     '<div class="companyHeroBrand"><img src="logo.svg" alt="24/7 Protection"><div><strong>24/7 Protection</strong><small>FIRE &amp; SECURITY FIELD WORKSPACE</small></div></div><h1>Zone Sketch <span class="byWill">company edition</span></h1>',
     'home brand')
once('<div class="creatorLine">Designed &amp; built by <strong>Will Flood</strong></div>',
     '<div class="creatorLine">24/7 Protection branded demo · Zone Sketch platform by <strong>Will Flood</strong></div><div class="companyIsolationNote">Separate demo storage · projects created here cannot appear in the normal Zone Sketch app.</div>',
     'home attribution')
once('<div class="homeVersion">ZONE SKETCH · v0.50</div>','<div class="homeVersion">24/7 PROTECTION DEMO · ZONE SKETCH v0.50</div>','home version')
once('<strong>Site-ready workspace</strong><small>Local autosave · touch-first controls · offline project data</small>',
     '<strong>24/7 Protection workspace demo</strong><small>Local autosave · touch-first controls · isolated company-demo project data</small>',
     'home badge')
once('<small>BY WILL FLOOD · ZONE PLAN + SURVEY → WIRING → AS-FIT</small>',
     '<small>24/7 PROTECTION · ZONE PLAN + SURVEY → WIRING → AS-FIT · COMPANY DEMO</small>',
     'circuit identity')
once('<div class="settingsMark">ZS</div>','<div class="settingsMark">24/7</div>','settings mark')
once('<span>ZONE SKETCH · <b>v0.50</b> · DESIGNED &amp; BUILT BY <b>WILL FLOOD</b></span>',
     '<span><b>24/7 PROTECTION</b> · COMPANY DEMO · ZONE SKETCH v0.50 · PLATFORM BY <b>WILL FLOOD</b> · SEPARATE DEMO STORAGE</span>',
     'settings footer')
once('<button id="betaPortalBtn">Beta tester portal</button>','<button id="betaPortalBtn" hidden>Beta tester portal</button>','hide normal beta portal')
once('<small class="draftBadge">PLAN / ZONE MAKER</small>','<small class="draftBadge">PLAN / ZONE MAKER</small><small class="companyBrandTag" title="Separate company demo">24/7 DEMO</small>','floor demo marker')

# HARD SEPARATION: different IndexedDB and all local preference keys.
once("indexedDB.open('ZoneSketch-v1',1)","indexedDB.open('ZoneSketch-247Protection-v1',1)",'separate indexeddb')
t=t.replace('zoneSketch','zoneSketch247Protection')
t=t.replace('Zone-Sketch-by-Will','247-Protection-Zone-Sketch-Demo')

# Preload the supplied logo once so canvas-based PNG/PDF/As-Fit exports can use it.
logo_boot="""<script>window.COMPANY247={name:'24/7 Protection',demo:true,logoImage:new Image()};window.COMPANY247.logoImage.src='logo.svg';</script>\n"""
once('<script src="../../vendor/pdf.min.js"></script>',logo_boot+'<script src="../../vendor/pdf.min.js"></script>','logo preload')

# Brand zone-plan / site-survey exports. PDFs are built from these branded canvases.
old="x.fillStyle='#fff';x.font='bold 26px system-ui';x.fillText(((state.site||'Untitled site')+' — '+f.name).slice(0,120),pad,33,exportWidth-2*pad);x.font='14px system-ui';x.fillText('ZONE SKETCH BY WILL · '+(zoneMode?'ZONE PLAN':'SITE SURVEY')+' · '+(state.meta?.drawingRef||'No reference')+' · Rev '+(state.meta?.revision||'—')+' · '+(state.meta?.surveyDate||new Date().toLocaleDateString('en-GB')),pad,57,exportWidth-2*pad);"
new="x.fillStyle='#fff';const companyLogo=window.COMPANY247?.logoImage;if(companyLogo?.complete&&companyLogo.naturalWidth)x.drawImage(companyLogo,pad+2,7,58,58);const companyHeaderX=pad+74;x.font='bold 26px system-ui';x.fillText(((state.site||'Untitled site')+' — '+f.name).slice(0,120),companyHeaderX,33,exportWidth-companyHeaderX-pad);x.font='14px system-ui';x.fillText('24/7 PROTECTION · '+(zoneMode?'ZONE PLAN':'SITE SURVEY')+' · '+(state.meta?.drawingRef||'No reference')+' · Rev '+(state.meta?.revision||'—')+' · '+(state.meta?.surveyDate||new Date().toLocaleDateString('en-GB')),companyHeaderX,57,exportWidth-companyHeaderX-pad);"
once(old,new,'zone/survey export header')

old="x.fillStyle='#fff';x.font='bold 36px system-ui';x.fillText(state.site||'Untitled site',65,65,1470);x.font='22px system-ui';x.fillText((mode==='survey'?'SITE SURVEY DEVICE SUMMARY':'BUILDING ZONE INDEX')+' · '+pageNo,65,110);"
new="x.fillStyle='#fff';const companyIndexLogo=window.COMPANY247?.logoImage;if(companyIndexLogo?.complete&&companyIndexLogo.naturalWidth)x.drawImage(companyIndexLogo,65,10,95,95);x.font='bold 36px system-ui';x.fillText(state.site||'Untitled site',180,65,1355);x.font='22px system-ui';x.fillText('24/7 PROTECTION · '+(mode==='survey'?'SITE SURVEY DEVICE SUMMARY':'BUILDING ZONE INDEX')+' · '+pageNo,180,110);"
once(old,new,'pdf index brand')
once("x.fillText('Zone Sketch by Will · '+(mode==='survey'?'Site survey':'Zone plan')+' draft · Office verification required',65,2040);",
     "x.fillText('24/7 Protection · '+(mode==='survey'?'Site survey':'Zone plan')+' draft · Powered by Zone Sketch · Office verification required',65,2040);",
     'pdf footer brand')

# Brand As-Fit PNG header too.
old="if(header){x.fillStyle='#16283e';x.fillRect(0,0,W,64);x.fillStyle='#fff';x.font='800 24px system-ui';x.fillText((state.site||'Site')+' — '+activeFloor().name+' — AS-FIT',30,29);x.font='13px system-ui';x.fillText('Generated from Zone Plan + Site Survey + completed Circuit Builder routes',30,50)}"
new="if(header){x.fillStyle='#16283e';x.fillRect(0,0,W,64);const companyAsFitLogo=window.COMPANY247?.logoImage;if(companyAsFitLogo?.complete&&companyAsFitLogo.naturalWidth)x.drawImage(companyAsFitLogo,24,5,54,54);const ahx=90;x.fillStyle='#fff';x.font='800 24px system-ui';x.fillText((state.site||'Site')+' — '+activeFloor().name+' — AS-FIT',ahx,29,W-ahx-24);x.font='13px system-ui';x.fillText('24/7 Protection · Generated from Zone Plan + Site Survey + completed Circuit Builder routes',ahx,50,W-ahx-24)}"
once(old,new,'asfit export brand')

OUT_DIR.mkdir(parents=True,exist_ok=True)
OUT.write_text(t)

# Separate install identity/scope so even Add to Home Screen cannot be confused with the original.
manifest={
 'name':'24/7 Protection Zone Sketch Demo','short_name':'24/7 Protection',
 'id':'/FIRE-ZONE-PLAN-APP/company-demos/247-protection/','start_url':'./','scope':'./','display':'standalone',
 'background_color':'#edf2f7','theme_color':'#10263d',
 'icons':[{'src':'logo.svg','sizes':'any','type':'image/svg+xml','purpose':'any maskable'}]
}
(OUT_DIR/'manifest.webmanifest').write_text(json.dumps(manifest,indent=2))
(OUT_DIR/'logo.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><rect width="512" height="512" rx="92" fill="#fff"/><image href="{logo}" x="22" y="22" width="468" height="468" preserveAspectRatio="xMidYMid meet"/></svg>''')

# Old experiment becomes only a redirect, so there is one company-demo implementation to test.
Path('247-protection-demo.html').write_text('''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=company-demos/247-protection/"><title>24/7 Protection demo</title></head><body><p>Opening the isolated 24/7 Protection demo… <a href="company-demos/247-protection/">Continue</a></p></body></html>''')

# Safety assertions: generated copy is branded + isolated; original source remains untouched in memory.
assert "ZoneSketch-247Protection-v1" in t
assert "indexedDB.open('ZoneSketch-v1',1)" not in t
assert 'companyBrandLogo' in t and '24/7 PROTECTION' in t
assert base==SRC.read_text(), 'Main app changed unexpectedly'
print('Built isolated 24/7 Protection demo; original app untouched')
