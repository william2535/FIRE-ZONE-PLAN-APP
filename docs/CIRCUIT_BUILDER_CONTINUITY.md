# Circuit Builder continuity brief

This file is the persistent handoff for ongoing Circuit Builder work in Zone Sketch by Will Flood. Read this before making Circuit Builder changes in a new session.

## Current production state

- Current generation: v0.57 Smart Route.
- Main branch baseline before the next editing pass: `a86011206cd6751eddbc45fd1f9828268d33ff59` plus this continuity-document update.
- Smart Route separates raw/coalesced pointer input, swept device-hit detection and final drawn/saved cable geometry.
- Explicit routing states are present.
- Addressable return magnet is retained.
- Deterministic aggressive-touch testing exists across small iPhone, large iPhone, Android, small tablet and landscape/desktop viewports.
- Permanent hardening coverage exists for sparse multi-device sweeps, zoom-in -> fit continuation and viewport-resize checkpoint/resume.
- Latest validated application suite before the next editing release: 29/29 regression files plus successful Android build.

## Confirmed real-world bug after tablet testing

The user reports that v0.57 feels substantially better after several real runs, but a remaining routing defect is visible during aggressive routing.

Observed symptom:

- When a newly reached detector starts the next outgoing route, a very long temporary leg can shoot outward and move with the thumb, almost like a border/rubber-band line.
- It happens quickly and appears to settle/place when the finger leaves or the next routing action commits.
- Treat this as a transient-preview/state-transition bug, not merely an ugly saved-route threshold problem.
- Reproduce it using aggressive movement immediately after device capture, especially on tablet/mobile, before changing the engine.
- Investigate whether stale pre-capture coordinates, `lastPointer`, `routeInput`, capture guard state, pending corner state, or the first post-capture render tail is creating a provisional segment from the wrong origin.
- Add a deterministic regression that fails if the first live segment after device capture can jump a large distance away from the captured detector before deliberate movement warrants it.

Do not guess or hide the problem by clipping line length. Fix the state/geometry cause.

## Confirmed manual route editing UX

The user wants a professional local cable-editing workflow for situations where Smart Route is valid but a local section contains an unnecessary dogleg/corner.

### Controls

Expose manual editing in BOTH places:

1. a small pencil/edit action beside each zone/circuit in the left Circuit Builder list; and
2. an Edit control beside the `- / Fit / +` canvas controls for the currently open circuit.

Also expose:

- a Bin/Delete route tool;
- Undo;
- Redo;
- Done / Validate;
- a Bridge Mode toggle; and
- a compact route-cleaning options dropdown at the top while editing.

The controls must remain usable on phone portrait and tablet landscape without obscuring the drawing.

### Pencil / redraw behaviour

The pencil may start from ANY existing cable segment or device.

Supported edit joins must include:

- cable -> cable;
- device -> cable;
- cable -> device; and
- device -> device.

Preferred workflow:

1. Enter Edit mode.
2. Touch any existing cable section or device.
3. Draw the better replacement route.
4. Keep immediate live drawing responsive and visually rough enough to follow the thumb continuously; do not over-smooth the live stroke because the user likes the immediate/dopamine feedback.
5. Finish by touching another existing cable section or device.
6. On pointer release, run the configured geometry-cleaning pass.
7. Keep the new replacement section.
8. Switch to Bin/Delete and remove the old unwanted corner/section.
9. Press Done.
10. Revalidate topology before restoring COMPLETE state.

Manual routing remains 90-degree / Smart Grid based. It is not a freehand final-output mode.

### Post-release bend cleaning

Add a dropdown/options control at the top of Circuit Builder Edit mode containing a bend-cleaning slider.

Required behaviour:

- Live pencil geometry remains responsive and relatively literal while the finger is down.
- Cleanup activates when the finger is released / the edit stroke is committed.
- Default should start conservatively around cleaning repeated bend noise such as 2+ unnecessary small bends/stair-steps in succession rather than aggressively rewriting every corner.
- The slider changes how strongly post-release geometry is simplified.
- Low setting preserves more intentional detail.
- Higher setting removes more repeated micro-doglegs / stair-stepping.
- Never move cable endpoints away from the chosen cable/device anchors.
- Never simplify through a device, across an invalid obstacle, or into a different topology merely to reduce point count.
- Keep the default professional but not over-aggressive.

Implementation may expose friendly labels (for example Light / Normal / Strong) over a numeric internal threshold, but the user specifically wants a slider, not only presets.

### Bin / Delete behaviour

The Bin tool should follow the existing Zone Plan erase interaction philosophy.

Confirmed rule:

- one intentional tap targets ONE cable segment/local section, not an entire detector-to-detector leg and never an entire circuit.

Requirements:

- forgiving but bounded cable hit area;
- cable should win over nearby device deletion because this tool edits route geometry only;
- devices are not deleted by this Circuit Builder bin tool;
- push undo state before deletion;
- visually identify/highlight the targeted segment where practical before/destructively during the action;
- allow repeated local deletion to remove an old dogleg after its replacement has been drawn.

