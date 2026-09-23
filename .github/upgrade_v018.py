from pathlib import Path
import re

paths = [Path('index.html'), Path('ZoneSketch.html'), Path('app/src/main/assets/index.html')]
t = paths[0].read_text()

old_draw = re.compile(r"function drawSymbol\(c,p,type,size,color='#172333'\)\{.*?\}\nfunction drawPin", re.S)
new_draw = """function drawSymbol(c,p,type,size,color='#172333',rotation=0){const r=Math.max(5,size),label={panel:'FAP',mcp:'MCP',smoke:'SD',heat:'HD',sounder:'S',you:'YOU'}[type]||'?';c.save();c.translate(p.x,p.y);c.rotate((Number(rotation)||0)*Math.PI/180);c.strokeStyle=color;c.fillStyle='#fff';c.lineWidth=Math.max(.8,r*.09);c.textAlign='center';c.textBaseline='middle';if(type==='panel'||type==='mcp'){const w=r*2.15,h=r*1.55;c.fillRect(-w/2,-h/2,w,h);c.strokeRect(-w/2,-h/2,w,h)}else if(type==='you'){c.beginPath();c.moveTo(0,-r*1.1);c.lineTo(r*.78,r*.45);c.lineTo(0,r*.12);c.lineTo(-r*.78,r*.45);c.closePath();c.fill();c.stroke()}else{c.beginPath();c.arc(0,0,r,0,Math.PI*2);c.fill();c.stroke()}c.fillStyle=color;c.font=`700 ${Math.max(5,r*.55)}px system-ui`;c.fillText(label,0,type==='you'?r*.7:0);c.restore()}
function drawPin"""
t, n = old_draw.subn(new_draw, t, count=1)
if n != 1:
    raise SystemExit(f'drawSymbol replacement failed: {n}')

repls = {
    "drawSymbol(ctx,p,sm.type,stampSize*(sm.scale||1),sm.color||'#172333')": "drawSymbol(ctx,p,sm.type,stampSize*(sm.scale||1),sm.color||'#172333',sm.rotation||0)",
    "drawSymbol(x,map(sm),sm.type,stampSize*(sm.scale||1),sm.color||'#172333')": "drawSymbol(x,map(sm),sm.type,stampSize*(sm.scale||1),sm.color||'#172333',sm.rotation||0)",
    "mapObjectPoints(r.type,o,fn);if(mode==='mirror'&&r.type==='doors')o.side=-(o.side||1)": "mapObjectPoints(r.type,o,fn);if(mode==='rotate'&&r.type==='symbols')o.rotation=((Number(o.rotation)||0)+90)%360;if(mode==='mirror'&&r.type==='doors')o.side=-(o.side||1)",
    "canTransform=['walls','doors','windows','shutters','stairs','shapes'].includes(ref.type)": "canTransform=['walls','doors','windows','shutters','stairs','shapes','symbols'].includes(ref.type)",
}
for old, new in repls.items():
    if old not in t:
        raise SystemExit('missing marker: ' + old[:90])
    t = t.replace(old, new, 1)

# New stamps explicitly start at 0 degrees, while old saved drafts safely default to 0 at render time.
old_stamp = "state.symbols.push({id:uid(),...inputPoint(e.clientX,e.clientY),type:symbolStamp,color:symbolColor,scale:1,group:null})"
new_stamp = "state.symbols.push({id:uid(),...inputPoint(e.clientX,e.clientY),type:symbolStamp,color:symbolColor,scale:1,rotation:0,group:null})"
if old_stamp in t:
    t = t.replace(old_stamp, new_stamp, 1)

for p in paths:
    p.write_text(t)

print('Applied v0.18 symbol orientation support to all app copies')
