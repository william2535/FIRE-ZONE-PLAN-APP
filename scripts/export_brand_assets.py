#!/usr/bin/env python3
"""Render Zone Sketch SVG masters into deterministic PNG export sizes."""
from pathlib import Path
try:
    import cairosvg
except ImportError:
    raise SystemExit("Install CairoSVG first: python -m pip install cairosvg")

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "assets" / "brand" / "master-v1"
EXPORT = MASTER / "exports"
SIZES = (1024, 512, 256, 192, 180, 128, 64, 32)

def render(svg: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    for size in SIZES:
        out = output_dir / f"{svg.stem}-{size}.png"
        cairosvg.svg2png(url=str(svg), write_to=str(out), output_width=size, output_height=size)
        print(out.relative_to(ROOT))

for name in ("primary", "fire", "cctv", "access", "mono"):
    render(MASTER / f"zone-sketch-mark-{name}.svg", EXPORT / name)
