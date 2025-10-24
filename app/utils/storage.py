import json
from pathlib import Path

STATE_FILE = Path("db.json")

def load_state():
    if not STATE_FILE.exists():
        return {"count": 0, "impostor_assigned": False, "character": None, "first_assigned": False}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
