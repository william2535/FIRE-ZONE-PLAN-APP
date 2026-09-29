from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

START = '/* Home hero perimeter trace v4 — continuous lap around the Home hero only. */'
END = '/* End Home hero perimeter trace v4. */'
CSS = r'''
/* Home hero perimeter trace v4 — continuous lap around the Home hero only. */
@property --zsHeroTraceAngle{
  syntax:'<angle>';
  inherits:false;
  initial-value:0deg;
}
@keyframes zsHeroPerimeterRun{to{--zsHeroTraceAngle:360deg}}

#projectsHome .homeProductHero:before{
  content:''!important;
  position:absolute!important;
  inset:0!important;
  width:auto!important;
  height:auto!important;
  border-radius:inherit!important;
  padding:2px!important;
  background:conic-gradient(
    from var(--zsHeroTraceAngle),
    transparent 0deg 254deg,
    rgba(0,194,255,.10) 270deg,
    #73deff 289deg,
    #c7ff96 310deg,
    #9bff3f 327deg,
    transparent 345deg 360deg
  )!important;
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0)!important;
  -webkit-mask-composite:xor!important;
  mask-composite:exclude!important;
  transform:none!important;
  opacity:1!important;
  box-shadow:none!important;
  filter:drop-shadow(0 0 5px rgba(155,255,63,.30));
  pointer-events:none!important;
  z-index:4!important;
}

html body.zsMotionActive #projectsHome .homeProductHero:before{
  animation:zsHeroPerimeterRun 4.2s linear infinite!important;
  will-change:background;
}
body.zsMotionPaused #projectsHome .homeProductHero:before{animation-play-state:paused!important}
body.zsMotionOff #projectsHome .homeProductHero:before{animation:none!important}
@media(prefers-reduced-motion:reduce){
  body:not(.zsMotionActive) #projectsHome .homeProductHero:before{animation:none!important}
}
/* End Home hero perimeter trace v4. */
'''.strip()

if START in text and END in text:
    start = text.index(START)
    end = text.index(END, start) + len(END)
    text = text[:start] + CSS + text[end:]
elif START not in text and END not in text:
    if '</style>' not in text:
        raise SystemExit('index.html: closing style tag not found')
    text = text.replace('</style>', '\n' + CSS + '\n</style>', 1)
else:
    raise SystemExit('index.html: partial Home perimeter marker found')

p.write_text(text, encoding='utf-8')
print('index.html: Home hero perimeter trace set to a continuous 4.2s lap')
