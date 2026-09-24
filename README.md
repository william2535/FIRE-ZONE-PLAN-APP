<p align="center">
  <img src="assets/on-site-zone-planner-cover.webp" alt="On Site Zone Planner" width="100%">
</p>

# Zone Sketch by Will — site draft for the office


A small offline Android app for walking a site and marking fire-alarm zone areas on a floor-plan image. It is a **working draft for an office CAD redraw**, not a finished customer chart or a substitute for checking the current fire strategy.

## Use on site

1. Tap **Import plan** and choose a photo, PNG or JPG. For a PDF page, take a screenshot or export that page to an image first.
2. Type the site name. Tap **+ Zone**, enter its number and short area description.
3. Leave **Box** selected and drag across a rectangular area. Use **Outline** to tap corners for irregular areas, then **Finish outline**. Select an existing zone to add another disconnected area in the same colour.
4. Use **Note** for uncertainties the office should check. Use **Move plan** or two fingers to pan and zoom.
5. Tap **Send to office** and choose email, Teams, WhatsApp, Uptick, etc. The shared PNG includes the plan, zone outlines, key, date and draft label.

The current draft autosaves on this tablet. **New** replaces that saved draft. Send the PNG before starting the next site. This first version saves one active site draft, not a project library. Original high-resolution image is resized to at most 3000 pixels on its longest edge to keep cheap tablets responsive.

## Build the APK with GitHub

Upload the contents of this folder as the root of a new GitHub repository (including `.github/workflows/build-apk.yml`) and commit to `main`. Open **Actions → Build Android APK → latest run → Zone-Sketch-by-Will-APK**. Download the artifact ZIP; the `app-debug.apk` inside is installable on Android 8 or newer. If Actions is disabled in the repo, enable it under the repository Actions settings, then use **Run workflow**.

This is a debug-signed APK for personal testing. Updates built from the same GitHub runner may use a different debug key and require uninstalling the old APK; uninstalling clears the saved draft, so send it first. A stable release signature and multiple saved site projects can be added after field testing.

There is no login, subscription, internet permission, camera permission or analytics. Floor plans and sketches remain on the device unless you share the exported PNG. The Android wrapper uses a WebView, an image picker and the system share sheet.

## Project files

- `app/src/main/assets/index.html`: the entire drawing interface.
- `app/src/main/java/com/zonesketch/app/`: Android image picker and PNG sharing.
- `.github/workflows/build-apk.yml`: APK build workflow.
- `Zone-Sketch-by-Will.html`: branded standalone browser preview of the interface.
- `ZoneSketch.html`: compatibility copy kept in sync for older tooling.

## Known first-version limits

- Image plans only; PDF import, perspective straightening and a multi-project library are later additions.
- Zone outlines are manual. The PNG is for the CAD team to verify and redraw.
- No measured scale or fire design compliance calculations.

## Version 0.2 — tracing and blank plans

- **Picture opacity** fades an imported image while keeping wall lines, zones and notes solid. The same opacity applies to PNG export.
- **Hide picture** removes the image from both the canvas and export while keeping your drawing. **Show picture** restores it.
- **New blank** / **Start blank canvas** starts a white 1600 × 1000 page without an import. Share the existing draft before replacing it.
- **Wall line** draws individual straight segments and snaps nearly horizontal/vertical lines. **Pen** draws freehand. Both support undo and redo and autosave with the draft.

## Version 0.3 — doors, room labels and precise delete

- **Door**: drag from the hinge to the door edge to add a simple swing symbol for the office/CAD redraw.
- **Room label**: tap a room and type its name; labels stay readable over a faded plan and are included in PNG export.
- **Delete**: tap a wall/pen stroke, zone area, door, note or room label to remove only that item. **Undo** immediately restores accidental deletions.
- Existing Version 0.2 drafts remain compatible; new door and room-label data is simply added when used.

## Version 0.4 — snapped doors, wall junctions and groups

