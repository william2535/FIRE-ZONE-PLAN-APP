from pathlib import Path

FILES = [
    Path('index.html'),
    Path('ZoneSketch.html'),
    Path('Zone-Sketch-by-Will.html'),
    Path('app/src/main/assets/index.html'),
]

steps = "[2,5,10,20,40,50,100,150,200,250]"
late = f"const SURVEY_GRID_STEPS={steps};function syncSurveyTools()"
early = f"const SURVEY_GRID_STEPS={steps};\nconst fresh=()=>"

for path in FILES:
    text = path.read_text()
    if late in text:
        text = text.replace(late, "function syncSurveyTools()", 1)
    if early not in text:
        marker = "const fresh=()=>"
        if marker not in text:
            raise SystemExit(f'grid init marker missing in {path}')
        text = text.replace(marker, early, 1)
    # There must be exactly one initialized grid-step constant, and it must be
    # near the top of the app before any startup/render call can reach
    # syncSurveyTools().
    if text.count(f"const SURVEY_GRID_STEPS={steps};") != 1:
        raise SystemExit(f'unexpected SURVEY_GRID_STEPS count in {path}')
    path.write_text(text)

print('Fixed v0.42 Survey grid startup ordering')
