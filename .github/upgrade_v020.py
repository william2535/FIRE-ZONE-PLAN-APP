from pathlib import Path

ROOT = Path('.')
paths = [ROOT/'index.html', ROOT/'ZoneSketch.html', ROOT/'app/src/main/assets/index.html']
text = paths[0].read_text()


def rep(old, new, label):
    global text
    if old not in text:
        raise SystemExit(f'v0.20 patch marker missing: {label}')
    text = text.replace(old, new, 1)

# Public-facing menu wording and new tools.
rep(
    'Zone contains Box, Outline and Fill area. Building layout contains walls and room layout tools. Doors, windows, shutters and stairs are under Objects.',
    'Zone contains Box, Outline and Fill area. Building layout contains walls, boxes, outlines, circular rooms and room labels. Doors, double doors, windows, shutters and stairs are under Objects.',
    'help wording'
)
rep(
    '<button data-menu-tool="layoutPoly">⬡ Outline</button><button data-menu-tool="label">Room label</button>',
    '<button data-menu-tool="layoutPoly">⬡ Outline</button><button data-menu-tool="layoutEllipse">◯ Circular room</button><button data-menu-tool="label">Room label</button>',
    'circular room menu button'
)
rep(
    '<button data-menu-tool="door">Door</button><button data-menu-tool="window">Window</button>',
    '<button data-menu-tool="door">Door</button><button data-menu-tool="doubleDoor">Double door</button><button data-menu-tool="window">Window</button>',
    'double door menu button'
)

# Tool registration / labels / hints.
rep(
    "const zoneTools=new Set(['rect','poly','fill']),layoutTools=new Set(['wall','pen','layoutRect','layoutPoly','label','quickLabel','trim']),objectTools=new Set(['door','window','shutter','stairs']),symbolTools=new Set(['symbol']),detailTools=new Set(['pinNote','pinPhoto']),wallObjectTools=new Set(['door','window','shutter']);",
    "const zoneTools=new Set(['rect','poly','fill']),layoutTools=new Set(['wall','pen','layoutRect','layoutPoly','layoutEllipse','label','quickLabel','trim']),objectTools=new Set(['door','doubleDoor','window','shutter','stairs']),symbolTools=new Set(['symbol']),detailTools=new Set(['pinNote','pinPhoto']),wallObjectTools=new Set(['door','doubleDoor','window','shutter']);",
    'tool sets'
)
rep(
    "return({rect:'Box',poly:'Outline',fill:'Fill area',wall:'Wall',pen:'Pen',door:'Door',window:'Window',shutter:'Roller shutter',stairs:'Stairway',layoutRect:'Box',layoutPoly:'Outline',label:'Room label',trim:'Trim / Extend',pinNote:'Pinned note',pinPhoto:'Pinned photo'})[t]||t",
    "return({rect:'Box',poly:'Outline',fill:'Fill area',wall:'Wall',pen:'Pen',door:'Door',doubleDoor:'Double door',window:'Window',shutter:'Roller shutter',stairs:'Stairway',layoutRect:'Box',layoutPoly:'Outline',layoutEllipse:'Circular room',label:'Room label',trim:'Trim / Extend',pinNote:'Pinned note',pinPhoto:'Pinned photo'})[t]||t",
    'tool labels'
)
rep(
    "door:'Drag along a wall · finger side chooses the swing · orange preview shows the result',window:",
    "door:'Drag along a wall · finger side chooses the swing · orange preview shows the result',doubleDoor:'Drag along a wall · finger side chooses the swing · orange preview shows both leaves',window:",
    'double door hint'
)
rep(
    "layoutRect:'Drag a box to create four black building walls',layoutPoly:'Tap building corners, then Finish outline to create black walls',label:",
    "layoutRect:'Drag a box to create four black building walls',layoutPoly:'Tap building corners, then Finish outline to create black walls',layoutEllipse:'Drag an oval or circle · it becomes editable wall sections for doors and windows',label:",
    'circular room hint'
)

