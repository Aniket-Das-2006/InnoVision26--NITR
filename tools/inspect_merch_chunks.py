import requests
import re

r = requests.get("https://www.innonitrkl.com/merch")
scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', r.text)
print("Merch scripts:")
for s in scripts:
    print(" ", s)

# Let's inspect the specific merch page chunk
for s in scripts:
    if 'merch' in s or 'page-' in s:
        url = "https://www.innonitrkl.com" + s if s.startswith('/') else s
        chunk = requests.get(url).text
        merch_imgs = re.findall(r'https?://ik\.imagekit\.io[^\s"\'<>)]+', chunk)
        print(f"ImageKit in {s}:", set(merch_imgs))
