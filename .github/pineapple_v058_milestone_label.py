from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'index.html'
COPIES = [
    ROOT / 'Zone-Sketch-by-Will.html',
    ROOT / 'ZoneSketch.html',
    ROOT / 'app' / 'src' / 'main' / 'assets' / 'index.html',
]

OLD = '<title>Zone Sketch by Will Flood v0.57 — Fire &amp; Security Field Workspace</title>'
NEW = '<title>Zone Sketch by Will Flood v0.58 — Fire &amp; Security Field Workspace</title>'

text = APP.read_text(encoding='utf-8')
old_count = text.count(OLD)
new_count = text.count(NEW)
if old_count == 1:
    text = text.replace(OLD, NEW, 1)
    APP.write_text(text, encoding='utf-8')
    print('Updated web/app title to v0.58')
elif old_count == 0 and new_count == 1:
    print('v0.58 milestone label already present')
else:
    raise SystemExit(f'Unexpected title state: old={old_count}, new={new_count}')

for dst in COPIES:
    shutil.copyfile(APP, dst)

for path in [APP, *COPIES]:
    out = path.read_text(encoding='utf-8')
    if NEW not in out:
        raise SystemExit(f'{path}: v0.58 title missing')
    if OLD in out:
        raise SystemExit(f'{path}: stale v0.57 title remains')

print('Milestone label synchronized across all generated app copies')
