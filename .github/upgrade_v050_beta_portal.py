from pathlib import Path

APP_URL='https://william2535.github.io/FIRE-ZONE-PLAN-APP/'
BETA_URL=APP_URL+'beta.html'

p=Path('index.html')
t=p.read_text()

def once(old,new,label):
    global t
    if old in t:
        t=t.replace(old,new,1)
    elif new not in t:
        raise SystemExit(f'v0.50 patch marker missing: {label}')

# Version bump.
t=t.replace('v0.49','v0.50')

# Make the browser build installable and properly branded on iPhone/iPad/Android.
once('<title>Zone Sketch by Will v0.50 — zone plan move controls</title>',
'''<title>Zone Sketch by Will Flood v0.50 — Fire &amp; Security Field Workspace</title>
<meta name="theme-color" content="#10263d">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Zone Sketch by Will">
<meta name="application-name" content="Zone Sketch by Will Flood">
<meta name="description" content="Zone Sketch by Will Flood — a touch-first fire &amp; security site survey, circuit and As-Fit workspace.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="assets/on-site-zone-planner-icon.webp">''',
'web app branding')

# Full-name attribution in the places engineers will actually see.
once('<div class="homeEyebrow">FIRE &amp; SECURITY · FIELD WORKSPACE</div><h1>Zone Sketch</h1><p>Capture the building, survey installed devices, build validated circuits and produce an As-Fit route — all from the same project.</p>',
'''<div class="homeEyebrow">FIRE &amp; SECURITY · FIELD WORKSPACE · BETA</div><h1>Zone Sketch <span class="byWill">by Will</span></h1><p>Capture the building, survey installed devices, build validated circuits and produce an As-Fit route — all from the same project.</p><div class="creatorLine">Designed &amp; built by <strong>Will Flood</strong></div>''',
'home creator branding')

once('<div class="brand">ZONE SKETCH BY WILL<small>PLAN / ZONE MAKER</small></div>',
'''<div class="brand">ZONE SKETCH <span class="brandBy">BY WILL FLOOD</span><small>PLAN / ZONE MAKER · BETA v0.50</small></div>''',
'top creator branding')

once('<header class="cbTop"><div><strong>CIRCUIT BUILDER</strong><small>ZONE PLAN + SURVEY → WIRING → AS-FIT</small></div>',
'''<header class="cbTop"><div><strong>CIRCUIT BUILDER</strong><small>BY WILL FLOOD · ZONE PLAN + SURVEY → WIRING → AS-FIT</small></div>''',
'circuit creator branding')

once('<div class="settingsFooter"><span>ZONE SKETCH · <b>v0.50</b></span><button id="appSettingsClose" class="primary">Done</button></div>',
'''<div class="settingsFooter"><span>ZONE SKETCH · <b>v0.50</b> · DESIGNED &amp; BUILT BY <b>WILL FLOOD</b></span><button id="appSettingsClose" class="primary">Done</button></div>''',
'settings creator branding')

# Put the beta portal in the normal Project menu so installed Android and browser testers can always get back to it.
once('<button id="drawingDetails">Drawing details</button><button id="appSettingsBtn">App settings</button><button id="backupProject">Save editable backup</button>',
'''<button id="drawingDetails">Drawing details</button><button id="appSettingsBtn">App settings</button><button id="betaPortalBtn">Beta tester portal</button><button id="backupProject">Save editable backup</button>''',
'beta portal menu button')

# Small branding layer, deliberately isolated from the mature drawing engine.
css=r'''
/* v0.50 — beta identity and author attribution. */
.byWill{font-weight:500;color:#b9d5ed}.creatorLine{margin-top:11px;font-size:11px;font-weight:700;letter-spacing:.055em;text-transform:uppercase;color:#9fc8ef}.creatorLine strong{color:#fff}.brandBy{font-size:.82em;color:#a9c9e4;font-weight:800}.brand small{margin-top:2px}.homeHeroBadge:before{content:'BETA TESTER BUILD';display:inline-flex;margin-bottom:9px;padding:5px 8px;border-radius:999px;background:#e6493f;color:#fff;font-size:8px;font-weight:950;letter-spacing:.13em}.betaPortalMenuGlow{box-shadow:inset 0 0 0 1px #85b8e8!important;background:#edf6ff!important;color:#1d5e98!important;font-weight:850!important}
@media(max-width:720px){.brandBy{display:block;font-size:.7em;line-height:1.1}.brand small{font-size:8px!important}.creatorLine{font-size:10px}}
'''
once('</style>',css+'\n</style>','branding css')

