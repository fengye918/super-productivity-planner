#!/usr/bin/env python3
"""Fetch 学在浙大 todos with a browser-like direct ZJUAM login.

This avoids the current login-zju initial-fetch issue on GitHub-hosted runners
by sending a normal browser User-Agent from the very first CAS request.
"""

from __future__ import annotations

import html
import json
import os
import re
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
MATERIALS_DIR = ROOT / "course_materials"
TODOS_FILE = DATA_DIR / "zju_todos.json"
CHANGES_FILE = DATA_DIR / "zju_changes.json"

USERNAME = os.environ.get("ZJU_USERNAME", "")
PASSWORD = os.environ.get("ZJU_PASSWORD", "")
if not USERNAME or not PASSWORD:
    raise SystemExit("Missing ZJU_USERNAME/ZJU_PASSWORD Actions secrets")

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/153.0.0.0 Safari/537.36"
)


def hidden_field(text: str, name: str) -> str:
    patterns = [
        rf'<input[^>]+name=["\']{re.escape(name)}["\'][^>]+value=["\']([^"\']*)["\']',
        rf'<input[^>]+value=["\']([^"\']*)["\'][^>]+name=["\']{re.escape(name)}["\']',
    ]
    for pattern in patterns:
        m = re.search(pattern, text, flags=re.I)
        if m:
            return html.unescape(m.group(1))
    return ""


