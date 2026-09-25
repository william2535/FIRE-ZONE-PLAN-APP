# Project Pineapple — Live Checkpoint

Durable handoff for the ongoing Pineapple work. Update before risky edits and after meaningful CI/results so work can resume immediately after a crash.

## START HERE

Read `/PROJECT_PINEAPPLE_START_HERE.md` first. It is the short, obvious entry point for Operation Pineapple.

## Branch / live web / safety

- Development branch: `project-pineapple-v058`
- Stable web branch: `main`
- **Current live web milestone:** `89eee3561d652f510458a172151d1d1cdb849dfd`
- Milestone PR: `#3 — Publish Pineapple v0.58 web milestone`
- Exact release-gate checkpoint before merge: `5f4ec568487216648151f1cc84f0a6283649c2d8`
- Protected 24/7 build must remain unchanged.

## Current objective

Continue v0.58 Circuit Builder/manual-editor hardening autonomously while preserving accepted Smart Route/capture behaviour. Save continuously to Pineapple. Promote only coherent green major milestones to `main` for real-device web testing.

## First formal web milestone — DEPLOYED

**Pineapple v0.58 — Manual Editor Core Green** was promoted to `main` at:

`89eee3561d652f510458a172151d1d1cdb849dfd`

Before promotion, checkpoint `5f4ec568487216648151f1cc84f0a6283649c2d8` passed all three normal Pineapple release lanes:

- manual editor: PASS
- routing compatibility: PASS
- aggressive-touch / capture transition: PASS

The Pineapple release checks also preserve:

- protected 24/7 verification: PASS
- inline JavaScript parser: PASS
- clean browser startup: PASS
- generated app-copy equality: PASS
- visible browser/app title: v0.58

## Green foundations

- Former parser crash is fixed. Root cause was `cbEditAnchorAt()` missing the brace closing its outer leg loop before `return best`.
- Parser repair commit: `2a35764842c87fa897064b0d9a2e7117f9b5923a`.
- Browser startup reaches the normal ready state with editor controls mounted.
- Routing compatibility remains green.
- Aggressive-touch / capture transition remains green.
- Generated app copies remain synchronized by Pineapple checks.

## Manual editor milestone — GREEN

The manual-editor regression covers:

1. persisted draft-first edit session;
2. Pencil replacement staging;
3. Bin committing the staged replacement;
4. actual route-coordinate change;
5. local bridge bookkeeping;
6. explicit `ROUTE OPEN` state after local deletion;
7. Undo restoring connectivity;
8. Redo restoring the gap;
9. Done rejecting an open route;
10. Undo repairing the route;
11. validation passing on the repaired route;
12. Done successfully committing the repaired route and clearing the draft;
13. cleanup remaining orthogonal and non-increasing in complexity;
14. Smart Route compatibility and generated-copy equality.

## Bridge coordinate defect — repaired

A genuine app bug was confirmed in Bridge mode:

`conflict.crossings.map(h => ({ point: cbPxBoard(h.point, w, h), ... }))`

The callback parameter `h` shadowed the numeric canvas-height argument `h`, so a crossing object could be passed to `cbPxBoard()` where height was expected.

The generated app and generator source now use:

`conflict.crossings.map(hit => ({ point: cbPxBoard(hit.point, w, h), ... }))`

This preserves the real canvas height during coordinate conversion.

## NEXT EXACT STEP

1. Continue from `project-pineapple-v058`, not `main`.
2. Add a dedicated real-crossing Bridge regression rather than relying only on source inspection.
3. Prove bridge markers are finite and survive staged replacement, splice commit, Done/save, reopen and redraw.
4. Break-test manual editing across:
   - small iPhone portrait;
   - larger iPhone portrait;
   - typical Android phone;
   - small tablet;
   - landscape/desktop;
   - zoomed in/out;
   - fast, shaky, diagonal and awkward input.
5. Keep editor/routing/capture/protected-24-7/generated-copy gates green.
6. When the next coherent feature set is green, publish a new major milestone to `main` and replace the live-web SHA in START HERE and this checkpoint.

## Continuous-save rule

- Save every meaningful logical change to `project-pineapple-v058` continuously.
- Commit before risky structural edits.
- Update this checkpoint whenever the active blocker, CI outcome, known-good commit or next exact step changes materially.
- Update `/PROJECT_PINEAPPLE_START_HERE.md` at major milestones so a new session has one obvious entry point.
- Prefer small reproducible commits/patchers over broad unsaved changes.
- Never leave a long investigation existing only in chat state.

## Web milestone rule

At each major milestone:

1. require relevant Pineapple tests to be green;
2. require protected 24/7 verification to stay green;
3. require generated app copies to agree;
4. promote/merge the known-good milestone to `main`;
5. record the exact deployed `main` SHA in START HERE and this checkpoint;
6. return experimental work to the Pineapple branch.

Do not publish every diagnostic commit to the web app; publish coherent, usable milestones.
