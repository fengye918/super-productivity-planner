#!/usr/bin/env python3
"""Survey only the authenticated 传感与检测 course's accessible lecture resources."""
import importlib.util
import json
from pathlib import Path
from urllib.parse import urlencode
import requests

ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location("zju_sync",ROOT/"scripts"/"fetch-zju-direct.py")
z=importlib.util.module_from_spec(spec)
spec.loader.exec_module(z)
s=requests.Session()
s.headers.update({"User-Agent":z.UA,"Accept-Language":"zh-CN,zh;q=0.9,en;q=0.7"})
report={"course":None,"course_count":0,"activities":[],"errors":[],"file_candidates":[]}

def safe_json(path):
    try:
        return z.api_json(s,path)
    except Exception as exc:
        report["errors"].append({"request_path":path.split("courses.zju.edu.cn")[-1].split("?")[0],"error":type(exc).__name__})
        return {}

def meta(a):
    return {k:a.get(k) for k in ("id","title","name","type","created_at","updated_at","start_time","end_time","published","is_locked","course_id","position","sort","order") if isinstance(a,dict) and k in a}

try:
    z.login_zjuam(s)
    try:
        z.login_courses(s)
    except requests.HTTPError as login_error:
        # Course SSO occasionally returns HTTP 401 after CAS login.
        # Retry the explicit CAS service flow without exposing tokens.
        print("Courses SSO initial retry:", type(login_error).__name__)
        from urllib.parse import quote
        service="https://courses.zju.edu.cn/user/index"
        u="https://zjuam.zju.edu.cn/cas/login?service="+quote(service,safe="")
        step=s.get(u,allow_redirects=True,timeout=45)
        print("Explicit service SSO status:",step.status_code,step.url.split("?")[0])
        try:
            z.login_courses(s)
        except requests.HTTPError:
            # Last attempt: new session, fresh CAS cookies and a fresh SSO ticket.
            print("Retrying with a fresh CAS session.")
            s=requests.Session()
            s.headers.update({"User-Agent":z.UA,"Accept-Language":"zh-CN,zh;q=0.9,en;q=0.7"})
            z.login_zjuam(s)
            second=s.get(u,allow_redirects=True,timeout=45)
            print("Fresh explicit SSO status:",second.status_code,second.url.split("?")[0])
            z.login_courses(s)
    sem=safe_json("https://courses.zju.edu.cn/api/my-semesters?fields=id,name,sort,is_active,code")
    semesters=sem.get("semesters",[])
    ids=[]
    for x in semesters:
        if x.get("is_active") and isinstance(x.get("id"),int):
            ids.extend([x["id"],x["id"]+1,x["id"]+2])
    filters={"page":1,"page_size":1000,"sort":"all","normal":json.dumps({"version":7,"apiVersion":"1.1.0"}),
             "conditions":json.dumps({"role":[],"semester_id":sorted(set(ids)),"academic_year_id":[],
               "status":["ongoing","notStarted"],"course_type":[],"effectiveness":[],
               "published":[],"display_studio_list":False},ensure_ascii=False),
             "fields":"id,name,course_code"}
    courses=safe_json("https://courses.zju.edu.cn/api/my-courses?"+urlencode(filters)).get("courses",[])
    report["course_count"]=len(courses)
    matching=[c for c in courses if ("传感" in str(c.get("name","")) and "检测" in str(c.get("name","")))]
    if not matching:
        report["errors"].append({"note":"传感与检测 missing from active course listing"})
    for course in matching:
        cid=course["id"]
        report["course"]={"id":cid,"name":course.get("name"),"course_code":course.get("course_code")}
        listing=safe_json(f"https://courses.zju.edu.cn/api/courses/{cid}/activities")
        report["activity_payload_keys"]=list(listing.keys()) if isinstance(listing,dict) else []
        acts=listing.get("activities",[]) if isinstance(listing,dict) else []
        report["activity_count"]=len(acts)
        for a in acts:
            row=meta(a)
            files=z.collect_attachment_refs(a)
            if files: row["files"]=[{"id":f.get("id") or f.get("upload_id"),"name":f.get("detected_name"),"size":f.get("size")} for f in files]
            report["activities"].append(row)
            for f in files:
                n=f.get("detected_name") or ""
                if n.lower().endswith((".ppt",".pptx",".pdf")):
                    report["file_candidates"].append({"activity":row,"file":{"id":f.get("id") or f.get("upload_id"),"name":n}})
        # Fetch details for likely latest study materials; do not fetch homework unrelated to this course.
        ranked=sorted(acts,key=lambda a:str(a.get("start_time") or a.get("updated_at") or a.get("created_at") or ""),reverse=True)
        candidates=[a for a in ranked if "作业" in str(a.get("title") or a.get("name") or "")
                    or str(a.get("type","")).lower() not in ("homework","exam")]
        report["detail_survey"]=[]
        for a in candidates[:24]:
            aid=a.get("id")
            if not aid: continue
            detail=safe_json(f"https://courses.zju.edu.cn/api/activities/{aid}?sub_course_id=0")
            refs=z.collect_attachment_refs(detail)
            row={"activity":meta(a),"payload_keys":list(detail.keys()) if isinstance(detail,dict) else [],
                 "files":[{"id":f.get("id") or f.get("upload_id"),"name":f.get("detected_name"),"size":f.get("size")} for f in refs]}
            report["detail_survey"].append(row)
            for f in refs:
                n=f.get("detected_name") or ""
                if n.lower().endswith((".ppt",".pptx",".pdf")):
                    report["file_candidates"].append({"activity":meta(a),"file":{"id":f.get("id") or f.get("upload_id"),"name":n}})
except Exception as e:
    report["errors"].append({"fatal":type(e).__name__,"description":str(e)[:160]})
out=ROOT/"data"/"sensor_lms_inventory.json"
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print("Sensor inventory done:",report.get("course"),"activities",report.get("activity_count"),"candidates",len(report["file_candidates"]),"errors",len(report["errors"]))
