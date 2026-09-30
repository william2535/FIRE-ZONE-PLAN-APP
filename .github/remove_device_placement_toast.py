from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

replacements = [
    (
        "if(surveyMode){surveyPlacementSound('beam');uiToast('Beam detector added','success')}",
        "if(surveyMode)surveyPlacementSound('beam');",
    ),
    (
        "if(surveyMode){surveyPlacementSound(symbolStamp);uiToast((symbolNames[symbolStamp]||'Device')+' added','success')}",
        "if(surveyMode)surveyPlacementSound(symbolStamp);",
    ),
]

changed = False
for old, new in replacements:
    count = text.count(old)
    if count > 1:
        raise SystemExit(f'Expected at most one placement-toast match, found {count}: {old[:70]}')
    if count == 1:
        text = text.replace(old, new, 1)
        changed = True
    elif new not in text:
        raise SystemExit(f'Could not find expected device-placement code: {old[:70]}')

path.write_text(text, encoding='utf-8')
print('Device placement success popups removed.' if changed else 'Device placement success popups already removed.')
