from pathlib import Path

paths = [Path('index.html'), Path('ZoneSketch.html'), Path('app/src/main/assets/index.html')]
s = paths[0].read_text()


def replace_one(old, new, label):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly 1 match, found {count}')
    s = s.replace(old, new, 1)

# Put the same Delete tool beside Undo/Redo in the top-right for fast onsite use.
replace_one(
    '<button class="primary" id="shareBtn">Send to office</button><button class="iconBtn" id="undoTop" aria-label="Undo" title="Undo">↶</button><button class="iconBtn" id="redoTop" aria-label="Redo" title="Redo">↷</button>',
    '<button class="primary" id="shareBtn">Send to office</button><button class="iconBtn" id="deleteTop" data-tool="erase" aria-label="Delete" title="Delete">⌫</button><button class="iconBtn" id="undoTop" aria-label="Undo" title="Undo">↶</button><button class="iconBtn" id="redoTop" aria-label="Redo" title="Redo">↷</button>',
    'top delete button',
)

replace_one(
    '<small>Select a room/group to move it, or drag one of the blue corner handles to resize it.</small>',
    '<small>Select a room/group to move it. Drag a blue corner handle to resize; the opposite corner stays fixed.</small>',
    'resize help text',
)

# v0.12 resized from the already-mutated object on every pointermove, which compounded
# the scale and made groups shoot away/shrink. Always rebuild geometry from the immutable
# pointer-down snapshot instead, with the opposite corner acting as the fixed anchor.
old_resize = "function resizeSelectionFromHandle(d,target){const old=d.bounds,t=snapGridPoint(target),minX=Math.max(.002,8/img.width),minY=Math.max(.002,8/img.height);let x1=old.x1,y1=old.y1,x2=old.x2,y2=old.y2;if(d.handle.includes('w'))x1=Math.min(t.x,x2-minX);if(d.handle.includes('e'))x2=Math.max(t.x,x1+minX);if(d.handle.includes('n'))y1=Math.min(t.y,y2-minY);if(d.handle.includes('s'))y2=Math.max(t.y,y1+minY);const ow=Math.max(minX,old.x2-old.x1),oh=Math.max(minY,old.y2-old.y1),nw=Math.max(minX,x2-x1),nh=Math.max(minY,y2-y1),sx=nw/ow,sy=nh/oh;for(const snap of d.snap){const o=getObj(snap.ref);if(!o)continue;const fn=p=>({x:clamp(x1+(p.x-old.x1)*sx),y:clamp(y1+(p.y-old.y1)*sy)});mapObjectPoints(snap.ref.type,o,fn);if(snap.ref.type==='labels'||snap.ref.type==='symbols')o.scale=Math.max(.25,Math.min(4,(snap.orig.scale||1)*Math.sqrt(Math.abs(sx*sy))))}}"
new_resize = "function resizeSelectionFromHandle(d,target){const old=d.bounds,t=snapGridPoint(target),v=transform(),minX=Math.max(.001,24/(img.width*v.s)),minY=Math.max(.001,24/(img.height*v.s));let x1=old.x1,y1=old.y1,x2=old.x2,y2=old.y2;if(d.handle.includes('w'))x1=Math.min(t.x,old.x2-minX);if(d.handle.includes('e'))x2=Math.max(t.x,old.x1+minX);if(d.handle.includes('n'))y1=Math.min(t.y,old.y2-minY);if(d.handle.includes('s'))y2=Math.max(t.y,old.y1+minY);const ow=Math.max(minX,old.x2-old.x1),oh=Math.max(minY,old.y2-old.y1),sx=Math.max(minX,x2-x1)/ow,sy=Math.max(minY,y2-y1)/oh;for(const snap of d.snap){const o=getObj(snap.ref),src=snap.orig;if(!o||!src)continue;const fn=p=>({x:clamp(x1+(p.x-old.x1)*sx),y:clamp(y1+(p.y-old.y1)*sy)});if(snap.ref.type==='walls'||snap.ref.type==='shapes')o.points=(src.points||[]).map(fn);else if(['doors','windows','shutters','stairs'].includes(snap.ref.type)){o.a=fn(src.a);o.b=fn(src.b)}else{const p=fn({x:src.x,y:src.y});o.x=p.x;o.y=p.y}if(snap.ref.type==='labels'||snap.ref.type==='symbols')o.scale=Math.max(.25,Math.min(4,(src.scale||1)*Math.sqrt(Math.abs(sx*sy))))}}"
replace_one(old_resize, new_resize, 'stable resize geometry')

# Make the resize pointer explicitly use raw plan coordinates. Grid snapping is handled
# once inside resizeSelectionFromHandle so it cannot compound across move events.
replace_one(
    "if(drawing.moved){resizeSelectionFromHandle(drawing,point(e.clientX,e.clientY));draw()}",
    "if(drawing.moved){resizeSelectionFromHandle(drawing,point(e.clientX,e.clientY));draw()}",
    'resize pointer path',
)

# README note for the release.
readme = Path('README.md').read_text()
section = """

## Version 0.13 — stable corner resize + quick delete

- Delete is duplicated beside Undo / Redo in the top-right for faster onsite editing.
- Corner resize now recalculates every frame from the original selection snapshot, preventing cumulative shrink/jump behaviour.
- The opposite corner stays fixed while resizing a room or group.
- A 24-screen-pixel minimum prevents a selected corridor/room collapsing into an unusably tiny shape.
"""
if '## Version 0.13' not in readme:
    readme += section
Path('README.md').write_text(readme)

required = [
    'id="deleteTop" data-tool="erase"',
    'const o=getObj(snap.ref),src=snap.orig',
    '24/(img.width*v.s)',
    'opposite corner stays fixed',
]
for marker in required:
    if marker not in s:
        raise SystemExit(f'missing v0.13 marker: {marker}')

for p in paths:
    p.write_text(s)
