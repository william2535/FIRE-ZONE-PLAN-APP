from pathlib import Path
from PIL import Image

APP_HTML = Path('index.html')
SOURCE = Path('assets/brand/master-v2-approved/production/zone-sketch-primary-256.png')
MARK_PNG = Path('assets/zone-sketch-complete-house-v2.png')
OLD_MARK_SVG = Path('assets/zone-sketch-header-mark.svg')

# The approved icon is already a transparent, complete-house mark. Preserve its
# pixels exactly; the header uses the same artwork as the splash, tester hub and
# launcher rather than deriving a cropped/recoloured approximation.
img = Image.open(SOURCE).convert('RGBA')
mark = img.copy()
MARK_PNG.parent.mkdir(parents=True, exist_ok=True)
mark.save(MARK_PNG, 'PNG', optimize=True)
if OLD_MARK_SVG.exists():
    OLD_MARK_SVG.unlink()

text = APP_HTML.read_text(encoding='utf-8')
OLD_MARKER = '/* Header logo home button — transparent mark + restrained gloss sweep. */'
NEW_MARKER = '/* Header logo home button — approved original artwork + gloss only. */'
CSS = r'''
/* Header logo home button — approved original artwork + gloss only. */
@keyframes zsHeaderHomeShine{
  0%,70%,100%{transform:translateX(-190%) skewX(-18deg);opacity:0}
  75%{opacity:0}
  79%{opacity:.9}
  88%{transform:translateX(285%) skewX(-18deg);opacity:.10}
  90%{opacity:0}
}
.top .zsHeaderHomeBtn{
  position:relative;display:grid;place-items:center;flex:none;width:48px;height:48px;padding:0!important;
  border:0!important;border-radius:0!important;background:transparent!important;box-shadow:none!important;
  overflow:visible;cursor:pointer;touch-action:manipulation;transition:transform .14s ease!important;
}
.top .zsHeaderHomeBtn img{
  width:46px;height:46px;display:block;object-fit:contain;border-radius:0!important;
  filter:none!important;box-shadow:none!important;pointer-events:none;position:relative;z-index:1;
}
.zsHeaderHomeShine{
  position:absolute;z-index:2;inset:1px;pointer-events:none;overflow:hidden;
  -webkit-mask:url('assets/zone-sketch-complete-house-v2.png') center/contain no-repeat;
  mask:url('assets/zone-sketch-complete-house-v2.png') center/contain no-repeat;
}
.zsHeaderHomeShine:before{
  content:'';position:absolute;top:-28%;bottom:-28%;left:-55%;width:30%;opacity:0;
  background:linear-gradient(105deg,transparent 0,rgba(255,255,255,.06) 28%,rgba(255,255,255,.92) 49%,rgba(225,253,255,.24) 62%,transparent 100%);
  transform:translateX(-190%) skewX(-18deg);
}
body.zsMotionActive .zsHeaderHomeShine:before{animation:zsHeaderHomeShine 9.6s ease-in-out infinite}
body.zsMotionPaused .zsHeaderHomeShine:before{animation-play-state:paused!important}
.top .zsHeaderHomeBtn:active{transform:scale(.97)}
.top .zsHeaderHomeBtn:focus-visible{outline:2px solid #8eeaff!important;outline-offset:2px}
@media(max-width:720px){
  .top .zsHeaderHomeBtn{width:44px;height:44px}
  .top .zsHeaderHomeBtn img{width:42px;height:42px}
}
'''.strip()

# Replace the previous experimental block in place rather than stacking another effect.
marker_pos = text.find(OLD_MARKER)
if marker_pos < 0:
    marker_pos = text.find(NEW_MARKER)
if marker_pos >= 0:
    block_end = text.find('/* App motion parity', marker_pos)
    if block_end < 0:
        raise SystemExit('index.html: App motion parity marker not found after header logo CSS')
    text = text[:marker_pos] + CSS + '\n\n' + text[block_end:]
else:
    if '</style>' not in text:
        raise SystemExit('index.html: closing style tag not found')
    text = text.replace('</style>', CSS + '\n</style>', 1)

# Keep the existing Home button behavior, pointing it at the exact transparent mark.
text = text.replace('src="assets/zone-sketch-header-mark.svg"', 'src="assets/zone-sketch-complete-house-v2.png"')
text = text.replace('src="assets/zone-sketch-header-mark.png"', 'src="assets/zone-sketch-complete-house-v2.png"')

if 'id="headerHomeBtn"' not in text:
    old_header = '<div class="zsBrandLockup"><img src="assets/on-site-zone-planner-icon.webp" alt=""><div class="brand">ZONE SKETCH<small>BY WILL FLOOD · PLAN / ZONE MAKER · BETA v0.62</small></div></div>'
    new_header = '<div class="zsBrandLockup"><button type="button" id="headerHomeBtn" class="zsHeaderHomeBtn" aria-label="Home / Projects" title="Home / Projects"><span class="zsHeaderHomeShine" aria-hidden="true"></span><img src="assets/zone-sketch-complete-house-v2.png" alt="" aria-hidden="true"></button><div class="brand">ZONE SKETCH<small>BY WILL FLOOD · PLAN / ZONE MAKER · BETA v0.62</small></div></div>'
    if old_header not in text:
        raise SystemExit('index.html: expected header brand lockup not found')
    text = text.replace(old_header, new_header, 1)

home_handler = "$('homeBtn').onclick=()=>projectAction(openProjects);"
header_handler = "$('headerHomeBtn').onclick=()=>projectAction(openProjects);"
if header_handler not in text:
    if home_handler not in text:
        raise SystemExit('index.html: Home / Projects handler not found')
    text = text.replace(home_handler, header_handler + home_handler, 1)

APP_HTML.write_text(text, encoding='utf-8')
print('index.html: approved original logo restored; background removed; gloss-only animation retained')
print(f'{MARK_PNG}: generated from {SOURCE} without RGB recolouring')
