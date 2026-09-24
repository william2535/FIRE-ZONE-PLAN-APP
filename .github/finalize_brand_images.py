from pathlib import Path
import re

# Use the generated banner as the one visible repository cover.
r = Path('README.md')
t = r.read_text()
old_jpg = '<p align="center">\n  <img src="assets/on-site-zone-planner-cover.jpg" alt="On Site Zone Planner" width="100%">\n</p>\n\n'
new_webp = '<p align="center">\n  <img src="assets/on-site-zone-planner-cover.webp" alt="On Site Zone Planner" width="100%">\n</p>\n\n'
t = t.replace(old_jpg, '')
t = t.replace('\n![On Site Zone Planner](assets/on-site-zone-planner-cover.svg)\n', '\n')
t = t.replace(new_webp, '')
r.write_text(new_webp + t.lstrip())

# Use the generated square icon for both normal and round Android launcher icons.
m = Path('app/src/main/AndroidManifest.xml')
s = m.read_text()
s = re.sub(r' android:icon="@drawable/[^"]+"', '', s)
s = re.sub(r' android:roundIcon="@drawable/[^"]+"', '', s)
s = s.replace('android:label="Zone Sketch by Will"', 'android:label="Zone Sketch by Will" android:icon="@drawable/app_icon" android:roundIcon="@drawable/app_icon"', 1)
m.write_text(s)

# Remove older temporary / placeholder visual assets so copies are unambiguous.
for name in [
    'assets/on-site-zone-planner-cover.jpg',
    'assets/on-site-zone-planner-icon.png',
    'assets/on-site-zone-planner-cover.svg',
    'app/src/main/res/drawable/app_icon.png',
    'app/src/main/res/drawable/app_icon_brand.xml',
    'app/src/main/res/drawable/app_icon_zone_planner.xml',
]:
    p = Path(name)
    if p.exists():
        p.unlink()

print('Final On Site Zone Planner cover and launcher icon selected')