- **Door placement now locks to an existing wall.** Drag along the wall and only the exact opening is highlighted in orange. Releasing cuts that section from the wall and snaps the door into the opening; the door no longer slides around under your finger or paints a larger white gap over the wall.
- **Wall lines snap and split at corners/intersections.** A wall that continues past a T-junction becomes separate pieces at the junction, so **Delete** removes only the tapped protruding section instead of the whole wall run.
- Existing straight walls are split into junction pieces when an older draft is loaded, improving delete behaviour on previous sketches.
- **Group / Move** lets you drag a selection box around a room, press **Group selected**, then move the whole grouped room together. Tapping any item in a saved group selects that group again; **Ungroup** separates it.
- Doors created in a grouped wall inherit the same group so the wall pieces and door move together.

## Version 0.5 — clean doors, explicit groups, object move and grid

- **Door geometry is cleaner:** the swing arc now starts exactly on the opposite edge of the wall opening, so both ends of the door connect cleanly to the straight wall line.
- **Group is now an explicit action:** use **Box select**, then press **Group** in the bottom toolbar (or **Make group** in the selection bar). **Ungroup** is equally visible.
- **Select / Move** lets you tap and drag one wall section, door, room label, note or zone shape. Tapping any member of a saved group selects and moves the whole group as one object.
- **Grid off / Grid on** is available in the top bar. The grid is a screen-only drawing aid and is deliberately excluded from the exported office PNG.

## Version 0.6 — grouped Zone and Building Layout menus

- The bottom toolbar is simplified into two main drawing menus: **Zone** and **Building layout**.
- **Zone** shows the currently selected/created zone and contains **Box** and **Outline** for coloured zone areas, plus **Create zone** and the existing zone list.
- **Building layout** contains **Wall, Pen, Door, Box, Outline and Room label**. Its Box and Outline tools create black wall segments rather than zone areas, so they work with Delete, Select / Move and Group.
- Both menus open upward from the bottom toolbar and remember the last drawing tool used. Common edit controls remain directly accessible.

## Version 0.7 — drawing polish

- Building wall boxes/outlines now merge overlapping or near-overlapping horizontal/vertical wall runs into one clean line, then re-split them at real junctions so precise delete still works.
- Zone badges such as **Z1** are removed from the drawing; zone identification remains in the side index and exported zone key.
- Zone areas now use a restrained translucent fill and thin boundary instead of a heavy coloured border.
- The grid uses fixed plan-space spacing, so it stays anchored to the drawing while zooming.
- Room labels are sized from plan-space scale instead of a separate clamped zoom scale, so they remain visually attached to the plan.

## Version 0.8 — detail drawing controls

- Undo and redo are duplicated in the top-right so they remain easy to reach while drawing.
- Door placement now uses the finger side of the wall to choose the swing direction, with a live orange opening and swing preview before release.
- Blank plans use a 3200 × 2000 working canvas (four times the previous pixel area), and maximum zoom is increased from 8× to 32× for intricate rooms and corners.
- A Wall size slider in the top bar controls building wall/pen/door thickness from 0.75 to 5 px without the old automatic thickening while zooming.
- The selected wall thickness is also respected in the exported office PNG.

## Version 0.9 — zone fill and objects

- Zone colour fill is stronger while keeping the same thin professional border.
- **Fill area** finds the smallest fully enclosed face in the connected wall graph and creates a neat zone polygon automatically. Door/window/shutter openings count as closed boundaries for zoning.
- Drawing tools are split into **Zone**, **Building layout**, and **Objects** menus.
- **Objects** contains wall-snapped Door, Window and Roller shutter tools plus a drag-to-place Stairway symbol.
- New objects support selection, movement, grouping, deletion, undo/redo and PNG export.

## v0.10 — multiple floors

Use the Floor selector to switch drawings. Add Ground, First, Second, Third, Fourth, Basement, Mezzanine or a custom floor. Each floor keeps its own zones, image, opacity, objects and notes. Existing drafts migrate to Ground floor. Rename or delete a floor; Undo restores deletion. Blank this floor and Import plan affect only the selected floor. New starts a whole new site.

