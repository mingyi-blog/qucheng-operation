# -*- coding: utf-8 -*-
"""渠成 · 被动收益运营笔记 —— 静态博客生成器（与手到心安理疗线完全独立，无理疗品牌/CTA）。
数据驱动：文章存 posts_data.json，本脚本生成 index.html / posts/*.html / sitemap.xml / robots.txt。
新增文章：往 posts_data.json 追加一篇，再运行本脚本即可。"""
import os
import json

BASE = r"E:\workbuddy\2026-08-28-15-09-37\qucheng-blog"

SITE = {
    "title": "渠成 · 被动收益运营笔记",
    "sub": "调查 → 模仿 → 超越 → 总结 → 成长（认知差即商机）",
    "author": "渠成（旺存经营体）",
    "url": "https://mingyi-blog.github.io/qucheng-operation",
    "footer": "渠成 · 被动收益运营笔记　|　资产生产以实事求是、真正帮人为第一性",
    # 渠成自有媒体矩阵（暂不混入任何理疗账号）；未来每线独立接微博等，互不相通
    "social": [],
    "wechat": "",
}

_DATA = os.path.join(BASE, "posts_data.json")
if os.path.exists(_DATA):
    with open(_DATA, encoding="utf-8") as _f:
        posts = json.load(_f)
else:
    posts = []


POST_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · 渠成</title>
<meta name="description" content="{description}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="渠成">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">
{jsonld}
</script>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <h1 class="site-title">渠成</h1>
    <p class="site-sub">调查 · 模仿 · 超越 · 总结 · 成长</p>
    <div class="site-nav"><a href="../">首页</a><a href="../manifesto.html">创作理念</a></div>
  </div>
</header>
<main class="wrap article">
  <div class="article-header">
    <h1>{title}</h1>
    <div class="article-meta">{date} · {reading}阅读 · {author}</div>
  </div>
  <article class="article-body">
    {content}
    <div class="tags">{tags_html}</div>
    <div class="share-bar">
      <span class="share-tip">觉得有启发，分享给同路的人：</span>
      <button class="share-btn" data-share="weibo">微博</button>
      <button class="share-btn" data-share="qq">QQ</button>
      <button class="share-btn" data-share="copy">复制链接</button>
    </div>
    {related_html}
    {faq_html}
    {follow_block}
    <a class="back-home" href="../">← 返回首页</a>
  </article>
</main>
<footer class="site-footer">{footer}</footer>
<script src="../assets/share.js"></script>
</body>
</html>
"""

INDEX_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>渠成 · 被动收益运营笔记</title>
<meta name="description" content="渠成被动收益资产的生产与运营复盘：市场监测、资产方向裁决、认知差飞轮。调查→模仿→超越→总结→成长。">
<meta property="og:type" content="website">
<meta property="og:title" content="渠成 · 被动收益运营笔记">
<meta property="og:description" content="渠成被动收益资产的生产与运营复盘：市场监测、资产方向裁决、认知差飞轮。">
<meta property="og:url" content="{site_url}/">
<meta property="og:site_name" content="渠成">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <h1 class="site-title">渠成</h1>
    <p class="site-sub">调查 · 模仿 · 超越 · 总结 · 成长</p>
    <div class="site-nav"><a href="manifesto.html">创作理念</a><a href="./">首页</a></div>
  </div>
</header>
<main class="wrap post-list">
{cards}
</main>
{follow_block}
<footer class="site-footer">{footer}</footer>
</body>
</html>
"""


def tags_html(tags):
    return "".join('<span class="tag">{}</span>'.format(t) for t in tags)


def gen():
    os.makedirs(os.path.join(BASE, "posts"), exist_ok=True)

    # 渠成独立关注区块（无理疗账号，仅作品牌声明）
    follow_block = (
        '<section class="follow-box">'
        '<h3 class="box-title">渠成 · 被动收益运营笔记</h3>'
        '<p class="cta-text">本号独立记录被动收益资产的生产与运营复盘——调查市场、模仿标杆、超越成品、总结方法、沉淀认知差。与理疗业务线互不相交。</p>'
        '</section>'
    )

    slug_title = {p["slug"]: p["title"] for p in posts}

    for p in posts:
        related_html = ""
        if p.get("related"):
            links = "".join(
                '<a class="rel-link" href="../posts/{s}.html">{t}</a>'.format(s=s, t=slug_title.get(s, s))
                for s in p["related"]
            )
            related_html = (
                '<section class="rel-box"><h3 class="box-title">相关阅读</h3>'
                '<div class="rel-list">' + links + '</div></section>'
            )
        faq_html = ""
        if p.get("faq"):
            items = "".join(
                '<div class="faq-item"><p class="faq-q">Q：{q}</p><p class="faq-a">A：{a}</p></div>'.format(q=q, a=a)
                for q, a in p["faq"]
            )
            faq_html = '<section class="faq-box"><h3 class="box-title">大家还问</h3>' + items + '</section>'

        jsonld = json.dumps({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": p["title"],
            "author": {"@type": "Person", "name": SITE["author"]},
            "datePublished": p["iso"],
            "description": p["summary"],
            "mainEntityOfPage": SITE["url"] + "/posts/" + p["slug"] + ".html",
            "publisher": {"@type": "Organization", "name": "渠成"},
        }, ensure_ascii=False)

        html = POST_TEMPLATE.format(
            title=p["title"],
            description=p["summary"],
            url=SITE["url"] + "/posts/" + p["slug"] + ".html",
            jsonld=jsonld,
            date=p["date"],
            reading=p["reading"],
            author=SITE["author"],
            content=p["content"],
            tags_html=tags_html(p["tags"]),
            related_html=related_html,
            faq_html=faq_html,
            follow_block=follow_block,
            footer=SITE["footer"],
        )
        with open(os.path.join(BASE, "posts", p["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(html)

    cards = ""
    for p in posts:
        cards += (
            '<a class="post-card" href="posts/{slug}.html">'
            '<h2>{title}</h2>'
            '<p>{summary}</p>'
            '<div class="post-meta">{date} · {reading}阅读 · {tags}</div>'
            '</a>\n'
        ).format(
            slug=p["slug"],
            title=p["title"],
            summary=p["summary"],
            date=p["date"],
            reading=p["reading"],
            tags="、".join(p["tags"]),
        )
    index_html = INDEX_TEMPLATE.format(
        site_url=SITE["url"],
        cards=cards, follow_block=follow_block, footer=SITE["footer"]
    )
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    urls = [SITE["url"] + "/"]
    for p in posts:
        urls.append(SITE["url"] + "/posts/" + p["slug"] + ".html")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        xml += "  <url><loc>{}</loc></url>\n".format(u)
    xml += "</urlset>\n"
    with open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)

    robots = "User-agent: *\nAllow: /\nSitemap: {}/sitemap.xml\n".format(SITE["url"])
    with open(os.path.join(BASE, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    print("generated:", len(posts), "posts + index.html + sitemap.xml + robots.txt")


if __name__ == "__main__":
    gen()