# Double-door renderer. It uses one wall opening and two independent swing leaves.
needle = "function drawWindow(c,a,b,width=2,color='#172333')"
insert = """function drawDoubleDoor(c,a,b,width=3,side=1,color='#172333'){const dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy);if(L<4)return;const nx=(-dy/L)*side,ny=(dx/L)*side,hx=dx/2,hy=dy/2,half=L/2,m={x:(a.x+b.x)/2,y:(a.y+b.y)/2},leafA={x:a.x+nx*half,y:a.y+ny*half},leafB={x:b.x+nx*half,y:b.y+ny*half};c.save();c.lineCap='round';c.lineJoin='round';c.strokeStyle=color;c.lineWidth=width;c.beginPath();c.moveTo(a.x,a.y);c.lineTo(leafA.x,leafA.y);c.moveTo(b.x,b.y);c.lineTo(leafB.x,leafB.y);c.stroke();const steps=14;c.beginPath();c.moveTo(m.x,m.y);for(let i=1;i<=steps;i++){const t=(Math.PI/2)*(i/steps);c.lineTo(a.x+hx*Math.cos(t)+nx*half*Math.sin(t),a.y+hy*Math.cos(t)+ny*half*Math.sin(t))}c.stroke();c.beginPath();c.moveTo(m.x,m.y);for(let i=1;i<=steps;i++){const t=(Math.PI/2)*(i/steps);c.lineTo(b.x-hx*Math.cos(t)+nx*half*Math.sin(t),b.y-hy*Math.cos(t)+ny*half*Math.sin(t))}c.stroke();c.restore()}\n"""
if needle not in text:
    raise SystemExit('v0.20 patch marker missing: drawWindow insertion point')
text = text.replace(needle, insert + needle, 1)

# Store double doors in the existing door collection so old drafts remain compatible.
rep(
    "if(kind==='door'){obj.side=side>=0?1:-1;state.doors.push(obj)}else if(kind==='window')state.windows.push(obj);",
    "if(kind==='door'||kind==='doubleDoor'){obj.side=side>=0?1:-1;obj.double=kind==='doubleDoor';state.doors.push(obj)}else if(kind==='window')state.windows.push(obj);",
    'door object storage'
)

# Draw saved double doors correctly on screen and in office exports.
old_draw = "for(const door of state.doors)drawDoor(ctx,map(door.a),map(door.b),Math.max(1,state.wallWidth*.85),door.side||1);"
new_draw = "for(const door of state.doors){const a=map(door.a),b=map(door.b),w=Math.max(1,state.wallWidth*.85);door.double?drawDoubleDoor(ctx,a,b,w,door.side||1):drawDoor(ctx,a,b,w,door.side||1)}"
rep(old_draw, new_draw, 'onscreen door rendering')
old_export = "for(const door of d.doors)drawDoor(x,map(door.a),map(door.b),Math.max(.75,(d.wallWidth||3)*.85*W/1600),door.side||1);"
new_export = "for(const door of d.doors){const a=map(door.a),b=map(door.b),w=Math.max(.75,(d.wallWidth||3)*.85*W/1600);door.double?drawDoubleDoor(x,a,b,w,door.side||1):drawDoor(x,a,b,w,door.side||1)}"
rep(old_export, new_export, 'export door rendering')

# Live orange preview must use exactly the same side as final placement.
rep(
    "if(tool==='door')drawDoor(ctx,a,b,Math.max(1,state.wallWidth*.85),drawing.side||1,'#f59e0b');else if(tool==='window')",
    "if(tool==='door'||tool==='doubleDoor'){const fn=tool==='doubleDoor'?drawDoubleDoor:drawDoor;fn(ctx,a,b,Math.max(1,state.wallWidth*.85),drawing.side||1,'#f59e0b')}else if(tool==='window')",
    'door preview renderer'
)
rep(
    "if(tool==='door')drawing.side=doorSideFromPointer(w,q,e.clientX,e.clientY);draw()",
    "if(tool==='door'||tool==='doubleDoor')drawing.side=doorSideFromPointer(w,q,e.clientX,e.clientY);draw()",
    'door preview side tracking'
)

