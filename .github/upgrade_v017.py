from pathlib import Path
import re

FILES = [Path('index.html'), Path('ZoneSketch.html'), Path('app/src/main/assets/index.html')]
text = FILES[0].read_text(encoding='utf-8')

pattern = re.compile(r"function boundarySegments\(\)\{.*?\nfunction fillZoneAt\(p\)\{.*?\}\nfunction getObj\(ref\)", re.S)

replacement = r'''function boundarySegments(){const segs=[];for(const w of state.walls){if(w.kind==='wall'&&w.points?.length===2)segs.push([w.points[0],w.points[1]])}for(const key of ['doors','windows','shutters'])for(const o of state[key]||[])if(o.a&&o.b)segs.push([o.a,o.b]);return segs}
function buildFillBoundaryPx(tolPx=0){if(!img)return[];const W=img.width,H=img.height,base=boundarySegments(),raw=base.map(([a,b])=>[{x:a.x*W,y:a.y*H},{x:b.x*W,y:b.y*H}]),splits=raw.map(()=>[0,1]),bridges=[];const lerpPx=(a,b,t)=>({x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t}),dist=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);function projectPx(p,a,b){const dx=b.x-a.x,dy=b.y-a.y,l2=dx*dx+dy*dy;if(!l2)return{p:{...a},t:0,d:dist(p,a)};const t=Math.max(0,Math.min(1,((p.x-a.x)*dx+(p.y-a.y)*dy)/l2)),q=lerpPx(a,b,t);return{p:q,t,d:dist(p,q)}}function crossHit(a,b,c,d){const r={x:b.x-a.x,y:b.y-a.y},s={x:d.x-c.x,y:d.y-c.y},den=r.x*s.y-r.y*s.x;if(Math.abs(den)<1e-9)return null;const ca={x:c.x-a.x,y:c.y-a.y},t=(ca.x*s.y-ca.y*s.x)/den,u=(ca.x*r.y-ca.y*r.x)/den;if(t<-.000001||t>1.000001||u<-.000001||u>1.000001)return null;return{t:Math.max(0,Math.min(1,t)),u:Math.max(0,Math.min(1,u)),p:lerpPx(a,b,Math.max(0,Math.min(1,t)))}}
for(let i=0;i<raw.length;i++)for(let j=i+1;j<raw.length;j++){const h=crossHit(raw[i][0],raw[i][1],raw[j][0],raw[j][1]);if(h){splits[i].push(h.t);splits[j].push(h.u)}}
const heal=Math.max(0,tolPx);for(let i=0;i<raw.length;i++){for(const endpoint of raw[i]){let best=null;for(let j=0;j<raw.length;j++){if(j===i)continue;const q=projectPx(endpoint,raw[j][0],raw[j][1]);if(q.d<=heal+.01&&(!best||q.d<best.d))best={...q,j}}if(best){splits[best.j].push(best.t);if(best.d>.2)bridges.push([endpoint,best.p])}}}
const out=[],edgeKeys=new Set(),edgeKey=(a,b)=>{const ka=Math.round(a.x*10)+','+Math.round(a.y*10),kb=Math.round(b.x*10)+','+Math.round(b.y*10);return ka<kb?ka+'|'+kb:kb+'|'+ka},add=(a,b)=>{if(dist(a,b)<.3)return;const k=edgeKey(a,b);if(edgeKeys.has(k))return;edgeKeys.add(k);out.push([a,b])};for(let i=0;i<raw.length;i++){const ts=[...new Set(splits[i].map(t=>Math.round(t*1000000)/1000000))].sort((a,b)=>a-b);for(let n=1;n<ts.length;n++)add(lerpPx(raw[i][0],raw[i][1],ts[n-1]),lerpPx(raw[i][0],raw[i][1],ts[n]))}for(const [a,b] of bridges)add(a,b);return out}
function traceFillFacePx(segs,p){if(segs.length<3)return null;const verts=new Map(),adj=new Map(),key=q=>Math.round(q.x*10)+','+Math.round(q.y*10);function vertex(q){const k=key(q);if(!verts.has(k))verts.set(k,{x:q.x,y:q.y});if(!adj.has(k))adj.set(k,new Set());return k}for(const [a,b] of segs){const ka=vertex(a),kb=vertex(b);if(ka===kb)continue;adj.get(ka).add(kb);adj.get(kb).add(ka)}const visited=new Set(),faces=[];for(const [u,neighbors] of adj){for(const v of neighbors){const first=u+'>'+v;if(visited.has(first))continue;let a=u,b=v,poly=[],closed=false;for(let guard=0;guard<20000;guard++){const token=a+'>'+b;if(visited.has(token)&&token!==first)break;visited.add(token);poly.push(verts.get(a));const pivot=verts.get(b),list=[...(adj.get(b)||[])].sort((k1,k2)=>Math.atan2(verts.get(k1).y-pivot.y,verts.get(k1).x-pivot.x)-Math.atan2(verts.get(k2).y-pivot.y,verts.get(k2).x-pivot.x)),idx=list.indexOf(a);if(idx<0||!list.length)break;const next=list[(idx-1+list.length)%list.length];a=b;b=next;if(a===u&&b===v){closed=true;break}}if(closed&&poly.length>=3){const simple=simplifyPolygon(poly),area=Math.abs(polygonArea(simple));if(simple.length>=3&&area>.5&&pointInPoly(p,simple))faces.push({points:simple,area})}}}faces.sort((a,b)=>a.area-b.area);return faces[0]?.points||null}
function enclosedFaceAt(p){if(!img)return null;const W=img.width,H=img.height,tap={x:p.x*W,y:p.y*H},baseTol=Math.max(8,Math.min(24,Math.min(W,H)*.009)),tries=[0,Math.round(baseTol*.55),baseTol];for(const tol of tries){const face=traceFillFacePx(buildFillBoundaryPx(tol),tap);if(face){const points=face.map(q=>({x:clamp(q.x/W),y:clamp(q.y/H)}));points.healed=tol>0;points.healPx=tol;return points}}return null}
function fillZoneAt(p){if(!selected){openModal();return}const face=enclosedFaceAt(p);if(!face){setHint('Could not find a closed area · join any large visible wall gap and tap again');setTimeout(hint,1900);return}push();state.shapes.push({id:uid(),zone:selected,points:Array.from(face),source:'fill'});changed();setHint(face.healed?'Area filled · tiny wall gaps/junctions were joined automatically':'Enclosed area filled with the selected zone');setTimeout(hint,1400)}
function getObj(ref)'''

new_text, count = pattern.subn(replacement, text, count=1)
if count != 1:
    raise SystemExit(f'Expected to replace fill block once, replaced {count}')

# Version marker in README handled separately by workflow; keep app copies byte-identical.
for f in FILES:
    f.write_text(new_text, encoding='utf-8')

# Sanity markers.
for marker in ['function buildFillBoundaryPx', 'function traceFillFacePx', "points.healed=tol>0", 'tiny wall gaps/junctions were joined automatically']:
    if marker not in new_text:
        raise SystemExit('Missing marker: '+marker)

print('Applied v0.17 robust zone-fill geometry upgrade')
