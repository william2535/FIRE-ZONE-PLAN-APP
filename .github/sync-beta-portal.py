from pathlib import Path
import re
import sys

REPO = "william2535/FIRE-ZONE-PLAN-APP"
CANONICAL_BETA_URL = "https://william2535.github.io/FIRE-ZONE-PLAN-APP/beta.html"
PORTALS = (Path("beta.html"), Path("download.html"))


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: python .github/sync-beta-portal.py <version, e.g. 0.52>")

    version = sys.argv[1].strip().lstrip("v")
    if not re.fullmatch(r"\d+\.\d+", version):
        fail(f"invalid Zone Sketch version: {version!r}")

    tag = f"v{version}"
    apk = f"Zone-Sketch-by-Will-{tag}.apk"
    release_url = f"https://github.com/{REPO}/releases/download/{tag}/{apk}"
    mirror_path = f"downloads/{apk}"

    for portal in PORTALS:
        text = portal.read_text(encoding="utf-8")

        # The beta portal intentionally exposes only the current tester version.
        # Updating this one version value refreshes visible labels, feedback text,
        # release/mirror filenames and download URLs together.
        text = re.sub(r"v\d+\.\d+", tag, text)
        text = re.sub(
            rf"https://github\.com/{re.escape(REPO)}/releases/download/{re.escape(tag)}/Zone-Sketch-by-Will-{re.escape(tag)}\.apk",
            release_url,
            text,
        )
        text = re.sub(
            rf"downloads/Zone-Sketch-by-Will-{re.escape(tag)}\.apk",
            mirror_path,
            text,
        )

        portal.write_text(text, encoding="utf-8")

        required = (
            f"<title>Zone Sketch Beta Tester Portal · {tag} · Will Flood</title>",
            f"const BETA_VERSION='{tag}'",
            release_url,
            mirror_path,
            f'<link rel="canonical" href="{CANONICAL_BETA_URL}">',
            "href=\"./index.html\"",
            f"const betaUrl='{CANONICAL_BETA_URL}'",
        )
        missing = [item for item in required if item not in text]
        if missing:
            fail(f"{portal}: beta delivery guard failed; missing {missing}")

        versions = set(re.findall(r"v\d+\.\d+", text))
        if versions != {tag}:
            fail(f"{portal}: stale beta versions remain: {sorted(versions)}")

    if PORTALS[0].read_bytes() != PORTALS[1].read_bytes():
        fail("beta.html and download.html are not identical")

    print(f"Beta portal synced and verified for {tag}: {release_url}")


if __name__ == "__main__":
    main()
