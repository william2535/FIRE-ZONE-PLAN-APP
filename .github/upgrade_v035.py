from pathlib import Path

ROOT = Path('.')
html_paths = [
    ROOT/'index.html',
    ROOT/'ZoneSketch.html',
    ROOT/'Zone-Sketch-by-Will.html',
    ROOT/'app/src/main/assets/index.html',
]

text = html_paths[0].read_text()
if 'Zone Sketch by Will v0.34' not in text:
    raise SystemExit('v0.35 expected v0.34 HTML baseline was not found')

old_slider = '<input id="symbolStampScale" type="range" min="0.25" max="4" step="0.05" value="1" aria-label="New symbol size">'
new_slider = '<input id="symbolStampScale" type="range" min="0.10" max="4" step="0.05" value="1" aria-label="New symbol size">'
if old_slider not in text:
    raise SystemExit('v0.35 could not find symbol size slider minimum')
text = text.replace(old_slider, new_slider, 1)

old_load = "function loadSymbolScale(){try{const v=Number(localStorage.getItem('zoneSketchSymbolScale'));if(Number.isFinite(v)&&v>=.25&&v<=4)return v}catch(e){}return 1}"
new_load = "function loadSymbolScale(){try{const v=Number(localStorage.getItem('zoneSketchSymbolScale'));if(Number.isFinite(v)&&v>=.10&&v<=4)return v}catch(e){}return 1}"
if old_load not in text:
    raise SystemExit('v0.35 could not find symbol scale loader')
text = text.replace(old_load, new_load, 1)

old_set = "function setSymbolStampScale(value){const v=Number(value);symbolStampScale=Number.isFinite(v)?Math.max(.25,Math.min(4,v)):1;try{localStorage.setItem('zoneSketchSymbolScale',String(symbolStampScale))}catch(e){}syncSymbolScale()}"
new_set = "function setSymbolStampScale(value){const v=Number(value);symbolStampScale=Number.isFinite(v)?Math.max(.10,Math.min(4,v)):1;try{localStorage.setItem('zoneSketchSymbolScale',String(symbolStampScale))}catch(e){}syncSymbolScale()}"
if old_set not in text:
    raise SystemExit('v0.35 could not find symbol scale clamp')
text = text.replace(old_set, new_set, 1)

old_draw = "function drawSymbol(c,p,type,size,color='#172333',rotation=0){const r=Math.max(5,size),label={panel:'FAP',mcp:'MCP',smoke:'SD',heat:'HD',sounder:'S',beacon:'VAD',repeater:'REP',you:'YOU'}[type]||'?';c.save();c.translate(p.x,p.y);c.rotate((Number(rotation)||0)*Math.PI/180);c.strokeStyle=color;c.fillStyle='#fff';c.lineWidth=Math.max(.8,r*.09);c.textAlign='center';c.textBaseline='middle';if(type==='panel'||type==='mcp'||type==='repeater'){const w=r*2.15,h=r*1.55;c.fillRect(-w/2,-h/2,w,h);c.strokeRect(-w/2,-h/2,w,h)}else if(type==='you'){c.beginPath();c.moveTo(0,-r*1.1);c.lineTo(r*.78,r*.45);c.lineTo(0,r*.12);c.lineTo(-r*.78,r*.45);c.closePath();c.fill();c.stroke()}else{c.beginPath();c.arc(0,0,r,0,Math.PI*2);c.fill();c.stroke()}c.fillStyle=color;c.font=`700 ${Math.max(5,r*.55)}px system-ui`;c.fillText(label,0,type==='you'?r*.7:0);c.restore()}"
new_draw = "function drawSymbol(c,p,type,size,color='#172333',rotation=0){const r=Math.max(2,size),label={panel:'FAP',mcp:'MCP',smoke:'SD',heat:'HD',sounder:'S',beacon:'VAD',repeater:'REP',you:'YOU'}[type]||'?';c.save();c.translate(p.x,p.y);c.rotate((Number(rotation)||0)*Math.PI/180);c.strokeStyle=color;c.fillStyle='#fff';c.lineWidth=Math.max(.45,r*.09);c.textAlign='center';c.textBaseline='middle';if(type==='panel'||type==='mcp'||type==='repeater'){const w=r*2.15,h=r*1.55;c.fillRect(-w/2,-h/2,w,h);c.strokeRect(-w/2,-h/2,w,h)}else if(type==='you'){c.beginPath();c.moveTo(0,-r*1.1);c.lineTo(r*.78,r*.45);c.lineTo(0,r*.12);c.lineTo(-r*.78,r*.45);c.closePath();c.fill();c.stroke()}else{c.beginPath();c.arc(0,0,r,0,Math.PI*2);c.fill();c.stroke()}c.fillStyle=color;c.font=`700 ${Math.max(2.5,r*.55)}px system-ui`;c.fillText(label,0,type==='you'?r*.7:0);c.restore()}"
if old_draw not in text:
    raise SystemExit('v0.35 could not find symbol renderer')
text = text.replace(old_draw, new_draw, 1)

old_hint = 'Sets the size of new symbols. Symbols already on the plan keep their current size.'
new_hint = 'Sets the size of new symbols from tiny 0.10× up to 4×. Symbols already on the plan keep their current size.'
if old_hint not in text:
    raise SystemExit('v0.35 could not find symbol size hint')
text = text.replace(old_hint, new_hint, 1)

marker = "\n\n/* v0.35 — extra-small symbols: 0.10x slider minimum and a genuinely smaller renderer floor. */\n"
if 'v0.35 — extra-small symbols' not in text:
    text = text.replace('</style>', marker + '</style>', 1)

text = text.replace('<title>Zone Sketch by Will v0.34 — site survey draft</title>', '<title>Zone Sketch by Will v0.35 — site survey draft</title>', 1)
text = text.replace('ON SITE ZONE PLANNER · v0.34', 'ON SITE ZONE PLANNER · v0.35', 1)

for path in html_paths:
    path.write_text(text)

build = ROOT/'app/build.gradle'
b = build.read_text()
if 'versionCode 34' not in b or "versionName '0.34'" not in b:
    raise SystemExit('v0.35 expected Android v0.34 baseline was not found')
b = b.replace('versionCode 34', 'versionCode 35', 1)
b = b.replace("versionName '0.34'", "versionName '0.35'", 1)
build.write_text(b)

print('Applied v0.35: symbols can shrink to 0.10x with a lower rendering floor')
