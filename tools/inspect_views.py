import requests

code = requests.get("https://www.innonitrkl.com/_next/static/chunks/app/page-9024683cb3851e4c.js").text

idx = code.find("schedule:{")
if idx != -1:
    print(code[idx-300:idx+600])
