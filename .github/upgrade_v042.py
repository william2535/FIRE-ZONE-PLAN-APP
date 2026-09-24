from pathlib import Path
import subprocess, sys

# v0.42 includes every v0.41 fix first.
subprocess.run([sys.executable, '.github/upgrade_v041.py'], check=True)


def replace_once(text, old, new, label):
    if new in text and old not in text:
        return text
    if old not in text:
        raise SystemExit(f'v0.42 patch marker missing: {label}')
    return text.replace(old, new, 1)

p = Path('index.html')
text = p.read_text()
text = text.replace('v0.41', 'v0.42')

# Make the zoom range explicitly finger-draggable even inside the canvas wrapper,
# whose touch-action is intentionally locked for the drawing surface.
zoom_css = """
/* v0.42 — direct finger zoom slider, directional beam triangles and grid-safe duplication. */
.zoomDock input[type=range]{touch-action:none;height:30px;cursor:ew-resize}
.zoomDock input[type=range]::-webkit-slider-thumb{min-width:24px;min-height:24px}
"""
if '/* v0.42 — direct finger zoom slider' not in text:
    text = text.replace('</style>', zoom_css + '\n</style>', 1)

text = replace_once(
    text,
    "symbol:'Tap repeatedly to stamp '+symbolNames[symbolStamp]+' symbols'",
    "symbol:symbolStamp==='beam'?'Press where the beam starts, drag the triangle tip with your finger, then release':'Tap repeatedly to stamp '+symbolNames[symbolStamp]+' symbols'",
    'beam placement hint'
)

# A stretched beam is stored as a normal symbol anchor plus beamEnd. The helper
# draws a true triangle whose sharp tip is exactly the dragged endpoint.
beam_helper = """function drawBeamTriangle(c,a,tip,size,color='#172333',preview=false){const dx=tip.x-a.x,dy=tip.y-a.y,L=Math.hypot(dx,dy);if(L<1)return;const nx=-dy/L,ny=dx/L,half=Math.max(3,Math.min(Math.max(4,size*.72),L*.32));c.save();c.strokeStyle=color;c.fillStyle=color;c.lineWidth=Math.max(1,size*.12);c.lineJoin='round';c.beginPath();c.moveTo(a.x+nx*half,a.y+ny*half);c.lineTo(tip.x,tip.y);c.lineTo(a.x-nx*half,a.y-ny*half);c.closePath();c.globalAlpha=preview?.18:.11;c.fill();c.globalAlpha=preview?.9:1;c.stroke();c.beginPath();c.arc(tip.x,tip.y,Math.max(2,size*.15),0,Math.PI*2);c.fill();c.restore()}\n"""
if 'function drawBeamTriangle(' not in text:
    text = text.replace('function drawSymbol(c,p,type,size,color=', beam_helper + 'function drawSymbol(c,p,type,size,color=', 1)

text = replace_once(
    text,
    "c.textAlign='center';c.textBaseline='middle';if(type==='panel'||type==='mcp'||type==='repeater'||type==='beam'||type==='io')",
    "c.textAlign='center';c.textBaseline='middle';if(type==='beam'){c.beginPath();c.moveTo(-r*.7,-r*.65);c.lineTo(r*1.15,0);c.lineTo(-r*.7,r*.65);c.closePath();c.globalAlpha=.12;c.fill();c.globalAlpha=1;c.stroke();c.restore();return}if(type==='panel'||type==='mcp'||type==='repeater'||type==='io')",
    'compact beam symbol shape'
)

