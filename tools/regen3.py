import json,re,glob,subprocess
root='/home/claude/treyvas/'
subprocess.run(['python3','/home/claude/regen.py'],check=True)
subprocess.run(['node','/home/claude/prerender2.js'],check=True,capture_output=True)
pre=json.load(open('/tmp/pre.json'))
files={'home':root+'index.html'}
for f in glob.glob(root+'*/index.html'):files[f.split('/')[-2]]=f
for k,f in files.items():
    if k not in pre:continue
    s=open(f).read()
    a=s.index('<main id="app">')+len('<main id="app">');b=s.index('</main>',a)
    s=s[:a]+pre[k]['main']+s[b:]
    s=re.sub(r'<html lang="ru"[^>]*>','<html lang="ru" class="v2">',s,1)
    m=re.search(r'(<nav id="nav"[^>]*>)(.*?)(</nav>)',s,re.S)
    if m and pre[k]['nav']:s=s[:m.start(2)]+pre[k]['nav']+s[m.end(2):]
    open(f,'w').write(s)
print('ok',len(files))
