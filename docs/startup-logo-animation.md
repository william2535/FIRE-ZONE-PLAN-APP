# Opening logo animation

Each fresh page/app launch shows Will's supplied main house logo. Four image quarters initially assemble the original house exactly. Those same quarters separate and move outward. Each quarter's content stretches towards its sub-logo's bounds, then its silhouette continuously reforms into the target house and symbol. Signed-distance interpolation changes the visible outline while keeping the interior opaque; colours and surface detail change within that moving shape. This replaces the earlier image-opacity blend. The completed frame uses the exact supplied four-logo board. The source images are not traced, regenerated or modified.

The animation runs for 3.8 seconds and holds the completed logos until 4.6 seconds, followed by a short fade. Timing begins after both images decode. The workspace loads independently underneath. Skip intro and Escape dismiss it immediately; leaving the page also dismisses it. Tab can reach the intro controls without dismissing them.

OS or app reduced motion defaults to a gentle opacity transition. **Play full animation** explicitly enables the moving morph and remembers that choice for future launches in `zoneSketchIntroMotion`. This preference only affects the opening animation; it does not change the phone or app's other accessibility settings. Home's decorative Motion off setting does not suppress startup.

Failed images dismiss the overlay immediately. An 8-second asset-loading watchdog is cleared when decoding completes; a separate 15-second CSS fallback covers script failure. Explicit playback resets the fallback, so it still gets a complete sequence. It does not replay when returning to an already-open page or navigating within a project.

Source artwork remains byte-for-byte identical to Will's uploads:

- `assets/startup/main-logo.png`: `A1BDDFE4-336A-4363-9C92-9091FD37415C(4).png`.
- `assets/startup/four-systems.jpg`: `IMG_0661.jpeg`. The four image quarters provide the exact final logos; CSS windows are only used for the reduced-motion alternative.

Both assets are mirrored in `app/src/main/assets/assets/startup/` for offline Android use. All four app HTML mirrors match. Home branding, editor tools, project data and the protected demo remain unchanged.

`tests/startup-logo-split.cjs` verifies exact asset hashes, assembled artwork, intermediate separation and shape frames, exact final artwork pixels, final layout, five viewports, slow/missing/stalled image handling, natural exit, relaunch, reduced motion and explicit full-animation playback/persistence. WebGL renders the morph on the GPU; a bounded-resolution Canvas 2D implementation provides the same shape transition without WebGL. Tests cover that fallback too. CI also runs it in WebKit.

The Access schedule regression now waits for project activation to finish before using the Home control, matching the application's project-action guard and avoiding the earlier synthetic-click race in WebKit.