# Make the full double-door graphic selectable/deletable, including the second leaf and arc.
old_hit = "else if(ref.type==='doors'){const a=map(o.a),b=map(o.b),dx=b.x-a.x,dy=b.y-a.y,side=o.side||1,leaf={x:a.x-dy*side,y:a.y+dx*side};d=Math.min(segDistPx(click,a,b),segDistPx(click,a,leaf));let prev=b;for(let i=1;i<=24;i++){const t=Math.PI/2*i/24,next={x:a.x+dx*Math.cos(t)-dy*side*Math.sin(t),y:a.y+dy*Math.cos(t)+dx*side*Math.sin(t)};d=Math.min(d,segDistPx(click,prev,next));prev=next}}else if(['windows','shutters'].includes(ref.type))"
new_hit = "else if(ref.type==='doors'){const a=map(o.a),b=map(o.b),dx=b.x-a.x,dy=b.y-a.y,side=o.side||1;if(o.double){const m={x:(a.x+b.x)/2,y:(a.y+b.y)/2},hx=dx/2,hy=dy/2,leafA={x:a.x-hy*side,y:a.y+hx*side},leafB={x:b.x-hy*side,y:b.y+hx*side};d=Math.min(segDistPx(click,a,b),segDistPx(click,a,leafA),segDistPx(click,b,leafB));let p1=m,p2=m;for(let i=1;i<=24;i++){const t=Math.PI/2*i/24,n1={x:a.x+hx*Math.cos(t)-hy*side*Math.sin(t),y:a.y+hy*Math.cos(t)+hx*side*Math.sin(t)},n2={x:b.x-hx*Math.cos(t)-hy*side*Math.sin(t),y:b.y-hy*Math.cos(t)+hx*side*Math.sin(t)};d=Math.min(d,segDistPx(click,p1,n1),segDistPx(click,p2,n2));p1=n1;p2=n2}}else{const leaf={x:a.x-dy*side,y:a.y+dx*side};d=Math.min(segDistPx(click,a,b),segDistPx(click,a,leaf));let prev=b;for(let i=1;i<=24;i++){const t=Math.PI/2*i/24,next={x:a.x+dx*Math.cos(t)-dy*side*Math.sin(t),y:a.y+dy*Math.cos(t)+dx*side*Math.sin(t)};d=Math.min(d,segDistPx(click,prev,next));prev=next}}}else if(['windows','shutters'].includes(ref.type))"
rep(old_hit, new_hit, 'double door hit testing')

# Properties should identify a double door clearly.
rep(
    "$('propKind').textContent=refNames[ref.type]||ref.type;",
    "$('propKind').textContent=(ref.type==='doors'&&o.double)?'Double door':(refNames[ref.type]||ref.type);",
    'double door properties label'
)

# Circular-room preview.
ellipse_preview = """if(!navMode&&drawing&&tool==='layoutEllipse'){const a=map(drawing.start),b=map(drawing.now),cx=(a.x+b.x)/2,cy=(a.y+b.y)/2,rx=Math.abs(b.x-a.x)/2,ry=Math.abs(b.y-a.y)/2;ctx.save();ctx.strokeStyle='#172333';ctx.lineWidth=state.wallWidth;ctx.setLineDash([7,5]);ctx.beginPath();ctx.ellipse(cx,cy,rx,ry,0,0,Math.PI*2);ctx.stroke();ctx.restore()}\n"""
marker = "if(poly.length){const z=tool==='poly'?state.zones.find(z=>z.id===selected):null;"
if marker not in text:
    raise SystemExit('v0.20 patch marker missing: ellipse preview insertion')
text = text.replace(marker, ellipse_preview + marker, 1)

# Circular room participates in normal drag lifecycle.
rep(
    "if(tool==='layoutRect'){const p=inputPoint(e.clientX,e.clientY);drawing={start:p,now:p};return}",
    "if(tool==='layoutRect'||tool==='layoutEllipse'){const p=inputPoint(e.clientX,e.clientY);drawing={start:p,now:p};return}",
    'ellipse pointer down'
)
rep(
    "else if((tool==='rect'||tool==='layoutRect'||tool==='stairs')&&drawing){drawing.now=inputPoint(e.clientX,e.clientY);draw()}",
    "else if((tool==='rect'||tool==='layoutRect'||tool==='layoutEllipse'||tool==='stairs')&&drawing){drawing.now=inputPoint(e.clientX,e.clientY);draw()}",
    'ellipse pointer move'
)

