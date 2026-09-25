from pathlib import Path

p=Path('index.html')
t=p.read_text()
old='<div class="brand">ZONE SKETCH <span class="brandBy">BY WILL FLOOD</span><small>PLAN / ZONE MAKER · BETA v0.50</small></div>'
new='<div class="brand">ZONE SKETCH<small>BY WILL FLOOD · PLAN / ZONE MAKER · BETA v0.50</small></div>'
if old in t:
    t=t.replace(old,new,1)
elif new not in t:
    raise SystemExit('v0.50 header fit marker missing')
# Keep the author line readable but reserve horizontal room for Export + field controls.
fit='''\n/* v0.50 header fit: full author attribution without crowding controls. */\n.topMain .brand{line-height:1.02}.topMain .brand small{max-width:210px;overflow:hidden;text-overflow:ellipsis}.topMain #site{min-width:90px}\n@media(max-width:1250px) and (min-width:721px){.topMain .brand{font-size:13px}.topMain .brand small{font-size:8px;letter-spacing:.055em;max-width:185px}.topMain #site{width:120px;max-width:180px}.top{gap:6px}.topMain,.topEssential{gap:6px}.top button{padding-left:10px;padding-right:10px}}\n'''
if '/* v0.50 header fit:' not in t:
    t=t.replace('</style>',fit+'</style>',1)
for name in ['index.html','ZoneSketch.html','Zone-Sketch-by-Will.html','app/src/main/assets/index.html']:
    Path(name).write_text(t)
print('Applied v0.50 compact Will Flood header fit')
