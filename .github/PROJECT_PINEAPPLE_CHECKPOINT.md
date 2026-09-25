# Project Pineapple — Live Checkpoint

This file is the durable handoff for the ongoing Pineapple work. Update it at every meaningful milestone, before risky edits, and after important CI results so work can resume immediately after a chat/tool crash.

## Current branch

- Branch: `project-pineapple-v058`
- Protected 24/7 build must remain unchanged.

## Current objective

Continue the v0.58 Circuit Builder / manual editor hardening work without waiting for repeated user prompts. The target is a polished, predictable routing/editor system, not a narrow threshold patch.

## What is already established

- Aggressive-touch / capture-transition work had been accepted sufficiently to move on to manual editor hardening.
- The branch already contains a real manual editor implementation rather than just UI: Edit, Pencil/Bin, Undo/Redo, Bridge, Cleanup, Done validation, persisted `editDraft`, As-Fit blocking for unfinished edits, bridge rendering, staged replacement/splice, and crossing/overlap validation.
- A concrete editor defect was found: deleting one local cable section could remove bridge metadata too broadly on the same detector-to-detector leg.
- Bridge-locality regression work and local bridge bookkeeping changes are already on the branch and must be preserved.

## Current blocker

The manual-editor branch currently contains malformed inline JavaScript and cannot initialize the app.

Observed failure:

- `SyntaxError: Unexpected token ')'` at final `})();`
- Browser startup never reaches ready state.
- Protected 24/7 verification continues to pass.

## Confirmed baseline

### Last confirmed good app

`fcd59d236411c41e48383b774fbc632c4ebf0e16` — `Apply Pineapple v0.58 editor transformation`

CI on this SHA:
- Capture transition run `36191711835`: PASS
- Routing compatibility run `36191711836`: PASS
- Editor apply run `36191711987`: PASS and generated the editor commit.

### Generated editor commit under investigation

`c8b76b265702b6667fe780fca360c7e68393ce0a` — `Add manual Circuit Builder route editor core`

It changes the four app HTML copies and was generated from `.github/pineapple_v058_editor_patch.py`.

## Exact syntax isolation result

A deterministic hunk-by-hunk parser bisect was added:

- Script: `tests/circuit-editor-hunk-bisect-v058.py`
- Script commit: `502259a7477a377cb858ae99894365406bbc43c0`
- Workflow wiring commit: `230342111fe594d319873ffb6d17f629f86caca3`
- Manual editor workflow run: `36195630175`
- Job: `108270710594`

Result:

- Known-good `fcd59d...` parses cleanly.
- Original editor diff contains 8 hunks.
- Hunks 1–5: PASS.
- **Hunk 6 is the first syntax-breaking hunk.**
- Hunk header: `@@ -893,12 +899,57 @@ ...`
- This is the large editor-engine insertion beginning with `cbEditClone`, `cbEditBoardClose`, `cbEditSimplifyBoard`, `cbEditGapMatches`, `cbEditDraft`, `cbEditVisibleSegments`, `cbEditEnsureDraft`, etc., around the `cbLegSegments` / board-routing area.
- Failure immediately after applying hunk 6: final `})();` gives `Unexpected token ')'`.
- Normal parser gate reproduces the same failure.

Important correction: do not blame the landing-page or `cbOpenCircuit` replacement first; those are in earlier/later hunks and hunks 1–5 already parse. The syntax fault is inside hunk 6 itself.

## Immediate next steps

1. Split hunk 6 into smaller function-level chunks and run syntax checking after each group to identify the exact malformed editor function/block.
2. Fix the reproducible editor patch source rather than hand-editing four HTML copies where possible.
3. Apply a small repair to the current branch while preserving later bridge-locality/editor improvements.
4. Re-run:
   - inline script parser
   - browser startup
   - manual editor behaviour + bridge locality
   - Smart Route compatibility
   - capture/aggressive-touch/return-magnet gates
   - protected 24/7 verification
   - generated-copy equality
5. Once green, continue deliberate break-testing of Pencil splice anchors, bridge persistence, undo/redo topology, cleanup strength, Done/open-route validation, As-Fit, and phone/tablet behaviour.

## Pineapple continuity rule

- Save meaningful progress to the branch continuously.
- Update this checkpoint before risky structural edits.
- Update it after important CI outcomes or whenever the active blocker changes.
- Prefer small reproducible patch/generator commits over unsaved broad changes.
- Never leave a long investigation existing only in chat state.