old_rect_finish = "else if(tool==='layoutRect'&&drawing){const a=drawing.start,b=inputPoint(e.clientX,e.clientY);drawing=null;const dx=Math.abs(a.x-b.x),dy=Math.abs(a.y-b.y);if(dx>.012&&dy>.012){push();const pts=[a,{x:b.x,y:a.y},b,{x:a.x,y:b.y}];for(let i=0;i<4;i++)addWallSegment(pts[i],pts[(i+1)%4]);mergeOverlappingWalls();changed()}else draw()}\nelse if(tool==='poly'||tool==='layoutPoly')"
new_rect_finish = "else if(tool==='layoutRect'&&drawing){const a=drawing.start,b=inputPoint(e.clientX,e.clientY);drawing=null;const dx=Math.abs(a.x-b.x),dy=Math.abs(a.y-b.y);if(dx>.012&&dy>.012){push();const pts=[a,{x:b.x,y:a.y},b,{x:a.x,y:b.y}];for(let i=0;i<4;i++)addWallSegment(pts[i],pts[(i+1)%4]);mergeOverlappingWalls();changed()}else draw()}\nelse if(tool==='layoutEllipse'&&drawing){const a=drawing.start,b=inputPoint(e.clientX,e.clientY);drawing=null;const dx=Math.abs(a.x-b.x),dy=Math.abs(a.y-b.y);if(dx>.018&&dy>.018){push();const cx=(a.x+b.x)/2,cy=(a.y+b.y)/2,rx=dx/2,ry=dy/2,steps=32,gid=uid(),pts=[];for(let i=0;i<steps;i++){const t=Math.PI*2*i/steps;pts.push({x:cx+rx*Math.cos(t),y:cy+ry*Math.sin(t)})}for(let i=0;i<steps;i++)addWallSegment(pts[i],pts[(i+1)%steps],gid);mergeOverlappingWalls();changed();setHint('Circular room created · wall sections can take doors and windows');setTimeout(hint,1000)}else{setHint('Drag a larger circle or oval');setTimeout(hint,1000);draw()}}\nelse if(tool==='poly'||tool==='layoutPoly')"
rep(old_rect_finish, new_rect_finish, 'ellipse placement')

# Double-door placement and minimum opening size.
rep(
    "minPx=kind==='shutter'?28:18;if(openingPx<minPx)",
    "minPx=kind==='shutter'?28:kind==='doubleDoor'?34:18;if(openingPx<minPx)",
    'double door minimum size'
)
rep(
    "const side=kind==='door'?doorSideFromPointer(w,q,e.clientX,e.clientY):1;push();",
    "const side=(kind==='door'||kind==='doubleDoor')?doorSideFromPointer(w,q,e.clientX,e.clientY):1;push();",
    'double door final side'
)
rep(
    "setHint(kind==='door'?'Door placed':kind==='window'?'Window placed':'Roller shutter placed');",
    "setHint(kind==='door'?'Door placed':kind==='doubleDoor'?'Double door placed':kind==='window'?'Window placed':'Roller shutter placed');",
    'double door placed message'
)

# Copy-floor description should include all wall-opening objects.
text = text.replace(
    'Copies walls, doors, windows, stairs and room labels onto a blank plan.',
    'Copies walls, doors, double doors, windows, shutters, stairs and room labels onto a blank plan.',
    1
)

# Release-identifying metadata for testers.
text = text.replace('<title>Zone Sketch — site draft</title>', '<title>Zone Sketch v0.20 — site survey draft</title>', 1)

# Keep browser, standalone and Android copies byte-identical.
for p in paths:
    p.write_text(text)

# Android version bump.
build = ROOT/'app/build.gradle'
b = build.read_text()
if "versionCode 19" not in b or "versionName '0.19'" not in b:
    raise SystemExit('v0.20 expected Android v0.19 baseline was not found')
b = b.replace('versionCode 19', 'versionCode 20', 1).replace("versionName '0.19'", "versionName '0.20'", 1)
build.write_text(b)

print('Applied Zone Sketch v0.20 public tester upgrade')
