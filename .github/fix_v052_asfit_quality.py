from pathlib import Path

MAIN = Path('index.html')
t = MAIN.read_text()


def once(old, new, label):
    global t
    if old in t:
        t = t.replace(old, new, 1)
    elif new not in t:
        raise SystemExit(f'v0.52 patch marker missing: {label}')

# Version the main app forward. Company demo copies are deliberately not touched.
t = t.replace('v0.51', 'v0.52')

# Let As-Fit choose a cable width that scales with the detector symbols while preserving
# the existing 5px/7px Circuit Builder game appearance by default.
old_bundle = "function cbDrawBundled(x,segments,map){const counts=new Map(),seen=new Map();for(const s of segments){const k=cbSegKey(s.a,s.b);counts.set(k,(counts.get(k)||0)+1)}for(const s of segments){const k=cbSegKey(s.a,s.b),n=counts.get(k)||1,i=seen.get(k)||0;seen.set(k,i+1);const a=map(s.a),b=map(s.b),dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy)||1,off=(i-(n-1)/2)*7,nx=-dy/L,ny=dx/L;x.save();x.strokeStyle=s.color;x.lineWidth=5;x.lineCap='round';x.lineJoin='round';x.beginPath();x.moveTo(a.x+nx*off,a.y+ny*off);x.lineTo(b.x+nx*off,b.y+ny*off);x.stroke();x.restore()}}"
new_bundle = "function cbDrawBundled(x,segments,map,lineWidth=5,bundleGap=7){const counts=new Map(),seen=new Map();for(const s of segments){const k=cbSegKey(s.a,s.b);counts.set(k,(counts.get(k)||0)+1)}for(const s of segments){const k=cbSegKey(s.a,s.b),n=counts.get(k)||1,i=seen.get(k)||0;seen.set(k,i+1);const a=map(s.a),b=map(s.b),dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy)||1,off=(i-(n-1)/2)*bundleGap,nx=-dy/L,ny=dx/L;x.save();x.strokeStyle=s.color;x.lineWidth=lineWidth;x.lineCap='round';x.lineJoin='round';x.beginPath();x.moveTo(a.x+nx*off,a.y+ny*off);x.lineTo(b.x+nx*off,b.y+ny*off);x.stroke();x.restore()}}"
once(old_bundle, new_bundle, 'configurable cable width')

# Keep export header/legend proportionate when the output canvas is several thousand pixels wide.
old_prefix = "function cbDrawAsFitOn(canvas,W,H,header=false){const x=canvas.getContext('2d');x.setTransform(1,0,0,1,0,0);x.clearRect(0,0,W,H);x.fillStyle='#fff';x.fillRect(0,0,W,H);let top=header?78:16,bottom=header?76:16;if(header){x.fillStyle='#16283e';x.fillRect(0,0,W,64);x.fillStyle='#fff';x.font='800 24px system-ui';x.fillText((state.site||'Site')+' — '+activeFloor().name+' — AS-FIT',30,29);x.font='13px system-ui';x.fillText('Generated from Zone Plan + Site Survey + completed Circuit Builder routes',30,50)}const aw=W-50,ah=H-top-bottom,aspect=img?img.width/img.height:1.6;"
new_prefix = "// v0.52 As-Fit quality — thin proportional cable, retina preview and high-resolution PNG export.\nfunction cbDrawAsFitOn(canvas,W,H,header=false){const x=canvas.getContext('2d');x.setTransform(1,0,0,1,0,0);x.clearRect(0,0,W,H);x.fillStyle='#fff';x.fillRect(0,0,W,H);const uiScale=header?Math.max(1,W/2400):1;let top=header?78*uiScale:16,bottom=header?76*uiScale:16;if(header){x.fillStyle='#16283e';x.fillRect(0,0,W,64*uiScale);x.fillStyle='#fff';x.font=`800 ${24*uiScale}px system-ui`;x.fillText((state.site||'Site')+' — '+activeFloor().name+' — AS-FIT',30*uiScale,29*uiScale);x.font=`${13*uiScale}px system-ui`;x.fillText('Generated from Zone Plan + Site Survey + completed Circuit Builder routes',30*uiScale,50*uiScale)}const aw=W-50*uiScale,ah=H-top-bottom,aspect=img?img.width/img.height:1.6;"
once(old_prefix, new_prefix, 'scaled export chrome')

