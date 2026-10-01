# Opening logo animation

Each fresh page/app launch shows the supplied main logo on black, then four system logos spread into the reference layout: Fire / Intruder above Access Control / CCTV. The artwork sequence takes 2.15 seconds after the images decode, followed by a short fade. The workspace loads independently underneath.

**Skip intro**, keyboard input, leaving the page or switching away dismisses the intro. OS reduced motion, the app's reduced-motion setting and its saved Motion off preference use a brief static screen. Failed images dismiss it immediately; a 3.2-second JavaScript watchdog and a 3.5-second CSS fallback prevent slow assets or script failures leaving the overlay in the way. It does not replay when returning from the browser back/forward cache or navigating within a project.

The two source assets are copied byte-for-byte from Will's uploads:

- `assets/startup/main-logo.png`: `A1BDDFE4-336A-4363-9C92-9091FD37415C(4).png`.
- `assets/startup/four-systems.jpg`: `IMG_0661.jpeg`, the supplied four-logo arrangement. Four CSS background windows let each logo move separately without redrawing, recolouring or re-encoding the supplied artwork.

The artwork is also mirrored in `app/src/main/assets/assets/startup/` for offline Android startup. Home, project storage, editor tools and the protected demo are unchanged. `tests/startup-logo-split.cjs` checks asset hashes/parity, layout on five viewport sizes, the start/end frames, fresh relaunch, natural dismissal, skip/keyboard dismissal, reduced/off motion and missing/stalled artwork. CI also runs the focused test in WebKit.
