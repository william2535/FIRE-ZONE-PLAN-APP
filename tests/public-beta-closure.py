"""Check public Pages closure without changing the native app or Play testing."""
from pathlib import Path
import argparse
import fnmatch
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PLAY = 'https://play.google.com/store/apps/details?id=com.zonesketch.app'
ROUTES = {'index.html', 'beta.html', 'download.html', 'ZoneSketch.html', 'Zone-Sketch-by-Will.html', '404.html'} | {f'web-v0{v}.html' for v in range(58, 65)}
PROTECTED_TEMPLATES = {
    'protected-demo.html': ('company-demos/247-protection/index.html', 'index.html'),
    'protected-logo.svg': ('company-demos/247-protection/logo.svg', 'logo.svg'),
    'protected-manifest.webmanifest': ('company-demos/247-protection/manifest.webmanifest', 'manifest.webmanifest'),
}
CLOSED_NAMES = {'closed-' + name + '.html' for name in ['home', 'beta', 'download', 'zone-sketch', 'zone-sketch-by-will', 'not-found']} | {f'closed-web-v0{v}.html' for v in range(58, 65)}
ALLOWED = {'public-closure', 'privacy.html', 'terms.html', '247-protection-demo.html', 'vendor', 'pdf.min.js', 'pdf.worker.min.js'} | CLOSED_NAMES | set(PROTECTED_TEMPLATES)


def check(site=None):
    config = json.loads((ROOT / '_config.yml').read_text())  # JSON is valid YAML.
    assert config['exclude'] == ['*'], 'Pages must default to excluding repository files'
    assert set(config['include']) == ALLOWED, 'Only the reviewed closure/privacy/protected-demo resources may publish'
    assert not (ROOT / '.nojekyll').exists(), '.nojekyll would bypass the exclusion policy'
    assert config['baseurl'] == '/FIRE-ZONE-PLAN-APP'
    assert config['includes_dir'] == 'company-demos/247-protection'
    assert {p.name for p in (ROOT / 'public-closure').iterdir()} == CLOSED_NAMES | set(PROTECTED_TEMPLATES)
    # Jekyll 3.10 checks includes against a bare entry basename, not its full
    # directory-relative path. Listing a directory does NOT allow its children.
    # In particular, allowing index.html would expose the original root app.
    # Unique template basenames keep the default-deny filter effective.
    for forbidden in ['index.html', 'beta.html', 'download.html', 'ZoneSketch.html',
                      'Zone-Sketch-by-Will.html', 'web-v064.html',
                      'downloads/Zone-Sketch-by-Will-v0.64.apk',
                      'app/src/main/assets/index.html', 'node_modules/anything.js',
                      'tests/browser.cjs', 'docs/source.md', 'scripts/source.py']:
        assert not any(fnmatch.fnmatchcase(Path(forbidden).name, item) or Path(forbidden).name.startswith(item)
                       for item in ALLOWED), forbidden
    found = set()
    for page in (ROOT / 'public-closure').glob('closed-*.html'):
        text = page.read_text()
        match = re.match(r'---\nlayout: null\npermalink: /([^\n]+)\n---\n', text)
        assert match, page
        found.add(match[1])
        assert 'Public beta closed' in text and PLAY in text, page
        assert 'Google Play testing is separate and has not been closed.' in text, page
        assert '<script' not in text.lower() and '<iframe' not in text.lower(), page
        assert not re.search(r'href=[\"\'][^\"\']*(?:\.apk|web-v\d+\.html|/index\.html)', text), page
    assert found == ROUTES, (found, ROUTES)
    for name, (route, source) in PROTECTED_TEMPLATES.items():
        expected = f'---\nlayout: null\npermalink: /{route}\n---\n{{% include {source} %}}'
        assert (ROOT / 'public-closure' / name).read_text() == expected, name
    workflow = (ROOT / '.github/workflows/build-apk.yml').read_text()
    assert workflow.count("vars.ZONE_SKETCH_PUBLIC_BETA == 'enabled'") == 2, 'Public release and installable artifact both require deliberate opt-in'
    assert 'python3 tests/public-beta-closure.py' in workflow
    if site:
        site = Path(site)
        for route in ROUTES:
            text = (site / route).read_text()
            assert 'Public beta closed' in text and PLAY in text, route
        for forbidden in ['app', 'downloads', 'node_modules', 'tests', 'docs', 'scripts', '.github']:
            assert not (site / forbidden).exists(), f'Excluded source reached Pages: {forbidden}'
        assert not any(site.rglob('*.apk')), 'Installable APK leaked into Pages'
        for protected in ['247-protection-demo.html', 'company-demos/247-protection/index.html',
                          'company-demos/247-protection/logo.svg',
                          'company-demos/247-protection/manifest.webmanifest',
                          'vendor/pdf.min.js', 'vendor/pdf.worker.min.js', 'privacy.html', 'terms.html']:
            assert (site / protected).read_bytes() == (ROOT / protected).read_bytes(), protected
    print('PASS public beta closure, source exclusions, Play link and protected-demo preservation' + (' in actual Jekyll output' if site else ' (source checks)'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, help='Also verify actual Jekyll output')
    check(parser.parse_args().site)
