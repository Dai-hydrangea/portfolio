#!/usr/bin/env python3
# stories.md（紹介文の原本）＋ raw.json（Apple lookup）から data.js を生成する。
# 使い方: python3 build_data.py
import json, re, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))

# ジャンル構成（表示順）。各アプリは trackId で stories.md / raw.json と対応。
GROUPS=[
 ("音楽","music",[6761473626,6818659518,6770044564,6761536209,6770239687]),
 ("ゲーム","games",[6814348109,6815019523,6821778220,6782213686]),
 ("対話","dialogue",[6761684130,6762501528,6762042775,6767699405,6816667779,6814029651]),
 ("ツール","tools",[6823900768,6761721069,6780187534,6800747512]),
 ("その他","others",[6767963171,6775810849,6766134357,6761618784,6763751678]),
]

def parse_stories(path):
    txt=open(path,encoding="utf-8").read()
    stories={}; cur=None; buf=[]
    for line in txt.split("\n"):
        m=re.match(r'^###\s+.*\(id:\s*(\d+)\)\s*$', line)
        if m:
            if cur is not None: stories[cur]="\n".join(buf).strip()
            cur=int(m.group(1)); buf=[]
        elif line.startswith("## ") or line.startswith("# "):
            if cur is not None: stories[cur]="\n".join(buf).strip(); cur=None; buf=[]
        elif cur is not None:
            buf.append(line)
    if cur is not None: stories[cur]="\n".join(buf).strip()
    return stories

def shots(r):
    return [re.sub(r'/\d+x\d+bb\.(jpg|png|jpeg)$', r'/600x0w.\1', s) for s in r.get("screenshotUrls",[])]

raw=json.load(open(os.path.join(HERE,"raw.json")))
apps={r["trackId"]:r for r in raw["results"] if r.get("wrapperType")!="artist"}
stories=parse_stories(os.path.join(HERE,"stories.md"))

data=[]; missing=[]
for verb,en,ids in GROUPS:
    out=[]
    for tid in ids:
        r=apps.get(tid)
        if not r: missing.append(("raw",tid)); continue
        st=stories.get(tid,"")
        if not st: missing.append(("story",tid))
        out.append({"name":r["trackName"],"id":tid,"url":r["trackViewUrl"].split("?")[0],
            "icon":r.get("artworkUrl512") or r.get("artworkUrl100"),
            "genreName":r.get("primaryGenreName"),"price":r.get("formattedPrice"),
            "shots":shots(r),"story":st})
    data.append({"verb":verb,"en":en,"apps":out})

with open(os.path.join(HERE,"data.js"),"w",encoding="utf-8") as f:
    f.write("// 自動生成: build_data.py (stories.md + raw.json より)。手で編集しない。\n")
    f.write("window.DATA = "+json.dumps(data,ensure_ascii=False,indent=1)+";\n")

n=sum(len(g['apps']) for g in data)
print(f"wrote data.js: {len(data)} genres / {n} apps")
if missing: print("WARN missing:",missing)
else: print("all stories matched OK")
