from pathlib import Path

ROOT=Path('.')
paths=[ROOT/'index.html',ROOT/'ZoneSketch.html',ROOT/'Zone-Sketch-by-Will.html',ROOT/'app/src/main/assets/index.html']
text=paths[0].read_text()

def rep(old,new,label):
    global text
    if old not in text:
        raise SystemExit(f'v0.26 marker missing: {label}')
    text=text.replace(old,new,1)

# Version / visible build identity.
rep('Zone Sketch by Will v0.25','Zone Sketch by Will v0.26','browser title')
rep('ON SITE ZONE PLANNER · v0.25','ON SITE ZONE PLANNER · v0.26','home version')

# Building menu: keep drawing-only workflow and add faster geometry cleanup tools.
rep(
'<button data-menu-tool="layoutEllipse">◯ Circular room</button><button data-menu-tool="label">Room label</button><button data-menu-tool="trim">Trim / Extend</button>',
'<button data-menu-tool="layoutEllipse">◯ Circular room</button><button data-menu-tool="corridor">▯ Corridor</button><button data-menu-tool="layoutL">⌞ L-shaped room</button><button data-menu-tool="label">Room label</button><button data-menu-tool="trim">Trim / Extend</button><button data-menu-tool="wallEnds">● Edit wall ends</button><button data-menu-tool="joinWalls">Join wall gap</button><button data-menu-tool="splitWall">Split wall</button>',
'building menu tools')

rep(
"const zoneTools=new Set(['rect','poly','fill']),layoutTools=new Set(['wall','pen','layoutRect','layoutPoly','layoutEllipse','label','quickLabel','trim']),objectTools=",
"const zoneTools=new Set(['rect','poly','fill']),layoutTools=new Set(['wall','pen','layoutRect','layoutPoly','layoutEllipse','corridor','layoutL','label','quickLabel','trim','wallEnds','joinWalls','splitWall']),objectTools=",
'tool set')

rep(
"layoutRect:'Box',layoutPoly:'Outline',layoutEllipse:'Circular room',label:'Room label',trim:'Trim / Extend',",
"layoutRect:'Box',layoutPoly:'Outline',layoutEllipse:'Circular room',corridor:'Corridor',layoutL:'L-shaped room',label:'Room label',trim:'Trim / Extend',wallEnds:'Edit wall ends',joinWalls:'Join wall gap',splitWall:'Split wall',",
'tool labels')

rep(
"layoutEllipse:'Drag an oval or circle · it becomes editable wall sections for doors and windows',label:'Tap a room and type its name',trim:'Tap near a wall end · it automatically trims or extends to the nearest intersecting wall',",
"layoutEllipse:'Drag an oval or circle · it becomes editable wall sections for doors and windows',corridor:'Drag a corridor box · it creates grouped walls and labels it Corridor',layoutL:'Drag the outside size of an L-shaped room · rotate or mirror it afterwards if needed',label:'Tap a room and type its name',trim:'Tap near a wall end · it automatically trims or extends to the nearest intersecting wall',wallEnds:'Blue dots show wall ends · drag a dot to correct that wall end',joinWalls:'Tap the wall end to move, then tap the wall end it should join to',splitWall:'Tap a wall where you want a new junction / split point',",
'tool hints')

# Allow new drawing tools in Favourite Tools.
rep(
"'tool:layoutRect':{label:'Room',kind:'tool',value:'layoutRect'},'tool:layoutEllipse':{label:'Round room',kind:'tool',value:'layoutEllipse'},'tool:door':",
"'tool:layoutRect':{label:'Room',kind:'tool',value:'layoutRect'},'tool:layoutEllipse':{label:'Round room',kind:'tool',value:'layoutEllipse'},'tool:corridor':{label:'Corridor',kind:'tool',value:'corridor'},'tool:layoutL':{label:'L-room',kind:'tool',value:'layoutL'},'tool:wallEnds':{label:'Wall ends',kind:'tool',value:'wallEnds'},'tool:joinWalls':{label:'Join walls',kind:'tool',value:'joinWalls'},'tool:splitWall':{label:'Split wall',kind:'tool',value:'splitWall'},'tool:door':",
'favourite catalogue')

