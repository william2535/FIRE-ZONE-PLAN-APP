from pathlib import Path

p=Path('index.html')
t=p.read_text()

def once(old,new,label):
    global t
    if old not in t:
        if new in t:
            return
        raise SystemExit(f'v0.49 patch marker missing: {label}')
    t=t.replace(old,new,1)

# Version labels.
t=t.replace('v0.48','v0.49')

# Premium visual system. Kept as end-of-style overrides so the mature drawing logic stays untouched.
css=r'''
/* v0.49 — site-ready professional finish. */
:root{
 --zs-navy:#10263d;--zs-navy2:#173854;--zs-blue:#2e72c9;--zs-blue2:#235fa8;
 --zs-green:#238655;--zs-amber:#c98620;--zs-red:#c3433d;--zs-bg:#edf2f7;
 --zs-surface:#fff;--zs-surface2:#f7f9fc;--zs-border:#d4dfe9;--zs-text:#18283a;
 --zs-muted:#64768a;--zs-shadow:0 12px 34px #10263d14;--zs-shadow-lg:0 24px 70px #10263d24;
}
body{background:var(--zs-bg);color:var(--zs-text);-webkit-tap-highlight-color:transparent}
button{min-height:44px;border-radius:12px;transition:transform .12s ease,background .16s ease,box-shadow .16s ease,border-color .16s ease;touch-action:manipulation}
button:active:not(:disabled){transform:scale(.98)}
button.primary,.top button.primary,.tools button.primary,.projectActions .primary,.cbCard button.primary,.cbActions .primary,#empty button:not(.secondary){background:var(--zs-blue)!important;color:#fff!important;box-shadow:0 5px 16px #2867b22c}
button.primary:hover{background:var(--zs-blue2)!important}
button.danger,.danger{color:#a93832}.danger.active{background:var(--zs-red)!important;color:#fff}
.top{background:linear-gradient(135deg,var(--zs-navy),var(--zs-navy2));border-bottom:1px solid #ffffff12;box-shadow:0 6px 22px #10263d24}
.top button{border:1px solid #ffffff12;background:#ffffff12}.top button:hover{background:#ffffff1b}
.top input{background:#ffffff10;border-color:#ffffff24}.brand{letter-spacing:.025em}.brand small{color:#bcd0e3}
.backgroundBar,.selectionBar{border-color:var(--zs-border);background:#f8fafc}.selectionBar{background:#edf5ff}
.canvasWrap{background:linear-gradient(145deg,#e8edf3,#dce5ee)}
.tools,#surveyTools{box-shadow:0 -8px 25px #10263d0c;border-color:var(--zs-border)!important}
.toolPopup,.box,.projectCard,.cbCard,.cbModePanel,.cbCircuitRow{border-color:var(--zs-border)!important;box-shadow:var(--zs-shadow)}
.toolPopup{border-radius:18px;background:#fffffff8;backdrop-filter:blur(14px)}
.box{border:1px solid var(--zs-border);border-radius:20px}.modal{background:#0e223a99;backdrop-filter:blur(5px)}
.modal.open .box{animation:zsModalIn .18s ease-out}.toolPopup.open{animation:zsMenuIn .15s ease-out}
@keyframes zsModalIn{from{opacity:0;transform:translateY(8px) scale(.985)}to{opacity:1;transform:none}}
@keyframes zsMenuIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:none}}
.empty{border:1px solid var(--zs-border);box-shadow:var(--zs-shadow-lg);border-radius:22px}.empty strong{font-size:20px}.empty p{color:var(--zs-muted)}

/* Home / Projects — deliberate product first impression. */
#projectsHome{background:radial-gradient(circle at 85% 0,#dceaff 0,transparent 34%),linear-gradient(145deg,#f2f6fa,#e9eff5);padding-top:calc(22px + env(safe-area-inset-top))}
.homeInner{max-width:1100px!important}.homeProductHero{position:relative;overflow:hidden;display:grid;grid-template-columns:minmax(0,1.3fr) minmax(260px,.7fr);gap:22px;padding:26px;margin:0 0 22px;border-radius:26px;background:linear-gradient(135deg,#10263d,#174365);color:#fff;box-shadow:0 22px 60px #10263d2b;border:1px solid #ffffff18}
.homeProductHero:after{content:'';position:absolute;width:300px;height:300px;border-radius:50%;right:-95px;top:-130px;background:radial-gradient(circle,#5da2ff42,transparent 68%);pointer-events:none}.homeProductHero>*{position:relative;z-index:1}
.homeEyebrow{font-size:10px;font-weight:900;letter-spacing:.18em;color:#9fc8ef;text-transform:uppercase}.homeProductHero h1{font-size:clamp(29px,5vw,46px);line-height:1.03;margin:8px 0 11px;letter-spacing:-.03em}.homeProductHero p{max-width:650px;margin:0;color:#d6e3ef;font-size:14px;line-height:1.55}.homeHeroBadge{align-self:center;justify-self:end;width:min(100%,300px);padding:17px;border-radius:18px;background:#ffffff0d;border:1px solid #ffffff1b;backdrop-filter:blur(8px)}.homeHeroBadge strong{display:block;font-size:13px}.homeHeroBadge small{display:block;color:#bcd0df;margin-top:5px;line-height:1.4}
.workflowTrack{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:19px}.workflowStep{position:relative;padding:9px 8px;border-radius:10px;background:#ffffff0c;border:1px solid #ffffff12;font-size:10px;font-weight:800;color:#dce9f4;text-align:center}.workflowStep b{display:block;color:#7fb5ea;font-size:9px;margin-bottom:3px}.workflowStep:not(:last-child):after{content:'›';position:absolute;right:-7px;top:50%;transform:translateY(-50%);color:#7fa5c5;z-index:2;font-size:16px}
.homeHeading{padding:0 2px}.homeHeading h1{font-size:22px!important;margin-bottom:5px}.homeVersion{font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:#6b7e91}.homeIntro{font-size:13px}.homeSearch{box-shadow:0 4px 18px #10263d0b;border-color:var(--zs-border)}
.projectGrid{gap:14px}.projectCard{border-radius:19px;padding:15px;transition:transform .16s ease,box-shadow .16s ease}.projectCard:hover{transform:translateY(-2px);box-shadow:0 15px 34px #10263d18}.projectCard img{border-radius:12px;background:#f5f8fb}.projectActions button{border:1px solid #d8e2eb;background:#f1f5f8}.homeActions .primary{background:var(--zs-blue)!important}

/* Save confidence indicator. */
.saveIndicator{margin-left:auto;padding:5px 9px;border-radius:999px;border:1px solid transparent;font-weight:750;transition:.16s ease}
.saveIndicator[data-state="saving"]{color:#8a5b12;background:#fff3d9;border-color:#ebcf93}.saveIndicator[data-state="saved"]{color:#17643d;background:#eaf8f0;border-color:#b9dec8}.saveIndicator[data-state="error"]{color:#9d302c;background:#fff0ef;border-color:#e6b6b3}.saveIndicator[data-state="idle"]{color:#65778a;background:#eef3f7;border-color:#d9e2ea}

/* Survey picker grouping and touch confidence. */
.symbolCategory{margin:0 0 11px}.symbolCategory:last-of-type{margin-bottom:0}.symbolCategoryTitle{margin:0 3px 6px;font-size:9px;font-weight:900;letter-spacing:.13em;text-transform:uppercase;color:#6a7d91}.symbolCategory:not(:has(button:not([hidden]))){display:none}.symbolCategory .symbolGrid{grid-template-columns:1fr 1fr}.symbolCategory button{min-height:44px;border:1px solid #d8e2eb;background:#f2f6fa}.app.surveyMode #surveyTools button{border:1px solid #d9e3ec;border-radius:12px}.app.surveyMode #surveyDevice{background:#eaf3ff!important;color:#1d5d9e;font-weight:800}.surveyFavouriteQuick{border-radius:10px!important}

/* App settings / professional notices. */
.appSettingsBox{width:min(470px,100%)}.settingsHeader{display:flex;align-items:flex-start;gap:12px;margin-bottom:14px}.settingsMark{width:42px;height:42px;border-radius:13px;display:grid;place-items:center;background:linear-gradient(145deg,#2e72c9,#1e568f);color:#fff;font-weight:950;box-shadow:0 7px 20px #2464a82b}.settingsHeader h2{margin:1px 0 3px}.settingsHeader p{margin:0;color:var(--zs-muted);font-size:12px}.settingsList{display:grid;gap:8px}.appSettingRow{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:12px;width:100%;padding:12px 13px;border:1px solid #d9e3ec;border-radius:14px;background:#f8fafc;text-align:left}.appSettingRow strong{display:block;font-size:13px}.appSettingRow small{display:block;margin-top:3px;color:#6a7c8e;font-size:11px;font-weight:500}.settingValue{min-width:66px;padding:6px 9px;border-radius:999px;background:#e6edf4;color:#52677b;font-size:10px;font-weight:900;text-align:center}.appSettingRow.on .settingValue{background:#e7f7ee;color:#187144}.appSettingRow.static{cursor:default}.settingsFooter{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:15px;color:#697b8d;font-size:11px}.settingsFooter b{color:#34506a}
.uiNoticeBox{width:min(420px,100%);text-align:center;padding:26px 23px}.uiNoticeIcon{width:52px;height:52px;margin:0 auto 11px;border-radius:16px;display:grid;place-items:center;background:#edf4fc;color:#2768b1;font-size:24px;font-weight:900}.uiNoticeBox h2{margin:0 0 7px}.uiNoticeBox p{margin:0;color:#607286;font-size:13px;line-height:1.5}.uiNoticeBox .row{justify-content:center}.uiNoticeBox .row button{min-width:120px}
.uiToastStack{position:fixed;z-index:180;left:50%;bottom:calc(18px + env(safe-area-inset-bottom));transform:translateX(-50%);display:grid;gap:7px;width:min(430px,calc(100vw - 24px));pointer-events:none}.uiToast{display:flex;align-items:center;gap:9px;padding:11px 13px;border-radius:13px;background:#122940ed;color:#fff;box-shadow:0 12px 32px #0d213849;backdrop-filter:blur(10px);font-size:12px;font-weight:750;animation:zsToastIn .18s ease-out}.uiToast:before{content:'•';width:22px;height:22px;border-radius:50%;display:grid;place-items:center;background:#ffffff16;color:#b9d7f3}.uiToast.success:before{content:'✓';background:#2a925c;color:#fff}.uiToast.warn:before{content:'!';background:#bd8021;color:#fff}.uiToast.error:before{content:'!';background:#bb433e;color:#fff}@keyframes zsToastIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

/* Circuit Builder — more like a finished field product, still uncluttered. */
#circuitBuilder{background:radial-gradient(circle at 95% 0,#dceaff 0,transparent 30%),linear-gradient(145deg,#edf3f8,#e5edf5)}
.cbTop{background:linear-gradient(135deg,#10263d,#183f5f);box-shadow:0 8px 28px #10263d22}.cbTop strong{font-weight:900;letter-spacing:.09em}.cbTop button{border:1px solid #ffffff16;background:#ffffff10}.cbLanding{padding:4px 2px 22px}.cbLandingHero{padding:17px 18px;margin-bottom:13px;border-radius:19px;background:linear-gradient(135deg,#153651,#1f537b);color:#fff;box-shadow:0 12px 30px #10263d1c}.cbLandingHero .eyebrow{font-size:9px;font-weight:900;letter-spacing:.16em;color:#9ecaf0}.cbLandingHero h1{margin:5px 0 6px;color:#fff}.cbLandingHero p{margin:0;color:#d4e2ee;line-height:1.5;font-size:12px}.cbModeGrid{gap:13px}.cbModePanel{border-radius:19px;padding:16px;background:#fffffff7}.cbModePanel h2{font-size:18px}.cbModePanel>p{color:#66798c}.cbZoneButton{border:1px solid #d8e2eb;background:#f2f6fa;min-height:46px}.cbZoneButton.done{border-color:#abd8bc;background:#edf9f2}.cbCircuitRow{border-radius:14px;padding:10px}.cbCircuitRow.done{background:#f5fcf8}.cbCircuitRow small{color:#6b7d8f}.cbBoardWrap{border-radius:20px;border-color:#c9d8e5;box-shadow:0 12px 36px #10263d11;background:#fff}.cbGameHeader{padding:2px}.cbPill{background:#fff;border-color:#d1dde7;font-weight:800}.cbActions{padding-top:1px}.cbActions button{border-radius:11px}.cbActions .complete{background:var(--zs-red)}.cbActions .complete.ready{background:var(--zs-green)}.cbDetectorHud{background:linear-gradient(135deg,#10263df4,#173d5af2);border:1px solid #ffffff12}.cbDetectorHud .number{letter-spacing:-.02em}.cbHudBar{background:#ffffff1e}.cbHudBar i{background:linear-gradient(90deg,#f1b445,#38bd70)}.cbPairBadge{border-radius:999px;font-weight:900}.cbPairBadge.on{background:#e7f8ee;color:#187447}.cbZoomDock{border-radius:14px;box-shadow:0 9px 25px #10263d1a}.cbCelebrateCard{border-radius:26px!important}.cbCelebrateKicker{letter-spacing:.2em!important}.cbCompletionStats strong{color:#197447}.cbMilestone{border-radius:999px}.cbAsFitSummary{display:flex;align-items:center;gap:8px;padding:10px 12px;border:1px solid #b9dec8;border-radius:13px;background:#edf9f2;color:#1b6842;font-size:12px;font-weight:800}.cbAsFitSummary:before{content:'✓';width:22px;height:22px;border-radius:50%;display:grid;place-items:center;background:#258655;color:#fff;font-size:11px}.cbAsFitWrap{border-radius:19px;box-shadow:var(--zs-shadow)}

/* Motion preference. */
body.reduceMotion *,body.reduceMotion *::before,body.reduceMotion *::after{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important;scroll-behavior:auto!important}.reduceMotion .cbConfetti{display:none!important}
@media(max-width:700px){.homeProductHero{grid-template-columns:1fr;padding:20px}.homeHeroBadge{justify-self:stretch;width:100%}.workflowTrack{grid-template-columns:repeat(2,1fr)}.workflowStep:nth-child(2):after{display:none}.homeProductHero h1{font-size:32px}.homeHeading h1{font-size:20px!important}.uiToastStack{bottom:calc(10px + env(safe-area-inset-bottom))}.settingsFooter{align-items:flex-start;flex-direction:column}.cbLandingHero{padding:14px}.cbModePanel{padding:14px}}
@media(max-height:560px){.uiToastStack{bottom:6px}.homeProductHero{padding:14px}.cbLandingHero{padding:10px 13px}.cbAsFitSummary{padding:7px 9px}}
'''
once('</style>',css+'\n</style>','premium CSS')

