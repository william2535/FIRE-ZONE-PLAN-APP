from pathlib import Path

old="http.createServer((q,r)=>r.end(fs.readFileSync('index.html')))"
new="http.createServer((q,r)=>{const path=(q.url||'/').split('?')[0],file=path==='/'?'index.html':path.slice(1);try{const data=fs.readFileSync(file);r.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':file.endsWith('.pdf')?'application/pdf':'text/html');r.end(data)}catch(e){r.statusCode=404;r.end('not found')}})"
old_browser="http.createServer((req,res)=>{res.setHeader('Content-Type','text/html');res.end(html)})"
new_browser="http.createServer((req,res)=>{const path=(req.url||'/').split('?')[0],file=path==='/'?'index.html':path.slice(1);try{const data=fs.readFileSync(file);res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':file.endsWith('.pdf')?'application/pdf':'text/html');res.end(data)}catch(e){res.statusCode=404;res.end('not found')}})"

changed=[]
for path in sorted(Path('tests').glob('*.cjs')):
    if path.name == 'plan-tools-v027.cjs':
        continue
    text=path.read_text()
    updated=text.replace(old,new,1).replace(old_browser,new_browser,1)
    if updated != text:
        path.write_text(updated)
        changed.append(path.as_posix())

if not changed:
    print('No legacy single-file test servers needed updating')
else:
    print('Updated static test servers:')
    for path in changed:
        print(' -',path)
