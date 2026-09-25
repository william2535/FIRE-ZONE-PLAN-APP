from pathlib import Path

p=Path('index.html')
t=p.read_text()
marker='/* v0.46 — celebration child style isolation. */'
if marker not in t:
    css=r'''
/* v0.46 — celebration child style isolation. */
#cbCelebrate .cbConfetti{position:absolute;inset:0;pointer-events:none;overflow:hidden;background:transparent;border-radius:0;padding:0;box-shadow:none;font-size:inherit;font-weight:400;animation:none}
#cbCelebrate .cbCelebrateCard{position:relative;z-index:2;width:min(390px,88%);padding:22px 20px 18px!important;border:1px solid #ffffff90;border-radius:24px!important;text-align:center;background:linear-gradient(180deg,#ffffff 0,#f3fff7 100%)!important;box-shadow:0 24px 70px #10263d73,0 0 0 7px #34b76c20!important;font-size:inherit;font-weight:400;animation:cbWinCard .34s cubic-bezier(.2,.9,.24,1.25)!important;overflow:hidden}
#cbCelebrate .cbCelebrateCard>.cbCelebrateBadge{width:74px;height:74px;margin:-2px auto 10px;padding:0;border-radius:50%;display:grid;place-items:center;background:linear-gradient(145deg,#32bd6d,#16884a);color:#fff;font-size:42px;font-weight:950;box-shadow:0 9px 26px #218c504c,0 0 0 8px #31b96b18;animation:cbBadgeBounce .55s cubic-bezier(.2,.9,.2,1.3)}
#cbCelebrate .cbCelebrateCard>.cbCelebrateKicker{margin:0 0 4px;padding:0;background:transparent;border-radius:0;box-shadow:none;font-size:10px;font-weight:900;letter-spacing:.18em;color:#25834e;animation:none}
#cbCelebrate .cbCelebrateCard>.cbCelebrateTitle{margin:0;padding:0;background:transparent;border-radius:0;box-shadow:none;font-size:23px;font-weight:900;color:#173a29;animation:none}
#cbCelebrate .cbCelebrateCard>.cbCelebrateSub{margin:7px auto 14px;padding:0;max-width:290px;background:transparent;border-radius:0;box-shadow:none;font-size:12px;font-weight:500;color:#587061;line-height:1.4;animation:none}
#cbCelebrate .cbCelebrateCard>.cbCelebrateActions{margin:0;padding:0;background:transparent;border-radius:0;box-shadow:none;font-size:inherit;font-weight:400;animation:none;display:grid;grid-template-columns:1fr 1fr;gap:7px}
@media(max-width:520px){#cbCelebrate .cbCelebrateCard{width:min(350px,91%);padding:18px 14px 14px!important}#cbCelebrate .cbCelebrateCard>.cbCelebrateBadge{width:64px;height:64px;font-size:36px}#cbCelebrate .cbCelebrateCard>.cbCelebrateTitle{font-size:20px}#cbCelebrate .cbCelebrateCard>.cbCelebrateActions{grid-template-columns:1fr}}
'''
    t=t.replace('</style>',css+'</style>',1)
for name in ['index.html','ZoneSketch.html','Zone-Sketch-by-Will.html','app/src/main/assets/index.html']:
    Path(name).write_text(t)
print('Applied v0.46 celebration style isolation')