# Home product hero while retaining all existing project IDs and behaviours.
old_home='''<section id="projectsHome" aria-label="Projects"><div class="homeInner"><div class="homeHeading"><div><div class="homeVersion">ON SITE ZONE PLANNER · v0.49</div><h1>Your plans</h1></div><button id="resumeProject" hidden>Back to drawing</button></div><p class="homeIntro">Make a new plan or carry on where you left off. The same plan feeds the zone plan, site survey and Circuit Builder.</p><div class="homeActions"><button id="homeNew" class="primary" disabled>Make a new plan</button><button id="homeImport" disabled>Import backup</button></div><input id="projectSearch" class="homeSearch" type="search" placeholder="Find a plan…" aria-label="Search plans"><p id="homeMessage" role="status">Loading saved projects…</p><div id="projectGrid" class="projectGrid"></div><p class="homeIntro">Export an editable backup to keep a separate copy or move a survey to another device.</p></div></section>'''
new_home='''<section id="projectsHome" aria-label="Projects"><div class="homeInner"><div class="homeProductHero"><div><div class="homeEyebrow">FIRE &amp; SECURITY · FIELD WORKSPACE</div><h1>Zone Sketch</h1><p>Capture the building, survey installed devices, build validated circuits and produce an As-Fit route — all from the same project.</p><div class="workflowTrack" aria-label="Project workflow"><div class="workflowStep"><b>01</b>PLAN</div><div class="workflowStep"><b>02</b>SURVEY</div><div class="workflowStep"><b>03</b>CIRCUITS</div><div class="workflowStep"><b>04</b>AS-FIT</div></div></div><div class="homeHeroBadge"><strong>Site-ready workspace</strong><small>Local autosave · touch-first controls · offline project data</small></div></div><div class="homeHeading"><div><div class="homeVersion">ZONE SKETCH · v0.49</div><h1>Recent projects</h1></div><button id="resumeProject" hidden>Back to drawing</button></div><p class="homeIntro">Start a new survey or continue exactly where you left off.</p><div class="homeActions"><button id="homeNew" class="primary" disabled>＋ New project</button><button id="homeImport" disabled>Import backup</button></div><input id="projectSearch" class="homeSearch" type="search" placeholder="Search projects…" aria-label="Search projects"><p id="homeMessage" role="status">Loading saved projects…</p><div id="projectGrid" class="projectGrid"></div><p class="homeIntro">Editable backups preserve every floor, device, photo and circuit so a project can move between devices.</p></div></section>'''
once(old_home,new_home,'home hero')

