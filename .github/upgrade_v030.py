from pathlib import Path

ROOT = Path('.')
html_paths = [
    ROOT/'index.html',
    ROOT/'ZoneSketch.html',
    ROOT/'Zone-Sketch-by-Will.html',
    ROOT/'app/src/main/assets/index.html',
]

text = html_paths[0].read_text()
if 'Zone Sketch by Will v0.29' not in text:
    raise SystemExit('v0.30 expected v0.29 HTML baseline was not found')

# Keep the old zone DOM for saved-project/backward compatibility, but remove the
# visual barrier completely. Zones are managed from the existing bottom Zone menu.
css = r'''

/* v0.30 — full-canvas zone workflow: no permanent Zones side/bottom barrier. */
#zoneSide{display:none!important}
#zonesPanelBtn,#closeZones{display:none!important}
.workspace{width:100%}
.canvasWrap{width:100%;flex:1 1 auto}
'''
if 'v0.30 — full-canvas zone workflow' not in text:
    if '</style>' not in text:
        raise SystemExit('v0.30 could not find closing style tag')
    text = text.replace('</style>', css + '\n</style>', 1)

# Zone Box gets a wall-aware corner snap. Endpoints take priority, then the X/Y
# axes can independently align to near-vertical/horizontal walls. This lets a
# roughly dragged rectangular zone lock neatly to room walls/corners.
helper = r'''
function snapZoneCorner(p,maxPx=18){
  const base=snapGridPoint(p),P=screenPoint(base);
  let endpoint=null,xHit=null,yHit=null,wallHit=null;
  for(const w of state.walls){
    if(w.kind!=='wall'||w.points?.length!==2)continue;
    const a=w.points[0],b=w.points[1],A=screenPoint(a),B=screenPoint(b);
    for(const ep of [a,b]){
      const E=screenPoint(ep),d=Math.hypot(P.x-E.x,P.y-E.y);
      if(d<=maxPx&&(!endpoint||d<endpoint.d))endpoint={p:{...ep},d};
    }
    const q=proj(base,a,b),Q=screenPoint(q.p),d=Math.hypot(P.x-Q.x,P.y-Q.y);
    if(d>maxPx)continue;
    if(!wallHit||d<wallHit.d)wallHit={p:q.p,d};
    const dx=Math.abs(B.x-A.x),dy=Math.abs(B.y-A.y);
    if(dx<=Math.max(3,dy*.18)&&(!xHit||d<xHit.d))xHit={value:q.p.x,d};
    if(dy<=Math.max(3,dx*.18)&&(!yHit||d<yHit.d))yHit={value:q.p.y,d};
  }
  if(endpoint){snapGuide={p:endpoint.p,kind:'END'};return endpoint.p}
  if(xHit||yHit){
    const out={...base};
    if(xHit)out.x=xHit.value;
    if(yHit)out.y=yHit.value;
    snapGuide={p:out,kind:xHit&&yHit?'CORNER':'WALL'};
    return out;
  }
  if(wallHit){snapGuide={p:wallHit.p,kind:'WALL'};return wallHit.p}
  snapGuide=null;
  return base;
}
'''
if 'function snapZoneCorner(' not in text:
    marker='function nearestWallEnd(clientX,clientY,maxPx=28)'
    if marker not in text:
        raise SystemExit('v0.30 could not find wall snapping insertion point')
    text=text.replace(marker,helper+'\n'+marker,1)

old="if(tool==='rect'){if(!selected){openModal();return}const p=inputPoint(e.clientX,e.clientY);drawing={start:p,now:p};return}"
new="if(tool==='rect'){if(!selected){openModal();return}const p=snapZoneCorner(inputPoint(e.clientX,e.clientY));drawing={start:p,now:p};return}"
if old not in text:
    raise SystemExit('v0.30 could not patch Zone Box pointer-down snapping')
text=text.replace(old,new,1)

old="else if((tool==='rect'||tool==='layoutRect'||tool==='layoutEllipse'||tool==='corridor'||tool==='layoutL'||tool==='stairs')&&drawing){drawing.now=inputPoint(e.clientX,e.clientY);draw()}"
new="else if(tool==='rect'&&drawing){drawing.now=snapZoneCorner(inputPoint(e.clientX,e.clientY));draw()}else if((tool==='layoutRect'||tool==='layoutEllipse'||tool==='corridor'||tool==='layoutL'||tool==='stairs')&&drawing){drawing.now=inputPoint(e.clientX,e.clientY);draw()}"
if old not in text:
    raise SystemExit('v0.30 could not patch Zone Box pointer-move snapping')
text=text.replace(old,new,1)

old="if(tool==='rect'&&drawing){const a=drawing.start,b=inputPoint(e.clientX,e.clientY);drawing=null;"
new="if(tool==='rect'&&drawing){const a=drawing.start,b=snapZoneCorner(inputPoint(e.clientX,e.clientY));drawing=null;"
if old not in text:
    raise SystemExit('v0.30 could not patch Zone Box pointer-up snapping')
text=text.replace(old,new,1)

old="rect:'Drag a box over the selected zone area'"
new="rect:'Drag a zone box · corners and edges snap to nearby building walls'"
if old not in text:
    raise SystemExit('v0.30 could not update Zone Box hint')
text=text.replace(old,new,1)

# Only update visible release/version strings; preserve comments documenting the
# v0.28 Safari lock and v0.29 compatibility fix.
text=text.replace('<title>Zone Sketch by Will v0.29 — site survey draft</title>', '<title>Zone Sketch by Will v0.30 — site survey draft</title>', 1)
text=text.replace('ON SITE ZONE PLANNER · v0.29', 'ON SITE ZONE PLANNER · v0.30', 1)

for path in html_paths:
    path.write_text(text)

build = ROOT/'app/build.gradle'
b = build.read_text()
if 'versionCode 29' not in b or "versionName '0.29'" not in b:
    raise SystemExit('v0.30 expected Android v0.29 baseline was not found')
b = b.replace('versionCode 29', 'versionCode 30', 1)
b = b.replace("versionName '0.29'", "versionName '0.30'", 1)
build.write_text(b)

print('Applied v0.30 full-canvas zones workflow and wall-snapping Zone Box')
