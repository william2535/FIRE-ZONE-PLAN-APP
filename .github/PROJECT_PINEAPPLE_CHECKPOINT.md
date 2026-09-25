# Project Pineapple — Live Checkpoint

This file is the durable handoff for the ongoing Pineapple work. Update it at every meaningful milestone, before risky edits, and after important CI results so work can resume immediately after a chat/tool crash.

## Current branch

- Branch: `project-pineapple-v058`
- Last confirmed branch head before this checkpoint: `364ec3b01b734c636b09d4c96f74fd1e52b57bdf`
- Head commit message: `Trace exact unmatched editor brace boundary`
- Protected 24/7 build must remain unchanged.

## Current objective

Continue the v0.58 Circuit Builder / manual editor hardening work without waiting for repeated user prompts. The target is a polished, predictable routing/editor system, not a narrow threshold patch.

## What is already established

- Aggressive-touch / capture-transition work had been accepted sufficiently to move on to manual editor hardening.
- The branch already contains a real manual editor implementation rather than just UI:
  - Edit mode
  - Pencil / Bin
  - Undo / Redo
  - Bridge
  - Cleanup control
  - Done validation
  - persisted `editDraft`
  - As-Fit blocked while an unfinished edit exists
  - bridge rendering into As-Fit
  - staged replacement geometry followed by deleting the old span to splice it in
  - crossing/overlap validation
- A concrete editor defect was found: deleting one local cable section could remove bridge metadata too broadly on the same detector-to-detector leg.
- Bridge-locality regression work was added and bridge bookkeeping was changed so bridge markers are intended to be scoped to the edited geometric span/segment rather than the whole leg.

## Current blocker

The manual-editor CI is currently failing at inline JavaScript parsing before browser tests can run.

Observed failure:

- `SyntaxError: Unexpected token ')'` at the closing `})();`
- Parser reports an unclosed `{` inside the main app IIFE.
- The protected 24/7 build check still passes.
- The current syntax diagnostic commit is only diagnostic; do not treat its brace-depth trace as definitive where template literals can distort simple token-depth accounting.
- The wall merge routine around the first reported top-level-loss area was manually inspected and appears structurally balanced, so the next step is commit-level isolation rather than blindly adding a brace there.

## Useful recent commits / checkpoints

- `364ec3b01b734c636b09d4c96f74fd1e52b57bdf` — Trace exact unmatched editor brace boundary
- `6ad737dca8ee0dc352cdc4a39aa7e4ea8494c089` — Locate swallowed Circuit Builder function after missing brace
- `b2099a22b902c88b6e5cc93f6ab82d0407154bfb` — Fix manual editor UI synchronizer calls
- `b389823d868f7f6365283308ec8ac92d3ddaca31` — Scope bridge metadata to edited cable sections
- `f7a8bf2732c1e4b59be91d975b7612a713adb6cc` — Add bridge-locality regression to manual editor

## Latest CI evidence

Manual editor workflow on head `364ec3...`:

- Protected 24/7 verification: PASS
- `Parse inline JavaScript before browser startup`: FAIL
- Browser/editor behaviour tests: skipped because parse gate failed
- Smart Route compatibility: skipped because parse gate failed

The previous bridge-scope/editor commits were already failing editor CI, so the syntax break predates the newest diagnostic commit and must be isolated to the first green→red app change.

## Immediate next steps

1. Find the last manual-editor workflow run/commit where inline JS parsed successfully.
2. Compare that commit to the first failing commit and isolate the smallest app diff responsible for the unmatched block / swallowed function.
3. Fix the structural syntax issue without rolling back bridge-locality work.
4. Re-run:
   - inline script parse gate
   - manual-editor behaviour regression
   - bridge-locality regression
   - Smart Route compatibility
   - protected 24/7 verification
5. Once green, continue deliberate break-testing of the editor rather than rebuilding UI that already exists.

## Pineapple continuity rule

From this point onward:

- Save meaningful progress to the branch continuously.
- Update this checkpoint before risky structural edits.
- Update it again after important CI outcomes or when the active blocker changes.
- Prefer small reproducible patch/generator commits over unsaved broad changes.
- Never leave a long investigation existing only in chat state.
