from __future__ import annotations

import base64
from hashlib import sha256
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / ".github/brand-v2-source"
OUT = ROOT / "assets/brand/master-v2-approved/production"
WEB_ICON = ROOT / "assets/on-site-zone-planner-icon.webp"
ANDROID_DRAWABLE = ROOT / "app/src/main/res/drawable"
RESAMPLE = Image.Resampling.LANCZOS

def assemble_primary() -> bytes:
    # part01 deliberately contains source chunks 01+02 from the interrupted upload.
    names = ["primary.part00.b64","primary.part01.b64","primary.part02.b64","primary.part04.b64"]
    encoded = "".join((PARTS / n).read_text(encoding="utf-8").strip() for n in names)
    return base64.b64decode(encoded, validate=True)

def save_png(im: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "PNG", optimize=True)

def save_webp(im: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "WEBP", lossless=True, method=6)

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ANDROID_DRAWABLE.mkdir(parents=True, exist_ok=True)

    source_bytes = assemble_primary()
    source = OUT / "zone-sketch-primary-source.webp"
    source.write_bytes(source_bytes)

    with Image.open(source) as opened:
        primary = opened.convert("RGBA")
    if primary.size != (312, 312):
        raise SystemExit(f"Unexpected approved primary size {primary.size}; expected 312x312")

    for size in (1024,512,256,192,180,128,64,32,16):
        save_png(primary.resize((size,size), RESAMPLE), OUT / f"zone-sketch-primary-{size}.png")

    primary_1024 = primary.resize((1024,1024), RESAMPLE)
    save_webp(primary_1024, OUT / "zone-sketch-primary-1024.webp")
    save_webp(primary_1024, WEB_ICON)
    save_webp(primary_1024, ANDROID_DRAWABLE / "app_icon.webp")

    digest = sha256(source_bytes).hexdigest()
    (OUT / "primary-source.sha256").write_text(digest + "\n", encoding="utf-8")
    print(f"Built approved v2 primary brand source: {primary.size}, sha256={digest}")

if __name__ == "__main__":
    main()
