# iPhone portrait menu and shared brand motion

The portrait `.app > .top .topMain` grid rule appeared after the collapsed-header rule at equal specificity. It kept the header visible while the button and floor strip said it was closed. A scoped collapsed-state rule now wins. The essential row uses real 44px touch targets, including the full Menu/Close button, across 320–430px phones.

The previous focused regression removed overlays and called `onclick()` directly. The replacement creates a real project and taps Menu, Project, Close, Home and Survey; it rotates the viewport and repeats the interactions. Existing UI tests now open the header before using its controls rather than depending on the faulty visible collapsed header. CI reproduces the original failure first.

Conflicting decorative animation declarations were removed in favour of one final motion layer. The approved transparent home artwork gets a complete white shine crossing its full width; Favourites keeps its yellow identity. Workflow/card/portal effects, header and Circuit Builder accents share visibility and page-lifecycle pausing. Dynamic project cards are observed after creation. The requested app branding remains always on, including explicit branding overrides on reduced-motion devices; functional UI reduced motion stays separate. The tester portal retains its existing preference control.

Artwork cohesion: a lightweight vector circuit pattern in headers; matching Survey dock and technical menu/modal headings. The Home-only logo removal, clean light side panel, original logo geometry/colours, drawing outputs and protected 24/7 build are preserved. Packaged APK downloads are unchanged by this web update.
