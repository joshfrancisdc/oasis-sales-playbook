import io
html=open('index.html',encoding='utf-8').read()
fonts=open('assets/fonts_embed.css',encoding='utf-8').read()
dark=open('assets/logo/DXC-Horizontal-Tagline-Full-Color-Dark.svg',encoding='utf-8').read().strip()
light=open('assets/logo/DXC-Horizontal-Tagline-Full-Color-Light.svg',encoding='utf-8').read().strip()
# strip any xml prolog
for s in ('dark','light'):
    pass
def clean(svg):
    i=svg.find('<svg'); return svg[i:] if i>=0 else svg
dark=clean(dark); light=clean(light)
assert '/*@FONTS@*/' in html, 'fonts marker missing'
assert '<!--@LOGO_DARK@-->' in html, 'logo dark marker missing'
assert html.count('<!--@LOGO_LIGHT@-->')>=2, 'logo light markers missing'
html=html.replace('/*@FONTS@*/', '/* embedded DXC fonts */\n'+fonts)
html=html.replace('<!--@LOGO_DARK@-->', dark)
html=html.replace('<!--@LOGO_LIGHT@-->', light)
open('index.html','w',encoding='utf-8').write(html)
print('injected: fonts %dKB, dark svg %dB, light svg %dB'%(len(fonts)/1024,len(dark),len(light)))
print('final index.html %dKB'%(len(html)/1024))
