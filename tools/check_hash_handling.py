with open(r'D:\NITR\inspect_scripts.py') as f: pass
import requests
import re

code = requests.get("https://www.innonitrkl.com/_next/static/chunks/app/page-9024683cb3851e4c.js").text

for keyword in ['hashchange', 'schedule', 'gallery', 'ambassador', 'worlds']:
    matches = [m.start() for m in re.finditer(keyword, code, re.IGNORECASE)]
    print(f"Keyword '{keyword}' count: {len(matches)}")
    for m in matches[:3]:
        print("  Snippet:", code[max(0, m-80):min(len(code), m+120)])
