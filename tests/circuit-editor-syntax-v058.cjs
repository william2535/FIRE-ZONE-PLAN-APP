const fs=require('fs'),vm=require('node:vm'),assert=require('node:assert/strict'),acorn=require('acorn');
const html=fs.readFileSync('index.html','utf8');
const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(m=>m[1]).filter(s=>s.trim());
assert(scripts.length,'No inline scripts found');
let failures=0;
function snippet(code,pos,r=120){return code.slice(Math.max(0,pos-r),Math.min(code.length,pos+r)).replace(/\s+/g,' ')}
function balanceTrace(code){
 const stack=[],pairs={'}':'{',')':'(',']':'[','${':'{'},tokens=[];
 const toks=acorn.tokenizer(code,{ecmaVersion:'latest',locations:true,allowHashBang:true});
 try{
  while(true){const t=toks.getToken(),label=t.type.label;tokens.push(t);if(label==='eof')break;if(label==='{'||label==='('||label==='['||label==='${')stack.push({label:label==='${'?'{':label,line:t.loc.start.line,col:t.loc.start.column,start:t.start,near:snippet(code,t.start,70)});else if(label==='}'||label===')'||label===']'){const want=pairs[label],top=stack.at(-1);if(!top||top.label!==want){console.error(`DELIMITER_MISMATCH closing ${label} at ${t.loc.start.line}:${t.loc.start.column}; expected close for ${top?.label||'nothing'}`);break}stack.pop()}}
 }catch(e){console.error('TOKENIZER_ERROR '+(e.stack||e))}
 if(stack.length){console.error('UNCLOSED_DELIMITERS');for(const x of stack.slice(-16))console.error(`  ${x.label} opened at ${x.line}:${x.col} :: ${x.near}`)}
 let braceDepth=0,lastDepthOnePos=0,lastDepthOneLine=1,lastTopFunction=null,firstNestedFunction=null;
 const depthRecords=[];
 for(let i=0;i<tokens.length;i++){
  const t=tokens[i],label=t.type.label;
  if(label==='{' )braceDepth++;
  else if(label==='}')braceDepth--;
  if(braceDepth===1){lastDepthOnePos=t.end;lastDepthOneLine=t.loc.end.line}
  if((t.type.keyword==='function'||label==='function')){
   const m=/^function\s+([A-Za-z_$][\w$]*)/.exec(code.slice(t.start,t.start+120));
   if(m){const rec={name:m[1],depth:braceDepth,line:t.loc.start.line,pos:t.start};depthRecords.push(rec);if(braceDepth===1)lastTopFunction=rec;else if(braceDepth>1&&!firstNestedFunction)firstNestedFunction=rec}
  }
 }
 console.error(`LAST_IIFE_TOP_LEVEL_TOKEN line=${lastDepthOneLine} pos=${lastDepthOnePos} :: ${snippet(code,lastDepthOnePos)}`);
 if(lastTopFunction)console.error(`LAST_TOP_LEVEL_FUNCTION ${lastTopFunction.name} depth=${lastTopFunction.depth} line=${lastTopFunction.line}`);
 const firstAfter=depthRecords.find(r=>r.pos>lastDepthOnePos);
 if(firstAfter)console.error(`FIRST_FUNCTION_AFTER_TOP_LEVEL_LOSS ${firstAfter.name} depth=${firstAfter.depth} line=${firstAfter.line} :: ${snippet(code,firstAfter.pos)}`);
 if(firstNestedFunction)console.error(`FIRST_NESTED_FUNCTION ${firstNestedFunction.name} depth=${firstNestedFunction.depth} line=${firstNestedFunction.line}`);
 const lastFns=depthRecords.slice(-12).map(r=>`${r.name}@${r.line}:d${r.depth}`).join(' | ');if(lastFns)console.error('LAST_FUNCTION_DEPTHS '+lastFns);
 console.error(`FINAL_BRACE_DEPTH ${braceDepth}`);
 return stack;
}
for(let i=0;i<scripts.length;i++){
 try{new vm.Script(scripts[i],{filename:`index-inline-${i+1}.js`})}
 catch(e){failures++;console.error(`INLINE_SCRIPT_${i+1}_SYNTAX_ERROR\n${e.stack||e}`);balanceTrace(scripts[i])}
}
if(failures)process.exit(1);
console.log(`PASS: ${scripts.length} inline script(s) parse cleanly`);
