# Public web/APK beta closure

Prepared 18 November 2026, from Zone Sketch source `e658e60b824b9f04f972ef64c46e38e4c1f6fe9d` (0.64, Android code 65, package `com.zonesketch.app`). The owner explicitly asked to close the public free web/APK route while leaving Google Play testing open.

## What this change does

- Uses the existing branch-based GitHub Pages Jekyll publication with a default-deny file selection. Retiring `.nojekyll` is necessary so `_config.yml` is honoured.
- Jekyll 3.10 matches included entry basenames, not nested paths. Closure templates therefore use unique `closed-*` names with public permalinks; do not add `index.html` or other original app basenames to the include list. Three small include templates publish the unchanged protected company demo and its two assets at their existing paths. The output check compares these with the original bytes.
- Publishes closed notices at the home, beta, download, named app aliases, seven old version launchers and the 404 page. These notices link to `https://play.google.com/store/apps/details?id=com.zonesketch.app` and do not promise public listing availability. An anonymous UK request returned 404 during preparation; existing tester access may differ.
- Excludes native/web app source, direct APK mirrors, tests, scripts and repository tooling from the Pages site. The actual source and APK files remain intact in Git.
- Stops automatic public release APK publication and installable Actions artifact publication unless the owner deliberately sets repository variable `ZONE_SKETCH_PUBLIC_BETA` to `enabled`. It does not change Google Play tracks, testers or releases.
- Preserves the separately locked 24/7 Protection company demo and its PDF runtime byte-for-byte, including its existing public route. It is outside this requested generic-beta closure.
- Does not delete browser storage or installed apps. Existing offline/downloaded copies cannot be remotely revoked by a website change.

## What remains public until the owner changes repository/release access

This repository is public. Raw files, Git history, source clones, historical GitHub Release APK assets and previously generated Actions artifacts may remain accessible outside GitHub Pages. The current v0.64 release and earlier releases were public during inspection. No release, artifact, source file or history was deleted here, and repository visibility was not changed.

Closing Pages routes therefore closes the normal hosted tester path, **not every possible way to obtain an old copy**. To stop new public access through GitHub as well, the owner must make this repository private in GitHub **Settings → General → Danger Zone → Change repository visibility**, or separately decide which release assets/artifacts to withdraw and how to protect source. Making it private affects the open-source repository and may affect Pages availability depending on the account plan. The connection used here does not establish administrative access to change visibility. Copies already downloaded or forked cannot be recalled.

Do not set `ZONE_SKETCH_PUBLIC_BETA=enabled`, restore `.nojekyll`, widen the Pages include list or run old historical publication workflows unless intentionally reopening distribution. Old manually dispatched release workflows remain historical tooling and were not invoked by this change.

## Verification

Run `python3 tests/public-beta-closure.py`, `python3 .github/verify_247_protected.py` and `node tests/release-v064.cjs`. The new `Verify public beta closure` workflow also builds with the official GitHub Pages Jekyll action and checks its actual output with `--site _site`.

After publication, verify `/beta.html`, `/download.html`, `/index.html` and old launcher aliases show the closure notice; direct `/downloads/*.apk` and `/app/src/main/assets/index.html` should return 404. Confirm the protected company demo still loads. Do not call closure fully verified until those live checks and the Jekyll-output check pass.
