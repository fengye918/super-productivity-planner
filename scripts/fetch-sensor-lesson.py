#!/usr/bin/env python3
"""Download latest authorized sensor lecture PDFs and render their final pages."""
from pathlib import Path
import importlib.util
import json
import requests
import fitz

ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location("zju_sync",ROOT/"scripts"/"fetch-zju-direct.py")
z=importlib.util.module_from_spec(spec)
spec.loader.exec_module(z)
inv=json.loads((ROOT/"data"/"sensor_lms_inventory.json").read_text(encoding="utf-8"))
assert inv["course"]["id"]==101075 and inv["course"]["name"]=="传感与检测"
latest=max(inv["activities"],key=lambda a:a.get("updated_at") or a.get("created_at") or "")
assert latest["id"]==1199023 and latest["type"]=="material",latest
assert len(latest.get("files",[]))==2
s=requests.Session()
s.headers.update({"User-Agent":z.UA,"Accept-Language":"zh-CN,zh;q=0.9,en;q=0.7"})
z.login_zjuam(s)
z.login_courses(s)
base=ROOT/"course_materials"/"传感与检测"/"课件"
preview=ROOT/"data"/"sensor_homework_previews"
base.mkdir(parents=True,exist_ok=True)
preview.mkdir(parents=True,exist_ok=True)
report={"course":inv["course"],"activity":{k:latest[k] for k in ("id","title","updated_at")},"materials":[]}
for entry in latest["files"]:
    upload=int(entry["id"])
    name=entry["name"]
    assert name.endswith(".pdf") and "/" not in name and ".." not in name
    print("Download",name,upload)
    resp=s.get(f"https://courses.zju.edu.cn/api/uploads/{upload}/blob",allow_redirects=True,timeout=65)
    resp.raise_for_status()
    assert resp.content[:4]==b"%PDF" and len(resp.content)>10000,(name,resp.status_code,resp.headers.get("Content-Type"))
    pdfpath=base/name
    pdfpath.write_bytes(resp.content)
    d=fitz.open(pdfpath)
    meta={"name":name,"upload_id":upload,"repo_path":pdfpath.relative_to(ROOT).as_posix(),"size":len(resp.content),"total_pages":len(d),"last_pages":[]}
    for pageno in range(max(0,len(d)-3),len(d)):
        page=d[pageno]
        txt=page.get_text("text",sort=True)
        pic=f"{upload}_p{pageno+1:02d}.png"
        page.get_pixmap(matrix=fitz.Matrix(1.65,1.65),alpha=False).save(str(preview/pic))
        meta["last_pages"].append({"page_num":pageno+1,"page_png":(preview/pic).relative_to(ROOT).as_posix(),"text":txt})
    report["materials"].append(meta)
(preview/"latest_materials.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print("Completed",len(report["materials"]),"source docs")
