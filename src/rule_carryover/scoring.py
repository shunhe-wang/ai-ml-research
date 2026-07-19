from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Literal

from rule_carryover.domain import Decision

ErrorType = Literal["refusal", "schema_invalid", "decision_error", "rule_error", "margin_error"]


@dataclass(frozen=True)
class ResponseScore:
    schema_valid: bool
    refusal: bool
    parsed_decision: Literal["APPROVE", "DENY"] | None
    decision_correct: bool
    rule_correct: bool
    margin_correct: bool
    error_type: ErrorType | None


_REFUSAL_PATTERNS = (
    re.compile(r"\bi cannot\b", re.IGNORECASE),
    re.compile(r"\bi can't\b", re.IGNORECASE),
    re.compile(r"\bunable to (?:decide|make|provide)\b", re.IGNORECASE),
    re.compile(r"\brefuse\b", re.IGNORECASE),
)


def _is_refusal(raw: str) -> bool:
    return any(pattern.search(raw) for pattern in _REFUSAL_PATTERNS)


def _valid_payload(raw: str) -> dict[str, object] | None:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    required = {"decision", "rule_id", "margin"}
    if set(payload) != required:
        return None
    if payload["decision"] not in {"APPROVE", "DENY"}:
        return None
    if not isinstance(payload["rule_id"], str):
        return None
    margin = payload["margin"]
    if isinstance(margin, bool) or not isinstance(margin, int):
        return None
    return payload


def score_response(raw: str, gold: Decision) -> ResponseScore:
    refusal = _is_refusal(raw)
    payload = _valid_payload(raw)
    if payload is None:
        return ResponseScore(
            schema_valid=False,
            refusal=refusal,
            parsed_decision=None,
            decision_correct=False,
            rule_correct=False,
            margin_correct=False,
            error_type="refusal" if refusal else "schema_invalid",
        )

    parsed = payload["decision"]
    assert parsed in {"APPROVE", "DENY"}
    decision_correct = parsed == gold.label
    rule_correct = payload["rule_id"] == gold.rule_id
    margin_correct = payload["margin"] == gold.margin
    error_type: ErrorType | None = None
    if not decision_correct:
        error_type = "decision_error"
    elif not rule_correct:
        error_type = "rule_error"
    elif not margin_correct:
        error_type = "margin_error"
    return ResponseScore(
        schema_valid=True,
        refusal=refusal,
        parsed_decision=parsed,
        decision_correct=decision_correct,
        rule_correct=rule_correct,
        margin_correct=margin_correct,
        error_type=error_type,
    )


def extract_decision_sensitivity(raw: str) -> Literal["APPROVE", "DENY"] | None:
    """Extract one unambiguous decision for a predeclared sensitivity analysis."""
    labels = {match.group(0).upper() for match in re.finditer(r"\b(?:APPROVE|DENY)\b", raw, re.I)}
    if labels == {"APPROVE"}:
        return "APPROVE"
    if labels == {"DENY"}:
        return "DENY"
    return None
