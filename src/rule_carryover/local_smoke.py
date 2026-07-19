from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from rule_carryover.case_set import FrozenCaseSet, select_label_stratified
from rule_carryover.providers import Provider
from rule_carryover.rendering import Boundary, Channel, render_request
from rule_carryover.runner import execute_once
from rule_carryover.storage import ExecutionLog, StoredExecution


@dataclass(frozen=True)
class BaselineSummary:
    total: int
    attempts: int
    schema_valid: int
    decision_correct: int
    rule_correct: int
    margin_correct: int
    exact_correct: int
    refusals: int
    transport_errors: int
    unresolved_transport_targets: int


def run_fresh_baseline(
    *,
    case_set: FrozenCaseSet,
    provider: Provider,
    provider_name: str,
    model_id: str,
    run_id: str,
    log_path: Path,
    max_tokens: int,
    limit: int | None = None,
    max_transport_retries: int = 0,
) -> BaselineSummary:
    """Run a disjoint fresh-context baseline and retain complete execution records."""
    items = select_label_stratified(case_set, limit)
    if max_transport_retries < 0:
        raise ValueError("max_transport_retries cannot be negative")
    log = ExecutionLog(log_path)
    attempts = 0
    schema_valid = 0
    decision_correct = 0
    rule_correct = 0
    margin_correct = 0
    exact_correct = 0
    refusals = 0
    transport_errors = 0
    unresolved_transport_targets = 0
    for index, item in enumerate(items):
        request = render_request(
            case_set.schema,
            item.case,
            (),
            channel=Channel.NEUTRAL,
            boundary=Boundary.FRESH,
        )
        cell_id = f"{item.case.case_id}|fresh|{model_id}"
        parent_attempt_id = None
        final_record = None
        for retry_index in range(max_transport_retries + 1):
            attempt_id = f"{run_id}-t{index:05d}-r{retry_index}"
            record = execute_once(
                provider=provider,
                provider_name=provider_name,
                model_id=model_id,
                request=request,
                gold=item.decision,
                decoding={"temperature": 0, "max_tokens": max_tokens},
            )
            log.append(
                StoredExecution(
                    run_id=run_id,
                    cell_id=cell_id,
                    attempt_id=attempt_id,
                    parent_attempt_id=parent_attempt_id,
                    request=request,
                    gold=item.decision,
                    record=record,
                )
            )
            attempts += 1
            final_record = record
            if record.transport_error is None:
                break
            transport_errors += 1
            parent_attempt_id = attempt_id
        assert final_record is not None
        if final_record.transport_error is not None:
            unresolved_transport_targets += 1
            continue
        assert final_record.score is not None
        schema_valid += int(final_record.score.schema_valid)
        decision_correct += int(final_record.score.decision_correct)
        rule_correct += int(final_record.score.rule_correct)
        margin_correct += int(final_record.score.margin_correct)
        exact_correct += int(
            final_record.score.decision_correct
            and final_record.score.rule_correct
            and final_record.score.margin_correct
        )
        refusals += int(final_record.score.refusal)
    return BaselineSummary(
        total=len(items),
        attempts=attempts,
        schema_valid=schema_valid,
        decision_correct=decision_correct,
        rule_correct=rule_correct,
        margin_correct=margin_correct,
        exact_correct=exact_correct,
        refusals=refusals,
        transport_errors=transport_errors,
        unresolved_transport_targets=unresolved_transport_targets,
    )
