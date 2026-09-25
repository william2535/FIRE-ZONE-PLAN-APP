from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'index.html'
s=SRC.read_text(encoding='utf-8')
count=s.count('cbSyncEditUi()')
if count!=6:
    raise SystemExit(f'Expected 6 stale cbSyncEditUi calls, found {count}')
s=s.replace('cbSyncEditUi()','cbEditSyncUi()')
SRC.write_text(s,encoding='utf-8')
for rel in ['Zone-Sketch-by-Will.html','ZoneSketch.html','app/src/main/assets/index.html']:
    shutil.copyfile(SRC,ROOT/rel)
print('Fixed all 6 editor UI synchronizer calls in all app copies')
