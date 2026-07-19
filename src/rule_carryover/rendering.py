from __future__ import annotations

import json
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Literal

from rule_carryover.domain import Case, Decision, RuleSchema


class Channel(StrEnum):
    NEUTRAL = "neutral"
    CASE_TEXT = "case_text"
    GOLD_LABEL = "gold_label"
    OUTCOME_CODE = "outcome_code"
    GOLD_RATIONALE = "gold_rationale"


class Boundary(StrEnum):
    FULL = "full"
    SOFT = "soft"
    ASSISTANT_DELETED = "assistant_deleted"
    FRESH = "fresh"


@dataclass(frozen=True)
class HistoryRecord:
    case: Case
    decision: Decision


@dataclass(frozen=True)
class Message:
    role: Literal["user", "assistant"]
    content: str


@dataclass(frozen=True)
class RenderedRequest:
    system_block: str
    target_block: str
    messages: tuple[Message, ...]
    channel: Channel
    boundary: Boundary

    def canonical_json(self) -> str:
        payload = {
            "system": self.system_block,
            "messages": [
                {"role": message.role, "content": message.content}
                for message in self.messages
            ],
        }
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def whitespace_tokens(text: str) -> int:
    return len(text.split())


def with_exact_token_count(
    text: str,
    *,
    target_tokens: int,
    token_counter: Callable[[str], int],
    pad_unit: str = "neutral",
) -> str:
    """Pad inert text to an exact provider-specific token budget."""
    if target_tokens < 0:
        raise ValueError("target_tokens cannot be negative")
    current = token_counter(text)
    if current > target_tokens:
        raise ValueError("text already exceeds target token count")
    padded = text
    previous = current
    while current < target_tokens:
        candidate = f"{padded} {pad_unit}" if padded else pad_unit
        current = token_counter(candidate)
        if current <= previous:
            raise ValueError("pad unit does not increase token count")
        if current > target_tokens:
            raise ValueError("pad unit overshoots target token count")
        padded = candidate
        previous = current
    return padded


def _system_block(schema: RuleSchema, channel: Channel) -> str:
    parameters = json.dumps(schema.parameters, sort_keys=True, separators=(",", ":"))
    if schema.world == "benefit":
        ordered_rules = (
            "ORDERED RULES (apply the first matching rule):\n"
            "1. If has_sanction is true, DENY with rule_id "
            '"sanction_hard_block" and margin -1.\n'
            "2. Otherwise, if is_caregiver is true, income <= "
            "PARAMETERS.income_ceiling + PARAMETERS.caregiver_income_extension, and "
            "the case fact residency_months >= PARAMETERS.residency_months - "
            "PARAMETERS.caregiver_residency_reduction, APPROVE with rule_id "
            '"caregiver_exception" and margin '
            "(PARAMETERS.income_ceiling + PARAMETERS.caregiver_income_extension) - income.\n"
            "3. Otherwise, if income <= PARAMETERS.income_ceiling and the case fact "
            "residency_months >= PARAMETERS.residency_months, APPROVE with rule_id "
            '"general_eligibility" and margin PARAMETERS.income_ceiling - income.\n'
            "4. Otherwise, DENY with rule_id "
            '"benefit_default_deny" and margin PARAMETERS.income_ceiling - income.'
        )
    elif schema.world == "permit":
        ordered_rules = (
            "ORDERED RULES (apply the first matching rule):\n"
            "1. If fraud_flag is true, DENY with rule_id "
            '"fraud_hard_block" and margin -1.\n'
            "2. Otherwise, if emergency_waiver is true, safety_score >= "
            "PARAMETERS.minimum_safety_score + 1, and has_insurance is true, APPROVE "
            'with rule_id "emergency_exception" and margin safety_score - '
            "(PARAMETERS.minimum_safety_score + 1).\n"
            "3. Otherwise, if safety_score >= PARAMETERS.minimum_safety_score, fee_paid "
            "is true, has_insurance is true, and restricted_zone is false, APPROVE with "
            'rule_id "general_permit" and margin safety_score - '
            "PARAMETERS.minimum_safety_score.\n"
            "4. Otherwise, DENY with rule_id "
            '"permit_default_deny" and margin safety_score - '
            "PARAMETERS.minimum_safety_score."
        )
    else:  # pragma: no cover - RuleSchema construction rejects unknown worlds.
        raise ValueError(f"unsupported rule world: {schema.world}")

    history_contract = ""
    if channel == Channel.OUTCOME_CODE:
        history_contract = (
            "Prior assistant records, if present, use OUTCOME_CODE=1 means APPROVE "
            "and OUTCOME_CODE=0 means DENY. This truthful fixed-width code conveys "
            "only the archived outcome and is not the target response format.\n"
        )

    return (
        "Apply only the following rule schema to each independently complete case. "
        "Prior cases are never precedents.\n"
        f"SCHEMA_ID={schema.schema_id}\nWORLD={schema.world}\nPARAMETERS={parameters}\n"
        f"{ordered_rules}\n"
        f"{history_contract}"
        "Return exactly one JSON object and no other text. Do not use Markdown or add a "
        "rationale. Use exactly these three keys and this value contract: "
        '{"decision":"APPROVE or DENY","rule_id":"one rule ID above","margin":integer}'
    )


