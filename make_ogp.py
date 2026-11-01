#!/usr/bin/env python3
# OGP画像(ogp.png 1200x630) と favicon.png を生成。
# 使い方: ./.venv/bin/python make_ogp.py
import json, os, re, io, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE=os.path.dirname(os.path.abspath(__file__))
CACHE=os.path.join(HERE,".build_icons"); os.makedirs(CACHE,exist_ok=True)

# data.js からアイコンURLを取得
src=open(os.path.join(HERE,"data.js"),encoding="utf-8").read()
data=json.loads(src[src.index("["):src.rindex("]")+1])
icons=[a["icon"] for g in data for a in g["apps"]]

def fetch(url):
    key=os.path.join(CACHE, re.sub(r'\W','_',url)[-80:]+".png")
    if not os.path.exists(key):
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req,timeout=20) as r: open(key,"wb").write(r.read())
    return Image.open(key).convert("RGBA")

def rounded(im,size,rad):
    im=ImageOps.fit(im,(size,size),Image.LANCZOS)
    mask=Image.new("L",(size,size),0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,size,size],radius=rad,fill=255)
    out=Image.new("RGBA",(size,size),(0,0,0,0)); out.paste(im,(0,0),mask); return out

def vgrad(w,h,top,bot):
    base=Image.new("RGB",(w,h),top)
    for y in range(h):
        t=y/h; c=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3))
        ImageDraw.Draw(base).line([(0,y),(w,y)],fill=c)
    return base

def font(sz,bold=False):
    try: return ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", sz, index=1 if bold else 0)
    except Exception:
        try: return ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", sz)
        except Exception: return ImageFont.load_default()

# ---- OGP 1200x630 ----
W,H=1200,630
img=vgrad(W,H,(244,248,249),(224,232,236)).convert("RGBA")
d=ImageDraw.Draw(img)
d.text((70,74),  "つくったもの棚", font=font(70,True), fill=(31,43,51))
d.text((74,170), "D.Seto — 瀬戸大作が作った 24 のアプリ", font=font(30), fill=(79,111,120))
d.text((76,214), "apps as gateways", font=font(20), fill=(130,150,160))

# アイコングリッド 8x3
cols,rows,ic,gap=8,3,96,18
gw=cols*ic+(cols-1)*gap
sx=(W-gw)//2; sy=288
for i,url in enumerate(icons[:cols*rows]):
    try: tile=rounded(fetch(url),ic,int(ic*0.22))
    except Exception: continue
    x=sx+(i%cols)*(ic+gap); y=sy+(i//cols)*(ic+gap)
    sh=Image.new("RGBA",(ic+10,ic+10),(0,0,0,0))
    ImageDraw.Draw(sh).rounded_rectangle([5,8,ic+5,ic+8],radius=int(ic*0.22),fill=(20,50,70,60))
    img.alpha_composite(sh,(x-5,y-5)); img.alpha_composite(tile,(x,y))
img.convert("RGB").save(os.path.join(HERE,"ogp.png"),quality=92)
print("wrote ogp.png")

# ---- favicon 256x256（池テーマの雫マーク）----
S=256; fav=vgrad(S,S,(79,170,180),(47,111,143)).convert("RGBA")
m=Image.new("L",(S,S),0); ImageDraw.Draw(m).rounded_rectangle([0,0,S,S],radius=56,fill=255)
fav.putalpha(m)
fd=ImageDraw.Draw(fav)
# 水面の波3本
for k,yy in enumerate((150,180,210)):
    fd.arc([40-k*6,yy-30,216+k*6,yy+30],180,360,fill=(255,255,255,120+k*20),width=7)
# 雫
fd.ellipse([103,58,153,108],fill=(255,255,255,235))
fd.polygon([(128,40),(108,78),(148,78)],fill=(255,255,255,235))
fav.save(os.path.join(HERE,"favicon.png"))
print("wrote favicon.png")
