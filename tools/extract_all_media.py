import os
import requests
import re
from urllib.parse import urljoin

base_url = "https://www.innonitrkl.com"

# Let's inspect all chunks in webpack and HTML
chunks_to_download = [
    # Static chunks from index.html
    "/_next/static/chunks/4bd1b696-0562a75e9b1eb3c3.js",
    "/_next/static/chunks/3794-4302ec24624ce230.js",
    "/_next/static/chunks/main-app-262697177778d708.js",
    "/_next/static/chunks/app/error-2728c60759f22e39.js",
    "/_next/static/chunks/8500-e4dd1cb1bb626827.js",
    "/_next/static/chunks/app/not-found-40fc21b1a5de0d32.js",
    "/_next/static/chunks/app/global-error-faa8b07628323b46.js",
    "/_next/static/chunks/app/layout-3d0cf70584b929a9.js",
    "/_next/static/chunks/44530001-06361d81d0d308be.js",
    "/_next/static/chunks/c15bf2b0-98325d36a1a29411.js",
    "/_next/static/chunks/3953-53c529af9c813e1c.js",
    "/_next/static/chunks/5911-eb39648c6aa7dcdc.js",
    "/_next/static/chunks/9931-9fd2b8af4466bcd9.js",
    "/_next/static/chunks/5872-51d1b77308e83427.js",
    "/_next/static/chunks/5669-77d9ca8d2acf44a3.js",
    "/_next/static/chunks/app/page-9024683cb3851e4c.js",
    "/_next/static/chunks/polyfills-42372ed130431b0a.js",
    "/_next/static/chunks/webpack-59ebd1f44e204ed8.js",
    # Dynamic chunks from webpack manifest
    "/_next/static/chunks/bc98253f.28485b6529a1b8e7.js",
    "/_next/static/chunks/704.569413513205e4e7.js",
    "/_next/static/chunks/768.c14af6cc36ecda36.js",
    "/_next/static/chunks/1992.3ab47769f7c826e3.js",
    "/_next/static/chunks/2485.e31fe94b382a2ef0.js",
    "/_next/static/chunks/2517.d8efb64168cee224.js",
    "/_next/static/chunks/2885.f23ffbe69618d232.js",
    "/_next/static/chunks/164f4fb6.27d490fe23ffa262.js",
    "/_next/static/chunks/4233.9ebd217175818b45.js",
    "/_next/static/chunks/ad2866b8.71091ba302e684b4.js",
    "/_next/static/chunks/4360.fb8bc8979846d028.js",
    "/_next/static/chunks/2f0b94e8.c03c597ed708d982.js",
    "/_next/static/chunks/5902.57b50b3397fc4d7b.js",
    "/_next/static/chunks/8385.b6176812204c9f79.js",
    "/_next/static/chunks/9106.35f0e0ff0ed5a47a.js",
    # CSS files
    "/_next/static/css/58674fb7950da55a.css",
    "/_next/static/css/8c1ceca851ae029e.css",
    "/_next/static/css/184cfac8c54b4486.css",
    "/_next/static/css/a95bf5a24b725f1c.css"
]

found_media = set()
found_audio = set()
found_images = set()
found_fonts = set()
found_other = set()

for c in chunks_to_download:
    url = base_url + c
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            text = r.text
            # Find audio/video extensions
            media_matches = re.findall(r'["\']([^"\']+\.(?:mp3|wav|ogg|aac|m4a|mp4|webm|mov|glb|gltf|bin))["\']', text, re.IGNORECASE)
            for m in media_matches:
                if 'mp3' in m or 'wav' in m or 'ogg' in m:
                    found_audio.add(m)
                else:
                    found_media.add(m)
            # Find image extensions
            img_matches = re.findall(r'["\']([^"\']+\.(?:webp|png|jpg|jpeg|gif|svg|ico))["\']', text, re.IGNORECASE)
            for img in img_matches:
                if not img.startswith('data:'):
                    found_images.add(img)
            # Find font extensions
            font_matches = re.findall(r'["\']([^"\']+\.(?:woff2|woff|ttf|otf))["\']', text, re.IGNORECASE)
            for f in font_matches:
                found_fonts.add(f)
            # Find assets path
            assets = re.findall(r'(/assets/[^"\'\s)]+)', text)
            for a in assets:
                found_other.add(a)
    except Exception as e:
        print(f"Error {c}: {e}")

print("FOUND AUDIO:", found_audio)
print("FOUND MEDIA:", found_media)
print(f"FOUND IMAGES count: {len(found_images)}")
for im in sorted(found_images)[:20]:
    print("  img:", im)
print(f"FOUND FONTS ({len(found_fonts)}):", found_fonts)
print(f"FOUND OTHER ASSETS ({len(found_other)}):", found_other)