# More deliberate Circuit Builder landing.
old_cb='''<section id="cbLanding" class="cbLanding"><h1>Turn the survey into the circuit</h1><p>The room layout stays recognisable behind the devices, but the devices spread out just enough to make tracing the wiring clear and satisfying.</p><div class="cbModeGrid">'''
new_cb='''<section id="cbLanding" class="cbLanding"><div class="cbLandingHero"><div class="eyebrow">SURVEY → VALIDATED ROUTE</div><h1>Build the circuit</h1><p>Trace the real installation while keeping the building recognisable. Circuit Builder validates every selected device and keeps the route ready for the As-Fit.</p></div><div class="cbModeGrid">'''
once(old_cb,new_cb,'Circuit Builder landing hero')

# As-Fit validation strip.
old_asfit='''<section id="cbAsFit" class="cbAsFit" hidden><div class="cbGameHeader"><button id="cbAsFitBack">← Circuits</button><strong>As-Fit preview</strong><span class="cbGrow"></span><button id="cbExportAsFit" class="primary">Export As-Fit PNG</button></div><div class="cbAsFitWrap"><canvas id="cbAsFitCanvas"></canvas></div></section>'''
new_asfit='''<section id="cbAsFit" class="cbAsFit" hidden><div class="cbGameHeader"><button id="cbAsFitBack">← Circuits</button><strong>As-Fit preview</strong><span class="cbGrow"></span><button id="cbExportAsFit" class="primary">Export As-Fit PNG</button></div><div id="cbAsFitSummary" class="cbAsFitSummary">Validated from completed circuits</div><div class="cbAsFitWrap"><canvas id="cbAsFitCanvas"></canvas></div></section>'''
once(old_asfit,new_asfit,'As-Fit summary')

