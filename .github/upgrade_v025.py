from pathlib import Path

ROOT = Path('.')
html_paths = [
    ROOT/'index.html',
    ROOT/'ZoneSketch.html',
    ROOT/'Zone-Sketch-by-Will.html',
    ROOT/'app/src/main/assets/index.html',
]
text = html_paths[0].read_text()


def rep(old, new, label):
    global text
    if old not in text:
        raise SystemExit(f'v0.25 patch marker missing: {label}')
    text = text.replace(old, new, 1)

# Version shown to browser/app users.
text = text.replace('v0.24', 'v0.25')

# Notes use the same scalable drawing model as room labels/symbols.
rep(
    "function badge(c,x,y,label,color){c.save();c.font='bold 18px system-ui';const W=Math.max(34,c.measureText(label).width+18);c.fillStyle='#fff';c.fillRect(x-W/2-2,y-18,W+4,35);c.fillStyle=color;c.fillRect(x-W/2,y-16,W,31);c.fillStyle='#fff';c.textAlign='center';c.textBaseline='middle';c.fillText(label,x,y);c.restore()}",
    "function badge(c,x,y,label,color,scale=1){const s=Math.max(.25,Math.min(4,Number(scale)||1)),fs=18*s;c.save();c.font=`bold ${fs}px system-ui`;const W=Math.max(34*s,c.measureText(label).width+18*s);c.fillStyle='#fff';c.fillRect(x-W/2-2*s,y-18*s,W+4*s,35*s);c.fillStyle=color;c.fillRect(x-W/2,y-16*s,W,31*s);c.fillStyle='#fff';c.textAlign='center';c.textBaseline='middle';c.fillText(label,x,y);c.restore()}",
    'scalable note badge'
)

# Give note/pin selections real bounds so they have usable blue resize handles.
rep(
    "if(ref.type==='labels'&&img){const sc=o.scale||1,fs=Math.min(img.width,img.height)*.022*sc,w=(Math.max(1,(o.text||'').length)*fs*.62+fs*.9)/img.width,h=fs*1.6/img.height;return{x1:clamp(o.x-w/2),y1:clamp(o.y-h/2),x2:clamp(o.x+w/2),y2:clamp(o.y+h/2)}}if(ref.type==='symbols'&&img)",
    "if(ref.type==='labels'&&img){const sc=o.scale||1,fs=Math.min(img.width,img.height)*.022*sc,w=(Math.max(1,(o.text||'').length)*fs*.62+fs*.9)/img.width,h=fs*1.6/img.height;return{x1:clamp(o.x-w/2),y1:clamp(o.y-h/2),x2:clamp(o.x+w/2),y2:clamp(o.y+h/2)}}if(ref.type==='notes'&&img){const sc=o.scale||1,v=transform(),fs=18*sc,w=Math.max(34*sc,Math.max(1,(o.text||'').length)*fs*.62+18*sc)/(img.width*v.s),h=35*sc/(img.height*v.s);return{x1:clamp(o.x-w/2),y1:clamp(o.y-h/2),x2:clamp(o.x+w/2),y2:clamp(o.y+h/2)}}if(ref.type==='pins'&&img){const r=Math.min(img.width,img.height)*.018*.72*(o.scale||1),w=r*2.5/img.width,h=r*2.5/img.height;return{x1:clamp(o.x-w/2),y1:clamp(o.y-h/2),x2:clamp(o.x+w/2),y2:clamp(o.y+h/2)}}if(ref.type==='symbols'&&img)",
    'note and pin selection bounds'
)

rep(
    "if(snap.ref.type==='labels'||snap.ref.type==='symbols')o.scale=Math.max(.25,Math.min(4,(src.scale||1)*Math.sqrt(Math.abs(sx*sy))))",
    "if(['labels','symbols','notes','pins'].includes(snap.ref.type))o.scale=Math.max(.25,Math.min(4,(src.scale||1)*Math.sqrt(Math.abs(sx*sy))))",
    'resize note and pin scale'
)

# Properties Size slider now applies to notes and pins too.
rep(
    "hasScale=['labels','symbols'].includes(ref.type),canTransform=",
    "hasScale=['labels','symbols','notes','pins'].includes(ref.type),canTransform=",
    'properties note scale visibility'
)
rep(
    "if(['labels','symbols'].includes(ref.type))o.scale=Number($('propScale').value)||1;",
    "if(['labels','symbols','notes','pins'].includes(ref.type))o.scale=Math.max(.25,Math.min(4,Number($('propScale').value)||1));",
    'properties note scale save'
)

# Existing note/pin creation gets scale=1; older saved objects safely fall back to 1.
rep(
    "state.pins.push({id:uid(),...inputPoint(e.clientX,e.clientY),kind:'note',text:value.trim().slice(0,80),group:null})",
    "state.pins.push({id:uid(),...inputPoint(e.clientX,e.clientY),kind:'note',text:value.trim().slice(0,80),scale:1,group:null})",
    'new pinned note scale'
)
rep(
    "state.notes.push({id:uid(),...inputPoint(e.clientX,e.clientY),text:value.trim().slice(0,50)})",
    "state.notes.push({id:uid(),...inputPoint(e.clientX,e.clientY),text:value.trim().slice(0,50),scale:1})",
    'new normal note scale'
)
rep(
    "state.pins.push({id:uid(),x:at.x,y:at.y,kind:'photo',text:caption||'Site photo',image:c.toDataURL('image/jpeg',.7),group:null})",
    "state.pins.push({id:uid(),x:at.x,y:at.y,kind:'photo',text:caption||'Site photo',image:c.toDataURL('image/jpeg',.7),scale:1,group:null})",
    'new photo pin scale'
)

# Scale note badges and pinned markers both on screen and in office exports.
rep(
    "drawPin(ctx,{...pin,...p},i,stampSize*.72)",
    "drawPin(ctx,{...pin,...p},i,stampSize*.72*(pin.scale||1))",
    'onscreen pin scale'
)
rep(
    "badge(ctx,p.x,p.y,n.text,'#1b344e')",
    "badge(ctx,p.x,p.y,n.text,'#1b344e',n.scale||1)",
    'onscreen note scale'
)
rep(
    "drawPin(x,{...d.pins[i],...map(d.pins[i])},i,stampSize*.72)",
    "drawPin(x,{...d.pins[i],...map(d.pins[i])},i,stampSize*.72*(d.pins[i].scale||1))",
    'export pin scale'
)
rep(
    "badge(x,p.x,p.y,n.text,'#1b344e')",
    "badge(x,p.x,p.y,n.text,'#1b344e',n.scale||1)",
    'export note scale'
)

# Keep all HTML entry points identical.
for p in html_paths:
    p.write_text(text)

# Android update version.
build = ROOT/'app/build.gradle'
b = build.read_text()
if "versionCode 24" not in b or "versionName '0.24'" not in b:
    raise SystemExit('v0.25 expected Android v0.24 baseline was not found')
b = b.replace('versionCode 24', 'versionCode 25', 1).replace("versionName '0.24'", "versionName '0.25'", 1)
build.write_text(b)

# Document the user-facing change.
readme = ROOT/'README.md'
r = readme.read_text()
if '## v0.25 — Resizable notes' not in r:
    r += """

## v0.25 — Resizable notes

Plan notes can now be made smaller or larger. Select a normal Note or pinned site-detail marker and use **Properties → Size**, or drag the blue corner resize handles directly on the plan. Note/pin scale is stored with the project and is preserved in PNG/PDF office exports. Existing projects keep their current visual size until changed.
"""
readme.write_text(r)

print('Applied On Site Zone Planner v0.25 resizable notes upgrade')