# Beam geometry participates in bounds, hit testing, movement, resize, rotate,
# mirror, canvas rotate/expand and duplication just like other real objects.
text = replace_once(
    text,
    "function itemPoints(ref){const o=getObj(ref);if(!o)return[];if(ref.type==='walls'||ref.type==='shapes')return o.points||[];if(['doors','windows','shutters','stairs'].includes(ref.type))return[o.a,o.b];return[{x:o.x,y:o.y}]}",
    "function itemPoints(ref){const o=getObj(ref);if(!o)return[];if(ref.type==='walls'||ref.type==='shapes')return o.points||[];if(['doors','windows','shutters','stairs'].includes(ref.type))return[o.a,o.b];if(ref.type==='symbols'&&o.type==='beam'&&o.beamEnd)return[{x:o.x,y:o.y},o.beamEnd];return[{x:o.x,y:o.y}]}",
    'beam item points'
)
text = replace_once(
    text,
    "if(ref.type==='symbols'&&img){const r=Math.min(img.width,img.height)*.018*(o.scale||1),w=r*2.5/img.width,h=r*2.5/img.height;return{x1:clamp(o.x-w/2),y1:clamp(o.y-h/2),x2:clamp(o.x+w/2),y2:clamp(o.y+h/2)}}",
    "if(ref.type==='symbols'&&img){const r=Math.min(img.width,img.height)*.018*(o.scale||1),w=r*2.5/img.width,h=r*2.5/img.height;if(o.type==='beam'&&o.beamEnd){const px=r*.8/img.width,py=r*.8/img.height;return{x1:clamp(Math.min(o.x,o.beamEnd.x)-px),y1:clamp(Math.min(o.y,o.beamEnd.y)-py),x2:clamp(Math.max(o.x,o.beamEnd.x)+px),y2:clamp(Math.max(o.y,o.beamEnd.y)+py)}}return{x1:clamp(o.x-w/2),y1:clamp(o.y-h/2),x2:clamp(o.x+w/2),y2:clamp(o.y+h/2)}}",
    'beam symbol bounds'
)
text = replace_once(
    text,
    "if(['labels','notes','symbols','pins'].includes(ref.type)){const p=map(o);d=Math.hypot(click.x-p.x,click.y-p.y)}",
    "if(ref.type==='symbols'&&o.type==='beam'&&o.beamEnd){const a=map(o),b=map(o.beamEnd);d=Math.min(segDistPx(click,a,b),Math.hypot(click.x-a.x,click.y-a.y),Math.hypot(click.x-b.x,click.y-b.y))}else if(['labels','notes','symbols','pins'].includes(ref.type)){const p=map(o);d=Math.hypot(click.x-p.x,click.y-p.y)}",
    'beam hit testing'
)
text = replace_once(
    text,
    "function shiftObj(ref,orig,dx,dy){const o=getObj(ref);if(!o)return;if(ref.type==='walls'||ref.type==='shapes')o.points=orig.points.map(p=>({x:clamp(p.x+dx),y:clamp(p.y+dy)}));else if(['doors','windows','shutters','stairs'].includes(ref.type)){o.a={x:clamp(orig.a.x+dx),y:clamp(orig.a.y+dy)};o.b={x:clamp(orig.b.x+dx),y:clamp(orig.b.y+dy)}}else{o.x=clamp(orig.x+dx);o.y=clamp(orig.y+dy)}}",
    "function shiftObj(ref,orig,dx,dy){const o=getObj(ref);if(!o)return;if(ref.type==='walls'||ref.type==='shapes')o.points=orig.points.map(p=>({x:clamp(p.x+dx),y:clamp(p.y+dy)}));else if(['doors','windows','shutters','stairs'].includes(ref.type)){o.a={x:clamp(orig.a.x+dx),y:clamp(orig.a.y+dy)};o.b={x:clamp(orig.b.x+dx),y:clamp(orig.b.y+dy)}}else{o.x=clamp(orig.x+dx);o.y=clamp(orig.y+dy);if(ref.type==='symbols'&&orig.type==='beam'&&orig.beamEnd)o.beamEnd={x:clamp(orig.beamEnd.x+dx),y:clamp(orig.beamEnd.y+dy)}}}",
    'beam movement'
)
text = replace_once(
    text,
    "function mapObjectPoints(type,o,fn){if(type==='walls'||type==='shapes')o.points=(o.points||[]).map(fn);else if(['doors','windows','shutters','stairs'].includes(type)){o.a=fn(o.a);o.b=fn(o.b)}else{const p=fn({x:o.x,y:o.y});o.x=p.x;o.y=p.y}}",
    "function mapObjectPoints(type,o,fn){if(type==='walls'||type==='shapes')o.points=(o.points||[]).map(fn);else if(['doors','windows','shutters','stairs'].includes(type)){o.a=fn(o.a);o.b=fn(o.b)}else{const p=fn({x:o.x,y:o.y});o.x=p.x;o.y=p.y;if(type==='symbols'&&o.type==='beam'&&o.beamEnd)o.beamEnd=fn(o.beamEnd)}}",
    'beam transforms'
)

