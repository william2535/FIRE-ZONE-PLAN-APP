from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
original = text

version_markup = '<div class="homeVersion">ZONE SKETCH · v0.62</div>'
if version_markup in text:
    text = text.replace(version_markup, '', 1)

marker = '/* Home Recent Projects heading cleanup. */'
css = '''
/* Home Recent Projects heading cleanup. */
#projectsHome .homeHeading:after{display:none!important;animation:none!important;content:none!important}
/* End Home Recent Projects heading cleanup. */
'''.strip()
if marker not in text:
    if '</style>' not in text:
        raise SystemExit('Closing style tag not found')
    text = text.replace('</style>', css + '\n</style>', 1)

if text != original:
    p.write_text(text, encoding='utf-8')
    print('index.html: removed Recent Projects trace and version label')
else:
    print('index.html: Recent Projects heading already clean')
