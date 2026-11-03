import os
import sys
import requests
from urllib.parse import urlparse, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed

IMAGEKIT_FILE = r"D:\NITR\all_imagekit_urls.txt"
DEST_ROOT = r"D:\NITR\public\imagekit"

with open(IMAGEKIT_FILE, 'r', encoding='utf-8') as f:
    urls = [line.strip() for line in f if line.strip()]

print(f"Total image URLs to download: {len(urls)}")

def download_img(url):
    parsed = urlparse(url)
    # clean path
    rel_path = parsed.path.lstrip('/')
    # e.g. b4kmkfgaod/innovision/gallery/archive/innovision-09.webp
    local_path = os.path.join(DEST_ROOT, rel_path.replace('/', os.sep))
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        return url, True, 0
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(r.content)
            return url, True, len(r.content)
        else:
            return url, False, r.status_code
    except Exception as e:
        return url, False, str(e)

success = 0
failed = 0
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(download_img, url): url for url in urls}
    for future in as_completed(futures):
        url, ok, size_or_err = future.result()
        if ok:
            success += 1
            if success % 20 == 0:
                print(f"Progress: {success}/{len(urls)} downloaded...")
        else:
            failed += 1
            print(f"Failed {url}: {size_or_err}")

print(f"\nFinished! Success: {success}, Failed: {failed}")
