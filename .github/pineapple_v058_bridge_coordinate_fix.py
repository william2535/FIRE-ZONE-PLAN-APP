from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / '.github' / 'pineapple_v058_editor_patch.py'
APP = ROOT / 'index.html'
COPIES = [
    ROOT / 'Zone-Sketch-by-Will.html',
    ROOT / 'ZoneSketch.html',
    ROOT / 'app' / 'src' / 'main' / 'assets' / 'index.html',
]

BAD_BRIDGE = "conflict.crossings.map(h=>({point:cbPxBoard(h.point,w,h),axis:h.axis||'h'}))"
GOOD_BRIDGE = "conflict.crossings.map(hit=>({point:cbPxBoard(hit.point,w,h),axis:hit.axis||'h'}))"

OLD_REBASE = "function cbRebaseCircuit(c,bounds){if(!c||c.type!=='conventional'||!bounds)return false;const old=c.bounds;if(!old){c.bounds={...bounds};c.layout=cbMakeLayout([c.panelId,...(c.deviceIds||[])],c.bounds);return true}if(cbBoundsNear(old,bounds)){c.layout=cbMakeLayout([c.panelId,...(c.deviceIds||[])],bounds);return false}for(const leg of c.legs||[])leg.points=(leg.points||[]).map(p=>cbPlanToBoard(cbBoardToPlan(p,old),bounds));c.bounds={...bounds};c.layout=cbMakeLayout([c.panelId,...(c.deviceIds||[])],c.bounds);return true}"
NEW_REBASE = "function cbRebaseCircuit(c,bounds){if(!c||c.type!=='conventional'||!bounds)return false;const old=c.bounds;if(!old){c.bounds={...bounds};c.layout=cbMakeLayout([c.panelId,...(c.deviceIds||[])],c.bounds);return true}if(cbBoundsNear(old,bounds)){c.layout=cbMakeLayout([c.panelId,...(c.deviceIds||[])],bounds);return false}const remap=p=>cbPlanToBoard(cbBoardToPlan(p,old),bounds);for(const leg of c.legs||[])leg.points=(leg.points||[]).map(remap);for(const b of c.bridges||[])if(b?.point)b.point=remap(b.point);const d=c.editDraft;if(d){for(const leg of d.legs||[])leg.points=(leg.points||[]).map(remap);for(const g of d.gaps||[]){if(g?.a)g.a=remap(g.a);if(g?.b)g.b=remap(g.b)}for(const b of d.bridges||[])if(b?.point)b.point=remap(b.point);const p=d.pending;if(p){if(p.startPoint)p.startPoint=remap(p.startPoint);if(p.endPoint)p.endPoint=remap(p.endPoint);p.points=(p.points||[]).map(remap);for(const b of p.bridges||[])if(b?.point)b.point=remap(b.point)}}c.bounds={...bounds};c.layout=cbMakeLayout([c.panelId,...(c.deviceIds||[])],c.bounds);return true}"

OLD_STAGE = ".cbShell{grid-template-columns:1fr}.cbSide{display:none}.cbStage{padding:7px}"
NEW_STAGE = ".cbShell{grid-template-columns:1fr}.cbSide{display:none}.cbStage{padding:7px 7px calc(7px + env(safe-area-inset-bottom))}"
OLD_OPTIONS = ".cbEditOptionsPanel{position:fixed;top:auto;bottom:72px;right:8px;left:8px;width:auto}"
NEW_OPTIONS = ".cbEditOptionsPanel{position:fixed;top:auto;bottom:calc(72px + env(safe-area-inset-bottom));right:8px;left:8px;width:auto}"


def replace_once_or_present(path: Path, old: str, new: str, label: str) -> bool:
    text = path.read_text(encoding='utf-8')
    old_count = text.count(old)
    new_count = text.count(new)
    if old_count == 1:
        path.write_text(text.replace(old, new, 1), encoding='utf-8')
        print(f'fixed {label} in {path.relative_to(ROOT)}')
        return True
    if old_count == 0 and new_count >= 1:
        print(f'{label} already present in {path.relative_to(ROOT)}')
        return False
    raise SystemExit(f'{label} in {path}: expected one old token or an existing new token, found old={old_count}, new={new_count}')


# Keep the editor generator source safe for future re-application.
replace_once_or_present(GENERATOR, BAD_BRIDGE, GOOD_BRIDGE, 'bridge crossing callback')
replace_once_or_present(GENERATOR, OLD_OPTIONS, NEW_OPTIONS, 'mobile Cleanup safe-area offset')

# Repair the current app source, then mirror it byte-for-byte to every generated copy.
replace_once_or_present(APP, BAD_BRIDGE, GOOD_BRIDGE, 'bridge crossing callback')
replace_once_or_present(APP, OLD_REBASE, NEW_REBASE, 'conventional bounds rebase')
replace_once_or_present(APP, OLD_STAGE, NEW_STAGE, 'mobile Circuit Builder bottom safe area')
replace_once_or_present(APP, OLD_OPTIONS, NEW_OPTIONS, 'mobile Cleanup safe-area offset')

for dst in COPIES:
    shutil.copyfile(APP, dst)

for path in [APP, *COPIES]:
    text = path.read_text(encoding='utf-8')
    required = [GOOD_BRIDGE, NEW_REBASE, NEW_STAGE, NEW_OPTIONS]
    for token in required:
        if token not in text:
            raise SystemExit(f'{path}: expected Project Pineapple repair token missing')
    if BAD_BRIDGE in text or OLD_REBASE in text or OLD_STAGE in text or OLD_OPTIONS in text:
        raise SystemExit(f'{path}: stale Project Pineapple coordinate/safe-area token remains')

print('Pineapple coordinate rebase and iPhone bottom-edge repairs applied to all app copies')
