from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

utility = '<div class="brandUtility" data-brand-watch><span class="brandUtilityLabel"><i class="brandBeacon" aria-hidden="true"></i>YOUR WORKSPACE / 01</span><button type="button" class="brandMotionToggle" data-brand-motion aria-label="Decorative motion" aria-pressed="false">Motion</button></div>'
if utility in text:
    text = text.replace(utility, '', 1)
elif 'YOUR WORKSPACE / 01' in text or 'data-brand-motion' in text:
    raise SystemExit('home utility markup changed unexpectedly')
else:
    print('home utility already removed')

old_intro = "/* Motion belongs to the brand shell; it never touches a drawing or project.\n   Reduced Motion is the default, not a lock: the visible button can override it. */"
new_intro = "/* Decorative brand motion is always enabled. Functional UI motion remains separate. */"
if old_intro in text:
    text = text.replace(old_intro, new_intro, 1)

old = " const buttons=[...document.querySelectorAll('[data-brand-motion]')];\n if(!buttons.length)return;\n const media=window.matchMedia('(prefers-reduced-motion: reduce)');\n let mode='auto';\n try{\n  const saved=localStorage.getItem('zoneSketchBrandMotionMode');\n  if(saved==='on'||saved==='off'||saved==='auto')mode=saved;\n  else if(localStorage.getItem('zoneSketchBrandMotion')==='off')mode='off';\n }catch(e){}"
new = " const buttons=[];\n const media=window.matchMedia('(prefers-reduced-motion: reduce)');\n let mode='on';"
if old in text:
    text = text.replace(old, new, 1)
elif "const buttons=[];" not in text or "let mode='on';" not in text:
    raise SystemExit('brand motion bootstrap changed unexpectedly')

# Remove toggle click wiring and storage-driven mode changes; keep system/app state observers so
# brand motion classes stay synchronized without exposing a user-facing control.
old_click = " buttons.forEach(b=>b.addEventListener('click',()=>{\n  mode=active()?'off':'on';\n  save();sync();\n }));"
if old_click in text:
    text = text.replace(old_click, '', 1)

old_storage = " window.addEventListener('storage',e=>{\n  if(e.key==='zoneSketchBrandMotionMode'||e.key==='zoneSketchBrandMotion'){\n   try{const saved=localStorage.getItem('zoneSketchBrandMotionMode');mode=(saved==='on'||saved==='off'||saved==='auto')?saved:(localStorage.getItem('zoneSketchBrandMotion')==='off'?'off':'auto')}catch(err){}\n   sync();\n  }\n });"
if old_storage in text:
    text = text.replace(old_storage, '', 1)

p.write_text(text, encoding='utf-8')
