from pathlib import Path

p=Path('index.html')
t=p.read_text()

def once(old,new,label):
    global t
    if new in t and old not in t:
        return
    if old not in t:
        raise SystemExit(f'v0.44 fit patch marker missing: {label}')
    t=t.replace(old,new,1)

# Bump the web build.
t=t.replace('v0.43','v0.44')

# Use more of the available board so Circuit Builder feels zoomed-to-fit rather
# than artificially spread out.
once("const CB_ROUTE_GRID=20,CB_INSET=.08,CB_SPAN=.84,CB_COLORS=",
     "const CB_ROUTE_GRID=20,CB_INSET=.045,CB_SPAN=.91,CB_DEVICE_R=11,CB_PANEL_R=16,CB_COLORS=",
     'fit constants')

# Always include the FAP/panel, selected devices and the relevant zone geometry
# in the crop. This keeps the panel in its true relative location instead of
# clamping it to the edge of a zone-only crop.
once("function cbBoundsFor(zoneId,devices,panel){const zpts=zoneId?cbZoneShapes(zoneId).flatMap(s=>s.points):[];return cbBounds(zpts.length?zpts:[...devices,panel].filter(Boolean),zoneId?.05:.08)}",
     "function cbBoundsFor(zoneId,devices,panel){const zpts=zoneId?cbZoneShapes(zoneId).flatMap(s=>s.points):[],focus=[...zpts,...devices,panel].filter(Boolean);return cbBounds(focus.length?focus:[...devices,panel].filter(Boolean),.04)}",
     'panel-aware fit bounds')

# Preserve the actual Survey layout. The third mode now zooms that area to fit
# instead of pushing detectors around. This makes the wiring game easier to map
# back to the real building in your head.
start="function cbMakeLayout(ids,bounds){const layout={},anchors={};for(const id of ids){const s=cbSymbol(id);if(!s)continue;layout[id]=anchors[id]=cbPlanToBoard(s,bounds)}const keys=Object.keys(layout),gap=Math.max(.05,Math.min(.09,.36/Math.sqrt(Math.max(1,keys.length))));for(let pass=0;pass<24;pass++){for(let i=0;i<keys.length;i++)for(let j=i+1;j<keys.length;j++){const a=layout[keys[i]],b=layout[keys[j]],dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy);if(d<gap){const ang=d<.0001?(i*1.7+j*.9):Math.atan2(dy,dx),push=(gap-Math.max(d,.001))*.42,px=Math.cos(ang)*push,py=Math.sin(ang)*push;a.x-=px;a.y-=py;b.x+=px;b.y+=py}}for(const id of keys){const p=layout[id],a=anchors[id];p.x+=((a.x-p.x)*.12);p.y+=((a.y-p.y)*.12);p.x=clamp(p.x,Math.max(.045,a.x-.075),Math.min(.955,a.x+.075));p.y=clamp(p.y,Math.max(.045,a.y-.075),Math.min(.955,a.y+.075))}}return layout}"
replacement="function cbMakeLayout(ids,bounds){const layout={};for(const id of ids){const s=cbSymbol(id);if(s)layout[id]=cbPlanToBoard(s,bounds)}return layout}"
once(start,replacement,'preserve survey layout')

# Existing empty circuits from v0.43 can be safely re-fitted when opened. Once
# a wire has been drawn, its stored geometry is left alone.
once("function cbOpenCircuit(c){cbCircuit=c;cbDrag=null;cbHover=null;cbSelection.clear();",
     "function cbOpenCircuit(c){if(!(c.legs||[]).length&&!c.complete){const devices=(c.deviceIds||[]).map(cbSymbol).filter(Boolean),panel=cbSymbol(c.panelId);c.bounds=cbBoundsFor(c.zoneId,devices,panel);c.layout=cbMakeLayout([c.panelId,...c.deviceIds],c.bounds)}cbCircuit=c;cbDrag=null;cbHover=null;cbSelection.clear();",
     'refit empty circuits')

# Smaller symbols leave much more visible cable between devices, while the hit
# target remains 30px so it is still easy to use with a finger.
once("cbDrawNode(x,s,p,s.type==='panel'?20:17,ring,cbScreen==='select'&&s.type==='panel')",
     "cbDrawNode(x,s,p,s.type==='panel'?CB_PANEL_R:CB_DEVICE_R,ring,cbScreen==='select'&&s.type==='panel')",
     'smaller circuit nodes')

p.write_text(t)
for q in [Path('ZoneSketch.html'),Path('Zone-Sketch-by-Will.html'),Path('app/src/main/assets/index.html')]:
    q.write_text(t)

g=Path('app/build.gradle')
gt=g.read_text().replace('versionCode 44','versionCode 45').replace("versionName '0.43'","versionName '0.44'")
g.write_text(gt)
print('Applied v0.44 Circuit Builder fit/panel/device-size refinements')
