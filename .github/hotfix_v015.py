from pathlib import Path

s=Path('index.html').read_text()

def rep(old,new,label):
    global s
    c=s.count(old)
    if c!=1:
        raise SystemExit(f'{label}: expected 1 match, found {c}')
    s=s.replace(old,new,1)

rep(
    "if(pinchIds.has(e.pointerId)){pinchIds.delete(e.pointerId);drawing=null;return}if(!img)return;\nif((tool==='wall'||tool==='pen')&&drawing){",
    "if(pinchIds.has(e.pointerId)){pinchIds.delete(e.pointerId);drawing=null;return}if(!img)return;if(navMode&&drawing?.mode==='navPan'){drawing=null;return}\nif((tool==='wall'||tool==='pen')&&drawing){",
    'move mode pointer-up isolation'
)

rep(
    "document.querySelectorAll('[data-lock]').forEach(b=>b.onclick=()=>{const k=b.dataset.lock;state.locks[k]=!state.locks[k];renderLockMenu();syncBackground();persist();draw()});",
    "document.querySelectorAll('[data-lock]').forEach(b=>b.onclick=()=>{const k=b.dataset.lock;state.locks[k]=!state.locks[k];if(state.locks[k]){selection=[];drawing=null;syncSelectionBar()}renderLockMenu();syncBackground();persist();draw()});",
    'lock clears active selection'
)

rep(
    "document.querySelectorAll('[data-layer]').forEach(b=>b.onclick=()=>{const k=b.dataset.layer;state.layers[k]=state.layers[k]===false;renderLayersMenu();persist();draw()});",
    "document.querySelectorAll('[data-layer]').forEach(b=>b.onclick=()=>{const k=b.dataset.layer;state.layers[k]=state.layers[k]===false;if(state.layers[k]===false){selection=[];drawing=null;syncSelectionBar()}renderLayersMenu();persist();draw()});",
    'hidden layer clears active selection'
)

# Keep three distributable copies identical.
for p in [Path('index.html'),Path('ZoneSketch.html'),Path('app/src/main/assets/index.html')]:
    p.write_text(s)

r=Path('README.md')
text=r.read_text()
if 'Move-mode pointer-up isolation' not in text:
    text += '\n- v0.15 safety fix: Move-mode pointer-up isolation and clearing selections when layers/locks are activated.\n'
    r.write_text(text)

print('v0.15 interaction isolation hotfix applied')
