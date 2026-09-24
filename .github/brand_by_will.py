from pathlib import Path

ROOT = Path('.')
html_paths = [ROOT/'index.html', ROOT/'ZoneSketch.html', ROOT/'app/src/main/assets/index.html']
text = html_paths[0].read_text()

if 'Zone Sketch by Will' not in text:
    replacements = [
        ('<title>Zone Sketch v0.20 — site survey draft</title>', '<title>Zone Sketch by Will v0.21 — site survey draft</title>'),
        ('<div class="brand">ZONE SKETCH<small>ON-SITE DRAFT</small></div>', '<div class="brand">ZONE SKETCH BY WILL<small>ON-SITE DRAFT</small></div>'),
        ("'ZONE LAYOUT — SITE DRAFT · '", "'ZONE SKETCH BY WILL · ZONE LAYOUT — SITE DRAFT · '"),
        ("'ZONE SKETCH BUILDING PACK · '", "'ZONE SKETCH BY WILL · BUILDING PACK · '"),
        ("+'-zone-draft.png'", "+'-Zone-Sketch-by-Will-draft.png'"),
        ("+'-all-floors-zone-pack.png'", "+'-Zone-Sketch-by-Will-all-floors.png'"),
        ("'All-floor Zone Sketch building pack with floor plans and zone index.'", "'All-floor Zone Sketch by Will building pack with floor plans and zone index.'"),
        ("{format:'ZoneSketch',version:1,project:state}", "{format:'ZoneSketchByWill',version:1,project:state}"),
        ("filenameBase()+'.zonesketch.json'", "filenameBase()+'-Zone-Sketch-by-Will.zonesketch.json'"),
        ("raw?.format!=='ZoneSketch'||raw.version!==1", "!['ZoneSketch','ZoneSketchByWill'].includes(raw?.format)||raw.version!==1"),
        ("'This is not a supported Zone Sketch backup. The current site has not been replaced.'", "'This is not a supported Zone Sketch by Will backup. The current site has not been replaced.'"),
        ("filenameBase()+'-all-floors.pdf'", "filenameBase()+'-Zone-Sketch-by-Will-all-floors.pdf'"),
        ("'Site survey draft · Office verification and CAD redraw required'", "'Zone Sketch by Will · Site survey draft · Office verification and CAD redraw required'"),
    ]
    for old, new in replacements:
        if old not in text:
            raise SystemExit(f'Branding marker missing: {old[:90]}')
        text = text.replace(old, new, 1)
    text = text.replace('Zone Sketch building pack', 'Zone Sketch by Will building pack')

for p in html_paths:
    p.write_text(text)
(ROOT/'Zone-Sketch-by-Will.html').write_text(text)

manifest = ROOT/'app/src/main/AndroidManifest.xml'
m = manifest.read_text().replace('android:label="Zone Sketch"', 'android:label="Zone Sketch by Will"')
manifest.write_text(m)

main = ROOT/'app/src/main/java/com/zonesketch/app/MainActivity.java'
j = main.read_text()
j = j.replace('Could not load Zone Sketch', 'Could not load Zone Sketch by Will')
j = j.replace('Send Zone Sketch file', 'Send Zone Sketch by Will file')
main.write_text(j)

build = ROOT/'app/build.gradle'
b = build.read_text()
if "versionCode 20" in b:
    b = b.replace('versionCode 20', 'versionCode 21', 1).replace("versionName '0.20'", "versionName '0.21'", 1)
elif "versionCode 21" not in b:
    raise SystemExit('Unexpected Android version baseline')
build.write_text(b)

settings = ROOT/'settings.gradle'
s = settings.read_text().replace("rootProject.name = 'ZoneSketch'", "rootProject.name = 'ZoneSketchByWill'")
settings.write_text(s)

download = ROOT/'download.html'
d = download.read_text()
d = d.replace('downloads/ZoneSketch-v0.20.apk', 'downloads/Zone-Sketch-by-Will-v0.21.apk')
d = d.replace('downloads/ZoneSketch-v0.21.apk', 'downloads/Zone-Sketch-by-Will-v0.21.apk')
d = d.replace('Zone Sketch v0.20', 'Zone Sketch by Will v0.21')
d = d.replace('ZONE SKETCH<small>PUBLIC TESTER BUILD</small>', 'ZONE SKETCH BY WILL<small>PUBLIC TESTER BUILD</small>')
d = d.replace('v0.20', 'v0.21')
d = d.replace('Zone Sketch is an on-site', 'Zone Sketch by Will is an on-site')
d = d.replace('test Zone Sketch', 'test Zone Sketch by Will')
d = d.replace('official Zone Sketch link', 'official Zone Sketch by Will link')
download.write_text(d)

readme = ROOT/'README.md'
r = readme.read_text()
r = r.replace('# Zone Sketch — site draft for the office', '# Zone Sketch by Will — site draft for the office', 1)
r = r.replace('ZoneSketch-APK', 'Zone-Sketch-by-Will-APK')
r = r.replace('- `ZoneSketch.html`: standalone browser preview of the interface.', '- `Zone-Sketch-by-Will.html`: branded standalone browser preview of the interface.\n- `ZoneSketch.html`: compatibility copy kept in sync for older tooling.')
if '## Version 0.21 — Zone Sketch by Will branding' not in r:
    r += "\n\n## Version 0.21 — Zone Sketch by Will branding\n- Public-facing product name is **Zone Sketch by Will** across the browser app, Android launcher, public tester page and Android share UI.\n- APK, PNG, PDF and editable-backup filenames include **Zone-Sketch-by-Will** so shared copies are immediately recognisable.\n- Office exports and building packs carry **Zone Sketch by Will** branding.\n- New editable backups identify themselves as `ZoneSketchByWill`; older `ZoneSketch` backups remain supported.\n- Android package ID and browser storage identifiers intentionally remain unchanged so existing installs and saved drafts continue to work.\n"
readme.write_text(r)

print('Applied Zone Sketch by Will v0.21 branding')