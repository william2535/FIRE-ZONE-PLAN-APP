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
  --zs-shell-text:#e7f5ff;
  --zs-shell-muted:#9db8c8;
}

/* PLAN / SURVEY — same controls and handlers, cleaner field-workspace shell. */
.app>.top{
  background:linear-gradient(135deg,rgba(7,19,30,.98),rgba(11,33,48,.98));
  border-bottom:1px solid rgba(0,194,255,.28);
  box-shadow:0 9px 28px rgba(2,10,16,.18);
}
.app>.top .brand{color:var(--zs-shell-text);letter-spacing:.035em}
.app>.top .brand small{color:#8fb8ce}
.app>.top input,
.app>.top select,
.app>.top button{
  border:1px solid #2b5369;
  background:linear-gradient(145deg,#102b3d,#0a1e2d);
  color:#dff3ff;
  box-shadow:inset 0 1px rgba(255,255,255,.035);
}
.app>.top button.active,
.app>.top button[aria-pressed='true']{
  border-color:#43bfe9;
  background:linear-gradient(145deg,#12384d,#0d2637);
  box-shadow:inset 0 0 0 1px rgba(0,194,255,.16),0 0 16px rgba(0,194,255,.08);
}
.app>.top #topCollapseBtn{border-color:#35677f}

.app>.backgroundBar,
.app>.selectionBar{
  background:linear-gradient(90deg,#f5f9fc,#edf4f8);
  border-color:#c5d7e1;
  box-shadow:0 3px 10px rgba(16,38,61,.045);
}
.app>.backgroundBar button,
.app>.selectionBar button{
  border:1px solid #c9d9e3;
  border-radius:9px;
  background:#f8fbfd;
  color:#314c5f;
}
.app>.selectionBar .primary{background:#123f58;color:#fff;border-color:#1c6889}

.app .workspace{background:#dce5eb}
.app .side{
  background:linear-gradient(180deg,#fbfdfe,#f3f7f9);
  border-color:#c5d5df;
  box-shadow:5px 0 20px rgba(16,38,61,.04);
}
.app .side h3{color:#526f81;letter-spacing:.12em}
.app .zone{
  border-color:#cfdae2;
  border-radius:4px 11px 4px 11px;
  background:#fff;
  box-shadow:0 3px 10px rgba(16,38,61,.035);
}
.app .zone.active{
  border-color:#39a9d0;
  background:linear-gradient(130deg,#ecf9fd,#f8fcff);
  box-shadow:inset 3px 0 #00c2ff,0 4px 14px rgba(0,194,255,.06);
}
.app .canvasWrap{background:#dce5eb;box-shadow:inset 0 0 0 1px rgba(16,38,61,.035)}
.app .hint{
  background:rgba(7,19,30,.91);
  border:1px solid rgba(0,194,255,.24);
  color:#e9f7ff;
  box-shadow:0 7px 22px rgba(2,10,16,.16);
  backdrop-filter:blur(8px);
}

.app>.tools{
  background:linear-gradient(180deg,rgba(10,29,43,.98),rgba(6,19,29,.99));
  border-top:1px solid rgba(0,194,255,.24);
  box-shadow:0 -9px 28px rgba(2,10,16,.16);
}
.app>.tools button{
  border:1px solid #2a5065;
  border-radius:4px 11px 4px 11px;
  background:#102a3a;
  color:#d7edf9;
  box-shadow:inset 0 1px rgba(255,255,255,.03);
}
.app>.tools button.active{
  border-color:#3bc2ed;
  background:linear-gradient(135deg,#123c52,#0d2a3b);
  color:#fff;
  box-shadow:inset 0 -2px #9bff3f,0 0 14px rgba(0,194,255,.08);
}
.app>.tools button.primary{background:linear-gradient(125deg,#bdff77,#9bff3f 62%,#8cf02f);color:#102008;border-color:#b9ff79}
.app>.tools .divider{border-color:#2c4d5e}

.toolPopup{
  border:1px solid #8bb8cb;
  border-radius:5px 17px 5px 17px;
  box-shadow:0 18px 48px rgba(5,22,34,.24),0 0 0 1px rgba(0,194,255,.04);
}
.toolPopup h4{color:#3d6378;letter-spacing:.12em}
.toolPopup button{border:1px solid #d4e0e7;border-radius:8px;background:#f2f7fa}
.toolPopup button.active,.toolPopup .toggleItem.active{background:#102f42;color:#fff;border-color:#2e7894}

/* CIRCUIT BUILDER — retain every existing control and route behaviour, restyle shell only. */
#circuitBuilder{background:#e9eff4}
#circuitBuilder .cbTop{
  background:linear-gradient(135deg,#07131e,#0b2637 72%,#0f3344);
  border-bottom:1px solid rgba(0,194,255,.26);
  box-shadow:0 9px 28px rgba(2,10,16,.18);
}
#circuitBuilder .cbTop strong{color:#f1fbff;letter-spacing:.11em}
#circuitBuilder .cbTop small{color:#8eb4c8}
#circuitBuilder .cbTop button{
  border-color:#2b5369;
  background:#102b3d;
  color:#dff3ff;
  border-radius:4px 10px 4px 10px;
}
#circuitBuilder .cbFloorSwitch{border-color:#2c5870;background:#0c2130;color:#9fc4d6}
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
#circuitBuilder .cbModePanel,
#circuitBuilder .cbMainStatus{
  border:1px solid #ccdbe3;
  border-radius:5px 17px 5px 17px;
  box-shadow:0 8px 24px rgba(16,38,61,.055);
}
#circuitBuilder .cbZoneButton,
#circuitBuilder .cbCircuitRow{border-radius:4px 11px 4px 11px}
#circuitBuilder .cbBoardWrap{
  border-color:#8ebfd2;
  border-radius:5px 18px 5px 18px;
  box-shadow:0 14px 38px rgba(16,38,61,.10),inset 0 0 0 1px rgba(0,194,255,.035);
}
#circuitBuilder .cbDetectorHud{
  background:linear-gradient(135deg,rgba(7,19,30,.96),rgba(13,45,62,.95));
  border-color:rgba(0,194,255,.24);
  box-shadow:0 10px 28px rgba(2,10,16,.18);
}
#circuitBuilder .cbActions button{border-radius:4px 10px 4px 10px}
#circuitBuilder .cbPill{border-radius:4px 9px 4px 9px}
#circuitBuilder .cbEditBar{
  border:1px solid #c7d9e3;
  border-radius:4px 13px 4px 13px;
  box-shadow:0 6px 20px rgba(16,38,61,.05);
}

/* Tablet/phone: same controls, simply denser and easier to read. */
@media(max-width:720px){
  .app>.top{box-shadow:0 7px 20px rgba(2,10,16,.14)}
  .app>.tools{gap:6px;padding-top:7px}
  .app>.tools button{min-height:44px}
  .toolPopup{border-radius:4px 15px 4px 15px}
  #circuitBuilder .cbTop{box-shadow:0 7px 20px rgba(2,10,16,.14)}
  #circuitBuilder .cbModePanel{border-radius:4px 14px 4px 14px}
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
