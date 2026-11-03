import requests
import re

css_urls = [
    "/_next/static/css/184cfac8c54b4486.css",
    "/_next/static/css/2ca2ddc20d4aa821.css",
    "/_next/static/css/5403fa642f6d39a8.css",
    "/_next/static/css/58674fb7950da55a.css",
    "/_next/static/css/8c1ceca851ae029e.css",
    "/_next/static/css/a95bf5a24b725f1c.css"
]

base_url = "https://www.innonitrkl.com"

css_assets = set()

for c in css_urls:
    url = base_url + c
    r = requests.get(url)
    if r.status_code == 200:
        matches = re.findall(r'url\((["\']?)([^)"\']+)\1\)', r.text)
        for m in matches:
            css_assets.add(m[1])

print("CSS declared assets:", css_assets)
