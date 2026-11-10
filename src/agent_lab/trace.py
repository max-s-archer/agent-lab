"""Local JSONL run traces."""

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path

MAX_TRACE_CHARS = 1000


class JsonlTrace:
    """Append sanitized events for one local run."""

    def __init__(self, directory: Path, secret: str, run_id: str | None = None):
        self.run_id = run_id or uuid.uuid4().hex
        self._secret = secret
        self._sequence = 0
        directory.mkdir(parents=True, exist_ok=True)
        self.path = directory / f"{self.run_id}.jsonl"

    def append(self, event: dict) -> None:
        self._sequence += 1
        record = {
            "run_id": self.run_id,
            "sequence": self._sequence,
            "timestamp": datetime.now(UTC).isoformat(),
            **self._sanitize(event),
        }
        with self.path.open("a", encoding="utf-8") as trace_file:
            trace_file.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _sanitize(self, value):
        if isinstance(value, dict):
            return {
                key: "[REDACTED]" if key.lower() == "authorization" else self._sanitize(item)
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [self._sanitize(item) for item in value]
        if isinstance(value, str):
            redacted = value.replace(self._secret, "[REDACTED]") if self._secret else value
            if len(redacted) > MAX_TRACE_CHARS:
                return redacted[:MAX_TRACE_CHARS] + "...[truncated]"
            return redacted
        return value
