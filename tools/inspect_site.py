import re
import urllib.parse

with open(r'D:\NITR\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', text)
links = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', text)

print(f"SCRIPTS ({len(scripts)}):")
for s in scripts:
    print("  ", s)

print(f"\nLINKS ({len(links)}):")
for l in links:
    print("  ", l)

# Check title and meta
title = re.findall(r'<title>(.*?)</title>', text, re.IGNORECASE)
print(f"\nTitle: {title}")

# Check any other embedded data or routes
next_data = re.findall(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', text, re.DOTALL)
print(f"Has __NEXT_DATA__: {len(next_data) > 0}")

# Check for Next.js app router or pages router chunks
chunks = re.findall(r'/_next/static/[a-zA-Z0-9_\-\./]+', text)
print(f"Unique _next paths: {len(set(chunks))}")
for c in sorted(set(chunks))[:20]:
    print("  ", c)
