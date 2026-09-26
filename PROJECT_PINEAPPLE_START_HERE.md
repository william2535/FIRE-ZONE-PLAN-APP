# 🍍 OPERATION PINEAPPLE — START HERE

**If you are resuming this project after a chat reset, tool crash, or time away: start with this file.**

## Current working branch

`project-pineapple-v058`

Do **not** start by guessing from old chat messages. Read this file, then read `.github/PROJECT_PINEAPPLE_CHECKPOINT.md`, then inspect the latest CI for the branch head.

## Latest deployed major milestone

**Pineapple v0.58 — Manual Editor Core Green**

Stable web branch: `main`

Core web-app milestone merge:

`89eee3561d652f510458a172151d1d1cdb849dfd`

Milestone PR: `#3 — Publish Pineapple v0.58 web milestone`

The exact pre-merge Pineapple checkpoint that passed the original release gates was:

`5f4ec568487216648151f1cc84f0a6283649c2d8`

The v0.58 manual editor includes Pencil, Bin, Undo, Redo, Bridge, Cleanup and Done, with persisted edit drafts and As-Fit protection while a route is open.

## Latest known-green development hardening point

`3f1d1ebb91fca27824fd4ad0cbc8c0cf829366ff`

On that exact development checkpoint:

- manual editor lane: PASS
- routing compatibility lane: PASS
- aggressive-touch / capture transition lane: PASS
- protected 24/7 verification: PASS
- inline parser and browser startup: PASS
- dedicated real-crossing Bridge persistence regression: PASS
- Manual Edit mobile stress: PASS
- Smart Route compatibility: PASS
- generated HTML copy equality: PASS

The real Bridge regression proves finite crossing coordinates survive staged replacement, splice, Done/save, reopen and redraw.

The mobile stress harness covers tiny/small/large iPhone-sized viewports, Android phone, small tablet and orientation changes. Its fixture now validates itself before testing so a broken synthetic setup cannot masquerade as an app regression.

## LIVE WEB STATE

- **CORE WEB APP:** `main/index.html` = v0.58 with the manual editor present.
- **BETA PORTAL DELIVERY FIX:** PR `#5`, merged as `34af3e5737c2b1607c09073904df6c69dad373cb`.
- **FRESH UNCACHED WEB LAUNCHER:** `main/web-v058.html`.
- Fresh-launch PR: `#6 — Publish fresh v0.58 web launcher`.
- Fresh-launch main commit: `406dfdcc0bec0507825a0da9635147975b9bd7b1`.
- Public real-device entry point: `https://william2535.github.io/FIRE-ZONE-PLAN-APP/web-v058.html`.
- `web-v058.html` redirects to `index.html?pineapple=v058&fresh=<timestamp>` on every load, deliberately defeating reuse of an older v0.57 document.
- The portal explicitly shows **Web v0.58 · Android v0.57**.
- The current packaged Android release remains **v0.57** until a separate v0.58 APK is built and released.
- **DEVELOPMENT / CONTINUOUS SAVE:** `project-pineapple-v058`.

### Delivery verification already performed

The GitHub Pages deployment artifact for the v0.58 site was inspected and contained:

- `index.html` titled v0.58;
- `cbEditToggle`;
- `cbEditBar`;
- `cbEditBridge`;
- the full manual-editor code;
- `beta.html` labelled Web v0.58 / Android v0.57.

Therefore, if an old bookmark/tab still shows v0.57 or lacks the editor, do **not** diagnose the repo from that tab. First open the fresh `web-v058.html` entry point above.

## Branch divergence warning

Before the next publication, reconcile `project-pineapple-v058` with current `main`.

At the 2026-09-26 hardening checkpoint the Pineapple branch was **6 commits behind `main`**. Those `main` changes include delivery/version-launcher work that must not be accidentally discarded by a future promotion.

## NEXT EXACT STEP

1. Continue on `project-pineapple-v058`, not `main`.
2. Deepen Manual Edit stress with **committed** Pencil/Bin edits using fast, shaky, diagonal and direction-changing touch paths — the current mobile stress pass mainly proves controls, cancellation, mode switching and resize/orientation safety.
3. Add explicit zoomed-in and zoomed-out Manual Edit coverage for coordinate conversion and hit tolerances.
4. Keep Bridge persistence, Smart Route, routing, capture, protected-24/7 and generated-copy gates green.
5. Before the next coherent web milestone, reconcile the branch with current `main`, rerun all gates, then promote only the known-good result.
6. After any future promotion, verify GitHub Pages, `index.html`, `beta.html`, visible version labels and the fresh launcher together.

## Continuous-save rule

Operation Pineapple must never rely on chat state alone.

- Commit every meaningful logical change to `project-pineapple-v058` as it is completed.
- Commit before risky structural edits.
- Update `.github/PROJECT_PINEAPPLE_CHECKPOINT.md` whenever the active blocker, test result, deployment result or next step changes materially.
- Keep this START HERE file short and current: working branch, live-web state, latest known-good milestone/development checkpoint and next exact step.
- Prefer small reproducible changes over one giant unsaved edit.
- Never leave a long investigation only in conversation history.

## Web milestone rule

The web app is a **milestone surface**, not the scratch branch.

When a major milestone is reached:

1. all relevant Pineapple CI must be green;
2. protected 24/7 verification must remain green;
3. generated app copies must agree;
4. reconcile current `main` into the development line if the branches have diverged;
5. publish/merge the known-good milestone to `main`;
6. verify the actual Pages deployment/run and, where practical, its built artifact;
7. verify `index.html`, `beta.html`, visible version labels and launch URLs;
8. publish/update a version-specific fresh launcher for real-device testing;
9. immediately record the deployed web state here and in the checkpoint;
10. continue experimental work on the Pineapple branch rather than using the live web app as the scratchpad.

Do **not** publish every tiny diagnostic/test-only commit to the web app.

## Safety invariant

The protected 24/7 company/demo build must remain unchanged unless the user explicitly asks to change it.
