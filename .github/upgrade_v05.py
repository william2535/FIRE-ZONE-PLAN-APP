from pathlib import Path
import re

p = Path('index.html')
s = p.read_text()
if 'id="gridBtn"' in s and 'data-tool="select"' in s:
    print('Zone Sketch v0.5 already applied')
else:
    def need(old, new, count=1):
        global s
        if old not in s:
            raise SystemExit('Missing expected source fragment: ' + old[:100])
        s = s.replace(old, new, count)

    need('.top button{background:#2a415d;color:white}.top button.primary{background:#ec493b}',
         '.top button{background:#2a415d;color:white}.top button.primary{background:#ec493b}.top button.active{background:#47749f;color:#fff;box-shadow:inset 0 0 0 2px #8db4d8}')
    need('<button class="primary" id="shareBtn">Send to office</button>',
         '<button id="gridBtn">Grid off</button><button class="primary" id="shareBtn">Send to office</button>')
    s = re.sub(r'<div class="selectionBar" id="selectionBar" hidden>.*?</div>',
        '<div class="selectionBar" id="selectionBar" hidden><strong id="selectionText">0 items selected</strong><button class="primary" id="groupSelected">Make group</button><button id="ungroupSelected">Ungroup</button><button id="clearSelection">Clear selection</button><small>Grouped items act as one object in Select / Move.</small></div>', s, count=1)
    need('<button data-tool="erase" class="danger">⌫ Delete</button><button data-tool="group">▣ Group / Move</button><button data-tool="pan">✋ Move plan</button>',
         '<button data-tool="erase" class="danger">⌫ Delete</button><button data-tool="select">↖ Select / Move</button><button data-tool="group">▣ Box select</button><button id="makeGroup" disabled>Group</button><button id="breakGroup" disabled>Ungroup</button><button data-tool="pan">✋ Move plan</button>')
    need("pictureOpacity:1,pictureVisible:true,isBlank:false});", "pictureOpacity:1,pictureVisible:true,isBlank:false,gridVisible:false});")
    need("c.beginPath();c.moveTo(a.x,a.y);const steps=14;", "c.beginPath();c.moveTo(b.x,b.y);const steps=14;")
    need("function syncBackground(){", "function syncGrid(){const b=$('gridBtn');b.classList.toggle('active',!!state.gridVisible);b.textContent=state.gridVisible?'Grid on':'Grid off'}\nfunction drawGrid(c,v){if(!state.gridVisible||!img)return;let step=50;while(step*v.s<28)step*=2;while(step*v.s>72&&step>12.5)step/=2;const left=v.ox,top=v.oy,W=img.width*v.s,H=img.height*v.s;c.save();c.beginPath();c.rect(left,top,W,H);c.clip();c.lineWidth=1;c.strokeStyle='#486b8a32';c.beginPath();for(let x=0;x<=img.width+.001;x+=step){const sx=left+x*v.s;c.moveTo(sx,top);c.lineTo(sx,top+H)}for(let y=0;y<=img.height+.001;y+=step){const sy=top+y*v.s;c.moveTo(left,sy);c.lineTo(left+W,sy)}c.stroke();c.restore()}\nfunction syncBackground(){")
    need("$('togglePicture').onclick=()=>{push();state.pictureVisible=!state.pictureVisible;changed()};\nfunction openDB", "$('togglePicture').onclick=()=>{push();state.pictureVisible=!state.pictureVisible;changed()};$('gridBtn').onclick=()=>{state.gridVisible=!state.gridVisible;syncGrid();draw();persist()};\nfunction openDB")
    need("if(t!=='group')clearSelection();", "if(t!=='group'&&t!=='select')clearSelection();")
    need("erase:'Tap a wall section, door, label, note or zone area to delete only that item',group:'Drag a box around items to select them · then Group or drag the blue selection to move',pan:",
         "erase:'Tap a wall section, door, label, note or zone area to delete only that item',select:'Tap an object and drag it · grouped objects move together as one',group:'Drag a blue box around several objects · then press Group',pan:")

    pattern = r"function syncSelectionBar\(\).*?\$\('clearSelection'\)\.onclick=clearSelection;"
    replacement = """function selectionState(){const groups=[...new Set(selection.map(r=>getObj(r)?.group).filter(Boolean))],allSame=groups.length===1&&selection.length>0&&selection.every(r=>getObj(r)?.group===groups[0]);return{allSame,canGroup:selection.length>=2&&!allSame,canUngroup:allSame}}
function syncSelectionBar(){const bar=$('selectionBar');bar.hidden=!selection.length;const st=selectionState();$('makeGroup').disabled=!st.canGroup;$('breakGroup').disabled=!st.canUngroup;if(!selection.length)return;$('selectionText').textContent=selection.length+' item'+(selection.length===1?'':'s')+(st.allSame?' · grouped':'')+' selected';$('groupSelected').disabled=!st.canGroup;$('ungroupSelected').disabled=!st.canUngroup}
function groupSelection(){const st=selectionState();if(!st.canGroup)return;push();const g=uid();for(const r of selection){const o=getObj(r);if(o)o.group=g}changed();setHint('Group created · use Select / Move to move it as one');setTimeout(hint,1200)}
function ungroupSelection(){const st=selectionState();if(!st.canUngroup)return;push();for(const r of selection){const o=getObj(r);if(o)o.group=null}changed();setHint('Group separated');setTimeout(hint,900)}
$('groupSelected').onclick=groupSelection;$('ungroupSelected').onclick=ungroupSelection;$('makeGroup').onclick=groupSelection;$('breakGroup').onclick=ungroupSelection;
$('clearSelection').onclick=clearSelection;"""
    s, n = re.subn(pattern, replacement, s, count=1, flags=re.S)
    if n != 1: raise SystemExit('Could not replace selection controls')

    need("syncBackground();$('empty').hidden=!!img;", "syncBackground();syncGrid();$('empty').hidden=!!img;")
    need("picture(ctx,v.ox,v.oy,img.width*v.s,img.height*v.s);const map=", "picture(ctx,v.ox,v.oy,img.width*v.s,img.height*v.s);drawGrid(ctx,v);const map=")
    need("if(tool==='group')drawSelection(ctx,map)", "if(tool==='group'||tool==='select')drawSelection(ctx,map)")
    need("if(tool==='group'){const hit=hitRefAt(e.clientX,e.clientY,26);", "if(tool==='select'){const hit=hitRefAt(e.clientX,e.clientY,28);if(!hit){selection=[];syncSelectionBar();draw();return}const o=getObj(hit);selection=o?.group?refsForGroup(o.group):[hit];syncSelectionBar();drawing={mode:'moveSelection',start:point(e.clientX,e.clientY),snap:snapshotSelection(),moved:false};draw();return}if(tool==='group'){const hit=hitRefAt(e.clientX,e.clientY,26);")
    need("else if(tool==='group'&&drawing?.mode==='moveSelection'){", "else if((tool==='group'||tool==='select')&&drawing?.mode==='moveSelection'){", 2)
    need("setHint('Selection moved');", "setHint(selectionState().allSame?'Grouped object moved':'Object moved');")
    need('Group / Move lets you box-select a room and move it as one.', 'Box select lets you choose several items, Group makes them one object, and Select / Move lets you move either one item or a saved group.')

    for out in [Path('index.html'), Path('ZoneSketch.html'), Path('app/src/main/assets/index.html')]:
        out.write_text(s)

readme = Path('README.md')
r = readme.read_text()
if '## Version 0.5 — clean doors, explicit groups, object move and grid' not in r:
    r += """
## Version 0.5 — clean doors, explicit groups, object move and grid

- **Door geometry is cleaner:** the swing arc now starts exactly on the opposite edge of the wall opening, so both ends of the door connect cleanly to the straight wall line.
- **Group is now an explicit action:** use **Box select**, then press **Group** in the bottom toolbar (or **Make group** in the selection bar). **Ungroup** is equally visible.
- **Select / Move** lets you tap and drag one wall section, door, room label, note or zone shape. Tapping any member of a saved group selects and moves the whole group as one object.
- **Grid off / Grid on** is available in the top bar. The grid is a screen-only drawing aid and is deliberately excluded from the exported office PNG.
"""
    readme.write_text(r)
print('v0.5 source prepared')