### Temporary invalid state

Deletion is allowed to temporarily break the circuit.

When topology is broken:

- remove/withhold the COMPLETE state;
- show a clear status such as `EDITING · ROUTE OPEN`;
- disable final As-Fit validity for that circuit;
- retain all assigned devices and circuit identity;
- allow the user to continue drawing repairs;
- Done must not accept an invalid/open route.

When the topology becomes valid again and Done succeeds, restore the normal completed status.

### Same-circuit overlap and Bridge Mode

The user does NOT want ordinary editing to freely overlap/cross existing cable as a default workaround.

Add an explicit Bridge Mode control:

- shown as a compact circular toggle button at the side of the Circuit Builder canvas/edit controls;
- OFF by default;
- when OFF, retain normal route collision/no-crossing behaviour;
- when ON, the active pencil route may intentionally pass over existing cable;
- Bridge Mode behaviour is the SAME for conventional and addressable Circuit Builder modes;
- make the active state visually unmistakable;
- treat bridge/crossing intent as explicit state so an accidental crossing cannot be mistaken for a valid normal route.

The exact crossing visual treatment should be consistent and clear in Circuit Builder and As-Fit output. If a dedicated bridge/jump symbol is practical, prefer one over silently drawing two indistinguishable intersecting straight lines.

### Different-colour cable bundling / adjacency

Different-colour zone/circuit cables may intentionally come together and run next to each other.

Required behaviour:

- allow a route to magnet/snap alongside a nearby cable from a different circuit/colour;
- preserve a small visual separation/lane so the colours remain easy to distinguish;
- do not treat parallel adjacency as a crossing;
- do not merge the circuits electrically/topologically just because their visual lanes are adjacent;
- Bridge Mode is only needed when the route genuinely passes across/through an existing cable path rather than running parallel beside it.

This should extend the existing twin-cable / paired-line visual language rather than producing overlapping strokes.

### Undo / Redo

Undo and Redo must be directly available while editing.

They must correctly cover at least:

- pencil replacement commits;
- segment deletions;
- Bridge Mode crossing commits where geometry changes;
- cleanup/simplification result;
- repeated edit/delete cycles.

Undo must restore exact prior topology and completion/editing state.

### Done / Validate

Done performs an explicit topology/geometry validation.

Before returning to COMPLETE, check at minimum:

- every assigned device remains connected as intended;
- the FAP relationship is valid;
- conventional/addressable completion rules remain valid;
- no unintended orphan cable fragments remain;
- no zero-length/duplicate route segments remain;
- no invalid normal-mode crossings remain;
- intentional bridge crossings are represented as bridges;
- all stored coordinates are finite;
- edited geometry survives redraw/save/reload identically;
- As-Fit generation receives the edited route, not stale pre-edit geometry.

If validation fails, stay in `EDITING · ROUTE OPEN` or another explicit repair state and tell the user what remains open.

## Existing Zone Plan behaviour to reuse

Zone Plan already has a direct erase tool: `eraseAt(clientX, clientY)` finds the closest hittable object/section, pushes undo state, removes it and redraws. Zone rows already expose a pencil/edit affordance for zone metadata.

Reuse the interaction philosophy and visual language rather than inventing a completely different editor.

Do NOT reuse Zone Plan deletion semantics blindly where it would delete a whole route object: Circuit Builder needs local cable segment surgery.

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
11. After targeted fixes work, perform a fresh-eyes audit of the entire Circuit Builder screen rather than stopping at the reported bug.

## Required new deterministic regressions

### Transient long-leg bug

Add tests specifically for:

- device capture followed by almost-zero movement;
- device capture followed immediately by a fast movement in a new direction;
- device capture with overshoot and reversal;
- multiple devices captured rapidly in one continuous hold;
- first post-capture preview frame remains anchored at the newly captured device;
- live preview cannot create a huge provisional leg from stale pre-capture coordinates;
- the final saved route remains unchanged by whatever transient preview logic is used.

### Manual editor

Include deterministic tests for at least:

- replace one simple 90-degree corner;
- replace a multi-step dogleg with a simpler route;
- draw replacement first, then delete old section;
- cable -> cable replacement;
- device -> cable replacement;
- cable -> device replacement;
- device -> device replacement;
- delete one segment only;
- delete near a detector without deleting/disconnecting the detector accidentally;
- delete at a route/device endpoint;
- edit first leg from panel;
- edit final conventional leg;
- edit addressable return leg;
- temporarily broken route shows `EDITING · ROUTE OPEN`;
- Done rejects an open route;
- repair then Done restores completion;
- edit at 1x and high zoom;
- zoom/fit during editing;
- viewport resize/rotation during edit;
- fast pencil swipe;
- shaky pencil input;
- overshoot;
- undershoot;
- repeated reversals;
- diagonal finger input still produces orthogonal saved geometry;
- sparse pointer events;
- cleanup slider low/default/high produce deterministic progressively simpler geometry;
- cleanup only runs on release/commit, not while live drawing;
- cleanup preserves anchors and intended topology;
- undo/redo pencil edits;
- undo/redo deletions;
- repeated edit/delete cycles without geometry growth or orphan points;
- save project/reload project;
- reopen edited circuit;
- As-Fit output reflects edited geometry exactly.

