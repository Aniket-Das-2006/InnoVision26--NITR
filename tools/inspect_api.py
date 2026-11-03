import json

try:
    with open(r'D:\NITR\api_events.json', 'r', encoding='utf-8') as f:
        events = json.load(f)
    print("Events type:", type(events), "Count/Keys:", len(events) if isinstance(events, list) else list(events.keys()))
    if isinstance(events, list) and len(events) > 0:
        print("Sample event:", json.dumps(events[0], indent=2)[:500])
except Exception as e:
    print("Events error:", e)

try:
    with open(r'D:\NITR\api_gallery.json', 'r', encoding='utf-8') as f:
        gallery = json.load(f)
    print("Gallery:", gallery)
except Exception as e:
    print("Gallery error:", e)
