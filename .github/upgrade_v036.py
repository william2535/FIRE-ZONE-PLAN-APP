from pathlib import Path
import base64, gzip, subprocess

BASE = '40d3c980fdb05776c3a073376df1706b6225fdac'
subprocess.run(['git','fetch','--no-tags','--depth=1','origin',BASE], check=True, stdout=subprocess.DEVNULL)
parts=[]
for name in ('v036_payload_1.txt','v036_payload_2.txt','v036_payload_3.txt'):
    parts.append(subprocess.check_output(['git','show',f'{BASE}:.github/{name}'], text=True).strip())
payload=''.join(parts)
if [len(p) for p in parts] != [3700,3700,3700] or len(payload) != 11100:
    raise SystemExit(f'v0.36 verified payload mismatch: parts={[len(p) for p in parts]}, total={len(payload)}')
source=gzip.decompress(base64.b64decode(payload, validate=True)).decode('utf-8')
exec(compile(source, '.github/upgrade_v036.py.payload', 'exec'))

# At tablet widths, place the essential edit controls on their own row so they cannot
# overlap the Export/project controls after switching tools or creating a blank plan.
tablet_css='\n@media(max-width:1100px) and (min-width:721px){.topMain{flex-basis:100%;flex-wrap:wrap}.topEssential{width:100%;justify-content:flex-end}.topMain #shareBtn{margin-left:auto}}\n'
for path in [Path('index.html'),Path('ZoneSketch.html'),Path('Zone-Sketch-by-Will.html'),Path('app/src/main/assets/index.html')]:
    text=path.read_text()
    if tablet_css.strip() not in text:
        text=text.replace('</style>',tablet_css+'</style>',1)
        path.write_text(text)
# Browser regressions now understand the split: plan-only symbols in Plan mode,
# surveyed devices in Survey mode, and clean exports without the tracing picture.
print('Applied v0.36 plus tablet toolbar overlap fix')
