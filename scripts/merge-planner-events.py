#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "schedule.ics"
PLANNER = ROOT / "planner_events.ics"

base = BASE.read_text(encoding="utf-8")
planner = PLANNER.read_text(encoding="utf-8")

def event_blocks(text):
    return re.findall(r"BEGIN:VEVENT\n[\s\S]*?END:VEVENT\n?", text)


# The imported Modern Control lecture slots below are designated experimental
# teaching time. Their user-booked 16:00-17:30 lab events are already included
# in planner_events.ics, so hide only the duplicate generic class entries.
CONFIRMED_LAB_CLASS_UIDS = {
    "230ed1507bb1ced72b1b740edb44a7474e6eabcf",  # 2026-10-13
    "331b624bd6a3fa0d0a5e65f461b818cc76c1f3b4",  # 2026-10-27
}

# Remove previously generated planner events while leaving imported course/exam events untouched.
for block in event_blocks(base):
    if "@chatgpt-planner" in block or any(f"UID:{uid}" in block for uid in CONFIRMED_LAB_CLASS_UIDS):
        base = base.replace(block, "")

new_events = "".join(event_blocks(planner))
if not new_events:
    raise SystemExit("planner_events.ics contains no VEVENT blocks")

marker = "END:VCALENDAR"
idx = base.rfind(marker)
if idx < 0:
    raise SystemExit("schedule.ics is missing END:VCALENDAR")

merged = base[:idx].rstrip() + "\n" + new_events.rstrip() + "\n" + marker + "\n"
BASE.write_text(merged, encoding="utf-8")
print(f"Merged {len(event_blocks(planner))} planner events into schedule.ics")