Copy current building layout when adding a floor to reuse walls, openings, stairs and room labels, without copying zone assignments, notes or the background photo. Send to office exports the selected floor, with its name in the title and filename; switch floors to export the next drawing.

### Onsite workflow roadmap (see newer releases below)

- Favourite symbol stamps: fire panel, repeater, MCP, smoke, heat, sounder, beacon and you-are-here marker, with a clear symbol key.
- Repeat placement: keep a symbol selected and tap several locations; optional sequential device labels.
- Room-name shortcuts: Office, Store, Corridor, WC and Plant room, plus recently used names.
- Duplicate a selected room or group, with rotate and mirror controls.
- Pin photographs or dictated notes to a location for office follow-up.
- Export all floors together with a site-wide zone index and editable project backup.
- Large-button survey mode with favourites, Undo and Fit always visible.

## Version 0.11 — faster onsite workflow

- Floor selection now uses the same compact dropdown/popover style as Zone, Building, Objects and Symbols instead of a native floor select popup.
- Symbol favourites: Panel, MCP, Smoke, Heat, Sounder and You are here. Symbols are tap-to-repeat until another tool is selected.
- Quick room-name stamps for Office, Store, Corridor, WC, Plant room and custom names.
- Box-selected rooms/objects can be duplicated, rotated 90 degrees or mirrored; duplicates are kept together for immediate moving.
- Pinned notes and compressed pinned site photos stay at exact plan positions and are listed (with photo thumbnails) in office exports.
- Send all floors creates one combined building-pack PNG containing every floor plus a building-wide zone index.
- New objects remain floor-local, autosaved, undoable, groupable, selectable and movable.

## Version 0.12

- Selected rooms/groups can be resized by dragging blue corner handles. Quick room labels and favourite symbols scale with the selection.
- Bottom toolbar is ordered into Draw, Edit, View and History sections for faster onsite use.
- Grid spacing is adjustable and an optional Snap mode aligns new drawing points, stamps and selection movement to the grid.
- Favourite symbols have a colour palette; the selected colour is stored on each placed symbol and is preserved in exports.

## Version 0.13 — stable corner resize + quick delete

- Delete is duplicated beside Undo / Redo in the top-right for faster onsite editing.
- Corner resize now recalculates every frame from the original selection snapshot, preventing cumulative shrink/jump behaviour.
- The opposite corner stays fixed while resizing a room or group.
- A 24-screen-pixel minimum prevents a selected corridor/room collapsing into an unusably tiny shape.

## Version 0.15
- Global Move mode: ON pans/zooms without editing; OFF edits without canvas panning.
- Trim / Extend wall tool.
- Object Properties for selected items.
- Background, Building and Zone locks.
- View-only Layers menu for background, building, zones, symbols, labels, notes/pins and grid.
- Current-floor and whole-building device counts, also included in office exports.

- v0.15 safety fix: Move-mode pointer-up isolation and clearing selections when layers/locks are activated.

## Version 0.17
- Zone Fill Area now tolerates tiny touch-drawing gaps instead of requiring mathematically perfect wall joins.
- Fill detection splits unsplit T-junctions during calculation, so resized/moved rooms still fill correctly.
- Small geometry repairs are temporary for fill detection only; the user's actual building walls are not moved.

## Version 0.18
- Rotating a room/group now rotates symbol orientation as well as symbol position.
- Symbol rotation is saved per symbol and preserved in office exports.
- Single symbols can be rotated from Object Properties.
- Existing drafts remain compatible; symbols without a saved angle default to 0 degrees.

## Version 0.19 — clean controls and reliable office handoff