# Group survey symbols without changing any data-symbol hooks.
old_symbols='''<div class="symbolGrid"><button data-symbol="panel" data-symbol-scope="both">Panel</button><button data-symbol="mcp" data-symbol-scope="survey">MCP</button><button data-symbol="smoke" data-symbol-scope="survey">Smoke</button><button data-symbol="heat" data-symbol-scope="survey">Heat</button><button data-symbol="sounder" data-symbol-scope="survey">Sounder</button><button data-symbol="beacon" data-symbol-scope="survey">Beacon</button><button data-symbol="beam" data-symbol-scope="survey">Beam detector</button><button data-symbol="io" data-symbol-scope="survey">I/O unit</button><button data-symbol="repeater" data-symbol-scope="both">Repeater</button><button data-symbol="you" data-symbol-scope="plan">You are here</button></div>'''
new_symbols='''<div class="symbolCategory"><div class="symbolCategoryTitle">Detection</div><div class="symbolGrid"><button data-symbol="mcp" data-symbol-scope="survey">MCP</button><button data-symbol="smoke" data-symbol-scope="survey">Smoke</button><button data-symbol="heat" data-symbol-scope="survey">Heat</button><button data-symbol="beam" data-symbol-scope="survey">Beam detector</button></div></div><div class="symbolCategory"><div class="symbolCategoryTitle">Alarm</div><div class="symbolGrid"><button data-symbol="sounder" data-symbol-scope="survey">Sounder</button><button data-symbol="beacon" data-symbol-scope="survey">Beacon</button></div></div><div class="symbolCategory"><div class="symbolCategoryTitle">Control</div><div class="symbolGrid"><button data-symbol="panel" data-symbol-scope="both">Fire panel</button><button data-symbol="repeater" data-symbol-scope="both">Repeater</button><button data-symbol="io" data-symbol-scope="survey">I/O unit</button></div></div><div class="symbolCategory"><div class="symbolCategoryTitle">Reference</div><div class="symbolGrid"><button data-symbol="you" data-symbol-scope="plan">You are here</button></div></div>'''
once(old_symbols,new_symbols,'survey symbol categories')