# Survey duplicates now use the actual plan grid, not an arbitrary 24-screen-px
# offset. The duplicated detector anchor is one grid intersection away and the
# whole selected object/group keeps its geometry.
old_duplicate = "function duplicateSelection(){if(!selection.length||!img)return;push();const v=transform(),delta=boundedDelta(snapshotSelection(),24/(img.width*v.s),24/(img.height*v.s)),dx=delta.x,dy=delta.y,groupMap=new Map(),common=selection.length>1?uid():null,newRefs=[];for(const r of selection){const src=getObj(r);if(!src)continue;const copy=JSON.parse(JSON.stringify(src));copy.id=uid();if(src.group){if(!groupMap.has(src.group))groupMap.set(src.group,uid());copy.group=groupMap.get(src.group)}else if(common)copy.group=common;mapObjectPoints(r.type,copy,p=>({x:clamp(p.x+dx),y:clamp(p.y+dy)}));state[r.type].push(copy);newRefs.push({type:r.type,id:copy.id})}selection=newRefs;changed();setHint('Duplicate created · drag it with Select / Move');setTimeout(hint,1000)}"
new_duplicate = "function duplicateSelection(){if(!selection.length||!img)return;const snap=snapshotSelection(),v=transform();let delta;if(surveyMode&&state.snapGrid&&selection.every(r=>r.type==='symbols')){const b=selectionBounds(),step=gridStep(),anchor=snap[0]?.orig||getObj(selection[0]),sx=(b&&b.x2+step/img.width<=1)?1:-1,sy=(b&&b.y2+step/img.height<=1)?1:-1,target=snapGridPoint({x:anchor.x+sx*step/img.width,y:anchor.y+sy*step/img.height});delta=boundedDelta(snap,target.x-anchor.x,target.y-anchor.y)}else delta=boundedDelta(snap,24/(img.width*v.s),24/(img.height*v.s));push();const dx=delta.x,dy=delta.y,groupMap=new Map(),common=selection.length>1?uid():null,newRefs=[];for(const r of selection){const src=getObj(r);if(!src)continue;const copy=JSON.parse(JSON.stringify(src));copy.id=uid();if(src.group){if(!groupMap.has(src.group))groupMap.set(src.group,uid());copy.group=groupMap.get(src.group)}else if(common)copy.group=common;mapObjectPoints(r.type,copy,p=>({x:clamp(p.x+dx),y:clamp(p.y+dy)}));state[r.type].push(copy);newRefs.push({type:r.type,id:copy.id})}selection=newRefs;changed();setHint(surveyMode&&state.snapGrid?'Duplicate created on the grid':'Duplicate created · drag it with Select / Move');setTimeout(hint,1000)}"
text = replace_once(text, old_duplicate, new_duplicate, 'grid-safe duplicate')

# Beam drag lifecycle. Press = base, finger/release = pointed triangle tip.
pd_marker = "if(tool==='layoutRect'||tool==='layoutEllipse'||tool==='corridor'||tool==='layoutL'){const p=inputPoint(e.clientX,e.clientY);drawing={start:p,now:p};return}if((tool==='select'||tool==='group')&&selection.length)"
pd_new = "if(tool==='layoutRect'||tool==='layoutEllipse'||tool==='corridor'||tool==='layoutL'){const p=inputPoint(e.clientX,e.clientY);drawing={start:p,now:p};return}if(tool==='symbol'&&symbolStamp==='beam'){const p=inputPoint(e.clientX,e.clientY);drawing={mode:'beamSymbol',start:p,now:p};draw();return}if((tool==='select'||tool==='group')&&selection.length)"
text = replace_once(text, pd_marker, pd_new, 'beam pointer down')

