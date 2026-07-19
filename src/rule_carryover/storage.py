from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from rule_carryover.domain import Decision
from rule_carryover.rendering import RenderedRequest
from rule_carryover.runner import RunRecord


@dataclass(frozen=True)
class StoredExecution:
    run_id: str
    cell_id: str
    attempt_id: str
    parent_attempt_id: str | None
    request: RenderedRequest
    gold: Decision
    record: RunRecord

    def payload(self) -> dict[str, object]:
        score = asdict(self.record.score) if self.record.score is not None else None
        return {
            "run_id": self.run_id,
            "cell_id": self.cell_id,
            "attempt_id": self.attempt_id,
            "parent_attempt_id": self.parent_attempt_id,
            "request": {
                "system": self.request.system_block,
                "target": self.request.target_block,
                "channel": self.request.channel.value,
                "boundary": self.request.boundary.value,
                "messages": [
                    {"role": message.role, "content": message.content}
                    for message in self.request.messages
                ],
            },
            "gold": asdict(self.gold),
            "record": {
                "provider_name": self.record.provider_name,
                "model_id": self.record.model_id,
                "started_at": self.record.started_at,
                "completed_at": self.record.completed_at,
                "latency_ms": self.record.latency_ms,
                "request_hash": self.record.request_hash,
                "provider_prompt": self.record.provider_prompt,
                "provider_prompt_hash": self.record.provider_prompt_hash,
                "response_hash": self.record.response_hash,
                "raw_response": self.record.raw_response,
                "provider_request_id": self.record.provider_request_id,
                "prompt_tokens": self.record.prompt_tokens,
                "completion_tokens": self.record.completion_tokens,
                "score": score,
                "transport_error": self.record.transport_error,
            },
        }


class ExecutionLog:
    """Append-only JSONL writer with duplicate-attempt protection."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._attempt_ids = self._load_attempt_ids()

    def _load_attempt_ids(self) -> set[str]:
        if not self.path.exists():
            return set()
        attempt_ids = set()
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            payload = json.loads(line)
            attempt_ids.add(str(payload["attempt_id"]))
        return attempt_ids

    def append(self, execution: StoredExecution) -> None:
        if execution.attempt_id in self._attempt_ids:
            raise ValueError(f"duplicate attempt ID: {execution.attempt_id}")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(
            execution.payload(), ensure_ascii=False, separators=(",", ":"), sort_keys=True
        )
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        self._attempt_ids.add(execution.attempt_id)


def append_execution(path: Path, execution: StoredExecution) -> None:
    ExecutionLog(path).append(execution)
