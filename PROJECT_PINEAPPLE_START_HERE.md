Latest work: addressable return geometry, consistent drawing/As-Fit rendering and Restore return action. App source checkpoint `06fc5fd`; release evidence and final SHA: [PR #33](https://github.com/william2535/FIRE-ZONE-PLAN-APP/pull/33). See docs/CIRCUIT_BUILDER_CONTINUITY.md for tests and repair instructions.

# Intruder maps Stage 3 — current main task (1 October 2026)

Current Circuit Builder pass (1 October 2026): see the top checkpoint in `docs/CIRCUIT_BUILDER_CONTINUITY.md` for parallel cable lanes, touch recovery, partial-route editing and validation status.

Base inspected: deployed Stage 2 `adcec1d`. Security zone/device/run links, placed controller assignments, evidence, schedules and proposed-route comparison extend the shared editor and connection engine. See `docs/security-maps-stage3.md` for model, sources, checks and limits. The latest user instruction is Stage 3 only; Stage 4 and final integration are paused. Stop after Stage 3. These instructions supersede the historical tasks below.

# Access Control maps Stage 2 — current main task (1 October 2026)

Continues deployed Stage 1 `a732727`. Existing doors now carry stable equipment/evidence associations, map guides, cable-route editing and a compact schedule, using the shared editor and record states. See `docs/access-maps-stage2.md` for model, guidance, tests and limitations. This current-main Stage 2 request supersedes historical branch/stage instructions below. Stop after Stage 2.

# Current task — Maps and As-Fits Stage 1 (1 October 2026)

The user explicitly selected current `main` for this stage, superseding the historical development-branch instructions below. Stage 1 extends the shared editor with explicit record states, revision history and retained issued snapshots. See `docs/maps-asfit-stage1.md` for usage, model details, UK sources and limitations. Stop after this stage; do not begin subsequent feature stages.

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

**TESTED APP/TEST HEAD:** `4e7cf392d35d962923cba4c859fd66eb9824ca2a` (reconciled merge; same app/test tree as `7b0ed951fb758d05090d5bc364472bd493239b61`)

On that exact development checkpoint:

- manual editor lane: PASS
- routing compatibility lane: PASS
- aggressive-touch / capture transition lane: PASS
- protected 24/7 verification: PASS
- inline parser and browser startup: PASS
- dedicated real-crossing Bridge persistence regression: PASS
- multi-viewport Manual Edit stress: PASS
- committed rough Pencil/Bin splice at 1× zoom: PASS
- committed shaky/direction-changing Pencil/Bin splice at 6× zoom: PASS
- Smart Route compatibility: PASS
- generated HTML copy equality: PASS

The 1× and 6× gesture regression now performs actual saved route surgery: stage replacement → Bin old span → validate → Done. Test-fixture false alarms were corrected without unnecessary product-code changes.

## LIVE WEB STATE

- **CORE WEB APP:** `main/index.html` = v0.58 with the manual editor present.
- **BETA PORTAL DELIVERY FIX:** PR `#5`, merged as `34af3e5737c2b1607c09073904df6c69dad373cb`.
- **FRESH UNCACHED WEB LAUNCHER:** `main/web-v058.html`.
- Fresh-launch PR: `#6 — Publish fresh v0.58 web launcher`.
- Fresh-launch main commit: `406dfdcc0bec0507825a0da9635147975b9bd7b1`.
- Public real-device entry point: `https://william2535.github.io/FIRE-ZONE-PLAN-APP/web-v058.html`.
- `web-v058.html` redirects to `index.html?pineapple=v058&fresh=<timestamp>` on every load.
- The portal explicitly shows **Web v0.58 · Android v0.57**.
- The current packaged Android release remains **v0.57** until a separate v0.58 APK is built and released.
- **DEVELOPMENT / CONTINUOUS SAVE:** `project-pineapple-v058`.

## Reconciled development checkpoint

`main` at `37bb435ad82ef48d7cecf5d1da29231631af4140` was merged into Pineapple as `4e7cf392d35d962923cba4c859fd66eb9824ca2a` on 27 September 2026. The merge tree is identical to the prior Pineapple tree: the three visible v0.58 label corrections had already landed independently on both branches. The four generated app copies, beta portal, fresh launcher and protected 24/7 build were unchanged by the merge.

All three CI lanes passed on the exact remote merge commit: manual editor run `36331032811`, routing compatibility run `36331032678`, and capture transition run `36331032776`. The editor lane also verifies the protected build, parser, browser startup, Bridge crossing, mobile stress, committed zoom gestures and generated-copy equality.

## Active pass — 27 September 2026: mobile editor interruption safety

Development branch: `project-pineapple-v058`. Starting checkpoint: `3fc08209f638d02ddfbde844706d1de39114ba2d`; current live milestone is web v0.58 / packaged Android v0.57.

Completed work from earlier passes: post-capture rubber-band fix, draft-first Pencil/Bin/Bridge/Cleanup/Done editor, real Bridge persistence, mobile/zoom gesture stress, and reconciliation with main through `37bb435`. Do not redo those implementations. The historical requirements below remain acceptance criteria.

This active pass reproduced two production defects before changing code: view/app interruption left a live editor stroke/tap armed, and an out-and-back Bin drag was mistaken for a deliberate deletion tap. The baseline input-state regression failed 3 of 4 assertions. Both are fixed locally (4/4 pass), with explicit lost-pointer-capture recovery and mode-specific hints added. Earlier staged replacements are preserved.

Second audit: reproduced and fixed a stale LOOP CLOSED counter while the editor has an open route; it now follows EDITING / ROUTE OPEN / REPLACEMENT READY. Local production-function regression is 5/5. First browser run on `a2a4b5c8` passed the interruptions and 30 history cycles but failed reload because the synthetic fixture had no named project; the fixture now uses the real project activation path. Prior editor/Bridge/mobile/zoom tests remained green.

Third audit: on `46ca44a6`, the editor/routing/capture lanes and new WebKit interruption/reload test passed. Full suite had only the pre-existing v0.58 title allow-list failure. Reproduced two further lifecycle defects: switching circuits retained the old editor session, and a confirmed survey rebuild retained obsolete editDraft/bridges. Both fixed; local production-function checks 7/7. Circuit list completion ticks now respect editing status. Browser regression extended to switch away/back and rebuild.

Validation pending: new Chromium/WebKit interruption/30-cycle/save-reload/As-Fit regression, full serial suite (now including all v0.58 editor gates), Android build, visual audit and second fresh-eyes pass. No new public milestone yet. If interrupted, inspect current branch CI and fix failures before promotion; do not describe this as the premium loop being complete.

Continuation rule confirmed by Will: keep making useful improvements within the session after the first green CI run, and update this brief, NEXT_PROMPT, START_HERE and the checkpoint at meaningful steps. Do not end a pass merely by recording an unspecified future task.

## NEXT EXACT STEP

1. Continue on `project-pineapple-v058`, not `main`; the development branch now includes the current main history.
2. Choose the next concrete mobile/editor product improvement from real-device feedback, implement it in a small reproducible change, and run the relevant regressions.
3. Keep all three Pineapple lanes, generated copies and protected 24/7 verification green.
4. Do **not** publish a new web milestone merely for test or handoff changes; wait for a coherent usable product milestone.
5. Before any future promotion, recheck divergence from `main`, then verify Pages, `index.html`, `beta.html`, visible version labels and the fresh launcher together.

## Continuous-save rule

Operation Pineapple must never rely on chat state alone.

- Commit every meaningful logical change to `project-pineapple-v058` as it is completed.
- Commit before risky structural edits.
- Update `.github/PROJECT_PINEAPPLE_CHECKPOINT.md` whenever the active blocker, test result, deployment result or next step changes materially.
- Keep this START HERE file short and current.
- Prefer small reproducible changes over one giant unsaved edit.
- Never leave a long investigation only in conversation history.

## Web milestone rule

The web app is a **milestone surface**, not the scratch branch.

When a major milestone is reached:

1. all relevant Pineapple CI must be green;
2. protected 24/7 verification must remain green;
3. generated app copies must agree;
4. reconcile current `main` into development if branches have diverged;
5. publish/merge only a known-good coherent milestone to `main`;
6. verify the actual Pages deployment/run and, where practical, its artifact;
7. verify `index.html`, `beta.html`, visible version labels and launch URLs;
8. update the fresh launcher when appropriate;
9. immediately record the deployed web state here and in the checkpoint;
10. continue experimental work on Pineapple rather than using the live web app as the scratchpad.

Do **not** publish every diagnostic/test-only commit to the web app.

## Safety invariant

The protected 24/7 company/demo build must remain unchanged unless the user explicitly asks to change it.
