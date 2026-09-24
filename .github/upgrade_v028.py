from pathlib import Path

ROOT = Path('.')
html_paths = [
    ROOT/'index.html',
    ROOT/'ZoneSketch.html',
    ROOT/'Zone-Sketch-by-Will.html',
    ROOT/'app/src/main/assets/index.html',
]

text = html_paths[0].read_text()
if 'v0.27' not in text:
    raise SystemExit('v0.28 expected v0.27 HTML baseline was not found')

css = r'''

/* v0.28 — lock the app viewport so iOS/Safari cannot rubber-band the whole page. */
html{width:100%;height:100%;overflow:hidden;overscroll-behavior:none;background:#e8edf3}
body{width:100%;height:100%;min-height:0!important;overflow:hidden;overscroll-behavior:none;position:fixed;inset:0}
.app{height:100dvh;max-height:100dvh;overflow:hidden}
.workspace,.canvasWrap{overscroll-behavior:none}
.canvasWrap,.canvasWrap canvas{touch-action:none;-webkit-user-select:none;user-select:none}
#projectsHome,.toolPopup,.box,.side,.zoneList{overscroll-behavior:contain}
'''

if 'v0.28 — lock the app viewport' not in text:
    if '</style>' not in text:
        raise SystemExit('v0.28 could not find closing style tag')
    text = text.replace('</style>', css + '\n</style>', 1)

js = r'''
<script>
/* v0.28 iOS/Safari canvas scroll lock. Menus and modal panels keep their own scrolling. */
(()=>{
  const stopCanvasPageScroll=e=>{
    const target=e.target;
    if(target&&target.closest&&target.closest('.canvasWrap')) e.preventDefault();
  };
  document.addEventListener('touchmove',stopCanvasPageScroll,{passive:false});
})();
</script>
'''

if 'v0.28 iOS/Safari canvas scroll lock' not in text:
    if '</body>' not in text:
        raise SystemExit('v0.28 could not find closing body tag')
    text = text.replace('</body>', js + '\n</body>', 1)

text = text.replace('v0.27', 'v0.28')

for path in html_paths:
    path.write_text(text)

build = ROOT/'app/build.gradle'
b = build.read_text()
if 'versionCode 27' not in b or "versionName '0.27'" not in b:
    raise SystemExit('v0.28 expected Android v0.27 baseline was not found')
b = b.replace('versionCode 27', 'versionCode 28', 1)
b = b.replace("versionName '0.27'", "versionName '0.28'", 1)
build.write_text(b)

print('Applied v0.28 locked web viewport and iOS/Safari canvas scroll protection')
