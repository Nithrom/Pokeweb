"""Auditoría rápida de trainers_db.json (uso local)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
d = json.loads((ROOT / "data" / "trainers_db.json").read_text(encoding="utf-8"))
games = {g["slug"]: g for g in d["games"]}

print(f"{'slug':34} tot gym e4 ch  kah  no_mv empty")
for slug in sorted(games, key=lambda s: (games[s]["gen"], s)):
    trainers = d["trainers"].get(slug, [])
    gyms = sum(1 for t in trainers if t.get("type") == "gym")
    e4 = sum(1 for t in trainers if t.get("type") == "elite4")
    ch = sum(1 for t in trainers if t.get("type") == "champion")
    kah = sum(1 for t in trainers if t.get("type") == "kahuna")
    no_moves = empty_team = 0
    for t in trainers:
        team = t.get("team") or []
        if not team:
            empty_team += 1
        for mon in team:
            if not mon.get("moves"):
                no_moves += 1
    meta = games[slug].get("trainer_count")
    print(
        f"{slug:34} {len(trainers):3} {gyms:3} {e4:2} {ch:2}  {kah:2}  "
        f"{no_moves:4} {empty_team:5}  (meta={meta})"
    )
