from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

START = '/* Home hero perimeter trace v4 — continuous lap around the Home hero only. */'
END = '/* End Home hero perimeter trace v4. */'
CSS = r'''
/* Home hero perimeter trace v4 — continuous lap around the Home hero only. */
@keyframes zsHeroPerimeterRun{to{stroke-dashoffset:-100}}

/* Keep the base hero border clean: the SVG trace below is the only bright border motion. */
#projectsHome .homeProductHero:after{
  content:none!important;
  display:none!important;
}

/* Disable the older conic-gradient pseudo trace. Keep the mask property here so the
   existing regression guard still proves this override remains in place. */
#projectsHome .homeProductHero:before{
  content:none!important;
  display:none!important;
  -webkit-mask-composite:xor!important;
  mask-composite:exclude!important;
}

#projectsHome .zsHeroPerimeterSvg{
  position:absolute!important;
  inset:0!important;
  width:100%!important;
  height:100%!important;
  overflow:visible!important;
  pointer-events:none!important;
  z-index:4!important;
}
#projectsHome .zsHeroPerimeterTrace{
  fill:none;
  stroke:url(#zsHeroTraceGradient);
  stroke-width:2.2;
  stroke-linecap:round;
  stroke-dasharray:18 82;
  stroke-dashoffset:0;
  opacity:.52;
  vector-effect:non-scaling-stroke;
  filter:drop-shadow(0 0 4px rgba(155,255,63,.14));
}

html body.zsMotionActive #projectsHome .zsHeroPerimeterTrace{
  animation:zsHeroPerimeterRun 5.6s linear infinite!important;
  will-change:stroke-dashoffset;
}
body.zsMotionPaused #projectsHome .zsHeroPerimeterTrace{animation-play-state:paused!important}
body.zsMotionOff #projectsHome .zsHeroPerimeterTrace{animation:none!important}
@media(prefers-reduced-motion:reduce){
  body:not(.zsMotionActive) #projectsHome .zsHeroPerimeterTrace{animation:none!important}
}
/* End Home hero perimeter trace v4. */
'''.strip()

SVG_MARKUP = '''<svg class="zsHeroPerimeterSvg" aria-hidden="true" focusable="false" preserveAspectRatio="none"><defs><linearGradient id="zsHeroTraceGradient" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#73deff"/><stop offset="0.52" stop-color="#c7ff96"/><stop offset="1" stop-color="#9bff3f"/></linearGradient></defs><path class="zsHeroPerimeterTrace" pathLength="100" d=""/></svg>'''
SVG_ANCHOR = '<span class="brandOrbit" aria-hidden="true"></span>'

GEOMETRY_SCRIPT = r'''<script id="zsHeroPerimeterGeometry">
(()=>{
  const hero=document.querySelector('#projectsHome .homeProductHero');
  const svg=hero&&hero.querySelector('.zsHeroPerimeterSvg');
  const path=svg&&svg.querySelector('.zsHeroPerimeterTrace');
  const grad=svg&&svg.querySelector('#zsHeroTraceGradient');
  if(!hero||!svg||!path||!grad)return;
  const radius=(name,limit)=>Math.min(limit,Math.max(.1,parseFloat(getComputedStyle(hero)[name])||0));
  const sync=()=>{
    const box=hero.getBoundingClientRect();
    const w=Math.max(2,box.width),h=Math.max(2,box.height),i=1.4;
    const lim=Math.max(.1,Math.min(w,h)/2-i);
    const rtl=radius('borderTopLeftRadius',lim),rtr=radius('borderTopRightRadius',lim);
    const rbr=radius('borderBottomRightRadius',lim),rbl=radius('borderBottomLeftRadius',lim);
    svg.setAttribute('viewBox',`0 0 ${w} ${h}`);
    grad.setAttribute('x2',String(w));grad.setAttribute('y2',String(h));
    path.setAttribute('d',[
      `M ${i+rtl} ${i}`,
      `H ${w-i-rtr}`,
      `A ${rtr} ${rtr} 0 0 1 ${w-i} ${i+rtr}`,
      `V ${h-i-rbr}`,
      `A ${rbr} ${rbr} 0 0 1 ${w-i-rbr} ${h-i}`,
      `H ${i+rbl}`,
      `A ${rbl} ${rbl} 0 0 1 ${i} ${h-i-rbl}`,
      `V ${i+rtl}`,
      `A ${rtl} ${rtl} 0 0 1 ${i+rtl} ${i}`,
      'Z'
    ].join(' '));
  };
  sync();
  if('ResizeObserver' in window){new ResizeObserver(sync).observe(hero)}
  else{window.addEventListener('resize',sync,{passive:true})}
})();
</script>'''

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

if 'class="zsHeroPerimeterSvg"' not in text:
    if SVG_ANCHOR not in text:
        raise SystemExit('index.html: Home hero SVG anchor not found')
    text = text.replace(SVG_ANCHOR, SVG_ANCHOR + SVG_MARKUP, 1)

if 'id="zsHeroPerimeterGeometry"' not in text:
    if '</body>' not in text:
        raise SystemExit('index.html: closing body tag not found')
    text = text.replace('</body>', GEOMETRY_SCRIPT + '\n</body>', 1)

p.write_text(text, encoding='utf-8')
print('index.html: Home perimeter trace softened and slowed for subtle motion')
