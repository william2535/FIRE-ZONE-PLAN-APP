from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

OLD = r'''/* iPadOS standalone viewport fill — prevent exposed root strip at screen edge. */
html{min-width:100%;min-height:100%;background:#020a10}
body{min-width:100%;min-height:100%;background:#020a10}

/* Keep the normal browser layout unchanged. In an installed iOS/iPadOS web app,
   anchor the document to the standalone visual viewport rather than relying only
   on 100dvh, which can leave a thin uncovered strip after rotation/resizing. */
@media (display-mode:standalone){
  html,body{width:100%;height:100%;min-height:100%;background:#020a10;overflow:hidden;overscroll-behavior:none}
  body{position:fixed;inset:0}
  .app{width:100%;height:100%;min-height:100%;max-height:100%;overflow:hidden}
  #projectsHome{inset:0;width:100%;height:100%;min-height:100%;max-height:none;background-color:#020a10;padding-bottom:calc(36px + env(safe-area-inset-bottom))}
}

/* Safari's installed-web-app implementation also exposes this feature test on
   older iPadOS releases. It is intentionally limited to standalone mode above. */
@supports (-webkit-touch-callout:none){
  @media (display-mode:standalone){
    html,body,.app,#projectsHome{min-height:-webkit-fill-available}
  }
}
'''

CSS = r'''/* iOS/iPadOS standalone viewport fill — prevent exposed root strip at screen edge. */
html{min-width:100%;min-height:100%;background:#020a10}
body{min-width:100%;min-height:100%;background:#020a10}

/* Keep normal Safari/browser sizing untouched. Installed iPhone/iPad web apps
   get an explicit full-screen box so WebKit cannot leave its pale window surface
   exposed below the app after a viewport or safe-area recalculation. */
@media (display-mode:standalone){
  html,body{width:100%;height:100vh;min-height:100vh;background:#020a10;overflow:hidden;overscroll-behavior:none}
  body{position:fixed;inset:0}
  .app{width:100%;height:100vh;min-height:100vh;max-height:100vh;overflow:hidden;background:#020a10}
  #projectsHome{inset:0;width:100%;height:100vh;min-height:100vh;max-height:100vh;background-color:#020a10;padding-bottom:calc(36px + env(safe-area-inset-bottom));box-sizing:border-box}
}

/* Older installed WebKit builds use fill-available. Keep it as the fallback only. */
@supports (-webkit-touch-callout:none){
  @media (display-mode:standalone){
    html,body,.app,#projectsHome{min-height:-webkit-fill-available}
  }
}

/* Modern iOS/iPadOS: dynamic viewport units must win over percentage/fill-available
   sizing. This is the important iPhone fix for the bottom standalone strip. */
@supports (height:100dvh){
  @media (display-mode:standalone){
    html,body{height:100dvh;min-height:100dvh}
    .app,#projectsHome{height:100dvh;min-height:100dvh;max-height:100dvh}
  }
}
'''

if CSS in text:
    print('index.html: iOS/iPadOS standalone viewport fill already current')
elif OLD in text:
    text = text.replace(OLD, CSS, 1)
    p.write_text(text, encoding='utf-8')
    print('index.html: standalone viewport fill upgraded for iPhone and iPad')
elif 'standalone viewport fill' in text:
    raise SystemExit('index.html: an unknown standalone viewport block already exists')
else:
    # A previous motion-refresh helper used to replace everything through </style>,
    # which could remove this later CSS block. That helper is now bounded by its own
    # end marker, so it is safe to restore this block once at the end of the style.
    if '</style>' not in text:
        raise SystemExit('index.html: closing style tag not found')
    text = text.replace('</style>', CSS + '\n</style>', 1)
    p.write_text(text, encoding='utf-8')
    print('index.html: missing iOS/iPadOS standalone viewport fill restored')

# Workflow trigger marker: standalone iOS/iPadOS viewport integration.