# Settings entry in Project menu.
old_project='''<div id="projectMenu" class="toolPopup" aria-label="Project"><h4>Project</h4><button id="homeBtn">Home / Projects</button><div id="projectActions" class="menuRow"></div><div class="menuSep"></div><div class="menuRow"><button id="drawingDetails">Drawing details</button><button id="backupProject">Save editable backup</button><button id="restoreProject">Open backup</button></div><div class="menuHint">A backup preserves every floor, photo and editable object.</div></div>'''
new_project='''<div id="projectMenu" class="toolPopup" aria-label="Project"><h4>Project</h4><button id="homeBtn">Home / Projects</button><div id="projectActions" class="menuRow"></div><div class="menuSep"></div><div class="menuRow"><button id="drawingDetails">Drawing details</button><button id="appSettingsBtn">App settings</button><button id="backupProject">Save editable backup</button><button id="restoreProject">Open backup</button></div><div class="menuHint">Autosave is always on. A backup preserves every floor, photo and editable object.</div></div>'''
once(old_project,new_project,'project settings entry')

# App settings, notice sheet and toast surface.
anchor='''<div id="detailsModal" class="modal"><div class="box"><h2>Drawing details</h2><label>Drawing reference<input id="drawingRef" maxlength="32" placeholder="e.g. SCH-001"></label><label>Revision<input id="revision" maxlength="12" placeholder="e.g. A"></label><label>Surveyed by<input id="surveyedBy" maxlength="48"></label><label>Survey date<input id="surveyDate" type="date"></label><div class="row"><button id="detailsCancel">Cancel</button><button id="detailsSave" class="primary">Save</button></div></div></div>'''
addition=anchor+'''\n<div id="appSettingsModal" class="modal" role="dialog" aria-modal="true" aria-label="App settings"><div class="box appSettingsBox"><div class="settingsHeader"><div class="settingsMark">ZS</div><div><h2>App settings</h2><p>Field experience and accessibility</p></div></div><div class="settingsList"><button id="appSoundSetting" class="appSettingRow"><span><strong>Circuit sounds</strong><small>Rising detector bells and completion chime</small></span><span id="appSoundValue" class="settingValue">ON</span></button><button id="appHapticsSetting" class="appSettingRow"><span><strong>Haptics</strong><small>Completion vibration on supported devices</small></span><span id="appHapticsValue" class="settingValue">ON</span></button><button id="appMotionSetting" class="appSettingRow"><span><strong>Reduced motion</strong><small>Minimise celebration and interface animation</small></span><span id="appMotionValue" class="settingValue">OFF</span></button><div class="appSettingRow static"><span><strong>Autosave</strong><small>Project changes are saved locally as you work</small></span><span class="settingValue">ALWAYS ON</span></div></div><div class="settingsFooter"><span>ZONE SKETCH · <b>v0.49</b></span><button id="appSettingsClose" class="primary">Done</button></div></div></div>\n<div id="appNoticeModal" class="modal uiNoticeModal" role="dialog" aria-modal="true" aria-label="Message"><div class="box uiNoticeBox"><div class="uiNoticeIcon">i</div><h2 id="appNoticeTitle">Ready</h2><p id="appNoticeText"></p><div class="row"><button id="appNoticeClose" class="primary">OK</button></div></div></div>\n<div id="uiToastStack" class="uiToastStack" aria-live="polite" aria-atomic="true"></div>'''
once(anchor,addition,'settings and notice markup')

