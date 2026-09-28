from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

MARKER = '/* App motion parity — tester-hub movement mapped onto the real app shell. */'
CSS = r'''

/* App motion parity — tester-hub movement mapped onto the real app shell. */
@keyframes zsAppProjectRail{
  0%{left:16px;opacity:.38;box-shadow:0 0 8px rgba(0,194,255,.10)}
  42%{opacity:1;box-shadow:0 0 14px rgba(0,194,255,.34),0 0 8px rgba(155,255,63,.14)}
  100%{left:calc(100% - 58px);opacity:.45;box-shadow:0 0 8px rgba(155,255,63,.14)}
}
@keyframes zsAppBadgeBeacon{
  0%,100%{opacity:.48;transform:scale(.78);box-shadow:0 0 6px rgba(155,255,63,.30)}
  50%{opacity:1;transform:scale(1.18);box-shadow:0 0 15px rgba(155,255,63,.68),0 0 24px rgba(0,194,255,.12)}
}
@keyframes zsAppButtonSweep{
  0%,67%,100%{left:-70%;opacity:0}
  72%{opacity:.12}
  79%{opacity:.85}
  89%{left:150%;opacity:.10}
  91%{opacity:0}
}
@keyframes zsAppHeadingTrace{
  0%{transform:translateX(-125%);opacity:0}
  15%{opacity:.28}
  48%{opacity:.9}
  80%,100%{transform:translateX(520%);opacity:0}
}

/* The tester page already has moving signal rails. Give the real app project cards
   the same living top-edge signal instead of leaving that accent parked at the left. */
body.zsMotionActive #projectsHome .projectCard:before{
  animation:zsAppProjectRail 8.4s ease-in-out infinite alternate!important;
}
body.zsMotionActive #projectsHome .projectCard:nth-child(2):before{animation-delay:1s!important}
body.zsMotionActive #projectsHome .projectCard:nth-child(3):before{animation-delay:1.9s!important}
body.zsMotionActive #projectsHome .projectCard:nth-child(4):before{animation-delay:2.9s!important}
body.zsMotionActive #projectsHome .projectCard:nth-child(5):before{animation-delay:3.8s!important}
body.zsMotionActive #projectsHome .projectCard:nth-child(6):before{animation-delay:4.8s!important}

/* The ready-state dot now pulses like BETA LIVE on the tester hub. */
body.zsMotionActive #projectsHome .homeHeroBadge:after{
  animation:zsAppBadgeBeacon 3s ease-in-out infinite!important;
  transform-origin:center;
}

/* Tester primary actions visibly sweep even on touch screens. Mirror that ambient
   gloss on the app CTA instead of relying on desktop hover, which tablets never get. */
body.zsMotionActive #projectsHome button.primary:after{
  animation:zsAppButtonSweep 9.8s ease-in-out infinite!important;
}

/* Recent-project heading gets the same moving cyan/lime trace used by tester panels. */
#projectsHome .homeHeading{position:relative;overflow:hidden}
#projectsHome .homeHeading:after{
  content:'';position:absolute;left:0;top:0;width:60px;height:2px;pointer-events:none;
  background:linear-gradient(90deg,#00c2ff,#9bff3f);opacity:.42;
  transform:translateX(-125%);box-shadow:0 0 12px rgba(0,194,255,.20)
}
body.zsMotionActive #projectsHome .homeHeading:after{
  animation:zsAppHeadingTrace 13.8s ease-in-out infinite!important;
}

/* Keep the already-approved app motion, but make the project-card scan easier to
   actually perceive on a field tablet while retaining the same cyan/lime palette. */
body.zsMotionActive #projectsHome .projectCard:after{
  opacity:1;
  background:linear-gradient(90deg,transparent,rgba(142,231,255,.08),rgba(255,255,255,.15),rgba(155,255,63,.07),transparent);
}

/* Pause every added ambient effect with the existing motion/visibility controls. */
body.zsMotionPaused #projectsHome .projectCard:before,
body.zsMotionPaused #projectsHome .homeHeroBadge:after,
body.zsMotionPaused #projectsHome button.primary:after,
body.zsMotionPaused #projectsHome .homeHeading:after{animation-play-state:paused!important}
body.zsMotionOff #projectsHome .projectCard:before,
body.zsMotionOff #projectsHome .homeHeroBadge:after,
body.zsMotionOff #projectsHome button.primary:after,
body.zsMotionOff #projectsHome .homeHeading:after,
body.reduceMotion #projectsHome .projectCard:before,
body.reduceMotion #projectsHome .homeHeroBadge:after,
body.reduceMotion #projectsHome button.primary:after,
body.reduceMotion #projectsHome .homeHeading:after{animation:none!important}

@media(max-width:720px){
  /* Keep motion optical on touch: no cards physically slide around. */
  body.zsMotionActive #projectsHome .projectCard:before{animation-duration:9.6s!important}
  body.zsMotionActive #projectsHome button.primary:after{animation-duration:11s!important}
}
'''

if MARKER not in text:
    if '</style>' not in text:
        raise SystemExit('index.html: closing style tag not found')
    text = text.replace('</style>', CSS + '\n</style>', 1)
    p.write_text(text, encoding='utf-8')
    print('index.html: app motion parity installed')
else:
    print('index.html: app motion parity already current')
