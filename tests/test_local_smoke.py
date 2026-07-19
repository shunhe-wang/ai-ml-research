import json
from pathlib import Path

from rule_carryover.case_set import freeze_case_set
from rule_carryover.domain import RuleSchema
from rule_carryover.generation import generate_balanced_cases
from rule_carryover.local_smoke import run_fresh_baseline
from rule_carryover.providers import ScriptedProvider, TransportError


def test_fresh_baseline_runs_from_frozen_cases_and_writes_append_only_records(
    tmp_path: Path,
) -> None:
    schema = RuleSchema.permit(schema_id="smoke-example", minimum_safety_score=7)
    case_set = freeze_case_set(schema, generate_balanced_cases(schema, per_label=1, seed=5))
    responses = [
        json.dumps(
            {
                "decision": item.decision.label,
                "rule_id": item.decision.rule_id,
                "margin": item.decision.margin,
            }
        )
        for item in case_set.items
    ]
    log_path = tmp_path / "executions.jsonl"

    summary = run_fresh_baseline(
        case_set=case_set,
        provider=ScriptedProvider(responses),
        provider_name="scripted",
        model_id="scripted/model@v1",
        run_id="smoke-run",
        log_path=log_path,
        max_tokens=64,
    )

    assert summary.total == 2
    assert summary.attempts == 2
    assert summary.schema_valid == 2
    assert summary.decision_correct == 2
    assert summary.rule_correct == 2
    assert summary.margin_correct == 2
    assert summary.exact_correct == 2
    assert summary.transport_errors == 0
    assert summary.unresolved_transport_targets == 0
    assert len(log_path.read_text().splitlines()) == 2


def test_fresh_baseline_retries_transport_once_and_links_attempts(tmp_path: Path) -> None:
    schema = RuleSchema.permit(schema_id="retry-example", minimum_safety_score=7)
    case_set = freeze_case_set(schema, generate_balanced_cases(schema, per_label=1, seed=8))
    responses: list[str | TransportError] = [TransportError("temporary")]
    responses.extend(
        json.dumps(
            {
                "decision": item.decision.label,
                "rule_id": item.decision.rule_id,
                "margin": item.decision.margin,
            }
        )
        for item in case_set.items
    )
    log_path = tmp_path / "retry-executions.jsonl"

    summary = run_fresh_baseline(
        case_set=case_set,
        provider=ScriptedProvider(responses),
        provider_name="scripted",
        model_id="scripted/model@v1",
        run_id="retry-run",
        log_path=log_path,
        max_tokens=64,
        max_transport_retries=1,
    )

    records = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert summary.attempts == 3
    assert summary.transport_errors == 1
    assert summary.unresolved_transport_targets == 0
    assert records[1]["parent_attempt_id"] == records[0]["attempt_id"]


def test_fresh_baseline_limit_selects_label_stratified_cases(tmp_path: Path) -> None:
    schema = RuleSchema.permit(schema_id="stratified-example", minimum_safety_score=7)
    case_set = freeze_case_set(schema, generate_balanced_cases(schema, per_label=4, seed=9))
    buckets = {
        label: [item for item in case_set.items if item.decision.label == label]
        for label in ("APPROVE", "DENY")
    }
    selected = [buckets[label][index] for index in range(2) for label in buckets]
    responses = [
        json.dumps(
            {
                "decision": item.decision.label,
                "rule_id": item.decision.rule_id,
                "margin": item.decision.margin,
            }
        )
        for item in selected
    ]
    log_path = tmp_path / "stratified-executions.jsonl"

    summary = run_fresh_baseline(
        case_set=case_set,
        provider=ScriptedProvider(responses),
        provider_name="scripted",
        model_id="scripted/model@v1",
        run_id="stratified-run",
        log_path=log_path,
        max_tokens=64,
        limit=4,
    )

    records = [json.loads(line) for line in log_path.read_text().splitlines()]
    assert summary.total == 4
    assert summary.exact_correct == 4
    assert [record["gold"]["label"] for record in records] == [
        "APPROVE",
        "DENY",
        "APPROVE",
        "DENY",
    ]
