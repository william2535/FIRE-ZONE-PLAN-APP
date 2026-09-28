# Home and tester branding — 28 September 2026

Based on main 737e488 and the approved master-v2 identity. Home/Projects and beta/download now share the #06111D blueprint background, #00C2FF cyan frames, #9BFF3F primary actions and original approved house/red-flame artwork. No regenerated logo or changes to drawing colours or app logic.

Home includes themed search, project cards, action buttons, keyboard focus and responsive 320px–desktop layouts. Tester text has better contrast and readable mobile inputs. Fixed feedback reports losing their line breaks. Synchronised the previously outdated generated HTML copies and download portal. Included the approved image in Android's bundled assets so it is available offline on the next build.

Existing v0.62 APK downloads are unchanged; a new APK release is outside this web branding pass. The protected 24/7 demo remains unchanged.

Validation: inline parser, release/copy parity and protected-demo checks passed locally. Local browser execution is unavailable in this sandbox; the Home and tester branding checks workflow runs the existing project regression and Chromium/WebKit layout/feedback checks. Inspect that workflow and its previews before merging. The standard PR gate also runs the full regression suite and Android build.

## Motion refinement

Sharper asymmetric frames, metallic lime wordmark, compact mobile hero, and unified panel/card surfaces. Ambient header light sweep, slow technical rings, a four-step workflow light sequence and button sheen add restrained motion. Original approved artwork is unchanged.

The shared Motion toggle persists across Home and the tester portal. OS and in-app reduced-motion preferences take priority. Effects stop offscreen and pause when the browser tab is hidden; no per-frame JavaScript, new dependencies or drawing data changes. Browser review covers toggle persistence and reduced-motion changes as well as the established layout/project/feedback checks.