# Portal opener works in normal browsers and in the native Android wrapper.
portal_js=f'''\nfunction openBetaPortal(){{\n const url={BETA_URL!r};\n try{{if(window.AndroidBridge&&typeof AndroidBridge.openBetaPortal==='function'){{AndroidBridge.openBetaPortal();return}}}}catch(e){{}}\n const w=window.open(url,'_blank','noopener');if(!w)location.href=url;\n}}\n$('betaPortalBtn').onclick=openBetaPortal;$('betaPortalBtn').classList.add('betaPortalMenuGlow');\n'''
once('applyReducedMotion();\nconst fresh=', 'applyReducedMotion();'+portal_js+'\nconst fresh=', 'portal javascript')

# Keep every HTML entry point and Android WebView source identical.
for name in ['index.html','ZoneSketch.html','Zone-Sketch-by-Will.html','app/src/main/assets/index.html']:
    Path(name).write_text(t)

# Android wrapper version + a safe native route to the hosted tester portal.
g=Path('app/build.gradle').read_text()
g=g.replace('versionCode 50','versionCode 51').replace("versionName '0.49'","versionName '0.50'")
Path('app/build.gradle').write_text(g)

java=Path('app/src/main/java/com/zonesketch/app/MainActivity.java').read_text()
marker='''    private final class Bridge {\n        @JavascriptInterface public void sharePng(String dataUrl, String suggestedName) {'''
replacement=f'''    private final class Bridge {{\n        @JavascriptInterface public void openBetaPortal() {{\n            runOnUiThread(() -> {{\n                try {{\n                    Intent open = new Intent(Intent.ACTION_VIEW, Uri.parse("{BETA_URL}"));\n                    startActivity(open);\n                }} catch (Exception e) {{\n                    Toast.makeText(MainActivity.this, "Could not open the beta tester portal", Toast.LENGTH_LONG).show();\n                }}\n            }});\n        }}\n        @JavascriptInterface public void sharePng(String dataUrl, String suggestedName) {{'''
if marker in java:
    java=java.replace(marker,replacement,1)
elif 'openBetaPortal()' not in java:
    raise SystemExit('v0.50 patch marker missing: Android beta portal bridge')
Path('app/src/main/java/com/zonesketch/app/MainActivity.java').write_text(java)

# Installable web manifest.
manifest='''{
  "name": "Zone Sketch by Will Flood",
  "short_name": "Zone Sketch",
  "description": "Fire & security field workspace for plans, surveys, validated circuits and As-Fit drawings. Designed and built by Will Flood.",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "background_color": "#edf2f7",
  "theme_color": "#10263d",
  "icons": [
    {"src": "assets/zone-sketch-app-icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"}
  ]
}
'''
Path('manifest.webmanifest').write_text(manifest)

# Lightweight vector brand pack. Existing WEBP app icon/cover remain available too.
Path('assets/zone-sketch-app-icon.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#10263d"/><stop offset="1" stop-color="#1d5f91"/></linearGradient></defs><rect width="512" height="512" rx="112" fill="url(#g)"/><path d="M126 128h260v256H126z" fill="#fff" opacity=".08"/><path d="M156 166h200M156 226h128M156 286h200M156 346h92" stroke="#fff" stroke-width="24" stroke-linecap="round"/><circle cx="336" cy="226" r="27" fill="#ef4d43"/><circle cx="296" cy="346" r="27" fill="#ef4d43"/><path d="M336 253v45c0 27-14 48-40 48" fill="none" stroke="#ef4d43" stroke-width="18" stroke-linecap="round"/></svg>''')
Path('assets/zone-sketch-by-will-flood-wordmark.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300"><rect width="1200" height="300" rx="42" fill="#10263d"/><g transform="translate(52 46)"><rect width="208" height="208" rx="48" fill="#1d5f91"/><path d="M40 54h128M40 104h78M40 154h128" stroke="#fff" stroke-width="16" stroke-linecap="round"/><circle cx="144" cy="104" r="18" fill="#ef4d43"/><circle cx="120" cy="154" r="18" fill="#ef4d43"/></g><text x="302" y="126" font-family="Arial,Helvetica,sans-serif" font-size="72" font-weight="800" fill="#fff">ZONE SKETCH</text><text x="305" y="188" font-family="Arial,Helvetica,sans-serif" font-size="38" font-weight="700" fill="#a9c9e4">BY WILL FLOOD</text><text x="305" y="232" font-family="Arial,Helvetica,sans-serif" font-size="25" font-weight="600" letter-spacing="5" fill="#6f9fc5">FIRE &amp; SECURITY FIELD WORKSPACE</text></svg>''')
Path('assets/zone-sketch-beta-tester-badge.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 260"><rect width="900" height="260" rx="54" fill="#10263d"/><rect x="28" y="28" width="844" height="204" rx="38" fill="none" stroke="#315f86" stroke-width="4"/><circle cx="118" cy="130" r="54" fill="#ef4d43"/><path d="M89 130l20 20 40-46" fill="none" stroke="#fff" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/><text x="202" y="112" font-family="Arial,Helvetica,sans-serif" font-size="38" font-weight="800" fill="#fff">ZONE SKETCH BETA TESTER</text><text x="202" y="164" font-family="Arial,Helvetica,sans-serif" font-size="26" font-weight="700" fill="#a9c9e4">v0.50 · DESIGNED &amp; BUILT BY WILL FLOOD</text></svg>''')

