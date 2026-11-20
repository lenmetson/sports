import requests
from icalendar import Calendar

with open("feeds.txt") as f:
    urls = [u.strip() for u in f if u.strip() and not u.startswith("#")]

out = Calendar()
out.add("prodid", "-//sports-calendar//")
out.add("version", "2.0")
out.add("x-wr-calname", "Sports")
seen = set()

for url in urls:
    r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
    if not r.text.lstrip().startswith("BEGIN:VCALENDAR"):
        print(f"Skipped {url}")
        continue
    cal = Calendar.from_ical(r.content)
    for c in cal.subcomponents:
        key = c.get("TZID") if c.name == "VTIMEZONE" else c.get("UID")
        if c.name in ("VTIMEZONE", "VEVENT") and key not in seen:
            seen.add(key)
            out.add_component(c)

with open("public/sports.ics", "wb") as f:
    f.write(out.to_ical())