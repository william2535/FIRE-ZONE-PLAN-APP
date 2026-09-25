const fs=require('fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('index.html','utf8');
const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(m=>m[1]).filter(s=>s.trim());
assert(scripts.length,'No inline scripts found');
let failures=0;
for(let i=0;i<scripts.length;i++){
  try{new vm.Script(scripts[i],{filename:`index-inline-${i+1}.js`})}
  catch(e){failures++;console.error(`INLINE_SCRIPT_${i+1}_SYNTAX_ERROR\n${e.stack||e}`)}
}
if(failures)process.exit(1);
console.log(`PASS: ${scripts.length} inline script(s) parse cleanly`);
