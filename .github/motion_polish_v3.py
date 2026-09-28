from pathlib import Path

CSS = r'''

/* Motion polish v3 — quiet ambient movement, never the drawing workspace. */
@keyframes zsEdgeRun{0%,12%{transform:translateX(-130%);opacity:0}20%{opacity:.9}68%{opacity:.55}84%,100%{transform:translateX(560%);opacity:0}}
@keyframes zsLogoGlow{0%,100%{filter:drop-shadow(0 0 12px rgba(0,194,255,.12))}50%{filter:drop-shadow(0 0 22px rgba(0,194,255,.28)) drop-shadow(0 0 9px rgba(155,255,63,.10))}}
@keyframes zsLiveHalo{0%,100%{box-shadow:0 0 0 rgba(155,255,63,0),inset 0 0 0 rgba(0,194,255,0)}50%{box-shadow:0 0 18px rgba(155,255,63,.08),inset 0 0 18px rgba(0,194,255,.035)}}
@keyframes zsStepSignal{0%,12%,100%{border-color:#214558;box-shadow:0 0 0 rgba(0,194,255,0)}22%,38%{border-color:#2e7894;box-shadow:inset 0 0 0 1px rgba(0,194,255,.06),0 0 16px rgba(0,194,255,.055)}}
@keyframes zsCardScan{0%,64%{left:-30%;opacity:0}70%{opacity:.28}88%{left:120%;opacity:0}100%{left:120%;opacity:0}}
@keyframes zsSignalRail{0%{left:0;opacity:.5}45%{opacity:1}100%{left:calc(100% - 34px);opacity:.42}}
@keyframes zsPanelTrace{0%{left:0;opacity:.42}35%{opacity:.9}100%{left:calc(100% - 60px);opacity:.28}}
@keyframes zsGoodPulse{0%,100%{text-shadow:0 0 0 rgba(155,255,63,0)}50%{text-shadow:0 0 10px rgba(155,255,63,.22)}}
@keyframes zsSoftIn{from{opacity:.7;transform:translateY(7px)}to{opacity:1;transform:none}}

#projectsHome .homeProductHero:before,
.brandPortal .approvedHeroBrand:before{content:'';position:absolute;left:0;top:0;width:24%;height:1px;background:linear-gradient(90deg,transparent,#73deff,#c7ff96,transparent);box-shadow:0 0 12px rgba(0,194,255,.22);transform:translateX(-130%);opacity:0;pointer-events:none;z-index:4}
#projectsHome .projectCard:after{content:'';position:absolute;top:-25%;bottom:-25%;left:-30%;width:12%;background:linear-gradient(90deg,transparent,rgba(142,231,255,.05),rgba(255,255,255,.08),rgba(155,255,63,.035),transparent);transform:skewX(-14deg);opacity:0;pointer-events:none}
.brandPortal .signalCard:after{right:auto}
.brandPortal .panel:before{right:auto}

body.zsMotionActive #projectsHome .homeProductHero:before,
body.zsMotionActive.brandPortal .approvedHeroBrand:before{animation:zsEdgeRun 10.2s ease-in-out infinite!important}
body.zsMotionActive #projectsHome .homeBrandMark,
body.zsMotionActive.brandPortal .approvedHeroBrand>img{animation:zsLogoGlow 7s ease-in-out infinite!important}
body.zsMotionActive #projectsHome .homeHeroBadge,
body.zsMotionActive.brandPortal .statusPill.live{animation:zsLiveHalo 5.5s ease-in-out infinite!important}

body.zsMotionActive #projectsHome .workflowStep{animation:zsStepSignal 9.6s ease-in-out infinite!important}
body.zsMotionActive #projectsHome .workflowStep:nth-child(2){animation-delay:2.4s!important}
body.zsMotionActive #projectsHome .workflowStep:nth-child(3){animation-delay:4.8s!important}
body.zsMotionActive #projectsHome .workflowStep:nth-child(4){animation-delay:7.2s!important}

body.zsMotionActive #projectsHome .projectCard:after{animation:zsCardScan 14.4s ease-in-out infinite!important}
body.zsMotionActive #projectsHome .projectCard:nth-child(2):after{animation-delay:1.7s!important}
body.zsMotionActive #projectsHome .projectCard:nth-child(3):after{animation-delay:3.4s!important}
body.zsMotionActive #projectsHome .projectCard:nth-child(4):after{animation-delay:5s!important}
body.zsMotionActive #projectsHome .projectCard:nth-child(5):after{animation-delay:6.7s!important}
body.zsMotionActive #projectsHome .projectCard:nth-child(6):after{animation-delay:8.4s!important}

body.zsMotionActive.brandPortal .signalCard:after{animation:zsSignalRail 8.4s ease-in-out infinite alternate!important}
body.zsMotionActive.brandPortal .signalCard:nth-child(2):after{animation-delay:1s!important}
body.zsMotionActive.brandPortal .signalCard:nth-child(3):after{animation-delay:1.9s!important}
body.zsMotionActive.brandPortal .signalCard:nth-child(4):after{animation-delay:2.9s!important}
body.zsMotionActive.brandPortal .signalCard:nth-child(5):after{animation-delay:3.8s!important}
body.zsMotionActive.brandPortal .signalCard:nth-child(6):after{animation-delay:4.8s!important}
body.zsMotionActive.brandPortal main>.panel:before{animation:zsPanelTrace 15.6s ease-in-out infinite alternate!important}
body.zsMotionActive.brandPortal main>.panel:nth-child(2):before{animation-delay:1.4s!important}
body.zsMotionActive.brandPortal main>.panel:nth-child(3):before{animation-delay:2.9s!important}
body.zsMotionActive.brandPortal main>.panel:nth-child(4):before{animation-delay:4.3s!important}
body.zsMotionActive.brandPortal main>.panel:nth-child(5):before{animation-delay:5.8s!important}
body.zsMotionActive.brandPortal .nodeRow .good{animation:zsGoodPulse 4.8s ease-in-out infinite!important}

/* One restrained reveal when motion is enabled or the page first opens with motion active. */
body.zsMotionActive #projectsHome .homeProductHero,
body.zsMotionActive.brandPortal .heroGrid{animation:zsSoftIn .55s cubic-bezier(.2,.7,.25,1) both!important}
body.zsMotionActive #projectsHome .homeHeading{animation:zsSoftIn .5s .08s cubic-bezier(.2,.7,.25,1) both!important}
body.zsMotionActive #projectsHome .homeActions{animation:zsSoftIn .5s .14s cubic-bezier(.2,.7,.25,1) both!important}
body.zsMotionActive #projectsHome .homeSearch{animation:zsSoftIn .5s .18s cubic-bezier(.2,.7,.25,1) both!important}
body.zsMotionActive #projectsHome .projectCard{animation:zsSoftIn .5s .22s cubic-bezier(.2,.7,.25,1) both!important}
body.zsMotionActive.brandPortal main>.panel{animation:zsSoftIn .5s cubic-bezier(.2,.7,.25,1) both!important}
body.zsMotionActive.brandPortal main>.panel:nth-child(2){animation-delay:.06s!important}
body.zsMotionActive.brandPortal main>.panel:nth-child(3){animation-delay:.12s!important}
body.zsMotionActive.brandPortal main>.panel:nth-child(4){animation-delay:.18s!important}
body.zsMotionActive.brandPortal main>.panel:nth-child(5){animation-delay:.24s!important}

/* Keep movement optical rather than physical on touch devices. */
@media(max-width:720px){
 #projectsHome .projectCard:after{width:15%}
 body.zsMotionActive #projectsHome .homeBrandMark,
 body.zsMotionActive.brandPortal .approvedHeroBrand>img{animation-duration:7.8s!important}
 body.zsMotionActive.brandPortal main>.panel:before{animation-duration:18s!important}
}
'''

