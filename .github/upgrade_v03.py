from pathlib import Path

FILES = [
    Path('index.html'),
    Path('ZoneSketch.html'),
    Path('app/src/main/assets/index.html'),
]


def rep(s, old, new, label):
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    return s.replace(old, new, 1)


def upgrade(s):
    if 'data-tool="door"' in s and 'data-tool="erase"' in s:
        return s

    s = rep(s,
        ".tools button.primary{background:#ec493b;color:white}.tools .divider",
        ".tools button.primary{background:#ec493b;color:white}.tools button.danger.active{background:#a52b2b;color:#fff}.tools .divider",
        'danger css')

    s = rep(s,
        '<p class="help">Choose a zone, then drag a box over its area. For irregular rooms, tap Outline and mark the corners. Repeat for disconnected areas.</p>',
        '<p class="help">Choose a zone, then drag a box over its area. Use Outline for irregular areas. Door adds a swing symbol. Room label adds clean room names. Delete removes one tapped item.</p>',
        'help text')

    s = rep(s,
        '<button data-tool="wall">Wall line</button><button data-tool="pen">Pen</button><button data-tool="rect" class="active">▭ Box</button>',
        '<button data-tool="wall">Wall line</button><button data-tool="pen">Pen</button><button data-tool="door">Door</button><button data-tool="room">Room label</button><button data-tool="rect" class="active">▭ Box</button>',
        'door and room buttons')

    s = rep(s,
        '<button data-tool="note">＋ Note</button><button data-tool="pan">✋ Move plan</button>',
        '<button data-tool="note">＋ Note</button><button data-tool="erase" class="danger">⌫ Delete</button><button data-tool="pan">✋ Move plan</button>',
        'delete button')

    s = rep(s,
        "const fresh=()=>({site:'',zones:[],shapes:[],notes:[],walls:[],pictureOpacity:1,pictureVisible:true,isBlank:false});",
        "const fresh=()=>({site:'',zones:[],shapes:[],notes:[],walls:[],doors:[],labels:[],pictureOpacity:1,pictureVisible:true,isBlank:false});",
        'state arrays')

    stroke = "function stroke(c,points,width){if(points.length<2)return;c.save();c.beginPath();points.forEach((p,i)=>i?c.lineTo(p.x,p.y):c.moveTo(p.x,p.y));c.strokeStyle='#172333';c.lineWidth=width;c.lineCap='round';c.lineJoin='round';c.stroke();c.restore()}"
    helpers = stroke + "\n" + r"""function doorSymbol(c,a,b,width=3){const dx=b.x-a.x,dy=b.y-a.y,r=Math.hypot(dx,dy);if(r<2)return;const ang=Math.atan2(dy,dx);c.save();c.strokeStyle='#172333';c.lineWidth=width;c.lineCap='round';c.beginPath();c.moveTo(a.x,a.y);c.lineTo(b.x,b.y);c.stroke();c.beginPath();c.arc(a.x,a.y,r,ang,ang+Math.PI/2,false);c.strokeStyle='#657789';c.lineWidth=Math.max(1.5,width*.7);c.stroke();c.fillStyle='#172333';c.beginPath();c.arc(a.x,a.y,Math.max(2,width),0,Math.PI*2);c.fill();c.restore()}
function roomLabel(c,x,y,text,size=16){c.save();c.font=`600 ${size}px system-ui`;const pad=7,w=c.measureText(text).width+pad*2,h=size+10;c.fillStyle='#ffffffee';c.strokeStyle='#7a8795';c.lineWidth=1;c.beginPath();if(c.roundRect)c.roundRect(x-w/2,y-h/2,w,h,6);else c.rect(x-w/2,y-h/2,w,h);c.fill();c.stroke();c.fillStyle='#182332';c.textAlign='center';c.textBaseline='middle';c.fillText(text,x,y);c.restore()}"""
    s = rep(s, stroke, helpers, 'drawing helpers')

    s = rep(s,
        "function hint(){if(!img){setHint('');return}setHint(tool==='wall'?'Drag to draw a wall line · near-straight lines snap':tool==='pen'?'Draw with your finger or stylus':tool==='rect'?'Drag a box over a zone area':tool==='poly'?'Tap zone corners, then Finish outline':tool==='note'?'Tap the plan to add a note':'Drag to move · pinch to zoom')}",
        "function hint(){if(!img){setHint('');return}const h={wall:'Drag to draw a wall line · near-straight lines snap',pen:'Draw freehand with your finger or stylus',door:'Drag from the hinge to the door edge',room:'Tap where the room name should go',rect:'Drag a box over a zone area',poly:'Tap zone corners, then Finish outline',note:'Tap to add a note for the office',erase:'Tap an item to delete it · Undo restores it',pan:'Drag to move · pinch to zoom'};setHint(h[tool]||'')}",
        'tool hints')

    s = rep(s,
        "function point(x,y){const r=canvas.getBoundingClientRect(),v=transform();return {x:Math.max(0,Math.min(1,(x-r.left-v.ox)/(img.width*v.s))),y:Math.max(0,Math.min(1,(y-r.top-v.oy)/(img.height*v.s)))}}",
        "function point(x,y){const r=canvas.getBoundingClientRect(),v=transform();return {x:Math.max(0,Math.min(1,(x-r.left-v.ox)/(img.width*v.s))),y:Math.max(0,Math.min(1,(y-r.top-v.oy)/(img.height*v.s)))}}\nfunction screenPoint(p){const v=transform();return{x:v.ox+p.x*img.width*v.s,y:v.oy+p.y*img.height*v.s}}",
        'screen point')

    s = rep(s,
        "for(const wall of state.walls)stroke(ctx,wall.points.map(map),Math.max(2,3*Math.min(zoom,2)));",
        "for(const wall of state.walls)stroke(ctx,wall.points.map(map),Math.max(2,3*Math.min(zoom,2)));\nfor(const d of state.doors)doorSymbol(ctx,map(d.a),map(d.b),Math.max(2,3*Math.min(zoom,2)));\nfor(const l of state.labels){const p=map(l);roomLabel(ctx,p.x,p.y,l.text,Math.max(13,16*Math.min(zoom,1.5)))}",
        'draw saved door labels')

    s = rep(s,
        "if(drawing&&tool==='wall')stroke(ctx,[drawing.start,drawing.now].map(map),3);",
        "if(drawing&&tool==='wall')stroke(ctx,[drawing.start,drawing.now].map(map),3);\nif(drawing&&tool==='door')doorSymbol(ctx,map(drawing.start),map(drawing.now),3);",
        'door preview')

    s = rep(s,
        "state.shapes=[];state.notes=[];state.walls=[];state.isBlank=false;",
        "state.shapes=[];state.notes=[];state.walls=[];state.doors=[];state.labels=[];state.isBlank=false;",
        'clear new items')

    marker = "document.querySelectorAll('[data-tool]').forEach(b=>b.onclick=()=>setTool(b.dataset.tool));\n"
    erase_helpers = marker + r"""function distSeg(p,a,b){const vx=b.x-a.x,vy=b.y-a.y,l2=vx*vx+vy*vy;if(!l2)return Math.hypot(p.x-a.x,p.y-a.y);let t=((p.x-a.x)*vx+(p.y-a.y)*vy)/l2;t=Math.max(0,Math.min(1,t));return Math.hypot(p.x-(a.x+t*vx),p.y-(a.y+t*vy))}
function pointInPoly(p,pts){let inside=false;for(let i=0,j=pts.length-1;i<pts.length;j=i++){const a=pts[i],b=pts[j],hit=((a.y>p.y)!==(b.y>p.y))&&(p.x<(b.x-a.x)*(p.y-a.y)/(b.y-a.y||1e-9)+a.x);if(hit)inside=!inside}return inside}
function eraseAt(clientX,clientY){const r=canvas.getBoundingClientRect(),sp={x:clientX-r.left,y:clientY-r.top},near=(p,px=34)=>{const q=screenPoint(p);return Math.hypot(sp.x-q.x,sp.y-q.y)<=px};for(let i=state.labels.length-1;i>=0;i--)if(near(state.labels[i],45)){push();state.labels.splice(i,1);changed();return}for(let i=state.notes.length-1;i>=0;i--)if(near(state.notes[i],45)){push();state.notes.splice(i,1);changed();return}for(let i=state.doors.length-1;i>=0;i--){const a=screenPoint(state.doors[i].a),b=screenPoint(state.doors[i].b);if(distSeg(sp,a,b)<28||near(centre([state.doors[i].a,state.doors[i].b]),34)){push();state.doors.splice(i,1);changed();return}}for(let i=state.walls.length-1;i>=0;i--){const pts=state.walls[i].points.map(screenPoint);for(let j=1;j<pts.length;j++)if(distSeg(sp,pts[j-1],pts[j])<22){push();state.walls.splice(i,1);changed();return}}for(let i=state.shapes.length-1;i>=0;i--){const pts=state.shapes[i].points.map(screenPoint);if(pointInPoly(sp,pts)){push();state.shapes.splice(i,1);changed();return}}setHint('Nothing selected · tap closer to the item');setTimeout(hint,900)}
"""
    s = rep(s, marker, erase_helpers, 'delete helpers')

    s = rep(s,
        "if(tool==='wall'){const p=point(e.clientX,e.clientY);drawing={start:p,now:p};return}",
        "if(tool==='wall'||tool==='door'){const p=point(e.clientX,e.clientY);drawing={start:p,now:p};return}",
        'door pointer down')

    s = rep(s,
        "else if(tool==='wall'&&drawing){drawing.now=snapped(drawing.start,point(e.clientX,e.clientY));draw()}else if(tool==='rect'&&drawing)",
        "else if(tool==='wall'&&drawing){drawing.now=snapped(drawing.start,point(e.clientX,e.clientY));draw()}else if(tool==='door'&&drawing){drawing.now=point(e.clientX,e.clientY);draw()}else if(tool==='rect'&&drawing)",
        'door pointer move')

    wall_up = "if((tool==='wall'||tool==='pen')&&drawing){const pts=tool==='pen'?drawing.points:[drawing.start,snapped(drawing.start,point(e.clientX,e.clientY))];drawing=null;if(pts.length>1&&pts.some(p=>Math.hypot(p.x-pts[0].x,p.y-pts[0].y)>.005)){push();state.walls.push({points:pts});changed()}else draw();return}"
    door_up = wall_up + "if(tool==='door'&&drawing){const a=drawing.start,b=point(e.clientX,e.clientY);drawing=null;if(Math.hypot(a.x-b.x,a.y-b.y)>.01){push();state.doors.push({a,b});changed()}else draw();return}"
    s = rep(s, wall_up, door_up, 'door pointer up')

    s = rep(s,
        "else if(tool==='note'){const value=prompt('Note for the office (e.g. zone boundary to confirm):');if(value?.trim()){push();state.notes.push({...point(e.clientX,e.clientY),text:value.trim().slice(0,50)});changed()}}else drawing=null",
        "else if(tool==='note'){const value=prompt('Note for the office (e.g. zone boundary to confirm):');if(value?.trim()){push();state.notes.push({...point(e.clientX,e.clientY),text:value.trim().slice(0,50)});changed()}}else if(tool==='room'){const value=prompt('Room name (e.g. Office, Canteen, Store):');if(value?.trim()){push();state.labels.push({...point(e.clientX,e.clientY),text:value.trim().slice(0,40)});changed()}}else if(tool==='erase'){eraseAt(e.clientX,e.clientY)}else drawing=null",
        'room and delete pointer up')

    s = rep(s,
        "for(const wall of state.walls)stroke(x,wall.points.map(map),Math.max(3,W/500));for(const n of state.notes)",
        "for(const wall of state.walls)stroke(x,wall.points.map(map),Math.max(3,W/500));for(const d of state.doors)doorSymbol(x,map(d.a),map(d.b),Math.max(3,W/500));for(const l of state.labels){const p=map(l);roomLabel(x,p.x,p.y,l.text,Math.max(16,W/120))}for(const n of state.notes)",
        'export new items')

    s = rep(s,
        "if(!state.shapes.length&&!state.walls.length&&!state.notes.length&&!confirm('Nothing has been drawn. Send the plan anyway?'))return;",
        "if(!state.shapes.length&&!state.walls.length&&!state.notes.length&&!state.doors.length&&!state.labels.length&&!confirm('Nothing has been drawn. Send the plan anyway?'))return;",
        'share empty check')

    return s


for path in FILES:
    original = path.read_text(encoding='utf-8')
    updated = upgrade(original)
    path.write_text(updated, encoding='utf-8')
    print(f'updated {path}: {len(original)} -> {len(updated)} bytes')

readme = Path('README.md')
r = readme.read_text(encoding='utf-8')
section = """

## Version 0.3 — doors, room labels and precise delete

- **Door**: drag from the hinge to the door edge to add a simple swing symbol for the office/CAD redraw.
- **Room label**: tap a room and type its name; labels stay readable over a faded plan and are included in PNG export.
- **Delete**: tap a wall/pen stroke, zone area, door, note or room label to remove only that item. **Undo** immediately restores accidental deletions.
- Existing Version 0.2 drafts remain compatible; new door and room-label data is simply added when used.
"""
if '## Version 0.3 — doors, room labels and precise delete' not in r:
    readme.write_text(r.rstrip() + section + '\n', encoding='utf-8')
    print('updated README.md')
