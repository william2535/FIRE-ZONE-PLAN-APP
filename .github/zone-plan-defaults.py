from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

replacements = [
    (
        "gridVisible:false,snapGrid:false,gridSize:100",
        "gridVisible:true,snapGrid:false,gridSize:100",
        "default Zone Plan grid"
    ),
    (
        "let topSectionOpen=true;function syncTopSection()",
        "let topSectionOpen=false;function syncTopSection()",
        "collapsed top controls default"
    ),
    (
        "b.textContent=topSectionOpen?'▲':'▼';b.title=topSectionOpen?'Collapse top controls':'Show top controls';",
        "b.textContent=topSectionOpen?'▲':'Menu ▼';b.title=topSectionOpen?'Collapse top controls':'Show menu';",
        "collapsed menu label"
    ),
]

for old, new, label in replacements:
    if new in text:
        print(f'{label}: already current')
        continue
    if old not in text:
        raise SystemExit(f'{label}: expected source not found')
    text = text.replace(old, new, 1)
    print(f'{label}: updated')

p.write_text(text, encoding='utf-8')
