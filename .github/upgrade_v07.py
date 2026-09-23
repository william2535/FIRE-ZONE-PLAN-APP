from pathlib import Path

FILES = [Path('index.html'), Path('ZoneSketch.html'), Path('app/src/main/assets/index.html')]


def rep(s, old, new, label, count=1):
    n = s.count(old)
    if n < count:
        raise SystemExit(f'{label}: expected at least {count} match(es), found {n}')
    return s.replace(old, new, count)


def upgrade(s):
    if 'function mergeOverlappingWalls()' in s:
        print('v0.7 already applied')
        return s

    old_grid = "function drawGrid(c,v){if(!state.gridVisible||!img)return;let step=50;while(step*v.s<28)step*=2;while(step*v.s>72&&step>12.5)step/=2;const left=v.ox,top=v.oy,W=img.width*v.s,H=img.height*v.s;c.save();c.beginPath();c.rect(left,top,W,H);c.clip();c.lineWidth=1;c.strokeStyle='#486b8a32';c.beginPath();for(let x=0;x<=img.width+.001;x+=step){const sx=left+x*v.s;c.moveTo(sx,top);c.lineTo(sx,top+H)}for(let y=0;y<=img.height+.001;y+=step){const sy=top+y*v.s;c.moveTo(left,sy);c.lineTo(left+W,sy)}c.stroke();c.restore()}"
    new_grid = "function drawGrid(c,v){if(!state.gridVisible||!img)return;const raw=Math.max(img.width,img.height)/32,step=Math.max(20,Math.round(raw/10)*10);const left=v.ox,top=v.oy,W=img.width*v.s,H=img.height*v.s;c.save();c.beginPath();c.rect(left,top,W,H);c.clip();c.lineWidth=1;c.strokeStyle='#486b8a32';c.beginPath();for(let x=0;x<=img.width+.001;x+=step){const sx=left+x*v.s;c.moveTo(sx,top);c.lineTo(sx,top+H)}for(let y=0;y<=img.height+.001;y+=step){const sy=top+y*v.s;c.moveTo(left,sy);c.lineTo(left+W,sy)}c.stroke();c.restore()}"
    s = rep(s, old_grid, new_grid, 'fixed plan-space grid')

    old_label = "function roomLabel(c,x,y,text,scale=1){c.save();c.font=`bold ${Math.max(13,15*scale)}px system-ui`;const W=c.measureText(text).width+14,H=Math.max(22,24*scale);c.fillStyle='#ffffffdd';c.fillRect(x-W/2,y-H/2,W,H);c.strokeStyle='#7c8997';c.lineWidth=Math.max(1,scale);c.strokeRect(x-W/2,y-H/2,W,H);c.fillStyle='#182332';c.textAlign='center';c.textBaseline='middle';c.fillText(text,x,y);c.restore()}"
    new_label = "function roomLabel(c,x,y,text,fontSize=15){const fs=Math.max(4,fontSize),pad=fs*.45;c.save();c.font=`600 ${fs}px system-ui`;const W=c.measureText(text).width+pad*2,H=fs*1.6;c.fillStyle='#fffffff0';c.fillRect(x-W/2,y-H/2,W,H);c.strokeStyle='#7c8997';c.lineWidth=Math.max(.5,fs/18);c.strokeRect(x-W/2,y-H/2,W,H);c.fillStyle='#182332';c.textAlign='center';c.textBaseline='middle';c.fillText(text,x,y);c.restore()}"
    s = rep(s, old_label, new_label, 'plan-space room labels')

    old_shape = "function shape(c,pts,color,num,line=3,fill=true){c.save();c.beginPath();pts.forEach((p,i)=>i?c.lineTo(p.x,p.y):c.moveTo(p.x,p.y));c.closePath();if(fill){c.fillStyle=color+'25';c.fill()}c.lineWidth=line;c.strokeStyle=color;c.lineJoin='round';c.stroke();const mid=centre(pts);badge(c,mid.x,mid.y,'Z'+num,color);c.restore()}"
    new_shape = "function shape(c,pts,color,num,line=1.4,fill=true){c.save();c.beginPath();pts.forEach((p,i)=>i?c.lineTo(p.x,p.y):c.moveTo(p.x,p.y));c.closePath();if(fill){c.globalAlpha=.07;c.fillStyle=color;c.fill()}c.globalAlpha=.62;c.lineWidth=line;c.strokeStyle=color;c.lineJoin='round';c.stroke();c.restore()}"
    s = rep(s, old_shape, new_shape, 'subtle zone styling without badges')

    unique = "function uniqueTs(ts){return[...new Set(ts.map(t=>Math.round(t*100000)/100000))].sort((a,b)=>a-b)}"
    merge = unique + "\n" + r"""function mergeOverlappingWalls(){const tol=.003,fixed=[],diag=[],hs=[],vs=[];for(const w of state.walls||[]){if(w.group||w.kind!=='wall'||!w.points||w.points.length!==2){fixed.push(w);continue}const a=w.points[0],b=w.points[1],dx=Math.abs(b.x-a.x),dy=Math.abs(b.y-a.y);if(dy<=tol)hs.push({coord:(a.y+b.y)/2,start:Math.min(a.x,b.x),end:Math.max(a.x,b.x)});else if(dx<=tol)vs.push({coord:(a.x+b.x)/2,start:Math.min(a.y,b.y),end:Math.max(a.y,b.y)});else diag.push(w)}
function mergeAxis(items,horizontal){items.sort((a,b)=>a.coord-b.coord||a.start-b.start);const clusters=[];for(const it of items){let c=clusters[clusters.length-1];if(!c||Math.abs(it.coord-c.last)>tol){c={last:it.coord,items:[]};clusters.push(c)}c.items.push(it);c.last=it.coord}const out=[];for(const c of clusters){const ref=c.items.reduce((best,it)=>(it.end-it.start)>(best.end-best.start)?it:best,c.items[0]).coord,arr=c.items.slice().sort((a,b)=>a.start-b.start);let start=arr[0].start,end=arr[0].end;for(let i=1;i<arr.length;i++){const it=arr[i];if(it.start<=end+tol)end=Math.max(end,it.end);else{out.push({id:uid(),kind:'wall',group:null,points:horizontal?[{x:start,y:ref},{x:end,y:ref}]:[{x:ref,y:start},{x:ref,y:end}]});start=it.start;end=it.end}}out.push({id:uid(),kind:'wall',group:null,points:horizontal?[{x:start,y:ref},{x:end,y:ref}]:[{x:ref,y:start},{x:ref,y:end}]})}return out}
state.walls=[...fixed,...diag,...mergeAxis(hs,true),...mergeAxis(vs,false)];splitExistingWalls()}"""
    s = rep(s, unique, merge, 'overlap merge helper')

    s = rep(s,
        "normalizeWalls();splitExistingWalls();ensureIds();$('site').value=state.site||'';",
        "normalizeWalls();mergeOverlappingWalls();ensureIds();$('site').value=state.site||'';",
        'clean overlaps on load')
    s = rep(s,
        "normalizeWalls();splitExistingWalls();ensureIds();selection=[];",
        "normalizeWalls();mergeOverlappingWalls();ensureIds();selection=[];",
        'clean overlaps on restore')

    s = rep(s,
        "for(const sh of state.shapes){const z=state.zones.find(z=>z.id===sh.zone);if(z&&sh.points.length>2)shape(ctx,sh.points.map(map),z.color,z.number,Math.max(2,3*Math.min(zoom,2)),true)}",
        "for(const sh of state.shapes){const z=state.zones.find(z=>z.id===sh.zone);if(z&&sh.points.length>2)shape(ctx,sh.points.map(map),z.color,z.number,1.4,true)}",
        'thin on-screen zone borders')
    s = rep(s,
        "for(const l of state.labels){const p=map(l);roomLabel(ctx,p.x,p.y,l.text,Math.min(1.4,Math.max(.8,zoom)))}",
        "for(const l of state.labels){const p=map(l),fs=Math.min(img.width,img.height)*.022*v.s;roomLabel(ctx,p.x,p.y,l.text,fs)}",
        'labels fixed to plan scale')
    s = rep(s,
        "shape(ctx,[a,{x:b.x,y:a.y},b,{x:a.x,y:b.y}].map(map),z.color,z.number,2,true)",
        "shape(ctx,[a,{x:b.x,y:a.y},b,{x:a.x,y:b.y}].map(map),z.color,z.number,1.4,true)",
        'zone preview styling')

    s = rep(s,
        "push();addWallSegment(a,b);changed()",
        "push();addWallSegment(a,b);mergeOverlappingWalls();changed()",
        'merge manual wall overlaps')
    s = rep(s,
        "for(let i=0;i<4;i++)addWallSegment(pts[i],pts[(i+1)%4]);changed()",
        "for(let i=0;i<4;i++)addWallSegment(pts[i],pts[(i+1)%4]);mergeOverlappingWalls();changed()",
        'merge building box overlaps')
    s = rep(s,
        "for(let i=0;i<pts.length;i++)addWallSegment(pts[i],pts[(i+1)%pts.length]);changed()",
        "for(let i=0;i<pts.length;i++)addWallSegment(pts[i],pts[(i+1)%pts.length]);mergeOverlappingWalls();changed()",
        'merge building outline overlaps')

    s = rep(s,
        "shape(x,sh.points.map(map),z.color,z.number,Math.max(3,W/500),true)",
        "shape(x,sh.points.map(map),z.color,z.number,Math.max(1.4,W/1800),true)",
        'thin exported zone borders')
    s = rep(s,
        "roomLabel(x,p.x,p.y,l.text,Math.max(1,W/1600))",
        "roomLabel(x,p.x,p.y,l.text,Math.max(11,W/120))",
        'export room label size')

    s = rep(s,
        '<p class="small">The zone number and description appear on the plan sent to the office.</p>',
        '<p class="small">The zone number and description stay in the zone index/key rather than covering the drawing.</p>',
        'zone modal wording')

    return s


for path in FILES:
    original = path.read_text(encoding='utf-8')
    updated = upgrade(original)
    path.write_text(updated, encoding='utf-8')
    print(f'updated {path}: {len(original)} -> {len(updated)} bytes')

readme = Path('README.md')
r = readme.read_text(encoding='utf-8')
section = """

## Version 0.7 — drawing polish

- Building wall boxes/outlines now merge overlapping or near-overlapping horizontal/vertical wall runs into one clean line, then re-split them at real junctions so precise delete still works.
- Zone badges such as **Z1** are removed from the drawing; zone identification remains in the side index and exported zone key.
- Zone areas now use a restrained translucent fill and thin boundary instead of a heavy coloured border.
- The grid uses fixed plan-space spacing, so it stays anchored to the drawing while zooming.
- Room labels are sized from plan-space scale instead of a separate clamped zoom scale, so they remain visually attached to the plan.
"""
if '## Version 0.7 — drawing polish' not in r:
    readme.write_text(r.rstrip() + section + '\n', encoding='utf-8')
    print('updated README.md')
