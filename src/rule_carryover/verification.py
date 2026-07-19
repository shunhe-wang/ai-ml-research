from __future__ import annotations

import itertools
from collections import Counter
from dataclasses import dataclass

from rule_carryover.domain import Case, RuleSchema
from rule_carryover.solvers import solve_declarative, solve_imperative


@dataclass(frozen=True)
class CrosscheckReport:
    schema_id: str
    checked: int
    label_counts: dict[str, int]
    disagreements: tuple[str, ...]


def _benefit_grid(schema: RuleSchema) -> tuple[Case, ...]:
    ceiling = schema.parameters["income_ceiling"]
    residency = schema.parameters["residency_months"]
    exception_ceiling = ceiling + schema.parameters["caregiver_income_extension"]
    exception_residency = residency - schema.parameters["caregiver_residency_reduction"]
    incomes = sorted({ceiling - 1, ceiling, ceiling + 1, exception_ceiling, exception_ceiling + 1})
    residencies = sorted(
        {exception_residency - 1, exception_residency, residency - 1, residency, residency + 1}
    )
    cases = []
    for index, (income, months, sanction, caregiver) in enumerate(
        itertools.product(incomes, residencies, (False, True), (False, True))
    ):
        cases.append(
            Case(
                case_id=f"{schema.schema_id}-grid-{index:04d}",
                world="benefit",
                facts={
                    "income": income,
                    "residency_months": months,
                    "has_sanction": sanction,
                    "is_caregiver": caregiver,
                },
            )
        )
    return tuple(cases)


def _permit_grid(schema: RuleSchema) -> tuple[Case, ...]:
    minimum = schema.parameters["minimum_safety_score"]
    cases = []
    boolean_values = (False, True)
    combinations = itertools.product(
        (minimum - 1, minimum, minimum + 1, minimum + 2),
        boolean_values,
        boolean_values,
        boolean_values,
        boolean_values,
        boolean_values,
    )
    for index, (score, fee, insurance, restricted, emergency, fraud) in enumerate(combinations):
        cases.append(
            Case(
                case_id=f"{schema.schema_id}-grid-{index:04d}",
                world="permit",
                facts={
                    "safety_score": score,
                    "fee_paid": fee,
                    "has_insurance": insurance,
                    "restricted_zone": restricted,
                    "emergency_waiver": emergency,
                    "fraud_flag": fraud,
                },
            )
        )
    return tuple(cases)


def crosscheck_schema(schema: RuleSchema) -> CrosscheckReport:
    cases = _benefit_grid(schema) if schema.world == "benefit" else _permit_grid(schema)
    labels: Counter[str] = Counter()
    disagreements = []
    for case in cases:
        imperative = solve_imperative(schema, case)
        declarative = solve_declarative(schema, case)
        labels[imperative.label] += 1
        if imperative != declarative:
            disagreements.append(case.case_id)
    return CrosscheckReport(
        schema_id=schema.schema_id,
        checked=len(cases),
        label_counts=dict(labels),
        disagreements=tuple(disagreements),
    )
