# Camera pointing triangles

All five CCTV camera device types (fixed, dome, turret, PTZ and ANPR) now use a beam-style pointing triangle in the shared editor and plan exports. Their type abbreviation and existing device reference remain visible. NVRs, switches and other system symbols keep their existing shapes. The triangle documents pointing direction, not a measured or guaranteed field of view.

- Drag from the camera position towards the intended view when placing a camera. A tap still places it facing right.
- Select a camera and drag its gold aiming handle to change direction without moving the camera or its cable anchor. The handle has a 44-pixel touch hit area and stays at least 48 pixels from the camera centre.
- Properties provides a direction slider in degrees, alongside the existing rotate and mirror controls.
- Cancelled aiming gestures leave the saved direction unchanged. Completed adjustments use one undo step and the existing autosave/As-Fit change tracking.

Direction uses the existing `rotation` field. No new schema, duplicated metadata, or camera-to-cable references are introduced. Older cameras without rotation render facing right. Normal device duplication, project backups and drawing/report export retain the angle, IDs, notes and metadata. Batch-added cameras remain ordinary individual devices and can be aimed afterwards.

Focused checks in `tests/camera-direction.cjs` cover all camera types, drag placement, touch aiming and cancellation, stable cable endpoints, undo/redo, properties, rotate/mirror, old cameras, tap placement, five viewports, exported triangles, reload and backup export/import. The test is part of the full regression runner and also runs in WebKit CI. The existing beam regression and protected demo remain unchanged.
