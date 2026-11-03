import os
import requests
import re

# Let's inspect the main script chunks from index.html
with open(r'D:\NITR\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html)
print(f"Found {len(scripts)} scripts in index.html")

# Let's download them temporarily and inspect them
keywords = ['framer-motion', 'gsap', 'lenis', 'locomotive', 'three', 'canvas', 'spline', 'supabase', 'lucide', 'tailwind', 'audio', 'sound', 'video']

for s in scripts:
    url = "https://www.innonitrkl.com" + s if s.startswith('/') else s
    try:
        r = requests.get(url, timeout=10)
        found = [k for k in keywords if k in r.text.lower()]
        print(f"{s.split('/')[-1]}: {len(r.content)} bytes, matched: {found}")
    except Exception as e:
        print(f"Error {s}: {e}")
