# Site copies and Intruder placement

Use **Copy layout…** on a Home project card to start a CCTV or Intruder project
from an existing site. Choose the target system and a name, then create the copy.
The original site remains unchanged. The copy retains the building and imported
plans on every floor, with a fresh device library and system setup for its new
discipline. The existing **Duplicate** action still creates a complete copy in
the same discipline.

New-site creation saves the new record before switching the active workspace.
Closed browser database connections reconnect once, while interrupted or full
storage leaves the current site intact and reports the problem. The default
blank plan uses a compact prebuilt white PNG instead of allocating another
large temporary canvas, avoiding a reproduced allocation failure on creation.

Intruder equipment uses the existing wall placement behaviour. Place it near a
wall to snap to that side; place it away from walls for a free position. PIR and
dual-tech detectors support the same finger-drag aiming interaction as cameras.
Their position stays anchored while the selected detector's gold handle changes
its direction. Door contacts snap to nearby door openings.

The **360° detector** is a separate circular detector in the Intruder library.
It remains freely placed and has no directional handle. It participates in
device counts and Intruder zone assignment like the other detectors.

Placement and direction are included in the usual undo/redo, saved projects,
editable backups and drawing exports. Fire panel/MCP placement and CCTV camera
aiming retain their existing behaviour.

The focused browser checks are `tests/site-copy-create.cjs` and
`tests/intruder-placement.cjs`; both are included in the regression runner.
Relevant existing checks cover project storage, phone menus, wall-mounted Fire
devices, CCTV aiming and system device libraries.

The maintained source is `index.html`, mirrored into `ZoneSketch.html`,
`Zone-Sketch-by-Will.html` and `app/src/main/assets/index.html`.