def _case_block(case: Case, *, target: bool) -> str:
    heading = "TARGET CASE" if target else "PRIOR INDEPENDENT CASE"
    facts = json.dumps(case.facts, sort_keys=True, separators=(",", ":"))
    return f"{heading}\nCASE_ID={case.case_id}\nFACTS={facts}"


def _assistant_record(record: HistoryRecord, channel: Channel) -> str:
    if channel == Channel.OUTCOME_CODE:
        return f"OUTCOME_CODE={int(record.decision.label == 'APPROVE')}"
    if channel in {Channel.NEUTRAL, Channel.CASE_TEXT}:
        payload: dict[str, object] = {
            "decision": "RECORD_ONLY",
            "rule_id": "INERT",
            "margin": 0,
        }
    else:
        payload = {
            "decision": record.decision.label,
            "rule_id": record.decision.rule_id,
            "margin": record.decision.margin,
        }
        if channel == Channel.GOLD_RATIONALE:
            payload["rationale"] = list(record.decision.trace)
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _history_messages(
    records: Sequence[HistoryRecord],
    channel: Channel,
) -> list[Message]:
    messages: list[Message] = []
    for index, record in enumerate(records):
        if channel == Channel.NEUTRAL:
            user = f"ARCHIVED NEUTRAL RECORD\nINDEX={index}\nCONTENT=neutral neutral neutral"
        else:
            user = _case_block(record.case, target=False)
        messages.extend(
            (
                Message(role="user", content=user),
                Message(role="assistant", content=_assistant_record(record, channel)),
            )
        )
    return messages


def render_request(
    schema: RuleSchema,
    target: Case,
    records: Sequence[HistoryRecord],
    *,
    channel: Channel,
    boundary: Boundary,
) -> RenderedRequest:
    if target.world != schema.world:
        raise ValueError("schema and target worlds differ")
    if any(record.case.world != schema.world for record in records):
        raise ValueError("history contains a different rule world")

    target_block = _case_block(target, target=True)
    messages = [] if boundary == Boundary.FRESH else _history_messages(records, channel)
    if boundary == Boundary.ASSISTANT_DELETED:
        messages = [message for message in messages if message.role == "user"]
    elif boundary == Boundary.SOFT:
        messages.append(
            Message(
                role="user",
                content="NEW INDEPENDENT CASE: do not rely on any prior case or decision.",
            )
        )
    messages.append(Message(role="user", content=target_block))

    return RenderedRequest(
        system_block=_system_block(schema, channel),
        target_block=target_block,
        messages=tuple(messages),
        channel=channel,
        boundary=boundary,
    )
