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
            if line.startswith('\\ No newline') or not line:
                continue
            tag=line[0]; text=line[1:]
            if tag in (' ','-'): old.append(text)
            if tag in (' ','+'): new.append(text)
        hunks.append((header,old,new,body))
    return hunks


def replace_once(lines,old,new):
    if not old:
        raise RuntimeError('empty old hunk sequence')
    n=len(old)
    hits=[i for i in range(0,len(lines)-n+1) if lines[i:i+n]==old]
    if len(hits)!=1:
        raise RuntimeError(f'hunk context match count={len(hits)}')
    i=hits[0]
    return lines[:i]+new+lines[i+n:]


def preview(lines,limit=900,max_lines=18):
    changed=[]
    for line in lines:
        if line.startswith(('+','-')) and not line.startswith(('+++','---')):
            s=line.rstrip('\n')
            changed.append(s if len(s)<=limit else s[:limit]+' …[truncated]')
    return '\n'.join(changed[:max_lines])


def blocks_for(body):
    blocks=[]; i=0
    while i<len(body):
        line=body[i]
        if not line or line.startswith('\\ No newline') or line[0]==' ':
            i+=1; continue
        start=i
        while i<len(body):
            line=body[i]
            if not line or line.startswith('\\ No newline') or line[0]==' ':
                break
            i+=1
        blocks.append((start,i))
    return blocks


def hunk_variant(body,blocks,applied_count,partial_block=None,partial_plus=None):
    block_by_line={}
    for bi,(a,b) in enumerate(blocks):
        for j in range(a,b): block_by_line[j]=bi
    out=[]
    plus_seen={}
    for j,line in enumerate(body):
        if line.startswith('\\ No newline') or not line:
            continue
        tag=line[0]; text=line[1:]
        if tag==' ':
            out.append(text); continue
        bi=block_by_line[j]
        applied=bi<applied_count
        if partial_block is not None and bi==partial_block:
            if tag=='-':
                # For a pure insertion this does nothing; for replacements preserve old side.
                if any(body[k].startswith('-') for k in range(*blocks[bi])):
                    out.append(text)
            elif tag=='+':
                n=plus_seen.get(bi,0)
                if n<(partial_plus or 0): out.append(text)
                plus_seen[bi]=n+1
            continue
        if applied:
            if tag=='+': out.append(text)
        else:
            if tag=='-': out.append(text)
    return out


def line_label(line):
    raw=line[1:].strip() if line[:1] in '+-' else line.strip()
    m=re.match(r'function\s+([A-Za-z0-9_$]+)',raw)
    if m: return m.group(1)
    return raw[:120] or '<blank>'


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
    before=cur
    try:
        cur=replace_once(cur,old,new)
    except Exception as e:
        raise SystemExit(f'HUNK APPLY ERROR {idx} {header}: {e}\n{preview(body)}')
    ok,err=parse_html(''.join(cur),f'hunk {idx}')
    if ok:
        print(f'PASS hunk {idx} {header}')
        continue

    print(f'FIRST BAD HUNK {idx} {header}')
    print(preview(body))
    print(err)

    blocks=blocks_for(body)
    print(f'Granular check: {len(blocks)} change block(s) inside bad hunk')
    zero=hunk_variant(body,blocks,0)
    baseline=replace_once(before,old,zero)
    z_ok,z_err=parse_html(''.join(baseline),f'hunk {idx} zero changes')
    print('PASS zero-change reconstruction' if z_ok else 'ZERO-CHANGE RECONSTRUCTION FAILED')
    if not z_ok:
        print(z_err); raise SystemExit(1)

    bad_block=None
    for count in range(1,len(blocks)+1):
        variant=hunk_variant(body,blocks,count)
        candidate=replace_once(before,old,variant)
        b_ok,b_err=parse_html(''.join(candidate),f'hunk {idx} block {count}')
        a,b=blocks[count-1]
        if b_ok:
            print(f'PASS change block {count}: {line_label(body[a])}')
            continue
        bad_block=count-1
        print(f'FIRST BAD CHANGE BLOCK {count}:')
        print(preview(body[a:b]))
        print(b_err)
        break

    if bad_block is not None:
        a,b=blocks[bad_block]
        block=body[a:b]
        minus=[x for x in block if x.startswith('-')]
        plus=[x for x in block if x.startswith('+')]
        if not minus and plus:
            print(f'Refining pure insertion block across {len(plus)} added line(s)')
            for n in range(1,len(plus)+1):
                variant=hunk_variant(body,blocks,bad_block,partial_block=bad_block,partial_plus=n)
                candidate=replace_once(before,old,variant)
                l_ok,l_err=parse_html(''.join(candidate),f'hunk {idx} block {bad_block+1} line {n}')
                if l_ok:
                    print(f'PASS added line {n}: {line_label(plus[n-1])}')
                    continue
                print(f'FIRST BAD ADDED LINE {n}: {line_label(plus[n-1])}')
                raw=plus[n-1].rstrip('\n')
                print(raw if len(raw)<2000 else raw[:2000]+' …[truncated]')
                print(l_err)
                break
        else:
            print('Bad block is a replacement rather than a pure insertion; inspect this block directly.')
    raise SystemExit(1)

print('All original editor hunks parse cleanly; failure likely depends on later commit interaction or patch reconstruction.')
