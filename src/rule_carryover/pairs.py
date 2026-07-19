from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass

from rule_carryover.domain import Case, FactValue, RuleSchema
from rule_carryover.solvers import solve_declarative, solve_imperative


@dataclass(frozen=True)
class CounterfactualPair:
    pair_id: str
    positive: Case
    negative: Case
    changed_fact: str


type FactSignature = tuple[tuple[str, FactValue], ...]


def fact_signature(case: Case) -> FactSignature:
    return tuple(sorted(case.facts.items()))


def _benefit_pair(
    schema: RuleSchema,
    *,
    pair_id: str,
    rng: random.Random,
) -> CounterfactualPair:
    ceiling = schema.parameters["income_ceiling"]
    residency = schema.parameters["residency_months"] + rng.randint(0, 8)
    margin = rng.randint(1, min(500, max(1, ceiling)))
    common = {
        "residency_months": residency,
        "has_sanction": False,
        "is_caregiver": False,
    }
    return CounterfactualPair(
        pair_id=pair_id,
        positive=Case(
            case_id=f"{pair_id}-positive",
            world="benefit",
            facts={"income": ceiling - margin} | common,
        ),
        negative=Case(
            case_id=f"{pair_id}-negative",
            world="benefit",
            facts={"income": ceiling + margin} | common,
        ),
        changed_fact="income",
    )


def _permit_pair(
    schema: RuleSchema,
    *,
    pair_id: str,
    rng: random.Random,
) -> CounterfactualPair:
    minimum = schema.parameters["minimum_safety_score"]
    positive_margin = rng.randint(1, 50)
    common = {
        "fee_paid": True,
        "has_insurance": True,
        "restricted_zone": False,
        "emergency_waiver": False,
        "fraud_flag": False,
    }
    return CounterfactualPair(
        pair_id=pair_id,
        positive=Case(
            case_id=f"{pair_id}-positive",
            world="permit",
            facts={"safety_score": minimum + positive_margin} | common,
        ),
        negative=Case(
            case_id=f"{pair_id}-negative",
            world="permit",
            facts={"safety_score": minimum - positive_margin} | common,
        ),
        changed_fact="safety_score",
    )


def generate_counterfactual_pairs(
    schema: RuleSchema,
    *,
    count: int,
    seed: int,
    excluded_fact_signatures: set[FactSignature] | None = None,
    pair_filter: Callable[[CounterfactualPair], bool] | None = None,
) -> tuple[CounterfactualPair, ...]:
    """Generate seeded one-fact twins with opposite solver labels."""
    if count <= 0:
        raise ValueError("count must be positive")
    rng = random.Random(seed)
    pairs: list[CounterfactualPair] = []
    seen: set[FactSignature] = set()
    excluded = excluded_fact_signatures or set()
    attempts = 0
    while len(pairs) < count and attempts < count * 100:
        pair_id = f"{schema.schema_id}-pair-s{seed}-{len(pairs):04d}"
        pair = (
            _benefit_pair(schema, pair_id=pair_id, rng=rng)
            if schema.world == "benefit"
            else _permit_pair(schema, pair_id=pair_id, rng=rng)
        )
        positive_key = fact_signature(pair.positive)
        negative_key = fact_signature(pair.negative)
        attempts += 1
        if (
            positive_key in seen
            or negative_key in seen
            or positive_key in excluded
            or negative_key in excluded
        ):
            continue
        seen.update((positive_key, negative_key))
        positive = solve_imperative(schema, pair.positive)
        negative = solve_imperative(schema, pair.negative)
        if positive.label != "APPROVE" or negative.label != "DENY":
            raise AssertionError("counterfactual pair does not flip the decision")
        if positive != solve_declarative(schema, pair.positive):
            raise AssertionError("positive pair solver disagreement")
        if negative != solve_declarative(schema, pair.negative):
            raise AssertionError("negative pair solver disagreement")
        if pair_filter is not None and not pair_filter(pair):
            continue
        pairs.append(pair)
    if len(pairs) != count:
        raise RuntimeError(f"could generate only {len(pairs)} unique pairs")
    return tuple(pairs)
