"""Deterministic Pineapple v0.59 release preparation.

Runs only on the development branch via the v0.59 release-candidate workflow.
It promotes the already-hardened editor/mobile code to matched Web + Android
version metadata without touching the protected 24/7 company/demo build.
"""
from pathlib import Path

APP_COPIES = [
    Path('index.html'),
    Path('ZoneSketch.html'),
    Path('Zone-Sketch-by-Will.html'),
    Path('app/src/main/assets/index.html'),
]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old in text:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f'{label}: expected one old anchor, found {count}')
        return text.replace(old, new)
    if new in text:
        return text
    raise SystemExit(f'{label}: neither old nor new anchor found')


# Keep all generated app copies identical and change only user-visible release identity.
master = APP_COPIES[0].read_text()
master = replace_once(
    master,
    '<title>Zone Sketch by Will Flood v0.58 — Fire &amp; Security Field Workspace</title>',
    '<title>Zone Sketch by Will Flood v0.59 — Fire &amp; Security Field Workspace</title>',
    'document title',
)
master = replace_once(
    master,
    'BY WILL FLOOD · PLAN / ZONE MAKER · BETA v0.58',
    'BY WILL FLOOD · PLAN / ZONE MAKER · BETA v0.59',
    'visible app version',
)
for path in APP_COPIES:
    path.write_text(master)

# Android package version: v0.57 used versionCode 58, so v0.59 advances to 60.
gradle_path = Path('app/build.gradle')
gradle = gradle_path.read_text()
gradle = replace_once(gradle, 'versionCode 58', 'versionCode 60', 'Android versionCode')
gradle = replace_once(gradle, "versionName '0.57'", "versionName '0.59'", 'Android versionName')
gradle_path.write_text(gradle)

# Matched tester portal: one web milestone and one Android milestone.
beta_path = Path('beta.html')
beta = beta_path.read_text()
beta = beta.replace('v0.58', 'v0.59').replace('v0.57', 'v0.59')
beta = beta.replace('./index.html?v=0.59', './web-v059.html')
beta = beta.replace(
    'The browser build is v0.59. The Android APK remains v0.59 until the next Android package is built and released.',
    'Web and Android now match at v0.59. This milestone includes the hardened Manual Edit workflow and the latest mobile safety fixes.',
)
beta = beta.replace(
    'Web v0.59 is the current browser milestone. Android testers can still use the v0.59 APK below.',
    'Web v0.59 and Android v0.59 are the matched tester milestone. Use the fresh web launcher or install the APK below.',
)
beta = beta.replace(
    'The current packaged Android release is still v0.59. It downloads from the GitHub Release server rather than the web page host, which is more reliable in Chrome and Samsung Internet.',
    'The packaged Android v0.59 release matches the web milestone. It downloads from the GitHub Release server rather than the web page host, with the repository mirror kept as a backup.',
)
beta = beta.replace(
    '<div class="update"><strong>Circuit Builder</strong><span>Smart Route separates raw touch from saved cable geometry, catches fast passes with a swept device corridor, filters wobble/reversals and keeps the magnetic twin-cable return.</span></div>',
    '<div class="update"><strong>Manual cable editing</strong><span>Pencil, Bin, Undo/Redo, Bridge and Cleanup now survive interruptions safely, preserve staged work, keep circuit status honest and protect edited geometry when plan bounds change.</span></div>',
)
beta = beta.replace(
    'Dense real-world plans and rough one-handed routing are especially useful tests. Smart Route now filters touch noise and catches fast device passes; unusual tight obstacle layouts, manual As-Fit editing and Survey changes after circuits are built are still worth reporting.',
    'Dense real-world plans and rough one-handed routing are especially useful tests. Please stress Manual Edit on iPhone/Android, switch between circuits, rotate/resize the screen, reload a saved draft and check the final As-Fit still follows the edited route.',
)
beta_path.write_text(beta)
# Keep the legacy download entry point identical so tester delivery paths cannot drift.
Path('download.html').write_text(beta)

# Fresh uncached web entry point for real-device testing.
Path('web-v059.html').write_text('''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<title>Zone Sketch Web v0.59 — Fresh Launch</title>
<meta name="theme-color" content="#10263d">
<style>html,body{height:100%;margin:0;font-family:system-ui,-apple-system,sans-serif;background:#10263d;color:#fff}body{display:grid;place-items:center}.card{text-align:center;padding:24px;max-width:360px}.mark{font-size:42px}.title{font-size:21px;font-weight:900;margin:8px 0}.sub{color:#c6d7e6;font-size:13px;line-height:1.45}a{display:inline-block;margin-top:16px;padding:11px 15px;border-radius:11px;background:#fff;color:#10263d;text-decoration:none;font-weight:800}</style>
</head>
<body><div class="card"><div class="mark">🍍</div><div class="title">Opening Zone Sketch Web v0.59</div><div class="sub">Fresh Pineapple milestone launcher — bypassing any older cached app document.</div><a id="fallback" href="./index.html?pineapple=v059">Open v0.59</a></div>
<script>
const target='./index.html?pineapple=v059&fresh='+Date.now();
document.getElementById('fallback').href=target;
location.replace(target);
</script>
</body>
</html>
''')

print('Prepared matched Zone Sketch Web v0.59 + Android v0.59 release candidate.')
