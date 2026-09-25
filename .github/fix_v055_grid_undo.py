from pathlib import Path

# Follow-up to the v0.55 grid migration: enabling the mandatory Survey field grid must not
# create a user-visible Undo step on a fresh project. Only moving existing off-grid device
# points is an actual drawing edit worth putting in history.
files = ['index.html', 'ZoneSketch.html', 'Zone-Sketch-by-Will.html', 'app/src/main/assets/index.html']
old = "function ensureSurveyFieldGrid(align=true){if(!img)return 0;const off=align?surveyFieldGridMisaligned():0,needs=!state.gridVisible||!state.snapGrid||off>0;if(!needs){syncGrid();return 0}push();state.gridVisible=true;state.snapGrid=true;const moved=align?alignSurveyDevicesToFieldGrid():0;changed();return moved}"
new = "function ensureSurveyFieldGrid(align=true){if(!img)return 0;const off=align?surveyFieldGridMisaligned():0,needs=!state.gridVisible||!state.snapGrid||off>0;if(!needs){syncGrid();return 0}if(off>0)push();state.gridVisible=true;state.snapGrid=true;const moved=align?alignSurveyDevicesToFieldGrid():0;changed();return moved}"

for name in files:
    p = Path(name)
    t = p.read_text()
    if old in t:
        t = t.replace(old, new, 1)
    elif new not in t:
        raise SystemExit(f'v0.55 grid undo repair marker missing in {name}')
    p.write_text(t)

print('v0.55 field-grid activation no longer creates a fake Undo step')
