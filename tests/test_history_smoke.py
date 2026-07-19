import json
from collections.abc import Mapping, Sequence
from pathlib import Path

import pytest

from rule_carryover.case_set import FrozenCaseSet, freeze_case_set
from rule_carryover.domain import RuleSchema
from rule_carryover.generation import generate_balanced_cases
from rule_carryover.histories import HistorySequence, build_directional_history_bank
from rule_carryover.history_smoke import run_directional_history_smoke
from rule_carryover.pairs import fact_signature, generate_counterfactual_pairs
from rule_carryover.providers import (
    DecodingValue,
    ProviderCompletion,
    ScriptedProvider,
    TransportError,
)
from rule_carryover.rendering import Channel, Message, whitespace_tokens


def _inputs() -> tuple[FrozenCaseSet, tuple[HistorySequence, ...]]:
    schema = RuleSchema.permit(schema_id="history-smoke", minimum_safety_score=7)
    case_set = freeze_case_set(schema, generate_balanced_cases(schema, per_label=2, seed=21))
    pairs = generate_counterfactual_pairs(
        schema,
        count=8,
        seed=22,
        excluded_fact_signatures={fact_signature(item.case) for item in case_set.items},
    )
    histories = build_directional_history_bank(schema, pairs, sets=2, horizon=3, seed=23)
    return case_set, histories


class _ArmEchoProvider:
    def complete(
        self,
        *,
        system_block: str,
        messages: Sequence[Message],
        model_id: str,
        decoding: Mapping[str, DecodingValue],
    ) -> ProviderCompletion:
        del system_block, model_id, decoding
        assistant_records = [message.content for message in messages if message.role == "assistant"]
        positive = all('"decision":"APPROVE"' in record for record in assistant_records)
        decision = "APPROVE" if positive else "DENY"
        rule_id = "general_permit" if positive else "permit_default_deny"
        return ProviderCompletion(
            raw_response=json.dumps({"decision": decision, "rule_id": rule_id, "margin": 0})
        )


def test_directional_smoke_executes_token_matched_twins_and_estimates_difference(
    tmp_path: Path,
) -> None:
    case_set, histories = _inputs()
    summary = run_directional_history_smoke(
        case_set=case_set,
        histories=histories,
        provider=_ArmEchoProvider(),
        provider_name="scripted",
        model_id="scripted/model@v1",
        run_id="history-run",
        log_path=tmp_path / "executions.jsonl",
        max_tokens=64,
        token_counter=whitespace_tokens,
        request_token_counter=lambda request: whitespace_tokens(request.canonical_json()),
        schedule_seed=24,
        limit=2,
    )

    assert summary.targets == 2
    assert summary.executions == 4
    assert summary.attempts == 4
    assert summary.token_matched_pairs == 2
    assert summary.schema_valid == 4
    assert summary.paired_valid == 2
    assert summary.positive_approvals == 2
    assert summary.negative_approvals == 0
    assert summary.directional_risk_difference_complete_case == 1.0
    assert summary.directional_risk_difference_lower_bound == 1.0
    assert summary.directional_risk_difference_upper_bound == 1.0
    records = [
        json.loads(line)
        for line in (tmp_path / "executions.jsonl").read_text().splitlines()
    ]
    assert len(records) == 4
    assert {record["gold"]["label"] for record in records} == {"APPROVE", "DENY"}
    assert all(
        not message["content"].endswith(" x")
        for record in records
        for message in record["request"]["messages"]
    )


