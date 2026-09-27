# Project Pineapple — Live Checkpoint

Durable handoff for the ongoing Pineapple work. Update before risky edits and after meaningful CI/results so work can resume immediately after a crash.

## START HERE

Read `/PROJECT_PINEAPPLE_START_HERE.md` first. It is the short, obvious entry point for Operation Pineapple.

## Branch / live web / safety

- Development branch: `project-pineapple-v058`
- Stable web branch: `main`
- Current live web milestone remains Pineapple v0.58.
- Core milestone merge: `89eee3561d652f510458a172151d1d1cdb849dfd`
- Exact original release-gate checkpoint: `5f4ec568487216648151f1cc84f0a6283649c2d8`
- Protected 24/7 build must remain unchanged.
- Current `main` history through `37bb435ad82ef48d7cecf5d1da29231631af4140` was reconciled into Pineapple as `4e7cf392d35d962923cba4c859fd66eb9824ca2a`; check again for later divergence before future publication.

## Reconciliation completed — 27 September 2026

- The latest two main-only commits added a one-shot visible-version hotfix and then removed it after correcting the four app copies. Pineapple had independently made the same three visible v0.58 text corrections.
- The merge tree equals the preceding Pineapple tree byte for byte. No app, beta portal, fresh launcher, Android package or protected 24/7 content changed in the merge.
- GitHub CI on the exact remote merge commit passed: manual editor `36331032811`, routing compatibility `36331032678`, capture transition `36331032776`.
- The manual editor lane includes protected 24/7 verification, parser/startup, real Bridge crossing, mobile stress, committed 1× and 6× route surgery, Smart Route compatibility and generated-copy equality.
- Local parser and protected build checks passed. Local browser tests could not start because this workspace could not download Playwright Chromium; the three GitHub CI lanes supply the browser results.

## Latest known-green development checkpoint

**TESTED APP/TEST HEAD:** `4e7cf392d35d962923cba4c859fd66eb9824ca2a` (reconciled merge; same app/test tree as `7b0ed951fb758d05090d5bc364472bd493239b61`)

All three Pineapple lanes passed on this exact head:

- manual editor: PASS
- routing compatibility: PASS
- aggressive-touch / capture transition: PASS

The editor lane additionally passed:

- protected 24/7 verification
- inline JavaScript parser
- clean browser startup
- draft-first manual editor behaviour
- dedicated real Bridge crossing persistence
- Manual Edit mobile stress across 320×568, 375×667, 430×932, 412×915 and 768×1024 viewports plus orientation changes
- committed rough Pencil → Bin splice at 1× zoom
- committed shaky/direction-changing Pencil → Bin splice at 6× zoom
- Cleanup extremes and mode switching
- touch cancellation cleanup
- Smart Route compatibility
- generated app-copy equality

## Hardening completed

### Dedicated real-crossing Bridge regression — GREEN

`tests/circuit-bridge-crossing-v058.cjs` proves a real crossing is rejected with Bridge OFF, accepted with Bridge ON, keeps finite bridge coordinates, survives staged replacement/splice, Done/save, reopen and redraw.

### Multi-viewport Manual Edit stress — GREEN

`tests/circuit-editor-mobile-stress-v058.cjs` covers tiny/small/large iPhone sizes, Android phone, small tablet, orientation changes, real control hit boxes, overflow, rapid mode changes, Cleanup extremes, touch cancellation and Done/save.

### Committed gesture + zoom regression — GREEN

`tests/circuit-editor-gesture-zoom-v058.cjs` now proves Manual Edit can perform real saved route surgery rather than cancellation-only interaction:

1. at 1× zoom, a sparse/fast rough Pencil gesture stages a replacement;
2. Bin hits the intended old cable segment and commits the splice;
3. resulting geometry is finite, orthogonal, materially changed, valid and saveable;
4. at 6× zoom, a larger shaky/direction-changing gesture follows the same full Pencil → Bin → validate → Done path;
5. both scenarios preserve the expected device-to-device leg structure.

### False alarms deliberately separated from product defects

During harness development we caught and corrected test/setup mistakes instead of patching the app blindly:

- wrong Cleanup selector (`#cbEditOptionsPanel` vs `.cbEditOptionsPanel` inside `#cbEditOptions`);
- synthetic PointerEvents needing test-only pointer-capture stubs;
- a seeded duplicate elbow creating a zero-length segment;
- a 6× rough gesture that legitimately cleaned back to the original straight route, making a “geometry changed” assertion invalid until the fixture was made materially distinct.

