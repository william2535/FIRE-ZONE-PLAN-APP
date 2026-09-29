from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

OLD_START = '/* Home hero perimeter trace v4 — continuous lap around the Home hero only. */'
OLD_END = '/* End Home hero perimeter trace v4. */'
START = '/* Home hero perimeter trace v5 — gradient head with a short fading trail. */'
END = '/* End Home hero perimeter trace v5. */'
CSS = r'''
/* Home hero perimeter trace v5 — gradient head with a short fading trail. */
@keyframes zsHeroPerimeterTrailFarRun{to{stroke-dashoffset:-88}}
@keyframes zsHeroPerimeterTrailMidRun{to{stroke-dashoffset:-92}}
@keyframes zsHeroPerimeterTrailNearRun{to{stroke-dashoffset:-96}}
@keyframes zsHeroPerimeterHeadRun{to{stroke-dashoffset:-100}}

/* Keep the base hero border clean: this travelling head + fading trail is the
   only bright motion on the Home hero perimeter. */
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

#projectsHome .zsHeroPerimeterTrace,
#projectsHome .zsHeroPerimeterTrailMid,
#projectsHome .zsHeroPerimeterTrailNear,
#projectsHome .zsHeroPerimeterHead{
  fill:none;
  stroke:url(#zsHeroTraceGradient);
  stroke-linecap:round;
  vector-effect:non-scaling-stroke;
}

/* Three perfectly synced layers create a soft taper: the further the trail gets
   from the head, the thinner and more transparent it becomes. Total trail length
   is 12% of the perimeter, shorter than the previous 18% solid segment. */
#projectsHome .zsHeroPerimeterTrailFar{
  stroke-width:1.25;
  stroke-dasharray:12 88;
  stroke-dashoffset:12;
  opacity:.10;
  filter:drop-shadow(0 0 2px rgba(115,222,255,.06));
}
#projectsHome .zsHeroPerimeterTrailMid{
  stroke-width:1.5;
  stroke-dasharray:8 92;
  stroke-dashoffset:8;
  opacity:.16;
}
#projectsHome .zsHeroPerimeterTrailNear{
  stroke-width:1.75;
  stroke-dasharray:4 96;
  stroke-dashoffset:4;
  opacity:.24;
}

/* A tiny rounded dash behaves as the travelling dot. Because it uses the exact
   same user-space gradient and perimeter path, its colour changes with position
   and it stays attached to the front of all three trail layers. */
#projectsHome .zsHeroPerimeterHead{
  stroke-width:5.2;
  stroke-dasharray:.01 99.99;
  stroke-dashoffset:0;
  opacity:.82;
  filter:drop-shadow(0 0 3px rgba(199,255,150,.20));
}

html body.zsMotionActive #projectsHome .zsHeroPerimeterTrailFar{
  animation:zsHeroPerimeterTrailFarRun 5.6s linear infinite!important;
  will-change:stroke-dashoffset;
}
html body.zsMotionActive #projectsHome .zsHeroPerimeterTrailMid{
  animation:zsHeroPerimeterTrailMidRun 5.6s linear infinite!important;
  will-change:stroke-dashoffset;
}
html body.zsMotionActive #projectsHome .zsHeroPerimeterTrailNear{
  animation:zsHeroPerimeterTrailNearRun 5.6s linear infinite!important;
  will-change:stroke-dashoffset;
}
html body.zsMotionActive #projectsHome .zsHeroPerimeterHead{
  animation:zsHeroPerimeterHeadRun 5.6s linear infinite!important;
  will-change:stroke-dashoffset;
}

body.zsMotionPaused #projectsHome .zsHeroPerimeterTrailFar,
body.zsMotionPaused #projectsHome .zsHeroPerimeterTrailMid,
body.zsMotionPaused #projectsHome .zsHeroPerimeterTrailNear,
body.zsMotionPaused #projectsHome .zsHeroPerimeterHead{
  animation-play-state:paused!important;
}
body.zsMotionOff #projectsHome .zsHeroPerimeterTrailFar,
body.zsMotionOff #projectsHome .zsHeroPerimeterTrailMid,
body.zsMotionOff #projectsHome .zsHeroPerimeterTrailNear,
body.zsMotionOff #projectsHome .zsHeroPerimeterHead{
  animation:none!important;
  opacity:0!important;
}
@media(prefers-reduced-motion:reduce){
  body:not(.zsMotionActive) #projectsHome .zsHeroPerimeterTrailFar,
  body:not(.zsMotionActive) #projectsHome .zsHeroPerimeterTrailMid,
  body:not(.zsMotionActive) #projectsHome .zsHeroPerimeterTrailNear,
  body:not(.zsMotionActive) #projectsHome .zsHeroPerimeterHead{animation:none!important}
}
/* End Home hero perimeter trace v5. */
'''.strip()

