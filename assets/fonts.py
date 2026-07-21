import re, urllib.request, base64, subprocess, sys
css=open('assets/inter.css',encoding='utf-8').read()
pairs=re.findall(r'font-weight:\s*(\d+);.*?url\((https://[^)]+\.(?:ttf|woff2))\)', css, re.S)
ua={'User-Agent':'Mozilla/5.0 Chrome/120'}
fetch=lambda url: urllib.request.urlopen(urllib.request.Request(url,headers=ua),timeout=60).read()
out=[]
def face(f,wt,d): out.append("@font-face{font-family:'%s';font-style:normal;font-weight:%d;font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');}"%(f,wt,base64.b64encode(d).decode()))
def subset(src_bytes_or_path, wt, family, uni):
    import tempfile, os
    if isinstance(src_bytes_or_path, bytes):
        tmp='assets/fonts/_tmp_%d.ttf'%wt; open(tmp,'wb').write(src_bytes_or_path); src=tmp
    else: src=src_bytes_or_path
    dst='assets/fonts/%s-%d.sub.woff2'%(family.replace(' ',''),wt)
    subprocess.run([sys.executable,'-m','fontTools.subset',src,'--unicodes='+uni,'--flavor=woff2','--output-file='+dst,'--no-hinting','--desubroutinize'],check=True)
    d=open(dst,'rb').read(); face(family,wt,d); print(family,wt,len(d)); 
    if isinstance(src_bytes_or_path, bytes): os.remove(src)
inter_uni="U+0020-007E,U+00A0-00FF,U+2013,U+2014,U+2018,U+2019,U+201C,U+201D,U+2022,U+2026,U+2039,U+203A,U+2192,U+2191,U+2193,U+2190,U+2713,U+25CF,U+25CB,U+21BA,U+2726,U+27A4,U+26A0,U+2261,U+00D7"
for wt,url in pairs:
    wt=int(wt); subset(fetch(url), wt, 'Inter', inter_uni)
gt_uni="U+0020-007E,U+00A0,U+00B7,U+2013,U+2014,U+2018,U+2019,U+201C,U+201D,U+2022,U+2026"
for src,wt in [('assets/fonts/GT-Standard-L-Extended-Medium.otf',500),('assets/fonts/GT-Standard-L-Extended-Bold.otf',700)]:
    subset(src, wt, 'GT Standard', gt_uni)
open('assets/fonts_embed.css','w',encoding='utf-8').write('\n'.join(out))
print('TOTAL base64 ~%dKB across %d faces'%(sum(len(x) for x in out)/1024, len(out)))
