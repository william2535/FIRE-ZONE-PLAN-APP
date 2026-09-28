from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

SOUND_MARKER = 'function surveyPlacementSound(type=\'smoke\')'
SOUND_FUNCTION = r'''

let surveyPlacementSoundStep=0;
function surveyPlacementSound(type='smoke'){
 const ctx=cbEnsureAudio();if(!ctx)return;
 const now=ctx.currentTime+.003,steps=[.94,.98,1.02,1.06,1.10],step=steps[surveyPlacementSoundStep%steps.length];surveyPlacementSoundStep=(surveyPlacementSoundStep+1)%steps.length;
 const notes={panel:620,repeater:650,mcp:690,smoke:760,heat:720,sounder:665,beacon:810,beam:590,io:640},pitch=(notes[type]||720)*step;
 // A tiny tactile seat/thump makes the symbol feel like it physically lands on the plan.
 const body=ctx.createOscillator(),bodyGain=ctx.createGain();body.type='sine';body.frequency.setValueAtTime(205,now);body.frequency.exponentialRampToValueAtTime(102,now+.072);bodyGain.gain.setValueAtTime(.0001,now);bodyGain.gain.exponentialRampToValueAtTime(.052,now+.004);bodyGain.gain.exponentialRampToValueAtTime(.0001,now+.09);body.connect(bodyGain);bodyGain.connect(ctx.destination);body.start(now);body.stop(now+.1);
 // Short filtered texture: a soft ASMR click rather than a harsh UI beep.
 const samples=Math.max(64,Math.floor(ctx.sampleRate*.015)),buffer=ctx.createBuffer(1,samples,ctx.sampleRate),data=buffer.getChannelData(0);for(let i=0;i<samples;i++){const e=1-i/samples;data[i]=(Math.random()*2-1)*e*e}
 const click=ctx.createBufferSource(),filter=ctx.createBiquadFilter(),clickGain=ctx.createGain();click.buffer=buffer;filter.type='bandpass';filter.frequency.setValueAtTime(3200,now);filter.Q.setValueAtTime(.72,now);clickGain.gain.setValueAtTime(.0001,now);clickGain.gain.linearRampToValueAtTime(.022,now+.002);clickGain.gain.exponentialRampToValueAtTime(.0001,now+.021);click.connect(filter);filter.connect(clickGain);clickGain.connect(ctx.destination);click.start(now);click.stop(now+.024);
 // Glassy two-note shimmer. Repeated placements climb a five-step micro-scale for extra reward.
 for(const [mul,level,duration,delay,wave] of [[1,.041,.24,.014,'sine'],[2.01,.012,.18,.018,'triangle'],[3.98,.0045,.12,.024,'sine']]){const o=ctx.createOscillator(),g=ctx.createGain(),t=now+delay;o.type=wave;o.frequency.setValueAtTime(pitch*mul,t);o.frequency.exponentialRampToValueAtTime(pitch*mul*1.012,t+.038);g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(level,t+.006);g.gain.exponentialRampToValueAtTime(.0001,t+duration);o.connect(g);g.connect(ctx.destination);o.start(t);o.stop(t+duration+.025)}
 if(typeof uiHaptics!=='undefined'&&uiHaptics&&navigator.vibrate){try{navigator.vibrate(7)}catch(e){}}
}
'''

if SOUND_MARKER not in text:
    anchor = 'function cbPlayProgressBell(done,total)'
    if anchor not in text:
        raise SystemExit('Audio anchor not found')
    text = text.replace(anchor, SOUND_FUNCTION + '\n' + anchor, 1)

beam_old = "changed();if(surveyMode)uiToast('Beam detector added','success');setHint('Beam placed · triangle points where your finger finished');"
beam_new = "changed();if(surveyMode){surveyPlacementSound('beam');uiToast('Beam detector added','success')}setHint('Beam placed · triangle points where your finger finished');"
if beam_old in text:
    text = text.replace(beam_old, beam_new, 1)
elif beam_new not in text:
    raise SystemExit('Beam placement hook not found')

symbol_old = "else if(tool==='symbol'){push();state.symbols.push({id:uid(),...inputPoint(e.clientX,e.clientY),type:symbolStamp,color:symbolColor,scale:symbolStampScale,rotation:0,scope:surveyMode?'survey':'plan',group:null});changed();if(surveyMode)uiToast((symbolNames[symbolStamp]||'Device')+' added','success')}"
symbol_new = "else if(tool==='symbol'){push();state.symbols.push({id:uid(),...inputPoint(e.clientX,e.clientY),type:symbolStamp,color:symbolColor,scale:symbolStampScale,rotation:0,scope:surveyMode?'survey':'plan',group:null});changed();if(surveyMode){surveyPlacementSound(symbolStamp);uiToast((symbolNames[symbolStamp]||'Device')+' added','success')}}"
if symbol_old in text:
    text = text.replace(symbol_old, symbol_new, 1)
elif symbol_new not in text:
    raise SystemExit('Survey symbol placement hook not found')

text = text.replace('<strong>Circuit sounds</strong><small>Rising detector bells and completion chime</small>', '<strong>App sounds</strong><small>Survey placement ASMR + Circuit Builder chimes</small>', 1)
text = text.replace('title="Toggle Circuit Builder sounds"', 'title="Toggle app sounds"', 1)
text = text.replace("uiToast('Circuit sounds '+(cbSound?'on':'off'),'success')", "uiToast('Sounds '+(cbSound?'on':'off'),'success')")

p.write_text(text, encoding='utf-8')
print('index.html: survey placement ASMR sound installed')
