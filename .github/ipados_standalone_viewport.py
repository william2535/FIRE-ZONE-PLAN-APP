from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

MARKER = '/* iPadOS standalone viewport fill — prevent exposed root strip at screen edge. */'
CSS = r'''

/* iPadOS standalone viewport fill — prevent exposed root strip at screen edge. */
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

if MARKER not in text:
    if '</style>' not in text:
        raise SystemExit('index.html: closing style tag not found')
    text = text.replace('</style>', CSS + '\n</style>', 1)
    p.write_text(text, encoding='utf-8')
    print('index.html: iPadOS standalone viewport fill installed')
else:
    print('index.html: iPadOS standalone viewport fill already current')

# Workflow trigger marker: standalone iPad viewport integration.
