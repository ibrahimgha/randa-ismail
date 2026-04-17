from __future__ import annotations

import fnmatch
import json
import sys
from pathlib import Path


def main() -> int:
    payload = load_payload()
    command = extract_command(payload)
    config = load_config()
    patterns = config.get("deny_patterns", [])

    if command and any(fnmatch.fnmatch(command, pattern) for pattern in patterns):
        print(
            json.dumps(
                {
                    "decision": "deny",
                    "reason": f"Blocked by project Codex hook policy: {command}",
                }
            )
        )
        return 0

    print(json.dumps({"decision": "allow"}))
    return 0


def load_payload() -> dict:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}


def extract_command(payload: dict) -> str:
    for key in ("command", "cmd", "tool_input", "raw"):
        value = payload.get(key)
        if isinstance(value, str):
            return value.strip()
    if isinstance(payload.get("tool_input"), dict):
        nested = payload["tool_input"]
        for key in ("command", "cmd"):
            value = nested.get(key)
            if isinstance(value, str):
                return value.strip()
    return ""


def load_config() -> dict:
    hooks_json = Path(__file__).resolve().parents[1] / "hooks.json"
    try:
        return json.loads(hooks_json.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}


if __name__ == "__main__":
    raise SystemExit(main())