# State used by two-tap Join Wall.
rep('navMode=false,tapStart=null;','navMode=false,tapStart=null,joinPending=null;','join state')

# Smart endpoint helpers and manual wall cleanup.
needle="function snapToWalls(p,maxPx=14){let best={p,d:maxPx+1};for(const w of state.walls){if(w.kind!=='wall'||w.points.length!==2)continue;for(const ep of w.points){const d=Math.hypot(screenPoint(p).x-screenPoint(ep).x,screenPoint(p).y-screenPoint(ep).y);if(d<best.d)best={p:{...ep},d}}const q=proj(p,w.points[0],w.points[1]),d=segDistScreen(p,w.points[0],w.points[1]);if(d<best.d)best={p:q.p,d}}return best.d<=maxPx?best.p:p}\n"
if needle not in text: raise SystemExit('v0.26 marker missing: snapToWalls helper')
extra="""function nearestWallEnd(clientX,clientY,maxPx=28){if(!img)return null;const r=canvas.getBoundingClientRect(),p={x:clientX-r.left,y:clientY-r.top};let best=null;for(const w of state.walls){if(w.kind!=='wall'||w.points?.length!==2)continue;for(let end=0;end<2;end++){const s=screenPoint(w.points[end]),d=Math.hypot(p.x-s.x,p.y-s.y);if(d<=maxPx&&(!best||d<best.d))best={wall:w,end,p:w.points[end],d}}}return best}\nfunction snapWallEndPoint(p,excludeId,maxPx=18){let best={p:snapGridPoint(p),d:maxPx+1};for(const w of state.walls){if(w.id===excludeId||w.kind!=='wall'||w.points?.length!==2)continue;for(const ep of w.points){const d=Math.hypot(screenPoint(p).x-screenPoint(ep).x,screenPoint(p).y-screenPoint(ep).y);if(d<best.d)best={p:{...ep},d}}const mid=lerp(w.points[0],w.points[1],.5),md=Math.hypot(screenPoint(p).x-screenPoint(mid).x,screenPoint(p).y-screenPoint(mid).y);if(md<best.d)best={p:mid,d:md};const q=proj(p,w.points[0],w.points[1]),d=segDistScreen(p,w.points[0],w.points[1]);if(d<best.d)best={p:q.p,d}}return best.d<=maxPx?best.p:snapGridPoint(p)}\nfunction joinWallTap(clientX,clientY){const hit=nearestWallEnd(clientX,clientY,34);if(!hit){joinPending=null;setHint('Tap directly on a wall END to join a gap');setTimeout(hint,1300);draw();return}if(!joinPending){joinPending={wallId:hit.wall.id,end:hit.end};setHint('First wall end selected · tap the wall end it should join to');draw();return}const first=state.walls.find(w=>w.id===joinPending.wallId);if(!first||first.kind!=='wall'||first.points?.length!==2){joinPending=null;setHint('That wall changed · choose the first wall end again');setTimeout(hint,1200);return}if(first.id===hit.wall.id&&joinPending.end===hit.end){joinPending=null;setHint('Join cancelled');draw();return}push();first.points[joinPending.end]={...hit.wall.points[hit.end]};joinPending=null;splitExistingWalls();changed();setHint('Wall gap joined');setTimeout(hint,900)}\nfunction splitWallAt(clientX,clientY){const p=point(clientX,clientY),hit=nearestWall(p,30);if(!hit){setHint('Tap directly on the wall you want to split');setTimeout(hint,1200);return}if(hit.t<.035||hit.t>.965){setHint('Tap further away from the wall end');setTimeout(hint,1200);return}const idx=state.walls.findIndex(w=>w.id===hit.wall.id),w=state.walls[idx];if(idx<0)return;push();const gid=w.group||null,a=w.points[0],b=w.points[1],m=snapGridPoint(hit.p);state.walls.splice(idx,1,{id:uid(),kind:'wall',group:gid,points:[a,m]},{id:uid(),kind:'wall',group:gid,points:[m,b]});changed();setHint('Wall split · the two sections can now be edited separately');setTimeout(hint,1000)}\nfunction rectPoints(a,b){return[a,{x:b.x,y:a.y},b,{x:a.x,y:b.y}]}\nfunction lRoomPoints(a,b){const x1=Math.min(a.x,b.x),x2=Math.max(a.x,b.x),y1=Math.min(a.y,b.y),y2=Math.max(a.y,b.y),mx=x1+(x2-x1)*.55,my=y1+(y2-y1)*.55;return[{x:x1,y:y1},{x:x2,y:y1},{x:x2,y:my},{x:mx,y:my},{x:mx,y:y2},{x:x1,y:y2}]}\nfunction addWallLoop(pts,labelText=''){const gid=uid();for(let i=0;i<pts.length;i++)addWallSegment(pts[i],pts[(i+1)%pts.length],gid);if(labelText){const c=centre(pts);state.labels.push({id:uid(),x:c.x,y:c.y,text:labelText,scale:1,group:gid})}return gid}\n"""
text=text.replace(needle,needle+extra,1)

