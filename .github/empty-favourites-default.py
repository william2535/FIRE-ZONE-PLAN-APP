from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

old = "const defaultFavourites=['symbol:panel','symbol:repeater','symbol:you','tool:door','tool:wall','tool:pinNote'],legacyDefaultFavourites=['symbol:smoke','symbol:heat','symbol:mcp','tool:door','tool:wall','tool:pinNote'];let favourites=loadFavourites(),longPressTimer=null,longPressMessageTimer=null;\nfunction loadFavourites(){try{const saved=JSON.parse(localStorage.getItem('zoneSketchFavourites'));if(Array.isArray(saved)){const valid=[...new Set(saved)].filter(k=>favouriteCatalogue[k]);if(valid.join('|')===legacyDefaultFavourites.join('|'))return[...defaultFavourites];if(valid.length)return valid.slice(0,10)}}catch(e){}return [...defaultFavourites]}"
new = "const defaultFavourites=[],previousDefaultFavourites=['symbol:panel','symbol:repeater','symbol:you','tool:door','tool:wall','tool:pinNote'],legacyDefaultFavourites=['symbol:smoke','symbol:heat','symbol:mcp','tool:door','tool:wall','tool:pinNote'];let favourites=loadFavourites(),longPressTimer=null,longPressMessageTimer=null;\nfunction loadFavourites(){try{const saved=JSON.parse(localStorage.getItem('zoneSketchFavourites'));if(Array.isArray(saved)){const valid=[...new Set(saved)].filter(k=>favouriteCatalogue[k]);const key=valid.join('|');if(key===legacyDefaultFavourites.join('|')||key===previousDefaultFavourites.join('|'))return[];return valid.slice(0,10)}}catch(e){}return[]}"

if new in text:
    print('index.html: favourites already default to empty')
elif old in text:
    text = text.replace(old, new, 1)
    p.write_text(text, encoding='utf-8')
    print('index.html: default favourites cleared; custom saved favourites preserved')
else:
    raise SystemExit('Expected favourites default block not found')
