import os
import sys
import re
import json
import time
import requests
from urllib.parse import urljoin, urlparse, unquote

BASE_URL = "https://www.innonitrkl.com"
DEST_DIR = r"D:\NITR"

def ensure_dir(filepath):
    d = os.path.dirname(filepath)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def download_file(url, local_path, headers=None):
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        return True
    ensure_dir(local_path)
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(r.content)
            print(f"Downloaded ({len(r.content)} bytes): {local_path}")
            return True
        else:
            print(f"Failed {url} - Status {r.status_code}")
            return False
    except Exception as e:
        print(f"Error {url}: {e}")
        return False

# 1. Download HTML pages and their RSC payloads
PAGES = {
    "/": "index.html",
    "/events": "events.html",
    "/events/flagship-events": os.path.join("events", "flagship-events.html"),
    "/events/standout-events": os.path.join("events", "standout-events.html"),
    "/events/main-events": os.path.join("events", "main-events.html"),
    "/events/dts-and-fun-events": os.path.join("events", "dts-and-fun-events.html"),
    "/merch": "merch.html",
    "/privacy": "privacy.html",
    "/terms": "terms.html",
    "/robots.txt": "robots.txt",
    "/sitemap.xml": "sitemap.xml",
    "/favicon.ico": "favicon.ico",
    "/icon.png": "icon.png",
    "/apple-icon.png": "apple-icon.png",
}

print("=== 1. DOWNLOADING PAGES AND RSC PAYLOADS ===")
for path, rel_file in PAGES.items():
    url = urljoin(BASE_URL, path)
    local_path = os.path.join(DEST_DIR, "public", rel_file)
    download_file(url, local_path)
    
    # Also create index.html in subdirectories for static file servers
    if rel_file.endswith('.html') and rel_file != 'index.html':
        sub_dir = rel_file[:-5]
        sub_index = os.path.join(DEST_DIR, "public", sub_dir, "index.html")
        ensure_dir(sub_index)
        if not os.path.exists(sub_index) and os.path.exists(local_path):
            with open(local_path, 'rb') as src, open(sub_index, 'wb') as dst:
                dst.write(src.read())

    # Download RSC payload
    if rel_file.endswith('.html') or path == '/':
        rsc_file = rel_file[:-5] + ".rsc" if rel_file.endswith('.html') else "index.rsc"
        rsc_local = os.path.join(DEST_DIR, "public", rsc_file)
        download_file(url, rsc_local, headers={"RSC": "1"})

print("\n=== 2. DOWNLOADING API DATA ===")
download_file(urljoin(BASE_URL, "/api/events"), os.path.join(DEST_DIR, "public", "api", "events.json"))
download_file(urljoin(BASE_URL, "/api/gallery"), os.path.join(DEST_DIR, "public", "api", "gallery.json"))
