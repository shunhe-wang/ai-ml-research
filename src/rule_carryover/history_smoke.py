from __future__ import annotations

import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from rule_carryover.case_set import FrozenCaseSet, select_label_stratified
from rule_carryover.domain import Decision
from rule_carryover.histories import HistorySequence
from rule_carryover.pairs import fact_signature
from rule_carryover.providers import Provider
from rule_carryover.rendering import (
    Boundary,
    Channel,
    RenderedRequest,
    render_request,
)
from rule_carryover.runner import execute_once
from rule_carryover.storage import ExecutionLog, StoredExecution


@dataclass(frozen=True)
class DirectionalSmokeSummary:
    targets: int
    executions: int
    attempts: int
    token_matched_pairs: int
    schema_valid: int
    decision_correct: int
    refusals: int
    transport_errors: int
    unresolved_transport_executions: int
    paired_valid: int
    positive_approvals: int
    negative_approvals: int
    directional_risk_difference_complete_case: float | None
    directional_risk_difference_lower_bound: float
    directional_risk_difference_upper_bound: float


@dataclass(frozen=True)
class _ScheduledCell:
    target_index: int
    streak: Literal["positive", "negative"]
    history_id: str
    request: RenderedRequest
    gold: Decision


def _paired_histories(
    histories: Sequence[HistorySequence],
) -> tuple[tuple[HistorySequence, HistorySequence], ...]:
    by_set: dict[str, dict[str, HistorySequence]] = {}
    for history in histories:
        by_set.setdefault(history.set_id, {})[history.streak] = history
    pairs = []
    for set_id in sorted(by_set):
        variants = by_set[set_id]
        if set(variants) != {"positive", "negative"}:
            raise ValueError(f"history set {set_id} does not have one twin per streak")
        positive = variants["positive"]
        negative = variants["negative"]
        if positive.source_pair_ids != negative.source_pair_ids:
            raise ValueError(f"history set {set_id} does not share source pair IDs")
        pairs.append((positive, negative))
    if not pairs:
        raise ValueError("at least one paired history set is required")
    return tuple(pairs)


