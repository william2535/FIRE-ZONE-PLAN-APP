# Zone Sketch — site draft for the office

A small offline Android app for walking a site and marking fire-alarm zone areas on a floor-plan image. It is a **working draft for an office CAD redraw**, not a finished customer chart or a substitute for checking the current fire strategy.

## Use on site

1. Tap **Import plan** and choose a photo, PNG or JPG. For a PDF page, take a screenshot or export that page to an image first.
2. Type the site name. Tap **+ Zone**, enter its number and short area description.
3. Leave **Box** selected and drag across a rectangular area. Use **Outline** to tap corners for irregular areas, then **Finish outline**. Select an existing zone to add another disconnected area in the same colour.
4. Use **Note** for uncertainties the office should check. Use **Move plan** or two fingers to pan and zoom.
5. Tap **Send to office** and choose email, Teams, WhatsApp, Uptick, etc. The shared PNG includes the plan, zone outlines, key, date and draft label.

The current draft autosaves on this tablet. **New** replaces that saved draft. Send the PNG before starting the next site. This first version saves one active site draft, not a project library. Original high-resolution image is resized to at most 3000 pixels on its longest edge to keep cheap tablets responsive.

## Build the APK with GitHub

Upload the contents of this folder as the root of a new GitHub repository (including `.github/workflows/build-apk.yml`) and commit to `main`. Open **Actions → Build Android APK → latest run → ZoneSketch-APK**. Download the artifact ZIP; the `app-debug.apk` inside is installable on Android 8 or newer. If Actions is disabled in the repo, enable it under the repository Actions settings, then use **Run workflow**.

This is a debug-signed APK for personal testing. Updates built from the same GitHub runner may use a different debug key and require uninstalling the old APK; uninstalling clears the saved draft, so send it first. A stable release signature and multiple saved site projects can be added after field testing.

There is no login, subscription, internet permission, camera permission or analytics. Floor plans and sketches remain on the device unless you share the exported PNG. The Android wrapper uses a WebView, an image picker and the system share sheet.

## Project files

- `app/src/main/assets/index.html`: the entire drawing interface.
- `app/src/main/java/com/zonesketch/app/`: Android image picker and PNG sharing.
- `.github/workflows/build-apk.yml`: APK build workflow.
- `ZoneSketch.html`: standalone browser preview of the interface.

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
