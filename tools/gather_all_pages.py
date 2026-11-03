import requests
import re

pages = [
    "/",
    "/events",
    "/events/flagship-events",
    "/events/standout-events",
    "/events/main-events",
    "/events/dts-and-fun-events",
    "/merch",
    "/privacy",
    "/terms"
]

all_scripts = set()
all_css = set()
all_media = set()

base_url = "https://www.innonitrkl.com"

for p in pages:
    r = requests.get(base_url + p)
    scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', r.text)
    css = re.findall(r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)["\']', r.text)
    media = re.findall(r'href=["\']([^"\']+\.woff2[^"\']*)["\']', r.text)
    for s in scripts:
        all_scripts.add(s)
    for c in css:
        all_css.add(c)
    for m in media:
        all_media.add(m)

print(f"Total Unique Scripts across all pages: {len(all_scripts)}")
for s in sorted(all_scripts):
    print(" ", s)

print(f"\nTotal Unique CSS across all pages: {len(all_css)}")
for c in sorted(all_css):
    print(" ", c)

print(f"\nTotal Fonts: {len(all_media)}")
for m in sorted(all_media):
    print(" ", m)
