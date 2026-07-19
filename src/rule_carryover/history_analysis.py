from __future__ import annotations

import json
import math
import random
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, cast


@dataclass(frozen=True)
class HistoryAnalysis:
    targets: int
    paired_valid: int
    positive_schema_valid: int
    negative_schema_valid: int
    positive_decision_correct: int
    negative_decision_correct: int
    positive_approvals: int
    negative_approvals: int
    positive_only_approve: int
    negative_only_approve: int
    risk_difference_complete_case: float | None
    risk_difference_lower_bound: float
    risk_difference_upper_bound: float
    exact_one_sided_p: float | None
    exact_two_sided_p: float | None
    bootstrap_ci_lower: float | None
    bootstrap_ci_upper: float | None
    bootstrap_replications: int
    bootstrap_seed: int


def _binomial_upper_tail(successes: int, trials: int) -> float:
    return float(sum(math.comb(trials, value) for value in range(successes, trials + 1))) / float(
        2**trials
    )


def _binomial_lower_tail(successes: int, trials: int) -> float:
    return float(sum(math.comb(trials, value) for value in range(successes + 1))) / float(2**trials)


def _percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    index = round(probability * (len(ordered) - 1))
    return ordered[index]


def analyze_history_log(
    path: Path,
    *,
    bootstrap_replications: int,
    seed: int,
) -> HistoryAnalysis:
    return analyze_history_logs(
        (path,),
        bootstrap_replications=bootstrap_replications,
        seed=seed,
    )


def analyze_history_logs(
    paths: Sequence[Path],
    *,
    bootstrap_replications: int,
    seed: int,
) -> HistoryAnalysis:
    if bootstrap_replications <= 0:
        raise ValueError("bootstrap_replications must be positive")
    final_by_cell: dict[str, dict[str, Any]] = {}
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                payload = cast(dict[str, Any], json.loads(line))
                final_by_cell[str(payload["cell_id"])] = payload

    arms: dict[str, dict[str, tuple[Literal["APPROVE", "DENY"] | None, bool]]] = {}
    schema_valid = {"positive": 0, "negative": 0}
    decision_correct = {"positive": 0, "negative": 0}
    for cell_id, payload in final_by_cell.items():
        parts = cell_id.split("|")
        if len(parts) < 4 or parts[-2] not in {"positive", "negative"}:
            continue
        target = parts[0]
        streak = parts[-2]
        record = cast(dict[str, Any], payload["record"])
        score_raw = record.get("score")
        parsed: Literal["APPROVE", "DENY"] | None = None
        correct = False
        if score_raw is not None:
            score = cast(dict[str, Any], score_raw)
            if score.get("schema_valid") is True:
                schema_valid[streak] += 1
            parsed_raw = score.get("parsed_decision")
            if parsed_raw in {"APPROVE", "DENY"}:
                parsed = cast(Literal["APPROVE", "DENY"], parsed_raw)
            correct = score.get("decision_correct") is True
            decision_correct[streak] += int(correct)
        arms.setdefault(target, {})[streak] = (parsed, correct)

    targets = len(arms)
    if targets == 0:
        raise ValueError("no directional history cells found")
    positive_approvals = sum(
        values.get("positive", (None, False))[0] == "APPROVE" for values in arms.values()
    )
    negative_approvals = sum(
        values.get("negative", (None, False))[0] == "APPROVE" for values in arms.values()
    )
    positive_observed = sum(
        values.get("positive", (None, False))[0] is not None for values in arms.values()
    )
    negative_observed = sum(
        values.get("negative", (None, False))[0] is not None for values in arms.values()
    )
    paired_differences = []
    for values in arms.values():
        positive = values.get("positive", (None, False))[0]
        negative = values.get("negative", (None, False))[0]
        if positive is not None and negative is not None:
            paired_differences.append(int(positive == "APPROVE") - int(negative == "APPROVE"))

    positive_only = sum(value == 1 for value in paired_differences)
    negative_only = sum(value == -1 for value in paired_differences)
    discordant = positive_only + negative_only
    complete_case = None
    one_sided = None
    two_sided = None
    bootstrap_lower = None
    bootstrap_upper = None
    if paired_differences:
        complete_case = sum(paired_differences) / len(paired_differences)
        rng = random.Random(seed)
        bootstrap = [
            sum(rng.choice(paired_differences) for _ in paired_differences)
            / len(paired_differences)
            for _ in range(bootstrap_replications)
        ]
        bootstrap_lower = _percentile(bootstrap, 0.025)
        bootstrap_upper = _percentile(bootstrap, 0.975)
    if discordant:
        one_sided = _binomial_upper_tail(positive_only, discordant)
        two_sided = min(
            1.0,
            2
            * min(
                _binomial_lower_tail(positive_only, discordant),
                _binomial_upper_tail(positive_only, discordant),
            ),
        )

    return HistoryAnalysis(
        targets=targets,
        paired_valid=len(paired_differences),
        positive_schema_valid=schema_valid["positive"],
        negative_schema_valid=schema_valid["negative"],
        positive_decision_correct=decision_correct["positive"],
        negative_decision_correct=decision_correct["negative"],
        positive_approvals=positive_approvals,
        negative_approvals=negative_approvals,
        positive_only_approve=positive_only,
        negative_only_approve=negative_only,
        risk_difference_complete_case=complete_case,
        risk_difference_lower_bound=(
            positive_approvals / targets
            - (negative_approvals + targets - negative_observed) / targets
        ),
        risk_difference_upper_bound=(
            (positive_approvals + targets - positive_observed) / targets
            - negative_approvals / targets
        ),
        exact_one_sided_p=one_sided,
        exact_two_sided_p=two_sided,
        bootstrap_ci_lower=bootstrap_lower,
        bootstrap_ci_upper=bootstrap_upper,
        bootstrap_replications=bootstrap_replications,
        bootstrap_seed=seed,
    )
