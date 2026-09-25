from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / '.github' / 'pineapple_v058_editor_patch.py'
APP = ROOT / 'index.html'
COPIES = [
    ROOT / 'Zone-Sketch-by-Will.html',
    ROOT / 'ZoneSketch.html',
    ROOT / 'app' / 'src' / 'main' / 'assets' / 'index.html',
]

BAD = "conflict.crossings.map(h=>({point:cbPxBoard(h.point,w,h),axis:h.axis||'h'}))"
GOOD = "conflict.crossings.map(hit=>({point:cbPxBoard(hit.point,w,h),axis:hit.axis||'h'}))"


def fix_one(path: Path, label: str) -> bool:
    text = path.read_text(encoding='utf-8')
    bad_count = text.count(BAD)
    good_count = text.count(GOOD)
    if bad_count == 1:
        path.write_text(text.replace(BAD, GOOD, 1), encoding='utf-8')
        print(f'fixed {label}: bridge crossing callback no longer shadows canvas height')
        return True
    if bad_count == 0 and good_count >= 1:
        print(f'{label}: bridge coordinate repair already present')
        return False
    raise SystemExit(f'{label}: expected one bridge callback target, found bad={bad_count}, good={good_count}')

fix_one(GENERATOR, 'editor generator source')
fix_one(APP, 'index.html')
for dst in COPIES:
    shutil.copyfile(APP, dst)

for path in [GENERATOR, APP, *COPIES]:
    text = path.read_text(encoding='utf-8')
    if BAD in text:
        raise SystemExit(f'{path}: stale shadowing callback remains')
    if GOOD not in text:
        raise SystemExit(f'{path}: corrected bridge callback missing')

print('Pineapple bridge-coordinate repair applied to generator source and all app copies')
