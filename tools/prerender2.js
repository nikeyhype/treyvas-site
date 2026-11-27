const {JSDOM,VirtualConsole}=require('/tmp/node_modules/jsdom');const fs=require('fs');
const root='/home/claude/treyvas/';const html=fs.readFileSync(root+'index.html','utf8');
const pages=fs.readdirSync(root).filter(d=>fs.existsSync(root+d+'/index.html')&&!d.startsWith('.'));
const out={};
(async()=>{
for(const p of ['',...pages]){
  const vc=new VirtualConsole();let errs=[];vc.on('jsdomError',e=>errs.push(String(e.message||e).slice(0,120)));
  const dom=new JSDOM(html.replace(/<script[^>]*src=[^>]*><\/script>/g,''),{url:'https://treyvas.dev/'+(p?p+'/':''),runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
    w.matchMedia=()=>({matches:false,addEventListener(){},addListener(){}});w.IntersectionObserver=class{observe(){}disconnect(){}};w.ResizeObserver=class{observe(){}disconnect(){}};
    w.fetch=()=>Promise.reject('x');w.ym=()=>{};w.scrollTo=()=>{};w.HTMLMediaElement.prototype.play=()=>Promise.resolve();w.HTMLMediaElement.prototype.pause=()=>{};w.HTMLMediaElement.prototype.load=()=>{};
  }});
  await new Promise(r=>setTimeout(r,300));
  const d=dom.window.document;const app=d.getElementById('app');
  out[p||'home']={main:app?app.innerHTML:'',nav:d.getElementById('nav')?.innerHTML||'',v2:d.documentElement.classList.contains('v2'),errs:errs.slice(0,3)};
  dom.window.close();
}
fs.writeFileSync('/tmp/pre.json',JSON.stringify(out));
for(const [k,v] of Object.entries(out))console.log(k,v.v2,v.main.length,v.errs.join(' | '));
process.exit(0)})();