def test_directional_smoke_counts_malformed_refusal_and_transport_failures(
    tmp_path: Path,
) -> None:
    case_set, histories = _inputs()
    valid = json.dumps(
        {"decision": "APPROVE", "rule_id": "general_permit", "margin": 0}
    )
    responses = [
        valid,
        "not json",
        "I cannot decide this case",
        TransportError("injected outage"),
        valid,
        valid,
        valid,
        valid,
    ]

    summary = run_directional_history_smoke(
        case_set=case_set,
        histories=histories,
        provider=ScriptedProvider(responses),
        provider_name="scripted",
        model_id="scripted/model@v1",
        run_id="failure-run",
        log_path=tmp_path / "failures.jsonl",
        max_tokens=64,
        token_counter=whitespace_tokens,
        request_token_counter=lambda request: whitespace_tokens(request.canonical_json()),
        schedule_seed=25,
    )

    assert summary.schema_valid == 5
    assert summary.refusals == 1
    assert summary.transport_errors == 1
    assert summary.unresolved_transport_executions == 1
    assert summary.paired_valid < summary.targets
    assert summary.directional_risk_difference_lower_bound <= (
        summary.directional_risk_difference_complete_case or 0.0
    )
    assert summary.directional_risk_difference_upper_bound >= (
        summary.directional_risk_difference_complete_case or 0.0
    )


def test_directional_smoke_rejects_target_history_fact_overlap(tmp_path: Path) -> None:
    case_set, histories = _inputs()
    overlapping_case_set = freeze_case_set(
        case_set.schema,
        [histories[0].records[0].case],
    )

    with pytest.raises(ValueError, match="target and history fact pools overlap"):
        run_directional_history_smoke(
            case_set=overlapping_case_set,
            histories=histories,
            provider=ScriptedProvider([]),
            provider_name="scripted",
            model_id="scripted/model@v1",
            run_id="overlap-run",
            log_path=tmp_path / "overlap.jsonl",
            max_tokens=64,
            token_counter=whitespace_tokens,
            request_token_counter=lambda request: whitespace_tokens(request.canonical_json()),
            schedule_seed=26,
        )


def test_directional_smoke_retries_transport_and_links_attempts(tmp_path: Path) -> None:
    case_set, histories = _inputs()
    valid = '{"decision":"APPROVE","rule_id":"general_permit","margin":0}'
    log_path = tmp_path / "retry-history.jsonl"

    summary = run_directional_history_smoke(
        case_set=case_set,
        histories=histories,
        provider=ScriptedProvider([TransportError("temporary"), valid, valid]),
        provider_name="scripted",
        model_id="scripted/model@v1",
        run_id="retry-history-run",
        log_path=log_path,
        max_tokens=64,
        token_counter=whitespace_tokens,
        request_token_counter=lambda request: whitespace_tokens(request.canonical_json()),
        schedule_seed=27,
        limit=1,
        max_transport_retries=1,
    )

    records = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert summary.executions == 2
    assert summary.attempts == 3
    assert summary.transport_errors == 1
    assert summary.unresolved_transport_executions == 0
    assert records[1]["parent_attempt_id"] == records[0]["attempt_id"]


def test_directional_smoke_renders_explicit_outcome_code_channel(tmp_path: Path) -> None:
    case_set, histories = _inputs()
    valid = '{"decision":"APPROVE","rule_id":"general_permit","margin":0}'
    log_path = tmp_path / "coded-history.jsonl"

    summary = run_directional_history_smoke(
        case_set=case_set,
        histories=histories,
        provider=ScriptedProvider([valid, valid]),
        provider_name="scripted",
        model_id="scripted/model@v1",
        run_id="coded-history-run",
        log_path=log_path,
        max_tokens=64,
        token_counter=whitespace_tokens,
        request_token_counter=lambda request: whitespace_tokens(request.canonical_json()),
        schedule_seed=28,
        channel=Channel.OUTCOME_CODE,
        limit=1,
    )

    records = [json.loads(line) for line in log_path.read_text().splitlines()]
    assistant_messages = {
        message["content"]
        for record in records
        for message in record["request"]["messages"]
        if message["role"] == "assistant"
    }
    assert summary.executions == 2
    assert assistant_messages == {"OUTCOME_CODE=0", "OUTCOME_CODE=1"}
