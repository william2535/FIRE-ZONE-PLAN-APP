# Project Pineapple — Live Checkpoint

This file is the durable handoff for the ongoing Pineapple work. Update it at every meaningful milestone, before risky edits, and after important CI results so work can resume immediately after a chat/tool crash.

## Current branch

- Branch: `project-pineapple-v058`
- Current head before this checkpoint update: `1bb19696b7509779deedb4e66b45eecc9b5e7815` — `Checkpoint post-repair editor startup gate`
- Protected 24/7 build must remain unchanged.

## Current objective

Continue v0.58 Circuit Builder/manual-editor hardening autonomously. Preserve accepted Smart Route/capture behaviour while making editing predictable and professional.

## Parser/startup status

The former inline-JS parser break is repaired.

- Root cause: `cbEditAnchorAt()` was missing the brace closing its outer leg loop before `return best`.
- Repair commit: `2a35764842c87fa897064b0d9a2e7117f9b5923a` — `Fix manual editor anchor parser break`
- Current parser gate: PASS.
- Startup assertion was corrected in `b47d492d3c69856c728e907539edb0a38d6b4d2d` so it checks the actual mounted editor controls rather than expecting IIFE-local functions to be globals.
- Fresh startup on run `36196440655`: PASS with `ready:true` and `hasEditorUi:true`.

## Fresh CI on `1bb1969...`

- Capture transition run `36196440708`: PASS
- Routing compatibility run `36196440741`: PASS
- Manual editor run `36196440655`: FAIL only in `Run draft-first manual editor behaviour`
- Protected 24/7: PASS
- Inline parser: PASS
- Chromium/startup: PASS

### First real manual-editor failure

Job `108273247903` fails at `tests/circuit-manual-editor-v058.cjs` line 44:

`AssertionError: local leg geometry should actually change`

The assertion compares only the route point count before and after the Pencil/Bin splice. It observed `6` before and `6` after.

This is not sufficient evidence that the reroute failed: a legitimate replacement can keep the same number of orthogonal vertices while changing their coordinates. The editor successfully staged the replacement and `cbEditSplicePending()` cleared the pending state before this assertion.

## Immediate next step

1. Strengthen the regression so it snapshots the actual leg geometry before the splice and compares coordinates after the splice, rather than comparing only `.points.length`.
2. Log before/after geometry in CI so a genuine no-op is obvious.
3. Rerun manual-editor CI and follow the first genuine behavioural failure.
4. Once the splice regression advances, verify the existing bridge-locality assertions and then audit the suspected Bridge coordinate bug in `cbEditFinishStroke()`:
   - current callback appears to use `conflict.crossings.map(h=>({point:cbPxBoard(h.point,w,h),...}))`
   - callback variable `h` shadows the canvas-height parameter `h`, so Bridge mode may pass the crossing object as height.
   - confirm via behaviour/test before patching.
5. Keep capture/routing/24-7/generated-copy gates green throughout.

## Existing editor work that must be preserved

- Pencil/Bin replacement workflow
- explicit route-open state and Done rejection
- Undo/Redo
- persisted `editDraft`
- Bridge rendering / As-Fit integration
- cleanup control
- bridge-locality fix so deleting one segment does not remove unrelated bridge markers on the same leg

## Pineapple continuity rule

- Save meaningful progress to the branch continuously.
- Update this checkpoint before risky structural edits.
- Update it again after important CI outcomes or whenever the active blocker changes.
- Prefer small reproducible commits/patchers over unsaved broad changes.
- Never leave a long investigation existing only in chat state.