def raw_rsa_password(modulus_hex: str, exponent_hex: str, password: str) -> str:
    modulus = int(modulus_hex, 16)
    exponent = int(exponent_hex, 16)
    value = int(password.encode("utf-8").hex(), 16)
    width = max(128, (modulus.bit_length() + 3) // 4)
    return format(pow(value, exponent, modulus), "x").zfill(width)


def login_zjuam(s: requests.Session) -> None:
    login_url = "https://zjuam.zju.edu.cn/cas/login"
    r = s.get(login_url, timeout=20)
    print("ZJUAM initial GET:", r.status_code)
    r.raise_for_status()

    execution = hidden_field(r.text, "execution")
    if not execution:
        raise RuntimeError("ZJUAM login page did not contain execution token")

    r = s.get("https://zjuam.zju.edu.cn/cas/v2/getPubKey", timeout=20)
    print("ZJUAM pubkey GET:", r.status_code)
    r.raise_for_status()
    pub = r.json()

    encrypted = raw_rsa_password(pub["modulus"], pub["exponent"], PASSWORD)
    r = s.post(
        login_url,
        data={
            "username": USERNAME,
            "password": encrypted,
            "execution": execution,
            "_eventId": "submit",
            "authcode": "",
        },
        allow_redirects=False,
        timeout=20,
    )
    print("ZJUAM login POST:", r.status_code)

    if r.status_code not in (301, 302, 303, 307, 308):
        msg = None
        m = re.search(r'<span[^>]+id=["\']msg["\'][^>]*>([^<]+)', r.text, flags=re.I)
        if m:
            msg = html.unescape(m.group(1)).strip()
        raise RuntimeError(f"ZJUAM login failed: HTTP {r.status_code}" + (f" ({msg})" if msg else ""))

    cookie_names = sorted({c.name for c in s.cookies})
    print("ZJUAM cookie names:", ",".join(cookie_names))
    if "iPlanetDirectoryPro" not in cookie_names:
        print("Warning: iPlanetDirectoryPro not visible yet; continuing with service SSO.")


def login_courses(s: requests.Session) -> None:
    start = "https://courses.zju.edu.cn/user/index"
    r = s.get(start, allow_redirects=True, timeout=40)
    print("Courses SSO final:", r.status_code, r.url)
    r.raise_for_status()

    cookie_names = sorted({c.name for c in s.cookies})
    print("Courses cookie names:", ",".join(cookie_names))


def clean_text(value) -> str:
    if not isinstance(value, str):
        return ""
    value = re.sub(r"<style[\s\S]*?</style>", " ", value, flags=re.I)
    value = re.sub(r"<script[\s\S]*?</script>", " ", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


TEXT_KEYS = {
    "description", "content", "instruction", "instructions", "body",
    "intro", "introduction", "requirement", "requirements", "remark", "remarks"
}


def collect_text(node, out=None, depth=0):
    if out is None:
        out = []
    if depth > 8 or node is None:
        return out
    if isinstance(node, list):
        for item in node:
            collect_text(item, out, depth + 1)
    elif isinstance(node, dict):
        for key, value in node.items():
            if key.lower() in TEXT_KEYS and isinstance(value, str):
                t = clean_text(value)
                if t and t not in out:
                    out.append(t)
            if isinstance(value, (dict, list)):
                collect_text(value, out, depth + 1)
    return out


def collect_attachments(node, out=None, depth=0):
    if out is None:
        out = []
    if depth > 10 or node is None:
        return out
    if isinstance(node, list):
        for item in node:
            collect_attachments(item, out, depth + 1)
    elif isinstance(node, dict):
        for key, value in node.items():
            if (
                isinstance(value, str)
                and key.lower() in {"name", "filename", "file_name", "title"}
                and re.search(r"\.(pptx?|pdf|docx?|xlsx?|zip)$", value.strip(), flags=re.I)
            ):
                name = value.strip()
                if name not in out:
                    out.append(name)
            if isinstance(value, (dict, list)):
                collect_attachments(value, out, depth + 1)
    return out


def collect_attachment_refs(node, out=None, depth=0):
    """Collect only file-like attachment metadata, never unrelated activity data."""
    if out is None:
        out = []
    if depth > 10 or node is None:
        return out
    if isinstance(node, list):
        for item in node:
            collect_attachment_refs(item, out, depth + 1)
    elif isinstance(node, dict):
        file_name = None
        for key in ("name", "filename", "file_name", "title"):
            value = node.get(key)
            if isinstance(value, str) and re.search(r"\.(pptx?|pdf|docx?|xlsx?|zip)$", value.strip(), flags=re.I):
                file_name = value.strip()
                break
        if file_name:
            keep = {}
            for key in (
                "id", "upload_id", "name", "filename", "file_name", "title",
                "url", "download_url", "size", "mime_type", "content_type", "type"
            ):
                value = node.get(key)
                if isinstance(value, (str, int, float, bool)) or value is None:
                    keep[key] = value
            keep["detected_name"] = file_name
            if keep not in out:
                out.append(keep)
        for value in node.values():
            if isinstance(value, (dict, list)):
                collect_attachment_refs(value, out, depth + 1)
    return out


def collect_file_contexts(node, path="$", out=None, depth=0):
    """Keep only the local scalar context around file-looking strings."""
    if out is None:
        out = []
    if depth > 12 or node is None:
        return out
    blocked = ("token", "cookie", "password", "secret", "session", "phone", "email", "user")
    if isinstance(node, list):
        for i, item in enumerate(node):
            collect_file_contexts(item, f"{path}[{i}]", out, depth + 1)
    elif isinstance(node, dict):
        scalars = {}
        for k, v in node.items():
            kl = str(k).lower()
            if any(word in kl for word in blocked):
                continue
            if isinstance(v, (str, int, float, bool)) or v is None:
                if isinstance(v, str) and len(v) > 600:
                    scalars[k] = v[:600]
                else:
                    scalars[k] = v
        for k, v in node.items():
            if isinstance(v, str) and re.search(r"\.(pptx?|pdf|docx?|xlsx?|zip)$", v.strip(), flags=re.I):
                item = {"path": f"{path}.{k}", "filename": v.strip(), "container": scalars}
                if item not in out:
                    out.append(item)
            if isinstance(v, (dict, list)):
                collect_file_contexts(v, f"{path}.{k}", out, depth + 1)
    return out


def api_json(s: requests.Session, url: str):
    r = s.get(url, timeout=30, headers={"Accept": "application/json, text/plain, */*"})
    print("API", url.split("courses.zju.edu.cn")[-1].split("?")[0], r.status_code)
    r.raise_for_status()
    ctype = r.headers.get("content-type", "")
    if "json" not in ctype.lower() and r.text.lstrip().startswith("<"):
        raise RuntimeError(f"Expected JSON but got HTML from {url}")
    return r.json()


def safe_path_part(value: str) -> str:
    value = re.sub(r'[\\/:*?"<>|]+', "_", str(value)).strip().strip(".")
    return value[:120] or "unnamed"


def download_assignment_attachments(
    s: requests.Session,
    course_name: str,
    todo_id,
    refs: list[dict],
) -> list[dict]:
    downloaded = []
    if todo_id is None:
        return downloaded

    out_dir = MATERIALS_DIR / safe_path_part(course_name or "unknown_course") / "homework" / str(todo_id)
    out_dir.mkdir(parents=True, exist_ok=True)

    for ref in refs:
        upload_id = ref.get("id") or ref.get("upload_id")
        name = ref.get("detected_name") or ref.get("name") or ref.get("filename")
        if not upload_id or not name:
            continue
        target = out_dir / safe_path_part(name)
        try:
            r = s.get(
                f"https://courses.zju.edu.cn/api/uploads/{upload_id}/blob",
                allow_redirects=True,
                timeout=60,
            )
            r.raise_for_status()
            target.write_bytes(r.content)
            downloaded.append({
                "upload_id": upload_id,
                "name": name,
                "repo_path": target.relative_to(ROOT).as_posix(),
                "bytes": len(r.content),
            })
            print("Downloaded attachment:", target.relative_to(ROOT).as_posix(), len(r.content))
        except Exception as exc:
            downloaded.append({
                "upload_id": upload_id,
                "name": name,
                "error": f"{type(exc).__name__}: {exc}"[:500],
            })
    return downloaded


def normalize_todo(s: requests.Session, todo: dict) -> dict:
    detail = None
    detail_error = None
    todo_id = todo.get("id")
    if todo_id is not None:
        try:
            is_exam = "exam" in str(todo.get("type", "")).lower()
            url = (
                f"https://courses.zju.edu.cn/api/exams/{todo_id}"
                if is_exam
                else f"https://courses.zju.edu.cn/api/activities/{todo_id}?sub_course_id=0"
            )
            detail = api_json(s, url)
        except Exception as exc:
            detail_error = f"{type(exc).__name__}: {exc}"[:500]

    course_id = todo.get("course_id")
    attachment_refs = collect_attachment_refs(detail)[:50]
    downloaded_attachments = download_assignment_attachments(
        s,
        todo.get("course_name") or "unknown_course",
        todo_id,
        attachment_refs,
    )
    return {
        "source_id": todo_id,
        "course_id": course_id,
        "course_name": todo.get("course_name"),
        "course_code": todo.get("course_code"),
        "title": todo.get("title"),
        "type": todo.get("type"),
        "end_time": todo.get("end_time"),
        "is_locked": todo.get("is_locked"),
        "detail_text": " ".join(collect_text(detail))[:6000] or None,
        "attachment_names": collect_attachments(detail)[:50],
        "attachment_refs": attachment_refs,
        "attachment_contexts": collect_file_contexts(detail)[:50],
        "downloaded_attachments": downloaded_attachments,
        "detail_fetch_error": detail_error,
        "source_url": (
            f"https://courses.zju.edu.cn/course/{course_id}/learning-activity#/{todo_id}"
            if course_id is not None and todo_id is not None else None
        ),
    }


def stable_key(todo: dict) -> str:
    return str(todo.get("source_id") or todo.get("title") or "")


def read_previous() -> list[dict]:
    try:
        obj = json.loads(TODOS_FILE.read_text(encoding="utf-8"))
        return obj.get("todos", []) if isinstance(obj.get("todos"), list) else []
    except Exception:
        return []


def save(todos: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    previous = read_previous()
    old = {stable_key(x): x for x in previous}
    new = {stable_key(x): x for x in todos}

    added = [x for k, x in new.items() if k not in old]
    updated = [
        {"before": old[k], "after": x}
        for k, x in new.items()
        if k in old and old[k] != x
    ]
    removed = [x for k, x in old.items() if k not in new]

    TODOS_FILE.write_text(
        json.dumps({"todos": todos}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    CHANGES_FILE.write_text(
        json.dumps(
            {"added": added, "updated": updated, "removed": removed},
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    print(f"Synced {len(todos)} todos; added={len(added)}, updated={len(updated)}, removed={len(removed)}")


def main() -> None:
    s = requests.Session()
    s.headers.update({
        "User-Agent": UA,
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.7",
    })

    login_zjuam(s)
    login_courses(s)

    payload = api_json(s, "https://courses.zju.edu.cn/api/todos?no-intercept=true")
    raw = payload.get("todo_list", []) if isinstance(payload, dict) else []
    todos = [normalize_todo(s, x) for x in raw if isinstance(x, dict)]
    todos.sort(key=lambda x: (
        x.get("end_time") or "9999-12-31T23:59:59Z",
        x.get("course_name") or "",
    ))
    save(todos)


if __name__ == "__main__":
    main()