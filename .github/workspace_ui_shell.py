from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

START = '/* Workspace UI shell v1 — visual-only polish; no behaviour changes. */'
END = '/* End workspace UI shell v1. */'
CSS = r'''
/* Workspace UI shell v1 — visual-only polish; no behaviour changes. */
:root{
  --zs-shell:#07131e;
  --zs-shell-2:#0b2130;
  --zs-shell-3:#102c3d;
  --zs-shell-line:#23516a;
  --zs-shell-cyan:#00c2ff;
  --zs-shell-lime:#9bff3f;
  --zs-shell-amber:#ffb84d;
  --zs-shell-text:#e7f5ff;
  --zs-shell-muted:#9db8c8;
  --zs-panel:#f8fbfd;
  --zs-panel-line:#c9d9e3;
  --zs-soft-shadow:0 8px 24px rgba(16,38,61,.075);
}

/* PASS 2: strengthen visual hierarchy only. No controls, IDs or behaviours change. */

/* PLAN / SURVEY — same DOM and handlers, more coherent field-workspace chrome. */
.app>.top{
  position:relative;
  background:linear-gradient(135deg,rgba(7,19,30,.985),rgba(11,33,48,.985));
  border-bottom:1px solid rgba(0,194,255,.28);
  box-shadow:0 9px 28px rgba(2,10,16,.18);
}
.app>.top:after{
  content:'';position:absolute;left:0;right:0;bottom:-1px;height:1px;pointer-events:none;
  background:linear-gradient(90deg,transparent,rgba(0,194,255,.55),rgba(155,255,63,.35),transparent);
  opacity:.52;
}
.app>.top .brand{color:var(--zs-shell-text);letter-spacing:.035em}
.app>.top .brand small{color:#8fb8ce;letter-spacing:.085em}
.app>.top input,
.app>.top select,
.app>.top button{
  border:1px solid #2b5369;
  background:linear-gradient(145deg,#102b3d,#0a1e2d);
  color:#dff3ff;
  box-shadow:inset 0 1px rgba(255,255,255,.035);
}
.app>.top input:focus,
.app>.top select:focus{border-color:#49b8dc;box-shadow:0 0 0 2px rgba(0,194,255,.09)}
.app>.top button.active,
.app>.top button[aria-pressed='true']{
  border-color:#43bfe9;
  background:linear-gradient(145deg,#12384d,#0d2637);
  box-shadow:inset 0 -2px rgba(155,255,63,.65),inset 0 0 0 1px rgba(0,194,255,.12),0 0 16px rgba(0,194,255,.08);
}
.app>.top #topCollapseBtn{border-color:#35677f;min-width:46px}
.app>.top.collapsed #topCollapseBtn{
  border-color:#3a7894;background:linear-gradient(145deg,#12384d,#0c2636);box-shadow:0 0 16px rgba(0,194,255,.07)
}
.app .saveIndicator{
  color:#84dca5;background:rgba(40,120,78,.12);border:1px solid rgba(102,211,143,.25);
  padding:5px 8px;border-radius:999px;font-weight:750;letter-spacing:.025em
}

/* Thin utility rows should read as one tidy instrument strip, not another toolbar. */
.app>.backgroundBar,
.app>.selectionBar{
  background:linear-gradient(90deg,#f7fafc,#eef5f8);
  border-color:#c5d7e1;
  box-shadow:0 3px 10px rgba(16,38,61,.045);
}
.app>.backgroundBar label{color:#486577;font-weight:720}
.app>.backgroundBar button,
.app>.selectionBar button{
  border:1px solid #c9d9e3;
  border-radius:8px;
  background:#fbfdfe;
  color:#314c5f;
  box-shadow:inset 0 1px rgba(255,255,255,.8);
}
.app>.backgroundBar button.active,
.app>.selectionBar button.active{border-color:#6aaec6;background:#eef9fc;color:#174a60}
.app>.selectionBar{box-shadow:inset 3px 0 #00c2ff,0 3px 10px rgba(16,38,61,.04)}
.app>.selectionBar strong{color:#164d67;letter-spacing:.015em}
.app>.selectionBar .primary{background:#123f58;color:#fff;border-color:#1c6889}

/* Canvas itself remains bright and neutral so zone/device colours stay meaningful. */
.app .workspace{background:#dce5eb}
.app .side{
  background:linear-gradient(180deg,#fbfdfe,#f3f7f9);
  border-color:#c5d5df;
  box-shadow:5px 0 20px rgba(16,38,61,.04);
}
.app .sideHead{
  border-bottom:1px solid #dde7ec;padding-bottom:7px;margin-bottom:8px
}
.app .side h3{color:#526f81;letter-spacing:.12em;margin-top:6px}
.app .sideHead button{
  border:1px solid #d1dfe6;background:#f5f9fb;color:#34596c;border-radius:7px
}
.app .zone{
  position:relative;
  border-color:#cfdae2;
  border-radius:4px 11px 4px 11px;
  background:#fff;
  box-shadow:0 3px 10px rgba(16,38,61,.035);
  transition:border-color .14s ease,box-shadow .14s ease,background .14s ease;
}
.app .zone:before{
  content:'';position:absolute;left:0;top:8px;bottom:8px;width:2px;border-radius:2px;background:#d9e5ea
}
.app .zone.active{
  border-color:#39a9d0;
  background:linear-gradient(130deg,#ecf9fd,#f8fcff);
  box-shadow:inset 3px 0 #00c2ff,0 4px 14px rgba(0,194,255,.06);
}
.app .zone.active:before{background:#9bff3f}
.app .zone .swatch{box-shadow:0 0 0 2px #fff,0 0 0 3px rgba(49,81,99,.14)}
.app .zone b{color:#203c4d}
.app .zone small{color:#718895}
.app .canvasWrap{background:#dce5eb;box-shadow:inset 0 0 0 1px rgba(16,38,61,.035)}
.app .hint{
  background:rgba(7,19,30,.91);
  border:1px solid rgba(0,194,255,.24);
  color:#e9f7ff;
  box-shadow:0 7px 22px rgba(2,10,16,.16);
  backdrop-filter:blur(8px);
  font-weight:700;letter-spacing:.01em;
}

/* Bottom dock: preserve every tool, just make groups and selected state easier to scan. */
.app>.tools{
  background:linear-gradient(180deg,rgba(10,29,43,.985),rgba(6,19,29,.995));
  border-top:1px solid rgba(0,194,255,.24);
  box-shadow:0 -9px 28px rgba(2,10,16,.16);
}
.app>.tools button{
  position:relative;
  border:1px solid #2a5065;
  border-radius:4px 11px 4px 11px;
  background:#102a3a;
  color:#d7edf9;
  box-shadow:inset 0 1px rgba(255,255,255,.03);
}
.app>.tools button:not(.active):not(.primary){background:linear-gradient(145deg,#102b3a,#0b2230)}
.app>.tools button.active{
  border-color:#3bc2ed;
  background:linear-gradient(135deg,#123c52,#0d2a3b);
  color:#fff;
  box-shadow:inset 0 -2px #9bff3f,0 0 14px rgba(0,194,255,.08);
}
.app>.tools button.active:after{
  content:'';position:absolute;right:7px;top:7px;width:4px;height:4px;border-radius:50%;background:#9bff3f;box-shadow:0 0 7px rgba(155,255,63,.6)
}
.app>.tools button.primary{
  background:linear-gradient(125deg,#bdff77,#9bff3f 62%,#8cf02f);color:#102008;border-color:#b9ff79;
  box-shadow:inset 0 1px rgba(255,255,255,.45),0 0 16px rgba(155,255,63,.08)
}
.app>.tools .divider{border-color:#2c4d5e;height:30px}
.app>.tools .toolSection{color:#75a6bc}

/* Popovers / inspectors keep the existing content and callbacks. */
.toolPopup{
  border:1px solid #8bb8cb;
  border-radius:5px 17px 5px 17px;
  background:linear-gradient(155deg,#fff,#f7fbfd);
  box-shadow:0 18px 48px rgba(5,22,34,.24),0 0 0 1px rgba(0,194,255,.04);
}
.toolPopup h4{
  color:#3d6378;letter-spacing:.12em;border-bottom:1px solid #e0e9ee;padding-bottom:8px;margin-bottom:10px
}
.toolPopup .menuSep{background:#dce7ec}
.toolPopup button{
  border:1px solid #d4e0e7;border-radius:8px;background:#f2f7fa;color:#29495c;
  box-shadow:inset 0 1px rgba(255,255,255,.78)
}
.toolPopup button.active,.toolPopup .toggleItem.active{
  background:linear-gradient(145deg,#12394d,#0f2d3e);color:#fff;border-color:#2e7894;
  box-shadow:inset 0 -2px rgba(155,255,63,.55)
}
.toolPopup .menuHint{color:#6e8491;background:#f3f8fa;border-radius:7px}
.toolPopup .countGrid{background:#f5f9fb;border:1px solid #dce7ec;border-radius:8px}
.propertyReadout{border:1px solid #d8e4e9;background:#f5f9fb;color:#4d6776}
.symbolGrid{gap:8px}
.symbolGrid button{
  min-height:48px;background:#f8fbfd;border-color:#d5e1e7;border-radius:4px 10px 4px 10px
}
.symbolGrid button:active{background:#eaf6fa}
.symbolGrid canvas{
  border-radius:7px;background:#fff;box-shadow:0 0 0 1px #dce7ec,0 3px 8px rgba(16,38,61,.05)
}

/* Modal treatment matches the shell without making forms dark or harder to read. */
.modal{backdrop-filter:blur(3px)}
.box{
  border:1px solid #bad0dc;border-radius:5px 18px 5px 18px;
  box-shadow:0 22px 60px rgba(8,28,42,.28);background:linear-gradient(155deg,#fff,#f8fbfd)
}
.box h2{color:#173b50;letter-spacing:-.015em}
.box label{color:#456172}
.box input,.box select{border-color:#c6d7df;background:#fff}
.box input:focus,.box select:focus{outline:2px solid rgba(0,194,255,.28);outline-offset:1px;border-color:#58abc7}

/* CIRCUIT BUILDER — visual shell only; route engine and game logic untouched. */
#circuitBuilder{background:#e9eff4}
#circuitBuilder .cbTop{
  position:relative;
  background:linear-gradient(135deg,#07131e,#0b2637 72%,#0f3344);
  border-bottom:1px solid rgba(0,194,255,.26);
  box-shadow:0 9px 28px rgba(2,10,16,.18);
}
#circuitBuilder .cbTop:after{
  content:'';position:absolute;left:0;right:0;bottom:-1px;height:1px;pointer-events:none;
  background:linear-gradient(90deg,transparent,rgba(0,194,255,.58),rgba(255,184,77,.34),transparent);opacity:.55
}
#circuitBuilder .cbTop strong{color:#f1fbff;letter-spacing:.11em}
#circuitBuilder .cbTop small{color:#8eb4c8}
#circuitBuilder .cbTop button{
  border-color:#2b5369;background:#102b3d;color:#dff3ff;border-radius:4px 10px 4px 10px;
  box-shadow:inset 0 1px rgba(255,255,255,.035)
}
#circuitBuilder .cbTop button:active{background:#14384b}
#circuitBuilder .cbFloorSwitch{border-color:#2c5870;background:#0c2130;color:#9fc4d6}
#circuitBuilder .cbFloorSwitch select{border:1px solid #bed1dc;box-shadow:inset 0 1px rgba(255,255,255,.85)}
#circuitBuilder .cbShell{background:#e9eff4}
#circuitBuilder .cbSide{
  background:linear-gradient(180deg,#fbfdfe,#f4f8fa);
  border-color:#c8d8e1;
  box-shadow:5px 0 22px rgba(16,38,61,.045);
}
#circuitBuilder .cbLandingHero{
  background:linear-gradient(135deg,#0d2d42,#124a65);
  border:1px solid #266b89;
  box-shadow:0 12px 30px rgba(16,38,61,.12);
}
#circuitBuilder .cbLandingHero .eyebrow{color:#83dcf7}
#circuitBuilder .cbLandingHero h1{letter-spacing:-.025em}
#circuitBuilder .cbModePanel,
#circuitBuilder .cbMainStatus{
  border:1px solid #ccdbe3;
  border-radius:5px 17px 5px 17px;
  box-shadow:var(--zs-soft-shadow);
  background:linear-gradient(155deg,#fff,#f9fbfc)
}
#circuitBuilder .cbModePanel h2{color:#193d52;letter-spacing:-.012em}
#circuitBuilder .cbZoneButton,
#circuitBuilder .cbCircuitRow{
  border-radius:4px 11px 4px 11px;border-color:#d4e0e6;
  box-shadow:0 3px 10px rgba(16,38,61,.035)
}
#circuitBuilder .cbZoneButton.active{
  box-shadow:inset 3px 0 var(--cb-color,#00c2ff),0 4px 14px rgba(16,38,61,.06)!important
}
#circuitBuilder .cbCircuitRow.done{border-color:#b8d9c4;box-shadow:inset 3px 0 #39a86e,0 3px 10px rgba(16,38,61,.035)}
#circuitBuilder .cbBoardWrap{
  border-color:#8ebfd2;
  border-radius:5px 18px 5px 18px;
  box-shadow:0 14px 38px rgba(16,38,61,.10),inset 0 0 0 1px rgba(0,194,255,.035);
}
#circuitBuilder .cbBoardHint{
  border:1px solid rgba(0,194,255,.18);background:rgba(7,19,30,.88);color:#e8f7ff;
  box-shadow:0 7px 22px rgba(2,10,16,.14);backdrop-filter:blur(7px)
}
#circuitBuilder .cbGameHeader{gap:8px}
#circuitBuilder .cbPill{
  border-radius:4px 9px 4px 9px;border-color:#ccdce4;background:#fff;color:#365568;
  box-shadow:0 3px 10px rgba(16,38,61,.035)
}
#circuitBuilder .cbPill.zoneChallenge{box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--cb-color,#65768a) 18%,transparent),0 3px 10px rgba(16,38,61,.04)}
#circuitBuilder .cbDetectorHud{
  background:linear-gradient(135deg,rgba(7,19,30,.965),rgba(13,45,62,.955));
  border-color:rgba(0,194,255,.24);
  box-shadow:0 10px 28px rgba(2,10,16,.18);
}
#circuitBuilder .cbDetectorHud .number{color:#fff;text-shadow:0 0 16px rgba(0,194,255,.14)}
#circuitBuilder .cbHudBar{border:1px solid rgba(255,255,255,.06)}
#circuitBuilder .cbHudBar i{box-shadow:0 0 12px rgba(255,184,77,.16)}
#circuitBuilder .cbPairBadge{border:1px solid #cbdbe3;box-shadow:0 3px 10px rgba(16,38,61,.04)}
#circuitBuilder .cbPairBadge.on{box-shadow:0 0 0 3px rgba(56,189,112,.07),0 4px 14px rgba(16,38,61,.04)}
#circuitBuilder .cbActions button{border-radius:4px 10px 4px 10px;box-shadow:0 3px 10px rgba(16,38,61,.045)}
#circuitBuilder .cbActions .complete.ready{box-shadow:0 0 0 3px rgba(37,134,85,.08),0 5px 16px rgba(16,38,61,.06)}
#circuitBuilder .cbEditBar{
  border:1px solid #c7d9e3;
  border-radius:4px 13px 4px 13px;
  box-shadow:0 6px 20px rgba(16,38,61,.05);
  background:linear-gradient(155deg,#fff,#f8fbfd)
}
#circuitBuilder .cbZoomDock{
  border:1px solid #cbdbe3;box-shadow:0 9px 25px rgba(16,38,61,.10);background:rgba(255,255,255,.96)
}
#circuitBuilder .cbAsFitSummary{
  border-radius:4px 11px 4px 11px;box-shadow:0 4px 14px rgba(27,104,66,.055)
}
#circuitBuilder .cbAsFitWrap{border:1px solid #cadbe3;border-radius:5px 17px 5px 17px}

/* Touch layouts: no behavioural rearrangement; only density and touch polish. */
@media(max-width:720px){
  .app>.top{box-shadow:0 7px 20px rgba(2,10,16,.14)}
  .app>.top button{min-height:40px}
  .app>.tools{gap:6px;padding-top:7px}
  .app>.tools button{min-height:44px;padding-left:12px;padding-right:12px}
  .app .sideHead{margin-bottom:5px;padding-bottom:4px}
  .toolPopup{border-radius:4px 15px 4px 15px}
  .toolPopup button{min-height:44px}
  .symbolGrid button{min-height:50px}
  #circuitBuilder .cbTop{box-shadow:0 7px 20px rgba(2,10,16,.14)}
  #circuitBuilder .cbTop button{min-height:40px}
  #circuitBuilder .cbModePanel{border-radius:4px 14px 4px 14px}
  #circuitBuilder .cbActions button{min-height:44px}
}
/* End workspace UI shell v1. */
'''

if START in text and END in text:
    start = text.index(START)
    end = text.index(END, start) + len(END)
    current = text[start:end]
    replacement = CSS.strip()
    if current.strip() == replacement:
        print('index.html: workspace UI shell already current')
    else:
        text = text[:start] + replacement + text[end:]
        p.write_text(text, encoding='utf-8')
        print('index.html: workspace UI shell refreshed')
elif START not in text and END not in text:
    if '</style>' not in text:
        raise SystemExit('index.html: closing style tag not found')
    text = text.replace('</style>', '\n' + CSS.strip() + '\n</style>', 1)
    p.write_text(text, encoding='utf-8')
    print('index.html: workspace UI shell installed')
else:
    raise SystemExit('index.html: partial workspace UI shell marker found')
