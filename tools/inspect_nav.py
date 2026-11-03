import re

with open(r'D:\NITR\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

hrefs = re.findall(r'href=["\']([^"\']+)["\']', html)
print("ALL HREFS:")
for h in sorted(set(hrefs)):
    print("  ", h)

ids = re.findall(r'id=["\']([^"\']+)["\']', html)
print("\nALL IDS:")
for i in sorted(set(ids)):
    print("  ", i)

nav_matches = re.findall(r'<nav[^>]*>.*?</nav>', html, re.DOTALL)
print(f"\nNav matches: {len(nav_matches)}")
for n in nav_matches:
    print(n)
