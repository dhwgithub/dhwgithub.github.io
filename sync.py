#!/usr/bin/env python3
"""从 GitHub API 拉取仓库列表，重写 index.html 中的内联快照数据。

用法：
    python sync.py <github-用户名> [index.html 路径]

在 GitHub Actions 中由 .github/workflows/sync.yml 定时调用；
提交前请确保 index.html 里存在 `const SNAPSHOT = ...;` 这一行。
"""
import json
import re
import sys
import urllib.request

API = "https://api.github.com/users/{user}/repos?per_page=100&sort=updated"


def fetch(user):
    req = urllib.request.Request(
        API.format(user=user),
        headers={"User-Agent": "repo-page-sync", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def normalize(raw):
    repos = []
    for r in raw:
        repos.append({
            "name": r["name"],
            "desc": r.get("description") or "",
            "lang": r.get("language"),
            "stars": r.get("stargazers_count", 0),
            "forks": r.get("forks_count", 0),
            "fork": r.get("fork", False),
            "archived": r.get("archived", False),
            "topics": r.get("topics", []),
            "updated": (r.get("updated_at") or "")[:10],
            "created": (r.get("created_at") or "")[:10],
            "homepage": (r.get("homepage") or "").strip(),
            "url": r["html_url"],
            "size": r.get("size", 0),
            "branch": r.get("default_branch", "main"),
            "license": r["license"]["spdx_id"] if r.get("license") else None,
            "open_issues": r.get("open_issues_count", 0),
        })
    owner = raw[0]["owner"]
    return {
        "profile": {"login": owner["login"], "avatar": owner["avatar_url"], "url": owner["html_url"]},
        "repos": repos,
        "generated": __import__("datetime").date.today().isoformat(),
    }


def main():
    user = sys.argv[1] if len(sys.argv) > 1 else "dhwgithub"
    target = sys.argv[2] if len(sys.argv) > 2 else "index.html"

    raw = fetch(user)
    data = normalize(raw)

    # 单行紧凑 JSON；转义 < 以避免意外闭合 </script>
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")

    html = open(target, encoding="utf-8").read()
    pattern = re.compile(r"const SNAPSHOT = .*?;\n\n/\* ===== 语言配色", re.S)
    if not pattern.search(html):
        raise SystemExit("ERROR: 未在 index.html 中找到 `const SNAPSHOT = ...;` 锚点，已中止以免写坏文件")

    html = pattern.sub(lambda _: f"const SNAPSHOT = {payload};\n\n/* ===== 语言配色", html, count=1)
    open(target, "w", encoding="utf-8").write(html)
    print(f"OK: 已更新 {target}，共 {len(data['repos'])} 个仓库（{data['generated']}）")


if __name__ == "__main__":
    main()
