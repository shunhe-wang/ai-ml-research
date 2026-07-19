from __future__ import annotations

import random

from rule_carryover.domain import Case, FactValue, RuleSchema
from rule_carryover.solvers import solve_declarative, solve_imperative


class GenerationError(RuntimeError):
    """Raised when a requested balanced sample cannot be generated."""


def _benefit_facts(schema: RuleSchema, rng: random.Random) -> dict[str, FactValue]:
    ceiling = schema.parameters["income_ceiling"]
    residency = schema.parameters["residency_months"]
    return {
        "income": rng.randint(max(0, ceiling - 600), ceiling + 600),
        "residency_months": rng.randint(max(0, residency - 5), residency + 5),
        "has_sanction": rng.random() < 0.15,
        "is_caregiver": rng.random() < 0.35,
    }


def _permit_facts(schema: RuleSchema, rng: random.Random) -> dict[str, FactValue]:
    minimum = schema.parameters["minimum_safety_score"]
    return {
        "safety_score": rng.randint(max(0, minimum - 6), minimum + 10),
        "fee_paid": rng.random() < 0.65,
        "has_insurance": rng.random() < 0.75,
        "restricted_zone": rng.random() < 0.30,
        "emergency_waiver": rng.random() < 0.20,
        "fraud_flag": rng.random() < 0.10,
    }


def generate_balanced_cases(
    schema: RuleSchema,
    *,
    per_label: int,
    seed: int,
    max_attempts: int | None = None,
) -> tuple[Case, ...]:
    """Generate a deterministic label-balanced set and cross-check both solvers."""
    if per_label <= 0:
        raise ValueError("per_label must be positive")
    limit = max_attempts if max_attempts is not None else max(1_000, per_label * 200)
    rng = random.Random(seed)
    selected: dict[str, list[Case]] = {"APPROVE": [], "DENY": []}
    seen: set[tuple[tuple[str, FactValue], ...]] = set()

    for attempt in range(limit):
        facts = (
            _benefit_facts(schema, rng)
            if schema.world == "benefit"
            else _permit_facts(schema, rng)
        )
        fact_key = tuple(sorted(facts.items()))
        if fact_key in seen:
            continue
        seen.add(fact_key)

        case = Case(
            case_id=f"{schema.schema_id}-s{seed}-a{attempt:05d}",
            world=schema.world,
            facts=facts,
        )
        imperative = solve_imperative(schema, case)
        declarative = solve_declarative(schema, case)
        if imperative != declarative:
            raise GenerationError(f"solver disagreement for {case.case_id}")

        bucket = selected[imperative.label]
        if len(bucket) < per_label:
            bucket.append(case)
        if all(len(items) == per_label for items in selected.values()):
            combined = selected["APPROVE"] + selected["DENY"]
            rng.shuffle(combined)
            return tuple(combined)

    counts = {label: len(items) for label, items in selected.items()}
    raise GenerationError(f"could not generate balanced cases in {limit} attempts: {counts}")
