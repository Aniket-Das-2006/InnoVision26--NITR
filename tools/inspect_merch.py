import requests
import re

r = requests.get("https://www.innonitrkl.com/merch")
print("Merch status:", r.status_code)
# find all images and links in merch
imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', r.text)
print("Merch images:", imgs)
links = re.findall(r'href=["\']([^"\']+)["\']', r.text)
print("Merch links:", [l for l in links if not l.startswith('/_next')])