- Project and Drawing dropdowns declutter the header; floors use the same in-app menu and preset buttons. Menus scroll within the phone viewport.
- Door selection/deletion follows the visible leaf, swing arc and opening. Delete removes only the door, leaving the wall gap; Undo restores it. Zone fills no longer steal nearby object taps.
- Photos display matching P markers on screen and exports, with a preview in Properties.
- Beacon and repeater stamps, editable device references, and a symbol key on exported plans. “You are here” markers are excluded from device totals.
- Drawing reference, revision, surveyed-by and date fields appear in exports.
- Send to office offers current-floor PNG, a paged all-floor PDF with building zone index, or an editable JSON project backup. Open backups from Project; all floors/photos remain editable. PDF pages contain high-resolution raster drawings, not CAD vectors.
- Android shares PDF/PNG/JSON with the correct MIME type and filename; separate export files prevent a later share overwriting an earlier attachment.
- Fixed move-mode previews throwing errors, locked room stamps bypassing locks on touch-up, second-touch stamps, and groups distorting against the canvas edge. Cancelled drags roll back. Rotations outside the canvas are rejected instead of crushing geometry.
- Paints coalesce to animation frames; the canvas buffer only reallocates when size changes. Saved status waits for IndexedDB completion. Editable backups provide a portable copy of the device-local draft.

Validation: browser regression tests, multi-floor persistence/migration tests, and interaction tests for door deletion, locks, real multi-touch, grouped objects, pinned photos, PNG/PDF/backup exports and backup restore. Test screenshots cover tablet/phone menus. Android compilation runs in GitHub Actions. Physical-device sharing is not automated.

## Version 0.20 — public tester build
- Adds Double door as a proper wall-opening object with two swing leaves and finger-side swing preview.
- Adds Circular room under Building layout; drag a circle/oval to create editable wall sections that accept doors/windows and Zone Fill Area.
- Double doors remain selectable, deletable, movable, groupable, undoable and included correctly in office exports.
- Browser, standalone HTML and Android WebView copies are kept identical.
- Android app version bumped to 0.20 for the public tester release.
- Release workflow runs the full browser regression suite plus dedicated v0.20 geometry/mobile tests before building the APK.

## Version 0.21 — Zone Sketch by Will branding
- Public-facing product name is **Zone Sketch by Will** across the browser app, Android launcher, public tester page and Android share UI.
- APK, PNG, PDF and editable-backup filenames include **Zone-Sketch-by-Will** so shared copies are immediately recognisable.
- Office exports and building packs carry **Zone Sketch by Will** branding.
- New editable backups identify themselves as `ZoneSketchByWill`; older `ZoneSketch` backups remain supported.
- Android package ID and browser storage identifiers intentionally remain unchanged so existing installs and saved drafts continue to work.

## v0.22 — Projects / Home (roadmap step 1)

The app opens to **Your surveys**. Create a named blank survey, reopen a recent
project, or import an editable backup as a separate project. Cards show the site,
floor count, last edit time and a preview of the last drawing view, with Open,
Rename, Duplicate, Export and Delete actions. Return through **Project → Home / Projects**.

Each survey saves separately in the existing local IndexedDB database. The previous
single draft migrates automatically; backups remain compatible with version 1.
Project changes reset Undo/Redo, and switching stops if saving fails. Deleting a
project requires confirmation and cannot be undone. Export backups regularly:
clearing app/browser data still removes locally saved projects.

This step does not yet include reusable templates, recovery snapshots or cloud sync.
Browser regression coverage includes `node tests/projects.cjs` alongside the existing
browser, floors, interactions and v020 suites.

## v0.23 — Survey mode and project polish

Use **Survey mode** for a larger drawing area and six touch controls: Move, Undo,
Delete, Add device, Add room and Add note. **Full tools** restores the normal
interface; floor switching, project actions and export remain available. Entering
Survey mode starts in Move to avoid accidental marks. Mode selection lasts for the
current session and does not change exported drawings.

The Home screen now has survey search and a cleaner responsive card layout.
Opening a drawing no longer focuses the site-name field (and opens a phone keyboard).
Opening or reopening a saved survey no longer changes its last-edited date or
rewrites the full drawing. The last opened project is still restored correctly.

