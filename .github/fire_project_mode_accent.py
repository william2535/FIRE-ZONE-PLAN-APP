from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

START = '/* System-mode project rail v1 — FIRE. */'
END = '/* End system-mode project rail v1. */'
CSS = r'''
/* System-mode project rail v1 — FIRE.
   This moving top rail is a semantic system-mode accent, not decoration only.
   Current mapping: Fire = red/orange.
   Future mappings: Intruder = dark blue, CCTV = light blue/cyan, Access Control = green. */
@keyframes zsFireProjectRail{
  0%{
    left:16px;
    opacity:.58;
    box-shadow:0 0 10px rgba(214,31,37,.28),0 0 6px rgba(255,110,54,.14)
  }
  42%{
    opacity:1;
    box-shadow:0 0 18px rgba(255,49,49,.58),0 0 11px rgba(255,126,55,.30)
  }
  100%{
    left:calc(100% - 70px);
    opacity:.64;
    box-shadow:0 0 12px rgba(255,96,48,.36),0 0 7px rgba(146,20,29,.18)
  }
}

/* Fire mode owns the Recent Projects top-edge signal for now.
   Keep the motion language the same, but make the Fire identifier slightly
   wider/brighter so the system colour is obvious at a glance. */
#projectsHome .projectCard:before{
  width:54px!important;
  height:3px!important;
  border-radius:999px!important;
  background:linear-gradient(90deg,#7d1118 0%,#d8232e 28%,#ff3e38 58%,#ff6a3d 80%,#ff9b45 100%)!important;
}
body.zsMotionActive #projectsHome .projectCard:before{
  animation:zsFireProjectRail 8.4s ease-in-out infinite alternate!important;
}
body.zsMotionActive #projectsHome .projectCard:nth-child(2):before{animation-delay:1s!important}
body.zsMotionActive #projectsHome .projectCard:nth-child(3):before{animation-delay:1.9s!important}
body.zsMotionActive #projectsHome .projectCard:nth-child(4):before{animation-delay:2.9s!important}
body.zsMotionActive #projectsHome .projectCard:nth-child(5):before{animation-delay:3.8s!important}
body.zsMotionActive #projectsHome .projectCard:nth-child(6):before{animation-delay:4.8s!important}
body.zsMotionActive.reduceMotion #projectsHome .projectCard:before{
  animation:zsFireProjectRail 8.4s ease-in-out infinite alternate!important;
}
body.zsMotionPaused #projectsHome .projectCard:before{animation-play-state:paused!important}
body.zsMotionOff #projectsHome .projectCard:before,
body.reduceMotion:not(.zsMotionActive) #projectsHome .projectCard:before{animation:none!important}

@media(max-width:720px){
  body.zsMotionActive #projectsHome .projectCard:before,
  body.zsMotionActive.reduceMotion #projectsHome .projectCard:before{
    animation-duration:9.6s!important;
    animation-iteration-count:infinite!important;
  }
}
/* End system-mode project rail v1. */
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
    raise SystemExit('index.html: partial system-mode project rail marker found')

p.write_text(text, encoding='utf-8')
print('index.html: Fire Recent Projects identifiers made more prominent')
