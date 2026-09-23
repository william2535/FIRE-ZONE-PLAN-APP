from pathlib import Path

FILES = [Path('index.html'), Path('ZoneSketch.html'), Path('app/src/main/assets/index.html')]


def rep(s, old, new, label, count=1):
    n = s.count(old)
    if n < count:
        raise SystemExit(f'{label}: expected at least {count} match(es), found {n}')
    return s.replace(old, new, count)


def upgrade(s):
    if 'id="objectMenuBtn"' in s and 'function enclosedFaceAt' in s:
        print('v0.9 already applied')
        return s

    # Toolbar/menu reorganisation.
    s = rep(s,
        '<div class="workspace"><aside class="side"><h3>Zones</h3><div id="zones" class="zoneList"></div><p class="help">Use the Zone and Building layout menus to keep the toolbar clear. Building boxes/outlines create black wall segments; zone boxes/outlines use the selected zone colour.</p></aside>',
        '<div class="workspace"><aside class="side"><h3>Zones</h3><div id="zones" class="zoneList"></div><p class="help">Zone contains Box, Outline and Fill area. Building layout contains walls and room layout tools. Doors, windows, shutters and stairs are under Objects.</p></aside>',
        'side help')

    s = rep(s,
        '<footer class="tools"><button id="zoneMenuBtn" class="menuTool active">Zone · Box</button><button id="layoutMenuBtn" class="menuTool">Building layout</button><button id="finish" hidden>Finish outline</button>',
        '<footer class="tools"><button id="zoneMenuBtn" class="menuTool active">Zone · Box</button><button id="layoutMenuBtn" class="menuTool">Building layout</button><button id="objectMenuBtn" class="menuTool">Objects · Door</button><button id="finish" hidden>Finish outline</button>',
        'objects menu button')

    s = rep(s,
        '<div id="zoneMenu" class="toolPopup" aria-label="Zone tools"><h4>Zone</h4><div id="zoneMenuList"></div><div class="menuRow"><button id="zoneCreate">＋ Create zone</button></div><div class="menuSep"></div><div class="menuRow"><button data-menu-tool="rect">▭ Box</button><button data-menu-tool="poly">⬡ Outline</button></div></div>\n<div id="layoutMenu" class="toolPopup" aria-label="Building layout tools"><h4>Building layout</h4><div class="menuRow"><button data-menu-tool="wall">Wall</button><button data-menu-tool="pen">Pen</button><button data-menu-tool="door">Door</button><button data-menu-tool="layoutRect">▭ Box</button><button data-menu-tool="layoutPoly">⬡ Outline</button><button data-menu-tool="label">Room label</button></div></div>',
        '<div id="zoneMenu" class="toolPopup" aria-label="Zone tools"><h4>Zone</h4><div id="zoneMenuList"></div><div class="menuRow"><button id="zoneCreate">＋ Create zone</button></div><div class="menuSep"></div><div class="menuRow"><button data-menu-tool="rect">▭ Box</button><button data-menu-tool="poly">⬡ Outline</button><button data-menu-tool="fill">▨ Fill area</button></div></div>\n<div id="layoutMenu" class="toolPopup" aria-label="Building layout tools"><h4>Building layout</h4><div class="menuRow"><button data-menu-tool="wall">Wall</button><button data-menu-tool="pen">Pen</button><button data-menu-tool="layoutRect">▭ Box</button><button data-menu-tool="layoutPoly">⬡ Outline</button><button data-menu-tool="label">Room label</button></div></div>\n<div id="objectMenu" class="toolPopup" aria-label="Objects"><h4>Objects</h4><div class="menuRow"><button data-menu-tool="door">Door</button><button data-menu-tool="window">Window</button><button data-menu-tool="shutter">Roller shutter</button><button data-menu-tool="stairs">Stairway</button></div></div>',
        'menu contents')

    # State and migration for new object types.
    s = rep(s,
        "const fresh=()=>({site:'',zones:[],shapes:[],notes:[],walls:[],doors:[],labels:[],pictureOpacity:1,pictureVisible:true,isBlank:false,gridVisible:false,wallWidth:3});",
        "const fresh=()=>({site:'',zones:[],shapes:[],notes:[],walls:[],doors:[],windows:[],shutters:[],stairs:[],labels:[],pictureOpacity:1,pictureVisible:true,isBlank:false,gridVisible:false,wallWidth:3});",
        'new object state')
    s = rep(s,
        "let opacityEditing=false,state=fresh(),img=null,tool='rect',selected=null,drawing=null,poly=[],zoom=1,pan={x:0,y:0},pointers=new Map(),gesture=null,pinchIds=new Set(),undo=[],redo=[],db=null,editId=null,chosenColor=colors[0],saveTimer,selection=[],lastZoneTool='rect',lastLayoutTool='wall';",
        "let opacityEditing=false,state=fresh(),img=null,tool='rect',selected=null,drawing=null,poly=[],zoom=1,pan={x:0,y:0},pointers=new Map(),gesture=null,pinchIds=new Set(),undo=[],redo=[],db=null,editId=null,chosenColor=colors[0],saveTimer,selection=[],lastZoneTool='rect',lastLayoutTool='wall',lastObjectTool='door';",
        'last object tool')
    s = rep(s,
        "function ensureIds(){for(const key of ['walls','doors','labels','notes','shapes'])for(const o of state[key]||[])if(!o.id)o.id=uid()}",
        "function ensureIds(){for(const key of ['walls','doors','windows','shutters','stairs','labels','notes','shapes'])for(const o of state[key]||[])if(!o.id)o.id=uid()}",
        'ids for new objects')
    s = rep(s,
        "state={...fresh(),...req.result,doors:req.result.doors||[],labels:req.result.labels||[]};",
        "state={...fresh(),...req.result,doors:req.result.doors||[],windows:req.result.windows||[],shutters:req.result.shutters||[],stairs:req.result.stairs||[],labels:req.result.labels||[]};",
        'load object migration')
    s = rep(s,
        "state={...fresh(),...next,doors:next.doors||[],labels:next.labels||[]};",
        "state={...fresh(),...next,doors:next.doors||[],windows:next.windows||[],shutters:next.shutters||[],stairs:next.stairs||[],labels:next.labels||[]};",
        'restore object migration')
    s = rep(s,
        "state.shapes=[];state.notes=[];state.walls=[];state.doors=[];state.labels=[];",
        "state.shapes=[];state.notes=[];state.walls=[];state.doors=[];state.windows=[];state.shutters=[];state.stairs=[];state.labels=[];",
        'clear objects on import')

    # More visible fill, same border.
    s = rep(s,
        "if(fill){c.globalAlpha=.07;c.fillStyle=color;c.fill()}c.globalAlpha=.62;",
        "if(fill){c.globalAlpha=.14;c.fillStyle=color;c.fill()}c.globalAlpha=.62;",
        'stronger zone fill')

    # Object renderers.
    door_fn = "function drawDoor(c,a,b,width=3,side=1,color='#172333'){const dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy);if(L<2)return;const nx=(-dy/L)*side,ny=(dx/L)*side,leaf={x:a.x+nx*L,y:a.y+ny*L};c.save();c.lineCap='round';c.lineJoin='round';c.strokeStyle=color;c.lineWidth=width;c.beginPath();c.moveTo(a.x,a.y);c.lineTo(leaf.x,leaf.y);c.stroke();c.beginPath();c.moveTo(b.x,b.y);const steps=14;for(let i=1;i<=steps;i++){const t=(Math.PI/2)*(i/steps),x=a.x+dx*Math.cos(t)+nx*L*Math.sin(t),y=a.y+dy*Math.cos(t)+ny*L*Math.sin(t);c.lineTo(x,y)}c.stroke();c.restore()}"
    renderers = door_fn + "\n" + r"""function drawWindow(c,a,b,width=2,color='#172333'){const dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy);if(L<2)return;const nx=-dy/L,ny=dx/L,o=Math.max(2,width*1.15);c.save();c.strokeStyle=color;c.lineWidth=Math.max(.8,width*.42);c.lineCap='butt';for(const sign of [-1,1]){c.beginPath();c.moveTo(a.x+nx*o*sign,a.y+ny*o*sign);c.lineTo(b.x+nx*o*sign,b.y+ny*o*sign);c.stroke()}c.beginPath();c.moveTo(a.x-nx*o,a.y-ny*o);c.lineTo(a.x+nx*o,a.y+ny*o);c.moveTo(b.x-nx*o,b.y-ny*o);c.lineTo(b.x+nx*o,b.y+ny*o);c.stroke();c.restore()}
function drawShutter(c,a,b,width=2,color='#172333'){const dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy);if(L<2)return;const nx=-dy/L,ny=dx/L,tick=Math.max(3,width*1.7),count=Math.max(4,Math.min(14,Math.round(L/13)));c.save();c.strokeStyle=color;c.lineWidth=Math.max(.8,width*.42);c.lineCap='round';c.beginPath();c.moveTo(a.x,a.y);c.lineTo(b.x,b.y);c.stroke();for(let i=0;i<=count;i++){const t=i/count,x=a.x+dx*t,y=a.y+dy*t;c.beginPath();c.moveTo(x-nx*tick,y-ny*tick);c.lineTo(x+nx*tick,y+ny*tick);c.stroke()}c.restore()}
function drawStairs(c,a,b,width=1.5,color='#172333'){const x1=Math.min(a.x,b.x),x2=Math.max(a.x,b.x),y1=Math.min(a.y,b.y),y2=Math.max(a.y,b.y),W=x2-x1,H=y2-y1;if(W<4||H<4)return;const horizontal=W>=H,steps=9;c.save();c.strokeStyle=color;c.fillStyle=color;c.lineWidth=Math.max(.8,width*.55);c.strokeRect(x1,y1,W,H);c.beginPath();for(let i=1;i<steps;i++){const t=i/steps;if(horizontal){const x=x1+W*t;c.moveTo(x,y1);c.lineTo(x,y2)}else{const y=y1+H*t;c.moveTo(x1,y);c.lineTo(x2,y)}}c.stroke();const dir=horizontal?(b.x>=a.x?1:-1):(b.y>=a.y?1:-1);let sx,sy,ex,ey;if(horizontal){sy=ey=(y1+y2)/2;sx=dir>0?x1+W*.2:x2-W*.2;ex=dir>0?x1+W*.8:x2-W*.8}else{sx=ex=(x1+x2)/2;sy=dir>0?y1+H*.2:y2-H*.2;ey=dir>0?y1+H*.8:y2-H*.8}c.lineWidth=Math.max(1,width*.7);c.beginPath();c.moveTo(sx,sy);c.lineTo(ex,ey);c.stroke();const ang=Math.atan2(ey-sy,ex-sx),ah=Math.max(5,width*2.5);c.beginPath();c.moveTo(ex,ey);c.lineTo(ex-ah*Math.cos(ang-.55),ey-ah*Math.sin(ang-.55));c.lineTo(ex-ah*Math.cos(ang+.55),ey-ah*Math.sin(ang+.55));c.closePath();c.fill();c.restore()}"""
    s = rep(s, door_fn, renderers, 'object drawing functions')

    # Wall openings for door/window/shutter.
    old_split = "function splitWallForDoor(wallId,startT,endT,side=1){const idx=state.walls.findIndex(w=>w.id===wallId);if(idx<0)return false;const w=state.walls[idx],a=w.points[0],b=w.points[1],lo=Math.min(startT,endT),hi=Math.max(startT,endT);if(hi-lo<.02)return false;const low=lerp(a,b,lo),high=lerp(a,b,hi),hinge=startT<=endT?low:high,other=startT<=endT?high:low;state.walls.splice(idx,1);if(lo>.001)state.walls.push({id:uid(),kind:'wall',group:w.group||null,points:[a,low]});if(hi<.999)state.walls.push({id:uid(),kind:'wall',group:w.group||null,points:[high,b]});state.doors.push({id:uid(),group:w.group||null,a:hinge,b:other,side:side>=0?1:-1});return true}"
    new_split = r"""function splitWallForObject(wallId,startT,endT,kind='door',side=1){const idx=state.walls.findIndex(w=>w.id===wallId);if(idx<0)return false;const w=state.walls[idx],a=w.points[0],b=w.points[1],lo=Math.min(startT,endT),hi=Math.max(startT,endT);if(hi-lo<.02)return false;const low=lerp(a,b,lo),high=lerp(a,b,hi),start=lerp(a,b,startT),end=lerp(a,b,endT);state.walls.splice(idx,1);if(lo>.001)state.walls.push({id:uid(),kind:'wall',group:w.group||null,points:[a,low]});if(hi<.999)state.walls.push({id:uid(),kind:'wall',group:w.group||null,points:[high,b]});const obj={id:uid(),group:w.group||null,a:start,b:end};if(kind==='door'){obj.side=side>=0?1:-1;state.doors.push(obj)}else if(kind==='window')state.windows.push(obj);else if(kind==='shutter')state.shutters.push(obj);else return false;return true}
function splitWallForDoor(wallId,startT,endT,side=1){return splitWallForObject(wallId,startT,endT,'door',side)}"""
    s = rep(s, old_split, new_split, 'generic wall object opening')

    # Exact wall-face fill from the connected wall graph. Doors/windows/shutters close their openings for zoning.
    badge_marker = "function badge(c,x,y,label,color){c.save();c.font='bold 18px system-ui';const W=Math.max(34,c.measureText(label).width+18);c.fillStyle='#fff';c.fillRect(x-W/2-2,y-18,W+4,35);c.fillStyle=color;c.fillRect(x-W/2,y-16,W,31);c.fillStyle='#fff';c.textAlign='center';c.textBaseline='middle';c.fillText(label,x,y);c.restore()}"
    fill_helpers = badge_marker + "\n" + r"""function polygonArea(pts){let a=0;for(let i=0,j=pts.length-1;i<pts.length;j=i++)a+=pts[j].x*pts[i].y-pts[i].x*pts[j].y;return a/2}
function simplifyPolygon(pts){let out=pts.slice();for(let pass=0;pass<3&&out.length>3;pass++){const next=[];for(let i=0;i<out.length;i++){const a=out[(i-1+out.length)%out.length],b=out[i],c=out[(i+1)%out.length],cross=(b.x-a.x)*(c.y-b.y)-(b.y-a.y)*(c.x-b.x);if(Math.abs(cross)>1e-7)next.push(b)}if(next.length===out.length||next.length<3)break;out=next}return out}
function boundarySegments(){const segs=[];for(const w of state.walls){if(w.kind==='wall'&&w.points?.length===2)segs.push([w.points[0],w.points[1]])}for(const key of ['doors','windows','shutters'])for(const o of state[key]||[])if(o.a&&o.b)segs.push([o.a,o.b]);return segs}
function enclosedFaceAt(p){const segs=boundarySegments();if(segs.length<3)return null;const verts=new Map(),adj=new Map(),key=q=>Math.round(q.x*1e6)+','+Math.round(q.y*1e6);function vertex(q){const k=key(q);if(!verts.has(k))verts.set(k,{x:q.x,y:q.y});if(!adj.has(k))adj.set(k,new Set());return k}for(const [a,b] of segs){const ka=vertex(a),kb=vertex(b);if(ka===kb)continue;adj.get(ka).add(kb);adj.get(kb).add(ka)}const visited=new Set(),faces=[];for(const [u,neighbors] of adj){for(const v of neighbors){const first=u+'>'+v;if(visited.has(first))continue;let a=u,b=v,poly=[],closed=false;for(let guard=0;guard<10000;guard++){const token=a+'>'+b;if(visited.has(token)&&token!==first)break;visited.add(token);poly.push(verts.get(a));const base=verts.get(b),list=[...(adj.get(b)||[])].sort((k1,k2)=>Math.atan2(verts.get(k1).y-base.y,verts.get(k1).x-base.x)-Math.atan2(verts.get(k2).y-base.y,verts.get(k2).x-base.x));const idx=list.indexOf(a);if(idx<0||!list.length)break;const next=list[(idx-1+list.length)%list.length];a=b;b=next;if(a===u&&b===v){closed=true;break}}if(closed&&poly.length>=3){const simple=simplifyPolygon(poly),area=Math.abs(polygonArea(simple));if(simple.length>=3&&area>1e-7&&pointInPoly(p,simple))faces.push({points:simple,area})}}}faces.sort((a,b)=>a.area-b.area);return faces[0]?.points||null}
function fillZoneAt(p){if(!selected){openModal();return}const face=enclosedFaceAt(p);if(!face){setHint('Area is not fully enclosed · check the surrounding walls for a gap');setTimeout(hint,1800);return}push();state.shapes.push({id:uid(),zone:selected,points:face,source:'fill'});changed();setHint('Enclosed area filled with the selected zone');setTimeout(hint,1200)}"""
    s = rep(s, badge_marker, fill_helpers, 'zone fill geometry')

    # Selection/group support for all new objects.
    s = rep(s,
        "function allRefs(){const refs=[];for(const type of ['walls','doors','labels','notes','shapes'])for(const o of state[type])refs.push({type,id:o.id});return refs}",
        "function allRefs(){const refs=[];for(const type of ['walls','doors','windows','shutters','stairs','labels','notes','shapes'])for(const o of state[type]||[])refs.push({type,id:o.id});return refs}",
        'new objects in refs')
    s = rep(s,
        "function itemPoints(ref){const o=getObj(ref);if(!o)return[];if(ref.type==='walls'||ref.type==='shapes')return o.points||[];if(ref.type==='doors')return[o.a,o.b];return[{x:o.x,y:o.y}]}",
        "function itemPoints(ref){const o=getObj(ref);if(!o)return[];if(ref.type==='walls'||ref.type==='shapes')return o.points||[];if(['doors','windows','shutters','stairs'].includes(ref.type))return[o.a,o.b];return[{x:o.x,y:o.y}]}",
        'new object bounds')
    s = rep(s,
        "function shiftObj(ref,orig,dx,dy){const o=getObj(ref);if(!o)return;if(ref.type==='walls'||ref.type==='shapes')o.points=orig.points.map(p=>({x:clamp(p.x+dx),y:clamp(p.y+dy)}));else if(ref.type==='doors'){o.a={x:clamp(orig.a.x+dx),y:clamp(orig.a.y+dy)};o.b={x:clamp(orig.b.x+dx),y:clamp(orig.b.y+dy)}}else{o.x=clamp(orig.x+dx);o.y=clamp(orig.y+dy)}}",
        "function shiftObj(ref,orig,dx,dy){const o=getObj(ref);if(!o)return;if(ref.type==='walls'||ref.type==='shapes')o.points=orig.points.map(p=>({x:clamp(p.x+dx),y:clamp(p.y+dy)}));else if(['doors','windows','shutters','stairs'].includes(ref.type)){o.a={x:clamp(orig.a.x+dx),y:clamp(orig.a.y+dy)};o.b={x:clamp(orig.b.x+dx),y:clamp(orig.b.y+dy)}}else{o.x=clamp(orig.x+dx);o.y=clamp(orig.y+dy)}}",
        'move new objects')
    old_hit = "function hitRefAt(clientX,clientY,max=24){const r=canvas.getBoundingClientRect(),click={x:clientX-r.left,y:clientY-r.top},v=transform(),map=p=>({x:v.ox+p.x*img.width*v.s,y:v.oy+p.y*img.height*v.s}),hits=[];for(const ref of allRefs()){const o=getObj(ref);let d=Infinity;if(ref.type==='labels'||ref.type==='notes'){const p=map(o);d=Math.hypot(click.x-p.x,click.y-p.y)}else if(ref.type==='doors'){d=segDistPx(click,map(o.a),map(o.b))}else if(ref.type==='walls'){for(let j=1;j<o.points.length;j++)d=Math.min(d,segDistPx(click,map(o.points[j-1]),map(o.points[j])))}else if(ref.type==='shapes'){const pts=o.points.map(map);if(pointInPoly(click,pts))d=10;else for(let j=0;j<pts.length;j++)d=Math.min(d,segDistPx(click,pts[j],pts[(j+1)%pts.length]))}if(d<=max)hits.push({ref,d})}hits.sort((a,b)=>a.d-b.d);return hits[0]?.ref||null}"
    new_hit = r"""function hitRefAt(clientX,clientY,max=24){const r=canvas.getBoundingClientRect(),click={x:clientX-r.left,y:clientY-r.top},v=transform(),map=p=>({x:v.ox+p.x*img.width*v.s,y:v.oy+p.y*img.height*v.s}),hits=[];for(const ref of allRefs()){const o=getObj(ref);let d=Infinity;if(ref.type==='labels'||ref.type==='notes'){const p=map(o);d=Math.hypot(click.x-p.x,click.y-p.y)}else if(['doors','windows','shutters'].includes(ref.type)){d=segDistPx(click,map(o.a),map(o.b))}else if(ref.type==='stairs'){const a=map(o.a),b=map(o.b),x1=Math.min(a.x,b.x),x2=Math.max(a.x,b.x),y1=Math.min(a.y,b.y),y2=Math.max(a.y,b.y);if(click.x>=x1&&click.x<=x2&&click.y>=y1&&click.y<=y2)d=8;else{const p1={x:x1,y:y1},p2={x:x2,y:y1},p3={x:x2,y:y2},p4={x:x1,y:y2};d=Math.min(segDistPx(click,p1,p2),segDistPx(click,p2,p3),segDistPx(click,p3,p4),segDistPx(click,p4,p1))}}else if(ref.type==='walls'){for(let j=1;j<o.points.length;j++)d=Math.min(d,segDistPx(click,map(o.points[j-1]),map(o.points[j])))}else if(ref.type==='shapes'){const pts=o.points.map(map);if(pointInPoly(click,pts))d=10;else for(let j=0;j<pts.length;j++)d=Math.min(d,segDistPx(click,pts[j],pts[(j+1)%pts.length]))}if(d<=max)hits.push({ref,d})}hits.sort((a,b)=>a.d-b.d);return hits[0]?.ref||null}"""
    s = rep(s, old_hit, new_hit, 'hit testing new objects')

    # Menu/tool state.
    old_tools = "const zoneTools=new Set(['rect','poly']),layoutTools=new Set(['wall','pen','door','layoutRect','layoutPoly','label']);\nfunction toolLabel(t){return({rect:'Box',poly:'Outline',wall:'Wall',pen:'Pen',door:'Door',layoutRect:'Box',layoutPoly:'Outline',label:'Room label'})[t]||t}"
    new_tools = "const zoneTools=new Set(['rect','poly','fill']),layoutTools=new Set(['wall','pen','layoutRect','layoutPoly','label']),objectTools=new Set(['door','window','shutter','stairs']),wallObjectTools=new Set(['door','window','shutter']);\nfunction toolLabel(t){return({rect:'Box',poly:'Outline',fill:'Fill area',wall:'Wall',pen:'Pen',door:'Door',window:'Window',shutter:'Roller shutter',stairs:'Stairway',layoutRect:'Box',layoutPoly:'Outline',label:'Room label'})[t]||t}"
    s = rep(s, old_tools, new_tools, 'tool categories')
    s = rep(s,
        "function syncToolMenus(){const z=state.zones.find(z=>z.id===selected);$('zoneMenuBtn').textContent=z?'Zone '+z.number+' · '+toolLabel(lastZoneTool):'Zone · Create/select';$('layoutMenuBtn').textContent='Building · '+toolLabel(lastLayoutTool);$('zoneMenuBtn').classList.toggle('active',zoneTools.has(tool));$('layoutMenuBtn').classList.toggle('active',layoutTools.has(tool));document.querySelectorAll('[data-menu-tool]').forEach(b=>b.classList.toggle('active',b.dataset.menuTool===tool))}",
        "function syncToolMenus(){const z=state.zones.find(z=>z.id===selected);$('zoneMenuBtn').textContent=z?'Zone '+z.number+' · '+toolLabel(lastZoneTool):'Zone · Create/select';$('layoutMenuBtn').textContent='Building · '+toolLabel(lastLayoutTool);$('objectMenuBtn').textContent='Objects · '+toolLabel(lastObjectTool);$('zoneMenuBtn').classList.toggle('active',zoneTools.has(tool));$('layoutMenuBtn').classList.toggle('active',layoutTools.has(tool));$('objectMenuBtn').classList.toggle('active',objectTools.has(tool));document.querySelectorAll('[data-menu-tool]').forEach(b=>b.classList.toggle('active',b.dataset.menuTool===tool))}",
        'sync objects menu')
    s = rep(s,
        "function setTool(t){tool=t;drawing=null;poly=[];if(t!=='group'&&t!=='select')clearSelection();if(zoneTools.has(t))lastZoneTool=t;if(layoutTools.has(t))lastLayoutTool=t;document.querySelectorAll('[data-tool]').forEach(b=>b.classList.toggle('active',b.dataset.tool===t));document.querySelectorAll('[data-menu-tool]').forEach(b=>b.classList.toggle('active',b.dataset.menuTool===t));$('finish').hidden=!(t==='poly'||t==='layoutPoly');syncToolMenus();closeToolMenus();hint();draw()}",
        "function setTool(t){tool=t;drawing=null;poly=[];if(t!=='group'&&t!=='select')clearSelection();if(zoneTools.has(t))lastZoneTool=t;if(layoutTools.has(t))lastLayoutTool=t;if(objectTools.has(t))lastObjectTool=t;document.querySelectorAll('[data-tool]').forEach(b=>b.classList.toggle('active',b.dataset.tool===t));document.querySelectorAll('[data-menu-tool]').forEach(b=>b.classList.toggle('active',b.dataset.menuTool===t));$('finish').hidden=!(t==='poly'||t==='layoutPoly');syncToolMenus();closeToolMenus();hint();draw()}",
        'remember objects tool')
    old_hint = "function hint(){if(!img){setHint('');return}const h={wall:'Drag a wall · ends snap to nearby walls · intersections split into deletable pieces',pen:'Draw freehand with your finger or stylus',door:'Drag along an existing wall · move your finger to either side of the wall to choose the door swing · orange shows the opening',layoutRect:'Drag a box to create four black building walls',layoutPoly:'Tap building corners, then Finish outline to create black walls',label:'Tap a room and type its name',rect:'Drag a box over the selected zone area',poly:'Tap zone corners, then Finish outline',note:'Tap the plan to add a note',erase:'Tap a wall section, door, label, note or zone area to delete only that item',select:'Tap an object and drag it · grouped objects move together as one',group:'Drag a blue box around several objects · then press Group',pan:'Drag to move · pinch to zoom'};setHint(h[tool]||'')}"
    new_hint = "function hint(){if(!img){setHint('');return}const h={wall:'Drag a wall · ends snap to nearby walls · intersections split into deletable pieces',pen:'Draw freehand with your finger or stylus',door:'Drag along a wall · finger side chooses the swing · orange preview shows the result',window:'Drag along a wall to cut in a window · orange preview shows its width',shutter:'Drag along a wall to cut in a roller shutter · orange preview shows its width',stairs:'Drag a rectangle for the stairway · drag direction sets the up arrow',layoutRect:'Drag a box to create four black building walls',layoutPoly:'Tap building corners, then Finish outline to create black walls',label:'Tap a room and type its name',rect:'Drag a box over the selected zone area',poly:'Tap zone corners, then Finish outline',fill:'Tap inside a fully enclosed wall area to fill it with the selected zone',note:'Tap the plan to add a note',erase:'Tap a wall, object, label, note or zone area to delete only that item',select:'Tap an object and drag it · grouped objects move together as one',group:'Drag a blue box around several objects · then press Group',pan:'Drag to move · pinch to zoom'};setHint(h[tool]||'')}"
    s = rep(s, old_hint, new_hint, 'tool hints')

    # Popup handlers.
    s = rep(s,
        "$('zoneMenuBtn').onclick=()=>toggleMenu($('zoneMenu'),$('zoneMenuBtn'));$('layoutMenuBtn').onclick=()=>toggleMenu($('layoutMenu'),$('layoutMenuBtn'));$('zoneCreate').onclick=()=>{closeToolMenus();openModal()};",
        "$('zoneMenuBtn').onclick=()=>toggleMenu($('zoneMenu'),$('zoneMenuBtn'));$('layoutMenuBtn').onclick=()=>toggleMenu($('layoutMenu'),$('layoutMenuBtn'));$('objectMenuBtn').onclick=()=>toggleMenu($('objectMenu'),$('objectMenuBtn'));$('zoneCreate').onclick=()=>{closeToolMenus();openModal()};",
        'objects popup handler')
    s = rep(s,
        "if(!e.target.closest('.toolPopup')&&!e.target.closest('#zoneMenuBtn')&&!e.target.closest('#layoutMenuBtn'))closeToolMenus()",
        "if(!e.target.closest('.toolPopup')&&!e.target.closest('#zoneMenuBtn')&&!e.target.closest('#layoutMenuBtn')&&!e.target.closest('#objectMenuBtn'))closeToolMenus()",
        'objects popup outside click')

    # Canvas drawing of objects/previews.
    s = rep(s,
        "for(const door of state.doors)drawDoor(ctx,map(door.a),map(door.b),Math.max(1,state.wallWidth*.85),door.side||1);\nfor(const l of state.labels)",
        "for(const door of state.doors)drawDoor(ctx,map(door.a),map(door.b),Math.max(1,state.wallWidth*.85),door.side||1);\nfor(const win of state.windows)drawWindow(ctx,map(win.a),map(win.b),Math.max(1,state.wallWidth));\nfor(const sh of state.shutters)drawShutter(ctx,map(sh.a),map(sh.b),Math.max(1,state.wallWidth));\nfor(const st of state.stairs)drawStairs(ctx,map(st.a),map(st.b),Math.max(1,state.wallWidth));\nfor(const l of state.labels)",
        'draw objects on canvas')
    old_preview = "if(drawing&&tool==='door'&&drawing.wallId){const a=map(drawing.a),b=map(drawing.b);ctx.save();ctx.strokeStyle='#f59e0b';ctx.lineWidth=8;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();ctx.fillStyle='#f59e0b';for(const p of [a,b]){ctx.beginPath();ctx.arc(p.x,p.y,6,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=.78;drawDoor(ctx,a,b,Math.max(1,state.wallWidth*.85),drawing.side||1,'#f59e0b');ctx.restore()}"
    new_preview = r"""if(drawing&&wallObjectTools.has(tool)&&drawing.wallId){const a=map(drawing.a),b=map(drawing.b);ctx.save();ctx.strokeStyle='#f59e0b';ctx.lineWidth=8;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();ctx.fillStyle='#f59e0b';for(const p of [a,b]){ctx.beginPath();ctx.arc(p.x,p.y,6,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=.82;if(tool==='door')drawDoor(ctx,a,b,Math.max(1,state.wallWidth*.85),drawing.side||1,'#f59e0b');else if(tool==='window')drawWindow(ctx,a,b,Math.max(1,state.wallWidth),'#f59e0b');else drawShutter(ctx,a,b,Math.max(1,state.wallWidth),'#f59e0b');ctx.restore()}
if(drawing&&tool==='stairs'){drawStairs(ctx,map(drawing.start),map(drawing.now),Math.max(1,state.wallWidth),'#f59e0b')}"""
    s = rep(s, old_preview, new_preview, 'object previews')

    # Pointer interactions.
    old_down = "if(tool==='wall'){const p=snapToWalls(point(e.clientX,e.clientY));drawing={start:p,now:p};return}if(tool==='door'){const hit=nearestWall(point(e.clientX,e.clientY),28);if(!hit){setHint('Start on an existing wall so the door can snap into it');setTimeout(hint,1300);return}drawing={wallId:hit.wall.id,startT:hit.t,endT:hit.t,a:hit.p,b:hit.p,side:1};return}if(tool==='rect'){"
    new_down = "if(tool==='wall'){const p=snapToWalls(point(e.clientX,e.clientY));drawing={start:p,now:p};return}if(wallObjectTools.has(tool)){const hit=nearestWall(point(e.clientX,e.clientY),28);if(!hit){setHint('Start on an existing wall so the object can snap into it');setTimeout(hint,1300);return}drawing={wallId:hit.wall.id,startT:hit.t,endT:hit.t,a:hit.p,b:hit.p,side:1};return}if(tool==='stairs'){const p=point(e.clientX,e.clientY);drawing={start:p,now:p};return}if(tool==='fill'){if(!selected){openModal();return}drawing={mode:'fillTap',client:{x:e.clientX,y:e.clientY},moved:false};return}if(tool==='rect'){"
    s = rep(s, old_down, new_down, 'object pointer down')

    old_move = "else if(tool==='wall'&&drawing){drawing.now=snappedAxis(drawing.start,snapToWalls(point(e.clientX,e.clientY)));draw()}else if(tool==='door'&&drawing?.wallId){const w=state.walls.find(x=>x.id===drawing.wallId);if(!w)return;const q=proj(point(e.clientX,e.clientY),w.points[0],w.points[1]);drawing.endT=q.t;drawing.a=lerp(w.points[0],w.points[1],drawing.startT);drawing.b=q.p;drawing.side=doorSideFromPointer(w,q,e.clientX,e.clientY);draw()}else if((tool==='rect'||tool==='layoutRect')&&drawing){drawing.now=point(e.clientX,e.clientY);draw()}"
    new_move = "else if(tool==='wall'&&drawing){drawing.now=snappedAxis(drawing.start,snapToWalls(point(e.clientX,e.clientY)));draw()}else if(wallObjectTools.has(tool)&&drawing?.wallId){const w=state.walls.find(x=>x.id===drawing.wallId);if(!w)return;const q=proj(point(e.clientX,e.clientY),w.points[0],w.points[1]);drawing.endT=q.t;drawing.a=lerp(w.points[0],w.points[1],drawing.startT);drawing.b=q.p;if(tool==='door')drawing.side=doorSideFromPointer(w,q,e.clientX,e.clientY);draw()}else if(tool==='fill'&&drawing?.mode==='fillTap'){if(Math.hypot(e.clientX-drawing.client.x,e.clientY-drawing.client.y)>10)drawing.moved=true}else if((tool==='rect'||tool==='layoutRect'||tool==='stairs')&&drawing){drawing.now=point(e.clientX,e.clientY);draw()}"
    s = rep(s, old_move, new_move, 'object pointer move')

    old_door_up = "if(tool==='door'&&drawing?.wallId){const d=drawing;drawing=null;const w=state.walls.find(x=>x.id===d.wallId);if(!w){draw();return}const q=proj(point(e.clientX,e.clientY),w.points[0],w.points[1]);const px1=screenPoint(lerp(w.points[0],w.points[1],d.startT)),px2=screenPoint(q.p),openingPx=Math.hypot(px1.x-px2.x,px1.y-px2.y);if(openingPx<24){setHint('Door opening too small · drag a little further along the wall');setTimeout(hint,1400);draw();return}const side=doorSideFromPointer(w,q,e.clientX,e.clientY);push();if(splitWallForDoor(d.wallId,d.startT,q.t,side)){changed();setHint(side>0?'Door placed · swing side 1':'Door placed · swing side 2');setTimeout(hint,900)}else draw();return}\nif(tool==='rect'&&drawing){"
    new_door_up = r"""if(wallObjectTools.has(tool)&&drawing?.wallId){const kind=tool,d=drawing;drawing=null;const w=state.walls.find(x=>x.id===d.wallId);if(!w){draw();return}const q=proj(point(e.clientX,e.clientY),w.points[0],w.points[1]),px1=screenPoint(lerp(w.points[0],w.points[1],d.startT)),px2=screenPoint(q.p),openingPx=Math.hypot(px1.x-px2.x,px1.y-px2.y),minPx=kind==='shutter'?28:18;if(openingPx<minPx){setHint('Opening too small · drag a little further along the wall');setTimeout(hint,1400);draw();return}const side=kind==='door'?doorSideFromPointer(w,q,e.clientX,e.clientY):1;push();if(splitWallForObject(d.wallId,d.startT,q.t,kind,side)){changed();setHint(kind==='door'?'Door placed':kind==='window'?'Window placed':'Roller shutter placed');setTimeout(hint,900)}else draw();return}
if(tool==='fill'&&drawing?.mode==='fillTap'){const d=drawing;drawing=null;if(!d.moved)fillZoneAt(point(e.clientX,e.clientY));else draw();return}
if(tool==='stairs'&&drawing){const a=drawing.start,b=point(e.clientX,e.clientY);drawing=null;const p1=screenPoint(a),p2=screenPoint(b);if(Math.abs(p2.x-p1.x)>28&&Math.abs(p2.y-p1.y)>28){push();state.stairs.push({id:uid(),group:null,a,b});changed();setHint('Stairway placed');setTimeout(hint,800)}else{setHint('Drag a larger rectangle for the stairway');setTimeout(hint,1200);draw()}return}
if(tool==='rect'&&drawing){"""
    s = rep(s, old_door_up, new_door_up, 'object pointer up')

    # Export all objects and include them in empty-check logic.
    s = rep(s,
        "for(const door of state.doors)drawDoor(x,map(door.a),map(door.b),Math.max(.75,state.wallWidth*.85*W/1600),door.side||1);for(const l of state.labels)",
        "for(const door of state.doors)drawDoor(x,map(door.a),map(door.b),Math.max(.75,state.wallWidth*.85*W/1600),door.side||1);for(const win of state.windows)drawWindow(x,map(win.a),map(win.b),Math.max(.75,state.wallWidth*W/1600));for(const sh of state.shutters)drawShutter(x,map(sh.a),map(sh.b),Math.max(.75,state.wallWidth*W/1600));for(const st of state.stairs)drawStairs(x,map(st.a),map(st.b),Math.max(.75,state.wallWidth*W/1600));for(const l of state.labels)",
        'export new objects')
    s = rep(s,
        "if(!state.shapes.length&&!state.walls.length&&!state.doors.length&&!state.labels.length&&!state.notes.length&&!confirm('Nothing has been drawn. Send the plan anyway?'))return;",
        "if(!state.shapes.length&&!state.walls.length&&!state.doors.length&&!state.windows.length&&!state.shutters.length&&!state.stairs.length&&!state.labels.length&&!state.notes.length&&!confirm('Nothing has been drawn. Send the plan anyway?'))return;",
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

## Version 0.9 — zone fill and objects

- Zone colour fill is stronger while keeping the same thin professional border.
- **Fill area** finds the smallest fully enclosed face in the connected wall graph and creates a neat zone polygon automatically. Door/window/shutter openings count as closed boundaries for zoning.
- Drawing tools are split into **Zone**, **Building layout**, and **Objects** menus.
- **Objects** contains wall-snapped Door, Window and Roller shutter tools plus a drag-to-place Stairway symbol.
- New objects support selection, movement, grouping, deletion, undo/redo and PNG export.
"""
if '## Version 0.9 — zone fill and objects' not in r:
    readme.write_text(r.rstrip() + section + '\n', encoding='utf-8')
    print('updated README.md')
