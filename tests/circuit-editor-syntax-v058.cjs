const fs=require('fs'),vm=require('node:vm'),assert=require('node:assert/strict'),acorn=require('acorn');
const html=fs.readFileSync('index.html','utf8');
const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(m=>m[1]).filter(s=>s.trim());
assert(scripts.length,'No inline scripts found');
let failures=0;
function balanceTrace(code){
 const stack=[],pairs={'}':'{',')':'(',']':'[','${':'{'},tokens=[];
 const toks=acorn.tokenizer(code,{ecmaVersion:'latest',locations:true,allowHashBang:true});
 try{
  while(true){const t=toks.getToken(),label=t.type.label;tokens.push(t);if(label==='eof')break;if(label==='{'||label==='('||label==='['||label==='${')stack.push({label:label==='${'?'{':label,line:t.loc.start.line,col:t.loc.start.column,near:code.slice(Math.max(0,t.start-45),Math.min(code.length,t.end+70)).replace(/\s+/g,' ')});else if(label==='}'||label===')'||label===']'){const want=pairs[label],top=stack.at(-1);if(!top||top.label!==want){console.error(`DELIMITER_MISMATCH closing ${label} at ${t.loc.start.line}:${t.loc.start.column}; expected close for ${top?.label||'nothing'}`);break}stack.pop()}}
 }catch(e){console.error('TOKENIZER_ERROR '+(e.stack||e))}
 if(stack.length){console.error('UNCLOSED_DELIMITERS');for(const x of stack.slice(-12))console.error(`  ${x.label} opened at ${x.line}:${x.col} :: ${x.near}`)}
 // Trace named cb* function declarations and their brace nesting. Top-level app functions should begin at brace depth 1 (the IIFE).
 let braceDepth=0,firstNested=null,lastTop=null;
 for(let i=0;i<tokens.length;i++){
  const t=tokens[i],label=t.type.label;
  if((t.type.keyword==='function'||label==='function')){
   const m=/^function\s+(cb[A-Za-z0-9_$]*)/.exec(code.slice(t.start,t.start+90));
   if(m){const rec={name:m[1],depth:braceDepth,line:t.loc.start.line};if(braceDepth===1)lastTop=rec;else if(braceDepth>1&&!firstNested){firstNested=rec;console.error(`FIRST_NESTED_CB_FUNCTION ${rec.name} depth=${rec.depth} line=${rec.line}`);if(lastTop)console.error(`LAST_TOP_LEVEL_CB_FUNCTION ${lastTop.name} depth=${lastTop.depth} line=${lastTop.line}`)}}
  }
  if(label==='{')braceDepth++;else if(label==='}')braceDepth--;
 }
 return stack;
}
for(let i=0;i<scripts.length;i++){
 try{new vm.Script(scripts[i],{filename:`index-inline-${i+1}.js`})}
 catch(e){failures++;console.error(`INLINE_SCRIPT_${i+1}_SYNTAX_ERROR\n${e.stack||e}`);balanceTrace(scripts[i])}
}
if(failures)process.exit(1);
console.log(`PASS: ${scripts.length} inline script(s) parse cleanly`);
