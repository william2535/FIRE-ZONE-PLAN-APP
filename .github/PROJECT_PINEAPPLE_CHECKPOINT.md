# Project Pineapple — Live Checkpoint

Durable handoff for the ongoing Pineapple work. Update before risky edits and after meaningful CI/results so work can resume immediately after a crash.

## START HERE

Read `/PROJECT_PINEAPPLE_START_HERE.md` first. It is now the short, obvious entry point for Operation Pineapple.

## Branch / safety

- Branch: `project-pineapple-v058`
- Latest known-good app milestone before the new handoff docs: `6fbd5639df51c6b2b6be892a104c210df47519c2`
- Protected 24/7 build must remain unchanged.
- `main` is the stable web-milestone surface; Pineapple is the continuous development/checkpoint branch.

## Current objective

Continue v0.58 Circuit Builder/manual-editor hardening autonomously while preserving accepted Smart Route/capture behaviour. Save continuously, and promote coherent green milestones to the live web app on `main`.

## Green foundations

- Former parser crash is fixed. Root cause was `cbEditAnchorAt()` missing the brace closing its outer leg loop before `return best`.
- Parser repair commit: `2a35764842c87fa897064b0d9a2e7117f9b5923a`.
- Browser startup now reaches the normal ready state with editor controls mounted.
- Routing compatibility: PASS on the repaired editor build.
- Aggressive-touch / capture transition: PASS on the repaired editor build.
- Protected 24/7 verification: PASS.
- Generated app copies remain synchronized by the Pineapple checks.

## Manual editor milestone — GREEN

The full manual-editor lane reached green on commit:

`6fbd5639df51c6b2b6be892a104c210df47519c2`

The regression now successfully covers:

1. entering a persisted draft-first edit session;
2. Pencil replacement staging;
3. Bin committing the staged replacement;
4. actual route-coordinate change, not merely point-count change;
5. local bridge bookkeeping (deleting one section preserves unrelated bridges on the same leg);
6. explicit `ROUTE OPEN` state after local deletion;
7. Undo restoring connectivity;
8. Redo restoring the gap;
9. Done correctly rejecting an open route;
10. Undo repairing the route;
11. validation passing on the repaired route;
12. Done successfully committing the repaired route and clearing the draft;
13. cleanup strength remaining orthogonal and non-increasing in complexity;
14. Smart Route compatibility and generated-copy equality in the same editor lane.

The final apparent Done failure was test-only: successful `delete cbCircuit.editDraft` produces an absent/undefined property, while the regression expected literal `null`. The assertion now checks that no draft exists.

## Bridge coordinate defect — repaired

A genuine app bug was confirmed in Bridge mode:

`conflict.crossings.map(h => ({ point: cbPxBoard(h.point, w, h), ... }))`

The callback parameter `h` shadowed the numeric canvas-height argument `h`, so a crossing object could be passed to `cbPxBoard()` where height was expected.

The current generated app and generator source now use:

`conflict.crossings.map(hit => ({ point: cbPxBoard(hit.point, w, h), ... }))`

This preserves the real canvas height during coordinate conversion.

## Immediate next steps

1. Add a dedicated real-crossing Bridge regression rather than relying only on source inspection.
2. Prove bridge marker coordinates are finite and survive:
   - staged replacement;
   - splice commit;
   - Done/save;
   - reopen/redraw.
3. Break-test manual editing across phone/tablet sizes, zoomed in/out, fast/shaky input and awkward anchor returns.
4. Keep routing/capture/24-7/generated-copy gates green.
5. Treat the current editor-core-green state as a major milestone and publish it to `main` once its stale visible v0.57 label is corrected to v0.58.

## Continuous-save rule

- Save every meaningful logical change to `project-pineapple-v058` continuously.
- Commit before risky structural edits.
- Update this checkpoint whenever the active blocker, CI outcome, known-good commit or next exact step changes materially.
- Update `/PROJECT_PINEAPPLE_START_HERE.md` at major milestones so a new session has one obvious entry point.
- Prefer small reproducible commits/patchers over broad unsaved changes.
- Never leave a long investigation existing only in chat state.

## Web milestone rule

At each major milestone:

1. require the relevant Pineapple tests to be green;
2. require protected 24/7 verification to stay green;
3. require generated app copies to agree;
4. promote/merge that known-good milestone to `main` for real-device web testing;
5. record the deployed `main` commit in START HERE and this checkpoint;
6. return experimental work to the Pineapple branch.

Do not publish every diagnostic commit to the web app; publish coherent, usable milestones.
