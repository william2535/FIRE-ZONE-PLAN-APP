from pathlib import Path
import subprocess

# PERMANENT LOCK: the 24/7 Protection company demo is a separate, approved build.
# Normal Zone Sketch releases must never edit, regenerate, sync, or overwrite these files.
# If the company demo is intentionally revised one day, update this allow-list only as part
# of a deliberate 24/7-specific change after the new build has been approved.
EXPECTED = {
    'company-demos/247-protection/index.html': '46426ce3140511e334c79c5551e22267857b69f8',
    'company-demos/247-protection/logo.svg': '19efa04d3e735f7b8e26e1acf1168a2515a65d7c',
    'company-demos/247-protection/manifest.webmanifest': '50c55c3549e88b335a5b4631dad10fac7123776b',
    '247-protection-demo.html': '711b43c27946c729ef9eaf0549f73ce02be84039',
}

errors = []
for name, expected in EXPECTED.items():
    path = Path(name)
    if not path.is_file():
        errors.append(f'{name}: missing')
        continue
    actual = subprocess.check_output(['git', 'hash-object', name], text=True).strip()
    if actual != expected:
        errors.append(f'{name}: changed ({actual}, expected {expected})')

if errors:
    raise SystemExit(
        '24/7 Protection build is LOCKED and must remain untouched by Zone Sketch work.\n'
        + '\n'.join(errors)
    )

print('24/7 Protection build verified unchanged and protected')
