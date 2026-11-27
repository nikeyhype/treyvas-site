import re,glob,time,sys
root='/home/claude/treyvas/'
new=open(root+'index.html').read()
build=str(int(time.time()))
new=re.sub(r'const BUILD="\d+"',f'const BUILD="{build}"',new)
open(root+'index.html','w').write(new)
head_new,rest=new.split('<main id="app">',1)
_,tail_new=rest.split('</main>',1)
pats=[r'<meta name="description"[^>]*>',r'<title>.*?</title>',r'<link rel="canonical"[^>]*>',r'<meta property="og:title"[^>]*>',r'<meta property="og:description"[^>]*>',r'<meta property="og:url"[^>]*>',r'<meta property="og:image"[^>]*>',r'<meta name="twitter:[^>]*>']
files=glob.glob(root+'*/index.html')+[root+'404.html']
for f in files:
    old=open(f).read()
    oh,orest=old.split('<main id="app">',1)
    omain,_=orest.split('</main>',1)
    h=head_new
    # robots noindex etc: take whole <head> meta region from old for listed tags
    for p in pats:
        on=re.findall(p,oh,re.S);nn=re.findall(p,h,re.S)
        if len(on)==len(nn) and on:
            for a,b in zip(nn,on):h=h.replace(a,b,1)
    if '<meta name="robots" content="noindex">' in oh and 'noindex' not in h:
        h=h.replace('<title>','<meta name="robots" content="noindex">\n<title>',1)
    open(f,'w').write(h+'<main id="app">'+omain+'</main>'+tail_new)
print(len(files),build)
