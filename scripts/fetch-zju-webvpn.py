#!/usr/bin/env python3
"""Fetch 学在浙大 todos through Zhejiang University WebVPN.

This is a GitHub-Actions-friendly fallback for off-campus runners. It uses
only the repository Actions secrets ZJU_USERNAME and ZJU_PASSWORD and writes
normalized todo metadata to data/zju_todos.json / data/zju_changes.json.
"""

from __future__ import annotations

import html
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import quote, urlparse

import requests
from Crypto.Cipher import AES

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TODOS_FILE = DATA_DIR / "zju_todos.json"
CHANGES_FILE = DATA_DIR / "zju_changes.json"

WEBVPN_BASE = "https://webvpn.zju.edu.cn"
WEBVPN_LOGIN = WEBVPN_BASE + "/login"
WEBVPN_DO_LOGIN = WEBVPN_BASE + "/do-login"

# Protocol constants used by the WebVPN browser front-end.
URL_KEY = b"wrdvpnisthebest!"
PWD_KEY = b"wrdvpnisawesome!"

USERNAME = os.environ.get("ZJU_USERNAME", "")
PASSWORD = os.environ.get("ZJU_PASSWORD", "")

if not USERNAME or not PASSWORD:
    raise SystemExit("Missing ZJU_USERNAME/ZJU_PASSWORD Actions secrets")


def aes_cfb_encrypt(data: bytes, key: bytes) -> bytes:
    return AES.new(key, AES.MODE_CFB, iv=key, segment_size=128).encrypt(data)


def encode_field(value: str, key: bytes) -> str:
    prefix = key.decode("ascii").encode("ascii").hex()
    encrypted = aes_cfb_encrypt(value.encode("utf-8"), key).hex()
    return prefix + encrypted[: 2 * len(value.encode("utf-8"))]


def vpn_url(url: str) -> str:
    p = urlparse(url)
    if p.scheme not in {"http", "https"} or not p.hostname:
        raise ValueError(f"Unsupported URL: {url}")
    special_port = p.port is not None and not (
        (p.scheme == "http" and p.port == 80) or
        (p.scheme == "https" and p.port == 443)
    )
    prop = f"{p.scheme}-{p.port}" if special_port else p.scheme
    encoded_host = encode_field(p.hostname, URL_KEY)
    path = p.path or "/"
    if p.query:
        path += "?" + p.query
    return f"{WEBVPN_BASE}/{prop}/{encoded_host}{path}"


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


def login_webvpn(s: requests.Session) -> None:
    r = s.get(WEBVPN_LOGIN, timeout=20)
    r.raise_for_status()

    csrf = hidden_field(r.text, "_csrf")
    captcha_id = hidden_field(r.text, "captcha_id")
    auth_type = hidden_field(r.text, "auth_type")

    form = {
        "_csrf": csrf,
        "auth_type": auth_type,
        "sms_code": "",
        "captcha": "",
        "needCaptcha": "false",
        "captcha_id": captcha_id,
        "username": USERNAME,
        "password": encode_field(PASSWORD, PWD_KEY),
    }

    r = s.post(
        WEBVPN_DO_LOGIN,
        data=form,
        headers={"Referer": WEBVPN_LOGIN},
        timeout=20,
    )

    ok = False
    try:
        payload = r.json()
        ok = bool(payload.get("success"))
        if not ok and payload:
            safe_keys = {k: payload.get(k) for k in ("success", "message", "msg", "code") if k in payload}
            print("WebVPN login response:", safe_keys)
    except Exception:
        pass

    ticket = any("wengine_vpn_ticket" in c.name for c in s.cookies)
    if not ok and not ticket:
        # Newer deployments may ask for captcha/SMS/OTP. Detect that explicitly
        # instead of ever printing credentials or raw HTML.
        body = r.text.lower()
        hints = []
        for term in ("captcha", "sms", "otp", "动态口令", "验证码", "二次"):
            if term.lower() in body:
                hints.append(term)
        hint = ",".join(sorted(set(hints))) or "unknown authentication challenge"
        raise RuntimeError(f"WebVPN login did not issue a ticket ({hint})")


def raw_rsa_password(modulus_hex: str, exponent_hex: str, password: str) -> str:
    modulus = int(modulus_hex, 16)
    exponent = int(exponent_hex, 16)
    value = int(password.encode("utf-8").hex(), 16)
    width = max(128, (modulus.bit_length() + 3) // 4)
    return format(pow(value, exponent, modulus), "x").zfill(width)


def login_zjuam_via_vpn(s: requests.Session) -> None:
    login_url = vpn_url("https://zjuam.zju.edu.cn/cas/login")
    r = s.get(login_url, timeout=20)
    r.raise_for_status()

    m = re.search(r'name=["\']execution["\']\s+value=["\']([^"\']+)', r.text)
    if not m:
        m = re.search(r'value=["\']([^"\']+)["\']\s+name=["\']execution["\']', r.text)
    if not m:
        raise RuntimeError("Unable to obtain ZJUAM execution token through WebVPN")
    execution = html.unescape(m.group(1))

    r = s.get(vpn_url("https://zjuam.zju.edu.cn/cas/v2/getPubKey"), timeout=20)
    r.raise_for_status()
    pub = r.json()
    encrypted_password = raw_rsa_password(pub["modulus"], pub["exponent"], PASSWORD)

    r = s.post(
        login_url,
        data={
            "username": USERNAME,
            "password": encrypted_password,
            "execution": execution,
            "_eventId": "submit",
            "rememberMe": "true",
        },
        timeout=20,
    )
    r.raise_for_status()


def login_courses_via_vpn(s: requests.Session) -> None:
    service = (
        "https://zjuam.zju.edu.cn/cas/login"
        "?service=https%3A%2F%2Fcourses.zju.edu.cn%2Fuser%2Findex"
    )
    r = s.get(vpn_url(service), timeout=30)
    r.raise_for_status()


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


def fetch_json(s: requests.Session, url: str):
    r = s.get(vpn_url(url), timeout=30)
    r.raise_for_status()
    return r.json()


def normalize_todo(s: requests.Session, todo: dict) -> dict:
    detail = None
    detail_error = None
    todo_id = todo.get("id")
    if todo_id is not None:
        try:
            is_exam = "exam" in str(todo.get("type", "")).lower()
            detail_url = (
                f"https://courses.zju.edu.cn/api/exams/{todo_id}"
                if is_exam
                else f"https://courses.zju.edu.cn/api/activities/{todo_id}?sub_course_id=0"
            )
            detail = fetch_json(s, detail_url)
        except Exception as exc:
            detail_error = f"{type(exc).__name__}: {exc}"[:500]

    course_id = todo.get("course_id")
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


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/153 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.7",
    })

    print("Trying Zhejiang University WebVPN fallback...")
    login_webvpn(s)
    print("WebVPN ticket acquired.")
    login_zjuam_via_vpn(s)
    print("ZJUAM session established through WebVPN.")
    login_courses_via_vpn(s)
    print("Courses service opened through WebVPN.")

    payload = fetch_json(s, "https://courses.zju.edu.cn/api/todos?no-intercept=true")
    raw_todos = payload.get("todo_list", []) if isinstance(payload, dict) else []
    todos = [normalize_todo(s, x) for x in raw_todos if isinstance(x, dict)]
    todos.sort(key=lambda x: (
        x.get("end_time") or "9999-12-31T23:59:59Z",
        x.get("course_name") or "",
    ))

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
    print(f"Synced {len(todos)} todos via WebVPN; added={len(added)}, updated={len(updated)}, removed={len(removed)}")


if __name__ == "__main__":
    main()
