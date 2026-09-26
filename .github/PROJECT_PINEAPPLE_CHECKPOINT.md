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
- Do not promote the development branch blindly: at the 2026-09-26 hardening checkpoint it was still **6 commits behind `main`** and must be reconciled with current `main` before any future milestone publication.

## Current objective

Continue v0.58 Circuit Builder/manual-editor hardening autonomously while preserving accepted Smart Route/capture behaviour. Save continuously to Pineapple. The real-crossing Bridge regression and first multi-viewport Manual Edit stress pass are now complete and green.

## Latest known-green development checkpoint

`3f1d1ebb91fca27824fd4ad0cbc8c0cf829366ff`

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
- Cleanup extremes and mode switching
- touch cancellation cleanup
- Smart Route compatibility
- generated app-copy equality

## What was hardened in this pass

### Dedicated real-crossing Bridge regression — GREEN

`tests/circuit-bridge-crossing-v058.cjs` now proves:

1. a genuine crossing is rejected with Bridge OFF;
2. the same crossing is accepted with Bridge ON;
3. bridge marker coordinates are finite;
4. bridge metadata survives staged replacement and splice commit;
5. Done/save succeeds;
6. the saved circuit can be reopened and redrawn with the bridge intact.

This protects the repaired Bridge coordinate-shadowing defect where a crossing callback previously shadowed numeric canvas height `h`.

### Multi-viewport Manual Edit stress harness — GREEN

`tests/circuit-editor-mobile-stress-v058.cjs` now covers:

- tiny iPhone: 320×568
- small iPhone: 375×667
- large iPhone: 430×932
- typical Android: 412×915
- small tablet: 768×1024
- portrait → landscape → portrait resizing
- real control hit boxes and viewport overflow
- rapid Pencil/Bin and Bridge mode switching
- Cleanup 0 / 100 / 45 states
- pointer cancellation and stale-pointer cleanup
- Done/save after the stress sequence

Two false alarms in the new harness were explicitly corrected instead of being misdiagnosed as app bugs:

1. Cleanup is `.cbEditOptionsPanel` inside `#cbEditOptions`; the first harness revision incorrectly looked for a nonexistent `#cbEditOptionsPanel` ID.
2. JavaScript-created PointerEvents are not real browser-active pointers, so the harness now follows the existing repo convention of stubbing pointer capture for synthetic touch input.
3. The original seeded orthogonal route could create a duplicate elbow on a horizontally aligned leg; fixture legs now pass through `cbEditSimplifyBoard()` and the harness asserts the seeded route is valid before any stress action.

These were test-harness defects. No unnecessary product-code change was made for them.

## Green foundations retained

- Parser repair remains green.
- Browser startup reaches the normal ready state with editor controls mounted.
- Routing compatibility remains green.
- Aggressive-touch / capture transition remains green.
- Generated app copies remain synchronized.
- Protected 24/7 remains unchanged.
- Manual editor Pencil/Bin splice, gaps, Undo/Redo, ROUTE OPEN protection, Cleanup, Bridge and Done remain green.

## NEXT EXACT STEP

1. Continue from `project-pineapple-v058`, not `main`.
2. Deepen Manual Edit gesture stress beyond cancellation-only input: committed Pencil edits and Bin operations under fast, shaky, diagonal and direction-changing touch paths.
3. Add explicit zoomed-in and zoomed-out Manual Edit coverage so coordinate conversion and hit tolerances are tested at realistic extremes.
4. Preserve Bridge persistence, Smart Route, routing, capture, generated-copy and protected-24/7 gates while doing this.
5. Before the next web milestone, reconcile the Pineapple branch with the current `main` because `main` has delivery/version-launcher commits not present in the branch.
6. Only after reconciliation and a completely green release gate should a coherent next milestone be promoted to `main`; then verify Pages, `index.html`, `beta.html`, visible versions and the fresh launcher together.

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
4. reconcile current `main` into the development line before promotion if the branches have diverged;
5. promote/merge the known-good milestone to `main`;
6. record the exact deployed `main` SHA in START HERE and this checkpoint;
7. verify the actual GitHub Pages deployment/run and, where practical, its artifact;
8. verify `index.html`, `beta.html`, visible version labels and launch URLs together.

Do not publish every diagnostic/test-only commit to the web app; publish coherent, usable milestones.
