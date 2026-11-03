import os
import requests
import re
from urllib.parse import urljoin, urlparse

BASE_URL = "https://www.innonitrkl.com"
PAGES = [
    "/",
    "/events",
    "/events/flagship-events",
    "/events/standout-events",
    "/events/main-events",
    "/events/dts-and-fun-events",
    "/merch",
    "/privacy",
    "/terms",
    "/robots.txt",
    "/sitemap.xml",
    "/api/events",
    "/api/gallery",
]

all_assets = set()

for page in PAGES:
    url = urljoin(BASE_URL, page)
    print(f"Fetching {url}...")
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            print(f"  OK: {len(r.content)} bytes")
            # Extract script src
            for s in re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', r.text):
                all_assets.add(s)
            # Extract link href
            for l in re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', r.text):
                all_assets.add(l)
            # Extract img src
            for i in re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', r.text):
                all_assets.add(i)
            # Extract video/source src
            for v in re.findall(r'<source[^>]+src=["\']([^"\']+)["\']', r.text):
                all_assets.add(v)
            # Extract url(...)
            for u in re.findall(r'url\((["\']?)([^)"\']+)\1\)', r.text):
                all_assets.add(u[1])
            # Next.js chunks or assets pattern
            for chunk in re.findall(r'(/_next/static/[a-zA-Z0-9_\-\./]+(?:\?[^"\'\s>]+)?)', r.text):
                all_assets.add(chunk)
            for asset in re.findall(r'(/assets/[a-zA-Z0-9_\-\./]+)', r.text):
                all_assets.add(asset)
    except Exception as e:
        print(f"  Error fetching {url}: {e}")

print(f"\nTotal discovered assets: {len(all_assets)}")
with open(r'D:\NITR\assets_list.txt', 'w', encoding='utf-8') as f:
    for a in sorted(all_assets):
        f.write(a + '\n')
