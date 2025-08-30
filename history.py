import json
import os
from datetime import datetime

HISTORY_DIR = "history"
os.makedirs(HISTORY_DIR, exist_ok=True)

def save_history(file_name: str, record: dict):
    path = os.path.join(HISTORY_DIR, file_name)
    data = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    record["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data.append(record)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_history(file_name: str):
    path = os.path.join(HISTORY_DIR, file_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
