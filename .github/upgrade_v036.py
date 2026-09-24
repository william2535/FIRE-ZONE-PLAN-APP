from pathlib import Path
import base64, gzip

parts = [
    Path('.github/v036_payload_1.txt').read_text().strip(),
    Path('.github/v036_payload_2.txt').read_text().strip(),
    Path('.github/v036_payload_3.txt').read_text().strip(),
]
payload = ''.join(parts)
if [len(p) for p in parts] != [3700, 3700, 3700] or len(payload) != 11100:
    raise SystemExit(f'v0.36 payload length mismatch: parts={[len(p) for p in parts]}, total={len(payload)}')
source = gzip.decompress(base64.b64decode(payload, validate=True)).decode('utf-8')
exec(compile(source, '.github/upgrade_v036.py.payload', 'exec'))
