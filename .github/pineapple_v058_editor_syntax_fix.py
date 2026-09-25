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

BAD = "if(q.d<=24&&(!best||q.d<best.d))best={kind:'segment',legIndex:li,segmentIndex:si,t:q.t,pos:si+q.t,point:cbPxBoard(q.p,w,h),d:q.d}}return best}"
GOOD = "if(q.d<=24&&(!best||q.d<best.d))best={kind:'segment',legIndex:li,segmentIndex:si,t:q.t,pos:si+q.t,point:cbPxBoard(q.p,w,h),d:q.d}}}return best}"


def fix_one(path: Path, label: str) -> bool:
    text = path.read_text(encoding='utf-8')
    bad_count = text.count(BAD)
    good_count = text.count(GOOD)
    if bad_count == 1:
        path.write_text(text.replace(BAD, GOOD, 1), encoding='utf-8')
        print(f'fixed {label}: restored missing cbEditAnchorAt closing brace')
        return True
    if bad_count == 0 and good_count >= 1:
        print(f'{label}: syntax repair already present')
        return False
    raise SystemExit(f'{label}: expected exactly one malformed cbEditAnchorAt tail, found bad={bad_count}, good={good_count}')


fix_one(GENERATOR, 'editor generator source')
fix_one(APP, 'index.html')

# Generated app copies are contractually identical on this branch.
for dst in COPIES:
    shutil.copyfile(APP, dst)

print('Pineapple editor syntax repair applied to generator source and all app copies')
