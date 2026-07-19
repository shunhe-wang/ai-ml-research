from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime

from rule_carryover.domain import Decision
from rule_carryover.providers import DecodingValue, Provider, TransportError
from rule_carryover.rendering import RenderedRequest
from rule_carryover.scoring import ResponseScore, score_response


@dataclass(frozen=True)
class RunRecord:
    provider_name: str
    model_id: str
    started_at: str
    completed_at: str
    latency_ms: float
    request_hash: str
    provider_prompt: str | None
    provider_prompt_hash: str | None
    response_hash: str | None
    raw_response: str | None
    provider_request_id: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    score: ResponseScore | None
    transport_error: str | None


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _request_hash(
    *,
    provider_name: str,
    model_id: str,
    request: RenderedRequest,
    decoding: Mapping[str, DecodingValue],
) -> str:
    payload = {
        "provider": provider_name,
        "model_id": model_id,
        "request": json.loads(request.canonical_json()),
        "decoding": dict(decoding),
    }
    canonical = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return _sha256(canonical)


def execute_once(
    *,
    provider: Provider,
    provider_name: str,
    model_id: str,
    request: RenderedRequest,
    gold: Decision,
    decoding: Mapping[str, DecodingValue],
) -> RunRecord:
    started_at = datetime.now(UTC).isoformat()
    started_clock = time.perf_counter()
    request_hash = _request_hash(
        provider_name=provider_name,
        model_id=model_id,
        request=request,
        decoding=decoding,
    )
    try:
        completion = provider.complete(
            system_block=request.system_block,
            messages=request.messages,
            model_id=model_id,
            decoding=decoding,
        )
    except TransportError as error:
        completed_at = datetime.now(UTC).isoformat()
        return RunRecord(
            provider_name=provider_name,
            model_id=model_id,
            started_at=started_at,
            completed_at=completed_at,
            latency_ms=(time.perf_counter() - started_clock) * 1000,
            request_hash=request_hash,
            provider_prompt=None,
            provider_prompt_hash=None,
            response_hash=None,
            raw_response=None,
            provider_request_id=None,
            prompt_tokens=None,
            completion_tokens=None,
            score=None,
            transport_error=str(error),
        )

    raw = completion.raw_response
    completed_at = datetime.now(UTC).isoformat()
    return RunRecord(
        provider_name=provider_name,
        model_id=model_id,
        started_at=started_at,
        completed_at=completed_at,
        latency_ms=(time.perf_counter() - started_clock) * 1000,
        request_hash=request_hash,
        provider_prompt=completion.provider_prompt,
        provider_prompt_hash=completion.provider_prompt_hash,
        response_hash=_sha256(raw),
        raw_response=raw,
        provider_request_id=completion.provider_request_id,
        prompt_tokens=completion.prompt_tokens,
        completion_tokens=completion.completion_tokens,
        score=score_response(raw, gold),
        transport_error=None,
    )
