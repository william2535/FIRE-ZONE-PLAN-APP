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
- Do not promote the development branch blindly: it still needs reconciliation with current `main` before any future milestone publication.

## Latest known-green development checkpoint

**TESTED APP/TEST HEAD:** `ea7b0255b6e01d195f36b286f4e69e909a83f12a`

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

## NEXT EXACT STEP

1. Continue from `project-pineapple-v058`, not `main`.
2. Inspect the exact commits/files that exist on current `main` but not Pineapple; do not assume they are delivery-only.
3. Reconcile `main` into Pineapple carefully, preserving both the green v0.58 editor/routing work and current live delivery/version-launcher changes.
4. Rerun all Pineapple gates after reconciliation and verify generated copies + protected 24/7.
5. Do **not** publish a new web milestone merely because tests were hardened; publish only when the resulting product change is a coherent usable milestone.
6. Before any future promotion, verify `index.html`, `beta.html`, visible version labels, fresh launcher and Pages together.

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
