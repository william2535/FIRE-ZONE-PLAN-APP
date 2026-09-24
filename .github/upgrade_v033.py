from pathlib import Path

ROOT = Path('.')
html_paths = [
    ROOT/'index.html',
    ROOT/'ZoneSketch.html',
    ROOT/'Zone-Sketch-by-Will.html',
    ROOT/'app/src/main/assets/index.html',
]

text = html_paths[0].read_text()
if 'Zone Sketch by Will v0.32' not in text:
    raise SystemExit('v0.33 expected v0.32 HTML baseline was not found')

# Render all zones into one fully opaque temporary layer, then apply the visual
# transparency once when that layer is composited onto the plan. This prevents
# repeated/overlapping zone polygons from stacking alpha and becoming darker.
old_shape = "function shape(c,pts,color,num,line=1.4,fill=true){c.save();c.beginPath();pts.forEach((p,i)=>i?c.lineTo(p.x,p.y):c.moveTo(p.x,p.y));c.closePath();if(fill){c.globalAlpha=.14;c.fillStyle=color;c.fill()}c.restore()}"
new_shape = "function shape(c,pts,color,num,line=1.4,fill=true){c.save();c.beginPath();pts.forEach((p,i)=>i?c.lineTo(p.x,p.y):c.moveTo(p.x,p.y));c.closePath();if(fill){c.globalAlpha=.14;c.fillStyle=color;c.fill()}c.restore()}\nfunction drawZoneLayer(c,shapes,zones,map,alpha=.14){if(!shapes?.length)return;const layer=document.createElement('canvas');layer.width=c.canvas.width;layer.height=c.canvas.height;const x=layer.getContext('2d'),t=c.getTransform();x.setTransform(t.a,t.b,t.c,t.d,t.e,t.f);for(const sh of shapes){const z=zones.find(z=>z.id===sh.zone);if(!z||!sh.points||sh.points.length<3)continue;const pts=sh.points.map(map);x.beginPath();pts.forEach((p,i)=>i?x.lineTo(p.x,p.y):x.moveTo(p.x,p.y));x.closePath();x.globalAlpha=1;x.fillStyle=z.color;x.fill()}c.save();c.setTransform(1,0,0,1,0,0);c.globalAlpha=alpha;c.drawImage(layer,0,0);c.restore()}"
if old_shape not in text:
    raise SystemExit('v0.33 could not find v0.32 zone shape renderer')
text = text.replace(old_shape, new_shape, 1)

old_live = "if(state.layers.zones!==false)for(const sh of state.shapes){const z=state.zones.find(z=>z.id===sh.zone);if(z&&sh.points.length>2)shape(ctx,sh.points.map(map),z.color,z.number,1.4,true)}"
new_live = "if(state.layers.zones!==false){const zonePaint=state.shapes.slice();if(!navMode&&drawing&&tool==='rect'&&selected){const a=drawing.start,b=drawing.now;zonePaint.push({zone:selected,points:[a,{x:b.x,y:a.y},b,{x:a.x,y:b.y}]})}if(!navMode&&tool==='poly'&&poly.length>=3&&selected)zonePaint.push({zone:selected,points:poly});drawZoneLayer(ctx,zonePaint,state.zones,map,.14)}"
if old_live not in text:
    raise SystemExit('v0.33 could not find live zone drawing loop')
text = text.replace(old_live, new_live, 1)

old_rect_preview = "if(!navMode&&drawing&&tool==='rect'){const z=state.zones.find(z=>z.id===selected);if(z){const a=drawing.start,b=drawing.now;shape(ctx,[a,{x:b.x,y:a.y},b,{x:a.x,y:b.y}].map(map),z.color,z.number,1.4,true)}}\n"
if old_rect_preview not in text:
    raise SystemExit('v0.33 could not find Zone Box preview renderer')
text = text.replace(old_rect_preview, '', 1)

old_poly = "if(poly.length){const pts=poly.map(map);if(tool==='poly'){const z=state.zones.find(z=>z.id===selected);ctx.save();ctx.fillStyle=z?.color||'#ee3333';if(pts.length>=3){ctx.globalAlpha=.14;ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.closePath();ctx.fill()}else{ctx.globalAlpha=.55;for(const p of pts){ctx.beginPath();ctx.arc(p.x,p.y,4,0,Math.PI*2);ctx.fill()}}ctx.restore()}else{ctx.save();ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.strokeStyle='#172333';ctx.lineWidth=state.wallWidth;ctx.setLineDash([7,5]);ctx.stroke();ctx.restore()}}"
new_poly = "if(poly.length){const pts=poly.map(map);if(tool==='poly'){if(pts.length<3){const z=state.zones.find(z=>z.id===selected);ctx.save();ctx.globalAlpha=.55;ctx.fillStyle=z?.color||'#ee3333';for(const p of pts){ctx.beginPath();ctx.arc(p.x,p.y,4,0,Math.PI*2);ctx.fill()}ctx.restore()}}else{ctx.save();ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.strokeStyle='#172333';ctx.lineWidth=state.wallWidth;ctx.setLineDash([7,5]);ctx.stroke();ctx.restore()}}"
if old_poly not in text:
    raise SystemExit('v0.33 could not find polygon zone preview renderer')
text = text.replace(old_poly, new_poly, 1)

old_export = "for(const sh of d.shapes){const z=d.zones.find(z=>z.id===sh.zone);if(z&&sh.points.length>2)shape(x,sh.points.map(map),z.color,z.number,Math.max(1.4,W/1800),true)}"
new_export = "drawZoneLayer(x,d.shapes,d.zones,map,.14)"
if old_export not in text:
    raise SystemExit('v0.33 could not find export zone drawing loop')
text = text.replace(old_export, new_export, 1)

marker = "\n\n/* v0.33 — zone transparency is composited once, so overlaps never darken. */\n"
if 'v0.33 — zone transparency is composited once' not in text:
    text = text.replace('</style>', marker + '</style>', 1)

text = text.replace('<title>Zone Sketch by Will v0.32 — site survey draft</title>', '<title>Zone Sketch by Will v0.33 — site survey draft</title>', 1)
text = text.replace('ON SITE ZONE PLANNER · v0.32', 'ON SITE ZONE PLANNER · v0.33', 1)

for path in html_paths:
    path.write_text(text)

build = ROOT/'app/build.gradle'
b = build.read_text()
if 'versionCode 32' not in b or "versionName '0.32'" not in b:
    raise SystemExit('v0.33 expected Android v0.32 baseline was not found')
b = b.replace('versionCode 32', 'versionCode 33', 1)
b = b.replace("versionName '0.32'", "versionName '0.33'", 1)
build.write_text(b)

print('Applied v0.33: zone overlaps keep constant transparency')
