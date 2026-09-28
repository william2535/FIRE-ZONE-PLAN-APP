from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "assets/brand/master-v2-approved/approved-board.webp"
OUT = ROOT / "assets/brand/master-v2-approved/production"
ANDROID_DRAWABLE = ROOT / "app/src/main/res/drawable"
WEB_ICON = ROOT / "assets/on-site-zone-planner-icon.webp"
RESAMPLE = Image.Resampling.LANCZOS
DARK = (2, 10, 16)


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "PNG", optimize=True)


def save_webp(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "WEBP", lossless=True, method=6)


def square_primary(board: Image.Image) -> Image.Image:
    # Exact approved primary icon region from the locked 1536x1024 board.
    # The source region is 312x272; 20px top/bottom dark padding preserves the
    # approved house/frame proportions while producing a square launcher asset.
    crop = board.crop((52, 78, 364, 350)).convert("RGB")
    out = Image.new("RGB", (312, 312), DARK)
    out.paste(crop, (0, 20))
    return out


def square_crop(board: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    return board.crop(box).convert("RGB")


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    board = Image.open(BOARD).convert("RGB")
    if board.size != (1536, 1024):
        raise SystemExit(f"Unexpected approved board size {board.size}; expected 1536x1024")

    OUT.mkdir(parents=True, exist_ok=True)
    ANDROID_DRAWABLE.mkdir(parents=True, exist_ok=True)

    sources = {
        "primary": square_primary(board),
        "fire": square_crop(board, (435, 80, 600, 245)),
        "cctv": square_crop(board, (610, 80, 775, 245)),
        "access": square_crop(board, (785, 80, 950, 245)),
        "mono": square_crop(board, (960, 80, 1120, 240)),
    }

    generated: list[Path] = []
    for name, image in sources.items():
        source_path = OUT / f"zone-sketch-{name}-source.png"
        save_png(image, source_path)
        generated.append(source_path)

        p1024 = OUT / f"zone-sketch-{name}-1024.png"
        save_png(image.resize((1024, 1024), RESAMPLE), p1024)
        generated.append(p1024)

    primary = sources["primary"]
    for size in (512, 256, 192, 180, 128, 64, 32, 16):
        p = OUT / f"zone-sketch-primary-{size}.png"
        save_png(primary.resize((size, size), RESAMPLE), p)
        generated.append(p)

    primary_1024 = primary.resize((1024, 1024), RESAMPLE)
    p_primary_webp = OUT / "zone-sketch-primary-1024.webp"
    save_webp(primary_1024, p_primary_webp)
    generated.append(p_primary_webp)

    # Keep the exact approved wordmark and splash regions as their own masters.
    wordmark = board.crop((30, 520, 490, 655)).convert("RGB")
    p_wordmark_source = OUT / "zone-sketch-wordmark-source.png"
    save_png(wordmark, p_wordmark_source)
    generated.append(p_wordmark_source)
    p_wordmark = OUT / "zone-sketch-wordmark-1840.png"
    save_png(wordmark.resize((1840, 540), RESAMPLE), p_wordmark)
    generated.append(p_wordmark)

    splash = board.crop((945, 455, 1190, 840)).convert("RGB")
    p_splash_source = OUT / "zone-sketch-splash-source.png"
    save_png(splash, p_splash_source)
    generated.append(p_splash_source)
    splash_h = round(1080 * splash.height / splash.width)
    splash_big = splash.resize((1080, splash_h), RESAMPLE)
    p_splash_png = OUT / "zone-sketch-splash-1080.png"
    save_png(splash_big, p_splash_png)
    generated.append(p_splash_png)
    p_splash_webp = OUT / "zone-sketch-splash-1080.webp"
    save_webp(splash_big, p_splash_webp)
    generated.append(p_splash_webp)

    # Live integration targets. These are generated from the same locked board,
    # not redrawn SVG approximations.
    save_webp(primary_1024, WEB_ICON)
    generated.append(WEB_ICON)
    save_webp(primary_1024, ANDROID_DRAWABLE / "app_icon.webp")
    generated.append(ANDROID_DRAWABLE / "app_icon.webp")
    save_webp(splash_big, ANDROID_DRAWABLE / "app_splash.webp")
    generated.append(ANDROID_DRAWABLE / "app_splash.webp")

    manifest = {
        "source": str(BOARD.relative_to(ROOT)),
        "source_size": list(board.size),
        "rule": "Exact crops from the user-approved v2 board; never regenerate or reinterpret for production.",
        "primary": {
            "house": "glossy blue/cyan to green",
            "flame": "layered glowing red/orange",
        },
        "access_control": "green",
        "files": {
            str(path.relative_to(ROOT)): {
                "bytes": path.stat().st_size,
                "sha256": digest(path),
            }
            for path in generated
        },
    }
    (OUT / "production-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"Generated {len(generated)} approved brand assets from {BOARD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
