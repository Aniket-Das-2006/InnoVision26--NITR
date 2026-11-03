with open(r'D:\NITR\inspect_scripts.py', 'r') as f:
    pass

import os
import requests
import re

# Search in the downloaded scripts or search all chunks for .mp3 / Audio / sound
chunks_to_search = [
    "/_next/static/chunks/app/page-9024683cb3851e4c.js",
    "/_next/static/chunks/4bd1b696-0562a75e9b1eb3c3.js",
    "/_next/static/chunks/9931-9fd2b8af4466bcd9.js",
    "/_next/static/chunks/app/layout-3d0cf70584b929a9.js"
]

base_url = "https://www.innonitrkl.com"

for c in chunks_to_search:
    r = requests.get(base_url + c)
    if "beep" in r.text:
        print(f"Found 'beep' in {c}!")
        idx = r.text.find("beep")
        start = max(0, idx - 200)
        end = min(len(r.text), idx + 200)
        print("CONTEXT:", r.text[start:end])
    # Search for all strings ending in .mp3, .wav, .ogg, .mp4, etc.
    sounds = re.findall(r'["\']([^"\']+\.(?:mp3|wav|ogg|mp4|webm))["\']', r.text)
    if sounds:
        print(f"Sounds in {c}:", sounds)
