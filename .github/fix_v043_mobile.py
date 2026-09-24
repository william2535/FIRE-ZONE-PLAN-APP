from pathlib import Path

p=Path('index.html')
t=p.read_text()

def once(old,new,label):
    global t
    if new in t and old not in t:return
    if old not in t:raise SystemExit(f'v0.43 mobile fix marker missing: {label}')
    t=t.replace(old,new,1)

# Keep the ghost building unclamped so off-crop rooms are clipped instead of
# collapsing into a heavy border. Device positions are separately constrained.
once("return{x:clamp(CB_INSET+(p.x-b.x1)/w*CB_SPAN,.04,.96),y:clamp(CB_INSET+(p.y-b.y1)/h*CB_SPAN,.04,.96)}",
     "return{x:CB_INSET+(p.x-b.x1)/w*CB_SPAN,y:CB_INSET+(p.y-b.y1)/h*CB_SPAN}",
     'unclamped ghost transform')

# The tablet sidebar is intentionally hidden on phones, so duplicate the created
# circuit list and Finish As-Fit action into the main landing page for mobile.
once('<button id="cbAddressableStart" class="primary">Highlight a loop</button></div></div></section>',
     '<button id="cbAddressableStart" class="primary">Highlight a loop</button></div></div><div class="cbModePanel cbMainStatus"><h2>Created circuits</h2><div id="cbExistingMain"></div><button id="cbFinishAsFitMain" class="cbFinish" disabled>Finish As-Fit</button><p id="cbFinishStatusMain" class="cbEmpty">Complete the circuits you create, then build the As-Fit.</p></div></section>',
     'mobile circuit status card')

css='''\n.cbMainStatus{margin-top:12px}\n@media(min-width:761px){.cbMainStatus{display:none}}\n'''
if '.cbMainStatus{margin-top:12px}' not in t:t=t.replace('</style>',css+'</style>',1)

old="if(!list.length){const e=document.createElement('div');e.className='cbEmpty';e.textContent='No circuits built yet.';existing.append(e)}const ready=list.length>0&&list.every(c=>c.complete);$('cbFinishAsFit').disabled=!ready;$('cbFinishStatus').textContent=ready?'All created circuits are complete. Finish builds the As-Fit from the real surveyed positions.':list.length?'Complete every circuit above before finishing the As-Fit.':'Complete the circuits you create, then build the As-Fit.'}"
new="if(!list.length){const e=document.createElement('div');e.className='cbEmpty';e.textContent='No circuits built yet.';existing.append(e)}const main=$('cbExistingMain');if(main){main.textContent='';for(const c of list){const row=document.createElement('div');row.className='cbCircuitRow'+(c.complete?' done':'');row.style.setProperty('--cb-color',c.color||'#65768a');const dot=document.createElement('span');dot.className='cbDot';const label=document.createElement('div');const s=document.createElement('strong');s.textContent=c.name;const small=document.createElement('small');small.textContent=(c.type==='addressable'?'Addressable loop':'Conventional')+' · '+(c.deviceIds?.length||0)+' devices'+(c.complete?' · complete':'');label.append(s,small);const open=document.createElement('button');open.textContent='Open';open.onclick=()=>cbOpenCircuit(c);row.append(dot,label,open);main.append(row)}if(!list.length){const e=document.createElement('div');e.className='cbEmpty';e.textContent='No circuits built yet.';main.append(e)}}const ready=list.length>0&&list.every(c=>c.complete),status=ready?'All created circuits are complete. Finish builds the As-Fit from the real surveyed positions.':list.length?'Complete every circuit above before finishing the As-Fit.':'Complete the circuits you create, then build the As-Fit.';$('cbFinishAsFit').disabled=!ready;$('cbFinishStatus').textContent=status;if($('cbFinishAsFitMain'))$('cbFinishAsFitMain').disabled=!ready;if($('cbFinishStatusMain'))$('cbFinishStatusMain').textContent=status}"
once(old,new,'mobile created circuits rendering')

once("$('cbFinishAsFit').onclick=cbFinishAsFit;$('cbAsFitBack').onclick=()=>cbShow('home');",
     "$('cbFinishAsFit').onclick=cbFinishAsFit;if($('cbFinishAsFitMain'))$('cbFinishAsFitMain').onclick=cbFinishAsFit;$('cbAsFitBack').onclick=()=>cbShow('home');",
     'mobile finish handler')

p.write_text(t)
for q in [Path('ZoneSketch.html'),Path('Zone-Sketch-by-Will.html'),Path('app/src/main/assets/index.html')]:q.write_text(t)
print('Applied v0.43 mobile Circuit Builder hardening')
