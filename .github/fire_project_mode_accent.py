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
    opacity:.42;
    box-shadow:0 0 8px rgba(178,28,32,.16),0 0 5px rgba(255,110,54,.08)
  }
  42%{
    opacity:1;
    box-shadow:0 0 15px rgba(255,49,49,.42),0 0 9px rgba(255,126,55,.20)
  }
  100%{
    left:calc(100% - 58px);
    opacity:.5;
    box-shadow:0 0 9px rgba(255,96,48,.24),0 0 5px rgba(146,20,29,.12)
  }
}

/* Fire mode owns the Recent Projects top-edge signal for now.
   Keep the geometry/motion exactly the same; only the semantic colour family changes. */
#projectsHome .projectCard:before{
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
print('index.html: Recent Projects rail set to the Fire red/orange mode accent')
