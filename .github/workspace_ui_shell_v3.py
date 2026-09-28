from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

START = '/* Workspace UI shell v3 — tech-grid aesthetic only; no behaviour changes. */'
END = '/* End workspace UI shell v3. */'
CSS = r'''
/* Workspace UI shell v3 — tech-grid aesthetic only; no behaviour changes. */
:root{
  --zs-grid-dark:rgba(74,175,218,.042);
  --zs-grid-dark-major:rgba(123,218,246,.024);
  --zs-grid-light:rgba(25,92,122,.035);
}

/* PLAN / SURVEY chrome: use the calmer, larger grid language from the home / Circuit Builder aesthetic.
   Keep it out of the actual drawing surface so the functional plan grid remains visually separate. */
.app>.top{
  background-color:#07131e;
  background-image:
    linear-gradient(var(--zs-grid-dark) 1px,transparent 1px),
    linear-gradient(90deg,var(--zs-grid-dark) 1px,transparent 1px),
    linear-gradient(var(--zs-grid-dark-major) 1px,transparent 1px),
    linear-gradient(90deg,var(--zs-grid-dark-major) 1px,transparent 1px),
    linear-gradient(135deg,rgba(7,19,30,.985),rgba(11,33,48,.985));
  background-size:16px 16px,16px 16px,64px 64px,64px 64px,100% 100%;
  background-position:0 0;
  box-shadow:0 9px 28px rgba(2,10,16,.18),inset 0 -1px rgba(111,216,247,.04);
}
.app>.tools{
  background-color:#06131d;
  background-image:
    linear-gradient(rgba(74,175,218,.028) 1px,transparent 1px),
    linear-gradient(90deg,rgba(74,175,218,.028) 1px,transparent 1px),
    linear-gradient(180deg,rgba(10,29,43,.985),rgba(6,19,29,.995));
  background-size:16px 16px,16px 16px,100% 100%;
  background-position:0 0;
}

/* Keep Zone Plan's light side panel clean. A second pale grid beside the real drawing grid looked too busy. */
.app .side{
  background-image:linear-gradient(180deg,rgba(251,253,254,.99),rgba(244,248,250,.99));
  background-size:100% 100%;
}

/* Circuit Builder was already visually right, so leave its established grid treatment untouched. */
#circuitBuilder .cbSide{
  background-image:
    linear-gradient(var(--zs-grid-light) 1px,transparent 1px),
    linear-gradient(90deg,var(--zs-grid-light) 1px,transparent 1px),
    linear-gradient(180deg,rgba(251,253,254,.985),rgba(244,248,250,.985));
  background-size:24px 24px,24px 24px,100% 100%;
}

/* Small technical labels: same content, simply a cleaner instrument-panel voice. */
.app>.top .brand small,
.app .side h3,
.toolPopup h4,
#circuitBuilder .cbTop small,
#circuitBuilder .cbLandingHero .eyebrow{
  font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,'Liberation Mono',monospace;
  text-transform:uppercase;
  letter-spacing:.11em;
}

/* Circuit Builder uses the same grid language, with a slightly warmer circuit accent. */
#circuitBuilder .cbTop{
  background-color:#07131e;
  background-image:
    linear-gradient(rgba(74,175,218,.05) 1px,transparent 1px),
    linear-gradient(90deg,rgba(74,175,218,.05) 1px,transparent 1px),
    linear-gradient(rgba(255,184,77,.02) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,184,77,.02) 1px,transparent 1px),
    linear-gradient(135deg,#07131e,#0b2637 72%,#0f3344);
  background-size:8px 8px,8px 8px,32px 32px,32px 32px,100% 100%;
}
#circuitBuilder .cbLandingHero{
  background-color:#0d2d42;
  background-image:
    linear-gradient(rgba(95,209,240,.055) 1px,transparent 1px),
    linear-gradient(90deg,rgba(95,209,240,.055) 1px,transparent 1px),
    linear-gradient(135deg,#0d2d42,#124a65);
  background-size:16px 16px,16px 16px,100% 100%;
}

/* Bring the approved transparent Home mark's original gloss sweep back reliably.
   No geometry, colour or click behaviour is changed. */
body:not(.zsMotionPaused) .top .zsHeaderHomeShine:before{
  animation:zsHeaderHomeShine 9.6s ease-in-out infinite!important;
  will-change:transform,opacity;
}
body.zsMotionPaused .top .zsHeaderHomeShine:before{animation-play-state:paused!important}

/* Tiny depth cues only: no button sizing, layout or interaction changes. */
.app>.top,
.app>.tools,
#circuitBuilder .cbTop{background-attachment:local}
.toolPopup,.box,#circuitBuilder .cbModePanel,#circuitBuilder .cbMainStatus{
  box-shadow:0 18px 46px rgba(5,22,34,.16),inset 0 1px rgba(255,255,255,.72);
}

@media(max-width:720px){
  .app>.top{background-size:16px 16px,16px 16px,64px 64px,64px 64px,100% 100%}
  #circuitBuilder .cbTop{background-size:8px 8px,8px 8px,24px 24px,24px 24px,100% 100%}
  #circuitBuilder .cbSide{background-size:20px 20px,20px 20px,100% 100%}
}
/* End workspace UI shell v3. */
'''

if START in text and END in text:
    start = text.index(START)
    end = text.index(END, start) + len(END)
    replacement = CSS.strip()
    if text[start:end].strip() == replacement:
        print('index.html: tech-grid aesthetic already current')
    else:
        text = text[:start] + replacement + text[end:]
        p.write_text(text, encoding='utf-8')
        print('index.html: tech-grid aesthetic refreshed')
elif START not in text and END not in text:
    if '</style>' not in text:
        raise SystemExit('index.html: closing style tag not found')
    text = text.replace('</style>', '\n' + CSS.strip() + '\n</style>', 1)
    p.write_text(text, encoding='utf-8')
    print('index.html: tech-grid aesthetic installed')
else:
    raise SystemExit('index.html: partial tech-grid marker found')
