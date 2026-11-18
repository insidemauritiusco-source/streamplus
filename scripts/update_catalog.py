#!/usr/bin/env python3
"""Refresh StreamPlus movie discovery catalog using Apple's public search API."""
import json,datetime,urllib.request,urllib.parse,time,pathlib
terms=["2026 movie","2025 movie","2024 movie","Bollywood movie","action movie","animation movie"]
movies={}
for term in terms:
 try:
  params=urllib.parse.urlencode({"term":term,"country":"us","media":"movie","entity":"movie","limit":100})
  req=urllib.request.Request("https://itunes.apple.com/search?"+params,headers={"User-Agent":"StreamPlusCatalog/1.0"})
  with urllib.request.urlopen(req,timeout=20) as response: data=json.load(response)
  for m in data.get("results",[]):
   if m.get("kind")!="feature-movie" or not all(m.get(k) for k in ("trackId","trackName","trackViewUrl","artworkUrl100")):continue
   poster=m["artworkUrl100"].replace("100x100bb","600x900bb")
   movies[str(m["trackId"])]={"id":m["trackId"],"title":m["trackName"],"release":m.get("releaseDate",""),"genre":m.get("primaryGenreName","Movie"),"poster":poster,"link":m["trackViewUrl"],"preview":m.get("previewUrl",""),"description":m.get("longDescription") or m.get("shortDescription",""),"duration":round(m["trackTimeMillis"]/60000) if m.get("trackTimeMillis") else None,"rating":m.get("contentAdvisoryRating","")}
 except Exception as exc:print("Warning:",term,str(exc))
 time.sleep(1)
path=pathlib.Path("catalog.json")
if movies:
 items=sorted(movies.values(),key=lambda m:m["release"],reverse=True)
 path.write_text(json.dumps({"updated":datetime.datetime.now(datetime.timezone.utc).isoformat(),"items":items},ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
 print("Updated",len(items),"movies")
else:
 print("No API results; leaving existing catalog untouched")
