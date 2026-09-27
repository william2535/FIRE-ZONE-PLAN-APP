"""Guarded, repeatable mobile editor input fix for the four generated app copies."""
from pathlib import Path

path = Path('index.html')
text = path.read_text()

def replace(old, new):
    global text
    if text.count(old) == 1:
        text = text.replace(old, new)
    elif text.count(new) != 1:
        raise SystemExit(f'Expected exactly one old/new patch anchor: {old[:90]}')

replace('function cbCheckpointDrag(clear=false){if(cbDrag?.targets?.length)',
        'function cbCheckpointDrag(clear=false){if(cbEdit?.active){cbEdit.stroke=null;cbEdit.tap=null}if(cbDrag?.targets?.length)')
replace("function cbEditSetMode(mode){if(!cbEdit?.active)return;cbEdit.mode=mode;cbEdit.stroke=null;",
        "function cbEditSetMode(mode){if(!cbEdit?.active)return;cbCheckpointDrag();cbEdit.mode=mode;cbEdit.stroke=null;")
replace("function cbEditUndo(){if(!cbEdit?.active||!cbEdit.undo.length)return false;const now=",
        "function cbEditUndo(){if(!cbEdit?.active||!cbEdit.undo.length)return false;cbCheckpointDrag();const now=")
replace("function cbEditRedo(){if(!cbEdit?.active||!cbEdit.redo.length)return false;const now=",
        "function cbEditRedo(){if(!cbEdit?.active||!cbEdit.redo.length)return false;cbCheckpointDrag();const now=")
replace("function cbEditDone(){if(!cbEdit?.active)return false;const check=",
        "function cbEditDone(){if(!cbEdit?.active)return false;cbCheckpointDrag(true);const check=")
replace("for(const p of samples)cbEditMoveStroke(p,w,h);return true}",
        "for(const p of samples)cbEditMoveStroke(p,w,h);if(cbEdit.mode==='bin'&&cbEdit.tap?.pointerId===e.pointerId&&samples.some(p=>Math.hypot(p.x-cbEdit.tap.start.x,p.y-cbEdit.tap.start.y)>12))cbEdit.tap.moved=true;return true}")
replace("const moved=Math.hypot(p.x-cbEdit.tap.start.x,p.y-cbEdit.tap.start.y);cbEdit.tap=null;if(moved>12)return true;",
        "const moved=cbEdit.tap.moved||Math.hypot(p.x-cbEdit.tap.start.x,p.y-cbEdit.tap.start.y)>12;cbEdit.tap=null;if(moved)return true;")
replace("$('cbCanvas').onpointercancel=cbCanvasCancel;$('cbCanvas').addEventListener('wheel'",
        "$('cbCanvas').onpointercancel=cbCanvasCancel;$('cbCanvas').onlostpointercapture=cbCanvasCancel;$('cbCanvas').addEventListener('wheel'")
replace("$(id)?.classList.toggle('active',on);if($('cbEditBridge'))",
        "{$(id)?.classList.toggle('active',on);$(id)?.setAttribute('aria-pressed',String(on))}if($('cbEditBridge'))")
replace("if($('cbComplete'))$('cbComplete').hidden=true}",
        "if($('cbComplete'))$('cbComplete').hidden=true;cbUpdateGame()}")
replace("$('cbDetectorLeft').textContent=cbCircuit.complete?",
        "$('cbDetectorLeft').textContent=cbEdit?.active?(cbEditRouteOpen()?'ROUTE OPEN':cbCircuit.editDraft?.pending?'REPLACEMENT READY':'EDITING'):cbCircuit.complete?")
hint = "function cbEditHint(){const d=cbCircuit?.editDraft;if(cbEdit?.stroke)return 'Pencil · keep drawing, then finish on cable or a device on this leg';if(d?.pending)return 'Replacement ready · use Bin on the old section, then Done';if(cbEdit?.mode==='bin')return 'Bin · tap one cable section to remove it · Undo restores it';if(d?.gaps?.length)return 'Route open · Pencil across the gap, then Done to validate';return 'Pencil · start on cable or a device, then finish on the same leg'}"
if hint not in text:
    replace('function cbPaintBoard(){', hint + '\nfunction cbPaintBoard(){')
replace("if(cbScreen==='select')$('cbBoardHint').textContent='Pinch to zoom · tap or sweep across the devices in this loop';",
        "if(cbEdit?.active&&cbScreen==='game')$('cbBoardHint').textContent=cbEditHint();else if(cbScreen==='select')$('cbBoardHint').textContent='Pinch to zoom · tap or sweep across the devices in this loop';")

for name in ['index.html', 'ZoneSketch.html', 'Zone-Sketch-by-Will.html', 'app/src/main/assets/index.html']:
    Path(name).write_text(text)
print('Editor interruption, Bin drag rejection, capture-loss recovery and mode hints applied to all four copies.')
