import os
import sys
import re
import json
import time
import requests
from urllib.parse import urljoin, urlparse, unquote

BASE_URL = "https://www.innonitrkl.com"
DEST_DIR = r"D:\NITR\public"

def ensure_dir(filepath):
    d = os.path.dirname(filepath)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def download_file(url, local_path):
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        return True
    ensure_dir(local_path)
    try:
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(r.content)
            print(f"[OK] {os.path.basename(local_path)} ({len(r.content)} B)")
            return True
        else:
            print(f"[FAILED {r.status_code}] {url}")
            return False
    except Exception as e:
        print(f"[ERROR] {url}: {e}")
        return False

# 1. Chunks
chunks = [
    "/_next/static/chunks/4bd1b696-0562a75e9b1eb3c3.js",
    "/_next/static/chunks/3794-4302ec24624ce230.js",
    "/_next/static/chunks/main-app-262697177778d708.js",
    "/_next/static/chunks/app/error-2728c60759f22e39.js",
    "/_next/static/chunks/8500-e4dd1cb1bb626827.js",
    "/_next/static/chunks/app/not-found-40fc21b1a5de0d32.js",
    "/_next/static/chunks/app/global-error-faa8b07628323b46.js",
    "/_next/static/chunks/app/layout-3d0cf70584b929a9.js",
    "/_next/static/chunks/44530001-06361d81d0d308be.js",
    "/_next/static/chunks/c15bf2b0-98325d36a1a29411.js",
    "/_next/static/chunks/3953-53c529af9c813e1c.js",
    "/_next/static/chunks/5911-eb39648c6aa7dcdc.js",
    "/_next/static/chunks/9931-9fd2b8af4466bcd9.js",
    "/_next/static/chunks/5872-51d1b77308e83427.js",
    "/_next/static/chunks/5669-77d9ca8d2acf44a3.js",
    "/_next/static/chunks/5772-5a4189e7a8225bba.js",
    "/_next/static/chunks/app/page-9024683cb3851e4c.js",
    "/_next/static/chunks/app/events/page-ea9cc018c58b6114.js",
    "/_next/static/chunks/app/events/%5Bworld%5D/page-ea9cc018c58b6114.js",
    "/_next/static/chunks/app/merch/page-326bf7941742460a.js",
    "/_next/static/chunks/app/privacy/page-a800436781c1195a.js",
    "/_next/static/chunks/app/terms/page-a800436781c1195a.js",
    "/_next/static/chunks/polyfills-42372ed130431b0a.js",
    "/_next/static/chunks/webpack-59ebd1f44e204ed8.js",
    "/_next/static/chunks/bc98253f.28485b6529a1b8e7.js",
    "/_next/static/chunks/704.569413513205e4e7.js",
    "/_next/static/chunks/768.c14af6cc36ecda36.js",
    "/_next/static/chunks/1992.3ab47769f7c826e3.js",
    "/_next/static/chunks/2485.e31fe94b382a2ef0.js",
    "/_next/static/chunks/2517.d8efb64168cee224.js",
    "/_next/static/chunks/2885.f23ffbe69618d232.js",
    "/_next/static/chunks/164f4fb6.27d490fe23ffa262.js",
    "/_next/static/chunks/4233.9ebd217175818b45.js",
    "/_next/static/chunks/ad2866b8.71091ba302e684b4.js",
    "/_next/static/chunks/4360.fb8bc8979846d028.js",
    "/_next/static/chunks/2f0b94e8.c03c597ed708d982.js",
    "/_next/static/chunks/5902.57b50b3397fc4d7b.js",
    "/_next/static/chunks/8385.b6176812204c9f79.js",
    "/_next/static/chunks/9106.35f0e0ff0ed5a47a.js",
]

print("=== DOWNLOADING CHUNKS ===")
for c in chunks:
    # Handle encoded %5Bworld%5D -> [world] on disk or keep decoded
    rel_path = c.lstrip('/')
    # Note: URL requires %5Bworld%5D, disk can be [world] or %5Bworld%5D
    # Let's save as both decoded and encoded to avoid any mismatch!
    url = BASE_URL + c
    local_path = os.path.join(DEST_DIR, unquote(rel_path).replace('/', os.sep))
    download_file(url, local_path)
    if '%5B' in rel_path or '%5b' in rel_path:
        local_raw = os.path.join(DEST_DIR, rel_path.replace('/', os.sep))
        download_file(url, local_raw)

# 2. CSS
css_files = [
    "/_next/static/css/184cfac8c54b4486.css",
    "/_next/static/css/2ca2ddc20d4aa821.css",
    "/_next/static/css/5403fa642f6d39a8.css",
    "/_next/static/css/58674fb7950da55a.css",
    "/_next/static/css/8c1ceca851ae029e.css",
    "/_next/static/css/a95bf5a24b725f1c.css",
]

print("\n=== DOWNLOADING CSS ===")
for css in css_files:
    rel_path = css.lstrip('/')
    url = BASE_URL + css
    local_path = os.path.join(DEST_DIR, rel_path.replace('/', os.sep))
    download_file(url, local_path)

# 3. Fonts
fonts = [
    "/_next/static/media/49eec060ce8bd0da-s.p.woff2",
    "/_next/static/media/8760c4774489e4ba-s.p.woff2",
    "/_next/static/media/fa3e259cafa8f47e-s.p.woff2",
    "/_next/static/media/39f449c8730c2295-s.woff2",
    "/_next/static/media/ccc01da6a2b3d788-s.woff2",
    "/_next/static/media/86f65e8637cc94e3-s.woff2",
    "/_next/static/media/f9e1dbe9676d9bb6-s.woff2",
    "/_next/static/media/20fd6a0e301296d5-s.woff2",
    "/_next/static/media/9fabb9c65b63d798-s.woff2",
    "/_next/static/media/a1f87af3f44fadbb-s.woff2",
]

print("\n=== DOWNLOADING FONTS ===")
for f in fonts:
    rel_path = f.lstrip('/')
    url = BASE_URL + f
    local_path = os.path.join(DEST_DIR, rel_path.replace('/', os.sep))
    download_file(url, local_path)

# 4. Assets in /assets/
assets = [
    "/assets/asteroid.webp",
    "/assets/astronaut-flag-planted.png",
    "/assets/astronaut-lunar.webp",
    "/assets/astronaut-snowboard.webp",
    "/assets/beep.mp3",
    "/assets/indian-astronaut.webp",
    "/assets/INNOVISION%20LOGO.png",
    "/assets/lab.webp",
    "/assets/lander.webp",
    "/assets/mesa.svg",
    "/assets/moon-cratered.webp",
    "/assets/moon-full.webp",
    "/assets/payment-qr.webp",
    "/assets/planet-crescent.webp",
    "/assets/planet-earth.webp",
    "/assets/planet-mars.webp",
    "/assets/planet-mercury.webp",
    "/assets/planet-moon.webp",
    "/assets/planet-ringed.webp",
    "/assets/planet-storm.webp",
    "/assets/planet-tide.webp",
    "/assets/receiver.webp",
    "/assets/rocket.svg",
    "/assets/satellite.webp",
    "/assets/starfield.svg",
]

print("\n=== DOWNLOADING ASSETS ===")
for a in assets:
    rel_path = a.lstrip('/')
    url = BASE_URL + a
    local_path = os.path.join(DEST_DIR, unquote(rel_path).replace('/', os.sep))
    download_file(url, local_path)
    if '%' in rel_path:
        local_raw = os.path.join(DEST_DIR, rel_path.replace('/', os.sep))
        download_file(url, local_raw)

print("\nDone downloading chunks, css, fonts, and assets!")
