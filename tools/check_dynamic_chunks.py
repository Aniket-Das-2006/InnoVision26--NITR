import requests

r_sched = requests.get("https://www.innonitrkl.com/_next/static/chunks/2517.d8efb64168cee224.js")
print("Schedule chunk status:", r_sched.status_code, "Length:", len(r_sched.text))

r_gal = requests.get("https://www.innonitrkl.com/_next/static/chunks/9106.35f0e0ff0ed5a47a.js")
print("Gallery chunk status:", r_gal.status_code, "Length:", len(r_gal.text))

# Search for any API endpoints or image URLs in these chunks
import re
print("Gallery images:", re.findall(r'https?://[^\s"\'<>)]+\.webp', r_gal.text))
print("Schedule images/endpoints:", re.findall(r'https?://[^\s"\'<>)]+', r_sched.text))