No product-code change was made for these harness defects.

## Green foundations retained

- Parser/startup remain green.
- Manual editor Pencil/Bin splice, gaps, Undo/Redo, ROUTE OPEN protection, Cleanup, Bridge and Done remain green.
- Routing compatibility remains green.
- Aggressive-touch / capture transition remains green.
- Smart Route compatibility remains green.
- Generated app copies remain synchronized.
- Protected 24/7 remains unchanged.

## Active pass — 27 September 2026: mobile editor interruption safety

Development branch: `project-pineapple-v058`. Starting checkpoint: `3fc08209f638d02ddfbde844706d1de39114ba2d`; current live milestone is web v0.58 / packaged Android v0.57.

Completed work from earlier passes: post-capture rubber-band fix, draft-first Pencil/Bin/Bridge/Cleanup/Done editor, real Bridge persistence, mobile/zoom gesture stress, and reconciliation with main through `37bb435`. Do not redo those implementations. The historical requirements below remain acceptance criteria.

This active pass reproduced two production defects before changing code: view/app interruption left a live editor stroke/tap armed, and an out-and-back Bin drag was mistaken for a deliberate deletion tap. The baseline input-state regression failed 3 of 4 assertions. Both are fixed locally (4/4 pass), with explicit lost-pointer-capture recovery and mode-specific hints added. Earlier staged replacements are preserved.

Second audit: reproduced and fixed a stale LOOP CLOSED counter while the editor has an open route; it now follows EDITING / ROUTE OPEN / REPLACEMENT READY. Local production-function regression is 5/5. First browser run on `a2a4b5c8` passed the interruptions and 30 history cycles but failed reload because the synthetic fixture had no named project; the fixture now uses the real project activation path. Prior editor/Bridge/mobile/zoom tests remained green.

Third audit: on `46ca44a6`, the editor/routing/capture lanes and new WebKit interruption/reload test passed. Full suite had only the pre-existing v0.58 title allow-list failure. Reproduced two further lifecycle defects: switching circuits retained the old editor session, and a confirmed survey rebuild retained obsolete editDraft/bridges. Both fixed; local production-function checks 7/7. Circuit list completion ticks now respect editing status. Browser regression extended to switch away/back and rebuild.

Validation pending: new Chromium/WebKit interruption/30-cycle/save-reload/As-Fit regression, full serial suite (now including all v0.58 editor gates), Android build, visual audit and second fresh-eyes pass. No new public milestone yet. If interrupted, inspect current branch CI and fix failures before promotion; do not describe this as the premium loop being complete.

Continuation rule confirmed by Will: keep making useful improvements within the session after the first green CI run, and update this brief, NEXT_PROMPT, START_HERE and the checkpoint at meaningful steps. Do not end a pass merely by recording an unspecified future task.

## NEXT EXACT STEP

1. Continue from `project-pineapple-v058`; reconciliation with `main` through `37bb435` and its three CI lanes are complete.
2. Select a concrete mobile/editor improvement from real-device feedback and make a small reproducible product change.
3. Run relevant Pineapple gates, generated-copy equality and protected 24/7 verification on the changed head.
4. Publish only a coherent usable product milestone, then verify `index.html`, `beta.html`, visible version labels, fresh launcher and Pages together.

## Continuous-save rule

- Save every meaningful logical change to `project-pineapple-v058` continuously.
- Commit before risky structural edits.
- Update this checkpoint whenever the active blocker, CI outcome, known-good commit or next exact step changes materially.
- Update `/PROJECT_PINEAPPLE_START_HERE.md` when the handoff/next step materially changes or at major milestones.
- Prefer small reproducible changes over broad unsaved changes.
- Never leave a long investigation existing only in chat state.

## Web milestone rule

At each major milestone:

1. require relevant Pineapple tests to be green;
2. require protected 24/7 verification to stay green;
3. require generated app copies to agree;
4. reconcile current `main` into development if branches have diverged;
5. promote only a known-good coherent milestone to `main`;
6. record exact deployed `main` SHA;
7. verify Pages deployment/artifact where practical;
8. verify `index.html`, `beta.html`, visible version labels and launch URLs together.

Do not publish every diagnostic/test-only commit to the web app.
