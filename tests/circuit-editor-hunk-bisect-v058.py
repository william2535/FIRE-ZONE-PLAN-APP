import re
import subprocess
import tempfile
from pathlib import Path

GOOD='fcd59d236411c41e48383b774fbc632c4ebf0e16'
BAD='c8b76b265702b6667fe780fca360c7e68393ce0a'
TARGET='index.html'


def run(*args, check=True):
    p=subprocess.run(args,text=True,capture_output=True)
    if check and p.returncode:
        raise SystemExit((p.stdout or '')+(p.stderr or ''))
    return p


def git_text(*args):
    return run('git',*args).stdout


def inline_scripts(html):
    return [m.group(1) for m in re.finditer(r'<script(?:\s[^>]*)?>([\s\S]*?)</script>',html,re.I) if m.group(1).strip()]


def parse_html(html,label):
    scripts=inline_scripts(html)
    if not scripts:
        return False,'no inline scripts found'
    for i,code in enumerate(scripts,1):
        with tempfile.NamedTemporaryFile('w',suffix='.js',encoding='utf-8',delete=False) as f:
            f.write(code)
            path=f.name
        p=run('node','--check',path,check=False)
        Path(path).unlink(missing_ok=True)
        if p.returncode:
            return False,f'{label} inline script {i}:\n{p.stderr or p.stdout}'
    return True,''


def parse_hunks(diff):
    lines=diff.splitlines(keepends=True)
    hunks=[]
    i=0
    while i<len(lines):
        if not lines[i].startswith('@@ '):
            i+=1; continue
        header=lines[i].rstrip('\n')
        i+=1
        body=[]
        while i<len(lines) and not lines[i].startswith('@@ '):
            if lines[i].startswith(('diff --git ','index ','--- ','+++ ')):
                i+=1; continue
            body.append(lines[i]); i+=1
        old=[]; new=[]
        for line in body:
            if line.startswith('\\ No newline'):
                continue
            if not line:
                continue
            tag=line[0]
            text=line[1:]
            if tag in (' ','-'): old.append(text)
            if tag in (' ','+'): new.append(text)
        hunks.append((header,old,new,body))
    return hunks


def replace_once(lines,old,new):
    if not old:
        raise RuntimeError('empty old hunk sequence')
    n=len(old)
    hits=[]
    for i in range(0,len(lines)-n+1):
        if lines[i:i+n]==old:
            hits.append(i)
    if len(hits)!=1:
        raise RuntimeError(f'hunk context match count={len(hits)}')
    i=hits[0]
    return lines[:i]+new+lines[i+n:]


def preview(body,limit=900):
    changed=[]
    for line in body:
        if line.startswith(('+','-')) and not line.startswith(('+++','---')):
            s=line.rstrip('\n')
            changed.append(s if len(s)<=limit else s[:limit]+' …[truncated]')
    return '\n'.join(changed[:14])


good=git_text('show',f'{GOOD}:{TARGET}')
ok,err=parse_html(good,'GOOD')
if not ok:
    raise SystemExit('Known-good baseline does not parse:\n'+err)
print(f'PASS baseline {GOOD[:8]} parses cleanly')

diff=git_text('diff','--no-color','--unified=3',GOOD,BAD,'--',TARGET)
hunks=parse_hunks(diff)
if not hunks:
    raise SystemExit('No hunks found')
print(f'Applying {len(hunks)} original editor hunks in order')

cur=good.splitlines(keepends=True)
for idx,(header,old,new,body) in enumerate(hunks,1):
    try:
        cur=replace_once(cur,old,new)
    except Exception as e:
        raise SystemExit(f'HUNK APPLY ERROR {idx} {header}: {e}\n{preview(body)}')
    html=''.join(cur)
    ok,err=parse_html(html,f'hunk {idx}')
    if not ok:
        print(f'FIRST BAD HUNK {idx} {header}')
        print(preview(body))
        print(err)
        raise SystemExit(1)
    print(f'PASS hunk {idx} {header}')

print('All original editor hunks parse cleanly; failure likely depends on later commit interaction or patch reconstruction.')
