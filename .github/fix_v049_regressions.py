from pathlib import Path

p=Path('index.html')
t=p.read_text()

replacements=[
    ('<button id="homeNew" class="primary" disabled>＋ New project</button>',
     '<button id="homeNew" class="primary" disabled>Make a new plan</button>',
     'home new-project compatibility'),
    ("pairMode&&cbDrag?.pairSnap?'⇄ CABLES PAIRED':'⇄ PAIR SNAP READY'",
     "pairMode&&cbDrag?.pairSnap?'⇄ CABLES PAIRED':'⇄ TWIN CABLE SNAP'",
     'pair-snap compatibility'),
    ("$('homeNew').disabled=false;$('homeImport').disabled=false;await renderProjects();",
     "await renderProjects();$('homeNew').disabled=false;$('homeImport').disabled=false;",
     'project-home load ordering'),
]
for old,new,label in replacements:
    if old in t:
        t=t.replace(old,new,1)
    elif new not in t:
        raise SystemExit(f'v0.49 regression fix marker missing: {label}')

# Global feedback must stay above the full-screen Circuit Builder overlay.
layer_css='#appNoticeModal,#appSettingsModal{z-index:260!important}.uiToastStack{z-index:270!important}'
if layer_css not in t:
    if '</style>' not in t:
        raise SystemExit('v0.49 regression fix marker missing: style close')
    t=t.replace('</style>',layer_css+'</style>',1)

for name in ['index.html','ZoneSketch.html','Zone-Sketch-by-Will.html','app/src/main/assets/index.html']:
    Path(name).write_text(t)

print('Applied v0.49 legacy regression and overlay-layer fixes')
