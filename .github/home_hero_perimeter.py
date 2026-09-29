from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

V4_START = '/* Home hero perimeter trace v4 — continuous lap around the Home hero only. */'
V4_END = '/* End Home hero perimeter trace v4. */'
V5_START = '/* Home hero perimeter trace v5 — gradient head with a short fading trail. */'
V5_END = '/* End Home hero perimeter trace v5. */'
START = '/* Home hero perimeter trace v6 — slower, fuller gradient head with a soft fading trail. */'
END = '/* End Home hero perimeter trace v6. */'
CSS = r'''
/* Home hero perimeter trace v6 — slower, fuller gradient head with a soft fading trail. */
@keyframes zsHeroPerimeterTrailFarRun{to{stroke-dashoffset:-86}}
@keyframes zsHeroPerimeterTrailMidRun{to{stroke-dashoffset:-90}}
@keyframes zsHeroPerimeterTrailNearRun{to{stroke-dashoffset:-94.5}}
@keyframes zsHeroPerimeterHeadRun{to{stroke-dashoffset:-100}}

/* Keep the card itself calm. The travelling cyan→lime head and its soft tail are
   the only bright perimeter motion, matching the restrained technical/glass UI. */
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
  stroke-linejoin:round;
  vector-effect:non-scaling-stroke;
}

/* The trail is deliberately fuller than v5 so it reads as part of the hero frame,
   not a hairline. Each layer gets wider/brighter toward the head, while the rear
   still dissolves softly into the dark border. */
#projectsHome .zsHeroPerimeterTrailFar{
  stroke-width:2.1;
  stroke-dasharray:14 86;
  stroke-dashoffset:14;
  opacity:.13;
  filter:drop-shadow(0 0 3px rgba(115,222,255,.08));
}
#projectsHome .zsHeroPerimeterTrailMid{
  stroke-width:2.55;
  stroke-dasharray:10 90;
  stroke-dashoffset:10;
  opacity:.22;
  filter:drop-shadow(0 0 3px rgba(143,231,202,.07));
}
#projectsHome .zsHeroPerimeterTrailNear{
  stroke-width:2.95;
  stroke-dasharray:5.5 94.5;
  stroke-dashoffset:5.5;
  opacity:.34;
  filter:drop-shadow(0 0 4px rgba(199,255,150,.09));
}

/* Rounded micro-dash = travelling dot. It shares the same user-space gradient as
   the tail, so the colour changes naturally as it moves around the hero frame. */
#projectsHome .zsHeroPerimeterHead{
  stroke-width:6.2;
  stroke-dasharray:.01 99.99;
  stroke-dashoffset:0;
  opacity:.88;
  filter:
    drop-shadow(0 0 3px rgba(115,222,255,.18))
    drop-shadow(0 0 6px rgba(155,255,63,.10));
}

/* Slower 8.4s lap gives the motion the same measured pace as the rest of the Home UI. */
html body.zsMotionActive #projectsHome .zsHeroPerimeterTrailFar{
  animation:zsHeroPerimeterTrailFarRun 8.4s linear infinite!important;
  will-change:stroke-dashoffset;
}
html body.zsMotionActive #projectsHome .zsHeroPerimeterTrailMid{
  animation:zsHeroPerimeterTrailMidRun 8.4s linear infinite!important;
  will-change:stroke-dashoffset;
}
html body.zsMotionActive #projectsHome .zsHeroPerimeterTrailNear{
  animation:zsHeroPerimeterTrailNearRun 8.4s linear infinite!important;
  will-change:stroke-dashoffset;
}
html body.zsMotionActive #projectsHome .zsHeroPerimeterHead{
  animation:zsHeroPerimeterHeadRun 8.4s linear infinite!important;
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
/* End Home hero perimeter trace v6. */
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
    const w=Math.max(2,box.width),h=Math.max(2,box.height),i=1.7;
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

# Upgrade v4/v5 or refresh an existing v6 block while remaining idempotent.
blocks = [
    (START, END),
    (V5_START, V5_END),
    (V4_START, V4_END),
]
replaced = False
for block_start, block_end in blocks:
    if block_start in text and block_end in text:
        start = text.index(block_start)
        end = text.index(block_end, start) + len(block_end)
        text = text[:start] + CSS + text[end:]
        replaced = True
        break
if not replaced:
    known_markers = [m for pair in blocks for m in pair]
    if any(marker in text for marker in known_markers):
        raise SystemExit('index.html: partial Home perimeter marker found')
    if '</style>' not in text:
        raise SystemExit('index.html: closing style tag not found')
    text = text.replace('</style>', '\n' + CSS + '\n</style>', 1)

# Always replace the SVG when it already exists so older markup upgrades cleanly.
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

# Replace geometry too so all four paths stay perfectly aligned on resize/rotation.
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
print('index.html: Home hero perimeter slowed and visually integrated with a fuller soft trail')
