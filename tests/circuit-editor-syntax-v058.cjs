const fs=require('fs'),vm=require('node:vm'),assert=require('node:assert/strict'),acorn=require('acorn');
const html=fs.readFileSync('index.html','utf8');
const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(m=>m[1]).filter(s=>s.trim());
assert(scripts.length,'No inline scripts found');
let failures=0;
function balanceTrace(code){
 const stack=[],pairs={'}':'{',')':'(',']':'[','${':'{'};
 const toks=acorn.tokenizer(code,{ecmaVersion:'latest',locations:true,allowHashBang:true});
 try{
  while(true){const t=toks.getToken(),label=t.type.label;if(label==='eof')break;if(label==='{'||label==='('||label==='['||label==='${')stack.push({label:label==='${'?'{':label,line:t.loc.start.line,col:t.loc.start.column,near:code.slice(Math.max(0,t.start-45),Math.min(code.length,t.end+70)).replace(/\s+/g,' ')});else if(label==='}'||label===')'||label===']'){const want=pairs[label],top=stack.at(-1);if(!top||top.label!==want){console.error(`DELIMITER_MISMATCH closing ${label} at ${t.loc.start.line}:${t.loc.start.column}; expected close for ${top?.label||'nothing'}`);break}stack.pop()}}
 }catch(e){console.error('TOKENIZER_ERROR '+(e.stack||e))}
 if(stack.length){console.error('UNCLOSED_DELIMITERS');for(const x of stack.slice(-12))console.error(`  ${x.label} opened at ${x.line}:${x.col} :: ${x.near}`)}
 return stack;
}
for(let i=0;i<scripts.length;i++){
 try{new vm.Script(scripts[i],{filename:`index-inline-${i+1}.js`})}
 catch(e){failures++;console.error(`INLINE_SCRIPT_${i+1}_SYNTAX_ERROR\n${e.stack||e}`);balanceTrace(scripts[i])}
}
if(failures)process.exit(1);
console.log(`PASS: ${scripts.length} inline script(s) parse cleanly`);
