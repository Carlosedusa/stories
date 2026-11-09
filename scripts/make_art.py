import sys, json, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n=int(sys.argv[1]); P=json.load(open(f"{ROOT}/pillars.json"))[n-1]
photos=sorted(os.listdir(f"{ROOT}/photos")); src=f"{ROOT}/photos/{photos[(n-1)%len(photos)]}"
B="/usr/share/fonts/opentype/inter/Inter-Bold.otf"; X="/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"; R="/usr/share/fonts/opentype/inter/Inter-Medium.otf"
def make(W,H,out):
    im=Image.open(src).convert("RGB"); s=max(W/im.width,H/im.height)
    im=im.resize((int(im.width*s)+1,int(im.height*s)+1),Image.LANCZOS); l=(im.width-W)//2; t=(im.height-H)//2
    im=ImageEnhance.Brightness(im.crop((l,t,l+W,t+H))).enhance(0.8)
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    for y in range(H):
        a=int(215*min(1,max(0,(y-H*0.18)/(H*0.5)))) if y>H*0.18 else 0
        d.line([(0,y),(W,y)],fill=(0,0,0,max(a,int(150*max(0,1-y/(H*0.22))))))
    im=Image.alpha_composite(im.convert("RGBA"),ov); d=ImageDraw.Draw(im)
    m=int(W*0.07); ora=(255,138,0); f=lambda p,s: ImageFont.truetype(p,s)
    d.text((m,int(H*0.05)),f"PSM  |  PILAR {n} DE 14",font=f(B,int(W*0.038)),fill=ora)
    d.text((m,int(H*0.05)+int(W*0.06)),"Segurança de Processo",font=f(R,int(W*0.034)),fill=(235,235,235))
    def wrap(txt,font,mw):
        o=[];c=""
        for w in txt.split():
            t=(c+" "+w).strip()
            if d.textlength(t,font=font)<=mw: c=t
            else: o.append(c);c=w
        o.append(c);return o
    th=f(X,int(W*0.098)); body=f(B,int(W*0.047)); foot=f(B,int(W*0.036))
    tl=wrap(P["title"],th,W-2*m); bl=wrap(P["body"],body,W-2*m)
    lh=int(th.size*1.12); bh=int(body.size*1.4); fy=H-int(H*0.065)-foot.size
    by=fy-int(H*0.035)-len(bl)*bh; ty=by-int(H*0.03)-len(tl)*lh
    d.rectangle([m,ty-int(H*0.022),m+int(W*0.14),ty-int(H*0.022)+8],fill=ora)
    y=ty
    for ln in tl: d.text((m,y),ln,font=th,fill=(255,255,255)); y+=lh
    y=by
    for ln in bl: d.text((m,y),ln,font=body,fill=(240,240,240)); y+=bh
    d.text((m,fy),"@cruz.engenharia.ltda",font=foot,fill=ora)
    d.text((W-m-d.textlength("Cruz Engenharia",font=foot),fy),"Cruz Engenharia",font=foot,fill=(235,235,235))
    im.convert("RGB").save(out,quality=88)
d=f"{ROOT}/out/pilar{n:02d}"; os.makedirs(d,exist_ok=True)
make(1080,1350,f"{d}/feed.jpg"); make(1080,1920,f"{d}/story.jpg"); print(d)
