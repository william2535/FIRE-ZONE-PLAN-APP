from pathlib import Path

p=Path('index.html')
t=p.read_text()
residue="if(cbScreen!=='game'||!cbDrag?.points)return;const target=cbHitNode(p,w,h,true);if(target)cbFinishLeg(target,w,h);else{cbDrag=null;cbHover=null;$('cbBoardHint').textContent='Release directly over the next device to lock the cable';cbDrawBoard()}}"
if residue in t:
    t=t.replace(residue,'',1)
if 'function cbCaptureDragTarget' not in t or 'function cbCanvasCancel' not in t:
    raise SystemExit('v0.45 pointer repair could not confirm new gesture handlers')
p.write_text(t)
for q in [Path('ZoneSketch.html'),Path('Zone-Sketch-by-Will.html'),Path('app/src/main/assets/index.html')]:
    q.write_text(t)
print('Removed old cbCanvasUp residue after v0.45 gesture replacement')
