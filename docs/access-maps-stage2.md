# Access Control maps — Stage 2

Extends the existing Zone Sketch editor and door objects. Home, branding, device catalogue, Fire routing and the protected 24/7 demo are retained.

## Use

Open Access Control tools → Door Setup. Select an existing plan door, record its optional field details, and expand **Associate placed equipment & onsite evidence**. Choose entry/exit readers, locks, RTE buttons, emergency releases, contacts, controllers and PSUs. Evidence references existing photo/note pins. Shared controllers and PSUs can be associated with multiple doors, including doors on different floors. Save associations independently from the detail form.

**Show door & associations** displays labelled doors and dotted equipment guides. These guides are not cable routes. The Door associations layer hides these guides and labels in the working view. Door properties show the same references; System setup edits them.

Door Connections uses the existing connection engine. Choose actual endpoints and optionally assign the cable to a door record. **Edit cable bends on plan** opens a draft: tap bends in order, undo bends, then Save route or Cancel. **Use automatic elbow** clears manual bends. Endpoints follow equipment movement; intermediate bends stay at their recorded plan positions. Record intended/installed cable status with the shared As-Fit states. No topology is generated from the equipment associations.

Door Schedule offers compact door cards and CSV export. Access Report and issued-record CSV also include the schedule, equipment references, cable records, outstanding documentation and revision. Drawing/PDF exports include door labels and existing cable/state graphics. Dotted selection guides are working-view aids and are excluded from drawings. Photos remain in the project backup and drawing evidence; schedule CSV references their stable pin IDs rather than embedding image bytes.

## Persistence and compatibility

- Additive `door.accessLinks`: role → `{floorId, deviceId}[]`. Role keys: `entryReaders`, `exitReaders`, `readers` (side unrecorded), `locks`, `rte`, `emergency`, `contacts`, `controllers`, `psus`.
- Additive `door.accessEvidence`: `{floorId, pinId}[]`. Existing `systemData` strings remain intact, including free-text door details. Additional optional strings are `cableNotes`, `commissionNotes`, `evidenceNotes`.
- Legacy `device.systemData.doorId` remains readable without migration. Resolve explicit `doorFloorId`, then the device's floor, then an unambiguous project-wide match. Explicit door-side associations take precedence over legacy links.
- Cable `metadata.doorId` / `doorFloorId` are optional. Connections with both endpoints belonging to the door, or an endpoint on the door itself, are also included when no explicit door assignment exists. This is a schedule grouping, not an inferred wiring requirement.
- Missing equipment/evidence remains referenced and produces a documentation prompt. Access endpoint deletion retains cable records; the existing safe renderer omits a path whose endpoint cannot resolve. Engineers can reconnect or explicitly delete it. Other systems retain their existing deletion behaviour.
- Autosave, project duplication, backup and issued snapshots retain IDs, floor qualifiers, routes, photos and revisions. Copying building layout to another floor or duplicating a door clears explicit equipment/evidence links; it does not claim the original installation exists at the new location.
- Door verification with explicit associations fingerprints associated equipment, routes and evidence. Editing/removing those records invalidates working-door verification. Issued snapshots remain unchanged. Missing states stay **Not recorded**; association and commissioning never imply onsite verification.

## Authoritative guidance reviewed 1 October 2026

- [BSI: BS EN 60839-11-2:2015 — electronic access control application guidelines](https://knowledge.bsigroup.com/products/alarm-and-electronic-security-systems-electronic-access-control-systems-application-guidelines). The public catalogue identifies it as current and describes planning, installation, commissioning, maintenance and documentation within its scope. Public summaries were reviewed; the full paid standard was not reproduced or treated as implemented by the app.
- [NSI: NCP 109 Issue 4 guidance, Access Control and Safe Escape](https://www.nsi.org.uk/access-control-safe-escape-and-ncp-109-issue-4/), and its [24 March 2026 announcement](https://www.nsi.org.uk/security-vs-safety-guide-to-the-new-ncp-109-issue-4/). Door purpose, escape arrangements and the site's fire strategy need consideration; there is no universal electric-release prescription. The guidance is an explainer, not the code itself.

Implementation decision: a maglock without a recorded emergency release prompts the engineer to record the release arrangement. Fire interface, fail mode and commissioning details remain optional records. No regulatory pass/fail, automatic design approval, wiring prescription or compliance certificate is produced.

## Validation and limits

`tests/access-maps-stage2.cjs` exercises actual association controls, floor-qualified duplicate IDs, shared equipment, evidence, touch route save/cancel, endpoint movement/deletion, verified-state invalidation, immutable issue content, schedule/report/drawing exports, reload, project duplication and backup import. It also checks invalid association data and five viewport sizes. Existing Phase 2/3 tests target the detail form specifically now that doors have a separate association form. The Stage 1 touch-target check now waits for its modal animation to finish before measuring, addressing the prior main-branch CI failure without weakening its 44px/viewport assertions. Full regression, protected-demo, parser, mirror and current-release gates are required; WebKit runs the Stage 1 and Stage 2 focused tests in CI.

Cable paths still belong to a single floor. Cross-floor equipment associations are supported, but cross-floor cable geometry is not introduced in this stage. Fire interface is optional descriptive information; no new interface device type or site topology is invented. Route editing uses ordered bend taps and undo, not draggable bend handles. Phone checks use Chromium/WebKit touch emulation rather than physical iOS/Android hardware. Local browser runtime is Playwright 1.51.1; repository CI uses its existing pinned 1.62.1 runtime. Stage 2 stops here.