# UI helper layer after the core element aliases exist.
js_anchor="const SURVEY_GRID_STEPS=[2,5,10,20,40,50,100,150,200,250];"
helpers=r'''let uiHaptics=true,uiReducedMotion=false;
try{uiHaptics=localStorage.getItem('zoneSketchHaptics')!=='off';const rm=localStorage.getItem('zoneSketchReducedMotion');uiReducedMotion=rm==='on'||(rm==null&&window.matchMedia?.('(prefers-reduced-motion: reduce)').matches)}catch(e){}
function applyReducedMotion(){document.body.classList.toggle('reduceMotion',!!uiReducedMotion)}
function uiToast(text,kind='info'){const stack=$('uiToastStack');if(!stack||!text)return;const el=document.createElement('div');el.className='uiToast '+kind;el.textContent=text;stack.append(el);while(stack.children.length>3)stack.firstElementChild.remove();setTimeout(()=>{el.style.opacity='0';el.style.transform='translateY(6px)';setTimeout(()=>el.remove(),180)},2200)}
function uiNotice(title,text){$('appNoticeTitle').textContent=title;$('appNoticeText').textContent=text;$('appNoticeModal').classList.add('open')}
$('appNoticeClose').onclick=()=>$('appNoticeModal').classList.remove('open');$('appNoticeModal').onclick=e=>{if(e.target===$('appNoticeModal'))$('appNoticeModal').classList.remove('open')};
function syncAppSettings(){if(!$('appSoundSetting'))return;const sound=typeof cbSound!=='undefined'?cbSound:true;$('appSoundSetting').classList.toggle('on',sound);$('appSoundValue').textContent=sound?'ON':'OFF';$('appHapticsSetting').classList.toggle('on',uiHaptics);$('appHapticsValue').textContent=uiHaptics?'ON':'OFF';$('appMotionSetting').classList.toggle('on',uiReducedMotion);$('appMotionValue').textContent=uiReducedMotion?'ON':'OFF'}
$('appSettingsBtn').onclick=()=>{closeToolMenus();syncAppSettings();$('appSettingsModal').classList.add('open')};$('appSettingsClose').onclick=()=>$('appSettingsModal').classList.remove('open');$('appSettingsModal').onclick=e=>{if(e.target===$('appSettingsModal'))$('appSettingsModal').classList.remove('open')};
$('appSoundSetting').onclick=()=>{cbSound=!cbSound;try{localStorage.setItem('zoneSketchCircuitSound',cbSound?'on':'off')}catch(e){}if(!cbSound)cbAudioCtx?.suspend().catch(()=>{});cbSyncSound();syncAppSettings();uiToast('Circuit sounds '+(cbSound?'on':'off'),'success')};
$('appHapticsSetting').onclick=()=>{uiHaptics=!uiHaptics;try{localStorage.setItem('zoneSketchHaptics',uiHaptics?'on':'off')}catch(e){}syncAppSettings();uiToast('Haptics '+(uiHaptics?'on':'off'),'success')};
$('appMotionSetting').onclick=()=>{uiReducedMotion=!uiReducedMotion;try{localStorage.setItem('zoneSketchReducedMotion',uiReducedMotion?'on':'off')}catch(e){}applyReducedMotion();syncAppSettings();uiToast('Reduced motion '+(uiReducedMotion?'on':'off'),'success')};
applyReducedMotion();'''
once(js_anchor,js_anchor+'\n'+helpers,'UI helpers')

# Give the save state a clear professional status.
old_save="function saveStatus(text){$('status').textContent=text;$('saveIndicator').textContent=text}"
new_save="function saveStatus(text){$('status').textContent=text;const el=$('saveIndicator');el.textContent=text;el.dataset.state=/failed|unavailable/i.test(text)?'error':/Saving/i.test(text)?'saving':/Saved/i.test(text)?'saved':'idle'}"
once(old_save,new_save,'save state styling')

# Toast new surveyed devices without interrupting repetitive placement.
old_place="else if(tool==='symbol'){push();state.symbols.push({id:uid(),...inputPoint(e.clientX,e.clientY),type:symbolStamp,color:symbolColor,scale:symbolStampScale,rotation:0,scope:surveyMode?'survey':'plan',group:null});changed()}"
new_place="else if(tool==='symbol'){push();state.symbols.push({id:uid(),...inputPoint(e.clientX,e.clientY),type:symbolStamp,color:symbolColor,scale:symbolStampScale,rotation:0,scope:surveyMode?'survey':'plan',group:null});changed();if(surveyMode)uiToast((symbolNames[symbolStamp]||'Device')+' added','success')}"
once(old_place,new_place,'survey placement toast')
old_beam="changed();setHint('Beam placed · triangle points where your finger finished');setTimeout(hint,1000);return}"
new_beam="changed();if(surveyMode)uiToast('Beam detector added','success');setHint('Beam placed · triangle points where your finger finished');setTimeout(hint,1000);return}"
once(old_beam,new_beam,'beam placement toast')

# Sync settings once Circuit Builder sound state exists.
old_sound="$('cbGame').insertBefore($('cbDetectorHud'),$('cbBoardWrap'));$('cbSoundToggle').onclick=()=>{cbSound=!cbSound;try{localStorage.setItem('zoneSketchCircuitSound',cbSound?'on':'off')}catch(e){}if(!cbSound)cbAudioCtx?.suspend().catch(()=>{});cbSyncSound()};cbSyncSound();"
new_sound="$('cbGame').insertBefore($('cbDetectorHud'),$('cbBoardWrap'));$('cbSoundToggle').onclick=()=>{cbSound=!cbSound;try{localStorage.setItem('zoneSketchCircuitSound',cbSound?'on':'off')}catch(e){}if(!cbSound)cbAudioCtx?.suspend().catch(()=>{});cbSyncSound();syncAppSettings();uiToast('Circuit sounds '+(cbSound?'on':'off'),'success')};cbSyncSound();syncAppSettings();"
once(old_sound,new_sound,'sound settings sync')

# Larger invisible device hit zones; visual symbols remain small.
t=t.replace('if(d<=22)hits.push({id,t,p})','if(d<=25)hits.push({id,t,p})',1)
t=t.replace('if(d<=30&&(!best||d<best.d))best={id,d}','if(d<=34&&(!best||d<best.d))best={id,d}',1)

