from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

START = '/* Home workflow one-shot fill — Plan > Survey > Circuits > As-Fit. */'
END = '/* End home workflow one-shot fill. */'

BODY = r'''
/* Keep the existing cyan-to-lime rail style and the approved 8s / 2s stagger,
   but run the fill once on load and hold the completed gradient afterwards. */
@keyframes zsWorkflowFillOnce{
  0%{transform:scaleX(.15);opacity:.22}
  20%,40%,100%{transform:scaleX(1);opacity:.9}
}
body.zsMotionActive #projectsHome .workflowStep:before{
  animation:zsWorkflowFillOnce 8s ease-in-out 1 both!important;
}
body.zsMotionActive #projectsHome .workflowStep:nth-child(2):before{animation-delay:2s!important}
body.zsMotionActive #projectsHome .workflowStep:nth-child(3):before{animation-delay:4s!important}
body.zsMotionActive #projectsHome .workflowStep:nth-child(4):before{animation-delay:6s!important}

/* Preserve the same one-shot behaviour when Zone Sketch explicitly keeps its
   decorative motion active on iOS / reduced-motion configurations. */
body.zsMotionActive.zsMotionForce #projectsHome .workflowStep:before,
body.zsMotionActive.reduceMotion #projectsHome .workflowStep:before{
  animation-name:zsWorkflowFillOnce!important;
  animation-duration:8s!important;
  animation-timing-function:ease-in-out!important;
  animation-iteration-count:1!important;
  animation-fill-mode:both!important;
}
body.zsMotionActive.zsMotionForce #projectsHome .workflowStep:nth-child(2):before,
body.zsMotionActive.reduceMotion #projectsHome .workflowStep:nth-child(2):before{animation-delay:2s!important}
body.zsMotionActive.zsMotionForce #projectsHome .workflowStep:nth-child(3):before,
body.zsMotionActive.reduceMotion #projectsHome .workflowStep:nth-child(3):before{animation-delay:4s!important}
body.zsMotionActive.zsMotionForce #projectsHome .workflowStep:nth-child(4):before,
body.zsMotionActive.reduceMotion #projectsHome .workflowStep:nth-child(4):before{animation-delay:6s!important}
'''.strip()

BLOCK = START + '\n' + BODY + '\n' + END

if START in text:
    start = text.index(START)
    end_marker = text.find(END, start)
    if end_marker == -1:
        raise SystemExit('index.html: workflow one-shot end marker missing')
    end = end_marker + len(END)
    updated = text[:start] + BLOCK + text[end:]
else:
    if '</style>' not in text:
        raise SystemExit('index.html: closing style tag not found')
    updated = text.replace('</style>', BLOCK + '\n</style>', 1)

if updated == text:
    print('index.html: workflow one-shot fill already current')
else:
    p.write_text(updated, encoding='utf-8')
    print('index.html: workflow rails now fill once and stay complete')
