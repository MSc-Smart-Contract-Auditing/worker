import json
from src.utils import URL, WorkingDirectory

with open(WorkingDirectory.get() / "config.json", "r") as f:
    config = json.load(f)

WORKER_URL = URL(config["worker_url"])
UI_URL = URL(config["ui_url"])
