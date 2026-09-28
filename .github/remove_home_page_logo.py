from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
original = text

home_logo = '<img class="homeBrandMark" src="assets/on-site-zone-planner-icon.webp" alt="Zone Sketch">'

if home_logo in text:
    text = text.replace(home_logo, '', 1)

if 'class="homeBrandMark"' in text:
    raise SystemExit('A home-page brand mark still remains after the targeted removal')

# Guard the two places the user explicitly wants to keep branded.
if 'id="zsSplash"' not in text or 'assets/on-site-zone-planner-icon.webp' not in text:
    raise SystemExit('Splash branding guard failed')
if 'id="headerHomeBtn"' not in text or 'assets/zone-sketch-header-mark.png' not in text:
    raise SystemExit('In-app header home-logo guard failed')

if text != original:
    p.write_text(text, encoding='utf-8')
    print('index.html: removed logo from Projects/Home hero only')
else:
    print('index.html: Projects/Home hero logo already removed')
