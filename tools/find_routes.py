import re
import requests
import json

base_url = "https://www.innonitrkl.com"

# 1. Look for buildId or chunk manifest in index.html
with open(r'D:\NITR\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Find all URLs, endpoints, routes
links = re.findall(r'href=["\']([^"\']+)["\']', html)
print("Internal / route links in HTML:")
for l in sorted(set(links)):
    if l.startswith('/') or 'innonitrkl' in l:
        print("  ", l)

# Check scripts
scripts = re.findall(r'src=["\']([^"\']+)["\']', html)
print("\nAll script URLs:")
for s in scripts:
    print("  ", s)

# Let's inspect the webpack and main-app chunks to find all page routes and chunk files!
