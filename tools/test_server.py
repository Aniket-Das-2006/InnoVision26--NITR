import subprocess
import time
import requests
import sys

# Start the server as a subprocess
proc = subprocess.Popen(["node", "server.js"], cwd=r"D:\NITR", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
time.sleep(2)

base = "http://localhost:3000"
tests = [
    # Pages (HTML)
    ("/", 200, "text/html"),
    ("/events", 200, "text/html"),
    ("/events/flagship-events", 200, "text/html"),
    ("/events/standout-events", 200, "text/html"),
    ("/events/main-events", 200, "text/html"),
    ("/events/dts-and-fun-events", 200, "text/html"),
    ("/merch", 200, "text/html"),
    ("/privacy", 200, "text/html"),
    ("/terms", 200, "text/html"),
    ("/robots.txt", 200, "text/plain"),
    ("/sitemap.xml", 200, "xml"),
    # API endpoints
    ("/api/events", 200, "application/json"),
    ("/api/gallery", 200, "application/json"),
    ("/api/seats", 200, "application/json"),
    ("/api/auth/session", 200, "application/json"),
    ("/api/ambassador/code", 401, "application/json"),
    # Assets
    ("/assets/asteroid.webp", 200, "image/webp"),
    ("/assets/starfield.svg", 200, "image/svg"),
    ("/assets/beep.mp3", 200, "audio/mpeg"),
    ("/assets/indian-astronaut.webp", 200, "image/webp"),
    # Next static chunks
    ("/_next/static/chunks/webpack-59ebd1f44e204ed8.js", 200, "javascript"),
    ("/_next/static/chunks/app/page-9024683cb3851e4c.js", 200, "javascript"),
    ("/_next/static/chunks/2517.d8efb64168cee224.js", 200, "javascript"),
    ("/_next/static/chunks/9106.35f0e0ff0ed5a47a.js", 200, "javascript"),
    ("/_next/static/chunks/704.569413513205e4e7.js", 200, "javascript"),
    ("/_next/static/chunks/2885.f23ffbe69618d232.js", 200, "javascript"),
    # CSS
    ("/_next/static/css/58674fb7950da55a.css", 200, "text/css"),
    ("/_next/static/css/184cfac8c54b4486.css", 200, "text/css"),
    # Fonts
    ("/_next/static/media/49eec060ce8bd0da-s.p.woff2", 200, "font/woff2"),
]

passed = 0
failed = 0

print("=== TESTING LOCAL SERVER ROUTES ===")
for path, expected_status, content_type_snippet in tests:
    url = base + path
    try:
        r = requests.get(url, timeout=5)
        ct = r.headers.get("Content-Type", "")
        if r.status_code == expected_status and content_type_snippet in ct:
            print(f" PASS: {path} -> {r.status_code} ({ct})")
            passed += 1
        else:
            print(f" FAIL: {path} -> Expected {expected_status} ({content_type_snippet}), got {r.status_code} ({ct})")
            failed += 1
    except Exception as e:
        print(f" ERROR: {path} -> {e}")
        failed += 1

# Test RSC requests
print("\n=== TESTING RSC FLIGHT REQUESTS ===")
rsc_tests = [
    ("/", 200),
    ("/events", 200),
    ("/events/flagship-events", 200),
    ("/merch", 200),
]
for path, exp_code in rsc_tests:
    try:
        r = requests.get(base + path, headers={"RSC": "1"}, timeout=5)
        ct = r.headers.get("Content-Type", "")
        if r.status_code == exp_code and "text/x-component" in ct:
            print(f" PASS RSC: {path} -> {r.status_code} ({ct})")
            passed += 1
        else:
            print(f" FAIL RSC: {path} -> {r.status_code} ({ct})")
            failed += 1
    except Exception as e:
        print(f" ERROR RSC: {path} -> {e}")
        failed += 1

proc.terminate()
print(f"\nTOTAL: {passed} PASSED, {failed} FAILED")
if failed > 0:
    sys.exit(1)