pm_marker = "else if((tool==='layoutRect'||tool==='layoutEllipse'||tool==='corridor'||tool==='layoutL'||tool==='stairs')&&drawing){drawing.now=inputPoint(e.clientX,e.clientY);draw()}else if(tool==='group'&&drawing?.mode==='selectBox')"
pm_new = "else if((tool==='layoutRect'||tool==='layoutEllipse'||tool==='corridor'||tool==='layoutL'||tool==='stairs')&&drawing){drawing.now=inputPoint(e.clientX,e.clientY);draw()}else if(tool==='symbol'&&symbolStamp==='beam'&&drawing?.mode==='beamSymbol'){drawing.now=inputPoint(e.clientX,e.clientY);draw()}else if(tool==='group'&&drawing?.mode==='selectBox')"
text = replace_once(text, pm_marker, pm_new, 'beam pointer move')

pu_marker = "if(['symbol','quickLabel','label','note','pinNote','pinPhoto','erase','poly','layoutPoly'].includes(tool)&&tapStart&&Math.hypot(e.clientX-tapStart.x,e.clientY-tapStart.y)>12){drawing=null;return}"
pu_new = "if(tool==='symbol'&&symbolStamp==='beam'&&drawing?.mode==='beamSymbol'){const d=drawing,tip=inputPoint(e.clientX,e.clientY),a=screenPoint(d.start),b=screenPoint(tip);drawing=null;if(Math.hypot(a.x-b.x,a.y-b.y)<18){setHint('Drag the beam triangle further so its direction is clear');setTimeout(hint,1200);draw();return}push();state.symbols.push({id:uid(),x:d.start.x,y:d.start.y,beamEnd:{x:tip.x,y:tip.y},type:'beam',color:symbolColor,scale:symbolStampScale,rotation:0,scope:surveyMode?'survey':'plan',group:null});changed();setHint('Beam placed · triangle points where your finger finished');setTimeout(hint,1000);return}if(['symbol','quickLabel','label','note','pinNote','pinPhoto','erase','poly','layoutPoly'].includes(tool)&&tapStart&&Math.hypot(e.clientX-tapStart.x,e.clientY-tapStart.y)>12){drawing=null;return}"
text = replace_once(text, pu_marker, pu_new, 'beam pointer up')

# Live canvas beam rendering and drag preview.
live_old = "const stampSize=Math.min(img.width,img.height)*.018*v.s;if(state.layers.symbols!==false)for(const sm of symbolsForMode(state.symbols,surveyMode?'survey':'plan')){const p=map(sm);drawSymbol(ctx,p,sm.type,stampSize*(sm.scale||1),sm.color||'#172333',sm.rotation||0);if(sm.reference)symbolReference(ctx,p,sm.reference,stampSize*(sm.scale||1))}if(state.layers.notes!==false)"
live_new = "const stampSize=Math.min(img.width,img.height)*.018*v.s;if(state.layers.symbols!==false)for(const sm of symbolsForMode(state.symbols,surveyMode?'survey':'plan')){const p=map(sm);if(sm.type==='beam'&&sm.beamEnd)drawBeamTriangle(ctx,p,map(sm.beamEnd),stampSize*(sm.scale||1),sm.color||'#172333');else drawSymbol(ctx,p,sm.type,stampSize*(sm.scale||1),sm.color||'#172333',sm.rotation||0);if(sm.reference)symbolReference(ctx,p,sm.reference,stampSize*(sm.scale||1))}if(!navMode&&drawing?.mode==='beamSymbol')drawBeamTriangle(ctx,map(drawing.start),map(drawing.now),stampSize*symbolStampScale,symbolColor,true);if(state.layers.notes!==false)"
text = replace_once(text, live_old, live_new, 'live beam rendering')

# Export the same beam geometry that the engineer drew onsite.
export_old = "for(const sm of d.symbols){drawSymbol(x,map(sm),sm.type,stampSize*(sm.scale||1),sm.color||'#172333',sm.rotation||0);if(sm.reference)symbolReference(x,map(sm),sm.reference,stampSize*(sm.scale||1))}"
export_new = "for(const sm of d.symbols){const sp=map(sm);if(sm.type==='beam'&&sm.beamEnd)drawBeamTriangle(x,sp,map(sm.beamEnd),stampSize*(sm.scale||1),sm.color||'#172333');else drawSymbol(x,sp,sm.type,stampSize*(sm.scale||1),sm.color||'#172333',sm.rotation||0);if(sm.reference)symbolReference(x,sp,sm.reference,stampSize*(sm.scale||1))}"
text = replace_once(text, export_old, export_new, 'export beam rendering')

