import json
from datetime import datetime
from pathlib import Path

AUDIT_FILE = Path("audit_log.json")

def log_decision(prompt: str, result: dict):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "result": result
    }
    data = []
    if AUDIT_FILE.exists():
        try:
            data = json.loads(AUDIT_FILE.read_text())
        except Exception:
            data = []
    data.append(record)
    AUDIT_FILE.write_text(json.dumps(data, indent=2))
