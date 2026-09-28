"""Wrap src/body.html (the same markup published as the Claude artifact) into the standalone web page.

Usage: python build.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://ssxx345-bit.github.io/xinzhai-tiaoxi/"
PAGE = "心齋調息.html"
PAGE_URL = SITE + "%E5%BF%83%E9%BD%8B%E8%AA%BF%E6%81%AF.html"
TITLE = "心齋調息｜呼吸練習、自然白噪音、專注計時"
DESC = ("免費、免安裝的靜心小工具：4-7-8 與方塊呼吸引導，雨聲、壁爐、溪流等瀏覽器即時合成的白噪音，"
        "番茄鐘專注計時，寫下煩惱再放下，以及焦慮時的五感著陸練習。不收集任何資料，可離線使用。")

ld = {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "心齋調息",
    "url": PAGE_URL,
    "description": DESC,
    "inLanguage": "zh-Hant",
    "applicationCategory": "HealthApplication",
    "operatingSystem": "Any",
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "TWD"},
}

HEAD = f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{PAGE_URL}">
<meta property="og:type" content="website">
<meta property="og:locale" content="zh_TW">
<meta property="og:site_name" content="心齋調息">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{PAGE_URL}">
<meta property="og:image" content="{SITE}icons/icon-512.png">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#F4EEE1">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/favicon.svg" type="image/svg+xml">
<link rel="icon" href="icons/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="心齋調息">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head>
<body>
"""

body = (ROOT / "src" / "body.html").read_text(encoding="utf-8")
body = body.replace("<title>心齋調息</title>\n", "", 1)   # the head carries the search-friendly title
(ROOT / PAGE).write_text(HEAD + body + "</body>\n</html>\n", encoding="utf-8")
print("built", PAGE)
