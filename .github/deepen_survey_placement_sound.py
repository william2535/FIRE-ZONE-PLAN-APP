from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

pattern = re.compile(r"let surveyPlacementSoundStep=0;\nfunction surveyPlacementSound\(type='smoke'\)\{.*?\n\}\n\nfunction cbPlayProgressBell", re.S)
replacement = r'''let surveyPlacementSoundStep=0;
function surveyPlacementSound(type='smoke'){
 const ctx=cbEnsureAudio();if(!ctx)return;
 const now=ctx.currentTime+.002,variations=[.97,1,.985,1.02],variation=variations[surveyPlacementSoundStep%variations.length];surveyPlacementSoundStep=(surveyPlacementSoundStep+1)%variations.length;
 const weight={panel:.92,repeater:.95,mcp:1,smoke:1.02,heat:.98,sounder:.94,beacon:1.04,beam:.90,io:.96}[type]||1;
 const master=ctx.createGain();master.gain.setValueAtTime(.88,now);master.connect(ctx.destination);
 // Deep mechanical-keyboard style THOCK: a heavy shell/body impact with a fast low-frequency drop.
 const body=ctx.createOscillator(),bodyGain=ctx.createGain();body.type='sine';body.frequency.setValueAtTime(188*weight*variation,now);body.frequency.exponentialRampToValueAtTime(82*weight,now+.095);bodyGain.gain.setValueAtTime(.0001,now);bodyGain.gain.exponentialRampToValueAtTime(.095,now+.003);bodyGain.gain.exponentialRampToValueAtTime(.0001,now+.115);body.connect(bodyGain);bodyGain.connect(master);body.start(now);body.stop(now+.125);
 // Switch snap: short, muted and low-mid rather than bright/glassy.
 const snap=ctx.createOscillator(),snapGain=ctx.createGain();snap.type='triangle';snap.frequency.setValueAtTime(520*weight*variation,now+.002);snap.frequency.exponentialRampToValueAtTime(285*weight,now+.026);snapGain.gain.setValueAtTime(.0001,now+.002);snapGain.gain.exponentialRampToValueAtTime(.048,now+.0045);snapGain.gain.exponentialRampToValueAtTime(.0001,now+.039);snap.connect(snapGain);snapGain.connect(master);snap.start(now+.002);snap.stop(now+.045);
 // Damped case resonance gives the click a dense mechanical-keyboard body without a musical shimmer.
 const knock=ctx.createOscillator(),knockGain=ctx.createGain();knock.type='triangle';knock.frequency.setValueAtTime(276*weight*variation,now+.006);knock.frequency.exponentialRampToValueAtTime(168*weight,now+.065);knockGain.gain.setValueAtTime(.0001,now+.006);knockGain.gain.exponentialRampToValueAtTime(.034,now+.011);knockGain.gain.exponentialRampToValueAtTime(.0001,now+.085);knock.connect(knockGain);knockGain.connect(master);knock.start(now+.006);knock.stop(now+.095);
 // Tiny low-passed texture creates the physical keycap contact, kept deliberately dark.
 const samples=Math.max(64,Math.floor(ctx.sampleRate*.018)),buffer=ctx.createBuffer(1,samples,ctx.sampleRate),data=buffer.getChannelData(0);for(let i=0;i<samples;i++){const e=1-i/samples;data[i]=(Math.random()*2-1)*e*e}
 const texture=ctx.createBufferSource(),filter=ctx.createBiquadFilter(),textureGain=ctx.createGain();texture.buffer=buffer;filter.type='lowpass';filter.frequency.setValueAtTime(1050*weight,now);filter.Q.setValueAtTime(.8,now);textureGain.gain.setValueAtTime(.0001,now);textureGain.gain.linearRampToValueAtTime(.026,now+.002);textureGain.gain.exponentialRampToValueAtTime(.0001,now+.025);texture.connect(filter);filter.connect(textureGain);textureGain.connect(master);texture.start(now);texture.stop(now+.03);
 const end=now+.14;setTimeout(()=>{try{master.disconnect()}catch(e){}},180);
 if(typeof uiHaptics!=='undefined'&&uiHaptics&&navigator.vibrate){try{navigator.vibrate(9)}catch(e){}}
}

function cbPlayProgressBell'''

if not pattern.search(text):
    raise SystemExit('Survey placement sound function not found')
text = pattern.sub(replacement, text, count=1)
p.write_text(text, encoding='utf-8')
print('index.html: Survey placement sound deepened to mechanical thock')
