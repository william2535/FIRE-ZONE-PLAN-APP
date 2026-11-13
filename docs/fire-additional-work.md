# Fire Additional work

The Fire New project dialog offers **Fresh install** (default) and **Additional
work** below the four discipline cards. The existing Create button creates the
project. Other disciplines and older projects keep their existing workflow.

Additional work reuses the editor in three stages:

1. **Building layout** — existing building, floor, import and editing tools;
   zone creation, assignment, fills and keys are hidden.
2. **Add devices** — existing Survey placement, references, properties and
   record states. Place the existing connection devices and the added devices.
3. **Circuit builder** — choose connection points, highlight the additional
   devices, then draw the section using the existing routing and editing tools.

## Connection setup

**Choose connection points** opens **Choose last device / cable joint location**.
Tap an existing device, drawn cable or blank plan location for Start, then tap
Return. Two successive taps on the same point reuse one reference. Blank plan
locations create standalone cable joints. The second tap opens device selection;
it does not draw or complete a circuit. Pan and pinch gestures do not select
endpoints. **Change connection points** lets you correct the selection before
building a circuit.

The circuit starts at the selected Start, passes through every highlighted
device and finishes at Return. No panel or dummy device is required. A
same-location return still needs an outgoing section and a real return route.

## Returning to a cable

After connecting the selected devices, draw to an existing cable and hold the
contact for five seconds. The visible progress bar records the deliberate hold.
Completion creates an attached joint and replaces the original Return. Small
finger wobble is allowed. Early release, movement away, pointer cancellation,
pan, pinch and leaving the view cancel the hold. Normal crossings never create
joints. The route must physically reach the contact; the hold cannot skip
devices or connect a remote, disconnected location. If the return joins its own
earlier cable, Reset or Undo restores the original return when that host cable
is removed. Route edits preserve attached joints and reject detached connections.

An unfinished cable tail is retained when lifting or leaving the builder. Its
green tip can be pressed to resume drawing or to start a new hold at a cable.
Undo removes this unfinished tail before removing a completed leg.

## Saved data and drawings

- Project `fireWorkType`: `fresh` or `additional`; absent means Fresh install.
- Floor `cableJoints`: stable IDs and plan coordinates, optionally attached to a
  circuit/leg/segment with an interpolation position.
- Floor `additionalSetup`: in-progress endpoint references and device selection.
- Additional circuits: explicit `startRef` and `returnRef`, selected device IDs,
  ordinary route legs, edit drafts and optional `routeDraft` for an unfinished
  tail. There is no synthetic panel.

Joints remain outside surveyed-device quantities. Autosave, backups, restore and
floor switching retain the workflow. Changed or missing cable attachments need
repair before the route can be treated as finished.

Building layout exports omit zone keys and empty-zone filler. Add devices uses
the existing survey output. As fit includes the layout, relevant devices, added
routes and actual Start/Return connections, with no hold indicator, temporary
handles or bridge editing marks. Saved As fit previews and Home drawing sets
remain available, using the Additional work stage names.

## Verification

New browser checks are included in `tests/run-regressions.cjs`:

- `additional-work-ui.cjs`: Fire selector, phone layout, zone-free building
  editing, Survey placement, work-type persistence and legacy behaviour.
- `additional-work-routing.cjs`: ordinary endpoint routing and circuit editing.
- `additional-work-setup-persistence.cjs`: unfinished endpoint and device selection
  restoration, cable attachments and same-joint reuse.
- `additional-work-hold.cjs`: actual phone pointer gestures, two-tap endpoints,
  timed cable returns, cancellation, identity, saved geometry and As fit.
- `additional-work-outputs.cjs`: backups, floors, joints, attachments, unfinished
  drafts, transformations and clean output.

`index.html` is mirrored to `ZoneSketch.html`, `Zone-Sketch-by-Will.html` and
`app/src/main/assets/index.html`. The separately protected 24/7 demo is unchanged.