# Captured detector ticks and a stronger FAP return target, without increasing symbol size.
old_node="function cbDrawNode(x,s,p,r,ring,muted=false){x.save();if(ring){x.beginPath();x.arc(p.x,p.y,r+8,0,Math.PI*2);x.strokeStyle=ring;x.lineWidth=4;x.globalAlpha=.8;x.stroke()}x.globalAlpha=muted?.42:1;drawSymbol(x,p,s.type,r,s.color||'#172333',s.rotation||0);if(s.reference){x.font='700 10px system-ui';x.fillStyle='#40546a';x.textAlign='center';x.fillText(s.reference,p.x,p.y+r+15)}x.restore()}"
new_node=r'''function cbDrawNode(x,s,p,r,ring,muted=false){x.save();const seq=new Set(cbCircuit?.sequence||[]),queued=new Set(cbDrag?.targets||[]),captured=cbScreen==='game'&&s.type!=='panel'&&(seq.has(s.id)||queued.has(s.id)),allDone=cbScreen==='game'&&cbCircuit?.deviceIds?.length&&cbCircuit.deviceIds.every(id=>seq.has(id)||queued.has(id)),panelReady=s.type==='panel'&&allDone&&!cbCircuit?.complete,current=((cbDrag?.targets||[]).at(-1)||cbCircuit?.sequence?.at(-1))===s.id;if(panelReady){x.beginPath();x.arc(p.x,p.y,r+13,0,Math.PI*2);x.fillStyle='#28a66020';x.fill();x.beginPath();x.arc(p.x,p.y,r+9,0,Math.PI*2);x.strokeStyle='#28a660';x.lineWidth=3;x.globalAlpha=.9;x.stroke()}if(ring){x.beginPath();x.arc(p.x,p.y,r+8,0,Math.PI*2);x.strokeStyle=ring;x.lineWidth=current?4.5:3.5;x.globalAlpha=.82;x.stroke()}x.globalAlpha=muted?.42:1;drawSymbol(x,p,s.type,r,s.color||'#172333',s.rotation||0);if(captured){const bx=p.x+r*.82,by=p.y-r*.82,br=Math.max(5,r*.46);x.globalAlpha=1;x.beginPath();x.arc(bx,by,br,0,Math.PI*2);x.fillStyle='#238655';x.fill();x.strokeStyle='#fff';x.lineWidth=1.4;x.stroke();x.fillStyle='#fff';x.font=`900 ${Math.max(7,br*1.15)}px system-ui`;x.textAlign='center';x.textBaseline='middle';x.fillText('✓',bx,by+.4)}if(s.reference){x.globalAlpha=1;x.font='700 10px system-ui';x.fillStyle='#40546a';x.textAlign='center';x.textBaseline='alphabetic';x.fillText(s.reference,p.x,p.y+r+15)}x.restore()}'''
once(old_node,new_node,'captured detector visuals')

# Professional Circuit Builder notices instead of browser alerts for common onsite states.
old_new="function cbNewCircuit(type,devices,zoneId=null){const panel=cbNearestPanel(devices);if(!panel){alert('Add a Panel symbol to the plan or survey first. Circuit Builder needs a start point.');return null}"
new_new="function cbNewCircuit(type,devices,zoneId=null){const panel=cbNearestPanel(devices);if(!panel){uiNotice('Fire panel required','Add a fire panel (FAP) in Survey before building this circuit. Circuit Builder uses it as the start and return point.');return null}"
once(old_new,new_new,'no panel notice')
old_open="function openCircuitBuilder(){if(!img){alert('Start or import a floor plan first.');return}"
new_open="function openCircuitBuilder(){if(!img){uiNotice('Start a project first','Import a floor plan or start a blank floor before opening Circuit Builder.');return}"
once(old_open,new_open,'no plan notice')
old_broken="if(!devices.length||!panel){alert('This circuit needs its devices and a fire panel. Restore them in Survey / Zone Plan, or remove this circuit and create a new one.');return}"
new_broken="if(!devices.length||!panel){uiNotice('Circuit needs attention','This saved route is missing surveyed devices or its fire panel. Restore them in Survey, or remove this circuit and create a new route.');return}"
once(old_broken,new_broken,'broken circuit notice')
old_start="function cbStartAddressable(){const devices=cbSurveyDevices();if(!devices.length){alert('Place the surveyed devices first.');return}if(!cbPanels().length){alert('Add a Panel symbol first.');return}"
new_start="function cbStartAddressable(){const devices=cbSurveyDevices();if(!devices.length){uiNotice('No surveyed devices yet','Place the installed detectors and field devices in Survey before creating an addressable loop.');return}if(!cbPanels().length){uiNotice('Fire panel required','Add a fire panel (FAP) in Survey before creating an addressable loop.');return}"
once(old_start,new_start,'addressable notices')

# Pair snap copy is shorter and more immediately understandable onsite.
t=t.replace("pairMode&&cbDrag?.pairSnap?'⇄ TWIN CABLE SNAPPED':'⇄ TWIN CABLE SNAP'","pairMode&&cbDrag?.pairSnap?'⇄ CABLES PAIRED':'⇄ PAIR SNAP READY'",1)

