from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
old = "gridVisible:true,snapGrid:false,gridSize:100"
new = "gridVisible:true,snapGrid:true,gridSize:100"
if new in text:
    print('Zone Plan grid + snap default: already current')
elif old in text:
    text = text.replace(old, new, 1)
    p.write_text(text, encoding='utf-8')
    print('Zone Plan grid + snap default: updated')
else:
    raise SystemExit('Expected Zone Plan grid default source not found')
