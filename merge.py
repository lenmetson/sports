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
    cal = Calendar.from_ical(requests.get(url, timeout=30).content)
    for c in cal.subcomponents:
        key = c.get("TZID") if c.name == "VTIMEZONE" else c.get("UID")
        if c.name in ("VTIMEZONE", "VEVENT") and key not in seen:
            seen.add(key)
            out.add_component(c)

with open("public/sports.ics", "wb") as f:
    f.write(out.to_ical())