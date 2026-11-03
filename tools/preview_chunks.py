import requests

r_gal = requests.get("https://www.innonitrkl.com/_next/static/chunks/9106.35f0e0ff0ed5a47a.js")
print("Gallery code preview:\n", r_gal.text[:1000])

r_sched = requests.get("https://www.innonitrkl.com/_next/static/chunks/2517.d8efb64168cee224.js")
print("\nSchedule code preview:\n", r_sched.text[:1000])
