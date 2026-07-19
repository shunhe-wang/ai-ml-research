from collections import Counter

from rule_carryover.domain import RuleSchema
from rule_carryover.generation import generate_balanced_cases
from rule_carryover.solvers import solve_declarative, solve_imperative


def test_generator_is_deterministic_balanced_and_solver_checked() -> None:
    schema = RuleSchema.benefit(
        schema_id="benefit-generation-example",
        income_ceiling=2_000,
        residency_months=12,
        caregiver_income_extension=300,
        caregiver_residency_reduction=2,
    )

    first = generate_balanced_cases(schema, per_label=8, seed=20260717)
    second = generate_balanced_cases(schema, per_label=8, seed=20260717)

    assert first == second
    assert len(first) == 16
    assert len({case.case_id for case in first}) == 16

    decisions = [solve_imperative(schema, case) for case in first]
    assert Counter(decision.label for decision in decisions) == {"APPROVE": 8, "DENY": 8}
    assert [solve_declarative(schema, case) for case in first] == decisions


def test_generator_changes_cases_when_seed_changes() -> None:
    schema = RuleSchema.permit(
        schema_id="permit-generation-example",
        minimum_safety_score=7,
    )

    first = generate_balanced_cases(schema, per_label=5, seed=1)
    second = generate_balanced_cases(schema, per_label=5, seed=2)

    assert first != second


def test_permit_generator_supports_the_plumbing_sample_size() -> None:
    schema = RuleSchema.permit(
        schema_id="permit-support-example",
        minimum_safety_score=7,
    )

    cases = generate_balanced_cases(schema, per_label=24, seed=2026071702)

    decisions = [solve_imperative(schema, case) for case in cases]
    assert Counter(decision.label for decision in decisions) == {"APPROVE": 24, "DENY": 24}