# Pointer down: manual cleanup tools and drag-shape tools.
rep(
"if(tool==='trim'){trimExtendAt(e.clientX,e.clientY);return}if(tool==='pen')",
"if(tool==='joinWalls'){joinWallTap(e.clientX,e.clientY);return}if(tool==='splitWall'){splitWallAt(e.clientX,e.clientY);return}if(tool==='wallEnds'){const hit=nearestWallEnd(e.clientX,e.clientY,32);if(!hit){setHint('Tap a blue wall-end handle');setTimeout(hint,1000);return}drawing={mode:'wallEnd',wallId:hit.wall.id,end:hit.end,orig:{...hit.wall.points[hit.end]},startClient:{x:e.clientX,y:e.clientY},moved:false};return}if(tool==='trim'){trimExtendAt(e.clientX,e.clientY);return}if(tool==='pen')",
'pointer down manual tools')
rep(
"if(tool==='layoutRect'||tool==='layoutEllipse'){const p=inputPoint(e.clientX,e.clientY);drawing={start:p,now:p};return}",
"if(tool==='layoutRect'||tool==='layoutEllipse'||tool==='corridor'||tool==='layoutL'){const p=inputPoint(e.clientX,e.clientY);drawing={start:p,now:p};return}",
'pointer down drag rooms')

# Pointer move: wall endpoint drag and new room previews.
rep(
"}else if(tool==='pen'&&drawing){drawing.points.push(point(e.clientX,e.clientY));draw()}",
"}else if(tool==='wallEnds'&&drawing?.mode==='wallEnd'){const w=state.walls.find(x=>x.id===drawing.wallId);if(!w)return;if(!drawing.moved&&Math.hypot(e.clientX-drawing.startClient.x,e.clientY-drawing.startClient.y)>3){push();drawing.moved=true}if(drawing.moved){w.points[drawing.end]=snapWallEndPoint(inputPoint(e.clientX,e.clientY),w.id);draw()}}else if(tool==='pen'&&drawing){drawing.points.push(point(e.clientX,e.clientY));draw()}",
'pointer move wall ends')
rep(
"else if((tool==='rect'||tool==='layoutRect'||tool==='layoutEllipse'||tool==='stairs')&&drawing){drawing.now=inputPoint(e.clientX,e.clientY);draw()}",
"else if((tool==='rect'||tool==='layoutRect'||tool==='layoutEllipse'||tool==='corridor'||tool==='layoutL'||tool==='stairs')&&drawing){drawing.now=inputPoint(e.clientX,e.clientY);draw()}",
'pointer move drag rooms')

# Pointer up wall-end completion.
rep(
"if(toolLockReason(tool)){drawing=null;return}if(['symbol'",
"if(toolLockReason(tool)){drawing=null;return}if(tool==='wallEnds'&&drawing?.mode==='wallEnd'){const moved=drawing.moved;drawing=null;if(moved){splitExistingWalls();changed();setHint('Wall end moved · nearby junctions snap automatically');setTimeout(hint,900)}else draw();return}if(['symbol'",
'pointer up wall end')