MARKER = '/* Motion polish v3 — quiet ambient movement, never the drawing workspace. */'

REPLACEMENTS = {
    'animation:zsEdgeRun 8.5s ease-in-out infinite!important': 'animation:zsEdgeRun 10.2s ease-in-out infinite!important',
    'animation:zsLogoGlow 5.8s ease-in-out infinite!important': 'animation:zsLogoGlow 7s ease-in-out infinite!important',
    'animation:zsLiveHalo 4.6s ease-in-out infinite!important': 'animation:zsLiveHalo 5.5s ease-in-out infinite!important',
    'animation:zsStepSignal 8s ease-in-out infinite!important': 'animation:zsStepSignal 9.6s ease-in-out infinite!important',
    '.workflowStep:nth-child(2){animation-delay:2s!important}': '.workflowStep:nth-child(2){animation-delay:2.4s!important}',
    '.workflowStep:nth-child(3){animation-delay:4s!important}': '.workflowStep:nth-child(3){animation-delay:4.8s!important}',
    '.workflowStep:nth-child(4){animation-delay:6s!important}': '.workflowStep:nth-child(4){animation-delay:7.2s!important}',
    'animation:zsCardScan 12s ease-in-out infinite!important': 'animation:zsCardScan 14.4s ease-in-out infinite!important',
    '.projectCard:nth-child(2):after{animation-delay:1.4s!important}': '.projectCard:nth-child(2):after{animation-delay:1.7s!important}',
    '.projectCard:nth-child(3):after{animation-delay:2.8s!important}': '.projectCard:nth-child(3):after{animation-delay:3.4s!important}',
    '.projectCard:nth-child(4):after{animation-delay:4.2s!important}': '.projectCard:nth-child(4):after{animation-delay:5s!important}',
    '.projectCard:nth-child(5):after{animation-delay:5.6s!important}': '.projectCard:nth-child(5):after{animation-delay:6.7s!important}',
    '.projectCard:nth-child(6):after{animation-delay:7s!important}': '.projectCard:nth-child(6):after{animation-delay:8.4s!important}',
    'animation:zsSignalRail 7s ease-in-out infinite alternate!important': 'animation:zsSignalRail 8.4s ease-in-out infinite alternate!important',
    '.signalCard:nth-child(2):after{animation-delay:.8s!important}': '.signalCard:nth-child(2):after{animation-delay:1s!important}',
    '.signalCard:nth-child(3):after{animation-delay:1.6s!important}': '.signalCard:nth-child(3):after{animation-delay:1.9s!important}',
    '.signalCard:nth-child(4):after{animation-delay:2.4s!important}': '.signalCard:nth-child(4):after{animation-delay:2.9s!important}',
    '.signalCard:nth-child(5):after{animation-delay:3.2s!important}': '.signalCard:nth-child(5):after{animation-delay:3.8s!important}',
    '.signalCard:nth-child(6):after{animation-delay:4s!important}': '.signalCard:nth-child(6):after{animation-delay:4.8s!important}',
    'animation:zsPanelTrace 13s ease-in-out infinite alternate!important': 'animation:zsPanelTrace 15.6s ease-in-out infinite alternate!important',
    'main>.panel:nth-child(2):before{animation-delay:1.2s!important}': 'main>.panel:nth-child(2):before{animation-delay:1.4s!important}',
    'main>.panel:nth-child(3):before{animation-delay:2.4s!important}': 'main>.panel:nth-child(3):before{animation-delay:2.9s!important}',
    'main>.panel:nth-child(4):before{animation-delay:3.6s!important}': 'main>.panel:nth-child(4):before{animation-delay:4.3s!important}',
    'main>.panel:nth-child(5):before{animation-delay:4.8s!important}': 'main>.panel:nth-child(5):before{animation-delay:5.8s!important}',
    'animation:zsGoodPulse 4s ease-in-out infinite!important': 'animation:zsGoodPulse 4.8s ease-in-out infinite!important',
    'animation-duration:6.5s!important': 'animation-duration:7.8s!important',
    'animation-duration:15s!important': 'animation-duration:18s!important',
}

for name in ('index.html', 'beta.html'):
    p = Path(name)
    text = p.read_text(encoding='utf-8')
    if MARKER in text:
        updated = text
        for old, new in REPLACEMENTS.items():
            updated = updated.replace(old, new)
        if updated != text:
            p.write_text(updated, encoding='utf-8')
            print(f'{name}: ambient motion slowed')
        else:
            print(f'{name}: motion timing already current')
        continue
    if '</style>' not in text:
        raise SystemExit(f'{name}: closing style tag not found')
    p.write_text(text.replace('</style>', CSS + '\n</style>', 1), encoding='utf-8')
    print(f'{name}: motion polish added')