# One send-ready portal for web/iOS/Android testers.
portal=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#10263d"><title>Zone Sketch Beta Tester Portal · v0.50 · Will Flood</title><style>
:root{{--navy:#10263d;--blue:#2e72c9;--red:#ef4d43;--green:#238655;--ink:#18283a;--muted:#64768a;--line:#d7e1ea;--bg:#edf2f7;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at 90% 0,#dceaff 0,transparent 30%),var(--bg);color:var(--ink)}}header{{background:linear-gradient(135deg,#0f243a,#19486d);color:#fff;padding:calc(18px + env(safe-area-inset-top)) 20px 54px}}.wrap{{width:min(1040px,100%);margin:auto}}.top{{display:flex;align-items:center;gap:13px}}.top img{{width:58px;height:58px;border-radius:15px}}.top strong{{display:block;font-size:17px}}.top small{{display:block;color:#aac6dc;margin-top:2px}}.hero{{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(250px,.75fr);gap:24px;align-items:end;margin-top:42px}}.eyebrow{{font-size:10px;font-weight:900;letter-spacing:.16em;color:#9fc8ef}}h1{{font-size:clamp(34px,6vw,62px);line-height:1;margin:8px 0 13px;letter-spacing:-.04em}}.lead{{max-width:690px;color:#d5e3ef;line-height:1.55}}.author{{margin-top:15px;font-size:12px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:#9fc8ef}}.author b{{color:#fff}}.version{{display:inline-flex;padding:7px 10px;border-radius:999px;background:#ef4d43;color:#fff;font-size:10px;font-weight:900;letter-spacing:.1em}}.heroCard{{padding:18px;border-radius:18px;background:#ffffff0e;border:1px solid #ffffff1c}}.heroCard strong{{display:block}}.heroCard p{{margin:6px 0 0;color:#c3d4e2;font-size:12px;line-height:1.5}}main{{width:min(1040px,calc(100% - 28px));margin:-28px auto 42px}}.panel{{background:#fff;border:1px solid var(--line);border-radius:22px;padding:22px;box-shadow:0 16px 45px #10263d14;margin-bottom:15px}}.actions{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}a.btn,button.btn{{border:0;text-decoration:none;text-align:center;padding:15px 14px;border-radius:13px;background:#eaf0f6;color:#23405d;font:inherit;font-weight:850;cursor:pointer}}a.btn.primary{{background:var(--blue);color:#fff}}a.btn.android{{background:var(--navy);color:#fff}}h2{{margin:0 0 6px;font-size:20px}}.sub{{margin:0 0 17px;color:var(--muted);font-size:13px;line-height:1.5}}.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}}.card{{border:1px solid var(--line);border-radius:15px;padding:15px;background:#f8fafc}}.card b{{display:block;margin-bottom:5px}}.card p{{margin:0;color:var(--muted);font-size:12px;line-height:1.5}}.updates{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}.update{{padding:14px;border-radius:14px;background:#f5f8fb;border:1px solid #dde6ee}}.update strong{{display:block;font-size:12px}}.update span{{display:block;margin-top:4px;color:#6c7e90;font-size:11px;line-height:1.45}}ol{{margin:10px 0 0;padding-left:22px}}li{{margin:8px 0;color:#526679;line-height:1.45;font-size:13px}}label{{display:block;font-size:12px;font-weight:800;margin:10px 0 5px}}input,select,textarea{{width:100%;border:1px solid #c8d5e0;border-radius:11px;padding:11px;background:#fff;font:inherit}}textarea{{min-height:120px;resize:vertical}}.feedbackActions{{display:flex;flex-wrap:wrap;gap:9px;margin-top:12px}}.feedbackActions button,.feedbackActions a{{border:0;border-radius:11px;padding:11px 13px;background:#eaf0f6;color:#284760;text-decoration:none;font:inherit;font-weight:800;cursor:pointer}}.feedbackActions .send{{background:var(--blue);color:#fff}}.brandPack{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px}}.asset{{display:flex;min-height:138px;align-items:center;justify-content:center;border:1px solid var(--line);border-radius:15px;background:#f6f9fb;padding:16px}}.asset img{{max-width:100%;max-height:105px}}.assetLink{{display:block;margin-top:7px;font-size:11px;color:#315f86;text-decoration:none;font-weight:800}}.known{{border-left:4px solid #d28a28;background:#fff9ef}}footer{{text-align:center;color:#6c7e90;font-size:11px;padding:12px 20px 36px}}code{{background:#edf2f6;padding:2px 5px;border-radius:5px}}@media(max-width:760px){{.hero{{grid-template-columns:1fr;margin-top:30px}}.actions,.updates,.grid,.brandPack{{grid-template-columns:1fr}}header{{padding-bottom:44px}}main{{margin-top:-22px}}.panel{{padding:18px}}}}
</style></head><body><header><div class="wrap"><div class="top"><img src="assets/on-site-zone-planner-icon.webp" alt="Zone Sketch icon"><div><strong>ZONE SKETCH BY WILL</strong><small>Beta Tester Portal · v0.50</small></div></div><div class="hero"><div><div class="eyebrow">FIRE &amp; SECURITY · FIELD BETA</div><h1>Help test Zone Sketch.</h1><div class="lead">This build is for engineers to try the real Plan → Survey → Circuit Builder → As-Fit workflow on phones, tablets and desktop before wider release.</div><div class="author">Designed &amp; built by <b>Will Flood</b></div></div><div class="heroCard"><span class="version">BETA v0.50</span><strong style="margin-top:10px">Tonight's tester build</strong><p>Same core project data across browser and Android. Use the browser version on iPhone/iPad and the APK on Android.</p></div></div></div></header><main>
<section class="panel"><h2>Start testing</h2><p class="sub">One link for everyone. Nothing needs setting up on iPhone or iPad; Android testers can use either option.</p><div class="actions"><a class="btn primary" href="./">Open web beta</a><a class="btn android" href="downloads/Zone-Sketch-by-Will-v0.50.apk" download>Download Android APK</a><button class="btn" id="copyLink">Copy tester link</button></div><div class="grid" style="margin-top:12px"><div class="card"><b>iPhone / iPad</b><p>Open the web beta in Safari. For an app-style icon: Share → Add to Home Screen.</p></div><div class="card"><b>Android</b><p>Download the APK above. Android may ask you to allow installs from the browser because this beta is not distributed through Play Store yet.</p></div></div></section>
<section class="panel"><h2>What's new in this tester build</h2><p class="sub">The focus is a smoother, more complete field experience while keeping the drawing tools and project data stable.</p><div class="updates"><div class="update"><strong>Professional project home</strong><span>Cleaner Plan → Survey → Circuits → As-Fit workflow, recent projects and clearer autosave confidence.</span></div><div class="update"><strong>Survey speed</strong><span>Grouped device picker, better touch hit areas and quicker visual feedback when placing devices.</span></div><div class="update"><strong>Circuit Builder</strong><span>Live detector progress, rising bell feedback, completion screen and addressable twin-cable return snapping.</span></div><div class="update"><strong>As-Fit workflow</strong><span>Validated completed circuits can be mapped back over the surveyed plan and exported as an As-Fit PNG.</span></div><div class="update"><strong>Field settings</strong><span>Circuit sounds, haptics, reduced motion and better in-app notices rather than browser-style alerts.</span></div><div class="update"><strong>Beta identity</strong><span>Clear Will Flood attribution, installable web-app metadata and this dedicated tester portal.</span></div></div></section>
<section class="panel"><h2>What I need you to test</h2><p class="sub">Try it like a real small job rather than just tapping random buttons.</p><ol><li>Create a project, import a plan or start blank, then draw a few rooms and zones.</li><li>Switch to Survey and add a panel plus several devices. Move/zoom around while placing them.</li><li>Open Circuit Builder. Try a conventional circuit and an addressable loop if possible.</li><li>On addressable, check the detector counter, bells, return-to-FAP stage and twin-cable snapping.</li><li>Complete the circuit, use Undo/Retry once, then keep it and generate the As-Fit preview.</li><li>Export something, return Home, close the app/browser, reopen it and confirm the project is still there.</li></ol></section>
<section class="panel known"><h2>Useful beta notes</h2><p class="sub" style="margin-bottom:0">Dense real-world plans are the most useful tests. Manual editing of the generated As-Fit route is still limited, advanced near-segment cable pairing is still being refined, and changing a Survey after circuits are built may still require rebuilding that circuit. Those are exactly the kinds of cases worth reporting.</p></section>
<section class="panel" id="feedback"><h2>Send feedback to Will</h2><p class="sub">Write it once here, then Share on your phone or copy the report into WhatsApp, Messages, email or GitHub.</p><div class="grid"><div><label for="tester">Your name (optional)</label><input id="tester" placeholder="e.g. John"><label for="device">Device</label><select id="device"><option>iPhone / iPad</option><option>Android phone</option><option>Android tablet</option><option>Desktop / laptop</option></select></div><div><label for="area">Area tested</label><select id="area"><option>General / whole app</option><option>Plan / Zone Maker</option><option>Survey</option><option>Circuit Builder</option><option>As-Fit / Export</option><option>Projects / Saving</option></select><label for="severity">How bad is it?</label><select id="severity"><option>Idea / improvement</option><option>Small annoyance</option><option>Bug but I can carry on</option><option>Stops me using the feature</option></select></div></div><label for="notes">What happened / what would make it better?</label><textarea id="notes" placeholder="Tell me what you were trying to do, what happened and what you expected instead."></textarea><div class="feedbackActions"><button class="send" id="shareReport">Share report</button><button id="copyReport">Copy report</button><a id="githubReport" href="https://github.com/william2535/FIRE-ZONE-PLAN-APP/issues/new?title=Beta%20feedback%20v0.50" target="_blank" rel="noopener">Open GitHub issue</a></div><p id="reportStatus" class="sub" style="margin-top:10px;margin-bottom:0"></p></section>
<section class="panel"><h2>Brand pack</h2><p class="sub">Useful if you want to share the tester link with another engineer without sending a random-looking URL.</p><div class="brandPack"><div><div class="asset"><img src="assets/zone-sketch-by-will-flood-wordmark.svg" alt="Zone Sketch by Will Flood wordmark"></div><a class="assetLink" href="assets/zone-sketch-by-will-flood-wordmark.svg" download>Download wordmark SVG</a></div><div><div class="asset"><img src="assets/zone-sketch-beta-tester-badge.svg" alt="Zone Sketch beta tester badge"></div><a class="assetLink" href="assets/zone-sketch-beta-tester-badge.svg" download>Download beta badge SVG</a></div><div><div class="asset"><img src="assets/on-site-zone-planner-icon.webp" alt="Zone Sketch app icon"></div><a class="assetLink" href="assets/on-site-zone-planner-icon.webp" download>Download app icon</a></div></div></section>
</main><footer>ZONE SKETCH BY WILL · v0.50 · DESIGNED &amp; BUILT BY <strong>WILL FLOOD</strong></footer><script>
const betaUrl=location.origin+location.pathname.replace(/[^/]*$/,'beta.html');const $=id=>document.getElementById(id);$('copyLink').onclick=async()=>{{try{{await navigator.clipboard.writeText(betaUrl);$('copyLink').textContent='Copied ✓'}}catch(e){{prompt('Copy tester link',betaUrl)}}}};function report(){{const who=$('tester').value.trim()||'Anonymous tester',notes=$('notes').value.trim()||'(no extra notes)';return `ZONE SKETCH BETA FEEDBACK — v0.50\nTester: ${{who}}\nDevice: ${{$('device').value}}\nArea: ${{$('area').value}}\nSeverity: ${{$('severity').value}}\nBrowser/device info: ${{navigator.userAgent}}\n\nFeedback:\n${{notes}}`;}}$('copyReport').onclick=async()=>{{try{{await navigator.clipboard.writeText(report());$('reportStatus').textContent='Report copied — paste it straight to Will.'}}catch(e){{prompt('Copy beta report',report())}}}};$('shareReport').onclick=async()=>{{const text=report();if(navigator.share){{try{{await navigator.share({{title:'Zone Sketch v0.50 beta feedback',text}});$('reportStatus').textContent='Thanks — report shared.';return}}catch(e){{if(e.name==='AbortError')return}}}}try{{await navigator.clipboard.writeText(text);$('reportStatus').textContent='Sharing is not available here, so the report was copied instead.'}}catch(e){{prompt('Copy beta report',text)}}}};
</script></body></html>'''
Path('beta.html').write_text(portal)
Path('download.html').write_text(portal)

print('Applied v0.50 beta tester portal, PWA identity and Will Flood branding')
