from __future__ import annotations

import hashlib
import json
import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Literal

from rule_carryover.domain import RuleSchema
from rule_carryover.pairs import CounterfactualPair
from rule_carryover.rendering import (
    Boundary,
    Channel,
    HistoryRecord,
    RenderedRequest,
    render_request,
)
from rule_carryover.solvers import solve_declarative, solve_imperative


@dataclass(frozen=True)
class HistorySequence:
    sequence_id: str
    set_id: str
    streak: Literal["positive", "negative"]
    source_pair_ids: tuple[str, ...]
    records: tuple[HistoryRecord, ...]


def history_bank_hash(histories: Sequence[HistorySequence]) -> str:
    payload = []
    for history in sorted(histories, key=lambda item: item.sequence_id):
        payload.append(
            {
                "sequence_id": history.sequence_id,
                "set_id": history.set_id,
                "streak": history.streak,
                "source_pair_ids": list(history.source_pair_ids),
                "records": [
                    {
                        "case": {
                            "case_id": record.case.case_id,
                            "world": record.case.world,
                            "facts": dict(record.case.facts),
                        },
                        "decision": {
                            "label": record.decision.label,
                            "rule_id": record.decision.rule_id,
                            "margin": record.decision.margin,
                            "trace": list(record.decision.trace),
                        },
                    }
                    for record in history.records
                ],
            }
        )
    canonical = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()


def pair_is_naturally_token_matched(
    schema: RuleSchema,
    pair: CounterfactualPair,
    token_counter: Callable[[str], int],
    request_token_counter: Callable[[RenderedRequest], int] | None = None,
    *,
    channel: Channel = Channel.GOLD_LABEL,
) -> bool:
    """Accept twins only when native records match without treatment-specific padding."""
    target = pair.positive
    positive = render_request(
        schema,
        target,
        (_record(schema, pair, positive=True),),
        channel=channel,
        boundary=Boundary.FULL,
    )
    negative = render_request(
        schema,
        target,
        (_record(schema, pair, positive=False),),
        channel=channel,
        boundary=Boundary.FULL,
    )
    if [message.role for message in positive.messages] != [
        message.role for message in negative.messages
    ]:
        return False
    if any(
        token_counter(first.content) != token_counter(second.content)
        for first, second in zip(positive.messages, negative.messages, strict=True)
    ):
        return False
    return request_token_counter is None or request_token_counter(
        positive
    ) == request_token_counter(negative)


def _record(schema: RuleSchema, pair: CounterfactualPair, *, positive: bool) -> HistoryRecord:
    case = pair.positive if positive else pair.negative
    imperative = solve_imperative(schema, case)
    declarative = solve_declarative(schema, case)
    if imperative != declarative:
        raise ValueError(f"solver disagreement for history case {case.case_id}")
    return HistoryRecord(case=case, decision=imperative)


def build_directional_history_bank(
    schema: RuleSchema,
    pairs: Sequence[CounterfactualPair],
    *,
    sets: int,
    horizon: int,
    seed: int,
) -> tuple[HistorySequence, ...]:
    """Build positive/negative twin sequences from the same pair assignments."""
    if sets <= 0:
        raise ValueError("sets must be positive")
    if horizon <= 0 or horizon > len(pairs):
        raise ValueError("horizon must be positive and no larger than the pair bank")
    if any(
        pair.positive.world != schema.world or pair.negative.world != schema.world for pair in pairs
    ):
        raise ValueError("pair bank contains a different rule world")

    rng = random.Random(seed)
    sequences = []
    for set_index in range(sets):
        selected = rng.sample(list(pairs), horizon)
        set_id = f"{schema.schema_id}-history-s{seed}-{set_index:04d}"
        pair_ids = tuple(pair.pair_id for pair in selected)
        streak_values: tuple[tuple[Literal["positive", "negative"], bool], ...] = (
            ("positive", True),
            ("negative", False),
        )
        for streak, positive in streak_values:
            records = tuple(_record(schema, pair, positive=positive) for pair in selected)
            sequences.append(
                HistorySequence(
                    sequence_id=f"{set_id}-{streak}",
                    set_id=set_id,
                    streak=streak,
                    source_pair_ids=pair_ids,
                    records=records,
                )
            )
    return tuple(sequences)