SVG_MARKUP = '''<svg class="zsHeroPerimeterSvg" aria-hidden="true" focusable="false" preserveAspectRatio="none"><defs><linearGradient id="zsHeroTraceGradient" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#73deff"/><stop offset="0.52" stop-color="#c7ff96"/><stop offset="1" stop-color="#9bff3f"/></linearGradient></defs><path class="zsHeroPerimeterTrace zsHeroPerimeterTrailFar" pathLength="100" d=""/><path class="zsHeroPerimeterTrailMid" pathLength="100" d=""/><path class="zsHeroPerimeterTrailNear" pathLength="100" d=""/><path class="zsHeroPerimeterHead" pathLength="100" d=""/></svg>'''
SVG_ANCHOR = '<span class="brandOrbit" aria-hidden="true"></span>'

GEOMETRY_SCRIPT = r'''<script id="zsHeroPerimeterGeometry">
(()=>{
  const hero=document.querySelector('#projectsHome .homeProductHero');
  const svg=hero&&hero.querySelector('.zsHeroPerimeterSvg');
  const paths=svg&&Array.from(svg.querySelectorAll('.zsHeroPerimeterTrace,.zsHeroPerimeterTrailMid,.zsHeroPerimeterTrailNear,.zsHeroPerimeterHead'));
  const grad=svg&&svg.querySelector('#zsHeroTraceGradient');
  if(!hero||!svg||!grad||!paths||paths.length!==4)return;
  const radius=(name,limit)=>Math.min(limit,Math.max(.1,parseFloat(getComputedStyle(hero)[name])||0));
  const sync=()=>{
    const box=hero.getBoundingClientRect();
    const w=Math.max(2,box.width),h=Math.max(2,box.height),i=1.4;
    const lim=Math.max(.1,Math.min(w,h)/2-i);
    const rtl=radius('borderTopLeftRadius',lim),rtr=radius('borderTopRightRadius',lim);
    const rbr=radius('borderBottomRightRadius',lim),rbl=radius('borderBottomLeftRadius',lim);
    svg.setAttribute('viewBox',`0 0 ${w} ${h}`);
    grad.setAttribute('x2',String(w));grad.setAttribute('y2',String(h));
    const d=[
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
    ].join(' ');
    paths.forEach(path=>path.setAttribute('d',d));
  };
  sync();
  if('ResizeObserver' in window){new ResizeObserver(sync).observe(hero)}
  else{window.addEventListener('resize',sync,{passive:true})}
})();
</script>'''

# Upgrade either the old v4 block or an existing v5 block, while remaining idempotent.
if START in text and END in text:
    start = text.index(START)
    end = text.index(END, start) + len(END)
    text = text[:start] + CSS + text[end:]
elif OLD_START in text and OLD_END in text:
    start = text.index(OLD_START)
    end = text.index(OLD_END, start) + len(OLD_END)
    text = text[:start] + CSS + text[end:]
elif START not in text and END not in text and OLD_START not in text and OLD_END not in text:
    if '</style>' not in text:
        raise SystemExit('index.html: closing style tag not found')
    text = text.replace('</style>', '\n' + CSS + '\n</style>', 1)
else:
    raise SystemExit('index.html: partial Home perimeter marker found')

# Always replace the SVG when it already exists so v4 markup upgrades to the
# separate fading trail layers plus moving head path.
svg_start = text.find('<svg class="zsHeroPerimeterSvg"')
if svg_start >= 0:
    svg_end = text.find('</svg>', svg_start)
    if svg_end < 0:
        raise SystemExit('index.html: Home hero SVG closing tag not found')
    svg_end += len('</svg>')
    text = text[:svg_start] + SVG_MARKUP + text[svg_end:]
else:
    if SVG_ANCHOR not in text:
        raise SystemExit('index.html: Home hero SVG anchor not found')
    text = text.replace(SVG_ANCHOR, SVG_ANCHOR + SVG_MARKUP, 1)

# Replace the geometry script as well so every trail/head path follows the exact
# same responsive rounded rectangle after rotations and resizes.
script_start = text.find('<script id="zsHeroPerimeterGeometry">')
if script_start >= 0:
    script_end = text.find('</script>', script_start)
    if script_end < 0:
        raise SystemExit('index.html: Home perimeter geometry closing script not found')
    script_end += len('</script>')
    text = text[:script_start] + GEOMETRY_SCRIPT + text[script_end:]
else:
    if '</body>' not in text:
        raise SystemExit('index.html: closing body tag not found')
    text = text.replace('</body>', GEOMETRY_SCRIPT + '\n</body>', 1)

p.write_text(text, encoding='utf-8')
print('index.html: Home hero now uses a gradient head with a short fading perimeter trail')
