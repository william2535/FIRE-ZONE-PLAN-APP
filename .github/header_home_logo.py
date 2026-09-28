from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

CSS_MARKER = '/* Header logo home button — transparent mark + restrained gloss sweep. */'
CSS = r'''

/* Header logo home button — transparent mark + restrained gloss sweep. */
@keyframes zsHeaderHomeShine{
  0%,68%,100%{transform:translateX(-175%) skewX(-18deg);opacity:0}
  73%{opacity:.08}
  78%{opacity:.8}
  88%{transform:translateX(245%) skewX(-18deg);opacity:.12}
  90%{opacity:0}
}
@keyframes zsHeaderHomeGlow{
  0%,100%{filter:drop-shadow(0 0 6px rgba(0,194,255,.16)) drop-shadow(0 0 9px rgba(155,255,63,.08))}
  50%{filter:drop-shadow(0 0 9px rgba(0,194,255,.28)) drop-shadow(0 0 13px rgba(155,255,63,.15))}
}
.top .zsHeaderHomeBtn{
  position:relative;display:grid;place-items:center;flex:none;width:46px;height:46px;padding:0!important;
  border:0!important;border-radius:14px;background:transparent!important;box-shadow:none!important;
  overflow:hidden;isolation:isolate;cursor:pointer;touch-action:manipulation;
  transition:transform .15s ease,filter .15s ease!important;
}
.top .zsHeaderHomeBtn img{
  width:42px;height:42px;display:block;object-fit:contain;border-radius:0!important;
  filter:drop-shadow(0 0 7px rgba(0,194,255,.2)) drop-shadow(0 0 10px rgba(155,255,63,.1));
  pointer-events:none;position:relative;z-index:1;
}
.top .zsHeaderHomeBtn:before{
  content:'';position:absolute;inset:5px;border-radius:13px;
  background:radial-gradient(circle at 50% 56%,rgba(0,194,255,.08),transparent 66%);
  opacity:.55;pointer-events:none;z-index:0;
}
.top .zsHeaderHomeBtn:after{
  content:'';position:absolute;inset:3px;border-radius:13px;
  box-shadow:inset 0 0 0 1px rgba(126,229,255,.05);pointer-events:none;z-index:3;
}
.zsHeaderHomeShine{
  position:absolute;z-index:2;top:-15%;bottom:-15%;left:-36%;width:34%;pointer-events:none;opacity:0;
  background:linear-gradient(105deg,transparent 0,rgba(255,255,255,.04) 28%,rgba(255,255,255,.82) 49%,rgba(193,252,255,.3) 60%,transparent 100%);
  filter:blur(.2px);transform:translateX(-175%) skewX(-18deg);
}
body.zsMotionActive .zsHeaderHomeShine{animation:zsHeaderHomeShine 9.6s ease-in-out infinite}
body.zsMotionActive .zsHeaderHomeBtn img{animation:zsHeaderHomeGlow 8.4s ease-in-out infinite}
body.zsMotionPaused .zsHeaderHomeShine,body.zsMotionPaused .zsHeaderHomeBtn img{animation-play-state:paused!important}
.top .zsHeaderHomeBtn:hover{filter:brightness(1.08)}
.top .zsHeaderHomeBtn:active{transform:scale(.955)}
.top .zsHeaderHomeBtn:focus-visible{outline:2px solid #8eeaff!important;outline-offset:2px}
@media(max-width:720px){
  .top .zsHeaderHomeBtn{width:42px;height:42px;border-radius:13px}
  .top .zsHeaderHomeBtn img{width:38px;height:38px}
}
'''

OLD_HEADER = '<div class="zsBrandLockup"><img src="assets/on-site-zone-planner-icon.webp" alt=""><div class="brand">ZONE SKETCH<small>BY WILL FLOOD · PLAN / ZONE MAKER · BETA v0.62</small></div></div>'
NEW_HEADER = '<div class="zsBrandLockup"><button type="button" id="headerHomeBtn" class="zsHeaderHomeBtn" aria-label="Home / Projects" title="Home / Projects"><span class="zsHeaderHomeShine" aria-hidden="true"></span><img src="assets/zone-sketch-header-mark.svg" alt="" aria-hidden="true"></button><div class="brand">ZONE SKETCH<small>BY WILL FLOOD · PLAN / ZONE MAKER · BETA v0.62</small></div></div>'

OLD_HANDLER = "$('homeBtn').onclick=()=>projectAction(openProjects);"
NEW_HANDLER = "$('headerHomeBtn').onclick=()=>projectAction(openProjects);" + OLD_HANDLER

changed = False

if CSS_MARKER not in text:
    if '</style>' not in text:
        raise SystemExit('index.html: closing style tag not found')
    text = text.replace('</style>', CSS + '\n</style>', 1)
    changed = True

if 'id="headerHomeBtn"' not in text:
    if OLD_HEADER not in text:
        raise SystemExit('index.html: expected header brand lockup not found')
    text = text.replace(OLD_HEADER, NEW_HEADER, 1)
    changed = True

if "$('headerHomeBtn').onclick=()=>projectAction(openProjects);" not in text:
    if OLD_HANDLER not in text:
        raise SystemExit('index.html: Home / Projects handler not found')
    text = text.replace(OLD_HANDLER, NEW_HANDLER, 1)
    changed = True

if changed:
    p.write_text(text, encoding='utf-8')
    print('index.html: transparent animated home logo installed')
else:
    print('index.html: header home logo already current')
