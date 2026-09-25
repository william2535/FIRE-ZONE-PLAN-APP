# Circuit Builder continuity brief

This file is the persistent handoff for ongoing Circuit Builder work in Zone Sketch by Will Flood. Read this before making Circuit Builder changes in a new session.

## Current production state

- Current generation: v0.57 Smart Route.
- Main branch baseline at time this brief was created: `a86011206cd6751eddbc45fd1f9828268d33ff59`.
- Smart Route separates raw/coalesced pointer input, swept device-hit detection and final drawn/saved cable geometry.
- Explicit routing states are present.
- Addressable return magnet is retained.
- Deterministic aggressive-touch testing exists across small iPhone, large iPhone, Android, small tablet and landscape/desktop viewports.
- Permanent hardening coverage also exists for sparse multi-device sweeps, zoom-in -> fit continuation and viewport-resize checkpoint/resume.
- Latest validated suite at this point: 29/29 regression files plus successful Android build.

## User feedback after real tablet testing

The user reports that v0.57 feels substantially better after several real runs, but has already found at least one remaining red-zone routing bug in a real completed circuit. Do not guess the exact red anomaly from the screenshot alone; confirm the exact symptom with the user before implementing a targeted fix.

The user also wants manual post-route correction for cases like the yellow/green screenshots where Smart Route is valid but contains an unnecessary dogleg/corner or where the engineer wants to tidy a local section manually.

## Requested manual route editing UX

The intended interaction should feel like the existing Zone Plan drawing/editing workflow rather than like editing control points in CAD.

Preferred UI direction:

- Add a pencil/edit action for each circuit/zone OR a clear Edit button beside the Circuit Builder Fit control. Final placement should prioritise mobile/tablet usability and clarity.
- Add a bin/delete action beside it.
- Edit mode should let the engineer redraw a local cable section using the same touch-first, orthogonal/grid-aware feel as normal routing.
- Delete mode should behave like the existing Zone Plan erase tool: tap directly on the cable section to remove the intended route piece, with a forgiving but bounded hit tolerance.
- The engineer must be able to draw the replacement section first and then delete the old unwanted corner/section, so a temporary overlap is allowed while editing.
- Example intent: redraw the corner of a yellow route more cleanly, then delete the old dogleg without rebuilding the whole circuit.
- Editing must preserve device order, device assignment, circuit colour, completion state where valid, As-Fit consistency and undo/redo safety.
- It must be difficult to accidentally disconnect a device or silently create corrupt route geometry.
- If an edit would leave the circuit topologically invalid, either block it with a clear message or mark the circuit as requiring repair; never silently save broken geometry.

## Existing Zone Plan behaviour to reuse

Zone Plan already has a direct erase tool: `eraseAt(clientX, clientY)` finds the closest hittable object/section, pushes undo state, removes it and redraws. Zone rows also already expose a pencil/edit affordance for zone metadata. Reuse the interaction philosophy and visual language rather than inventing a completely different editor.

## Required implementation philosophy

Do not treat future Circuit Builder requests as narrow patches. For every significant routing/editing change:

1. Reproduce the reported issue first where possible.
2. Add a deterministic regression before or alongside the fix.
3. Test at mobile and tablet sizes, not desktop only.
4. Exercise slow, fast, rough, diagonal, overshoot, undershoot and repeated-direction-change input.
5. Keep raw hit detection separate from final saved geometry.
6. Measure route quality where relevant: points, segments, corners, short legs, reversals, crossings, excess route length and devices captured.
7. Preserve all existing Circuit Builder regression gates; do not weaken tests to get a green build.
8. Test Chromium and, where practical for touch behaviour, WebKit/Safari engine.
9. Run the full serial regression suite and Android build before merging.
10. Prefer a branch/PR for non-trivial changes, then merge only after CI passes.

## Manual route editor stress cases to add

When the manual editor is implemented, include deterministic tests for at least:

- replace one simple 90-degree corner;
- replace a multi-step dogleg with a simpler route;
- draw replacement first, then delete old section;
- delete near a device without deleting the device connection;
- delete at a junction/device endpoint;
- attempt deletion that would split a circuit in two;
- edit first leg from panel;
- edit last leg / addressable return leg;
- edit completed conventional circuit;
- edit completed addressable loop;
- edit at 1x and high zoom;
- edit after viewport resize/rotation;
- undo/redo each edit operation;
- repeated edit/delete cycles without geometry growth or orphan points;
- prevent/handle self-crossings according to circuit mode rules;
- overlapping different-colour circuits remain independently editable;
- large device counts remain responsive;
- As-Fit output reflects edited geometry exactly.

## Questions still requiring user confirmation

Before implementing the next editing release, confirm:

1. What exact defect in the red circuit screenshot is the user calling the bug? Ask them to point to or describe the bad section.
2. Should the pencil be shown beside every zone/circuit in the left list, beside Fit on the canvas, or both?
3. In Edit mode, should the user redraw from cable-to-cable, device-to-cable, device-to-device, or support all three?
4. Should a replacement section snap to the nearest existing cable endpoint automatically when the finger gets close?
5. When deleting, should one tap remove one segment only, a whole leg between two devices, or the smallest continuous section between junctions/corners?
6. Should deletion be allowed before drawing a replacement, even if that temporarily makes the circuit incomplete?
7. Should invalid/incomplete edited circuits lose their completed tick until repaired?
8. Should manual edits still enforce Smart Grid / 90-degree routing, or should freehand be available as an optional mode?
9. Should manual edit mode allow crossing an existing cable, or keep the current no-crossing rule for conventional Zone Challenge circuits?
10. Should undo/redo controls be visible directly in Circuit Builder edit mode?
11. Should edited routes get a subtle 'manually adjusted' marker/history, or remain visually identical to Smart Route output?
12. Should the manual editor operate on historical/completed circuits visible behind the active one, or only the currently opened circuit?

## Reusable continuation instruction

If a future chat loses context, the user can send:

> Continue Circuit Builder work from `docs/CIRCUIT_BUILDER_CONTINUITY.md` in `william2535/FIRE-ZONE-PLAN-APP`. Read that file first, inspect current `main`, check recent Circuit Builder commits/tests, then continue from the open requirements without restarting solved work. Do not weaken existing regression coverage. Use a branch/PR for non-trivial changes and update the continuity brief before finishing.

## Maintenance rule

At the end of every meaningful Circuit Builder development session, update this file with:

- current version/commit;
- what changed;
- what passed/failed;
- outstanding bugs;
- user decisions/answers;
- next exact step.

That makes this file the source of truth for handoff across chats.