# Corridor / L room final creation before circular room branch.
marker="else if(tool==='layoutEllipse'&&drawing){const a=drawing.start,b=inputPoint(e.clientX,e.clientY);drawing=null;"
if marker not in text: raise SystemExit('v0.26 marker missing: layoutEllipse finish')
insert="""else if((tool==='corridor'||tool==='layoutL')&&drawing){const a=drawing.start,b=inputPoint(e.clientX,e.clientY),kind=tool;drawing=null;const dx=Math.abs(a.x-b.x),dy=Math.abs(a.y-b.y);if(dx>.014&&dy>.014){push();const pts=kind==='corridor'?rectPoints(a,b):lRoomPoints(a,b);addWallLoop(pts,kind==='corridor'?'Corridor':'');splitExistingWalls();changed();setHint(kind==='corridor'?'Corridor created and labelled':'L-shaped room created · rotate or mirror the group if needed');setTimeout(hint,1000)}else{setHint('Drag a larger area');setTimeout(hint,1000);draw()}}\n"""
text=text.replace(marker,insert+marker,1)

# Paint previews and visible endpoint handles.
rep(
"if(state.layers.building!==false)for(const wall of state.walls)stroke(ctx,wall.points.map(map),state.wallWidth);",
"if(state.layers.building!==false)for(const wall of state.walls)stroke(ctx,wall.points.map(map),state.wallWidth);if(!navMode&&tool==='wallEnds'&&state.layers.building!==false){ctx.save();ctx.fillStyle='#fff';ctx.strokeStyle='#2576b5';ctx.lineWidth=2;for(const wall of state.walls){if(wall.kind!=='wall'||wall.points?.length!==2)continue;for(const ep of wall.points){const p=map(ep);ctx.beginPath();ctx.arc(p.x,p.y,6,0,Math.PI*2);ctx.fill();ctx.stroke()}}ctx.restore()}",
'wall endpoint handles')
rep(
"if(!navMode&&drawing&&tool==='layoutRect'){const a=map(drawing.start),b=map(drawing.now);ctx.save();ctx.strokeStyle='#172333';ctx.lineWidth=state.wallWidth;ctx.setLineDash([7,5]);ctx.strokeRect(Math.min(a.x,b.x),Math.min(a.y,b.y),Math.abs(b.x-a.x),Math.abs(b.y-a.y));ctx.restore()}",
"if(!navMode&&drawing&&(tool==='layoutRect'||tool==='corridor')){const a=map(drawing.start),b=map(drawing.now);ctx.save();ctx.strokeStyle=tool==='corridor'?'#2576b5':'#172333';ctx.lineWidth=state.wallWidth;ctx.setLineDash([7,5]);ctx.strokeRect(Math.min(a.x,b.x),Math.min(a.y,b.y),Math.abs(b.x-a.x),Math.abs(b.y-a.y));ctx.restore()}if(!navMode&&drawing&&tool==='layoutL'){const pts=lRoomPoints(drawing.start,drawing.now).map(map);ctx.save();ctx.strokeStyle='#2576b5';ctx.lineWidth=state.wallWidth;ctx.setLineDash([7,5]);ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.closePath();ctx.stroke();ctx.restore()}",
'room previews')

# Changing tools cancels a half-finished join operation.
rep("function setTool(t){if(navMode){","function setTool(t){joinPending=null;if(navMode){",'cancel pending join')

# Sync all HTML copies.
for p in paths:p.write_text(text)

# Android version.
build=ROOT/'app/build.gradle';b=build.read_text()
if 'versionCode 25' not in b or "versionName '0.25'" not in b: raise SystemExit('Expected Android v0.25 baseline')
b=b.replace('versionCode 25','versionCode 26',1).replace("versionName '0.25'","versionName '0.26'",1);build.write_text(b)
print('Applied v0.26 drawing productivity tools')