# Direct pointer tracking for the zoom dock range. This bypasses iOS/Android
# native range quirks caused by the no-scroll drawing wrapper.
zoom_old = "$('viewZoom').oninput=e=>zoomAtCentre(2**Number(e.target.value));$('viewZoomIn').onclick=()=>zoomAtCentre(zoom*1.3);$('viewZoomOut').onclick=()=>zoomAtCentre(zoom/1.3);$('viewFit').onclick=()=>$('fit').click();"
zoom_new = "let zoomSliderPointer=null;function zoomSliderAt(clientX){const input=$('viewZoom'),r=input.getBoundingClientRect(),min=Number(input.min),max=Number(input.max),t=clamp((clientX-r.left)/Math.max(1,r.width));const value=min+t*(max-min);input.value=String(value);zoomAtCentre(2**value)}const zoomSlider=$('viewZoom');zoomSlider.oninput=e=>zoomAtCentre(2**Number(e.target.value));zoomSlider.addEventListener('pointerdown',e=>{if(!img)return;zoomSliderPointer=e.pointerId;e.preventDefault();e.stopPropagation();try{zoomSlider.setPointerCapture(e.pointerId)}catch(_){}zoomSliderAt(e.clientX)});zoomSlider.addEventListener('pointermove',e=>{if(e.pointerId!==zoomSliderPointer)return;e.preventDefault();e.stopPropagation();zoomSliderAt(e.clientX)});const finishZoomSlide=e=>{if(e.pointerId!==zoomSliderPointer)return;e.preventDefault();e.stopPropagation();zoomSliderAt(e.clientX);zoomSliderPointer=null;try{zoomSlider.releasePointerCapture(e.pointerId)}catch(_){}};zoomSlider.addEventListener('pointerup',finishZoomSlide);zoomSlider.addEventListener('pointercancel',e=>{if(e.pointerId===zoomSliderPointer)zoomSliderPointer=null});$('viewZoomIn').onclick=()=>zoomAtCentre(zoom*1.3);$('viewZoomOut').onclick=()=>zoomAtCentre(zoom/1.3);$('viewFit').onclick=()=>$('fit').click();"
text = replace_once(text, zoom_old, zoom_new, 'finger zoom slider')

# If a symbol is changed to/from Beam in Properties, keep a valid directional
# endpoint for Beam and remove it again for ordinary point detectors.
prop_old = "if(ref.type==='symbols'){o.type=$('propSymbolType').value;o.color=$('propColor').value;o.reference=$('propDevice').value.trim().slice(0,24);o.scope=surveyMode?'survey':'plan'}"
prop_new = "if(ref.type==='symbols'){o.type=$('propSymbolType').value;o.color=$('propColor').value;o.reference=$('propDevice').value.trim().slice(0,24);o.scope=surveyMode?'survey':'plan';if(o.type==='beam'&&!o.beamEnd){const step=gridStep();o.beamEnd=snapGridPoint({x:clamp(o.x+step/img.width),y:o.y})}else if(o.type!=='beam'&&o.beamEnd)delete o.beamEnd}"
text = replace_once(text, prop_old, prop_new, 'beam properties endpoint')

# Version bump for installable update.
gradle = Path('app/build.gradle').read_text()
gradle = gradle.replace('versionCode 42', 'versionCode 43').replace("versionName '0.41'", "versionName '0.42'")
Path('app/build.gradle').write_text(gradle)

p.write_text(text)
for path in ['ZoneSketch.html', 'Zone-Sketch-by-Will.html', 'app/src/main/assets/index.html']:
    Path(path).write_text(text)

print('Applied v0.42: finger zoom slider, stretched beam triangle and grid-safe detector duplication')
