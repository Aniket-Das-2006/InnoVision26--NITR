import requests
import re
import json

base_url = "https://www.innonitrkl.com"

# Read all chunks, html, etc.
files_to_check = [
    "/",
    "/events",
    "/events/flagship-events",
    "/events/standout-events",
    "/events/main-events",
    "/events/dts-and-fun-events",
    "/merch",
    "/privacy",
    "/terms",
    "/_next/static/chunks/3794-4302ec24624ce230.js",
    "/_next/static/chunks/3953-53c529af9c813e1c.js",
    "/_next/static/chunks/44530001-06361d81d0d308be.js",
    "/_next/static/chunks/4bd1b696-0562a75e9b1eb3c3.js",
    "/_next/static/chunks/5669-77d9ca8d2acf44a3.js",
    "/_next/static/chunks/5772-5a4189e7a8225bba.js",
    "/_next/static/chunks/5872-51d1b77308e83427.js",
    "/_next/static/chunks/5911-eb39648c6aa7dcdc.js",
    "/_next/static/chunks/8500-e4dd1cb1bb626827.js",
    "/_next/static/chunks/9931-9fd2b8af4466bcd9.js",
    "/_next/static/chunks/app/error-2728c60759f22e39.js",
    "/_next/static/chunks/app/events/%5Bworld%5D/page-ea9cc018c58b6114.js",
    "/_next/static/chunks/app/events/page-ea9cc018c58b6114.js",
    "/_next/static/chunks/app/global-error-faa8b07628323b46.js",
    "/_next/static/chunks/app/layout-3d0cf70584b929a9.js",
    "/_next/static/chunks/app/merch/page-326bf7941742460a.js",
    "/_next/static/chunks/app/not-found-40fc21b1a5de0d32.js",
    "/_next/static/chunks/app/page-9024683cb3851e4c.js",
    "/_next/static/chunks/app/privacy/page-a800436781c1195a.js",
    "/_next/static/chunks/app/terms/page-a800436781c1195a.js",
    "/_next/static/chunks/c15bf2b0-98325d36a1a29411.js",
    "/_next/static/chunks/main-app-262697177778d708.js",
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

all_imagekit_urls = set()
all_assets_urls = set()

for path in files_to_check:
    url = base_url + path
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            ik = re.findall(r'https://ik\.imagekit\.io/[a-zA-Z0-9_\-\./]+(?:\?[^\s"\'<>]*)?', r.text)
            for item in ik:
                # clean query params if needed or keep base URL
                all_imagekit_urls.add(item)
            assets = re.findall(r'["\'](/assets/[^"\'\s>)]+)["\']', r.text)
            for a in assets:
                all_assets_urls.add(a)
    except Exception as e:
        print(f"Error {path}: {e}")

# Also check api_events.json
with open(r'D:\NITR\api_events.json', 'r', encoding='utf-8') as f:
    events_data = json.load(f)
for ev in events_data.get('events', []):
    if ev.get('poster_url'):
        all_imagekit_urls.add(ev['poster_url'])

print(f"Total Unique ImageKit URLs: {len(all_imagekit_urls)}")
print(f"Total Unique /assets/ URLs: {len(all_assets_urls)}")
print("\nAssets:")
for a in sorted(all_assets_urls):
    print(" ", a)

with open(r'D:\NITR\all_imagekit_urls.txt', 'w', encoding='utf-8') as f:
    for u in sorted(all_imagekit_urls):
        f.write(u + '\n')
