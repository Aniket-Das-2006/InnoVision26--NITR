import requests
import re

r = requests.get("https://www.innonitrkl.com/_next/static/chunks/app/page-9024683cb3851e4c.js")
code = r.text

# Find 85749 module
idx = code.find("85749:")
if idx != -1:
    print("Found 85749:", code[idx:idx+300])

# Find all /assets/ references
assets = set(re.findall(r'["\'](/assets/[^"\'\s>)]+)["\']', code))
print("All /assets/ in page.js:", sorted(assets))

# Find all external URLs (imagekit, supabase, etc.)
urls = set(re.findall(r'https?://[^\s"\'<>)]+', code))
print("All external URLs in page.js:")
for u in sorted(urls):
    if 'w3.org' not in u:
        print("  ", u)
