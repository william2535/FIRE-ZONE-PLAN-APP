from pathlib import Path

ROOT = Path('.')
html_paths = [
    ROOT/'index.html',
    ROOT/'ZoneSketch.html',
    ROOT/'Zone-Sketch-by-Will.html',
    ROOT/'app/src/main/assets/index.html',
]

text = html_paths[0].read_text()
if 'Zone Sketch by Will v0.31' not in text:
    raise SystemExit('v0.32 expected v0.31 HTML baseline was not found')

# Zones should read as soft transparent areas, not coloured outlines. The shared
# shape renderer is used on-screen, during Zone Box preview and in office export,
# so removing the stroke here keeps all outputs consistent.
old_shape = "function shape(c,pts,color,num,line=1.4,fill=true){c.save();c.beginPath();pts.forEach((p,i)=>i?c.lineTo(p.x,p.y):c.moveTo(p.x,p.y));c.closePath();if(fill){c.globalAlpha=.14;c.fillStyle=color;c.fill()}c.globalAlpha=.62;c.lineWidth=line;c.strokeStyle=color;c.lineJoin='round';c.stroke();c.restore()}"
new_shape = "function shape(c,pts,color,num,line=1.4,fill=true){c.save();c.beginPath();pts.forEach((p,i)=>i?c.lineTo(p.x,p.y):c.moveTo(p.x,p.y));c.closePath();if(fill){c.globalAlpha=.14;c.fillStyle=color;c.fill()}c.restore()}"
if old_shape not in text:
    raise SystemExit('v0.32 could not find zone shape renderer')
text = text.replace(old_shape, new_shape, 1)

# A single selected zone should not gain a second full rectangular outline.
# Keep the existing resize handles so it remains easy to edit.
old_sel = "c.setLineDash([8,5]);c.fillRect(box.x,box.y,box.w,box.h);c.strokeRect(box.x,box.y,box.w,box.h);c.setLineDash([]);if(selectionCanResize())"
new_sel = "const zoneOnly=selection.length===1&&selection[0].type==='shapes';c.setLineDash([8,5]);if(!zoneOnly){c.fillRect(box.x,box.y,box.w,box.h);c.strokeRect(box.x,box.y,box.w,box.h)}c.setLineDash([]);if(selectionCanResize())"
if old_sel not in text:
    raise SystemExit('v0.32 could not find selection box renderer')
text = text.replace(old_sel, new_sel, 1)

# While creating a polygon Zone Outline, preview the translucent filled area once
# there are three points. Before that, show only small vertex dots. Building
# Outline keeps its dashed black wall preview.
old_poly = "if(poly.length){const z=tool==='poly'?state.zones.find(z=>z.id===selected):null;ctx.beginPath();poly.map(map).forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.strokeStyle=tool==='layoutPoly'?'#172333':(z?.color||'#ee3333');ctx.lineWidth=tool==='layoutPoly'?state.wallWidth:1.4;ctx.setLineDash([7,5]);ctx.stroke();ctx.setLineDash([])}"
new_poly = "if(poly.length){const pts=poly.map(map);if(tool==='poly'){const z=state.zones.find(z=>z.id===selected);ctx.save();ctx.fillStyle=z?.color||'#ee3333';if(pts.length>=3){ctx.globalAlpha=.14;ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.closePath();ctx.fill()}else{ctx.globalAlpha=.55;for(const p of pts){ctx.beginPath();ctx.arc(p.x,p.y,4,0,Math.PI*2);ctx.fill()}}ctx.restore()}else{ctx.save();ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.strokeStyle='#172333';ctx.lineWidth=state.wallWidth;ctx.setLineDash([7,5]);ctx.stroke();ctx.restore()}}"
if old_poly not in text:
    raise SystemExit('v0.32 could not find polygon preview renderer')
text = text.replace(old_poly, new_poly, 1)

# Add a stable marker for release checks.
marker = "\n\n/* v0.32 — zones are translucent fill only: no coloured zone perimeter stroke. */\n"
if 'v0.32 — zones are translucent fill only' not in text:
    text = text.replace('</style>', marker + '</style>', 1)

text = text.replace('<title>Zone Sketch by Will v0.31 — site survey draft</title>', '<title>Zone Sketch by Will v0.32 — site survey draft</title>', 1)
text = text.replace('ON SITE ZONE PLANNER · v0.31', 'ON SITE ZONE PLANNER · v0.32', 1)

for path in html_paths:
    path.write_text(text)

build = ROOT/'app/build.gradle'
b = build.read_text()
if 'versionCode 31' not in b or "versionName '0.31'" not in b:
    raise SystemExit('v0.32 expected Android v0.31 baseline was not found')
b = b.replace('versionCode 31', 'versionCode 32', 1)
b = b.replace("versionName '0.31'", "versionName '0.32'", 1)
build.write_text(b)

print('Applied v0.32: fill-only zones with no coloured perimeter outlines')