# Cable is now a small fraction of the detector radius, so it cannot visually overpower devices.
old_segments = "const segments=cbAsFitSegments();cbDrawBundled(x,segments,map);const size=Math.min(pw,ph)*.018;"
new_segments = "const size=Math.min(pw,ph)*.018,cableWidth=Math.max(1.05,size*.13),bundleGap=Math.max(cableWidth*1.9,size*.22),segments=cbAsFitSegments();cbDrawBundled(x,segments,map,cableWidth,bundleGap);"
once(old_segments, new_segments, 'thin proportional As-Fit cable')

# Scale the exported footer legend too, rather than leaving tiny text on a large PNG.
once("if(header){let lx=30,ly=H-35;x.textAlign='left';x.font='700 13px system-ui';", "if(header){let lx=30*uiScale,ly=H-35*uiScale;x.textAlign='left';x.font=`700 ${13*uiScale}px system-ui`;", 'scaled footer start')
once("x.fillRect(lx,ly-11,18,5);", "x.fillRect(lx,ly-11*uiScale,18*uiScale,5*uiScale);", 'scaled footer swatch')
once("lx+25,ly", "lx+25*uiScale,ly", 'scaled footer label')
once("lx+=Math.min(320,x.measureText(c.name).width+150);", "lx+=Math.min(320*uiScale,x.measureText(c.name).width+150*uiScale);", 'scaled footer spacing')
once("if(lx>W-280){lx=30;ly-=22}", "if(lx>W-280*uiScale){lx=30*uiScale;ly-=22*uiScale}", 'scaled footer wrap')

# The old preview rendered to a CSS-size temporary canvas and then enlarged it on retina screens.
# Draw straight into the high-density backing canvas instead so lines, text and device symbols stay crisp.
old_preview = "function cbDrawAsFitPreview(){const c=$('cbAsFitCanvas'),r=c.getBoundingClientRect(),dpr=Math.min(devicePixelRatio||1,2),W=Math.max(1,Math.round(r.width*dpr)),H=Math.max(1,Math.round(r.height*dpr));if(c.width!==W)c.width=W;if(c.height!==H)c.height=H;const x=c.getContext('2d');x.setTransform(dpr,0,0,dpr,0,0);x.clearRect(0,0,r.width,r.height);const tmp=document.createElement('canvas');tmp.width=Math.max(1,Math.round(r.width));tmp.height=Math.max(1,Math.round(r.height));cbDrawAsFitOn(tmp,tmp.width,tmp.height,false);x.drawImage(tmp,0,0,r.width,r.height)}"
new_preview = "function cbDrawAsFitPreview(){const c=$('cbAsFitCanvas'),r=c.getBoundingClientRect(),dpr=Math.min(devicePixelRatio||1,3),W=Math.max(1,Math.round(r.width*dpr)),H=Math.max(1,Math.round(r.height*dpr));if(c.width!==W)c.width=W;if(c.height!==H)c.height=H;cbDrawAsFitOn(c,W,H,false)}"
once(old_preview, new_preview, 'retina As-Fit preview')

# PNG export is now at least 4800px wide and up to 5600px, roughly doubling source-plan width
# where possible while remaining practical on phones/tablets.
old_export = "async function cbExportAsFit(){const base=Math.max(1800,Math.min(3600,img?.width||2400)),aspect=img?img.width/img.height:1.6,W=Math.round(base),H=Math.round(W/aspect+170),c=document.createElement('canvas');"
new_export = "async function cbExportAsFit(){const sourceW=Math.max(1,img?.width||2400),base=Math.max(4800,Math.min(5600,sourceW*2)),aspect=img?img.width/img.height:1.6,W=Math.round(base),H=Math.round(W/aspect+170*(W/2400)),c=document.createElement('canvas');"
once(old_export, new_export, 'high-resolution PNG export')

# Keep all main entry points identical.
for name in ['index.html', 'ZoneSketch.html', 'Zone-Sketch-by-Will.html', 'app/src/main/assets/index.html']:
    Path(name).write_text(t)

# Android release metadata.
g = Path('app/build.gradle').read_text()
g = g.replace('versionCode 52', 'versionCode 53').replace("versionName '0.51'", "versionName '0.52'")
Path('app/build.gradle').write_text(g)

# Add the new quality test to the normal regression runner.
rp = Path('tests/run-regressions.cjs')
r = rp.read_text()
if "'asfit-quality-v052'" not in r:
    r = r.replace("'circuit-grid-routing-v051']", "'circuit-grid-routing-v051','asfit-quality-v052']")
    rp.write_text(r)

assert 'v0.52 As-Fit quality' in t
assert 'size*.13' in t
assert 'Math.max(4800,Math.min(5600,sourceW*2))' in t
assert "versionName '0.52'" in g
print('Applied v0.52 thin-cable high-resolution As-Fit upgrade to main build')
