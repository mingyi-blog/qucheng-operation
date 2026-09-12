# -*- coding: utf-8 -*-
"""渠成博客推送脚本（独立仓库 mingyi-blog/qucheng-operation）。
与手到心安的 push_blog.py 完全独立、互不引用。Token 从隔离凭据读取。"""
import base64
import os
import subprocess
import sys
import requests
import datetime

TOKEN_FILE = os.path.expanduser(r"C:\Users\Administrator\.workbuddy\github_token.txt")
REPO = "mingyi-blog/qucheng-operation"
BASE = r"E:\workbuddy\2026-08-28-15-09-37\qucheng-blog"
API = f"https://api.github.com/repos/{REPO}/contents"


def read_env(name):
    """用户级环境变量：进程环境优先 → 注册表 HKCU\\Environment 兜底。
    兜底原因：环境变量写入后仅新进程继承，长期运行的宿主进程读不到，
    直接从注册表补读可消除"必须重启"的时序依赖。"""
    v = os.environ.get(name, "").strip()
    if v:
        return v
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            v, _ = winreg.QueryValueEx(k, name)
            return (v or "").strip()
    except Exception:
        return ""


def load_token():
    """凭据读取（安全优先级）：
    1) 用户级环境变量 GITHUB_TOKEN（首选，不落明文；含注册表兜底）
    2) 明文文件 ~/.workbuddy/github_token.txt（兜底）
    与手到心安 push_blog.py 逻辑一致，互不引用。"""
    tok = read_env("GITHUB_TOKEN")
    if tok:
        return tok
    if not os.path.isfile(TOKEN_FILE):
        sys.exit(f"--- 未找到凭据：环境变量 GITHUB_TOKEN 未设置，且凭据文件不存在：{TOKEN_FILE}")
    with open(TOKEN_FILE, "r", encoding="utf-8") as f:
        tok = f.read().strip()
    if not tok:
        sys.exit("--- 凭据文件为空，请写入有效的 GitHub PAT。")
    return tok


TOKEN = load_token()
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "workbuddy-push-qucheng",
}


def tracked_files():
    out = subprocess.check_output(["git", "-C", BASE, "ls-files"], text=True)
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def upload(path, msg):
    local = os.path.join(BASE, path)
    if not os.path.isfile(local):
        return
    with open(local, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    r = requests.get(f"{API}/{path}", headers=HEADERS, timeout=30)
    sha = r.json().get("sha") if r.status_code == 200 else None
    body = {"message": msg, "content": content}
    if sha:
        body["sha"] = sha
    r2 = requests.put(f"{API}/{path}", headers=HEADERS, json=body, timeout=30)
    code = r2.status_code
    ok = code in (200, 201)
    print(f"{'OK' if ok else 'FAIL'} [{code}] {path}")
    if not ok:
        print("   ", r2.text[:200])
    return ok


def main():
    args = sys.argv[1:]
    force = "--force" in args
    rest = [a for a in args if a != "--force"]
    msg = rest[0] if rest else "chore: 同步渠成博客静态文件"
    if not force:
        print("--- 非强制模式：加 --force 以推送（渠成站初期手动触发）。")
        sys.exit(0)
    files = tracked_files()
    skip = {".git", ".DS_Store"}
    ok_all = True
    for f in files:
        if f.startswith(".git") or os.path.basename(f) in skip:
            continue
        if not upload(f, msg):
            ok_all = False
    print("ALL_OK" if ok_all else "SOME_FAILED")


if __name__ == "__main__":
    main()
