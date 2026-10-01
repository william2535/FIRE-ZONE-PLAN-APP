# Opening logo animation

Each fresh page/app launch shows the supplied main logo on black, then four system logos spread into the reference layout: Fire / Intruder above Access Control / CCTV. The artwork sequence takes 3.8 seconds after the images decode, followed by a short fade. The workspace loads independently underneath.

**Skip intro**, keyboard input, leaving the page or switching away dismisses the intro. OS and app reduced motion show the main logo for 1.4 seconds, then the four logos without spatial movement, for the same full viewing period. Home's saved decorative Motion off preference does not skip startup. Failed images dismiss it immediately; an 8-second asset-loading watchdog is cleared once images decode, then the full 3.8-second sequence starts. A separate 15-second CSS fallback prevents script failure leaving the overlay in the way. It does not replay when returning from the browser back/forward cache or navigating within a project.

The two source assets are copied byte-for-byte from Will's uploads:

- `assets/startup/main-logo.png`: `A1BDDFE4-336A-4363-9C92-9091FD37415C(4).png`.
- `assets/startup/four-systems.jpg`: `IMG_0661.jpeg`, the supplied four-logo arrangement. Four CSS background windows let each logo move separately without redrawing, recolouring or re-encoding the supplied artwork.

The artwork is also mirrored in `app/src/main/assets/assets/startup/` for offline Android startup. Home, project storage, editor tools and the protected demo are unchanged. `tests/startup-logo-split.cjs` checks asset hashes/parity, layout on five viewport sizes, the start/end frames, fresh relaunch, natural dismissal, skip/keyboard dismissal, visible reduced/off motion, slow downloads and missing/stalled artwork. CI also runs the focused test in WebKit.