def run_directional_history_smoke(
    *,
    case_set: FrozenCaseSet,
    histories: Sequence[HistorySequence],
    provider: Provider,
    provider_name: str,
    model_id: str,
    run_id: str,
    log_path: Path,
    max_tokens: int,
    token_counter: Callable[[str], int],
    request_token_counter: Callable[[RenderedRequest], int],
    schedule_seed: int,
    channel: Channel = Channel.GOLD_LABEL,
    limit: int | None = None,
    max_transport_retries: int = 0,
) -> DirectionalSmokeSummary:
    """Run randomized, token-matched positive/negative history twins."""
    history_pairs = _paired_histories(histories)
    if max_transport_retries < 0:
        raise ValueError("max_transport_retries cannot be negative")
    target_facts = {fact_signature(item.case) for item in case_set.items}
    history_facts = {
        fact_signature(record.case)
        for history in histories
        for record in history.records
    }
    if target_facts & history_facts:
        raise ValueError("target and history fact pools overlap")
    schedule: list[_ScheduledCell] = []
    token_matched_pairs = 0
    items = select_label_stratified(case_set, limit)
    if not items:
        raise ValueError("history smoke requires at least one target")
    for target_index, item in enumerate(items):
        positive_history, negative_history = history_pairs[target_index % len(history_pairs)]
        positive = render_request(
            case_set.schema,
            item.case,
            positive_history.records,
            channel=channel,
            boundary=Boundary.FULL,
        )
        negative = render_request(
            case_set.schema,
            item.case,
            negative_history.records,
            channel=channel,
            boundary=Boundary.FULL,
        )
        if [message.role for message in positive.messages] != [
            message.role for message in negative.messages
        ]:
            raise ValueError("paired history role structures differ")
        if any(
            token_counter(first.content) != token_counter(second.content)
            for first, second in zip(positive.messages, negative.messages, strict=True)
        ):
            raise ValueError(
                "paired history messages are not naturally token matched; regenerate histories"
            )
        if request_token_counter(positive) != request_token_counter(negative):
            raise ValueError(
                "paired full prompts are not naturally token matched; regenerate histories"
            )
        token_matched_pairs += 1
        schedule.extend(
            (
                _ScheduledCell(
                    target_index=target_index,
                    streak="positive",
                    history_id=positive_history.sequence_id,
                    request=positive,
                    gold=item.decision,
                ),
                _ScheduledCell(
                    target_index=target_index,
                    streak="negative",
                    history_id=negative_history.sequence_id,
                    request=negative,
                    gold=item.decision,
                ),
            )
        )

    random.Random(schedule_seed).shuffle(schedule)
    log = ExecutionLog(log_path)
    schema_valid = 0
    decision_correct = 0
    refusals = 0
    transport_errors = 0
    unresolved_transport_executions = 0
    attempts = 0
    arm_decisions: dict[int, dict[str, Literal["APPROVE", "DENY"]]] = {}
    for cell_index, cell in enumerate(schedule):
        cell_id = (
            f"{items[cell.target_index].case.case_id}|"
            f"{cell.history_id}|{cell.streak}|{model_id}"
        )
        parent_attempt_id = None
        final_record = None
        for retry_index in range(max_transport_retries + 1):
            attempt_id = f"{run_id}-c{cell_index:05d}-r{retry_index}"
            record = execute_once(
                provider=provider,
                provider_name=provider_name,
                model_id=model_id,
                request=cell.request,
                gold=cell.gold,
                decoding={"temperature": 0, "max_tokens": max_tokens},
            )
            log.append(
                StoredExecution(
                    run_id=run_id,
                    cell_id=cell_id,
                    attempt_id=attempt_id,
                    parent_attempt_id=parent_attempt_id,
                    request=cell.request,
                    gold=cell.gold,
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
            unresolved_transport_executions += 1
            continue
        assert final_record.score is not None
        schema_valid += int(final_record.score.schema_valid)
        decision_correct += int(final_record.score.decision_correct)
        refusals += int(final_record.score.refusal)
        if final_record.score.parsed_decision is not None:
            arm_decisions.setdefault(cell.target_index, {})[cell.streak] = (
                final_record.score.parsed_decision
            )

    paired = [
        decisions
        for decisions in arm_decisions.values()
        if set(decisions) == {"positive", "negative"}
    ]
    positive_approvals = sum(
        decisions.get("positive") == "APPROVE" for decisions in arm_decisions.values()
    )
    negative_approvals = sum(
        decisions.get("negative") == "APPROVE" for decisions in arm_decisions.values()
    )
    directional_risk_difference_complete_case = None
    if paired:
        directional_risk_difference_complete_case = sum(
            int(decisions["positive"] == "APPROVE")
            - int(decisions["negative"] == "APPROVE")
            for decisions in paired
        ) / len(paired)
    positive_observed = sum("positive" in decisions for decisions in arm_decisions.values())
    negative_observed = sum("negative" in decisions for decisions in arm_decisions.values())
    targets = len(items)
    lower_bound = positive_approvals / targets - (
        negative_approvals + targets - negative_observed
    ) / targets
    upper_bound = (positive_approvals + targets - positive_observed) / targets - (
        negative_approvals / targets
    )
    return DirectionalSmokeSummary(
        targets=targets,
        executions=len(schedule),
        attempts=attempts,
        token_matched_pairs=token_matched_pairs,
        schema_valid=schema_valid,
        decision_correct=decision_correct,
        refusals=refusals,
        transport_errors=transport_errors,
        unresolved_transport_executions=unresolved_transport_executions,
        paired_valid=len(paired),
        positive_approvals=positive_approvals,
        negative_approvals=negative_approvals,
        directional_risk_difference_complete_case=directional_risk_difference_complete_case,
        directional_risk_difference_lower_bound=lower_bound,
        directional_risk_difference_upper_bound=upper_bound,
    )