### Bridge Mode

Test:

- bridge OFF blocks/avoids crossing in both conventional and addressable editing;
- bridge ON permits an intentional crossing in both modes;
- bridge state is clearly explicit and does not leak into later normal edits unexpectedly;
- bridge geometry survives save/reload;
- bridge geometry renders correctly in Circuit Builder and As-Fit;
- deleting/editing around a bridge does not corrupt either route;
- accidental near-crossing with Bridge OFF does not silently become a bridge.

### Different-colour adjacent routing

Test:

- different-colour cables can snap/run parallel beside each other;
- a visible gap/lane remains at normal and high zoom;
- adjacency does not electrically/topologically merge circuits;
- editing one colour does not modify the other;
- parallel adjacency and actual crossing are correctly distinguished;
- dense multi-colour routes remain readable.

## Fresh-eyes Circuit Builder audit after implementation

After the red bug and editor are working, audit the whole Circuit Builder workflow, not just the changed code.

Test:

- home/circuit list;
- zone switching;
- pencil icons beside circuits;
- edit control beside Fit;
- addressable selection;
- conventional Zone Challenge;
- incomplete circuits;
- completed circuits;
- `EDITING · ROUTE OPEN` state;
- Undo;
- Redo;
- Reset;
- zoom buttons;
- Fit;
- pinch/viewport changes where possible;
- sound/progress UI;
- completion card;
- route persistence;
- switching circuits while editing;
- deleting circuits;
- survey changes invalidating circuits;
- As-Fit generation;
- As-Fit export;
- mobile portrait;
- tablet landscape;
- desktop landscape;
- dense routes;
- overlapping/adjacent coloured circuits;
- bridge crossings;
- cleanup dropdown/slider layout.

Look for:

- controls obscuring drawing;
- stale completion state;
- wrong colours;
- routes from another circuit appearing incorrectly;
- accidental edits to inactive circuits;
- hit areas too large/small;
- geometry changing after redraw;
- state lost after reload;
- phone/tablet controls too small;
- inconsistent labels/buttons;
- regression introduced by manual editing;
- stale live-preview lines after a detector capture;
- a long provisional leg shooting from the new detector;
- bridge mode remaining on unexpectedly;
- adjacent coloured cable lanes collapsing into each other.

Do not weaken an existing regression test just to obtain green CI.

## Resolved user decisions

1. Red bug = transient long leg/rubber-band preview immediately after a new detector is captured; it follows the thumb briefly before settling.
2. Show Edit both beside each zone/circuit and beside Fit.
3. Pencil can start/end on any cable or device combination.
4. Replacement is drawn first, old section deleted afterward.
5. Bin removes one segment/local cable section, not a whole leg/circuit.
6. Broken edits use `EDITING · ROUTE OPEN` and lose valid completion until repaired.
7. Final manual geometry remains Smart Grid / 90-degree.
8. Live pencil stays rough/responsive; cleanup happens on release using a user-adjustable slider, defaulting to conservative cleanup around repeated 2+ bend noise.
9. Crossing requires explicit Bridge Mode; normal mode does not freely cross existing cable.
10. Different-colour cables may run snapped/parallel beside each other with a visible lane gap and remain separate circuits.
11. Undo/Redo are visible in edit mode.
12. Done explicitly validates before restoring completion.

## Small remaining product detail

One visual detail can be chosen during implementation if not otherwise specified by the user:

- Preferred bridge rendering: use a clear small cable-jump/bridge hump at the crossing if it remains readable at phone/tablet zoom; otherwise use another explicit crossing treatment. Do not render an intentional bridge as two ambiguous plain intersecting lines.

No other product clarification is required before beginning the next implementation pass.

## Reusable continuation instruction

If a future chat loses context, the user can send:

> Continue Circuit Builder work from `docs/CIRCUIT_BUILDER_CONTINUITY.md` in `william2535/FIRE-ZONE-PLAN-APP`. Read that file first, inspect current `main`, check recent Circuit Builder commits/tests, then continue from the open requirements without restarting solved work. Do not weaken existing regression coverage. Use a branch/PR for non-trivial changes and update the continuity brief before finishing.

For the next release specifically, the user can simply send:

> Continue the Circuit Builder red-bug + manual edit/bridge pass from the continuity brief. Reproduce first, implement on a branch, stress-test everything, and update the brief before stopping.

## Maintenance rule

At the end of every meaningful Circuit Builder development session, update this file with:

- current version/commit;
- what changed;
- what passed/failed;
- outstanding bugs;
- user decisions/answers;
- next exact step.

This file is the source of truth for handoff across chats.