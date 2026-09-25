# Project Pineapple — Live Checkpoint

Durable handoff for the ongoing Pineapple work. Update before risky edits and after meaningful CI/results so work can resume immediately after a crash.

## Branch / safety

- Branch: `project-pineapple-v058`
- Current app/checkpoint head before this update: `3559785531b8469c234019c626ae862a97ddac52`
- Protected 24/7 build must remain unchanged.

## Current objective

Continue v0.58 Circuit Builder/manual-editor hardening autonomously while preserving accepted Smart Route/capture behaviour.

## Repaired / green foundations

- Former parser crash is fixed. Root cause was `cbEditAnchorAt()` missing the brace closing its outer leg loop before `return best`.
- Repair commit: `2a35764842c87fa897064b0d9a2e7117f9b5923a`.
- Startup test now checks mounted editor UI instead of expecting IIFE-local functions to be globals (`b47d492d3c69856c728e907539edb0a38d6b4d2d`).
- Current parser gate: PASS.
- Current startup gate: PASS (`ready:true`, `hasEditorUi:true`).
- Capture transition on head `3559785...`: PASS, run `36196724926`.
- Routing compatibility on head `3559785...`: PASS, run `36196724831`.
- Protected 24/7 verification: PASS.

## Manual editor status

Manual editor run `36196724917`, job `108274138339`, is the only red gate.

The strengthened regression in `f211c886a1f891ee40b5fa462254ec40853e92af` now compares actual leg coordinates rather than point count. That improved test advances past the Pencil/Bin splice, proving the staged replacement genuinely changes route geometry.

Bridge-locality checks also advance: deleting one local segment preserves an unrelated bridge on the same leg, and Undo restores both bridge markers.

Open-route state also advances:

1. direct deletion creates one explicit gap and `ROUTE OPEN` status;
2. Undo restores zero gaps;
3. Redo restores the gap;
4. Done correctly rejects the open route;
5. Undo is then used to repair the route.

### Current exact failure

After that final Undo, the test calls `cbEditValidateDraft()` and its assertion passes (`ok:true`). Immediately afterwards `cbEditDone()` returns `false`:

`AssertionError: Done should accept repaired route` (`false !== true`).

`cbEditDone()` can return false only when either:

- `cbEdit?.active` is false; or
- its own second call to `cbEditValidateDraft()` returns non-ok.

Because an explicit validation immediately before Done is green, the next diagnostic must capture edit-active state + validation + Done result atomically in one browser execution, rather than weakening validation.

## Immediate next steps

1. Instrument `tests/circuit-manual-editor-v058.cjs` with a single atomic helper around the final Done call returning:
   - `activeBefore`
   - `validationBefore`
   - `result`
   - `activeAfter`
   - draft/gap summary before/after.
2. Run manual-editor CI and identify whether edit mode is being cleared asynchronously or the validator changes inside `cbEditDone()`.
3. Fix the actual runtime-state cause; do not loosen `cbEditValidateDraft()`.
4. Re-run full manual editor + Smart Route compatibility + capture + 24/7 + generated-copy equality.
5. Then test the separate suspected Bridge bug in `cbEditFinishStroke()` where `conflict.crossings.map(h=>({point:cbPxBoard(h.point,w,h),...}))` shadows canvas height `h`; confirm via behaviour test before patching.

## Editor work to preserve

- Pencil/Bin replacement workflow
- explicit route-open state and Done rejection
- Undo/Redo
- persisted `editDraft`
- Bridge rendering / As-Fit integration
- cleanup control
- bridge-locality fix

## Pineapple continuity rule

- Save meaningful progress to this branch continuously.
- Update this checkpoint before risky structural edits and after important CI outcomes.
- Prefer small reproducible commits/patchers over broad unsaved changes.
- Never leave a long investigation existing only in chat state.