## v0.24 — Favourite tools

The normal drawing toolbar now starts with a persistent **Favourites** section.
Defaults are Smoke, Heat, MCP, Door, Wall and Pinned note. Open **★ Favourites**
to choose up to ten tools, or press and hold a supported item in the Building,
Objects, Symbols, Zone or Site details menu to add/remove it quickly.

Favourites are stored as a device preference, so they remain available across all
projects and after reopening the browser/app. **Reset defaults** restores the standard
fire-survey set. The favourites row hides automatically in Survey mode, which keeps
its existing six large controls.


## v0.25 — Resizable notes

Plan notes can now be made smaller or larger. Select a normal Note or pinned site-detail marker and use **Properties → Size**, or drag the blue corner resize handles directly on the plan. Note/pin scale is stored with the project and is preserved in PNG/PDF office exports. Existing projects keep their current visual size until changed.

## Version 0.26 — drawing productivity
- Corridor tool creates a grouped rectangular corridor and labels it automatically.
- L-shaped room tool creates a six-wall grouped L room in one drag.
- Edit wall ends shows draggable endpoint handles for quick corrections.
- Join wall gap moves one wall endpoint directly onto another.
- Split wall creates a new editable junction/section with one tap.
- New drawing tools can be added to Favourite Tools.

## Version 0.27 — plan import and tracing cleanup
- Import PDF floor-plan pages directly as a background, with page choice for multi-page PDFs.
- PDF rendering is bundled locally so Android can open PDFs without an internet connection.
- Background cleanup adds brightness, contrast and black-and-white controls plus a plan preset.
- Four-corner perspective straighten corrects photographed plans before tracing.
- Rotate imported plans by 90 degrees before drawing.
- Snapping now shows endpoint, midpoint and wall snap markers plus alignment guides.

## Version 0.28 — mobile web stability
- Locks the main web-app viewport so Safari/iOS cannot drag the whole page up and down while drawing.
- Uses the dynamic viewport height so the workspace follows the visible browser area more reliably.
- Canvas touch movement is explicitly prevented from becoming page scrolling/rubber-banding.
- Menus, project lists and modal panels keep their own contained scrolling when content genuinely needs to scroll.

## Version 0.29 — zones panel visibility hotfix
- Keeps zone cards fully visible after the v0.28 locked-viewport change.
- Gives the zones list guaranteed usable space on shorter browser windows.
- Hides the long help copy automatically when vertical space is tight so it cannot crowd out the zones.
- On phones, zones use a stable-height horizontal strip instead of being vertically clipped.

## Version 0.30 — full canvas and wall-snapping zones
- Removes the permanent Zones side/bottom barrier so the drawing canvas uses the full workspace.
- Zones are still created, selected and edited from the bottom Zone menu.
- Zone Box now snaps its dragged corners/edges to nearby building wall endpoints and wall lines.
- Keeps the locked Safari/web viewport behaviour from v0.28.

## Version 0.31 — Zones sidebar restored
- Restores the visible, collapsible Zones list at the side on tablet/desktop and as a strip on phone.
- Keeps the v0.30 wall-aware Zone Box snapping improvement.
- Existing zone creation, selection, saved projects and collapse/reopen behaviour remain intact.

## Version 0.32 — cleaner zone fills
- Removes coloured perimeter outlines from completed zones, previews and exported plans.
- Keeps the light transparent zone colour fill so building walls stay visually dominant.
- A single selected zone shows resize handles without drawing another full box around it.
- Keeps the restored Zones sidebar and wall-aware Zone Box snapping from v0.31/v0.30.

## Version 0.33 — constant zone transparency
- Overlapping zone areas no longer become darker when the same area is covered more than once.
- Zone fills are composed into one layer first, then the transparency is applied once.
- The same constant-opacity behaviour is used on the live canvas, Zone Box/Outline previews and exported plans.
- Different overlapping zone colours can still replace one another visually, but the transparency never stacks darker.
