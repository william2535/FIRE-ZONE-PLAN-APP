from pathlib import Path

RELEASE_URL='https://github.com/william2535/FIRE-ZONE-PLAN-APP/releases/download/v0.50/Zone-Sketch-by-Will-v0.50.apk'
PAGES_URL='downloads/Zone-Sketch-by-Will-v0.50.apk'

for name in ['beta.html','download.html']:
    p=Path(name)
    t=p.read_text()
    t=t.replace(f'href="{PAGES_URL}" download', f'href="{RELEASE_URL}"')
    t=t.replace(f'href="{PAGES_URL}"', f'href="{RELEASE_URL}"')
    old='''<div class="card"><b>Android</b><p>Download the APK above. Android may ask you to allow installs from the browser because this beta is not distributed through Play Store yet.</p></div>'''
    new='''<div class="card"><b>Android</b><p>Use the Android APK button above. It now downloads from the GitHub Release server rather than the web page host, which is more reliable on Chrome/Samsung. If an older download is stuck at 100%, cancel that old download and tap the button again.</p><p style="margin-top:8px"><a href="downloads/Zone-Sketch-by-Will-v0.50.apk" style="color:#315f86;font-weight:800">Backup APK mirror</a></p></div>'''
    if old in t:
        t=t.replace(old,new,1)
    if 'GitHub Release server' not in t:
        raise SystemExit(f'Could not patch Android download help in {name}')
    p.write_text(t)
print('Patched v0.50 portal to use GitHub Release APK download with Pages backup mirror')