# As-Fit summary updates whenever the validated preview opens.
old_show="function cbShow(screen){cbCheckpointDrag(true);cbHideCelebrate();cbScreen=screen;$('cbLanding').hidden=screen!=='home';$('cbGame').hidden=!(screen==='game'||screen==='select');$('cbAsFit').hidden=screen!=='asfit';if(screen==='home')cbRenderLanding();if(screen==='asfit')requestAnimationFrame(cbDrawAsFitPreview)}"
new_show="function cbShow(screen){cbCheckpointDrag(true);cbHideCelebrate();cbScreen=screen;$('cbLanding').hidden=screen!=='home';$('cbGame').hidden=!(screen==='game'||screen==='select');$('cbAsFit').hidden=screen!=='asfit';if(screen==='home')cbRenderLanding();if(screen==='asfit'){const valid=cbCircuits().filter(c=>c.complete&&!cbCircuitIssue(c));$('cbAsFitSummary').textContent='Validated from '+valid.length+' completed circuit'+(valid.length===1?'':'s')+' · '+activeFloor().name;requestAnimationFrame(cbDrawAsFitPreview)}}"
once(old_show,new_show,'As-Fit summary update')

# Reward, Undo, Retry and As-Fit status feedback.
old_undo="function cbUndo(){cbCheckpointDrag(true);if(!cbCircuit?.legs?.length)return;push();state.asFit=null;cbHideCelebrate();cbCircuit.legs.pop();cbCircuit.sequence.pop();cbCircuit.complete=false;cbCircuit.eolId=null;cbCircuit.updatedAt=Date.now();persist();cbRenderLanding();cbUpdateGame()}"
new_undo="function cbUndo(){cbCheckpointDrag(true);if(!cbCircuit?.legs?.length)return;push();state.asFit=null;cbHideCelebrate();cbCircuit.legs.pop();cbCircuit.sequence.pop();cbCircuit.complete=false;cbCircuit.eolId=null;cbCircuit.updatedAt=Date.now();persist();cbRenderLanding();cbUpdateGame();uiToast('Last cable leg undone','success')}"
once(old_undo,new_undo,'undo toast')
old_reset="function cbResetCurrent(){cbCheckpointDrag(true);cbHideCelebrate();if(cbScreen==='select'){cbSelection.clear();cbUpdateGame();return}if(!cbCircuit)return;push();state.asFit=null;cbCircuit.legs=[];cbCircuit.sequence=[cbCircuit.panelId];cbCircuit.complete=false;cbCircuit.eolId=null;cbCircuit.updatedAt=Date.now();persist();cbRenderLanding();cbUpdateGame()}"
new_reset="function cbResetCurrent(){cbCheckpointDrag(true);cbHideCelebrate();if(cbScreen==='select'){cbSelection.clear();cbUpdateGame();uiToast('Highlighted devices cleared');return}if(!cbCircuit)return;push();state.asFit=null;cbCircuit.legs=[];cbCircuit.sequence=[cbCircuit.panelId];cbCircuit.complete=false;cbCircuit.eolId=null;cbCircuit.updatedAt=Date.now();persist();cbRenderLanding();cbUpdateGame();uiToast('Circuit reset · start from the FAP','success')}"
once(old_reset,new_reset,'reset toast')
old_keep="function cbKeepCompleteCircuit(){if(!cbCircuit?.complete)return;cbHideCelebrate();cbCircuit=null;cbShow('home')}"
new_keep="function cbKeepCompleteCircuit(){if(!cbCircuit?.complete)return;cbHideCelebrate();uiToast('Circuit saved and validated','success');cbCircuit=null;cbShow('home')}"
once(old_keep,new_keep,'keep toast')
old_retry="function cbRetryCompleteCircuit(){cbResetCurrent()}"
new_retry="function cbRetryCompleteCircuit(){cbResetCurrent();uiToast('New run ready · start at the FAP','success')}"
once(old_retry,new_retry,'retry toast')
old_finish="state.asFit={generatedAt:Date.now(),circuitIds:list.filter(c=>c.complete&&!cbCircuitIssue(c)).map(c=>c.id)};persist();cbShow('asfit')}"
new_finish="state.asFit={generatedAt:Date.now(),circuitIds:list.filter(c=>c.complete&&!cbCircuitIssue(c)).map(c=>c.id)};persist();cbShow('asfit');uiToast('As-Fit generated from validated circuits','success')}"
once(old_finish,new_finish,'As-Fit toast')

# Haptic preference gates the completion vibration.
old_vibrate="try{navigator.vibrate?.([35,35,70])}catch(e){}"
new_vibrate="if(uiHaptics)try{navigator.vibrate?.([35,35,70])}catch(e){}"
once(old_vibrate,new_vibrate,'haptic preference')

# Completion copy is rewarding but still professional.
old_celebrate="$('cbCelebrateSub').textContent=q.total+' device'+(q.total===1?'':'s')+' · '+back+'. Keep it, undo the last leg, or retry the run.';"
new_celebrate="$('cbCelebrateSub').textContent=q.total+' device'+(q.total===1?'':'s')+' linked · '+back+'. Route validated and ready to keep.';"
once(old_celebrate,new_celebrate,'completion copy')

# Export-safe title copy; no behaviour change.
t=t.replace('Back to drawing</button></header>','Back to plan</button></header>',1)

# Keep every HTML entry point identical.
for name in ['ZoneSketch.html','Zone-Sketch-by-Will.html','app/src/main/assets/index.html']:
    Path(name).write_text(t)
p.write_text(t)

g=Path('app/build.gradle')
s=g.read_text().replace('versionCode 49','versionCode 50').replace("versionName '0.48'","versionName '0.49'")
g.write_text(s)
print('Applied v0.49 site-ready professional polish')
